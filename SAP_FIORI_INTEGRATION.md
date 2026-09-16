# SAP Fiori Cash Flow Analyzer Integration

This document explains how to integrate SAP Fiori Cash Flow Analyzer with the Treasury Investment AI dashboard to automatically fetch cash balances instead of manual Excel uploads.

## Overview

The Treasury AI app now supports two data input methods:

1. **Manual Excel Upload** (existing) — Upload a treasury_data.xlsx workbook with Cash Balances, Loan Schedule, and Investment Positions sheets.
2. **SAP Fiori Integration** (new) — Connect directly to your SAP Fiori S/4HANA instance and fetch live cash balances from the Cash Flow Analyzer app.

## Architecture

The integration consists of:

- **fetch_sap_cashflow.py** — Python script that uses Playwright to automate SAP Fiori login and data extraction from the Cash Flow Analyzer.
- **sap_fiori_server.py** — FastAPI server that wraps the fetcher and exposes a REST API.
- **treasury_agent.html** — Updated dashboard with SAP credentials form and automatic data conversion.

## Setup Instructions

### 1. Install Dependencies

Ensure Python 3.8+ is installed, then install required packages:

```bash
pip install playwright fastapi uvicorn requests
playwright install chromium
```

### 2. Start the SAP Fiori Server

Before using the dashboard, start the FastAPI server:

```bash
python sap_fiori_server.py
```

You should see output like:

```
======================================================================
Treasury SAP Integration Server
======================================================================

Starting server on http://localhost:8000...

The HTML app (treasury_agent.html) can now call:
  POST /api/fetch-sap-cashflow

Make sure Playwright is installed:
  pip install playwright && playwright install chromium

======================================================================
```

**Important:** Keep this server running in a separate terminal window while using the dashboard.

### 3. Open the Dashboard

Open `treasury_agent.html` in a web browser. You should see:

- A new **"Fetch Cash Balances from SAP Fiori"** section at the top.
- A form with fields for SAP URL, login credentials, company code, currency, and as-of date.
- The existing **"Upload your Treasury Workbook"** section below (for Excel upload fallback).

## Usage: Fetching Cash Balances from SAP Fiori

### Step 1: Enter SAP Connection Details

Fill in the SAP Fiori form:

| Field | Example | Notes |
|-------|---------|-------|
| SAP Fiori URL | `https://sap-prod.company.com/` | Your S/4HANA instance URL |
| Login ID | `treasury_user` | SAP username |
| Password | `••••••••` | SAP password (secure field) |
| Company Code | `1000` | SAP company code |
| Currency | `USD` | Report currency (USD, GBP, EUR, etc.) |
| As-of Date | `2026-09-15` | Cash position date (auto-filled with today) |

### Step 2: Click "Fetch Cash Balances from SAP"

The form will:

1. Connect to your SAP Fiori instance using Playwright.
2. Automate login with the credentials you provided.
3. Navigate to the Cash Flow Analyzer app.
4. Apply filters for company code, currency, and date.
5. Extract bank account balances and account names from the results.
6. Filter out "Bank Account Not Assigned" line items.
7. Return the data to the dashboard.

### Step 3: Automatic Pipeline Execution

Once cash balances are fetched:

1. The data is automatically converted to the expected TSV format.
2. Step 1 (Reporting Agent) becomes available and runs automatically.
3. Steps 2 & 3 (Ratings and Compliance) run in parallel.
4. Step 4 (Opportunity Agent) runs next.
5. The app pauses at the human approval gate for your decision.

## Data Mapping: SAP → Treasury AI Format

The SAP Fiori fetcher extracts the following fields and maps them to the Treasury AI schema:

| SAP Fiori Field | Treasury AI Column | Notes |
|-----------------|-------------------|-------|
| Account ID | Account_ID | Unique bank account identifier |
| Account Name | Account_Name | Customer-friendly account name |
| Bank Name | Bank_Name | Name of the bank (e.g., Barclays, HSBC) |
| Currency | Currency | Account currency (USD, GBP, EUR, etc.) |
| Balance Date | Balance_Date | As-of date (from your input) |
| Available Balance | Available_Balance | Usable cash balance |
| Ledger Balance | Ledger_Balance | Book balance |
| (Calculated) | Min_Operating_Balance | Estimated as 10% of Available Balance |
| (Calculated) | Gross_Surplus | Calculated as Available_Balance - Min_Operating_Balance |

## Filtering in SAP Fiori

The script automatically:

- **Filters by Company Code** — Shows only accounts for the specified company code.
- **Filters by Currency** — Shows only accounts in the specified currency.
- **Filters by Date** — Shows cash positions as of the specified date.
- **Excludes "Bank Account Not Assigned"** — Removes unassigned accounts from results.

