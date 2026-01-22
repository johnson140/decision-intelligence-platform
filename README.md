# Decision Intelligence Platform for Transactional Businesses

## Overview

Transactional businesses generate large volumes of sales and inventory data, but most of this data is never transformed into clear, actionable decisions.

This project aims to bridge that gap by converting raw transactional data into **decision-ready insights** that help business owners and managers act with confidence.

This is not a dashboard-first system.
It is a **decision-first platform**.

---

## Problem Statement

Small and medium transactional businesses often face:

* Stock-outs of fast-moving products
* Excess cash locked in slow-moving inventory
* Poor visibility into which products truly drive value
* Reactive decisions made too late

Although data exists, it is rarely structured to answer practical business questions.

---

## Project Objective

To design and implement a system that:

* Identifies inventory risks before they occur
* Highlights products that negatively impact cash flow
* Recommends clear, explainable actions
* Presents insights in plain language for non-technical users

---

## Target Users

* Retail business owners
* Pharmacy managers
* Small distributors
* Operational decision-makers

This platform is **not** designed for analysts or data scientists.

---

## Planned Features (Phase 1)

* Transactional data ingestion (CSV-based)
* Inventory risk detection
* Slow-moving product identification
* Reorder quantity recommendations
* Decision-focused API endpoints

---

## Technology Stack (Initial)

* Backend: Python, FastAPI
* Frontend: React (lightweight UI)
* Data: CSV / relational structure
* Version Control: Git & GitHub

---

## Project Status

✅ **Phase 1 Complete** - Core platform implemented with all planned features.

---

## Quick Start

### Prerequisites

- Python 3.8+ 
- Node.js 16+ and npm
- Git

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

---

## Project Structure

```
decision-intelligence-platform/
├── backend/                 # FastAPI backend
│   ├── main.py             # Application entry point
│   ├── core/               # Core configuration and models
│   │   ├── config.py       # Application settings
│   │   └── models.py       # Data models and schemas
│   ├── services/           # Business logic services
│   │   ├── data_service.py      # Data ingestion
│   │   └── decision_service.py  # Decision generation
│   ├── api/                # API routes
│   │   └── routes/
│   │       ├── data_ingestion.py
│   │       └── decisions.py
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.jsx         # Main app component
│   │   └── main.jsx        # Entry point
│   └── package.json
├── data/                   # Data storage
│   ├── sample_data.csv     # Sample transaction data
│   └── uploads/            # Uploaded CSV files
└── README.md
```

---

## Usage

1. **Start the backend server** (port 8000)
2. **Start the frontend** (port 3000)
3. **Upload a CSV file** with transaction data using the web interface
4. **View decision insights** generated from your data

### CSV Format

Your CSV file should have the following columns:

```csv
transaction_id,product_id,product_name,quantity,unit_price,transaction_date,customer_id
TXN001,PROD001,Widget A,5,10.50,2024-01-15T10:30:00,CUST001
```

A sample CSV file is provided in `data/sample_data.csv`.

---

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

---

## Features Implemented

✅ **CSV Data Ingestion** - Upload and process transaction data from CSV files  
✅ **Inventory Risk Detection** - Identify products at risk of stockout  
✅ **Slow-Moving Product Identification** - Find products tying up cash  
✅ **Reorder Recommendations** - Get actionable reorder quantity suggestions  
✅ **Decision-Focused API** - RESTful endpoints for all decision types  
✅ **Modern Web Interface** - Clean, user-friendly React frontend  
✅ **Priority-Based Insights** - Filter insights by urgency (Critical, High, Medium, Low)  

---

## Next Steps

Future enhancements could include:
- Database integration for persistent storage
- User authentication and multi-tenant support
- Email/SMS notifications for critical alerts
- Advanced analytics and forecasting
- Integration with POS systems
- Mobile app for on-the-go decision making
