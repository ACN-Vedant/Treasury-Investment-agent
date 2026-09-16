# Step 2 — Ratings Sub-Agent

**Phase:** Identify Opportunities for Investment  
**Runs:** Automatically (no human decision needed)  
**Time:** ~1 minute  
**Input:** Sheet 4 (Investment Positions) + Sheet 5 (Market Rates & Policy)  
**Output:** JSON ratings summary — numeric credit scores for each counterparty

---

## What this agent does

The Ratings Sub-Agent converts the text credit ratings (e.g. AA+, A-, BBB+) from your Investment Positions sheet into a standardised numeric score. This allows the Opportunity Agent to objectively rank counterparties by credit quality and select the highest-rated option that still has headroom. It also flags any counterparty that falls below your policy minimum rating.

> **Note:** This agent runs in parallel with the Compliance Sub-Agent (Step 3). You can run Steps 2 and 3 simultaneously in two separate browser tabs if you want to save time.

---

## Prerequisites

Before running this step, make sure you have:

- [ ] Completed Step 1 and saved the Reporting Agent JSON output
- [ ] Your `treasury_data.xlsx` open with the **Investment Positions** and **Market Rates & Policy** sheets ready to copy

---

## Step-by-step instructions

### 1. Open a new chat in Claude.ai

Go to [claude.ai](https://claude.ai) and click **New chat**. This must be a fresh conversation — do not continue in the Step 1 chat.

---

### 2. Copy this system prompt

Copy the entire block below and paste it as your **first message**:

---

```
You are a credit ratings assessment agent for treasury investments.

Convert credit ratings to a numeric score using this scale:
AAA = 22
AA+ = 21
AA  = 20
AA- = 19
A+  = 18
A   = 17
A-  = 16
BBB+ = 15
BBB  = 14
BBB- = 13
BB+  = 12
BB   = 11
BB-  = 10
B+   = 9
B    = 8
B-   = 7
CCC+ = 6
CCC  = 5
CCC- = 4
CC   = 3
C    = 2
D    = 1

For each counterparty in the Investment Positions sheet:
- Record their credit rating as given
- Convert to numeric score using the scale above
- Compare against the Min_Credit_Rating from the policy sheet
- Set meets_policy = true if their score >= the policy minimum score

Return ONLY valid JSON in this exact schema — no other text before or after:

{
  "policy_min_rating": "A-",
  "policy_min_score": 16,
  "ratings_summary": [
    {
      "counterparty": "...",
      "rating": "AA+",
      "numeric_score": 21,
      "meets_policy": true,
      "margin_above_minimum": 5
    }
  ],
  "counterparties_below_minimum": []
}

Return no other text. Do not add any explanation before or after the JSON.
```

---

### 3. Copy your Investment Positions data from Excel

1. Open `treasury_data.xlsx`
2. Click the **Investment Positions** sheet tab
3. Select all data: click **A1**, press `Ctrl+Shift+End`, then `Ctrl+C`

---

### 4. Copy your Market Rates & Policy data from Excel

1. Click the **Market Rates & Policy** sheet tab
2. Select all data the same way and copy

---

### 5. Send the data to Claude

In the same chat, send a new message in this format:

```
INVESTMENT POSITIONS:
[paste your Investment Positions sheet data here]

POLICY MINIMUM RATING (from Market Rates & Policy sheet):
[paste your Market Rates & Policy sheet data here]
```

> **Tip:** You only need to paste the `Min_Credit_Rating` row from the Policy sheet for this agent — you do not need to paste the entire policy sheet. However, pasting the full sheet is also fine.

---

### 6. Review Claude's JSON output

Claude will return a ratings assessment JSON. Example of what to expect:

```json
{
  "policy_min_rating": "A-",
  "policy_min_score": 16,
  "ratings_summary": [
    {
      "counterparty": "Barclays",
      "rating": "AA+",
      "numeric_score": 21,
      "meets_policy": true,
      "margin_above_minimum": 5
    },
    {
      "counterparty": "JPMorgan",
      "rating": "AAA",
      "numeric_score": 22,
      "meets_policy": true,
      "margin_above_minimum": 6
    },
    {
      "counterparty": "HSBC",
      "rating": "AA-",
      "numeric_score": 19,
      "meets_policy": true,
      "margin_above_minimum": 3
    },
    {
      "counterparty": "Deutsche Bank",
      "rating": "A+",
      "numeric_score": 18,
      "meets_policy": true,
      "margin_above_minimum": 2
    }
  ],
  "counterparties_below_minimum": []
}
```

> **What to look for:** Any counterparty in `counterparties_below_minimum` cannot be recommended by the Opportunity Agent. If a key counterparty appears there, you may need to review whether your policy minimum is current.

---

### 7. Save the output

Copy the full JSON and save it in your text editor:

```
=== STEP 2 OUTPUT — RATINGS SUB-AGENT ===
[paste JSON here]
```

---

## Credit rating reference table

Use this table to verify or cross-check the agent's numeric scores:

| Rating | Score | Category |
|--------|-------|----------|
| AAA | 22 | Prime |
| AA+ | 21 | High grade |
| AA | 20 | High grade |
| AA- | 19 | High grade |
| A+ | 18 | Upper medium |
| A | 17 | Upper medium |
| **A- (policy floor)** | **16** | **Upper medium** |
| BBB+ | 15 | Lower medium |
| BBB | 14 | Lower medium |
| BBB- | 13 | Lower medium |

> Ratings below BBB- are considered below investment grade and will always fail the policy check.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Numeric scores look incorrect | Check the rating column in Sheet 4 — common issues are spaces (e.g. "AA +" instead of "AA+") or lowercase letters |
| `counterparties_below_minimum` is unexpectedly long | Verify the `Min_Credit_Rating` value in Sheet 5 — if it was recently updated, some counterparties may now be excluded |
| A counterparty appears twice in the output | This happens when the same counterparty has multiple positions with different ratings — the agent should use the most conservative (lowest) rating |

---

## What to do next

Once you have saved the Step 2 JSON output, proceed to:

**→ [Step 3 — Compliance Sub-Agent](03_compliance_agent.md)**

---

*Source: Treasury Investment AI Agent Implementation Guide — Section 4.2 (Ratings Sub-Agent — now Step 2)*
