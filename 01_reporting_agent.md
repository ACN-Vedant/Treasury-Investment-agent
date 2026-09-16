# Step 1 — Reporting Agent

**Phase:** Identify Excess Cash  
**Runs:** Automatically (no human decision needed)  
**Time:** ~2–3 minutes (streams output as it runs)  
**Input:** Sheet 1 (Cash Balances) + Sheet 2 (Bank Statements) + Sheet 3 (Loan Schedule) + Sheet 4 (Investment Positions)  
**Output:** JSON report of **recommended investable amount** per account (net surplus after trend-based haircut)

---

## What this agent does

The Reporting Agent performs a five-part analysis to calculate the amount it is prudent to invest per account:

1. **Gross surplus** — Available Balance minus Minimum Operating Balance per account
2. **Maturing investment proceeds** — For each existing investment maturing within 180 days, adds back the full **notional (principal)** being returned plus the interest due on maturity
3. **Loan obligation deduction** — Sums all principal repayments and interest payables from the Loan Schedule due within 180 days
4. **Net investable surplus** — Gross surplus + Maturing proceeds (principal + interest) − Loan obligations
5. **Trend-based haircut** — Analyses 30-day inflow vs outflow from the Bank Statements sheet, classifies the trend, and applies a prudential margin:

| Trend | Haircut | Rationale |
|-------|---------|-----------|
| Increasing | 2% | Cash is building — safe to invest more |
| Stable | 5% | Normal buffer |
| Decreasing | 15% | Cash is flowing out — hold more back |

The **recommended investable amount** = net investable surplus − haircut amount. This is the figure passed to the Opportunity Agent.

It also derives the `earliest_loan_due_date` per account, which constrains the maximum investment tenor in Step 4.

**Formula:**
```
net_investable_surplus       = gross_surplus + maturing_principal + interest_receivable − loan_obligations
haircut_amount               = net_investable_surplus × haircut_pct / 100
recommended_investable_amount = net_investable_surplus − haircut_amount
```

> **Why maturing principal matters:** When an existing investment matures, the bank returns both the original notional and the accrued interest. The principal is the larger component and significantly increases the cash available to re-invest. Adding only interest receivable (the old approach) materially understated the true investable surplus.
>
> **Double-counting safeguard:** The agent only adds the maturing principal if the Maturity_Date is still in the future (after today). Once a position has settled, the returned cash is already reflected in the Available_Balance, so it is not added again.

---

## Prerequisites

- [ ] Your `treasury_data.xlsx` open with **Cash Balances**, **Bank Statements**, **Loan Schedule**, and **Investment Positions** sheets ready to copy

---

## Step-by-step instructions

### 1. Open a new chat in Claude.ai

