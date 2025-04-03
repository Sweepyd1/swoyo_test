FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl

RUN curl -LsS https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY . .

RUN chmod +x ./prism-cli-linux

RUN /root/.cargo/bin/uv pip install -r requirements.txt

CMD ["sh", "-c", "/root/.cargo/bin/uvicorn main:app --host 0.0.0.0 --port 8000"]