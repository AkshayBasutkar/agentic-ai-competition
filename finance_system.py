"""
Multi-Agent Finance Intelligence System
Orchestrates Category Agent -> Budget Agent -> Advisor Agent workflow
"""
import json
from typing import Dict, Any
from category_agent import CategoryAgent
from budget_agent import BudgetAgent
from advisor_agent import SavingAdvisorAgent


class FinanceIntelligenceSystem:
    """
    Main orchestrator for the multi-agent finance intelligence system.
    Chains agents in the workflow: Category Agent -> Budget Agent -> Advisor Agent
    """
    
    def __init__(self, budget_limit: float = 30000):
        """
        Initialize the finance intelligence system.
        
        Args:
            budget_limit: Monthly budget limit (default: 30000)
        """
        self.category_agent = CategoryAgent()
        self.budget_agent = BudgetAgent(budget_limit=budget_limit)
        self.advisor_agent = SavingAdvisorAgent()
        self.budget_limit = budget_limit
    
    def process(self, transactions: Dict[str, Any], budget_limit: float = None) -> Dict[str, Any]:
        """
        Process transactions through all agents in sequence.
        
        Args:
            transactions: Dictionary containing user transactions
            budget_limit: Optional budget limit override
            
        Returns:
            Complete analysis with categorized transactions, budget analysis, advice, and summary
        """
        # Use provided budget limit or default
        if budget_limit is not None:
            self.budget_limit = budget_limit
            self.budget_agent.budget_limit = budget_limit
        
        # Step 1: Category Agent - Categorize transactions
        category_result = self.category_agent.process(transactions)
        
        # Step 2: Budget Agent - Analyze spending patterns
        budget_result = self.budget_agent.process(category_result, budget_limit=self.budget_limit)
        
        # Step 3: Advisor Agent - Generate advice and summary
        advisor_result = self.advisor_agent.process(budget_result)
        
        # Combine all results into final output
        final_output = {
            "categorized_transactions": category_result["categorized_transactions"],
            "budget_analysis": budget_result["budget_analysis"],
            "advice": advisor_result["advice"],
            "summary": advisor_result["summary"]
        }
        
        return final_output
    
    def process_from_json(self, json_input: str, budget_limit: float = None) -> str:
        """
        Process transactions from JSON string input.
        
        Args:
            json_input: JSON string containing transactions
            budget_limit: Optional budget limit override
            
        Returns:
            JSON string with complete analysis
        """
        try:
            input_data = json.loads(json_input)
            result = self.process(input_data, budget_limit=budget_limit)
            return json.dumps(result, indent=2)
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON input: {str(e)}"}, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Processing error: {str(e)}"}, indent=2)


def main():
    """Main function to demonstrate the system."""
    
    # Example transactions
    sample_transactions = {
        "transactions": [
            {
                "date": "2024-01-05",
                "description": "Swiggy Order",
                "amount": 450,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-06",
                "description": "Uber Ride",
                "amount": 150,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-07",
                "description": "Myntra Fashion",
                "amount": 2500,
                "type": "debit",
                "mode": "Card"
            },
            {
                "date": "2024-01-08",
                "description": "BigBasket Groceries",
                "amount": 1800,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-09",
                "description": "Netflix Subscription",
                "amount": 649,
                "type": "debit",
                "mode": "Card"
            },
            {
                "date": "2024-01-10",
                "description": "Electricity Bill",
                "amount": 1200,
                "type": "debit",
                "mode": "NetBanking"
            },
            {
                "date": "2024-01-11",
                "description": "Petrol Pump",
                "amount": 800,
                "type": "debit",
                "mode": "Card"
            },
            {
                "date": "2024-01-12",
                "description": "Zomato Food",
                "amount": 320,
                "type": "debit",
                "mode": "UPI"
            },
            {
                "date": "2024-01-13",
                "description": "Amazon Shopping",
                "amount": 3200,
                "type": "debit",
                "mode": "Card"
            },
            {
                "date": "2024-01-14",
                "description": "Coffee Shop",
                "amount": 280,
                "type": "debit",
                "mode": "Cash"
            }
        ]
    }
    
    # Initialize system with budget limit of 30000
    system = FinanceIntelligenceSystem(budget_limit=30000)
    
    # Process transactions
    result = system.process(sample_transactions)
    
    # Print results
    print("=" * 80)
    print("MULTI-AGENT FINANCE INTELLIGENCE SYSTEM")
    print("=" * 80)
    print()
    print(json.dumps(result, indent=2))
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(result["summary"])
    print("=" * 80)


if __name__ == "__main__":
    main()
