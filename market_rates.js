// Auto-generated daily by fetch_market_rates.py — do not edit by hand.
window.LIVE_MARKET_RATES = {
  "rate_date": "2026-09-11",
  "overnight_rate_pct": 3.62,
  "month_1_rate_pct": 3.65,
  "month_3_rate_pct": 3.65,
  "month_6_rate_pct": 3.66,
  "gbp_overnight_pct": 3.73,
  "eur_overnight_pct": 2.19,
  "fetched_at": "2026-09-15 08:46 UTC",
  "sources": {
    "overnight_and_term_proxy": "FRED (SOFR, SOFR30/90/180DAYAVG) \u2014 https://fred.stlouisfed.org",
    "gbp_overnight": "Bank of England SONIA (IUDSOIA), 11/09/2026",
    "eur_overnight": "ECB Data Portal EST/B.EU000A2X2A25.WT, 14/09/2026"
  },
  "note": "1M/3M/6M are FRED SOFR 30/90/180-day averages, used as a free proxy for the licensed CME Term SOFR / ICE Term SONIA benchmarks (which require a paid distribution license for automated use).",
  "audit_screenshots": [
    "rate_audit\\2026-09-15\\boe_sonia.png",
    "rate_audit\\2026-09-15\\ecb_estr.png"
  ]
};
