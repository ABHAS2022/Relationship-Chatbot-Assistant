FROM python:3.11-slim

# Add security patches
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y gcc libffi-dev libmariadb-dev libmariadb-dev-compat



WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

