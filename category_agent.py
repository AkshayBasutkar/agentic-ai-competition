"""
Category Agent: Classifies user-entered transactions into spending categories.
"""
import json
from typing import Dict, List, Any


class CategoryAgent:
    """Agent responsible for categorizing transactions."""
    
    CATEGORIES = [
        "Food",
        "Transport",
        "Shopping",
        "Groceries",
        "Entertainment",
        "Bills",
        "EMI",
        "Salary",
        "Investment",
        "Miscellaneous"
    ]
    
    # Mapping keywords to categories
    CATEGORY_KEYWORDS = {
        "Food": [
            "swiggy", "zomato", "restaurant", "cafe", "coffee", "food", 
            "pizza", "burger", "dining", "lunch", "dinner", "breakfast",
            "starbucks", "mcdonald", "kfc", "dominos", "subway"
        ],
        "Transport": [
            "uber", "ola", "rapido", "metro", "bus", "taxi", "petrol",
            "diesel", "fuel", "parking", "toll", "auto", "cab", "train"
        ],
        "Shopping": [
            "amazon", "flipkart", "myntra", "ajio", "shopping", "store",
            "mall", "purchase", "fashion", "clothes", "shoes", "electronics"
        ],
        "Groceries": [
            "bigbasket", "grofers", "blinkit", "zepto", "grocery", 
            "vegetables", "fruits", "supermarket", "dmart", "reliance fresh"
        ],
        "Entertainment": [
            "netflix", "amazon prime", "hotstar", "spotify", "movie",
            "theatre", "cinema", "concert", "game", "gaming", "youtube premium"
        ],
        "Bills": [
            "electricity", "water", "gas", "internet", "broadband", "mobile",
            "phone bill", "recharge", "utility", "rent", "maintenance"
        ],
        "EMI": [
            "emi", "loan", "installment", "credit card", "mortgage"
        ],
        "Salary": [
            "salary", "wages", "income", "payroll", "payment received"
        ],
        "Investment": [
            "mutual fund", "stocks", "sip", "investment", "shares", 
            "bonds", "fixed deposit", "fd", "rd"
        ]
    }
    
    def __init__(self):
        """Initialize the Category Agent."""
        pass
    
    def categorize_transaction(self, transaction: Dict[str, Any]) -> str:
        """
        Categorize a single transaction based on description, amount, and mode.
        
        Args:
            transaction: Dictionary containing transaction details
            
        Returns:
            Category name as string
        """
        description = transaction.get("description", "").lower()
        amount = transaction.get("amount", 0)
        trans_type = transaction.get("type", "").lower()
        mode = transaction.get("mode", "").lower()
        
        # Check for Salary (credit transactions with typical salary indicators)
        if trans_type == "credit" and amount > 10000:
            for keyword in self.CATEGORY_KEYWORDS["Salary"]:
                if keyword in description:
                    return "Salary"
        
        # Check each category's keywords
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        
        # Default categorization based on transaction type
        if trans_type == "credit":
            return "Miscellaneous"
        
        return "Miscellaneous"
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process transactions and categorize them.
        
        Args:
            input_data: Dictionary containing list of transactions
            
        Returns:
            Dictionary with categorized transactions
        """
        transactions = input_data.get("transactions", [])
        categorized_transactions = []
        
        for transaction in transactions:
            categorized_transaction = transaction.copy()
            categorized_transaction["category"] = self.categorize_transaction(transaction)
            categorized_transactions.append(categorized_transaction)
        
        return {
            "categorized_transactions": categorized_transactions
        }


if __name__ == "__main__":
    # Example usage
    sample_input = {
        "transactions": [
            {
                "date": "2024-01-15",
                "description": "Swiggy Order",
                "amount": 350,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-16",
                "description": "Uber Ride",
                "amount": 120,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-17",
                "description": "Myntra Shopping",
                "amount": 1500,
                "type": "debit",
                "mode": "Card"
            }
        ]
    }
    
    agent = CategoryAgent()
    result = agent.process(sample_input)
    print(json.dumps(result, indent=2))
