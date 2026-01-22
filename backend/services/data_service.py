"""
Data ingestion and management service
"""

import csv
import os
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path
from pydantic import ValidationError

from core.config import settings
from core.models import Transaction, ProductInventory


class DataService:
    """Service for handling data ingestion and storage"""
    
    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    def ingest_transactions_from_csv(self, file_path: str) -> List[Transaction]:
        """
        Ingest transactions from a CSV file
        
        Expected CSV format:
        transaction_id,product_id,product_name,quantity,unit_price,transaction_date,customer_id
        """
        transactions = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    try:
                        transaction = Transaction(
                            transaction_id=row.get('transaction_id', ''),
                            product_id=row.get('product_id', ''),
                            product_name=row.get('product_name', ''),
                            quantity=int(row.get('quantity', 0)),
                            unit_price=float(row.get('unit_price', 0)),
                            transaction_date=datetime.fromisoformat(
                                row.get('transaction_date', datetime.now().isoformat())
                            ),
                            customer_id=row.get('customer_id')
                        )
                        transactions.append(transaction)
                    except (ValueError, KeyError, ValidationError) as e:
                        # Skip invalid rows but continue processing
                        print(f"Warning: Skipping invalid row: {e}")
                        continue
        
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        except Exception as e:
            raise Exception(f"Error reading CSV file: {str(e)}")
        
        return transactions
    
    def calculate_product_inventory(
        self, 
        transactions: List[Transaction],
        initial_inventory: Optional[Dict[str, int]] = None
    ) -> Dict[str, ProductInventory]:
        """
        Calculate current inventory levels from transactions
        
        This is a simplified calculation. In production, you'd want
        to track actual inventory movements (purchases, returns, etc.)
        """
        product_data: Dict[str, Dict] = {}
        
        # Process transactions
        for transaction in transactions:
            product_id = transaction.product_id
            
            if product_id not in product_data:
                product_data[product_id] = {
                    'product_id': product_id,
                    'product_name': transaction.product_name,
                    'total_sold': 0,
                    'last_sale_date': transaction.transaction_date,
                    'first_sale_date': transaction.transaction_date,
                    'total_revenue': 0.0,
                    'sale_dates': []
                }
            
            product_data[product_id]['total_sold'] += transaction.quantity
            product_data[product_id]['total_revenue'] += (
                transaction.quantity * transaction.unit_price
            )
            product_data[product_id]['sale_dates'].append(transaction.transaction_date)
            
            if transaction.transaction_date > product_data[product_id]['last_sale_date']:
                product_data[product_id]['last_sale_date'] = transaction.transaction_date
            if transaction.transaction_date < product_data[product_id]['first_sale_date']:
                product_data[product_id]['first_sale_date'] = transaction.transaction_date
        
        # Calculate inventory and metrics
        inventory_dict = {}
        current_date = datetime.now()
        
        for product_id, data in product_data.items():
            # Calculate days of data
            days_span = (data['last_sale_date'] - data['first_sale_date']).days + 1
            days_span = max(days_span, 1)  # Avoid division by zero
            
            # Calculate average daily sales
            average_daily_sales = data['total_sold'] / days_span
            
            # Estimate current stock (simplified - assumes initial stock)
            initial_stock = initial_inventory.get(product_id, 0) if initial_inventory else 0
            estimated_stock = max(0, initial_stock - data['total_sold'])
            
            # Calculate days of stock remaining
            days_remaining = None
            if average_daily_sales > 0:
                days_remaining = estimated_stock / average_daily_sales
            
            inventory_dict[product_id] = ProductInventory(
                product_id=product_id,
                product_name=data['product_name'],
                current_stock=estimated_stock,
                unit_cost=0.0,  # Would need to be provided separately
                last_sale_date=data['last_sale_date'],
                average_daily_sales=average_daily_sales,
                days_of_stock_remaining=days_remaining
            )
        
        return inventory_dict
    
    def save_transactions(self, transactions: List[Transaction], filename: str = None):
        """Save transactions to a CSV file"""
        if filename is None:
            filename = f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        file_path = self.upload_dir / filename
        
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            if transactions:
                writer = csv.DictWriter(
                    file,
                    fieldnames=transactions[0].dict().keys()
                )
                writer.writeheader()
                for transaction in transactions:
                    writer.writerow(transaction.dict())
        
        return str(file_path)
