import sqlite3
import logging, sys

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

connection_count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    app.logger.debug("Connection to the database..")
    global connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    connection_count += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    app.logger.debug(f"Get post {post_id}..")
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    app.logger.debug(f"Getting all posts..")
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.warning(f'Article with id {post_id} not found')
      return render_template('404.html'), 404
    else:
      app.logger.debug(post)
      app.logger.debug(f"Returning post {post_id}: {post['title']}")
      postTitle = post['title']
      app.logger.info(f'Article "{postTitle}" retrieved!')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.debug("/about endpoint reached..")
    app.logger.info(f'About page visited')

    return render_template('about.html')

@app.route('/healthz')
def health():
     app.logger.debug(f" /healthz endpoint reached..")
     return app.response_class(
        response=json.dumps({ 'result': 'OK - healthy' }),
        status=200,
        mimetype='application/json'
    )
    
@app.route('/metrics')
def metrics():
    app.logger.debug(f"/metrics endpoint reached..")
    connection = get_db_connection()
    post_count = connection.execute('SELECT count(1) from posts').fetchone()[0]
    return app.response_class(
        response=json.dumps({
            'post_count': post_count,
            'db_connection_count': connection_count
        }),
        status=200,
        mimetype='application/json'
    )

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    app.logger.debug("/create post endpoint reached..")
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            app.logger.info(f'Article "{title}" created')

            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":   
   # Set logger to handle STDOUT and STDERR
   stdout_handler = logging.StreamHandler(sys.stdout)
   stderr_handler = logging.StreamHandler(sys.stderr)
   handlers = [stderr_handler, stdout_handler]
   logging.basicConfig(
       format='%(levelname)s:%(name)s:%(asctime)s, %(message)s', 
       datefmt='%m/%d/%Y, %H:%M:%S',
       level=logging.DEBUG,
       handlers=handlers)
   app.run(host='0.0.0.0', port='3111')