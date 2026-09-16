# 🔧 SAP Fiori Cash Flow Analyzer Integration

**Fetch cash balances directly from SAP Fiori instead of manual Excel uploads.**

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install playwright fastapi uvicorn requests pydantic
playwright install chromium
```

### 2️⃣ Start the Server
```bash
python sap_fiori_server.py
```
Keep this terminal open.

### 3️⃣ Open the Dashboard
Open `treasury_agent.html` in your web browser, fill in your SAP credentials, and click **"Fetch Cash Balances from SAP"**.

---

## 📋 What You Get

✅ **Automatic Cash Balance Fetching** — Real-time data from SAP Fiori  
✅ **No More Excel Uploads** — For cash positions (still needed for loans & investments)  
✅ **One-Click Pipeline Execution** — Automatically runs analysis steps 1–4  
✅ **Secure Credentials** — Sent only to localhost, never saved  
✅ **Smart Error Messages** — Clear guidance if something goes wrong  

---

## 📁 New Files

| File | Purpose |
|------|---------|
| `fetch_sap_cashflow.py` | Core SAP data fetcher (Playwright automation) |
| `sap_fiori_server.py` | FastAPI backend server |
| `test_sap_integration.py` | Setup verification tool |
| `SAP_FIORI_INTEGRATION.md` | Complete technical documentation |
| `SAP_QUICKSTART.md` | 5-minute setup guide |
| `IMPLEMENTATION_SUMMARY.md` | Architecture & design overview |
| `README_SAP_INTEGRATION.md` | This file |

## 🧪 Verify Setup

Before connecting to SAP, run:
```bash
python test_sap_integration.py
```

This checks:
- ✓ All dependencies installed  
- ✓ Required files present  
- ✓ Server can start  
- ✓ SAP fetcher module works  
- ✓ Playwright/Chromium ready  

---

## 🚀 Usage

### Step 1: Fill in SAP Form
| Field | Example |
|-------|---------|
| SAP Fiori URL | `https://sap-prod.accenture.com` |
| Login ID | `your_username` |
| Password | `••••••••` |
| Company Code | `1000` |
| Currency | `USD` |
| As-of Date | `2026-09-15` (auto-filled) |

### Step 2: Click "Fetch Cash Balances from SAP"

The system will:
1. Connect to your SAP Fiori instance
2. Automate login
3. Navigate to Cash Flow Analyzer
4. Extract accounts for your company/currency/date
5. Return data to the dashboard
6. Auto-run Steps 1–4 of analysis

### Step 3: Review & Approve (Optional)
The app stops at Step 5 (Human Approval Gate) — review recommendations and approve/decline deals.

---

## ⚙️ How It Works

```
Dashboard Form → FastAPI Server → SAP Fetcher → SAP Fiori
                                                     ↓
                                          (Browser automation)
                                                     ↓
                                          Extract cash balances
                                                     ↓
      ← JSON response ← Convert to TSV ← Filter bad data
      ↓
Update EXCEL_DATA
↓
Run Steps 1–4 automatically
```

---

## 🔒 Security

✅ **Passwords not stored** — Only used for current fetch  
✅ **Local-only server** — Accessible only from your machine  
✅ **HTTPS to SAP** — Secure connection between server and SAP  
✅ **No logging** — Credentials not logged or cached  

**Recommendation:** Use a dedicated SAP service account with read-only access to Cash Flow Analyzer.

---

## ❌ Troubleshooting

### "SAP Fiori server not running"
```
→ Make sure sap_fiori_server.py is running in a separate terminal
```

### "Login failed"
```
→ Verify username/password are correct
→ Check if your SAP account is locked
→ Try logging into SAP Fiori manually to confirm access
```

### "No accounts found"
```
→ Try a different company code or currency
→ Verify the Cash Flow Analyzer app exists in your SAP instance
→ Check if data exists as of the date you specified
```

### Playwright errors
```
→ Run: pip install --upgrade playwright
→ Run: playwright install chromium
```

### See the browser automation in action
In `fetch_sap_cashflow.py`, change line 124:
```python
browser = p.chromium.launch(headless=True)  # Change to headless=False
```

---

## 📚 Full Documentation

