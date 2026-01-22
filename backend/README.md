# Decision Intelligence Platform - Backend

FastAPI backend for the Decision Intelligence Platform.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Data Ingestion
- `POST /api/v1/ingest/csv` - Upload and process CSV transaction data
- `GET /api/v1/ingest/status` - Get ingestion service status

### Decisions
- `POST /api/v1/decisions/generate` - Generate decision insights (with optional CSV upload)
- `GET /api/v1/decisions/inventory-risks` - Get inventory risk assessments
- `GET /api/v1/decisions/slow-movers` - Get slow-moving product identification
- `GET /api/v1/decisions/reorder-recommendations` - Get reorder quantity recommendations
- `GET /api/v1/decisions/summary` - Get summary of all decision insights

## CSV Format

Expected CSV format for transaction data:

```csv
transaction_id,product_id,product_name,quantity,unit_price,transaction_date,customer_id
TXN001,PROD001,Widget A,5,10.50,2024-01-15T10:30:00,CUST001
TXN002,PROD002,Widget B,2,25.00,2024-01-15T11:00:00,CUST002
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── core/
│   ├── config.py          # Application configuration
│   └── models.py          # Pydantic models and schemas
├── services/
│   ├── data_service.py    # Data ingestion and management
│   └── decision_service.py # Business logic for decisions
└── api/
    └── routes/
        ├── data_ingestion.py # Data ingestion endpoints
        └── decisions.py      # Decision endpoints
```
