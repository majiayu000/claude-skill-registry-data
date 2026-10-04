---
name: token-receipts-audit
description: Attribute AI usage by tokens AND dollars so a high-volume cheap model is never mistaken for the expensive one. Use when the user asks where their AI spend actually goes, why the bill is high, which model is costing the most, or wants a usage audit across agents and models.
---

# Read the token receipts right: volume and cost are different leaderboards

Token rankings lie by omission: cheap open models win volume (they sit in busy agent loops), premium models win spend (they take the fewer, harder calls). The public version of this flip, from OpenRouter's June 2026 rankings: Anthropic models were ~12% of tokens but roughly 46% of revenue. The user's own receipts almost certainly hide the same flip. Your job is to compute it, show it, and stop them optimizing the wrong line.

## Steps

1. Get the usage export: tokens per model over a real period (a month, not a week; weekly snapshots are volatile and free-preview models spike then vanish). A gateway dashboard export works; so does a hand-assembled list.
2. Tier every model `cheap_open` or `premium`, and attach each model's unit price (`usd_per_mtok`) from the current pricing page, never from memory.
3. Compute, per tier: share of total tokens and share of total dollars. The signature of a healthy split is the flip: cheap models dominate volume, premium dominates cost.
4. Report it as one table plus one sentence: "X% of your tokens cost Y% of your money." Then the actionable read: if premium's cost-share is high *and* its calls look like bulk work, that's the routing bug to fix (see `route-cheap-escalate-hard`); if premium's cost-share is high on genuinely hard calls, the spend is earning its keep.
5. Run the proof below on their real numbers (the example uses the June 2026 public shape).

## Prove it

```bash verify
cat > receipts.json <<'JSON'
{
  "period": "2026-06",
  "models": [
    { "name": "DeepSeek V4 Flash", "tier": "cheap_open", "tokens": 167000000000, "usd_per_mtok": 0.28 },
    { "name": "GLM 5.2", "tier": "cheap_open", "tokens": 50200000000, "usd_per_mtok": 3.00 },
    { "name": "Claude Opus 4.8", "tier": "premium", "tokens": 14800000000, "usd_per_mtok": 25.00 }
  ]
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("receipts.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if ((c.models || []).length < 2) bad("need at least two models to compare");
let totTok = 0, totCost = 0; const tierTok = {}, tierCost = {};
for (const m of c.models) {
  if (!m.tier || m.tokens == null || m.usd_per_mtok == null) bad("each model needs tier, tokens, usd_per_mtok");
  const cost = (m.tokens / 1e6) * m.usd_per_mtok;
  totTok += m.tokens; totCost += cost;
  tierTok[m.tier] = (tierTok[m.tier] || 0) + m.tokens;
  tierCost[m.tier] = (tierCost[m.tier] || 0) + cost;
}
const pct = (x, t) => (x / t * 100).toFixed(1);
console.log("receipts OK: cheap_open is " + pct(tierTok.cheap_open || 0, totTok) + "% of volume but " + pct(tierCost.cheap_open || 0, totCost) + "% of cost; premium is " + pct(tierTok.premium || 0, totTok) + "% of volume but " + pct(tierCost.premium || 0, totCost) + "% of cost (volume != value)");
'
```

## Guardrails

- Never read a high token ranking as "best model" or "biggest cost". It usually means "cheap model in a busy loop", that's the whole point of this audit.
- Gateway receipts are incomplete by construction: usage on direct provider keys or private deployments never appears there. State what the export can and cannot see.
- Attribute over a real period. One anomalous week (a migration, a runaway loop, a free preview) will produce a confident wrong conclusion.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Read your token receipts right](https://flowstacks.xyz/workflows/token-volume-vs-cost-receipts)</sub>
