"""
Daily market-rate fetcher for the Treasury Investment AI app.

Pulls the overnight/1M/3M/6M reference rates it needs from official, free,
ToS-compliant sources (no scraping of paid terminals, no Yahoo Finance):

  - SOFR overnight + 30/90/180-day averages  -> FRED (fred.stlouisfed.org)
  - SONIA overnight (GBP)                    -> Bank of England statistical database
  - EUR short-term rate / EUR overnight       -> ECB Data Portal SDMX API

The 30/90/180-day SOFR averages are used as a free stand-in for the 1M/3M/6M
term rate cells. The *actual* forward-looking CME Term SOFR / ICE Term SONIA
benchmarks are commercial products that require a paid distribution license
for any automated/non-display use, so they are deliberately not fetched here.

Writes:
  - market_rates.js       <- window.LIVE_MARKET_RATES, loaded directly by treasury_agent.html
  - rate_audit/<date>/*.png <- screenshots of each official source page, for audit evidence

Run daily (see register_daily_task.ps1 for Windows Task Scheduler setup).
"""

import csv
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

SESSION = requests.Session()
# The Bank of England database returns 403 to the default python-requests
# user agent (basic bot filtering) but allows normal browser-like agents.
SESSION.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) treasury-rates-fetcher/1.0"})

PROJECT_DIR = Path(__file__).resolve().parent
AUDIT_DIR = PROJECT_DIR / "rate_audit"

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
BOE_CSV = (
    "https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp"
    "?csv.x=yes&Datefrom={date_from}&Dateto=now&SeriesCodes={codes}"
    "&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N"
)
ECB_CSV = "https://data-api.ecb.europa.eu/service/data/EST/B.EU000A2X2A25.WT?format=csvdata&lastNObservations=1"

SOURCE_PAGES = {
    "fred_sofr": "https://fred.stlouisfed.org/series/SOFR",
    "boe_sonia": "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp",
    "ecb_estr": "https://data.ecb.europa.eu/data/data-categories/financial-markets-and-interest-rates/euro-money-market/euro-short-term-rate",
}


def latest_fred_value(series: str) -> tuple[str, float]:
    """Return (date, value) for the most recent non-missing observation of a FRED series."""
    resp = SESSION.get(FRED_CSV.format(series=series), timeout=30)
    resp.raise_for_status()
    reader = csv.reader(io.StringIO(resp.text))
    rows = [r for r in reader if len(r) == 2 and r[1].strip() not in ("", ".")]
    if len(rows) < 2:
        raise RuntimeError(f"No usable data returned for FRED series {series}")
    date_str, value_str = rows[-1]
    return date_str, float(value_str)


def latest_fred_multi(series_list: list[str]) -> tuple[str, dict[str, float]]:
    """Return (date, {series: value}) for the most recent row where all series have data."""
    resp = SESSION.get(FRED_CSV.format(series=",".join(series_list)), timeout=30)
    resp.raise_for_status()
    reader = csv.reader(io.StringIO(resp.text))
    rows = list(reader)
    header = rows[0]
    for row in reversed(rows[1:]):
        if len(row) != len(header):
            continue
        values = row[1:]
        if all(v.strip() not in ("", ".") for v in values):
            return row[0], {header[i]: float(row[i]) for i in range(1, len(header))}
    raise RuntimeError(f"No row with complete data for {series_list}")


def latest_boe_sonia() -> tuple[str, float]:
    date_from = "01/" + datetime.now().strftime("%b/%Y")
    url = BOE_CSV.format(date_from=date_from, codes="IUDSOIA")
    resp = SESSION.get(url, timeout=30)
    resp.raise_for_status()
    reader = csv.reader(io.StringIO(resp.text))
    rows = [r for r in reader if len(r) == 2 and r[1].strip() != ""]
    if len(rows) < 2:
        raise RuntimeError("No usable SONIA data returned from Bank of England database")
    date_str, value_str = rows[-1]
    # BoE dates look like "11 Sep 2026" -> normalise to DD/MM/YYYY
    dt = datetime.strptime(date_str.strip(), "%d %b %Y")
    return dt.strftime("%d/%m/%Y"), float(value_str)


