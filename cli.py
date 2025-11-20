#!/usr/bin/env python3
"""
Command-Line Interface for Multi-Agent Finance Intelligence System
"""
import json
import sys
from finance_system import FinanceIntelligenceSystem


def print_banner():
    """Print welcome banner."""
    print("=" * 80)
    print("MULTI-AGENT FINANCE INTELLIGENCE SYSTEM")
    print("=" * 80)
    print()


def print_help():
    """Print usage help."""
    print("Usage:")
    print("  python3 cli.py <input_file.json> [budget_limit]")
    print()
    print("Arguments:")
    print("  input_file.json  - JSON file containing transactions")
    print("  budget_limit     - Optional monthly budget limit (default: 30000)")
    print()
    print("Example:")
    print("  python3 cli.py example_input.json")
    print("  python3 cli.py example_input.json 50000")
    print()


def main():
    """Main CLI function."""
    print_banner()
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Error: Missing input file")
        print()
        print_help()
        sys.exit(1)
    
    if sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)
    
    input_file = sys.argv[1]
    budget_limit = 30000
    
    if len(sys.argv) > 2:
        try:
            budget_limit = float(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid budget limit '{sys.argv[2]}'. Using default: 30000")
            budget_limit = 30000
    
    # Read input file
    try:
        with open(input_file, 'r') as f:
            transactions = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        sys.exit(1)
    
    # Initialize system
    system = FinanceIntelligenceSystem(budget_limit=budget_limit)
    
    # Process transactions
    print(f"Processing {len(transactions.get('transactions', []))} transactions...")
    print(f"Budget limit: ₹{budget_limit}")
    print()
    
    result = system.process(transactions, budget_limit=budget_limit)
    
    # Display results
    print("=" * 80)
    print("CATEGORIZED TRANSACTIONS")
    print("=" * 80)
    print()
    for txn in result["categorized_transactions"]:
        print(f"{txn['date']} | {txn['description']:25s} | ₹{txn['amount']:8.2f} | {txn['category']:15s}")
    print()
    
    print("=" * 80)
    print("BUDGET ANALYSIS")
    print("=" * 80)
    print()
    analysis = result["budget_analysis"]
    print(f"Month Total:        ₹{analysis['month_total']:,.2f}")
    print(f"Budget Limit:       ₹{analysis['limit']:,.2f}")
    print(f"Projected End:      ₹{analysis['projected_end_month']:,.2f}")
    print(f"Status:             {analysis['status'].upper()}")
    print()
    print("Category Breakdown:")
    for category, amount in sorted(analysis['categories'].items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / analysis['month_total'] * 100) if analysis['month_total'] > 0 else 0
        print(f"  {category:15s} ₹{amount:8.2f} ({percentage:5.1f}%)")
    print()
    
    print("=" * 80)
    print("FINANCIAL ADVICE")
    print("=" * 80)
    print()
    advice = result["advice"]
    print(f"Monthly Saving Goal: ₹{advice['monthly_saving_goal']:,.2f}")
    print()
    print("Action Items:")
    for i, action in enumerate(advice['actions'], 1):
        print(f"  {i}. {action}")
    print()
    print("Investment Ideas:")
    for i, idea in enumerate(advice['investment_ideas'], 1):
        print(f"  {i}. {idea}")
    print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(result["summary"])
    print()
    print("=" * 80)
    
    # Option to save output
    output_file = input_file.replace('.json', '_output.json')
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nFull output saved to: {output_file}")
    except Exception as e:
        print(f"\nWarning: Could not save output file: {e}")


if __name__ == "__main__":
    main()
