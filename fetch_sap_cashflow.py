"""
SAP Fiori Cash Flow Analyzer integration — fetches cash balances and bank accounts.

Automates login and data extraction from SAP Fiori S/4HANA Cash Flow Analyzer app.
Inputs:
  - SAP Fiori URL (e.g., https://your-sap-instance.sapfioriapps.com)
  - Login credentials (username, password)
  - Company code (e.g., 1000)
  - Currency (e.g., USD)
  - As-of date (e.g., 2026-09-15)

Output:
  - JSON file (sap_cashflow_data.json) containing:
    - Bank accounts with cash balances
    - Account names
    - Currencies
    - Excludes "Bank Account Not Assigned" line items
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright

PROJECT_DIR = Path(__file__).resolve().parent


def fetch_sap_cashflow(
    sap_url: str,
    username: str,
    password: str,
    company_code: str,
    currency: str,
    as_of_date: str,
) -> dict:
    """
    Connect to SAP Fiori Cash Flow Analyzer and fetch cash balances.

    Returns:
      {
        "status": "success" or "error",
        "data": [
          {"account_id": "ACC-001", "account_name": "Main Operating", "bank_name": "Barclays Bank",
           "currency": "USD", "balance_date": "2026-09-15", "available_balance": 16700000,
           "ledger_balance": 16500000, "gross_surplus": 11700000},
          ...
        ],
        "message": "...",
        "fetched_at": "2026-09-15 14:32 UTC"
      }
    """

    try:
        with sync_playwright() as p:
            # Launch browser in headless mode
            browser = p.chromium.launch(headless=True, args=["--disable-http2"])
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            )
            page = context.new_page()

            try:
                # Navigate to SAP Fiori login
                print(f"Connecting to {sap_url}...", file=sys.stderr)
                page.goto(sap_url, timeout=45000, wait_until="load")
                page.wait_for_timeout(2000)

                # Handle login — look for typical SAP login form fields
                # Username field (could be "logon-userName" or "username" or similar)
                user_selectors = [
                    'input[id*="userName"]',
                    'input[id*="username"]',
                    'input[name*="user"]',
                    'input[aria-label*="User"]',
                    'input[placeholder*="User"]',
                ]

                password_selectors = [
                    'input[id*="password"]',
                    'input[id*="passwd"]',
                    'input[name*="pass"]',
                    'input[aria-label*="Password"]',
                    'input[placeholder*="Pass"]',
                    'input[type="password"]',
                ]

                # Find and fill username field
                user_field = None
                for selector in user_selectors:
                    try:
                        user_field = page.query_selector(selector)
                        if user_field:
                            break
                    except:
                        pass

                if not user_field:
                    raise RuntimeError("Could not locate username field on SAP login page")

                user_field.fill(username)
                print(f"Entered username: {username}", file=sys.stderr)

                # Find and fill password field
                pass_field = None
                for selector in password_selectors:
                    try:
                        pass_field = page.query_selector(selector)
                        if pass_field:
                            break
                    except:
                        pass

                if not pass_field:
                    raise RuntimeError("Could not locate password field on SAP login page")

                pass_field.fill(password)
                print("Entered password", file=sys.stderr)

                # Find and click login button
                login_btn = None
                login_selectors = [
                    'button:has-text("Log On")',
                    'button:has-text("Login")',
                    'button[id*="login"]',
                    'button[type="submit"]',
                    'a:has-text("Log On")',
                ]

                for selector in login_selectors:
                    try:
                        login_btn = page.query_selector(selector)
                        if login_btn:
                            break
                    except:
                        pass

                if login_btn:
                    login_btn.click()
                    page.wait_for_timeout(3000)
                    page.wait_for_load_state("load")
                    print("Clicked login button, waiting for page load...", file=sys.stderr)
                else:
                    raise RuntimeError("Could not locate login button")

                # Navigate to Cash Flow Analyzer tile/app
                # Look for the app link or navigate directly to it
                print("Looking for Cash Flow Analyzer app...", file=sys.stderr)
                page.wait_for_timeout(2000)

                # Try to find Cash Flow Analyzer link
                cfa_link = page.query_selector('a:has-text("Cash Flow")')
                if cfa_link:
                    cfa_link.click()
                    page.wait_for_load_state("load")
                    page.wait_for_timeout(2000)
                else:
                    # Try direct navigation
                    # This is a typical SAP Fiori app URL pattern
                    cfa_url = f"{sap_url.rstrip('/')}/ui#/Shell-home"
                    page.goto(cfa_url, timeout=45000, wait_until="load")

                # Wait for app to load
                page.wait_for_timeout(3000)

                # Look for input fields for company code, currency, date
                # These are typically search/filter fields in Fiori apps
                print(f"Entering filter criteria: Company={company_code}, Currency={currency}, Date={as_of_date}", file=sys.stderr)

                # Try to find and fill company code input
                company_field = page.query_selector('input[placeholder*="Company"]') or \
                               page.query_selector('input[aria-label*="Company"]') or \
                               page.query_selector('input[id*="company"]')

                if company_field:
                    company_field.fill(company_code)
                    page.wait_for_timeout(500)

                # Try to find and fill currency input
                currency_field = page.query_selector('input[placeholder*="Currency"]') or \
                                page.query_selector('input[aria-label*="Currency"]') or \
                                page.query_selector('input[id*="currency"]')

                if currency_field:
                    currency_field.fill(currency)
                    page.wait_for_timeout(500)

                # Try to find and fill date input
                date_field = page.query_selector('input[placeholder*="Date"]') or \
                            page.query_selector('input[aria-label*="Date"]') or \
                            page.query_selector('input[id*="date"]') or \
                            page.query_selector('input[type="date"]')

                if date_field:
                    date_field.fill(as_of_date)
                    page.wait_for_timeout(500)

                # Look for and click "Go" / "Search" / "Execute" button
                go_btn = page.query_selector('button:has-text("Go")') or \
                        page.query_selector('button:has-text("Search")') or \
                        page.query_selector('button:has-text("Execute")') or \
                        page.query_selector('button[aria-label*="Execute"]')

                if go_btn:
                    go_btn.click()
                    page.wait_for_load_state("load")
                    page.wait_for_timeout(2000)
                    print("Executed search, fetching results...", file=sys.stderr)

                # Wait for results table to load
                page.wait_for_timeout(3000)

                # Extract cash flow data from table
                # Look for table rows with data
                rows = page.query_selector_all("table tr, [role='row']")

                data = []
                for row in rows:
                    try:
                        cells = row.query_selector_all("td, [role='gridcell']")
                        if len(cells) >= 3:
                            # Parse cells — adjust indices based on actual SAP response structure
                            # Typical columns: Account ID | Account Name | Bank Name | Currency | Balance Date | Available Balance | Ledger Balance | Gross Surplus
                            cell_texts = [cell.inner_text() for cell in cells]

                            # Skip header rows and "Bank Account Not Assigned" rows
                            if any(h in cell_texts[0].upper() for h in ["ACCOUNT", "BANK"]):
                                continue

                            if any("NOT ASSIGNED" in text.upper() for text in cell_texts):
                                continue

                            # Build record
                            record = {
                                "account_id": cell_texts[0] if len(cell_texts) > 0 else "",
                                "account_name": cell_texts[1] if len(cell_texts) > 1 else "",
                                "bank_name": cell_texts[2] if len(cell_texts) > 2 else "",
                                "currency": cell_texts[3] if len(cell_texts) > 3 else currency,
                                "balance_date": as_of_date,
                                "available_balance": float(cell_texts[4].replace(",", "")) if len(cell_texts) > 4 else 0,
                                "ledger_balance": float(cell_texts[5].replace(",", "")) if len(cell_texts) > 5 else 0,
                                "gross_surplus": float(cell_texts[6].replace(",", "")) if len(cell_texts) > 6 else 0,
                            }

                            data.append(record)
                    except Exception as e:
                        print(f"Error parsing row: {e}", file=sys.stderr)
                        continue

                if not data:
                    return {
                        "status": "error",
                        "message": "No cash flow data extracted from SAP Fiori",
                        "data": [],
                        "fetched_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                    }

                return {
                    "status": "success",
                    "data": data,
                    "message": f"Successfully fetched {len(data)} bank accounts from SAP Fiori",
                    "fetched_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
                }

            finally:
                context.close()
                browser.close()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": [],
            "fetched_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        }


def main() -> int:
    """
    Fetch SAP Cash Flow data and save to JSON file.
    Inputs are read from environment variables or command-line arguments.
    """

    # Example usage — in production, these would come from the HTML form
    sap_url = input("SAP Fiori URL: ").strip()
    username = input("Login ID: ").strip()
    password = input("Password: ").strip()
    company_code = input("Company Code: ").strip()
    currency = input("Currency (e.g., USD): ").strip()
    as_of_date = input("As-of Date (YYYY-MM-DD): ").strip()

    if not all([sap_url, username, password, company_code, currency, as_of_date]):
        print("Error: All inputs are required", file=sys.stderr)
        return 1

    print(f"\nFetching cash flow data from SAP Fiori...", file=sys.stderr)
    result = fetch_sap_cashflow(sap_url, username, password, company_code, currency, as_of_date)

    # Save result to JSON
    json_path = PROJECT_DIR / "sap_cashflow_data.json"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"\nResult saved to {json_path}")
    print(json.dumps(result, indent=2))

    return 0 if result["status"] == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
