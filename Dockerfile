FROM python:3.11-slim

ENV PYHTONBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN adduser --disabled-password --gecos "" appuser

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.7.1/en_core_web_md-3.7.1-py3-none-any.whl

COPY --chown=appuser:appuser . .

RUN chown -R appuser:appuser /home/appuser

USER appuser

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]



