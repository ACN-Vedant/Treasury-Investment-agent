# Step 4 — Opportunity Identification Agent

**Phase:** Identify Opportunities for Investment  
**Runs:** Automatically, then pauses for your decision on each deal  
**Time:** ~3 minutes  
**Input:** Step 1 output + Step 2 output + Step 3 output + Sheet 5 (Market Rates & Policy) + Sheet 3 (Loan Schedule)  
**Output:** Investment recommendation — crisp one-liner per currency first, then detail, then JSON — for your review and per-deal approval

---

## What this agent does

The Opportunity Identification Agent recommends investments using the **recommended investable amount** from Step 1 — which is the net investable surplus (gross surplus + maturing proceeds − loan obligations) further reduced by a trend-based haircut (2% increasing / 5% stable / 15% decreasing). It applies two constraints:

**Constraint 1 — Amount cap:** The investment notional must not exceed the account's `recommended_investable_amount`. This preserves the haircut margin as a liquidity buffer.

**Constraint 2 — Tenor cap:** The investment must mature on or before the account's `earliest_loan_due_date`. This ensures cash is available when needed for debt service. If no loan is due within the 180-day horizon, the standard `Max_Tenor_Days` policy applies.

These constraints mean the agent may recommend shorter tenors and lower notionals than in earlier versions — and the rationale will explicitly state when a loan date or haircut is the binding constraint.

---

## Prerequisites

- [ ] Step 1 output — Reporting Agent JSON (with recommended investable amount and loan data)
- [ ] Step 2 output — Ratings Sub-Agent JSON
- [ ] Step 3 output — Compliance Sub-Agent JSON
- [ ] Your `treasury_data.xlsx` open with **Market Rates & Policy** and **Loan Schedule** sheets ready to copy

---

## Step-by-step instructions

### 1. Open a new chat in Claude.ai

Fresh conversation. Do not continue in any previous step's chat.

---

### 2. Copy this system prompt

---

```
You are a treasury investment opportunity identification agent.

You will receive:
- A surplus cash analysis including net investable surplus and recommended investable amount
  per account (net surplus after a trend-based haircut: 2% increasing / 5% stable / 15% decreasing),
  each account's earliest_loan_due_date and max_investment_tenor_days
- A credit ratings assessment
- A compliance check
- Current market rates and investment policy

CRITICAL RULES — these override all other tenor and amount considerations:

RULE 1 — AMOUNT CONSTRAINT:
The investment notional for each account must not exceed the account's recommended_investable_amount.
Do NOT use net_investable_surplus or gross_surplus — the haircut margin must be preserved as a
liquidity buffer.

RULE 2 — TENOR CONSTRAINT:
The investment maturity date must be on or before the account's earliest_loan_due_date.
If earliest_loan_due_date is null (no loan due within horizon), apply Max_Tenor_Days from policy.
The effective max tenor in days = min(max_investment_tenor_days, Max_Tenor_Days from policy).

OTHER RULES:
- Only consider counterparties that are compliant AND meet credit rating policy
- Select the highest-yielding product available within the effective max tenor
- Rank by risk-adjusted yield
- Calculate yield advantage vs overnight rate in basis points
- If recommended_investable_amount for an account is below Min_Placement_Amount, do not recommend
  for that account

OUTPUT FORMAT — follow this order exactly:

SECTION 1 — RECOMMENDATIONS (lead with this).
Output one crisp one-line recommendation per currency and nothing else in this section.
Each line must follow this pattern:
  "Invest <recommended_investable_amount> <CCY> in <Product> with <Counterparty> for <tenor> at <yield>%"
Example: "Invest 14,005,375 USD in Fixed Deposit with Barclays for ~1.5 months at 5.20%"
Express tenor in the most natural unit (months if >= ~30 days, otherwise weeks/days).
Use the exact recommended_investable_amount — do not round it.
Use a simple bulleted list, one bullet per currency.
Do NOT add ratings, loan IDs, haircut details, or any other detail in this section.

SECTION 2 — DETAILS (after the one-liners, under a "Details" heading).
Provide the Treasury Manager level breakdown:
- Gross surplus per currency
- Maturing investment proceeds added (split into principal returned and interest receivable)
- Loan obligations deducted
- Net investable surplus per currency
- Trend observed and haircut applied per account
- Recommended investable amount per account
- Which accounts have their tenor constrained by a loan date (and what that date is)
- Counterparty rating, expected yield, and yield advantage vs overnight rate in bps
- Any accounts excluded because their recommended surplus falls below minimum placement size

SECTION 3 — JSON (last). Return the JSON object below.

{
  "summary_date": "YYYY-MM-DD",
  "total_gross_surplus": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_maturing_principal_added": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_interest_receivable_added": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_loan_obligations_deducted": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_net_investable_surplus": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_recommended_investable": { "USD": 0, "GBP": 0, "EUR": 0 },
  "recommendations": [
    {
      "rank": 1,
      "account_id": "...",
      "currency": "USD",
      "gross_surplus": 0,
      "maturing_principal_added": 0,
      "interest_receivable_added": 0,
      "loan_obligations_deducted": 0,
      "net_investable_amount": 0,
      "trend": "stable",
      "haircut_pct": 5,
      "haircut_amount": 0,
      "recommended_investable_amount": 0,
      "product": "Fixed Deposit",
      "counterparty": "...",
      "counterparty_rating": "AA+",
      "tenor_days": 0,
      "tenor_constrained_by_loan": true,
      "constraining_loan_id": "LN-001",
      "constraining_loan_due_date": "YYYY-MM-DD",
      "maturity_date": "YYYY-MM-DD",
      "expected_yield_pct": 0,
      "overnight_rate_pct": 0,
      "yield_advantage_bps": 0,
      "rationale": "..."
    }
  ]
}
```

