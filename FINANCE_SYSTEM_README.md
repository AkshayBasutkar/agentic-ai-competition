# Multi-Agent Finance Intelligence System

A sophisticated multi-agent system that analyzes personal financial transactions, categorizes spending, predicts budget overruns, and provides personalized financial advice.

## 🌟 Overview

This system consists of three intelligent agents working in sequence:

1. **Category Agent** - Classifies transactions into spending categories
2. **Budget Agent** - Analyzes spending patterns and predicts monthly totals
3. **Saving Advisor Agent** - Provides personalized financial advice

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentic-ai-competition

# No additional installation needed!
```

### Running the System

```bash
# Run the complete system with example data
python3 finance_system.py

# Or test individual agents
python3 category_agent.py
python3 budget_agent.py
python3 advisor_agent.py
```

## 📊 Input Format

The system accepts transactions in the following JSON format:

```json
{
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "Coffee",
      "amount": 120,
      "type": "debit",
      "mode": "UPI"
    }
  ]
}
```

### Input Fields

- **date**: Transaction date in YYYY-MM-DD format
- **description**: Brief description of the transaction
- **amount**: Transaction amount (positive number)
- **type**: "debit" or "credit"
- **mode**: Payment mode (UPI, Card, Cash, NetBanking, etc.)

## 📤 Output Format

The system returns a comprehensive analysis:

```json
{
  "categorized_transactions": [...],
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
  },
  "advice": {
    "monthly_saving_goal": 5000,
    "actions": [
      "Reduce eating out to twice a week.",
      "Avoid online shopping for the next 7 days."
    ],
    "investment_ideas": [
      "Start a ₹1000 SIP in an index fund.",
      "Put 10% of income into emergency fund."
    ]
  },
  "summary": "Plain, friendly, actionable English summary for the user"
}
```

## 🤖 Agent Details

### 1. Category Agent

**Purpose**: Automatically categorizes transactions based on description, amount, and payment mode.

**Categories**:
- Food
- Transport
- Shopping
- Groceries
- Entertainment
- Bills
- EMI
- Salary
- Investment
- Miscellaneous

**Example Categorization**:
- "Swiggy" → Food
- "Uber" → Transport
- "Myntra" → Shopping
- "Netflix" → Entertainment

### 2. Budget Agent

**Purpose**: Analyzes spending patterns and predicts budget status.

**Calculations**:
- Total monthly spending
- Category-wise breakdown
- Projected end-of-month spending (based on burn rate)
- Budget status (within budget or overspending)

**Default Budget**: ₹30,000 (customizable)

### 3. Saving Advisor Agent

**Purpose**: Provides intelligent, actionable financial advice.

**Generates**:
- Personalized saving tips based on spending patterns
- Overspending alerts and emergency fixes
- Investment suggestions
- Monthly saving goals

## 💡 Usage Examples

### Example 1: Basic Usage

```python
from finance_system import FinanceIntelligenceSystem

# Initialize system
system = FinanceIntelligenceSystem(budget_limit=30000)

# Process transactions
transactions = {
    "transactions": [
        {
            "date": "2024-01-15",
            "description": "Swiggy Order",
            "amount": 450,
            "type": "debit",
            "mode": "UPI"
        }
    ]
}

result = system.process(transactions)
print(result["summary"])
```

### Example 2: Custom Budget Limit

```python
system = FinanceIntelligenceSystem(budget_limit=50000)
result = system.process(transactions, budget_limit=50000)
```

### Example 3: JSON Input/Output

```python
import json

system = FinanceIntelligenceSystem()

# Read from file
with open('example_input.json', 'r') as f:
    transactions = json.load(f)

result = system.process(transactions)

# Save to file
with open('output.json', 'w') as f:
    json.dump(result, f, indent=2)
```

## 🔧 Customization

### Adding New Categories

Edit `category_agent.py` and add to the `CATEGORY_KEYWORDS` dictionary:

```python
CATEGORY_KEYWORDS = {
    "YourCategory": ["keyword1", "keyword2", "keyword3"]
}
```

### Modifying Advice Logic

Edit `advisor_agent.py` to customize the advice generation in:
- `generate_saving_tips()`
- `generate_investment_ideas()`

### Adjusting Budget Predictions

Edit `budget_agent.py` to modify the prediction algorithm in:
- `predict_end_month_spending()`

## 📁 Project Structure

```
agentic-ai-competition/
├── category_agent.py          # Transaction categorization
├── budget_agent.py            # Budget analysis and predictions
├── advisor_agent.py           # Financial advice generation
├── finance_system.py          # Main orchestrator
├── example_input.json         # Sample input data
├── requirements.txt           # Dependencies (none needed)
├── FINANCE_SYSTEM_README.md   # This file
└── README.md                  # Repository README
```

## 🧪 Testing

Each agent can be tested independently:

```bash
# Test Category Agent
python3 category_agent.py

# Test Budget Agent
python3 budget_agent.py

# Test Advisor Agent
python3 advisor_agent.py

# Test complete system
python3 finance_system.py
```

## 🎯 Features

✅ **Zero External Dependencies** - Uses only Python standard library
✅ **Modular Design** - Each agent works independently
✅ **Smart Categorization** - Intelligent keyword-based classification
✅ **Predictive Analysis** - Projects end-of-month spending
✅ **Personalized Advice** - Context-aware financial recommendations
✅ **JSON API** - Easy integration with other systems
✅ **Extensible** - Easy to add new categories and rules

## 📝 Agent Workflow

```
User Input (Transactions)
         ↓
Category Agent (Categorize)
         ↓
Budget Agent (Analyze & Predict)
         ↓
Advisor Agent (Generate Advice)
         ↓
Final Output (JSON + Summary)
```

## 🤝 Contributing

Feel free to enhance the system by:
1. Adding more spending categories
2. Improving categorization logic
3. Enhancing prediction algorithms
4. Adding more personalized advice rules

## 📄 License

This project is part of the Agentic AI Competition.

## 👥 Author

Created as part of the Agentic AI Competition to demonstrate multi-agent system design and implementation.

---

**Happy Financial Planning! 💰**
