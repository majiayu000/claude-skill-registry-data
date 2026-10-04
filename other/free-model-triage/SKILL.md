---
name: free-model-triage
description: Route high-volume, low-stakes triage (reading piles, inbox summaries, needs-reply flags) to a free model with a strict output schema. Use when the user wants one-line summaries of many items cheaply, asks to triage email, articles, or reports with AI, or wants to decide what's worth reading without paying premium rates for it.
---

# Triage is a free-model job

Deciding what to read is a cheaper problem than reading: a one-sentence summary plus a needs-reply flag per item. Skimming twenty long items by hand runs about an hour; reading twenty one-liners and opening only what earned it is about fifteen minutes. On a top-tier paid model that triage volume costs real money every month; on a gateway's free tier it costs nothing (OpenRouter free models, as of 2026-06: 20 requests/minute and 50/day, rising to 1,000/day once $10 of credit has ever been added). Your job is to wire the free lane with a schema strict enough that the output is usable, and to keep anything sensitive out of it.

## Steps

1. Confirm the pile fits the caps: daily item count vs. 50/day (or 1,000/day post-credit). Over the cap means batching across days or the cheapest paid model; still pennies.
2. Point any OpenAI-compatible client at `https://openrouter.ai/api/v1` with a model whose id ends in `:free`. That suffix is the contract; without it the "free" triage quietly bills.
3. Pin the output schema to exactly two fields: a string `summary` and a boolean `needs_reply`. The boolean is what makes triage actionable: a summary alone still makes the user read everything to find what needs them.
4. Give it one standing instruction ("Summarize in one sentence and flag whether it needs a reply") and run the proof below to validate the config shape.
5. Sort the results: needs-reply items first, everything else skimmable. The user opens what earned it.

## Prove it

```bash verify
cat > triage.json <<'JSON'
{
  "base_url": "https://openrouter.ai/api/v1",
  "model": "deepseek/deepseek-r1:free",
  "instruction": "Summarize this in one sentence and flag whether it needs a reply.",
  "response_schema": {
    "type": "object",
    "properties": {
      "summary": { "type": "string" },
      "needs_reply": { "type": "boolean" }
    },
    "required": ["summary", "needs_reply"]
  }
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("triage.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!String(c.base_url || "").includes("openrouter.ai")) bad("base_url does not point at OpenRouter");
if (!String(c.model || "").endsWith(":free")) bad("model id must end with :free, otherwise this quietly bills");
const props = (c.response_schema && c.response_schema.properties) || {};
if (!props.summary || props.summary.type !== "string") bad("schema missing a string summary");
if (!props.needs_reply || props.needs_reply.type !== "boolean") bad("schema missing a boolean needs_reply");
console.log("triage OK: free model " + c.model + " returns a one-line summary + needs_reply flag");
'
```

## Guardrails

- Free models are the most likely to retain or train on what they're sent. Anything private (client email, unreleased work, health, legal) goes to a cheap **paid** model instead; the difference is pennies and the policy is better.
- Triage decides what to read; it does not replace reading. A one-line squeeze sometimes flattens the one detail that mattered, so the flagged items still get opened.
- Respect the caps in the design, not in the error handler: 20/minute and 50/day sized up front, per `free-tier-batch-plan`, beats discovering the limit mid-pile.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Let a free model triage your reading](https://flowstacks.xyz/workflows/openrouter-free-triage)</sub>
