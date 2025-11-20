"""
Test suite for Multi-Agent Finance Intelligence System
"""
import json
from category_agent import CategoryAgent
from budget_agent import BudgetAgent
from advisor_agent import SavingAdvisorAgent
from finance_system import FinanceIntelligenceSystem


def test_category_agent():
    """Test Category Agent functionality."""
    print("Testing Category Agent...")
    
    agent = CategoryAgent()
    
    test_input = {
        "transactions": [
            {"date": "2024-01-01", "description": "Swiggy", "amount": 300, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-02", "description": "Uber", "amount": 150, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-03", "description": "Amazon", "amount": 2000, "type": "debit", "mode": "Card"},
            {"date": "2024-01-04", "description": "Salary Credit", "amount": 50000, "type": "credit", "mode": "NEFT"},
            {"date": "2024-01-05", "description": "Netflix", "amount": 649, "type": "debit", "mode": "Card"},
        ]
    }
    
    result = agent.process(test_input)
    
    # Verify categories
    categories = [t["category"] for t in result["categorized_transactions"]]
    
    assert categories[0] == "Food", f"Expected 'Food', got '{categories[0]}'"
    assert categories[1] == "Transport", f"Expected 'Transport', got '{categories[1]}'"
    assert categories[2] == "Shopping", f"Expected 'Shopping', got '{categories[2]}'"
    assert categories[3] == "Salary", f"Expected 'Salary', got '{categories[3]}'"
    assert categories[4] == "Entertainment", f"Expected 'Entertainment', got '{categories[4]}'"
    
    print("✅ Category Agent tests passed!")
    return True


def test_budget_agent():
    """Test Budget Agent functionality."""
    print("Testing Budget Agent...")
    
    agent = BudgetAgent(budget_limit=30000)
    
    test_input = {
        "categorized_transactions": [
            {"date": "2024-01-01", "description": "Food", "amount": 500, "type": "debit", "mode": "UPI", "category": "Food"},
            {"date": "2024-01-02", "description": "Transport", "amount": 200, "type": "debit", "mode": "UPI", "category": "Transport"},
            {"date": "2024-01-03", "description": "Shopping", "amount": 3000, "type": "debit", "mode": "Card", "category": "Shopping"},
        ]
    }
    
    result = agent.process(test_input)
    analysis = result["budget_analysis"]
    
    # Verify calculations
    assert analysis["month_total"] == 3700, f"Expected 3700, got {analysis['month_total']}"
    assert analysis["limit"] == 30000, f"Expected 30000, got {analysis['limit']}"
    assert "Food" in analysis["categories"], "Food category missing"
    assert analysis["categories"]["Food"] == 500, f"Expected 500, got {analysis['categories']['Food']}"
    assert analysis["status"] in ["within_budget", "overspending"], f"Invalid status: {analysis['status']}"
    
    print("✅ Budget Agent tests passed!")
    return True


def test_advisor_agent():
    """Test Advisor Agent functionality."""
    print("Testing Advisor Agent...")
    
    agent = SavingAdvisorAgent()
    
    # Test overspending scenario
    test_input_overspending = {
        "budget_analysis": {
            "month_total": 25000,
            "limit": 30000,
            "projected_end_month": 35000,
            "status": "overspending",
            "categories": {
                "Food": 5000,
                "Shopping": 8000,
                "Transport": 2000
            }
        }
    }
    
    result = agent.process(test_input_overspending)
    advice = result["advice"]
    
    assert "monthly_saving_goal" in advice, "Missing monthly_saving_goal"
    assert "actions" in advice and len(advice["actions"]) > 0, "Missing actions"
    assert "investment_ideas" in advice and len(advice["investment_ideas"]) > 0, "Missing investment_ideas"
    assert "summary" in result, "Missing summary"
    assert len(result["summary"]) > 0, "Empty summary"
    
    # Test within budget scenario
    test_input_good = {
        "budget_analysis": {
            "month_total": 15000,
            "limit": 30000,
            "projected_end_month": 20000,
            "status": "within_budget",
            "categories": {
                "Food": 3000,
                "Shopping": 4000,
                "Transport": 1000
            }
        }
    }
    
    result = agent.process(test_input_good)
    assert "summary" in result, "Missing summary"
    
    print("✅ Advisor Agent tests passed!")
    return True


