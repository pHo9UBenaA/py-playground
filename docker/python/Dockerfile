FROM python:3.9-slim

WORKDIR /app/scripts

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python"]
