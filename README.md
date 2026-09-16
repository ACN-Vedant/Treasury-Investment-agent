# Treasury Investment AI Agent

**Intelligent treasury management and investment analysis powered by free AI, with optional SAP Fiori integration for real-time treasury data.**

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-ACN--Vedant-blue?logo=github)](https://github.com/ACN-Vedant/Treasury-Investment-agent)

---

## 📋 Overview

Treasury Investment AI is a **standalone web-based application** that provides comprehensive treasury management and investment analysis. It features:

- **100% Standalone** - Runs entirely in the browser, no server required
- **Free AI Analysis** - Local analysis using built-in algorithms (no API keys needed)
- **SAP Fiori Integration** - Optional connection to SAP Treasury Position Management (TPM13)
- **4-Step Analysis Pipeline** - Automated reporting, ratings, compliance, and opportunity analysis
- **Real-Time Market Rates** - Auto-fetch rates from FRED, Bank of England, and ECB

---

## 🚀 Quick Start

### **Option 1: Standalone (No Server Required)**

1. **Download and open in browser:**
   ```bash
   # Clone the repository
   git clone https://github.com/ACN-Vedant/Treasury-Investment-agent.git
   cd Treasury-Investment-agent
   
   # Open in your browser
   # Double-click: treasury_ai_free.html
   ```

2. **Enter your treasury data** (JSON format) or click "Load Sample Data"

3. **Click "Run Analysis Pipeline"** and view the 4-step analysis:
   - Step 1: Treasury Reporting (surplus analysis)
   - Step 2: Credit Ratings Assessment
   - Step 3: Compliance Check
   - Step 4: Investment Recommendations

### **Option 2: With SAP Fiori Integration**

1. **Start the SAP server:**
   ```bash
   python sap_fiori_server.py
   ```

2. **Open treasury_agent.html** in your browser

3. **Enter your SAP credentials** and click "Fetch SAP Data & Run Analysis"

---

## ✨ Features

### **Treasury Data Analysis**
- **Surplus Calculation** - Analyze cash positions with margin haircut adjustment
- **Loan Obligation Tracking** - Monitor debt obligations across accounts
- **Investment Positioning** - Track existing investments and maturities
- **Multi-Currency Support** - Handle USD, GBP, EUR, and other currencies

### **AI-Powered Assessment**
- **Credit Ratings Analysis** - Validate counterparty creditworthiness
- **Compliance Checking** - Verify policy adherence (tenor, ratings, products)
- **Investment Recommendations** - Suggest optimal allocation strategies
- **Risk Assessment** - Identify counterparty and market risks

### **SAP Integration** (Optional)
- **Automated Login** - Playwright-based browser automation
- **Real-Time Fetching** - Pull live data from SAP Fiori TPM13
- **Complete Treasury Picture** - Cash, loans, and investments in one connection
- **Background Processing** - Non-blocking data retrieval

### **Market Data** (Optional)
- **FRED Rates** - Federal Reserve Economic Data rates
- **Bank of England Rates** - UK market rates (SONIA, etc.)
- **ECB Rates** - European Central Bank rates (ESTR, etc.)
- **Daily Auto-Fetch** - Scheduled rate updates via Windows Task Scheduler

---

## 📁 File Structure

```
Treasury-Investment-agent/
├── README.md                          # This file
├── .gitignore                         # Git configuration
│
├── CORE APPLICATION
├── treasury_ai_free.html              # Main standalone app (no server)
├── treasury_agent.html                # SAP-integrated dashboard
├── treasury_ai_claude.html            # Claude API variant
│
├── BACKEND SERVICES
├── sap_fiori_server.py                # FastAPI server for SAP automation
├── fetch_sap_treasury_data.py         # Comprehensive treasury fetcher
├── fetch_sap_cashflow.py              # Cash balance fetcher
├── fetch_market_rates.py              # Market rate fetcher
│
├── TESTING & VERIFICATION
├── test_sap_integration.py            # Integration test suite
│
├── DOCUMENTATION
├── SAP_FIORI_INTEGRATION.md           # SAP setup and integration guide
├── SAP_QUICKSTART.md                  # 5-minute quick start
├── TPM13_INTEGRATION_UPDATE.md        # TPM13 comprehensive guide
├── README_SAP_INTEGRATION.md          # Detailed integration documentation
├── IMPLEMENTATION_SUMMARY.md          # Architecture and design overview
├── [00-06]_*_agent.md                 # Agent documentation (analysis steps)
│
├── DATA FILES
├── treasury_sample_data.xlsx          # Sample treasury data
├── treasury_data - short version.xlsx # Condensed sample data
│
├── CONFIGURATION
├── register_daily_task.ps1            # Windows Task Scheduler setup
├── market_rates.js                    # Market rate helper functions
│
└── AUDIT & LOGS
   └── rate_audit/                     # Market rate audit screenshots
```

---

## 🔧 Installation & Setup

### **Prerequisites**
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Python 3.8+ (for SAP integration)
- Git

### **Standalone Installation**
```bash
git clone https://github.com/ACN-Vedant/Treasury-Investment-agent.git
cd Treasury-Investment-agent

# Just open treasury_ai_free.html in your browser!
```

### **SAP Integration Installation**
```bash
# Install Python dependencies
pip install fastapi uvicorn playwright

# Install Playwright browser
playwright install chromium

# Start the server
python sap_fiori_server.py

# Server runs on http://localhost:8000
```

### **Market Rate Auto-Fetching** (Optional)
```powershell
# Run the scheduler setup (Windows only)
.\register_daily_task.ps1

# This schedules daily market rate fetches at 7:00 AM
```

---

## 📊 How It Works

### **Data Input**
```json
{
  "cash_balances": [
    {
      "account_id": "ACC-001",
      "name": "Operating Account",
      "bank": "Barclays",
      "gross_surplus": 7500000
    }
  ],
  "loan_schedule": [
    {
      "loan_id": "LN-001",
      "principal": 2500000,
      "interest": 112500,
      "due": "30/06/2026"
    }
  ],
  "investment_positions": [
    {
      "counterparty": "JPMorgan",
      "amount": 3500000,
      "yield": 5.35,
      "rating": "AAA"
    }
  ]
}
```

### **Analysis Pipeline**

#### **Step 1: Treasury Reporting**
- Calculate net investable surplus per account
- Apply margin haircut (configurable: 0-100%)
- Identify available funds for investment

#### **Step 2: Credit Ratings Assessment**
- Validate counterparty credit ratings
- Check compliance with policy minimums (default: A-)
- Flag below-threshold counterparties

#### **Step 3: Compliance Check**
- Verify tenor limits (default: 180 days max)
- Validate product types (Fixed Deposit, T-Bill, CP)
- Check rating compliance per position

#### **Step 4: Investment Recommendations**
- Suggest optimal investment allocations
- Rank by yield and risk adjustment
- Provide portfolio composition breakdown

---

## 🎯 Usage Examples

### **Example 1: Quick Demo (No Server)**
```bash
# Open in browser
# Click "Load Sample Data"
# Adjust margin haircut if needed (default: 5%)
# Click "Run Analysis Pipeline"
# View all 4 steps of analysis
```

### **Example 2: Custom Data Analysis**
```bash
# Paste your treasury data (JSON) into the text area
# Configure analysis settings:
#   - Margin Haircut: Your buffer percentage
#   - Company Code: Your organization code
# Click "Run Analysis Pipeline"
# Export results from each tab
```

### **Example 3: SAP Live Connection**
```bash
# Start server: python sap_fiori_server.py
# Open treasury_agent.html
# Enter SAP credentials:
#   - SAP URL: https://your-sap-instance.com
#   - Username: your.username
#   - Password: your.password
#   - Company Code: 1000
#   - Currency: USD
# Click "Fetch SAP Data & Run Analysis"
# App fetches and analyzes live SAP data
```

---

## 🔑 Configuration

### **Analysis Settings**
- **Margin Haircut (%)** - Risk buffer applied to surplus (0-100%)
- **Company Code** - Your organization code
- **Policy Minimum Rating** - Default: A- (AA-, AAA, A, BBB+, etc.)
- **Max Tenor** - Default: 180 days

### **SAP Integration Settings**
Edit `sap_fiori_server.py`:
```python
# Server configuration
host = "127.0.0.1"
port = 8000

# Timeout settings
timeout = 45000  # milliseconds
```

### **Market Rate Fetching**
Edit `fetch_market_rates.py`:
```python
# Add your preferred sources
FRED_API_KEY = "your_api_key"  # Optional
BOE_ENDPOINT = "https://..."
ECB_ENDPOINT = "https://..."
```

---

## 🧪 Testing

Run the integration test suite:
```bash
python test_sap_integration.py
```

This verifies:
- ✓ Module dependencies
- ✓ File structure
- ✓ Server health
- ✓ SAP fetcher functions
- ✓ Playwright installation

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [SAP_FIORI_INTEGRATION.md](SAP_FIORI_INTEGRATION.md) | Complete SAP setup and integration guide |
| [SAP_QUICKSTART.md](SAP_QUICKSTART.md) | 5-minute quick start for SAP integration |
| [TPM13_INTEGRATION_UPDATE.md](TPM13_INTEGRATION_UPDATE.md) | Detailed TPM13 Treasury Position guide |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Architecture and design documentation |
| [README_SAP_INTEGRATION.md](README_SAP_INTEGRATION.md) | Integration troubleshooting guide |

---

## 🏗️ Architecture

### **Standalone Mode (Recommended)**
```
Browser (treasury_ai_free.html)
    ↓
[HTML/CSS/JavaScript]
    ↓
Local Analysis Engine
    ↓
Results Display (4-step tabs)
```

### **SAP Integration Mode**
```
Browser (treasury_agent.html)
    ↓
FastAPI Server (sap_fiori_server.py)
    ↓
Playwright Browser Automation
    ↓
SAP Fiori TPM13
    ↓
Treasury Data Extraction
    ↓
JSON Response
    ↓
Local Analysis Engine
    ↓
Results Display
```

---

## 🔐 Security

- **No API Keys Required** - Standalone mode uses no external APIs
- **Local Processing** - All analysis happens in your browser
- **SAP Credentials** - Only sent to your SAP instance, not stored
- **Market Rates** - Fetched from official sources (FRED, BoE, ECB)
- **No Telemetry** - Zero data collection

---

## 🐛 Troubleshooting

### **Standalone App Issues**

**JSON Parse Error**
- Ensure your treasury data is valid JSON
- Use the "Load Sample Data" button for format reference

**Missing Results**
- Check browser console for errors (F12)
- Ensure all required data fields are present

### **SAP Integration Issues**

**"Repository not found" error**
- Verify SAP URL is correct
- Check network connectivity
- Confirm SAP Fiori is accessible

**"Navigation is interrupted" error**
- Increase timeout in `sap_fiori_server.py`
- Check SAP server responsiveness
- Try disabling JavaScript caching

**Playwright timeout**
```bash
# Increase timeout (in milliseconds)
timeout = 60000  # 60 seconds
```

See [README_SAP_INTEGRATION.md](README_SAP_INTEGRATION.md) for detailed troubleshooting.

---

## 🎓 Learning Resources

- **[Agent Framework Documentation](00_overview.md)** - Understanding the analysis agents
- **[Reporting Agent](01_reporting_agent.md)** - Surplus calculation details
- **[Ratings Agent](02_ratings_agent.md)** - Credit assessment logic
- **[Compliance Agent](03_compliance_agent.md)** - Policy validation
- **[Opportunity Agent](04_opportunity_agent.md)** - Investment recommendations

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:
- Additional market data sources
- More currencies and instruments
- Advanced portfolio optimization
- Risk analytics expansion
- UI/UX improvements

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Vedant Shah**  
Accenture | Treasury & Investment Management  
Email: vedant.j.shah@accenture.com

---

## 🙏 Acknowledgments

- Claude AI for analysis pipeline logic
- SAP Fiori for treasury data integration
- FRED, BoE, and ECB for market rate data

---

## 📞 Support

For issues, questions, or suggestions:
1. Check the [documentation](README_SAP_INTEGRATION.md)
2. Review [troubleshooting guide](SAP_QUICKSTART.md)
3. Open an issue on GitHub

---

**Made with ❤️ for smarter treasury management**

Last Updated: 2026-09-16
