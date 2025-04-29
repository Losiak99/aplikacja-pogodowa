# Etap 1 - budowanie
FROM python:3.12-slim as builder
LABEL org.opencontainers.image.authors="Jan Kowalski"

WORKDIR /app
COPY app.py .
RUN pip install flask requests

# Etap 2 - finalny obraz
FROM python:3.12-slim
WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY app.py .

EXPOSE 5000
HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

CMD ["python", "app.py"]
