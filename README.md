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

