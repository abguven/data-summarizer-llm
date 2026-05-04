# --- Build stage ---
FROM python:3.15.0a8-slim AS build

WORKDIR /app

# Installer gcc uniquement pour la compilation des dépendances
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Installer les dépendances Python dans /install
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# --- Final stage ---
FROM python:3.15.0a8-slim

ARG APP_VERSION=dev

# Apply all available OS security patches
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Metadata OCI
LABEL org.opencontainers.image.title="Data Summarizer for LLM"
LABEL org.opencontainers.image.description="CLI tool to analyze and summarize datasets (CSV, Excel, JSON) for LLM context injection."
LABEL org.opencontainers.image.authors="abguven"
LABEL org.opencontainers.image.source="https://github.com/abguven/data-summarizer-llm"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="${APP_VERSION}"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV INPUT_DIR=/app/data/input
ENV OUTPUT_DIR=/app/data/output
ENV LOG_DIR=/app/logs

WORKDIR /app

# Copier les paquets Python installés depuis le build stage
COPY --from=build /install /usr/local

# Copier le code source
COPY src/ ./src/

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/data/input /app/data/output /app/logs && \
    chown -R appuser:appuser /app && \
    chmod 700 /app/data/input /app/data/output /app/logs

USER appuser

CMD ["python", "src/summarize_dataset.py"]
