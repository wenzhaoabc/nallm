FROM python:3.11
LABEL authors="shuai"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

EXPOSE 8080

CMD ["python", "main.py"]
