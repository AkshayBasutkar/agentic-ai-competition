"""
Saving Advisor Agent: Provides intelligent, actionable savings & investment advice.
"""
import json
from typing import Dict, List, Any


class SavingAdvisorAgent:
    """Agent responsible for providing financial advice and savings recommendations."""
    
    def __init__(self):
        """Initialize the Saving Advisor Agent."""
        pass
    
    def generate_saving_tips(self, budget_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate personalized saving tips based on spending patterns.
        
        Args:
            budget_analysis: Budget analysis data
            
        Returns:
            List of actionable saving tips
        """
        tips = []
        categories = budget_analysis.get("categories", {})
        month_total = budget_analysis.get("month_total", 0)
        status = budget_analysis.get("status", "within_budget")
        
        # Food spending tips
        food_spending = categories.get("Food", 0)
        if food_spending > 4000:
            tips.append("Reduce eating out to twice a week to save on food costs.")
        elif food_spending > 2500:
            tips.append("Consider meal prepping to reduce food delivery expenses.")
        
        # Transport tips
        transport_spending = categories.get("Transport", 0)
        if transport_spending > 2000:
            tips.append("Try carpooling or using public transport to cut transport costs.")
        elif transport_spending > 1000:
            tips.append("Consider a monthly transport pass if available in your area.")
        
        # Shopping tips
        shopping_spending = categories.get("Shopping", 0)
        if shopping_spending > 5000:
            tips.append("Avoid online shopping for the next 7 days.")
            tips.append("Create a wishlist and wait 48 hours before making purchases.")
        elif shopping_spending > 3000:
            tips.append("Set a monthly shopping budget and stick to it.")
        
        # Entertainment tips
        entertainment_spending = categories.get("Entertainment", 0)
        if entertainment_spending > 2000:
            tips.append("Review your streaming subscriptions and cancel unused ones.")
        
        # Groceries tips
        groceries_spending = categories.get("Groceries", 0)
        if groceries_spending > 5000:
            tips.append("Plan weekly meals and make a shopping list to avoid impulse buys.")
        
        # General overspending tips
        if status == "overspending":
            tips.append("Review and cut non-essential expenses immediately.")
            tips.append("Track daily spending to stay aware of your budget.")
        
        # If spending is low, encourage saving
        if month_total < 15000 and status == "within_budget":
            tips.append("Great job staying within budget! Keep it up.")
        
        # Default tip if no specific recommendations
        if not tips:
            tips.append("Continue monitoring your spending habits.")
            tips.append("Look for opportunities to save on recurring expenses.")
        
        return tips
    
    def generate_investment_ideas(self, budget_analysis: Dict[str, Any]) -> List[str]:
        """
        Generate investment suggestions based on financial profile.
        
        Args:
            budget_analysis: Budget analysis data
            
        Returns:
            List of investment suggestions
        """
        ideas = []
        status = budget_analysis.get("status", "within_budget")
        month_total = budget_analysis.get("month_total", 0)
        limit = budget_analysis.get("limit", 30000)
        
        # Calculate potential savings
        potential_savings = limit - month_total
        
        if status == "within_budget":
            if potential_savings > 5000:
                ideas.append("Start a ₹2000 SIP in a diversified equity mutual fund.")
                ideas.append("Put 20% of your remaining budget into an emergency fund.")
                ideas.append("Consider opening a high-yield savings account for short-term goals.")
            elif potential_savings > 2000:
                ideas.append("Start a ₹1000 SIP in an index fund.")
                ideas.append("Put 10% of income into emergency fund.")
            else:
                ideas.append("Save at least ₹500 monthly for emergencies.")
        else:
            # Focus on building emergency fund first when overspending
            ideas.append("Focus on reducing expenses before starting new investments.")
            ideas.append("Build a small emergency fund of ₹5000 first.")
        
        # Always suggest emergency fund if not mentioned
        if not any("emergency" in idea.lower() for idea in ideas):
            ideas.append("Maintain an emergency fund equal to 6 months of expenses.")
        
        return ideas
    
    def calculate_saving_goal(self, budget_analysis: Dict[str, Any]) -> float:
        """
        Calculate monthly saving goal based on analysis.
        
        Args:
            budget_analysis: Budget analysis data
            
        Returns:
            Monthly saving goal amount
        """
        limit = budget_analysis.get("limit", 30000)
        month_total = budget_analysis.get("month_total", 0)
        status = budget_analysis.get("status", "within_budget")
        
        if status == "within_budget":
            # Aim to save 20% of budget limit
            return round(limit * 0.20, 2)
        else:
            # In overspending, aim to bring spending down
            projected = budget_analysis.get("projected_end_month", month_total)
            reduction_needed = projected - limit
            return round(reduction_needed * 0.5, 2)  # Start with 50% reduction
    
    def generate_summary(self, budget_analysis: Dict[str, Any], advice: Dict[str, Any]) -> str:
        """
        Generate a friendly, actionable summary for the user.
        
        Args:
            budget_analysis: Budget analysis data
            advice: Advice data
            
        Returns:
            Plain English summary
        """
        status = budget_analysis.get("status", "within_budget")
        month_total = budget_analysis.get("month_total", 0)
        limit = budget_analysis.get("limit", 30000)
        projected = budget_analysis.get("projected_end_month", month_total)
        
        if status == "overspending":
            summary = f"⚠️ Alert! You've spent ₹{month_total} so far, and you're on track to spend ₹{projected} by month-end, which exceeds your ₹{limit} budget. "
            summary += "It's time to cut back on non-essential expenses. "
            summary += f"Try to save ₹{advice['monthly_saving_goal']} this month by following the tips provided."
        else:
            summary = f"✅ Good news! You've spent ₹{month_total} so far, and you're projected to spend ₹{projected} by month-end, staying within your ₹{limit} budget. "
            summary += f"Keep up the good work and aim to save ₹{advice['monthly_saving_goal']} this month. "
            summary += "Check out the investment ideas to grow your wealth!"
        
        return summary
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process budget analysis and generate advice.
        
        Args:
            input_data: Dictionary containing budget analysis
            
        Returns:
            Dictionary with advice and complete output
        """
        budget_analysis = input_data.get("budget_analysis", {})
        
        # Generate advice components
        saving_goal = self.calculate_saving_goal(budget_analysis)
        actions = self.generate_saving_tips(budget_analysis)
        investment_ideas = self.generate_investment_ideas(budget_analysis)
        
        advice = {
            "monthly_saving_goal": saving_goal,
            "actions": actions,
            "investment_ideas": investment_ideas
        }
        
        # Generate summary
        summary = self.generate_summary(budget_analysis, advice)
        
        return {
            "advice": advice,
            "summary": summary
        }


if __name__ == "__main__":
    # Example usage
    sample_input = {
        "budget_analysis": {
            "month_total": 14200,
            "limit": 30000,
            "projected_end_month": 32000,
            "status": "overspending",
            "categories": {
                "Food": 3800,
                "Transport": 1200,
                "Shopping": 4200
            }
        }
    }
    
    agent = SavingAdvisorAgent()
    result = agent.process(sample_input)
    print(json.dumps(result, indent=2))
