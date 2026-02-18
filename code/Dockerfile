FROM python:3.11-slim
# FROM --platform=linux/amd64 python:3.10-slim

EXPOSE 80

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY server.py /app

RUN python -m pip install -r requirements.txt

CMD ["python", "server.py"]