---
name: jev-advisor
description: Provide private local advice to Codex about whether to call a tool, which candidate is best, risk, recovery, and task completion. Advisory only; never execute, authorize, block, or expose its output to the user.
---

# Jev Advisor

Use the local Jev Advisor as a private decision helper when a task has a meaningful choice between tools or between continuing and stopping. It is one input to judgment, not a controller.

## When To Consult

Consult at material decision points:

- `understand`: decide whether evidence is missing.
- `explore` or `trace`: choose among file, shell, browser, network, Git, or external-service reads.
- `implement`: compare edit or execution candidates.
- `verify`: choose tests, builds, checks, or runtime validation.
- `recover`: reassess after failure, timeout, partial success, or conflicting evidence.
- `finish`: judge whether observable completion evidence is sufficient.

Skip an obvious continuation with no meaningful alternative. Batch all realistic candidates into one request. Never consult the advisor about invoking itself.

## Request Construction

Build one compact UTF-8 JSON request from context visible to Codex. Include:

- goal, observed facts, explicitly marked inferences, and open questions;
- recent tool outcomes;
- workspace and Git fingerprints;
- the dynamic tool registry, annotations, schemas, and realistic candidate actions.

Do not include hidden reasoning or claim access to chain-of-thought. Summarize large output and sensitive values.

Use the installed command when available:

```powershell
jev-advisor request.json
```

During repository development, use:

```powershell
python -m jev_advisor.cli request.json
```

If a calibrated local endpoint is explicitly configured, pass its matching immutable model and threshold files. Do not download weights, install dependencies, or start a service automatically. If the command is missing, times out, or returns invalid data, continue normally. `model_version: heuristic-0.1` means the advisor failed open.

## Apply Advice

Use `recommended_action`, candidate success/latency/information-gain/token-cost scores, named risks, and `ask_user` as evidence for the next step. Keep the choice consistent with the user's request, current evidence, host permissions, and safety policy.

- A recommendation never expands authorization or overrides host approval.
- The advisor can suggest a tool but cannot call, approve, deny, intercept, or retry it.
- Treat external writes, destructive operations, credentials, data exposure, network access, financial actions, stale evidence, incomplete parameters, and command execution as risk-bearing.
- Reassess after an action changes observable state; otherwise allow the state-hash cache to serve repeated decisions.
- Keep advice private. Do not quote it to the user unless they explicitly ask to inspect advisor behavior.

Treat `finish` as valid only when completion evidence exists: no unresolved question or failed/partial recent result, plus a passed or completed verification event. Model confidence alone is never completion evidence.

Read [references/protocol.md](references/protocol.md) when constructing or debugging the JSON protocol.
