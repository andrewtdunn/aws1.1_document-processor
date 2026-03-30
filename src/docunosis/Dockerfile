FROM public.ecr.aws/docker/library/python:3.11-slim
# FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.10-slim


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

# Set environment variable for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Node.js and npm via apt-get
# Note: This method often installs older versions of Node/npm from the Debian repositories.
RUN apt-get update && \
    apt-get install -y nodejs npm && \
    rm -rf /var/lib/apt/lists/*

RUN npm install

COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]
