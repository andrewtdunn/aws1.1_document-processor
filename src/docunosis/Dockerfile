FROM public.ecr.aws/docker/library/python:3.11-slim
# FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.10-slim


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN npm install

COPY . /app

ENTRYPOINT ["python"]

CMD ["app.py"]
