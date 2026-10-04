---
name: advisor-call-budget
description: Enforce a hard cap and a drift-check when a cheap executor model consults an expensive advisor model, and compute the effective cost from actual call counts instead of a benchmark's assumed rate. Use when the user adopts the advisor or orchestrator pattern, pairs a cheap model with an expensive reviewer, or quotes a benchmark discount like "63% of the price".
---

# Cap the advisor, catch the drift, compute the real discount

The advisor pattern (a cheap model executes; an expensive model is consulted *rarely*) is only as cheap as the word "rarely". The user is about to adopt it on the strength of a benchmark number. Your job is to make the savings enforceable instead of assumed: a hard cap on advisor calls, a drift-check so the executor can't run unchecked, and an effective-cost number computed from what actually happened.

## Steps

1. Write down the pair with real unit prices: the executor model and the advisor model, each with `usd_per_mtok_out` from the current pricing page (never from memory). The reference result this pattern leans on: Anthropic's internal eval had Sonnet 5 executing with Fable 5 advising about once per task, landing ~92% of Fable's SWE-bench Pro score at ~63% of the price. That is their task and their call rate, not the user's.
2. Set `max_advisor_calls` for the task, a hard cap, not a hope. An uncapped advisor erodes the discount one "just checking" call at a time.
3. Set `drift_check_every_n_steps`: past this many executor steps, the executor must get a fresh advisor check-in before continuing. Between check-ins the executor can silently drift from the advice it was given; this bounds how far.
4. After (or while) running, record `advisor_calls_actual` and compute the effective cost from the **actual** call mix. Compare it against the benchmark's assumed rate. If the task pulled the advisor in more often than "about once", the real discount is smaller than the quoted one, say by how much.
5. Run the proof below. It fails on a missing cap, a missing drift-check, or an actual call count that blew the budget.

## Prove it

```bash verify
cat > advisor-task.json <<'JSON'
{
  "executor": { "model": "sonnet-5", "usd_per_mtok_out": 15 },
  "advisor": { "model": "fable-5", "usd_per_mtok_out": 50 },
  "max_advisor_calls": 3,
  "drift_check_every_n_steps": 5,
  "task": { "steps": 20, "advisor_calls_actual": 2 }
}
JSON
node -e '
const c = JSON.parse(require("fs").readFileSync("advisor-task.json", "utf8"));
function bad(m) { console.error("BAD: " + m); process.exit(1); }
if (!c.max_advisor_calls || c.max_advisor_calls < 1) bad("set a hard max_advisor_calls, an uncapped advisor erodes the discount");
if (!c.drift_check_every_n_steps || c.drift_check_every_n_steps < 1) bad("set drift_check_every_n_steps so the executor cannot run unchecked forever");
const t = c.task || {};
if (t.advisor_calls_actual == null) bad("record advisor_calls_actual so the real rate can be compared to the assumed one");
if (t.advisor_calls_actual > c.max_advisor_calls) bad("advisor_calls_actual exceeds max_advisor_calls, the budget was not enforced");
const mix = t.advisor_calls_actual / (t.steps || 1);
const eff = ((1 - mix) * c.executor.usd_per_mtok_out + mix * c.advisor.usd_per_mtok_out) / c.advisor.usd_per_mtok_out;
console.log("advisor OK: cap " + c.max_advisor_calls + ", actual " + t.advisor_calls_actual + " call(s) over " + t.steps + " steps; effective cost ~" + Math.round(eff * 100) + "% of pure-advisor rate");
'
```

## Guardrails

- Never present 63% (or any benchmark discount) as the user's number. It was measured on two specific benchmarks with a specific call rate; their workload has neither.
- The pattern assumes hard reasoning concentrates at a few forks. If difficulty is spread evenly across the task, one check-in per task misses it and the executor drifts uncaught, that workload should not use this pattern.
- If the job is easy, skip the pattern entirely and run the cheap model alone. Orchestration only pays for itself on hard, multi-step work.
- Don't let the planner grade its own plan. If advisor and executor share a wrong assumption, this setup amplifies it with confidence; put an objective check (test, schema, known answer) wherever correctness matters.

---

<sub>Backed by a machine-verified recipe, re-checked by CI: [Advisor pattern: cap how often the expensive model gets called](https://flowstacks.xyz/workflows/advisor-pattern-call-budget-and-drift-check)</sub>
