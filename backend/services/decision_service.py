"""
Business logic for generating decision insights
"""

from datetime import datetime, timedelta
from typing import List, Dict
from collections import defaultdict

from core.models import (
    ProductInventory,
    InventoryRisk,
    SlowMovingProduct,
    ReorderRecommendation,
    DecisionInsight,
    DecisionType,
    RiskLevel
)
from core.config import settings


class DecisionService:
    """Service for generating business decisions and insights"""
    
    def __init__(self):
        self.slow_moving_threshold = settings.SLOW_MOVING_THRESHOLD_DAYS
        self.low_stock_threshold = settings.LOW_STOCK_THRESHOLD_PERCENT
        self.reorder_lead_time = settings.REORDER_LEAD_TIME_DAYS
    
    def identify_inventory_risks(
        self, 
        inventory: Dict[str, ProductInventory]
    ) -> List[InventoryRisk]:
        """
        Identify products at risk of stockout
        """
        risks = []
        current_date = datetime.now()
        
        for product_id, product in inventory.items():
            risk_level = RiskLevel.LOW
            risk_reason = ""
            days_until_stockout = None
            recommended_action = ""
            
            # Check if product has sales data
            if product.average_daily_sales == 0:
                continue  # Skip products with no sales history
            
            # Calculate days until stockout
            if product.days_of_stock_remaining is not None:
                days_until_stockout = product.days_of_stock_remaining
                
                # Determine risk level
                if days_until_stockout <= 3:
                    risk_level = RiskLevel.CRITICAL
                    risk_reason = f"Critical: Only {days_until_stockout:.1f} days of stock remaining"
                    recommended_action = "Urgent reorder required immediately"
                elif days_until_stockout <= 7:
                    risk_level = RiskLevel.HIGH
                    risk_reason = f"High risk: {days_until_stockout:.1f} days of stock remaining"
                    recommended_action = "Reorder within 24 hours"
                elif days_until_stockout <= 14:
                    risk_level = RiskLevel.MEDIUM
                    risk_reason = f"Medium risk: {days_until_stockout:.1f} days of stock remaining"
                    recommended_action = "Plan reorder within the week"
                else:
                    risk_level = RiskLevel.LOW
                    risk_reason = f"Low risk: {days_until_stockout:.1f} days of stock remaining"
                    recommended_action = "Monitor stock levels"
            
            # Check for zero stock
            if product.current_stock == 0:
                risk_level = RiskLevel.CRITICAL
                risk_reason = "Out of stock - immediate action required"
                recommended_action = "Urgent reorder - product is currently unavailable"
                days_until_stockout = 0
            
            risks.append(InventoryRisk(
                product_id=product_id,
                product_name=product.product_name,
                risk_level=risk_level,
                risk_reason=risk_reason,
                current_stock=product.current_stock,
                days_until_stockout=days_until_stockout,
                recommended_action=recommended_action
            ))
        
        # Sort by risk level (critical first)
        risk_priority = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3}
        risks.sort(key=lambda x: risk_priority[x.risk_level])
        
        return risks
    
    def identify_slow_moving_products(
        self,
        inventory: Dict[str, ProductInventory]
    ) -> List[SlowMovingProduct]:
        """
        Identify slow-moving products that tie up cash
        """
        slow_movers = []
        current_date = datetime.now()
        
        for product_id, product in inventory.items():
            if product.last_sale_date is None:
                continue
            
            days_since_last_sale = (current_date - product.last_sale_date).days
            
            if days_since_last_sale >= self.slow_moving_threshold:
                # Estimate total value (would need unit_cost in production)
                total_value = product.current_stock * 10.0  # Placeholder
                
                recommended_action = ""
                if product.current_stock > 0:
                    if days_since_last_sale >= 180:
                        recommended_action = "Consider discontinuing or deep discounting"
                    elif days_since_last_sale >= 120:
                        recommended_action = "Run promotional campaign to clear inventory"
                    else:
                        recommended_action = "Review pricing and marketing strategy"
                else:
                    recommended_action = "No action needed - already out of stock"
                
                slow_movers.append(SlowMovingProduct(
                    product_id=product_id,
                    product_name=product.product_name,
                    days_since_last_sale=days_since_last_sale,
                    current_stock=product.current_stock,
                    total_value=total_value,
                    recommended_action=recommended_action
                ))
        
        # Sort by days since last sale (longest first)
        slow_movers.sort(key=lambda x: x.days_since_last_sale, reverse=True)
        
        return slow_movers
    
    def generate_reorder_recommendations(
        self,
        inventory: Dict[str, ProductInventory],
        inventory_risks: List[InventoryRisk]
    ) -> List[ReorderRecommendation]:
        """
        Generate reorder quantity recommendations
        """
        recommendations = []
        
        # Create a risk lookup
        risk_lookup = {risk.product_id: risk for risk in inventory_risks}
        
        for product_id, product in inventory.items():
            # Only recommend for products that need reordering
            if product_id not in risk_lookup:
                continue
            
            risk = risk_lookup[product_id]
            
            # Skip if already out of stock and no sales history
            if product.current_stock == 0 and product.average_daily_sales == 0:
                continue
            
            # Calculate recommended quantity
            safety_buffer_days = 14  # 2 weeks safety buffer
            
            if product.average_daily_sales > 0:
                # Calculate days of stock needed (lead time + safety buffer)
                total_days_needed = self.reorder_lead_time + safety_buffer_days
                
                # Calculate quantity needed
                quantity_needed = product.average_daily_sales * total_days_needed
                
                # Adjust based on risk level
                if risk.risk_level == RiskLevel.CRITICAL:
                    quantity_needed *= 1.5  # Increase for critical items
                elif risk.risk_level == RiskLevel.HIGH:
                    quantity_needed *= 1.3
                
                # Round up to nearest reasonable quantity
                recommended_quantity = int(quantity_needed) + (10 - int(quantity_needed) % 10)
                
                # Minimum order quantity
                if recommended_quantity < 10:
                    recommended_quantity = 10
                
                # Generate reasoning for products with sales history
                reasoning = (
                    f"Based on average daily sales of {product.average_daily_sales:.1f} units, "
                    f"you need {total_days_needed} days of stock (including {self.reorder_lead_time} day lead time "
                    f"and {safety_buffer_days} day safety buffer). "
                    f"Current stock: {product.current_stock} units."
                )
            else:
                # For products with no sales history, suggest a small trial order
                recommended_quantity = 20
                total_days_needed = 30
                
                # Generate reasoning for products without sales history
                reasoning = (
                    f"This product has no sales history. Recommended trial order of {recommended_quantity} units "
                    f"to establish demand patterns. Current stock: {product.current_stock} units."
                )
            
            recommendations.append(ReorderRecommendation(
                product_id=product_id,
                product_name=product.product_name,
                current_stock=product.current_stock,
                recommended_quantity=recommended_quantity,
                reasoning=reasoning,
                urgency=risk.risk_level
            ))
        
        # Sort by urgency
        urgency_priority = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3}
        recommendations.sort(key=lambda x: urgency_priority[x.urgency])
        
        return recommendations
    
    def generate_decision_insights(
        self,
        inventory: Dict[str, ProductInventory],
        inventory_risks: List[InventoryRisk],
        slow_movers: List[SlowMovingProduct],
        reorder_recommendations: List[ReorderRecommendation]
    ) -> List[DecisionInsight]:
        """
        Generate comprehensive decision insights combining all analyses
        """
        insights = []
        
        # Process inventory risks and reorder recommendations
        reorder_lookup = {rec.product_id: rec for rec in reorder_recommendations}
        
        for risk in inventory_risks:
            product = inventory.get(risk.product_id)
            if not product:
                continue
            
            reorder_rec = reorder_lookup.get(risk.product_id)
            
            decision_type = DecisionType.REORDER
            summary = f"{risk.product_name} needs immediate attention"
            reasoning = risk.risk_reason
            
            if reorder_rec:
                reasoning += f" Recommended order quantity: {reorder_rec.recommended_quantity} units. {reorder_rec.reasoning}"
            
            estimated_impact = (
                f"Prevents stockout and potential lost sales. "
                f"Estimated impact: {risk.days_until_stockout:.0f} days until out of stock."
                if risk.days_until_stockout else "Prevents stockout."
            )
            
            insights.append(DecisionInsight(
                product_id=risk.product_id,
                product_name=risk.product_name,
                decision_type=decision_type,
                priority=risk.risk_level,
                summary=summary,
                reasoning=reasoning,
                recommended_action=risk.recommended_action,
                estimated_impact=estimated_impact
            ))
        
        # Process slow-moving products
        for slow_mover in slow_movers:
            decision_type = DecisionType.DISCONTINUE if slow_mover.days_since_last_sale >= 180 else DecisionType.REVIEW
            
            summary = f"{slow_mover.product_name} has not sold in {slow_mover.days_since_last_sale} days"
            reasoning = (
                f"This product has been sitting in inventory for {slow_mover.days_since_last_sale} days "
                f"without a sale, tying up ${slow_mover.total_value:.2f} in cash."
            )
            
            estimated_impact = (
                f"Freeing up ${slow_mover.total_value:.2f} in working capital. "
                f"Consider alternative products with better turnover."
            )
            
            priority = RiskLevel.HIGH if slow_mover.days_since_last_sale >= 180 else RiskLevel.MEDIUM
            
            insights.append(DecisionInsight(
                product_id=slow_mover.product_id,
                product_name=slow_mover.product_name,
                decision_type=decision_type,
                priority=priority,
                summary=summary,
                reasoning=reasoning,
                recommended_action=slow_mover.recommended_action,
                estimated_impact=estimated_impact
            ))
        
        # Sort by priority
        priority_order = {RiskLevel.CRITICAL: 0, RiskLevel.HIGH: 1, RiskLevel.MEDIUM: 2, RiskLevel.LOW: 3}
        insights.sort(key=lambda x: (priority_order[x.priority], x.product_name))
        
        return insights
