# Step 6 — Deal Approval Agent

**Phase:** Deal Approval  
**Runs:** Final step  
**Time:** ~2 minutes  
**Input:** Step 5 output + counterparty confirmation text + Loan Schedule  
**Output:** Final validated deal record JSON — APPROVED or REQUIRES_REVIEW

---

## What this agent does

The Deal Approval Agent now runs **7 validation checks** (up from 6). The new seventh check verifies that the deal's maturity date respects the loan obligation constraint from the Loan Schedule — ensuring funds are available for debt service before the deal is formally approved.

---

## Prerequisites

- [ ] Step 5 output — Trader Agent deal record JSON (includes `loan_maturity_check`)
- [ ] Counterparty confirmation text (same as Step 5)
- [ ] Loan Schedule data

---

## Step-by-step instructions

### 1. Open a new chat in Claude.ai

---

### 2. Copy this system prompt

```
You are a deal approval agent for treasury investments.

You will receive:
1. A TMS deal record JSON (including loan_maturity_check fields)
2. The original counterparty confirmation text
3. The Loan Schedule

Run the following 7 checks:

CHECK 1 — Notional amount: within 0.01% of net_investable_amount in the recommendation
CHECK 2 — Currency: exact match (case-insensitive)
CHECK 3 — Counterparty name: allow minor formatting differences (flag but do not fail alone)
CHECK 4 — Start date (value date): exact match
CHECK 5 — Maturity date: exact match between deal record and confirmation
CHECK 6 — Yield / interest rate: within 0.005% tolerance
CHECK 7 — Loan obligation constraint: deal maturity date must be on or before
           constraining_loan_due_date from the deal record's loan_maturity_check.
           If constraining_loan_due_date is null, mark PASS with note "No loan constraint applies."
           If deal_matures_before_loan_due is false in the deal record, this check FAILS.

Scoring:
- ALL 7 pass → status = "APPROVED"
- ANY fail (except minor name formatting) → status = "REQUIRES_REVIEW"

Return the complete updated TMS deal record with:
- status: "APPROVED" or "REQUIRES_REVIEW"
- audit_note: summary of validation outcome, explicitly mentioning the loan check result
- approval_timestamp: current ISO datetime
- validation_checks: array of {check, result, detail} for all 7 checks

Return ONLY valid JSON. No other text.
```

---

### 3. Send the data to Claude

```
TMS DEAL RECORD (from Step 5):
[paste Step 5 JSON]

COUNTERPARTY CONFIRMATION:
[paste confirmation text]

LOAN SCHEDULE:
[paste Loan Schedule data]
```

---

### 4. Review the output

Example of a fully approved deal with loan check:

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
  "status": "APPROVED",
  "audit_note": "All 7 validation checks passed. Amount USD 4,615,000 matches net investable surplus. Maturity 12 July 2026 is 3 days before LN-001 obligation due 15 July 2026 — loan constraint satisfied.",
  "approval_timestamp": "2026-06-02T14:35:00",
  "validation_checks": [
    { "check": "Notional amount", "result": "PASS", "detail": "4,615,000 — exact match" },
    { "check": "Currency", "result": "PASS", "detail": "Both USD" },
    { "check": "Counterparty name", "result": "PASS", "detail": "Barclays vs Barclays Bank PLC — minor formatting, acceptable" },
    { "check": "Start date", "result": "PASS", "detail": "Both 2026-06-02" },
    { "check": "Maturity date", "result": "PASS", "detail": "Both 2026-07-12" },
    { "check": "Yield / interest rate", "result": "PASS", "detail": "5.20% — exact match" },
    { "check": "Loan obligation constraint", "result": "PASS", "detail": "Deal matures 2026-07-12, LN-001 due 2026-07-15 — 3 days buffer. Constraint satisfied." }
  ]
}
```

---

### 5. Save the final record

Save the JSON as `deal_record_TMS-2026-0038.json`. Enter into TMS using:

| TMS Field | Source |
|-----------|--------|
| Deal Reference | `deal_ref` |
| Product Type | `product_type` |
| Counterparty | `counterparty` |
| Notional Amount | `notional` |
| Currency | `currency` |
| Value Date | `start_date` |
| Maturity Date | `maturity_date` |
| Yield / Rate | `yield_pct` |
| Tenor (days) | `tenor_days` |
| External Reference | `counterparty_ref` |

---

## REQUIRES_REVIEW — check 7 failure

If Check 7 fails, the deal record will show:

```json
{
  "check": "Loan obligation constraint",
  "result": "FAIL",
  "detail": "Deal matures 2026-09-01. LN-001 principal of USD 2,085,000 due 2026-07-15. Deal will not be liquid in time. Do not enter into TMS until resolved."
}
```

**Action:** Contact the bank to negotiate a shorter maturity. Do not enter into TMS until the deal maturity date is brought within the loan constraint.

---

## Audit trail

Retain together for each deal:

- [ ] Step 4 output — loan-constrained recommendation you approved
- [ ] Counterparty confirmation (email or PDF)
- [ ] Step 6 output — final approved deal record JSON with all 7 validation checks
- [ ] Your approval note: name, date, "approved as recommended"

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Check 7 fails but you believe the loan was refinanced | Do not approve. Update the Loan Schedule first to remove or extend the loan, then re-run from Step 1 to get updated constraints. |
| `constraining_loan_due_date` is null in the deal record | Either the recommendation had no loan constraint for this account, or it was not passed from Step 5. Reply: "Please check the loan_maturity_check field in the deal record and confirm the constraining_loan_due_date." |
| REQUIRES_REVIEW on check 3 only (name formatting) | This is safe to override. Reply: "Check 3 is a minor name format difference only. All other checks pass. Please set status to APPROVED and note the name variant in the audit_note." |

---

## Summary of all steps

| Step | Agent | Key input |
|------|-------|-----------|
| 1 | Reporting Agent | Cash Balances + Bank Statements + **Loan Schedule** |
| 2 | Compliance Sub-Agent | Investment Positions + Policy + Step 1 |
| 3 | Ratings Sub-Agent | Investment Positions + Policy |
| 4 | Opportunity Agent | Steps 1–3 + Policy + **Loan Schedule** |
| — | Human gate | Review loan-constrained recommendation |
| 5 | Trader Agent | Recommendation + Confirmation + **Loan Schedule** |
| 6 | Deal Approval Agent | Deal record + Confirmation + **Loan Schedule** |
| — | You | Enter deal into TMS |

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.6 (Deal Approval Agent — v2 with Loan Obligation Check)*
