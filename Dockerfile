
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

ARG APP_VERSION=v1
ENV APP_VERSION=${APP_VERSION}
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]