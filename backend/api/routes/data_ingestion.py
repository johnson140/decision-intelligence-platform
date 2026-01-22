"""
Data ingestion API routes
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional

from core.models import DataIngestionResponse
from services.data_service import DataService

router = APIRouter()
data_service = DataService()


@router.post("/ingest/csv", response_model=DataIngestionResponse)
async def ingest_csv_data(file: UploadFile = File(...)):
    """
    Upload and ingest transaction data from CSV file
    
    Expected CSV format:
    transaction_id,product_id,product_name,quantity,unit_price,transaction_date,customer_id
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")
    
    try:
        # Save uploaded file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        # Process the CSV
        transactions = data_service.ingest_transactions_from_csv(tmp_file_path)
        
        # Clean up temporary file
        os.unlink(tmp_file_path)
        
        # Get unique products
        unique_products = len(set(t.product_id for t in transactions))
        
        return DataIngestionResponse(
            success=True,
            records_processed=len(transactions),
            products_identified=unique_products,
            message=f"Successfully processed {len(transactions)} transactions for {unique_products} products"
        )
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


@router.get("/ingest/status")
async def get_ingestion_status():
    """Get status of data ingestion"""
    return {
        "status": "ready",
        "supported_formats": ["CSV"],
        "message": "Data ingestion service is operational"
    }
