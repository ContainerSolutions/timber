FROM python:3.7-alpine3.8

WORKDIR /app

RUN apk --no-cache add curl  

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app

CMD ["python3", "app.py"]
EXPOSE 8080
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
