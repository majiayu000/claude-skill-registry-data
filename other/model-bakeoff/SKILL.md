---
name: model-bakeoff
description: Choose a model with evidence by running the few prompts that actually matter across candidate models inside a free tier's caps, picking by a stated criterion. Use when the user asks "which model should I use", wants to evaluate a newly launched model, or is choosing between models for a specific task.
---

# Pick a model with evidence, not vibes

A "GPT-killer at a tenth of the price" launches roughly every other week, and the user's realistic options are (a) ignore it and maybe overpay forever, or (b) burn a day benchmarking. There's a third option: a one-afternoon bake-off on a free tier, sized so it provably fits the cap before it starts. GitHub Models (as of 2026-06) exposes 45+ models, frontier ones included, behind an existing GitHub login, capped around 50 requests/day on top models: too tight for production, exactly enough for a careful comparison.

## Steps

1. Collect the prompts that actually matter: 3-7 real examples of the user's task, with a known-good answer or a concrete scoring rule each. Not synthetic puzzles; the actual tickets, extractions, or drafts this model will face.
2. Pick 2-4 candidate models. Include the incumbent (the model currently doing the job) so the bake-off can conclude "keep what you have"; that is a valid and cheap outcome.
3. State `select_by` **before** running: exact-match rate, win rate on pairwise comparison, latency-under-quality-bar; anything, as long as it's written down first. A criterion chosen after seeing outputs is a rationalization.
4. Check the arithmetic: prompts x models must fit the free daily cap, or the bake-off dies at the rate limit halfway through with a biased partial result. Run the proof below.
5. Run, score, keep the winner; then move the workload to whichever provider hosts the winner properly. The free tier was for deciding, not serving.

## Prove it

```bash verify
cat > bakeoff.json <<'JSON'
{
  "prompts": ["summarize ticket", "extract fields", "classify intent", "draft reply", "rate sentiment"],
  "models": ["gpt-5.5", "deepseek-r1", "llama-4-maverick"],
  "select_by": "win_rate",
  "free_daily_cap": 50
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("bakeoff.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
const P = (c.prompts || []).length, M = (c.models || []).length;
if (P < 2) bad("need at least 2 prompts to compare meaningfully");
if (M < 2) bad("need at least 2 models for a bake-off");
if (!c.select_by) bad("no selection criterion stated before running (that is how rationalization starts)");
const calls = P * M;
if (c.free_daily_cap && calls > c.free_daily_cap) bad("bake-off needs " + calls + " calls but the free cap is " + c.free_daily_cap + "/day");
console.log("bakeoff OK: " + P + " prompt(s) x " + M + " model(s) = " + calls + " call(s), within " + c.free_daily_cap + "/day; pick by " + c.select_by);
'
```

## Guardrails

- The free tier is for deciding, not serving: roughly 10 requests/minute and 50/day on top models, with contexts capped near 8k in / 4k out; keep bake-off prompts compact and never point production at it.
- Scoring with an LLM judge inherits the judge's blind spots, especially when judge and contestant share a family. Prefer a concrete metric (exact match, schema-valid, tests pass) wherever one exists.
- One bake-off is a snapshot, not a marriage. Hosted models drift and reprice; for a workload where the choice keeps mattering, re-run the same bake-off on a schedule and keep the receipts.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [A GitHub Models bake-off that fits the free cap](https://flowstacks.xyz/workflows/github-models-prompt-bakeoff)</sub>
