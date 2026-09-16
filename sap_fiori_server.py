"""
Simple FastAPI server to fetch SAP Fiori cash flow data.
Run this server in the background, then the HTML app can call it.

Usage:
  python sap_fiori_server.py

Then access the app at http://localhost:8000 (or navigate to treasury_agent.html).
The server will listen on localhost:8000 for /api/fetch-sap-cashflow POST requests.
"""

import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the SAP fetcher functions
from fetch_sap_cashflow import fetch_sap_cashflow
from fetch_sap_treasury_data import fetch_sap_treasury_data

app = FastAPI(title="Treasury SAP Integration Server")

# Allow CORS for the HTML app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SAPFetchRequest(BaseModel):
    sap_url: str
    username: str
    password: str
    company_code: str
    currency: str
    as_of_date: str


@app.post("/api/fetch-sap-cashflow")
async def fetch_sap_endpoint(request: SAPFetchRequest) -> dict:
    """
    Fetch cash balances from SAP Fiori.
    """
    try:
        result = fetch_sap_cashflow(
            sap_url=request.sap_url,
            username=request.username,
            password=request.password,
            company_code=request.company_code,
            currency=request.currency,
            as_of_date=request.as_of_date,
        )

        if result["status"] != "success":
            raise HTTPException(status_code=400, detail=result.get("message", "SAP fetch failed"))

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/fetch-sap-treasury-data")
async def fetch_sap_treasury_endpoint(request: SAPFetchRequest) -> dict:
    """
    Fetch comprehensive treasury data from SAP Fiori TPM13:
    - Cash Balances
    - Loan Schedule
    - Investment Positions

    All in a single connection.
    """
    try:
        result = fetch_sap_treasury_data(
            sap_url=request.sap_url,
            username=request.username,
            password=request.password,
            company_code=request.company_code,
            currency=request.currency,
            as_of_date=request.as_of_date,
        )

        if result["status"] != "success":
            raise HTTPException(status_code=400, detail=result.get("message", "SAP fetch failed"))

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "Treasury SAP Integration Server"}


@app.get("/")
async def root():
    """Root endpoint — serve info about the server."""
    return {
        "service": "Treasury SAP Integration Server",
        "version": "1.0",
        "endpoints": {
            "health": "GET /health",
            "fetch_sap": "POST /api/fetch-sap-cashflow",
        },
        "note": "This server provides backend support for the Treasury Investment AI dashboard. Navigate to treasury_agent.html in a web browser to use the app.",
    }


if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*70)
    print("Treasury SAP Integration Server")
    print("="*70)
    print("\nStarting server on http://localhost:8000...")
    print("\nThe HTML app (treasury_agent.html) can now call:")
    print("  POST /api/fetch-sap-cashflow")
    print("\nMake sure Playwright is installed:")
    print("  pip install playwright && playwright install chromium")
    print("\n" + "="*70 + "\n")

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
