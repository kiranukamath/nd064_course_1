## ArgoCD Manifests 

Place the ArgoCD manifests in this directory.

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl get po -n argocd
kubectl get svc -n argocd

apply argocd-server-nodeport.yaml