---

### 3. Send all inputs to Claude

```
SURPLUS ANALYSIS WITH HAIRCUT (from Step 1):
[paste Step 1 JSON]

RATINGS ASSESSMENT (from Step 2):
[paste Step 2 JSON]

COMPLIANCE CHECK (from Step 3):
[paste Step 3 JSON]

MARKET RATES & POLICY (from Excel Sheet 5):
[paste Market Rates & Policy data]

LOAN SCHEDULE (from Excel Sheet 3):
[paste Loan Schedule data]
```

---

### 4. Read the recommendation

The agent leads with a crisp one-liner per currency, then a **Details** section, then the JSON:

---

**Recommendations**

- Invest 14,005,375 USD in Fixed Deposit with Barclays for ~1.5 months at 5.20%
- Invest 4,107,338 GBP in Fixed Deposit with HSBC for ~1 month at 4.95%
- Invest 1,810,956 EUR in Money Market Fund with BlackRock MMF for ~3 months at 3.85%

**Details**

*"As of 1 June 2026, net investable surplus across accounts totalled USD 14,742,500, GBP 4,323,500, and EUR 1,906,800. After applying trend-based haircuts — USD stable (5%: −USD 737,125), GBP stable (5%: −GBP 216,175), EUR stable (5%: −EUR 95,340) — recommended investable amounts are USD 14,005,375, GBP 4,107,325, and EUR 1,811,460.*

*ACC-001's USD tenor is capped at 44 days (maturity 15 July 2026) to ensure funds are available for the LN-001 principal repayment due that date. The recommended 40-day Fixed Deposit with Barclays (AA+) yields 5.20%, 10bps above the overnight rate."*

---

### 5. ★ Make your investment decision ★

You will be asked to **approve or decline each deal individually**. Before deciding on each, check:

- Is the investment amount equal to the `recommended_investable_amount` (not the gross or net surplus)?
- Does the maturity date fall before the constraining loan due date?
- Are you comfortable with the haircut applied — does the trend classification reflect reality?
- Is there any possibility the loan repayment date changes (e.g. a refinancing in progress)?

> ⚠️ **Important:** If a refinancing or loan extension is pending, inform the agent before running Step 4: "LN-001 is expected to be refinanced — please ignore the 15 July constraint for ACC-001 and use Max_Tenor_Days instead."

> ⚠️ **Overriding the haircut:** If you believe the trend-based haircut is too conservative or too generous, you may state your preferred investable amount directly: "Please use USD 15,000,000 for ACC-001 instead of the recommended amount."

---

### 6. Save the output

```
=== STEP 4 OUTPUT — OPPORTUNITY AGENT ===
[paste full response — both plain English and JSON]
```

---

## How haircut and loan constraints affect the recommended amount

| Factor | Effect |
|--------|--------|
| Decreasing trend | 15% haircut — meaningfully reduces investable amount |
| Stable trend | 5% haircut — standard buffer |
| Increasing trend | 2% haircut — minimal reduction |
| Loan due soon | Tenor capped at loan date — may reduce yield vs longer tenor |

If both a decreasing trend and an imminent loan apply to the same account, the recommended amount may be substantially lower than the gross surplus. This is intentional — it protects cash flow.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent recommends an amount higher than recommended_investable_amount | Reply: "Please use recommended_investable_amount as the investment notional, not net_investable_surplus or gross_surplus." |
| Tenor longer than earliest_loan_due_date | Reply: "Please ensure the maturity_date is on or before the constraining_loan_due_date for each account." |
| All EUR accounts excluded | EUR recommended amount may be below Min_Placement_Amount. Check the Step 1 output for EUR recommended figures. |
| Haircut seems wrong | Check the trend field in the Step 1 JSON. If the trend classification is incorrect, re-run Step 1 with a note explaining the anomaly in the bank statement data. |

---

## What to do next

If at least one deal is approved:

**→ [Step 5 — Trader Agent](05_trader_agent.md)**

Contact your counterparty bank with the recommended terms, then return to Step 5.

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.4 (Opportunity Identification Agent — v4 with Trend-Based Haircut)*
