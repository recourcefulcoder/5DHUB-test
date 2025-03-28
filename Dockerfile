# Stage 1 - package installation
FROM python:3.12-alpine AS builder

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Stage 2 - building
FROM python:3.12-alpine

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /app

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:${PYTHONPATH}"

EXPOSE 8000

CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
