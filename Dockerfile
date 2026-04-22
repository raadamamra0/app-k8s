FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/
COPY templates /app/templates
COPY static /app/static
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
