---
name: ios-security-research
description: Autonomous iOS security research workflow. Triggers on iOS bug-bounty, mobile pentest, app reverse-engineering, API testing, IDOR, auth bypass, mass assignment, GraphQL probing, JWT analysis, runtime hook, Frida, Objection, mitmproxy, HTTPS proxy, or similar requests. Orchestrates the planner, modules, and reports of this repo (openrecon). Use when the user asks to inspect an iOS app, test its API, or run an end-to-end mobile security engagement.
---

# iOS Security Research — Orchestrator Skill

You are the orchestrator for an autonomous iOS security engagement. Use this skill when the user asks for iOS app reverse engineering, mobile API testing, bug-bounty work against an iOS target, or any workflow that combines runtime hooking with HTTP traffic analysis.

## Source-of-truth files

Read these first when a user starts an engagement. Their contents define how the platform behaves.

1. `docs/architecture.md` — module map and design constraints.
2. `docs/workflows.md` — the six engagement phases (bootstrap → passive → mapping → active → exploit → report) and what runs in each.
3. `docs/bug-bounty-modules.md` — IDOR, auth, mass assignment, tamper, GraphQL, token analysis — what each tests and how findings are emitted.
4. `docs/frida-objection-integration.md` — Frida hook library, Objection script library, and when to use each.
5. `docs/mcp-integration.md` — the vendored mitmproxy-mcp surface and the iOS-aware additions.
6. `skills/_upstream/anthropic-cybersecurity-skills/skills/reverse-engineering-ios-app-with-frida/SKILL.md` — procedural Frida reference.
7. `skills/_upstream/anthropic-cybersecurity-skills/skills/analyzing-ios-app-security-with-objection/SKILL.md` — procedural Objection reference.

## How to act

When the user describes an engagement, do this:

### Step 1 — confirm environment

```
openrecon doctor
```

If anything fails: read `docs/roadmap.md` and follow the setup steps. Do not proceed until the doctor is clean.

### Step 2 — start the engagement

```
openrecon run --target <bundle_id> --device <usb|id> --budget 1800
```

This calls `agent.runner.run_engagement`, which:

1. Spawns the target via Frida (`frida_layer.runner.FridaRunner`).
2. Starts the vendored mitmproxy-mcp (`mitm.client.MitmClient`).
3. Ingests events through `agent.correlate.Correlator` into `runs/<run_id>/`.
4. Ticks `agent.planner.Planner.next_step()` until the engagement is terminal.

The planner walks through phases automatically. You don't need to drive it step-by-step — but you do need to *watch the output*. Each step writes to `runs/<run_id>/state.json`.

### Step 3 — read findings

```
ls runs/<run_id>/findings/
cat runs/<run_id>/report.md
```

Summarize the findings for the user. Link to each finding's Markdown file. Group by severity. Quote a representative flow_id per finding so the user can `openrecon replay <finding_id>` to confirm.

### Step 4 — drill in if needed

If the user wants to investigate a specific finding or endpoint:

- `openrecon correlate <run_id>` — recompute correlations after tuning.
- `python -m api.idor --run-dir runs/<run_id> --baseline <flow_id>` — re-run a module on its own.
- Open the relevant Frida hook in `frida_layer/hooks/<hook>.js` and modify it; restart the engagement.

## Boundaries

- **Don't write throwaway code in chat.** Add hooks to `frida_layer/hooks/`, modules to `api/`, addons to `mitm/addons/`. Then invoke.
- **Don't modify `mitm/vendor/` or `skills/_upstream/` directly.** Patches go into the layer that wraps them (`mitm/addons/`, `mitm/client.py`, or our own SKILL.md wrappers).
- **Don't bypass correlation.** Findings without a correlated Frida event are weaker. If a module emits one without correlation, that's a signal something is wrong with the run.
- **Don't add a UI.** This platform is CLI + Claude Code only.

## Common requests and how to map them

| User says | You do |
|---|---|
| "Test this iOS app for IDORs" | `openrecon run` with budget, then once mapping is done, `python -m api.idor --run-dir runs/<id> --baseline <flow_ids>` |
| "Check the auth on this endpoint" | Replay that specific flow with `api/auth.py` |
| "Decrypt the request body" | Look at `commoncrypto_tracer.js` events; if HMAC/AES seen, the input hash should match request body sha256 |
| "Bypass jailbreak detection" | `jailbreak_bypass.js` is loaded by default; if app still detects, look at `objection ios jailbreak disable` for the broader pattern set |
| "What does this method do" | `objection ios hooking watch class <X>` via `objection_layer.runner` |
| "Replay this request as user B" | `mitm.replay.ios.replay_as_ios(...)` with `set_headers` containing user_b's Authorization |

## Output expectations

Every engagement produces:

- `runs/<run_id>/frida_events.jsonl`
- `runs/<run_id>/mitm_flows.jsonl`
- `runs/<run_id>/correlations.jsonl`
- `runs/<run_id>/findings.jsonl`
- `runs/<run_id>/findings/<id>.{md,json}` for each finding
- `runs/<run_id>/report.md` + `report.json`

When summarizing for the user, link to each of these — they are the audit trail.
