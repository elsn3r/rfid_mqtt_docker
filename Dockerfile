FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc python3-dev libffi-dev libssl-dev \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python3", "app.py"]
