# FERPA Shield Navigator
An AI-powered policy navigator for UIUC staff, built with privacy as a first-class citizen.

## Key Features
- **Privacy Shield:** Automatic redaction of PII (Names, Emails, Phones) before processing.
- **Local RAG:** Uses `all-MiniLM-L6-v2` embeddings to keep data on-premise.
- **Auditable:** Direct citations to UIUC Student Code and FERPA documentation.

## Quick Start
1. Drop UIUC Policy PDFs into `data/raw/`
2. Run `docker-compose up --build`
3. Ingest data: `docker exec -it ferpa_shield_app python src/ingest.py`
4. Visit `http://localhost:8501`