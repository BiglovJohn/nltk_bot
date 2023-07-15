FROM python:3.10.6

RUN mkdir /app

COPY . /app/

RUN pip install -r requirements.txt

WORKDIR /app

ENTRYPOINT["python", "main.py"]