def test_complete_system():
    """Test complete system integration."""
    print("Testing Complete System...")
    
    system = FinanceIntelligenceSystem(budget_limit=30000)
    
    test_transactions = {
        "transactions": [
            {"date": "2024-01-01", "description": "Swiggy Order", "amount": 400, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-02", "description": "Uber Ride", "amount": 150, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-03", "description": "Myntra Shopping", "amount": 2500, "type": "debit", "mode": "Card"},
            {"date": "2024-01-04", "description": "BigBasket", "amount": 1500, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-05", "description": "Netflix", "amount": 649, "type": "debit", "mode": "Card"},
        ]
    }
    
    result = system.process(test_transactions)
    
    # Verify all sections are present
    assert "categorized_transactions" in result, "Missing categorized_transactions"
    assert "budget_analysis" in result, "Missing budget_analysis"
    assert "advice" in result, "Missing advice"
    assert "summary" in result, "Missing summary"
    
    # Verify data integrity
    assert len(result["categorized_transactions"]) == 5, "Wrong number of transactions"
    assert all("category" in t for t in result["categorized_transactions"]), "Missing categories"
    
    # Verify budget analysis
    analysis = result["budget_analysis"]
    assert analysis["month_total"] == 5199, f"Expected 5199, got {analysis['month_total']}"
    
    # Verify advice structure
    advice = result["advice"]
    assert isinstance(advice["monthly_saving_goal"], (int, float)), "Invalid saving goal type"
    assert isinstance(advice["actions"], list), "Actions should be a list"
    assert isinstance(advice["investment_ideas"], list), "Investment ideas should be a list"
    
    # Verify summary
    assert isinstance(result["summary"], str), "Summary should be a string"
    assert len(result["summary"]) > 50, "Summary too short"
    
    print("✅ Complete System tests passed!")
    return True


def test_edge_cases():
    """Test edge cases."""
    print("Testing Edge Cases...")
    
    system = FinanceIntelligenceSystem(budget_limit=30000)
    
    # Test with no transactions
    empty_input = {"transactions": []}
    result = system.process(empty_input)
    assert result["budget_analysis"]["month_total"] == 0, "Should handle empty transactions"
    
    # Test with only credit transactions
    credit_only = {
        "transactions": [
            {"date": "2024-01-01", "description": "Salary", "amount": 50000, "type": "credit", "mode": "NEFT"}
        ]
    }
    result = system.process(credit_only)
    assert result["budget_analysis"]["month_total"] == 0, "Should ignore credit transactions in spending"
    
    # Test with mixed case descriptions
    mixed_case = {
        "transactions": [
            {"date": "2024-01-01", "description": "SWIGGY ORDER", "amount": 300, "type": "debit", "mode": "UPI"},
            {"date": "2024-01-02", "description": "uber ride", "amount": 150, "type": "debit", "mode": "UPI"},
        ]
    }
    result = system.process(mixed_case)
    categories = [t["category"] for t in result["categorized_transactions"]]
    assert "Food" in categories, "Should handle uppercase"
    assert "Transport" in categories, "Should handle lowercase"
    
    print("✅ Edge case tests passed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("RUNNING TEST SUITE FOR MULTI-AGENT FINANCE INTELLIGENCE SYSTEM")
    print("=" * 80)
    print()
    
    tests = [
        test_category_agent,
        test_budget_agent,
        test_advisor_agent,
        test_complete_system,
        test_edge_cases,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"❌ Test failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ Test error: {e}")
            failed += 1
        print()
    
    print("=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
