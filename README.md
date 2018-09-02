# Helm Chart Generator

Small microservice for generate HELM charts.

## QuickStart

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

## Build

    s2i build . centos/python-35-centos7 egeneralov/helm-chart-generator --loglevel 2



'''
curl -d'{"host":"jenkins.goodbit.tk","version":"1.0.1","image":"registry.goodbit.tk/egeneralov/jenkins","imageTag":"SHA","port":80}' 127.0.0.1:8080/helm/

- step: create helm deployment (microservice)
- step: create gitlab deploy token
- step: create k8s namespace with helm tiller (k8s.sh) and grant access to gitlab registry
- step: 

python3
import yaml, json
file = 'Chart.yaml'
with open(file) as f:
  raw = yaml.load(f.read())

json.dumps(raw)

'''



