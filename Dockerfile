FROM python:3.8-slim
WORKDIR /app

# dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# application
COPY check.py .

# run
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "check:app", "--host", "0.0.0.0", "--port", "8000" ]