def latest_estr() -> tuple[str, float]:
    resp = SESSION.get(ECB_CSV, timeout=30)
    resp.raise_for_status()
    reader = csv.DictReader(io.StringIO(resp.text))
    rows = list(reader)
    if not rows:
        raise RuntimeError("No €STR observation returned by ECB Data Portal")
    row = rows[-1]
    dt = datetime.strptime(row["TIME_PERIOD"], "%Y-%m-%d")
    return dt.strftime("%d/%m/%Y"), float(row["OBS_VALUE"])


def capture_audit_screenshots(dest_dir: Path) -> list[str]:
    """Screenshot each official source page as audit evidence. Best-effort — a screenshot
    failure must never block the numeric rate update, since the numbers are already fetched
    directly from the APIs above, not read off these pages."""
    saved = []
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed — skipping audit screenshots (pip install playwright && playwright install chromium)", file=sys.stderr)
        return saved

    dest_dir.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--disable-http2"])
            for name, url in SOURCE_PAGES.items():
                out_path = dest_dir / f"{name}.png"
                # Fresh context+page per URL so one navigation failure can't leave
                # stale in-flight state that corrupts the next screenshot.
                context = browser.new_context(
                    viewport={"width": 1440, "height": 900},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                )
                page = context.new_page()
                try:
                    page.goto(url, timeout=45000, wait_until="load")
                    page.wait_for_timeout(1500)
                    page.screenshot(path=str(out_path), full_page=False)
                    saved.append(str(out_path.relative_to(PROJECT_DIR)))
                except Exception as e:
                    print(f"Screenshot failed for {name} ({url}): {e}", file=sys.stderr)
                finally:
                    context.close()
            browser.close()
    except Exception as e:
        print(f"Playwright audit screenshots skipped: {e}", file=sys.stderr)
    return saved


def main() -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    errors = []

    try:
        sofr_date, sofr = latest_fred_value("SOFR")
    except Exception as e:
        errors.append(f"SOFR (FRED): {e}")
        sofr_date, sofr = None, None

    try:
        _, term_avgs = latest_fred_multi(["SOFR30DAYAVG", "SOFR90DAYAVG", "SOFR180DAYAVG"])
    except Exception as e:
        errors.append(f"SOFR term averages (FRED): {e}")
        term_avgs = {}

    try:
        sonia_date, sonia = latest_boe_sonia()
    except Exception as e:
        errors.append(f"SONIA (Bank of England): {e}")
        sonia_date, sonia = None, None

    try:
        estr_date, estr = latest_estr()
    except Exception as e:
        errors.append(f"€STR (ECB): {e}")
        estr_date, estr = None, None

    if errors:
        print("Some rates failed to fetch:\n  " + "\n  ".join(errors), file=sys.stderr)

    if sofr is None or sonia is None or estr is None or not term_avgs:
        print("Aborting: one or more required rates could not be fetched. market_rates.js left unchanged.", file=sys.stderr)
        return 1

    live_rates = {
        "rate_date": sofr_date,
        "overnight_rate_pct": round(sofr, 2),
        "month_1_rate_pct": round(term_avgs["SOFR30DAYAVG"], 2),
        "month_3_rate_pct": round(term_avgs["SOFR90DAYAVG"], 2),
        "month_6_rate_pct": round(term_avgs["SOFR180DAYAVG"], 2),
        "gbp_overnight_pct": round(sonia, 2),
        "eur_overnight_pct": round(estr, 2),
        "fetched_at": fetched_at,
        "sources": {
            "overnight_and_term_proxy": "FRED (SOFR, SOFR30/90/180DAYAVG) — https://fred.stlouisfed.org",
            "gbp_overnight": f"Bank of England SONIA (IUDSOIA), {sonia_date}",
            "eur_overnight": f"ECB Data Portal EST/B.EU000A2X2A25.WT, {estr_date}",
        },
        "note": "1M/3M/6M are FRED SOFR 30/90/180-day averages, used as a free proxy for the "
                "licensed CME Term SOFR / ICE Term SONIA benchmarks (which require a paid "
                "distribution license for automated use).",
    }

    audit_dir = AUDIT_DIR / today
    screenshots = capture_audit_screenshots(audit_dir)
    live_rates["audit_screenshots"] = screenshots

    js_path = PROJECT_DIR / "market_rates.js"
    js_path.write_text(
        "// Auto-generated daily by fetch_market_rates.py — do not edit by hand.\n"
        f"window.LIVE_MARKET_RATES = {json.dumps(live_rates, indent=2)};\n",
        encoding="utf-8",
    )

    print(f"market_rates.js updated: {live_rates}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
