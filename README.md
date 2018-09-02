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

