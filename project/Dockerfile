FROM python:3.8

EXPOSE 3111

WORKDIR /techtrends

COPY ./techtrends .

RUN pip install -r requirements.txt
RUN python init_db.py

ENTRYPOINT [ "python","app.py" ]