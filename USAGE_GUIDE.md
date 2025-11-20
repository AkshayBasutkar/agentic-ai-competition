# Usage Guide - Multi-Agent Finance Intelligence System

## Table of Contents
1. [Quick Start](#quick-start)
2. [Input Format](#input-format)
3. [Running the System](#running-the-system)
4. [Understanding the Output](#understanding-the-output)
5. [Advanced Usage](#advanced-usage)
6. [Examples](#examples)

---

## Quick Start

### 1. Run with Example Data
```bash
python3 finance_system.py
```

### 2. Run with CLI (Recommended)
```bash
python3 cli.py example_input.json
```

### 3. Run with Custom Budget
```bash
python3 cli.py example_input.json 50000
```

---

## Input Format

Create a JSON file with your transactions:

```json
{
  "transactions": [
    {
      "date": "2024-01-15",
      "description": "Coffee at Starbucks",
      "amount": 350,
      "type": "debit",
      "mode": "UPI"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Required | Description | Example Values |
|-------|------|----------|-------------|----------------|
| date | string | Yes | Transaction date | "2024-01-15" |
| description | string | Yes | What you spent on | "Swiggy Order", "Uber Ride" |
| amount | number | Yes | Amount in ₹ | 350, 1200.50 |
| type | string | Yes | Transaction type | "debit", "credit" |
| mode | string | Yes | Payment method | "UPI", "Card", "Cash", "NetBanking" |

---

## Running the System

### Option 1: Using CLI (Best for Users)

```bash
# Basic usage
python3 cli.py your_transactions.json

# With custom budget
python3 cli.py your_transactions.json 40000

# View help
python3 cli.py --help
```

**Output:**
- Beautiful formatted console output
- Automatic JSON file saved as `your_transactions_output.json`

### Option 2: Using Python Script

```bash
python3 finance_system.py
```

### Option 3: Programmatic Usage

```python
from finance_system import FinanceIntelligenceSystem

# Initialize
system = FinanceIntelligenceSystem(budget_limit=30000)

# Your transactions
transactions = {
    "transactions": [
        {
            "date": "2024-01-15",
            "description": "Swiggy",
            "amount": 450,
            "type": "debit",
            "mode": "UPI"
        }
    ]
}

# Process
result = system.process(transactions)

# Access results
print(result["summary"])
print(f"Total spent: ₹{result['budget_analysis']['month_total']}")
```

---

## Understanding the Output

### 1. Categorized Transactions

Each transaction is automatically categorized:

```json
{
  "date": "2024-01-15",
  "description": "Swiggy Order",
  "amount": 450,
  "type": "debit",
  "mode": "UPI",
  "category": "Food"  // ← Automatically assigned
}
```

**Categories:**
- 🍔 **Food** - Restaurants, food delivery (Swiggy, Zomato)
- 🚗 **Transport** - Uber, Ola, fuel, parking
- 🛍️ **Shopping** - Amazon, Flipkart, Myntra, retail
- 🥕 **Groceries** - BigBasket, Blinkit, supermarkets
- 🎬 **Entertainment** - Netflix, movies, games
- 💡 **Bills** - Electricity, water, internet, rent
- 💳 **EMI** - Loan installments, credit card payments
- 💰 **Salary** - Income, wages
- 📈 **Investment** - Mutual funds, stocks, SIP
- 📦 **Miscellaneous** - Everything else

### 2. Budget Analysis

```json
{
  "month_total": 14200,          // Total spent this month
  "limit": 30000,                // Your budget limit
  "projected_end_month": 32000,  // Predicted month-end spending
  "status": "overspending",      // or "within_budget"
  "categories": {
    "Food": 3800,
    "Transport": 1200,
    "Shopping": 4200
  }
}
```

**Status Meanings:**
- ✅ **within_budget** - You're on track to stay within budget
- ⚠️ **overspending** - You're projected to exceed your budget

### 3. Financial Advice

```json
{
  "monthly_saving_goal": 5000,
  "actions": [
    "Reduce eating out to twice a week.",
    "Avoid online shopping for the next 7 days."
  ],
  "investment_ideas": [
    "Start a ₹1000 SIP in an index fund.",
    "Put 10% of income into emergency fund."
  ]
}
```

### 4. Summary

A plain English explanation of your financial situation with actionable advice.

---

## Advanced Usage

### Testing Individual Agents

```bash
# Test Category Agent
python3 category_agent.py

# Test Budget Agent
python3 budget_agent.py

# Test Advisor Agent
python3 advisor_agent.py
```

### Running Tests

```bash
python3 test_system.py
```

### Custom Budget Limits

```python
from finance_system import FinanceIntelligenceSystem

# Different budget scenarios
system_student = FinanceIntelligenceSystem(budget_limit=15000)
system_professional = FinanceIntelligenceSystem(budget_limit=50000)
system_family = FinanceIntelligenceSystem(budget_limit=100000)
```

---

## Examples

### Example 1: Normal Spending

**Input:** `example_input.json`
- 10 transactions
- ₹11,349 spent
- Budget: ₹30,000

**Result:**
```
Status: ✅ WITHIN_BUDGET
Projected: ₹17,023
Saving Goal: ₹6,000
```

### Example 2: Overspending

**Input:** `example_overspending.json`
- 15 transactions
- ₹31,129 spent
- Budget: ₹25,000

**Result:**
```
Status: ⚠️ OVERSPENDING
Projected: ₹46,693
Action Required: Cut non-essential expenses
```

---

## Tips for Best Results

### 1. Consistent Descriptions
Use recognizable brand names:
- ✅ "Swiggy Order" → Food
- ❌ "Food" → May categorize as Miscellaneous

### 2. Accurate Dates
Use actual transaction dates for better projections:
- Format: `YYYY-MM-DD`
- Current month transactions give better predictions

### 3. Complete Transactions
Include all transactions for accurate analysis:
- Include small purchases
- Don't forget cash transactions
- Add all credit card spends

### 4. Regular Updates
Update your transactions regularly:
- Weekly updates recommended
- Monthly at minimum
- Real-time for best results

### 5. Set Realistic Budgets
- Consider your income
- Account for fixed expenses (rent, EMIs)
- Leave room for unexpected costs

---

## Troubleshooting

### Issue: Wrong Category Assigned

**Solution:** The system uses keywords. If a transaction is miscategorized:
1. Make description more specific
2. Or, edit `category_agent.py` to add custom keywords

### Issue: Projection Seems Off

**Solution:** 
- Ensure dates are accurate
- Include more transactions from the month
- Projections improve with more data points

### Issue: No Investment Ideas

**Solution:**
- Focus on reducing expenses first
- Build emergency fund
- Once within budget, system suggests investments

---

## Real-World Usage Scenarios

### Scenario 1: Monthly Budget Review
```bash
# End of month check
python3 cli.py january_transactions.json 30000
```

### Scenario 2: Mid-Month Check-In
```bash
# See if you're on track
python3 cli.py transactions_so_far.json 30000
```

### Scenario 3: Budget Planning
```bash
# Test different budget limits
python3 cli.py transactions.json 25000
python3 cli.py transactions.json 35000
python3 cli.py transactions.json 45000
```

---

## Next Steps

1. ✅ Add your transactions to a JSON file
2. ✅ Run the system with your data
3. ✅ Review the advice provided
4. ✅ Take action on recommendations
5. ✅ Track progress weekly

**Remember:** The goal is financial awareness and smart spending, not restriction!

---

For detailed technical documentation, see [FINANCE_SYSTEM_README.md](FINANCE_SYSTEM_README.md)