Go to [claude.ai](https://claude.ai) and click **New chat**.

---

### 2. Copy this system prompt

Paste this as your first message:

---

```
You are a treasury reporting agent. You will receive cash balance data, bank statement data,
a loan schedule, and existing investment positions.

Your tasks:

1. For each account: gross_surplus = Available_Balance - Min_Operating_Balance

2. MATURING INVESTMENTS — PRINCIPAL + INTEREST RECEIVABLE:
   From the Investment Positions sheet, identify all positions where Maturity_Date
   falls within 180 days from today's analysis date.
   For each such position, calculate:
     a) maturing_principal = Notional_Amount  (the full face value returned on maturity)
     b) interest_receivable = Notional_Amount × (Yield_Percent / 100) × (Tenor_Days / 365)
     c) total_maturing_proceeds = maturing_principal + interest_receivable
   Sum per account/currency. If positions cannot be matched to a specific account,
   allocate by currency to the primary account in that currency.
   total_maturing_principal = sum of all Notional_Amounts for positions maturing within 180 days
   total_interest_receivable = sum of interest receivable from all maturing positions
   total_maturing_proceeds = total_maturing_principal + total_interest_receivable

   IMPORTANT: Add maturing_principal ONLY if Maturity_Date is after today (position not yet
   settled). If already settled, the cash is already in Available_Balance — do not double-count.

3. LOAN OBLIGATIONS:
   From the loan schedule, identify all obligations (principal + interest payables)
   per account where the due date falls within 180 days from today's analysis date.
   total_loan_obligations = sum of (Principal_Due_Amount + Interest_Due_Amount)
   for all loans linked to that account due within the horizon.

4. net_investable_surplus = gross_surplus + total_maturing_proceeds - total_loan_obligations
   (if negative, set to 0 and mark investable=false)

5. Determine earliest_loan_due_date per account — the soonest loan obligation date
   within the horizon. max_investment_tenor_days = days from analysis date to
   earliest_loan_due_date (use 180 if no loan due within horizon).

6. Flag accounts where net_investable_surplus > 0 as investable=true.

7. Analyse 30-day inflow vs outflow trend per account from bank statement data.
   Classify each account as: increasing, stable, or decreasing.

8. TREND-BASED HAIRCUT — apply a prudential margin to net_investable_surplus:
   - increasing:  haircut_pct = 2%   (cash is building — safe to invest more)
   - stable:      haircut_pct = 5%   (normal buffer)
   - decreasing:  haircut_pct = 15%  (cash is flowing out — hold more back)
   haircut_amount = round(net_investable_surplus × haircut_pct / 100)
   recommended_investable_amount = net_investable_surplus - haircut_amount
   If net_investable_surplus is 0 (investable=false), set both to 0.

OUTPUT FORMAT — follow this order exactly, with all three sections:

SECTION 1 — ONE-LINERS (lead with this). One short line per currency, nothing else. Pattern:
  "<CCY>: net investable <net_amount> across <n> account(s) — recommended <recommended_amount> after <haircut_pct>% <trend> haircut"
  Example: "USD: net investable 22,980,000 across 4 accounts — recommended 21,831,000 after 5% stable haircut"
Use a simple bulleted list, one bullet per currency.

SECTION 2 — SUMMARY (after the one-liners, under a "Summary" heading). Brief prose: per-account
breakdown showing gross surplus, maturing investment principal, interest receivable, loan obligations
deducted, net investable surplus, trend observed, haircut applied, and recommended investable amount.
Note accounts marked non-investable.

SECTION 3 — JSON (last). Return the JSON object below in this exact schema:

{
  "analysis_date": "YYYY-MM-DD",
  "investment_horizon_days": 180,
  "accounts": [
    {
      "account_id": "...",
      "account_name": "...",
      "currency": "...",
      "available_balance": 0,
      "min_operating_balance": 0,
      "gross_surplus": 0,
      "maturing_principal_within_horizon": 0,
      "interest_receivable_within_horizon": 0,
      "total_maturing_proceeds_within_horizon": 0,
      "maturing_position_detail": [
        {
          "position_id": "...",
          "counterparty": "...",
          "maturity_date": "YYYY-MM-DD",
          "notional": 0,
          "yield_pct": 0,
          "tenor_days": 0,
          "maturing_principal": 0,
          "interest_receivable": 0,
          "total_proceeds": 0
        }
      ],
      "total_loan_obligations_within_horizon": 0,
      "loan_obligation_detail": [
        {
          "loan_id": "...",
          "due_date": "YYYY-MM-DD",
          "principal_due": 0,
          "interest_due": 0,
          "total_due": 0
        }
      ],
      "net_investable_surplus": 0,
      "earliest_loan_due_date": "YYYY-MM-DD or null",
      "max_investment_tenor_days": 0,
      "investable": true,
      "30d_net_flow": 0,
      "trend": "increasing|stable|decreasing",
      "haircut_pct": 5,
      "haircut_amount": 0,
      "recommended_investable_amount": 0
    }
  ],
  "total_gross_surplus": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_maturing_principal": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_interest_receivable": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_maturing_proceeds": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_loan_obligations": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_net_investable_surplus": { "USD": 0, "GBP": 0, "EUR": 0 },
  "total_recommended_investable": { "USD": 0, "GBP": 0, "EUR": 0 }
}

Return the JSON exactly per the schema. The one-liners and summary come before it;
the JSON must be the last thing in your response.
```

---

### 3. Copy your data from Excel

Copy four sheets: **Cash Balances**, **Bank Statements**, **Loan Schedule**, and **Investment Positions**.

For each: click the sheet tab, click **A1**, press `Ctrl+Shift+End`, then `Ctrl+C`.

---

### 4. Send the data to Claude

Send a new message in this format:

```
CASH BALANCES:
[paste Cash Balances data]

BANK STATEMENTS:
[paste Bank Statements data]

LOAN SCHEDULE:
[paste Loan Schedule data]

INVESTMENT POSITIONS (for maturing principal + interest receivable):
[paste Investment Positions data]
```

---

### 5. Review Claude's output

Key fields to check:

```json
{
  "analysis_date": "2026-06-01",
  "accounts": [
    {
      "account_id": "ACC-001",
      "account_name": "Main Operating Account",
      "currency": "USD",
      "gross_surplus": 6700000,
      "maturing_principal_within_horizon": 10000000,
      "interest_receivable_within_horizon": 127500,
      "total_maturing_proceeds_within_horizon": 10127500,
      "total_loan_obligations_within_horizon": 2085000,
      "net_investable_surplus": 14742500,
      "earliest_loan_due_date": "2026-07-15",
      "max_investment_tenor_days": 44,
      "investable": true,
      "trend": "stable",
      "haircut_pct": 5,
      "haircut_amount": 737125,
      "recommended_investable_amount": 14005375
    }
  ],
  "total_gross_surplus": { "USD": 14100000, "GBP": 3050000, "EUR": 1980000 },
  "total_net_investable_surplus": { "USD": 22980000, "GBP": 4551250, "EUR": 2006400 },
  "total_recommended_investable": { "USD": 21831000, "GBP": 4323688, "EUR": 1906080 }
}
```

> **What to look for:** `recommended_investable_amount` is the figure the Opportunity Agent will use — it is lower than `net_investable_surplus` by the haircut margin. Check that the trend classification looks correct for each account; if you disagree with the trend, you can override the recommended amount when you pass data to Step 4.

---

### 6. Save the output

```
=== STEP 1 OUTPUT — REPORTING AGENT ===
[paste JSON here]
```

---

## Loan Schedule — what to include

Only include loans where **your company is the borrower**. Include:
- Term loans with scheduled amortisation
- Revolving credit facilities with drawn amounts
- Working capital lines with upcoming repayments
- Overdraft facilities being cleared

Do **not** include:
- Undrawn credit lines (no cash obligation)
- Loan obligations more than 180 days away
- Internal inter-company loans unless they represent real cash movements

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `net_investable_surplus` is negative | Loan obligations exceed gross surplus + maturing proceeds. Account is correctly marked `investable: false`. |
| `maturing_principal_within_horizon` is 0 | No existing positions mature within 180 days — this is correct if all positions run longer. |
| `total_maturing_proceeds_within_horizon` seems too high | Verify the agent is not adding principal for positions that have already settled (Maturity_Date in the past). Those should be excluded. |
| `max_investment_tenor_days` is very short | A loan repayment is imminent. Only a short-tenor or overnight placement may be feasible. |
| Trend classification looks wrong | Review the Bank Statements sheet. Reply: "Please re-assess the trend for ACC-XXX — the large outflow on [date] was a one-off payment, not a structural decline." |
| Haircut seems too conservative | You may override the recommended amount in Step 4. State your preferred investable amount in your message to the Opportunity Agent. |
| Loan obligations not appearing | Check that `Account_ID` in the Loan Schedule exactly matches `Account_ID` in Cash Balances. |
| Multiple loans on one account | The agent should sum all. If only one shows, reply: "Please aggregate all loan obligations per account_id." |

---

## What to do next

**→ [Step 2 — Ratings Sub-Agent](02_ratings_agent.md)** and **→ [Step 3 — Compliance Sub-Agent](03_compliance_agent.md)** — these can run in parallel.

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.1 (Reporting Agent — v5 with Trend-Based Haircut)*
