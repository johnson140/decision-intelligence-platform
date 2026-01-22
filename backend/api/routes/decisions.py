"""
Decision-focused API routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import tempfile
import os

from core.models import (
    DecisionResponse,
    DecisionInsight,
    InventoryRisk,
    SlowMovingProduct,
    ReorderRecommendation
)
from services.data_service import DataService
from services.decision_service import DecisionService

router = APIRouter()
data_service = DataService()
decision_service = DecisionService()

# In-memory storage for demo purposes
# In production, use a proper database
_inventory_cache = {}
_transactions_cache = []


@router.post("/decisions/generate", response_model=DecisionResponse)
async def generate_decisions(file: Optional[UploadFile] = File(None)):
    """
    Generate decision insights from transaction data
    
    If a CSV file is provided, it will be processed first.
    Otherwise, uses cached data from previous ingestion.
    """
    global _inventory_cache, _transactions_cache
    
    try:
        # Process CSV if provided
        if file:
            if not file.filename.endswith('.csv'):
                raise HTTPException(status_code=400, detail="File must be a CSV file")
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name
            
            transactions = data_service.ingest_transactions_from_csv(tmp_file_path)
            _transactions_cache = transactions
            os.unlink(tmp_file_path)
        elif not _transactions_cache:
            raise HTTPException(
                status_code=400, 
                detail="No data available. Please upload a CSV file first."
            )
        else:
            transactions = _transactions_cache
        
        # Calculate inventory
        inventory = data_service.calculate_product_inventory(transactions)
        _inventory_cache = inventory
        
        # Generate insights
        inventory_risks = decision_service.identify_inventory_risks(inventory)
        slow_movers = decision_service.identify_slow_moving_products(inventory)
        reorder_recommendations = decision_service.generate_reorder_recommendations(
            inventory, inventory_risks
        )
        
        # Generate comprehensive decision insights
        insights = decision_service.generate_decision_insights(
            inventory,
            inventory_risks,
            slow_movers,
            reorder_recommendations
        )
        
        # Count critical actions
        from core.models import RiskLevel
        critical_count = sum(1 for i in insights if i.priority == RiskLevel.CRITICAL)
        
        from datetime import datetime
        return DecisionResponse(
            timestamp=datetime.now(),
            total_insights=len(insights),
            critical_actions=critical_count,
            insights=insights
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating decisions: {str(e)}")


@router.get("/decisions/inventory-risks")
async def get_inventory_risks():
    """Get inventory risk assessments"""
    if not _inventory_cache:
        raise HTTPException(
            status_code=404,
            detail="No inventory data available. Please generate decisions first."
        )
    
    risks = decision_service.identify_inventory_risks(_inventory_cache)
    return {"risks": risks, "total": len(risks)}


@router.get("/decisions/slow-movers")
async def get_slow_moving_products():
    """Get slow-moving product identification"""
    if not _inventory_cache:
        raise HTTPException(
            status_code=404,
            detail="No inventory data available. Please generate decisions first."
        )
    
    slow_movers = decision_service.identify_slow_moving_products(_inventory_cache)
    return {"slow_movers": slow_movers, "total": len(slow_movers)}


@router.get("/decisions/reorder-recommendations")
async def get_reorder_recommendations():
    """Get reorder quantity recommendations"""
    if not _inventory_cache:
        raise HTTPException(
            status_code=404,
            detail="No inventory data available. Please generate decisions first."
        )
    
    risks = decision_service.identify_inventory_risks(_inventory_cache)
    recommendations = decision_service.generate_reorder_recommendations(
        _inventory_cache, risks
    )
    return {"recommendations": recommendations, "total": len(recommendations)}


@router.get("/decisions/summary")
async def get_decisions_summary():
    """Get a summary of all decision insights"""
    if not _inventory_cache:
        raise HTTPException(
            status_code=404,
            detail="No inventory data available. Please generate decisions first."
        )
    
    risks = decision_service.identify_inventory_risks(_inventory_cache)
    slow_movers = decision_service.identify_slow_moving_products(_inventory_cache)
    reorder_recs = decision_service.generate_reorder_recommendations(
        _inventory_cache, risks
    )
    
    from core.models import RiskLevel
    critical_risks = [r for r in risks if r.risk_level == RiskLevel.CRITICAL]
    high_risks = [r for r in risks if r.risk_level == RiskLevel.HIGH]
    
    return {
        "inventory_risks": {
            "total": len(risks),
            "critical": len(critical_risks),
            "high": len(high_risks),
            "medium": len([r for r in risks if r.risk_level == RiskLevel.MEDIUM]),
            "low": len([r for r in risks if r.risk_level == RiskLevel.LOW])
        },
        "slow_moving_products": len(slow_movers),
        "reorder_recommendations": len(reorder_recs),
        "total_products": len(_inventory_cache)
    }
