# Treasury Investment AI Agent System — No-Code Guide

> **What this is:** A complete, step-by-step guide to running all six Claude AI agents directly inside [claude.ai](https://claude.ai) — no Python, no VS Code, no programming required. You copy prompts, paste data, and follow the flow manually.

---

## How the no-code approach works

Each AI agent is a separate conversation in Claude.ai. You run them one at a time, copy the output of each agent, and paste it as input to the next. The Treasury Manager's approval decision happens between Step 4 and Step 5.

**Key features of this version:**

- **Loan Schedule integration** — upcoming principal repayments and interest payables are deducted from gross surplus before recommending investable amounts. The Opportunity Agent caps investment tenors at the earliest loan due date per account.
- **Maturing investment proceeds** — the Reporting Agent adds both the returning **principal** and interest receivable from existing investments maturing within 180 days to the gross surplus, giving a complete picture of available cash.
- **Trend-based haircut** — the Reporting Agent analyses the 30-day cash flow trend per account and applies a prudential margin before passing the investable amount to the Opportunity Agent: 2% for increasing trends, 5% for stable, and 15% for decreasing. Only the post-haircut amount is recommended for investment.
- **Policy-only compliance** — the Compliance Sub-Agent defines the envelope of what is *permitted* for new deals (approved counterparties, products, rating floor, max tenor, min yield). It does not re-check existing positions.

```
[Your Excel data — 5 sheets]
       ↓
Step 1 — Reporting Agent          (Cash Balances + Bank Statements + Loan Schedule
                                   + Investment Positions)
                                   → gross surplus per account
                                   → + maturing investment principal (notional returned)
                                   → + interest receivable from maturing investments
                                   → − loan obligations due within 180 days
                                   → = net investable surplus per account
                                   → derives max tenor per account from earliest loan date
                                   → applies trend-based haircut (2% / 5% / 15%)
                                   → = recommended investable amount per account
       ↓ copy JSON output
Step 2 — Ratings Sub-Agent        (Investment Positions + Policy)
                                   → converts text ratings to numeric scores
       ↓ copy JSON output
Step 3 — Compliance Sub-Agent     (Market Rates & Policy only)
                                   → extracts policy rules for new deals
                                   → approved counterparties, products, rating floor,
                                     max tenor, min yield, per-counterparty limits
       ↓ copy JSON output
Step 4 — Opportunity Agent        (all three outputs + Policy + Loan Schedule)
                                   → recommends investments within recommended investable amount
                                   → caps tenor at earliest loan due date per account
       ↓
  ★ HUMAN DECISION — Treasury Manager reviews and approves each deal individually ★
       ↓ (only if at least one deal approved)
Step 5 — Trader Agent             (approved recommendation + counterparty confirmation
                                   + Loan Schedule)
                                   → extracts deal terms from bank confirmation
                                   → checks deal maturity does not breach loan date
       ↓ copy JSON output
Step 6 — Deal Approval Agent      (Step 5 output + counterparty confirmation + Loan Schedule)
                                   → 7-check validation, including loan maturity check
       ↓
[Deal record JSON — save for TMS entry]
```

---

## Files in this guide

| File | Agent | Phase | Notes |
|------|-------|-------|-------|
| `01_reporting_agent.md` | Reporting Agent | Identify excess cash | Adds maturing principal + interest receivable; applies trend-based haircut |
| `02_ratings_agent.md` | Ratings Sub-Agent | Credit assessment | Now Step 2 |
| `03_compliance_agent.md` | Compliance Sub-Agent | Define policy rules for new deals | Now Step 3; policy-only — does not check existing positions |
| `04_opportunity_agent.md` | Opportunity Agent | Recommend investment | Uses recommended investable amount (post-haircut); loan-constrained tenor |
| `05_trader_agent.md` | Trader Agent | Create deal record | Loan maturity cross-check |
| `06_deal_approval_agent.md` | Deal Approval Agent | Validate & approve | 7th check: loan obligation constraint |

---

## Excel file structure

Your `treasury_data.xlsx` has **5 sheets**:

| Sheet | Name | Purpose |
|-------|------|---------|
| 1 | Cash Balances | Available balance, minimum operating balance, gross surplus per account |
| 2 | Bank Statements | Last 30 days of transactions for trend analysis and haircut determination |
| 3 | Loan Schedule | Principal repayment dates, interest payables, loan type and lender per account |
| 4 | Investment Positions | Existing investments — notional, yield, tenor, maturity date, counterparty, credit rating |
| 5 | Market Rates & Policy | Current rates, approved counterparties/products, min yield, max tenor, min credit rating, per-counterparty limits |

---

## Understanding recommended investable amount

| Term | Definition |
|------|------------|
| Gross surplus | Available Balance − Minimum Operating Balance |
| Maturing principal | Sum of notional amounts from existing investments maturing within 180 days (not yet settled) |
| Interest receivable | Sum of interest due on existing investments maturing within 180 days |
| Maturing proceeds | Maturing principal + Interest receivable |
| Loan obligations | Sum of principal + interest due within 180 days for loans on this account |
| Net investable surplus | Gross surplus + Maturing proceeds − Loan obligations |
| Cash flow trend | 30-day inflow vs outflow pattern: increasing / stable / decreasing |
| Haircut | Prudential margin withheld based on trend: 2% (increasing), 5% (stable), 15% (decreasing) |
| **Recommended investable amount** | **Net investable surplus − Haircut amount** |
| Max investment tenor | Days until the earliest loan due date on this account (180 days if no loan due) |

**Example:**
Account ACC-001 has a gross surplus of USD 6,700,000. It has an existing Fixed Deposit with Barclays (notional USD 10,000,000) maturing in 30 days — total maturing proceeds of USD 10,127,500. It also has a term loan repayment of USD 2,085,000 due 15 July 2026 (44 days away). Net investable surplus = USD 14,742,500. The account shows a stable trend, so a 5% haircut of USD 737,125 is applied. **Recommended investable amount = USD 14,005,375.** Maximum tenor = 44 days.

---

## Before you start

- [ ] Open [claude.ai](https://claude.ai) and sign in
- [ ] Have your `treasury_data.xlsx` open — confirm it has all 5 sheets including the Loan Schedule
- [ ] Have a plain text editor open to store intermediate JSON outputs
- [ ] Allocate **25–35 minutes** for a full run on your first attempt; subsequent runs 12–18 minutes

---

## General tips

**Copying sheet data:** In Excel, click A1, press `Ctrl+Shift+End`, then `Ctrl+C`. Paste directly into Claude.

**Saving outputs:** After each agent produces JSON, copy the full block and paste it into your text editor before moving on.

**Starting fresh:** Begin each agent in a **new Claude.ai conversation**. This keeps context clean.

**If Claude adds extra text:** Copy everything from the first `{` to the last `}`.

**If a loan is being refinanced:** Add a note to the Step 4 message: "LN-XXX is being refinanced — please disregard this constraint and use Max_Tenor_Days for account ACC-XXX instead."

**If you disagree with the haircut:** The haircut percentages (2% / 5% / 15%) are defaults. You may override the recommended investable amount at Step 4 by stating your preferred amount in your message to the agent.

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 6 (No-Code Option — v4)*
