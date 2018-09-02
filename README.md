# Helm Chart Generator

Small microservice for generate HELM charts. See also [Command-line client](https://github.com/egeneralov/helm-chart-generator-cli).

## QuickStart

    docker run -d --name hcg --rm -p 8080:8080 egeneralov/helm-chart-generator
    wget 127.0.0.1:8080/download/$(curl -d@payload.json 127.0.0.1:8080/generate/)

## Details

- generate json
  - host
  - version
  - image
  - imageTag
  - port
- POST it to /generate/
  - answer will be filename like ${host}-${version}.tar.gz
- GET /download/${filename}
  - answer will be contents

## note for k8s deployment

- create PVC with ReadWriteMany
- apply for current deployment
- scale it, if you have many CI requests



## How to

#### go to local repository

    cd ~/.helm/repository/local/

#### generate chart

    export VERSION=1.0
    hcg --endpoint 178.128.193.32:1234 --host egeneralov.ru --port 8080 --version ${VERSION} --image egeneralov/helm-chart-generator --tag v${VERSION} --save

#### Run systemd helm server

    cat << EOF > /etc/systemd/system/helm.service
    [Unit]
    Description=Helm local repository
    [Service]
    Type=simple
    Restart=always
    WorkingDir=/root/backend/
    Environment=HOME=/root/
    ExecStart=/usr/local/sbin/helm serve
    [Install]
    WantedBy=multi-user.target
    EOF

    systemctl enable helm.service
    systemctl start helm.service

#### verify repository

    root@master:~# helm search | grep local
    local/egeneralov.ru                  	1.0.0        	                            	Helm chart for Kubernetes.                        

#### install chart

    root@master:~# helm install local/egeneralov.ru --name hcg

#### verify installation

    root@master:~# helm status hcg
    LAST DEPLOYED: Sun Sep  2 04:57:16 2018
    NAMESPACE: default
    STATUS: DEPLOYED

    RESOURCES:
    ==> v1/Service
    NAME  TYPE       CLUSTER-IP   EXTERNAL-IP  PORT(S)   AGE
    hcg   ClusterIP  10.0.176.96  <none>       8080/TCP  2m

    ==> v1beta1/Deployment
    NAME  DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
    hcg   1        1        1           1          2m

    ==> v1beta1/Ingress
    NAME  HOSTS          ADDRESS  PORTS  AGE
    hcg   egeneralov.ru  80, 443  2m

    ==> v1alpha1/Certificate
    NAME  AGE
    hcg   2m

    ==> v1/Pod(related)
    NAME                  READY  STATUS   RESTARTS  AGE
    hcg-766b4966c5-scndq  1/1    Running  0         2m

#### generate next version

    export VERSION=1.0.1
    hcg --endpoint 178.128.193.32:1234 --host egeneralov.ru --port 8080 --version ${VERSION} --image egeneralov/helm-chart-generator --tag v${VERSION} --save

#### upgrade chart

    root@master:~# systemctl restart helm
    root@master:~# helm upgrade hcg local/egeneralov.ru

    Release "hcg" has been upgraded. Happy Helming!
    LAST DEPLOYED: Sun Sep  2 05:17:09 2018
    NAMESPACE: default
    STATUS: DEPLOYED

    RESOURCES:
    ==> v1beta1/Deployment
    NAME  DESIRED  CURRENT  UP-TO-DATE  AVAILABLE  AGE
    hcg   1        2        1           0          11m

    ==> v1beta1/Ingress
    NAME  HOSTS          ADDRESS  PORTS  AGE
    hcg   egeneralov.ru  80, 443  11m

    ==> v1alpha1/Certificate
    NAME  AGE
    hcg   11m

    ==> v1/Pod(related)
    NAME                  READY  STATUS             RESTARTS  AGE
    hcg-766b4966c5-54sk9  0/1    ContainerCreating  0         0s
    hcg-76db9666b6-ddjz4  0/1    Running            5         11m

    ==> v1/Service
    NAME  TYPE       CLUSTER-IP   EXTERNAL-IP  PORT(S)   AGE
    hcg   ClusterIP  10.0.33.220  <none>       8080/TCP  11m


