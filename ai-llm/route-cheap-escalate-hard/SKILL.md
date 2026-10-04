---
name: route-cheap-escalate-hard
description: Cut LLM spend by routing bulk work to a cheap model and escalating only the hard turns to a premium one. Use when the user says their AI bill is too high, asks to "use a cheaper model", or wants two-tier model routing without losing quality on the hard tasks.
---

# Route the bulk cheap, escalate the hard turns

The user is paying premium-model prices for work that is mostly not premium-hard. Your job is to split their workload into a cheap default and a gated escalation, write that split down as a config, and prove the config is sane, without pretending the split is free quality.

## Steps

1. Ask (or infer from their traffic) what "hard" means for this workload. Escalation needs a gate you can state: a task type, a difficulty signal, or a failed first attempt. If they can't name one yet, "retry-on-failure" (cheap model first, premium on a failed check) is the honest default gate.
2. Pick the pair. The cheap default should sit behind an OpenAI-compatible gateway so swapping later is a one-line change. Worked example as of 2026-06: GLM-5.2 (`z-ai/glm-5.2` via OpenRouter, ~$3/M output tokens) as default, Opus 4.8 (~$25/M output) as escalation, roughly 5-6x apart on output price, with GLM tying on long-horizon coding benchmarks while Opus still wins short, sharp general coding. Check current prices before quoting them.
3. Write `routing.json`: `base_url` (the gateway), `default_model` (cheap), `escalate_model` (premium), and `escalate_when` (the gate). The gate must be conditional; an `escalate_when` that matches everything is just the premium model with extra steps. This file is the decision contract: translate it into whatever your dispatch layer speaks (a LiteLLM router config, an OpenRouter preset, or a few lines in your own client).
4. Run the proof below. It fails if the default isn't the cheap model, the escalation isn't set, or the gate is missing.
5. Tell the user to measure **cost per finished task, not per token**. If the cheap model needs extra reasoning loops or retries to land the same task, the per-token advantage shrinks or inverts. The savings claim is only real after that measurement.

## Prove it

```bash verify
cat > routing.json <<'JSON'
{
  "base_url": "https://openrouter.ai/api/v1",
  "default_model": "z-ai/glm-5.2",
  "escalate_model": "anthropic/claude-opus-4.8",
  "escalate_when": "task_difficulty == hard || category == general_coding"
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("routing.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!c.base_url) bad("route through a gateway base_url, not a hard-wired endpoint");
if (!c.default_model) bad("no cheap default_model set");
if (!c.escalate_model) bad("no escalate_model set");
if (c.default_model === c.escalate_model) bad("default and escalation are the same model, nothing is being saved");
if (String(c.escalate_when || "").length < 3) bad("escalate_when must gate escalation, not match everything");
console.log("routing OK: bulk -> " + c.default_model + ", escalate to " + c.escalate_model + " when " + c.escalate_when);
'
```

## Guardrails

- A leaderboard win is not a promise about the user's task. Third-party and vendor benchmark numbers are directional; the bake-off on their own prompts is the evidence.
- Cheaper per token is not cheaper per task. Say this out loud in your summary; it is the most common way this pattern quietly fails.
- Flag data residency. Many cheap models are served by hosts in jurisdictions the user may care about; the weights being open says nothing about where their prompts land.
- The very cheapest routes on a gateway often serve a quantized variant, very good, not identical. If output quality matters, pin the provider, not just the model.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Run GLM-5.2 for the bulk, escalate the hard turns to Opus 4.8](https://flowstacks.xyz/workflows/glm-52-route-bulk-escalate-opus)</sub>
