# Step 3 — Compliance Sub-Agent

**Phase:** Identify Opportunities for Investment  
**Runs:** Automatically (no human decision needed)  
**Time:** ~1 minute  
**Input:** Sheet 5 (Market Rates & Policy) only  
**Output:** JSON policy envelope — what is permitted for new deals

---

## What this agent does

The Compliance Sub-Agent reads the Market Rates & Policy sheet and extracts the rules that govern what new investments are permitted. It does **not** check existing investment positions — its sole purpose is to define the compliance envelope that the Opportunity Agent must work within when recommending new deals.

The agent extracts:
1. **Approved counterparties** — which banks and funds are eligible for new placements
2. **Approved products** — which instrument types are permitted
3. **Minimum credit rating** — the lowest rating an eligible counterparty may hold
4. **Maximum tenor** — the longest duration permitted for any new deal
5. **Minimum yield** — the lowest acceptable rate for any new placement
6. **Per-counterparty limits** — the maximum exposure ceiling per counterparty

This output is used by the Opportunity Agent (Step 4) to ensure it only recommends compliant new investments.

> **Note:** This agent runs in parallel with the Ratings Sub-Agent (Step 2). You can run Steps 2 and 3 simultaneously in two separate browser tabs if you want to save time.

> **Note:** Checking whether existing investments comply with current policy is a separate exercise and is out of scope for this pipeline. This agent exclusively defines what is permissible for *new* deals.

---

## Prerequisites

- [ ] Your `treasury_data.xlsx` open with the **Market Rates & Policy** sheet ready to copy

---

## Step-by-step instructions

### 1. Open a new chat in Claude.ai

Go to [claude.ai](https://claude.ai) and click **New chat**. Do not continue in the same chat as Steps 1 or 2 — start fresh.

---

### 2. Copy this system prompt

Copy the entire block below and paste it as your **first message**:

---

```
You are a treasury compliance policy agent. Your job is to read the Market Rates & Policy
sheet and extract the rules that govern what new investments are permitted.
You are NOT checking existing positions — you are defining the compliance envelope
for new deals.

Extract and output the following policy parameters:
1. Approved_Counterparties — list of counterparties eligible for new placements
2. Approved_Products — list of product types permitted
3. Min_Credit_Rating — minimum credit rating a counterparty must hold
4. Max_Tenor_Days — maximum tenor allowed for any new deal
5. Min_Acceptable_Yield — minimum yield any new deal must achieve
6. Max_Counterparty_Limit — per-counterparty exposure ceiling for new placements

Return ONLY valid JSON in this exact schema — no other text before or after:

{
  "policy_compliant": true,
  "approved_counterparties": ["..."],
  "approved_products": ["..."],
  "counterparty_limits": [
    { "counterparty": "...", "max_limit": 0 }
  ],
  "policy_rules": {
    "min_credit_rating": "...",
    "max_tenor_days": 0,
    "min_acceptable_yield_pct": 0
  }
}

Return no other text. Do not add any explanation before or after the JSON.
```

---

### 3. Copy your Market Rates & Policy data from Excel

1. Open `treasury_data.xlsx`
2. Click the **Market Rates & Policy** sheet tab
3. Select all data: click **A1**, press `Ctrl+Shift+End`, then `Ctrl+C`

---

### 4. Send the data to Claude

In the same chat, send a new message:

```
MARKET RATES & POLICY:
[paste your Market Rates & Policy sheet data here]
```

---

### 5. Review Claude's JSON output

Claude will return the policy envelope JSON. Example of what to expect:

```json
{
  "policy_compliant": true,
  "approved_counterparties": [
    "Barclays", "HSBC", "JPMorgan", "Citibank",
    "Deutsche Bank", "BNP Paribas", "NatWest", "Wells Fargo", "BlackRock MMF"
  ],
  "approved_products": [
    "Fixed Deposit", "T-Bill", "Money Market Fund", "Commercial Paper"
  ],
  "counterparty_limits": [
    { "counterparty": "Barclays", "max_limit": 20000000 },
    { "counterparty": "HSBC", "max_limit": 20000000 },
    { "counterparty": "JPMorgan", "max_limit": 25000000 }
  ],
  "policy_rules": {
    "min_credit_rating": "A-",
    "max_tenor_days": 180,
    "min_acceptable_yield_pct": 4.80
  }
}
```

> **What to look for:** Confirm the approved counterparty list and product list match your expectations. The Opportunity Agent will only recommend deals that are within this envelope.

---

### 6. Save the output

Copy the full JSON and save it in your text editor:

```
=== STEP 3 OUTPUT — COMPLIANCE SUB-AGENT ===
[paste JSON here]
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `approved_counterparties` list is shorter than expected | Check the Approved_Counterparties row in your policy sheet — names must be separated consistently (semicolons or commas) |
| `max_limit` values are 0 or missing | Confirm your policy sheet has a per-counterparty limit row/column. If limits are uniform, add a note: "All counterparty limits are X" |
| `min_acceptable_yield_pct` seems wrong | Check that the yield value in the policy sheet is formatted as a percentage (e.g. 4.80% not 0.048) |

---

## What to do next

Once you have saved the Step 3 JSON output, proceed to:

**→ [Step 4 — Opportunity Identification Agent](04_opportunity_agent.md)**

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.3 (Compliance Sub-Agent — now Step 3)*
