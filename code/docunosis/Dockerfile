FROM public.ecr.aws/docker/library/python:3.11-slim
# Alternative: FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.10-slim

EXPOSE 80

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

RUN python -m pip install -r requirements.txt

CMD ["python", "app.py"]