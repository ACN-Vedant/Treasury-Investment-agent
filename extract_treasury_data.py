import pandas as pd
import json
import os

# Read the Excel file
excel_file = r"C:\Users\vedant.j.shah\OneDrive - Accenture\Desktop\AI Agents\Investment App connected with SAP\treasury_data - short version.xlsx"

# Read all sheets
xls = pd.ExcelFile(excel_file)
print(f"Sheet names: {xls.sheet_names}\n")

# Dictionary to store data
treasury_data = {}

# Read Cash Balances
try:
    df_cash = pd.read_excel(excel_file, sheet_name='Cash Balances')
    cash_balances = []
    for idx, row in df_cash.iterrows():
        cash_balances.append({
            "account_id": str(row.get('Account ID', f'ACC-{idx+1}')).strip(),
            "account_name": str(row.get('Account Name', '')).strip(),
            "available_balance": float(row.get('Available Balance', 0)) if pd.notna(row.get('Available Balance')) else 0,
            "min_operating_balance": float(row.get('Minimum Operating Balance', 0)) if pd.notna(row.get('Minimum Operating Balance')) else 0,
            "currency": str(row.get('Currency', 'EUR')).strip()
        })
    treasury_data['cash_balances'] = cash_balances
    print(f"Cash Balances found: {len(cash_balances)} accounts")
    print(json.dumps(cash_balances, indent=2))
except Exception as e:
    print(f"Error reading Cash Balances: {e}")
    treasury_data['cash_balances'] = []

print("\n" + "="*60 + "\n")

# Read Loan Schedule
try:
    df_loans = pd.read_excel(excel_file, sheet_name='Loan Schedule')
    loan_schedule = []
    for idx, row in df_loans.iterrows():
        loan_schedule.append({
            "loan_id": str(row.get('Loan ID', f'LN-{idx+1}')).strip(),
            "account_id": str(row.get('Account ID', '')).strip(),
            "principal": float(row.get('Principal Amount', 0)) if pd.notna(row.get('Principal Amount')) else 0,
            "interest": float(row.get('Interest Amount', 0)) if pd.notna(row.get('Interest Amount')) else 0,
            "due_date": str(row.get('Due Date', '')).strip(),
            "currency": str(row.get('Currency', 'EUR')).strip()
        })
    treasury_data['loan_schedule'] = loan_schedule
    print(f"Loan Schedule found: {len(loan_schedule)} loans")
    print(json.dumps(loan_schedule, indent=2))
except Exception as e:
    print(f"Error reading Loan Schedule: {e}")
    treasury_data['loan_schedule'] = []

print("\n" + "="*60 + "\n")

# Read Investment Positions
try:
    df_invest = pd.read_excel(excel_file, sheet_name='Investment Positions')
    investment_positions = []
    for idx, row in df_invest.iterrows():
        investment_positions.append({
            "position_id": str(row.get('Position ID', f'P-{idx+1}')).strip(),
            "counterparty": str(row.get('Counterparty', '')).strip(),
            "notional_amount": float(row.get('Notional Amount', 0)) if pd.notna(row.get('Notional Amount')) else 0,
            "yield_percent": float(row.get('Yield %', 0)) if pd.notna(row.get('Yield %')) else 0,
            "rating": str(row.get('Rating', 'BBB')).strip(),
            "maturity_date": str(row.get('Maturity Date', '')).strip(),
            "currency": str(row.get('Currency', 'EUR')).strip()
        })
    treasury_data['investment_positions'] = investment_positions
    print(f"Investment Positions found: {len(investment_positions)} positions")
    print(json.dumps(investment_positions, indent=2))
except Exception as e:
    print(f"Error reading Investment Positions: {e}")
    treasury_data['investment_positions'] = []

print("\n" + "="*60 + "\n")
print("COMPLETE TREASURY DATA JSON:\n")
print(json.dumps(treasury_data, indent=2))

# Save to JSON file
output_file = r"C:\Users\vedant.j.shah\OneDrive - Accenture\Desktop\AI Agents\Investment App connected with SAP\real_treasury_data.json"
with open(output_file, 'w') as f:
    json.dump(treasury_data, f, indent=2)
print(f"\n✓ Data saved to: {output_file}")