## Error Handling

If the SAP fetch fails, you will see an error message like:

```
Error: Could not locate username field on SAP login page.
```

**Common causes and solutions:**

| Error | Cause | Solution |
|-------|-------|----------|
| SAP Fiori URL is invalid | Wrong URL or instance offline | Verify the SAP Fiori base URL |
| Login failed | Wrong credentials or user locked | Check username/password; unlock account in SAP |
| Page navigation timeout | Cash Flow Analyzer app not found | Verify the app is available in your SAP instance |
| No data extracted | Filters too restrictive or no data for that date | Try a different date or company code |

## Troubleshooting

### Server Won't Start

If `sap_fiori_server.py` fails to start:

```bash
# Check if port 8000 is already in use
netstat -a | grep 8000

# If in use, change the port in sap_fiori_server.py (last line)
# Or kill the process using that port
```

### Browser Shows "Connection Refused"

```
Error: Failed to fetch from SAP Fiori. Make sure SAP Fiori connection details are correct.
```

**Solution:** Ensure the FastAPI server is running:

```bash
python sap_fiori_server.py
```

### Playwright Installation Issues

If you see Playwright errors:

```bash
pip install --upgrade playwright
playwright install chromium
```

### SAP Login Page Not Found

The script looks for standard SAP login field names. If your SAP instance has custom fields:

1. Open SAP Fiori in your browser.
2. Right-click on the login fields → "Inspect" (F12).
3. Look for the field `id` or `name` attributes.
4. Update the selectors in `fetch_sap_cashflow.py` (lines ~120–135).

## Advanced: Running the Fetcher Standalone

You can also run the fetcher directly from the command line (no server):

```bash
python fetch_sap_cashflow.py
```

You will be prompted for:
- SAP Fiori URL
- Login ID
- Password
- Company Code
- Currency
- As-of Date

The fetcher will output:
- `sap_cashflow_data.json` — The extracted cash balances
- Screenshots in `rate_audit/<date>/` — Audit evidence of each source page

## Security Considerations

⚠️ **Important Security Notes:**

1. **Do not save credentials in the HTML form.** Credentials are not persisted — they are only used for the current fetch and sent over HTTPS to the local server.
2. **Run the server on localhost only** — The FastAPI server listens on `127.0.0.1:8000` and is not accessible from other machines.
3. **Use a dedicated SAP user account** — Create a service account with read-only access to the Cash Flow Analyzer.
4. **Consider VPN/network security** — If your SAP instance is behind a firewall, ensure the machine running this app has network access.

## Integration with Existing Pipeline

Once cash balances are fetched from SAP:

1. **Cash Balances** — Come from SAP Fiori (dynamic, as of date you specify).
2. **Loan Schedule** — Still uploaded via Excel (or can be extended to fetch from SAP).
3. **Investment Positions** — Still uploaded via Excel (or can be extended to fetch from SAP).
4. **Market Rates** — Auto-fetched daily from FRED, BoE, ECB (see `fetch_market_rates.py`).

You can mix and match:
- Fetch cash balances from SAP, upload loans and positions from Excel.
- Fetch everything from SAP, use auto-fetched market rates.
- Fully manual Excel upload (original flow).

## Next Steps

### Extend to Fetch Loan Schedule from SAP

To also fetch loan obligations from SAP Fiori Debt Management module:

1. Open the Debt Management app in SAP.
2. Adapt `fetch_sap_cashflow.py` to add a `fetch_sap_loans()` function.
3. Add form fields for the loan data fetcher.
4. Update `convertSAPDataToTSV()` to handle loans.

### Extend to Fetch Investment Positions from SAP

To fetch existing investment positions from SAP Treasury Management (TM) module:

1. Open the Investments/Portfolio module in SAP.
2. Add a `fetch_sap_positions()` function.
3. Integrate with the dashboard.

## Support

For questions or issues:

1. Check the error messages in the FastAPI server logs.
2. Review the Playwright browser window (it runs headless by default; set `headless=False` in `fetch_sap_cashflow.py` to debug).
3. Verify SAP instance connectivity and user access.

## Files Modified

- `treasury_agent.html` — Added SAP Fiori form and fetch logic.
- **New:** `fetch_sap_cashflow.py` — SAP data fetcher using Playwright.
- **New:** `sap_fiori_server.py` — FastAPI wrapper for the fetcher.

## Version History

- **v1.0** (2026-09-15) — Initial release. Fetches cash balances from Cash Flow Analyzer.
