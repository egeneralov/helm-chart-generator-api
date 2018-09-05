import os
import shutil
import io

from flask import Flask, Response, request, send_file
import yaml, json, jsonschema


def mkdir(path):
  try:
    os.stat(path)
  except:
    os.mkdir(path)

def put_data(path, data):
  with open(path, 'w+') as file:
    file.write(my_file)


class cd:
  def __init__(self, newPath):
    self.newPath = os.path.expanduser(newPath)
  def __enter__(self):
    self.savedPath = os.getcwd()
    os.chdir(self.newPath)
  def __exit__(self, etype, value, traceback):
    os.chdir(self.savedPath)


app = Flask(__name__)


@app.route("/", methods=['GET'])
def alive():
  return '', 200

@app.route("/generate/", methods=['POST'])
def generate():
  '''
  POST /generate/
    - checking json
    - validating schema
    - unpack skeleton
    - write values.yaml & Chart.yaml
    - helm package
    - remove source directory
    - return .tar.gz
  '''
  raw = request.get_data().decode()
  try:
    data = json.loads(raw)
  except json.decoder.JSONDecodeError as error:
    return str(error), 400, {'Content-Type': 'application/json'}
  schema = {"title":"chart","type":"object","properties":{"host":{"type":"string"},"version":{"type":"string"},"image":{"type":"string"},"imageTag":{"type":"string"},"port":{"type":"integer"},"imagePullSecret":{"type":"integer"}}}
  try:
    jsonschema.validate(data, schema)
  except jsonschema.exceptions.ValidationError as error:
    return str(error.message), 400, {'Content-Type': 'application/json'}
  values = {
    "imageTag": data['imageTag'],
    "image": data['image'],
    "envSecret": {},
    "service": { "port": data['port'] },
    "replicas": 1,
#    "imagePullSecret": "registry",
    "env": {},
    "ingress": {
      "host": data['host']
    },
    "app": {"resources":{"limits":{"memory":"256Mi","cpu":"200m"},"datas":{"memory":"256Mi","cpu":"200m"}}}
  }
  if 'imagePullSecret' in data.keys():
    values['imagePullSecret'] = data['imagePullSecret']
  values_yaml = yaml.dump(values)
  chart = {
    "sources": [data['image']],
    "description": "Helm chart for Kubernetes.",
    "name": data['host'],
    "version": data['version'],
    "home": data['host'],
    "maintainers": [ { "name": "Eduard Generalov", "email": "eduard@generalov.net" } ]
  }
  chart_yaml = yaml.dump(chart)
  answer = '{}\n\n\n\n{}\n'.format(values_yaml, chart_yaml)

  data['host'] = data['host']
  mkdir(data['host'])
  os.system('tar xzvf skeleton.tar.gz -C {}'.format(data['host']))
  with cd(data['host']):
    with open('values.yaml', 'w+') as f:
      f.write(values_yaml)
    with open('Chart.yaml', 'w+') as f:
      f.write(chart_yaml)
#    os.system('tar czvf {}-{}.tgz *'.format(data['host'], data['version']))

  os.system('helm package ' + data['host'])
  shutil.rmtree(data['host'])
  return '{}-{}.tgz'.format(data['host'], data['version']), 201
#  return '{}-{}.tgz'.format(data['host'], data['version'])
#  return send_file(os.path.join(os.environ['PWD'], '{}-{}.tgz'.format(data['host'], data['version'])), as_attachment=True)
#  with open('{}-{}.tgz'.format(data['host'], data['version']), 'rb') as bites:
#    return send_file(
#      io.BytesIO(bites.read()),
#      '{}-{}.tgz'.format(data['host'], data['version']),
#      attachment_filename='{}-{}.tgz *'.format(data['host'], data['version']),
#      as_attachment=True,
#      mimetype='application/gzip'
#    )


@app.route('/download/<path:filename>')
def download(filename):
  return send_file(os.path.join(os.getcwd(), filename), as_attachment=True)

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080,debug=True)


