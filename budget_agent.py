"""
Budget Agent: Analyzes categorized transactions and determines spending patterns.
"""
import json
from typing import Dict, List, Any
from datetime import datetime, date
from calendar import monthrange


class BudgetAgent:
    """Agent responsible for budget analysis and overspending prediction."""
    
    def __init__(self, budget_limit: float = 30000):
        """
        Initialize the Budget Agent.
        
        Args:
            budget_limit: Monthly budget limit in currency units (default: 30000)
        """
        self.budget_limit = budget_limit
    
    def calculate_category_spending(self, transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Calculate spending per category.
        
        Args:
            transactions: List of categorized transactions
            
        Returns:
            Dictionary with category-wise spending
        """
        category_spending = {}
        
        for transaction in transactions:
            if transaction.get("type", "").lower() == "debit":
                category = transaction.get("category", "Miscellaneous")
                amount = transaction.get("amount", 0)
                category_spending[category] = category_spending.get(category, 0) + amount
        
        return category_spending
    
    def calculate_monthly_total(self, transactions: List[Dict[str, Any]]) -> float:
        """
        Calculate total monthly spending (only debits).
        
        Args:
            transactions: List of categorized transactions
            
        Returns:
            Total spending amount
        """
        total = 0
        for transaction in transactions:
            if transaction.get("type", "").lower() == "debit":
                total += transaction.get("amount", 0)
        
        return total
    
    def predict_end_month_spending(self, transactions: List[Dict[str, Any]]) -> float:
        """
        Predict end-of-month spending based on current burn rate.
        
        Args:
            transactions: List of categorized transactions
            
        Returns:
            Projected end-of-month spending
        """
        if not transactions:
            return 0
        
        # Get current date and days in month
        today = date.today()
        days_in_month = monthrange(today.year, today.month)[1]
        current_day = today.day
        
        # Calculate spending so far
        current_spending = self.calculate_monthly_total(transactions)
        
        # If no transactions yet, return 0
        if current_spending == 0:
            return 0
        
        # Get the earliest transaction date to determine days elapsed
        transaction_dates = []
        for transaction in transactions:
            try:
                trans_date = datetime.strptime(transaction.get("date", ""), "%Y-%m-%d").date()
                # Only consider transactions from current month
                if trans_date.year == today.year and trans_date.month == today.month:
                    transaction_dates.append(trans_date)
            except:
                pass
        
        if not transaction_dates:
            # Fallback to current day if no valid dates
            days_elapsed = current_day
        else:
            # Calculate days from earliest transaction to today
            earliest_date = min(transaction_dates)
            days_elapsed = (today - earliest_date).days + 1
        
        # Avoid division by zero
        if days_elapsed == 0:
            days_elapsed = 1
        
        # Calculate daily burn rate
        daily_burn_rate = current_spending / days_elapsed
        
        # Project for the full month
        projected_spending = daily_burn_rate * days_in_month
        
        return round(projected_spending, 2)
    
    def determine_status(self, projected_spending: float) -> str:
        """
        Determine budget status.
        
        Args:
            projected_spending: Projected end-of-month spending
            
        Returns:
            Status string: "overspending" or "within_budget"
        """
        if projected_spending > self.budget_limit:
            return "overspending"
        return "within_budget"
    
    def process(self, input_data: Dict[str, Any], budget_limit: float = None) -> Dict[str, Any]:
        """
        Process categorized transactions and perform budget analysis.
        
        Args:
            input_data: Dictionary containing categorized transactions
            budget_limit: Optional budget limit override
            
        Returns:
            Dictionary with budget analysis
        """
        if budget_limit is not None:
            self.budget_limit = budget_limit
        
        categorized_transactions = input_data.get("categorized_transactions", [])
        
        # Calculate metrics
        month_total = self.calculate_monthly_total(categorized_transactions)
        category_spending = self.calculate_category_spending(categorized_transactions)
        projected_spending = self.predict_end_month_spending(categorized_transactions)
        status = self.determine_status(projected_spending)
        
        return {
            "budget_analysis": {
                "month_total": month_total,
                "limit": self.budget_limit,
                "projected_end_month": projected_spending,
                "status": status,
                "categories": category_spending
            }
        }


if __name__ == "__main__":
    # Example usage
    sample_input = {
        "categorized_transactions": [
            {
                "date": "2024-01-15",
                "description": "Swiggy Order",
                "amount": 350,
                "type": "debit",
                "mode": "UPI",
                "category": "Food"
            },
            {
                "date": "2024-01-16",
                "description": "Uber Ride",
                "amount": 120,
                "type": "debit",
                "mode": "UPI",
                "category": "Transport"
            },
            {
                "date": "2024-01-17",
                "description": "Myntra Shopping",
                "amount": 1500,
                "type": "debit",
                "mode": "Card",
                "category": "Shopping"
            }
        ]
    }
    
    agent = BudgetAgent(budget_limit=30000)
    result = agent.process(sample_input)
    print(json.dumps(result, indent=2))