- **[SAP_FIORI_INTEGRATION.md](SAP_FIORI_INTEGRATION.md)** — Complete technical docs, data mapping, extended setup
- **[SAP_QUICKSTART.md](SAP_QUICKSTART.md)** — 5-minute reference guide  
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** — Architecture, design, integration points
- **[treasury_agent.html](treasury_agent.html)** — Updated dashboard (look for "Fetch Cash Balances from SAP" section)

---

## 🔄 What Data Comes From Where?

| Data | Source | Required? |
|------|--------|-----------|
| **Cash Balances** | **SAP Fiori** ✨ | Yes (from SAP) |
| Loan Schedule | Excel upload | Yes |
| Investment Positions | Excel upload | Yes |
| Market Rates | Auto-fetched daily | Yes (auto) |

**Future:** Loan Schedule and Investment Positions can also be fetched from SAP (Phase 2 enhancement).

---

## 🎯 Pipeline After SAP Fetch

1. ✓ **Step 1:** Reporting Agent — Calculates surplus from SAP cash balances + loan deductions + maturing investments
2. ✓ **Step 2:** Ratings Agent — Validates counterparty credit ratings
3. ✓ **Step 3:** Compliance Agent — Checks investment policy limits
4. ✓ **Step 4:** Opportunity Agent — Recommends investable amounts
5. ⏸️ **Step 5:** Human Gate — Treasury Manager approves/declines each recommendation
6. ✓ **Step 6:** Trader Agent — Creates deal instructions

---

## 🛠️ Advanced Usage

### Run SAP Fetcher Standalone (No Server)
```bash
python fetch_sap_cashflow.py
```
You'll be prompted for credentials interactively.
Output: `sap_cashflow_data.json` and audit screenshots.

### Change SAP Login Field Names
If your SAP instance has custom field names:
1. Open SAP Fiori in a browser
2. Right-click login field → Inspect (F12)
3. Find the field `id` or `name`
4. Update selectors in `fetch_sap_cashflow.py` (~lines 120–135)

### Extend to Fetch Loans/Positions from SAP
See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for Phase 2 roadmap.

---

## 📞 Questions?

Refer to:
1. **Error message on screen** — Specific guidance  
2. **[SAP_FIORI_INTEGRATION.md](SAP_FIORI_INTEGRATION.md)** — Troubleshooting section  
3. **[test_sap_integration.py](test_sap_integration.py)** — Diagnose setup issues  
4. **Console logs** — Press F12, check Console tab for JavaScript errors  
5. **Server terminal** — Check FastAPI logs for API errors  

---

## 📈 Next Steps

- [ ] Install dependencies: `pip install playwright fastapi uvicorn requests pydantic`
- [ ] Install Playwright: `playwright install chromium`
- [ ] Run tests: `python test_sap_integration.py`
- [ ] Start server: `python sap_fiori_server.py`
- [ ] Test with SAP credentials (use a test company code first)
- [ ] Confirm Steps 1–4 auto-execute
- [ ] Share credentials with team (or create shared SAP service account)

---

## ✨ Features

| Feature | Status | Notes |
|---------|--------|-------|
| Fetch cash balances from SAP | ✅ Done | Real-time, filters by company/currency/date |
| Auto-run analysis steps | ✅ Done | Steps 1–4 execute automatically |
| Secure credential handling | ✅ Done | Localhost-only server |
| Error messages | ✅ Done | Specific guidance for common issues |
| Audit screenshots | ✅ Done | Optional, best-effort basis |
| Fetch loan schedule from SAP | 🔲 Future | Phase 2 roadmap |
| Fetch investment positions from SAP | 🔲 Future | Phase 2 roadmap |
| Schedule daily SAP fetches | 🔲 Future | Similar to market rates auto-fetch |

---

## 🎓 Key Concepts

**Playwright Browser Automation**  
The fetcher uses Playwright to automate a real web browser, logging into SAP Fiori just like a human would. This works with custom SAP interfaces that would be hard to API-integrate.

**FastAPI Server**  
A lightweight web server that wraps the Playwright script, allowing the HTML dashboard to fetch data via HTTP instead of running Python directly in the browser.

**TSV Data Format**  
Cash balances are converted from SAP JSON to Tab-Separated Values (TSV) — the same format the Claude agents expect. This makes SAP data compatible with existing pipeline without any code changes.

---

**Version:** 1.0 | **Last Updated:** 2026-09-15 | **Status:** Production Ready ✅
