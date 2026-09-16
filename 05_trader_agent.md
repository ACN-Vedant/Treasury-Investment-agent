# Step 5 — Trader Agent

**Phase:** Deal Creation  
**Runs:** After your approval in Step 4  
**Time:** ~2 minutes  
**Input:** Approved recommendation (loan-constrained) + counterparty confirmation text + Loan Schedule  
**Output:** Structured TMS deal record JSON — including a loan maturity cross-check

---

## What this agent does

The Trader Agent extracts deal terms from the counterparty confirmation and structures them into a TMS deal record. It now performs an additional **loan maturity cross-check**: it verifies that the deal's maturity date does not exceed the `constraining_loan_due_date` from the Step 4 recommendation. If the bank has confirmed a maturity date that runs past a loan obligation, this is flagged as a discrepancy before the deal is approved.

---

## Prerequisites

- [ ] Step 4 output — Opportunity Agent JSON (with loan-constrained recommendation)
- [ ] Contacted the counterparty bank and obtained their deal confirmation
- [ ] The Loan Schedule data ready to paste (or saved from Step 1)

---

## Step-by-step instructions

### 1. Contact the counterparty bank

Call or email the bank with the loan-constrained terms from Step 4. Be explicit about the maturity date:

> *"We would like to place a Fixed Deposit of USD 4,615,000 for 40 days starting 2 June 2026 to mature on or before 12 July 2026. Please confirm at your best rate and send a deal confirmation."*

> **Note:** Specifying a maturity date tied to your loan repayment is normal in treasury. Banks are accustomed to date-specific maturity requests.

---

### 2. Copy this system prompt

```
You are a treasury trader agent responsible for creating deal records.

You will receive:
1. An approved investment recommendation including loan-constraint fields
   (net_investable_amount, constraining_loan_due_date, maturity_date)
2. The Loan Schedule
3. Counterparty confirmation text

Tasks:
1. Extract all key deal terms from the confirmation:
   - Notional amount, currency, counterparty, product
   - Start date (value date), maturity date, yield/interest rate
   - Counterparty reference number

2. Cross-check each extracted term against the approved recommendation:
   - Amount within 0.01% tolerance of net_investable_amount
   - Yield within 0.005% tolerance
   - Dates must match exactly
   - Currency and counterparty must match exactly
   - Flag any mismatch with "DISCREPANCY: [description]"

3. LOAN MATURITY CROSS-CHECK:
   - Identify the constraining_loan_due_date from the recommendation
   - If the deal maturity date is after the constraining_loan_due_date, flag as:
     "DISCREPANCY: Deal maturity [date] exceeds loan obligation date [date] for [Loan_ID].
      Funds will not be available for debt service. Must renegotiate with bank."
   - Calculate days_buffer = constraining_loan_due_date - deal maturity date (positive = safe)

Return ONLY valid JSON:

{
  "deal_ref": "TMS-2026-NNNN",
  "product_type": "...",
  "counterparty": "...",
  "notional": 0,
  "currency": "...",
  "start_date": "YYYY-MM-DD",
  "maturity_date": "YYYY-MM-DD",
  "yield_pct": 0,
  "tenor_days": 0,
  "counterparty_ref": "...",
  "loan_maturity_check": {
    "constraining_loan_id": "LN-XXX or null",
    "constraining_loan_due_date": "YYYY-MM-DD or null",
    "deal_matures_before_loan_due": true,
    "days_buffer": 0,
    "note": "..."
  },
  "discrepancies": [],
  "status": "PENDING_APPROVAL",
  "extracted_from": "counterparty confirmation"
}

Return no other text.
```

---

### 3. Send the data to Claude

```
APPROVED RECOMMENDATION (from Step 4):
[paste Step 4 JSON]

LOAN SCHEDULE:
[paste Loan Schedule data]

COUNTERPARTY CONFIRMATION:
[paste confirmation text]
```

---

### 4. Review the output

A clean record looks like:

```json
{
  "deal_ref": "TMS-2026-0038",
  "product_type": "Fixed Deposit",
  "counterparty": "Barclays",
  "notional": 4615000,
  "currency": "USD",
  "start_date": "2026-06-02",
  "maturity_date": "2026-07-12",
  "yield_pct": 5.20,
  "tenor_days": 40,
  "counterparty_ref": "BRC-2026-48821",
  "loan_maturity_check": {
    "constraining_loan_id": "LN-001",
    "constraining_loan_due_date": "2026-07-15",
    "deal_matures_before_loan_due": true,
    "days_buffer": 3,
    "note": "Deal matures 12 Jul, LN-001 due 15 Jul — 3 days buffer available."
  },
  "discrepancies": [],
  "status": "PENDING_APPROVAL"
}
```

> **What to look for:** `deal_matures_before_loan_due` must be `true`. A `days_buffer` of 0 is technically acceptable but leaves no room for settlement delays — a buffer of 2–5 business days is preferable in practice.

---

## Discrepancy types — updated

| Discrepancy | What it means | Action |
|-------------|---------------|--------|
| Amount > net_investable_amount | Bank quoted a higher notional than approved | Instruct bank to reduce to the approved net investable amount |
| Maturity date after loan due date | Bank's proposed maturity runs past your repayment obligation | Renegotiate — request a shorter maturity, or ask the bank to split the placement |
| Maturity date too early | Bank proposed an earlier maturity — less ideal but acceptable | Confirm you accept; you may re-invest the proceeds |
| Yield differs | Rate changed during negotiation | Verify — if acceptable, note the change before Step 6 |

---

## Save the output

```
=== STEP 5 OUTPUT — TRADER AGENT ===
[paste JSON here]

=== COUNTERPARTY CONFIRMATION TEXT (keep for Step 6) ===
[paste confirmation text here]
```

---

**→ [Step 6 — Deal Approval Agent](06_deal_approval_agent.md)**

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.5 (Trader Agent — v2 with Loan Maturity Check)*
