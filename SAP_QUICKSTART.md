# SAP Fiori Integration — Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python Dependencies (1 minute)

```bash
pip install playwright fastapi uvicorn requests
playwright install chromium
```

### Step 2: Start the SAP Server (30 seconds)

Open a terminal in the project directory and run:

```bash
python sap_fiori_server.py
```

Keep this terminal open while using the app.

### Step 3: Open the Dashboard (30 seconds)

Open `treasury_agent.html` in a web browser. You should see the new SAP Fiori section.

### Step 4: Enter SAP Credentials (2 minutes)

Fill in the form:

- **SAP Fiori URL:** Your S/4HANA instance URL (e.g., `https://sap-prod.accenture.com`)
- **Login ID:** Your SAP username
- **Password:** Your SAP password
- **Company Code:** E.g., `1000`, `2000`, etc.
- **Currency:** `USD`, `GBP`, `EUR`, etc.
- **As-of Date:** Auto-filled with today's date (change if needed)

### Step 5: Click "Fetch Cash Balances from SAP"

The dashboard will:
1. ✓ Connect to SAP Fiori
2. ✓ Extract cash balances for your company/currency/date
3. ✓ Auto-run the investment analysis pipeline

You'll see a message like: **"✓ Successfully fetched 4 accounts from SAP Fiori"**

---

## If It Doesn't Work

| Problem | Solution |
|---------|----------|
| **Connection Refused** | Is `sap_fiori_server.py` running? Check the terminal. |
| **SAP Login Failed** | Verify your username/password are correct. Check if your SAP account is locked. |
| **No Data Returned** | Try a different company code or currency. Verify the Cash Flow Analyzer app exists in your SAP instance. |
| **Playwright Error** | Run `playwright install chromium` and try again. |

---

## Alternative: Manual Script Execution

If the server approach doesn't work, you can run the fetcher manually:

```bash
python fetch_sap_cashflow.py
```

You'll be prompted for credentials. The script outputs `sap_cashflow_data.json` which you can then paste into the HTML app.

---

## File Reference

- `treasury_agent.html` — The main dashboard (open this in a browser).
- `sap_fiori_server.py` — Backend server (run in a terminal).
- `fetch_sap_cashflow.py` — Core SAP fetcher (called by the server).
- `SAP_FIORI_INTEGRATION.md` — Full documentation.

---

## Next: Run a Test

1. **Click "Fetch Cash Balances from SAP"** with your real SAP credentials.
2. **Wait** 10–20 seconds for the browser automation to complete.
3. **See results** in the dashboard: account names, balances, currencies.
4. **Auto-run** Steps 1–4 of the investment analysis pipeline.

That's it! 🎉
