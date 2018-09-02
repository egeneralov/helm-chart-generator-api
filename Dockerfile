FROM python:3.5
LABEL MAINTANER Eduard Generalov <eduard@generalov.net>
WORKDIR /app/

# install modeules
ADD requirements.txt .
RUN pip install -r requirements.txt

# install helm binary
RUN curl -s https://storage.googleapis.com/kubernetes-helm/helm-v2.9.1-linux-amd64.tar.gz | tar xzvf - -C /tmp && \
mv /tmp/linux-amd64/helm /usr/local/sbin/helm && rm -rf /tmp/linux-amd64/

# add project files
ADD . .

# add build time
RUN date > build_time.txt

# serve via 1 tread
CMD gunicorn --threads 1 --bind 0.0.0.0:8080 app:app
