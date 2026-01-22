"""
Data models and schemas for the Decision Intelligence Platform
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class DecisionType(str, Enum):
    """Type of decision recommendation"""
    REORDER = "reorder"
    DISCONTINUE = "discontinue"
    PROMOTE = "promote"
    REVIEW = "review"


class Transaction(BaseModel):
    """Transaction data model"""
    transaction_id: str
    product_id: str
    product_name: str
    quantity: int = Field(gt=0)
    unit_price: float = Field(gt=0)
    transaction_date: datetime
    customer_id: Optional[str] = None


class ProductInventory(BaseModel):
    """Product inventory data model"""
    product_id: str
    product_name: str
    current_stock: int
    unit_cost: float
    last_sale_date: Optional[datetime] = None
    average_daily_sales: float = 0.0
    days_of_stock_remaining: Optional[float] = None


class InventoryRisk(BaseModel):
    """Inventory risk assessment"""
    product_id: str
    product_name: str
    risk_level: RiskLevel
    risk_reason: str
    current_stock: int
    days_until_stockout: Optional[float] = None
    recommended_action: str


class SlowMovingProduct(BaseModel):
    """Slow-moving product identification"""
    product_id: str
    product_name: str
    days_since_last_sale: int
    current_stock: int
    total_value: float
    recommended_action: str


class ReorderRecommendation(BaseModel):
    """Reorder quantity recommendation"""
    product_id: str
    product_name: str
    current_stock: int
    recommended_quantity: int
    reasoning: str
    urgency: RiskLevel


class DecisionInsight(BaseModel):
    """Complete decision insight for a product"""
    product_id: str
    product_name: str
    decision_type: DecisionType
    priority: RiskLevel
    summary: str
    reasoning: str
    recommended_action: str
    estimated_impact: Optional[str] = None


class DecisionResponse(BaseModel):
    """Response containing all decision insights"""
    timestamp: datetime
    total_insights: int
    critical_actions: int
    insights: List[DecisionInsight]


class DataIngestionResponse(BaseModel):
    """Response from data ingestion"""
    success: bool
    records_processed: int
    products_identified: int
    message: str
