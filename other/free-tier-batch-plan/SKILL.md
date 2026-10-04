---
name: free-tier-batch-plan
description: Size a big one-time batch job against a free tier's rate limit and token budget BEFORE starting it, with a proven wall-clock ETA. Use when the user wants to label a dataset, summarize an archive, or process a large backlog for free (or on a tiny rate limit), or asks "will this finish overnight?"
---

# Prove the batch fits before you start it

Some free tiers have a strange, exploitable shape: a painfully low rate ceiling paired with a huge monthly token budget (Mistral's free Experiment tier, as of 2026-06: about 2 requests/minute but around a billion tokens/month). Useless for anything live; ideal for a patient overnight grind. The failure mode is starting the job unsized and finding it stalled, or 12% done, in the morning. Your job is the arithmetic, up front.

## Steps

1. Count the backlog: how many items, and a realistic `est_tokens_per_item` (input + output; when unsure, run 3 samples and measure rather than guessing).
2. Look up the tier's actual limits (the rate ceiling in requests/minute and any monthly token budget) from the provider's current docs, not from memory or this file.
3. Compute two numbers and show both:
   - **Budget fit:** items x tokens/item vs. the monthly budget. Over budget means shrink the job or split it across months.
   - **ETA:** items / (rpm x 60) hours at the ceiling. This tells the user whether "overnight" is 8 hours or 3 days; both are fine, but only if known in advance.
4. Run the proof below; it fails on a job that doesn't fit its budget.
5. Only then queue it, with a runner that actually paces to the rate limit (bursting past it gets throttled or banned, which destroys the ETA you just computed).

## Prove it

```bash verify
cat > batch.json <<'JSON'
{
  "provider": "mistral",
  "items": 3000,
  "rate_limit_rpm": 2,
  "est_tokens_per_item": 1200,
  "monthly_token_budget": 1000000000
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("batch.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!c.items || c.items < 1) bad("no items to process");
if (!c.rate_limit_rpm || c.rate_limit_rpm < 1) bad("rate_limit_rpm must be at least 1");
if (!c.est_tokens_per_item || c.est_tokens_per_item < 1) bad("est_tokens_per_item must be set (measure 3 samples if unsure)");
const used = c.items * c.est_tokens_per_item;
if (c.monthly_token_budget && used > c.monthly_token_budget) bad("job needs " + used + " tokens but the monthly budget is " + c.monthly_token_budget);
const etaH = (c.items / (c.rate_limit_rpm * 60)).toFixed(1);
console.log("batch OK: " + c.items + " item(s) at " + c.rate_limit_rpm + " req/min = ~" + etaH + "h, using " + used + " of " + c.monthly_token_budget + " monthly tokens");
'
```

## Guardrails

- Nothing live or interactive belongs on a 2-requests/minute tier. This pattern is for a one-time backlog with nobody waiting on it.
- Free tiers often use prompts to improve models. Sensitive or confidential material goes on a paid tier; still pennies, and worth it.
- This pays off for a single big grind, not recurring work. If the same batch runs weekly, price a paid lane and compare honestly.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Grind a huge one-time job overnight on a free tier](https://flowstacks.xyz/workflows/free-tier-overnight-batch)</sub>
