# --- Build stage ---
ARG PYTHON_VERSION=3.14.3
FROM python:${PYTHON_VERSION}-slim AS build

WORKDIR /app

# Installer gcc uniquement pour la compilation des dépendances
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Installer les dépendances Python dans /install
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# --- Final stage ---
ARG PYTHON_VERSION=3.14.3
FROM python:${PYTHON_VERSION}-slim

# Metadata OCI
LABEL org.opencontainers.image.title="Data Summarizer for LLM"
LABEL org.opencontainers.image.description="CLI tool to analyze and summarize datasets (CSV, Excel, JSON) for LLM context injection."
LABEL org.opencontainers.image.authors="abguven"
LABEL org.opencontainers.image.source="https://github.com/abguven/data-summarizer-llm"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="1.2"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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
