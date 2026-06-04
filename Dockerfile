# Multi-stage build for Green IT (Numérique Responsable)
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . .

# Sécurité : éviter l'exécution en root
RUN useradd -m appuser && chown -R appuser:appuser /app && chmod +x /app/entrypoint.sh
USER appuser

EXPOSE 8000

CMD ["/app/entrypoint.sh"]