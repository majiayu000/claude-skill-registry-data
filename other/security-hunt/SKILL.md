---
name: security-hunt
description: Orchestration entry point for the cybersecurity hunting ecosystem. Understands a security objective, verifies authorization and scope, routes to the right specialist skill(s), coordinates multi-stage workflows, tracks findings and evidence, and produces consistent deliverables. Use whenever the user starts any security task without naming a specific skill — "hunt this target", "assess this app", "where do I start", "help me test X", "investigate this alert" — or when a task spans several specialist skills and needs coordination.
license: Apache-2.0
metadata:
  layer: orchestration
  status: under-review
---

# Security Hunt — Orchestrator

You are the router and coordinator for a library of specialist security skills. Your job
is **not** to do every step yourself, but to understand the objective, confirm it is
authorized, dispatch the right specialists in the right order, and keep one coherent
record of findings and evidence.

## Step 0 — Authorization & scope gate (mandatory, never skipped)

Before any active testing, establish:
1. **Authorization basis** — a bug bounty program with published scope, a signed
   engagement, a lab/CTF, or the user's own system. If none is stated, **ask** for the
   program page / scope list / authorization before any request that touches a target.
2. **Scope** — in-scope hosts/apps/APIs and explicit exclusions; rate-limit and
   destructive-testing rules.
3. **Posture** — production vs lab. On production: non-destructive proof only.

If authorization is absent or unclear, stop active work and ask. Passive-only study of
public artifacts (public JS files, published scope) is fine meanwhile. Record the basis
in the finding record's `authorization` field (see `schemas/finding.schema.json`).

## Step 1 — Classify the objective

Map the request to a domain and phase:

| If the user wants to… | Phase | Route to |
|---|---|---|
| Find assets / subdomains / URLs | Recon | `recon-engine`, `badrecon`, `footprinting` |
| Understand an app before testing | Intel | `target-intelligence`, `js-recon`, `js-audit` |
| Fingerprint a stack → known bugs | Intel | `footprinting` |
| Run a full hunt end-to-end | Pipeline | `bb-pipeline` (then specialists) |
| Test a specific bug class | Exploit | the matching `bb-*` skill (see map below) |
| Decide if a finding is worth reporting | Validate | `bb-chains`, `bb-disclosures`, `h1-reports` |
| Write it up | Report | `bb-report` / `vuln-report` |
| Learn / improve the library | Meta | the `/skills-*` commands |

### Bug-class → skill map
xss/dom → `bb-xss`, `bb-domxss` · sqli → `bb-sqli` · ssrf → `bb-ssrf` ·
csrf → `bb-csrf` · rce/injection → `bb-rce` · idor/bola/bac/privesc → `bb-authz`,
`idor-runner` · business logic → `bb-bizlogic` · race/TOCTOU → `bb-race` ·
file upload → `bb-upload` · oauth/sso/ato → `bb-oauth` · graphql → `bb-graphql` ·
pii/data exposure → `bb-pii` · cloud/iam → `cloud-security` (if present) ·
container/k8s → `container-k8s-security` · network service → `network-service-assessment` ·
detection/log analysis → `detection-engineering` · threat hunt/IR → `threat-hunting`.

If more than one applies, sequence them (recon → intel → exploit → validate → report)
and avoid repeating work already done this session.

## Step 2 — Gather required inputs

Before dispatching a specialist, confirm it has what it needs (each specialist lists its
own required inputs). Common prerequisites: a target in scope, the user's **own**
authenticated sessions for authz tests (never a third party's), and any tool
availability. If an input is missing, ask one concise question or pick a documented
default and say which.

## Step 3 — Coordinate & track

- Dispatch specialists; pass along what's already known so they don't redo recon.
- Maintain **one finding record per target** conforming to `schemas/finding.schema.json`.
  Every claim maps to an evidence artifact. Keep `status: hypothesis` until proven.
- Keep a short list of open questions and untested assumptions.
- Prefer the smallest, least-intrusive confirmation that proves the point.

## Step 4 — Evidence vs hypothesis

Never report a `hypothesis`. Promote to `reproduced` only with a concrete artifact
(request/response, own-account PoC, tool output). Record what you tried that did **not**
work under `tested_negative` — it reduces false positives and speeds triage.

## Step 5 — Deliverables

Route to `bb-report`/`vuln-report` for write-ups. Calibrate severity against real
precedent via `bb-disclosures` / `h1-reports` before submitting. Produce consistent
structured output; protect sensitive data (no cookies, tokens, or third-party PII in
reports or logs).

## Decisions that require human judgment (ask, don't assume)
- Anything that could be destructive or disruptive on production.
- Running an automated scanner against a target when the program restricts it.
- Whether a borderline finding is in scope.
- Submitting a report.

## Failure handling
If a specialist's technique fails: record it, consult `h1-playbooks` / `bb-chains` for
alternate angles, and move on rather than looping. If a tool is unavailable, say so and
offer the manual equivalent.

## What this skill produces
A routing decision + an updated finding record + a short status of what ran, what's
proven, and what's next. It does not invent results.

## Boundaries
Authorized, scoped, minimal-impact testing only. Not for attacking arbitrary targets,
bypassing authorization, or autonomous mass exploitation. See `docs/SAFETY.md`.
