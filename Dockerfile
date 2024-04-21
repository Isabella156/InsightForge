FROM python:3.11-slim
WORKDIR /usr/src/app

COPY src/ ./src/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["python", "./src/pipeline.py"]
CMD ["python", "./src/main.py"]
