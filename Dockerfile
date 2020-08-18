FROM python:2-alpine3.7

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD ["main.py"]
