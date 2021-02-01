FROM python:latest

RUN mkdir /app
WORKDIR /app


COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY /scr .

EXPOSE 5000

CMD ["python", "main.py"]
