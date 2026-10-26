---
name: engagement
description: Persistent authorization, scope, and progress state for a bug-bounty engagement, plus first-class ingestion of an existing recon directory. Establishes the authorization+scope gate ONCE per engagement and writes an engagement manifest (engagement.json) that every other skill reads so routine authorized research proceeds without repeated confirmation prompts. Classifies targets in-scope/out-of-scope/needs-clarification, keeps out-of-scope assets in a separate excluded inventory, builds a deduplicated master URL inventory from supplied recon output (txt/csv/json/jsonl), routes each URL to the right specialist, and tracks per-URL progress for resume. Use at the start of any hunt, when the user supplies a program/scope, when resuming a hunt, or when the user provides an existing recon folder to analyze.
license: Apache-2.0
metadata:
  layer: orchestration-support
  status: under-review
---

# Engagement — persistent authorization, scope & recon-folder ingestion

This skill owns the **engagement manifest**: the one durable record that lets the whole
ecosystem run a hunt continuously instead of re-asking the user for permission at every
step. It is the memory behind "understand the engagement once, then work."

Scripts (stdlib, run isolated — `python3 -I <script>`):
- `scripts/engagement.py` — create/reuse/update the manifest; classify targets; resume.
- `scripts/ingest_recon.py` — ingest a supplied recon directory into a hunt inventory.

Schema: `schemas/engagement.schema.json`. Format + resume rules: `docs/ENGAGEMENT.md`.

## 1. Establish the engagement ONCE (the only authorization gate)

At the start of a hunt, run the authorization + scope gate a **single** time:

1. Identify the program and the scope the user supplied (program page, a scope file, or
   an explicit statement that the targets belong to a program they are authorized to hunt).
2. Read any supplied rules, exclusions, testing restrictions, required headers, and rate
   limits. **Extract them from the supplied page/files/workspace automatically** — do not
   ask the user to retype what is already in front of you.
3. Write the manifest:

```bash
python3 -I scripts/engagement.py --workspace recon init \
  --program hackerone:acme --scope-source <url-or-path> \
  --roots "*.acme.com, api.acme.io" --exclude "blog.acme.com, *.vendor.com" \
  --rate-limit 5 --restrictions "no automated scanning; no DoS; payment flows need approval" \
  --header "X-H1: <researcher-tag>" --posture production
```

`init` is **idempotent**: if a manifest for the same program already exists it is
**reused** (status `reused`), not re-gated — this is how resume avoids re-confirming
scope. A *different* program in the same workspace is a conflict: a new or materially
changed scope gets its own workspace/engagement. **Authorization is never carried from
one program to unrelated targets.**

Never pass raw credentials, cookies, API tokens, or session secrets to the manifest. The
script refuses secret-shaped values (exit 2) so they cannot enter persistent state. The
`researcher-tag`/required headers stored here are non-secret identifiers only.

## 2. Once established, stop re-asking

When `authorization.established` is true for the engagement, do **not**:
- re-ask whether the target is authorized,
- ask for approval before each request, URL, vulnerability class, specialist, or batch,
- ask the user to choose each next phase,
- ask "should I continue?" after each success,
- redo the scope-confirmation when resuming with a valid saved state.

Automatically choose the next logical action and continue until the workflow is complete,
a **genuine blocker** occurs, or the permitted testing boundary is reached. If an
essential detail is genuinely missing or contradictory, ask **one** consolidated question
after exhausting the local files, supplied materials, and accessible program info — never
turn one gap into a sequence of prompts. For non-essential gaps, use documented defaults
that respect program rules and continue.

**Human approval is still required** for genuinely consequential actions (see
`docs/SAFETY.md`): destructive/disruptive production testing, a material scope ambiguity,
anything the program prohibits or restricts, mass test-account creation, payment-flow
testing, and any external report submission. Automation removes repeated *confirmations*,
never these gates.

## 3. Scope classification (never silently test the wrong thing)

```bash
python3 -I scripts/engagement.py --workspace recon classify app.acme.com blog.acme.com evil.com
```

Each target is `in_scope`, `out_of_scope`, or `needs_clarification`. Rules: exclusions
beat inclusions (an excluded host is never tested even when it shows up inside an in-scope
app's crawl output); a host matching no in-scope root is `needs_clarification` and is not
tested. Wildcards (`*.acme.com`, `*.cloud.acme.com`) match subdomains; a bare apex matches
only itself. Out-of-scope assets are recorded separately and never enter the hunt queue.

## 4. Recon: fresh vs supplied (decide, don't re-run blindly)

- **Fresh recon needed** → hand off to `recon-engine` (`scripts/recon.sh` is the standard
  active engine, vendored from the canonical repo `M0st8fa/Recon-Script`). **Before the
  run, verify the engine is current:** `python3 -I <recon-engine>/scripts/recon_sync.py
  status --dir <clone>` and, if `stale`/`missing`, `recon_sync.py ensure --dir <clone>`
  (then `setup.sh` if the toolchain is absent). Then check `recon.status`: if `running` or
  results already exist, do **not** launch a duplicate scan.
- **User supplied a recon directory** → ingest it instead of running recon again:

```bash
python3 -I scripts/ingest_recon.py <recon_dir> --workspace recon
```

This inventories the directory recursively, reads run config/logs first (recording which
tools ran, failed, or were skipped — a failed tool is *missing evidence*, never coverage),
extracts URLs from `.txt/.csv/.json/.jsonl`, and builds a **deduplicated master
inventory** (`inventory.jsonl`) that preserves meaningful variants (method, param-set,
endpoint — a POST is never collapsed onto a GET, a parameterized URL never onto its bare
path) with source provenance. In-scope URLs get a suggested specialist route and
`test_status: pending`; out-of-scope URLs go to `excluded_inventory.jsonl` and are never
scheduled. Re-running the ingest preserves prior `test_status`, `evidence`, and
`findings` (resume-safe).

## 5. Schedule every distinct in-scope URL

```bash
python3 -I scripts/ingest_recon.py <recon_dir> --workspace recon --next-batch 50
python3 -I scripts/ingest_recon.py <recon_dir> --workspace recon --next-batch 50 --route bb-authz
```

Process **all** distinct in-scope URLs, not just the homepage or the first few lines —
batch and prioritize, but impose no arbitrary cap that leaves the rest untested. Route by
endpoint semantics: object/API endpoints → `api-security`/`bb-authz`/`idor-runner`,
parameterized search → `bb-sqli`/`bb-xss`, redirect/fetch params → `bb-ssrf`, JS bundles →
`js-recon`/`js-audit`, auth/account endpoints → `bb-oauth`/`signup-agent`. Mark each URL's
`test_status` done as you go; resume from the inventory, never from scratch.

## 6. Progress, resume & coverage

```bash
python3 -I scripts/engagement.py --workspace recon resume     # next incomplete phase
python3 -I scripts/engagement.py --workspace recon set --phase routing --add-completed "inventory built"
```

Before declaring a hunt complete, review the inventory: which in-scope URLs were analyzed,
which checks passed/failed, which remain. **Do not claim full coverage while eligible work
remains, or while a tool failure left a gap.** Pass the manifest + inventory to specialists
so they inherit scope, completed work, and evidence instead of restarting the interview.

## Boundaries
Authorized, scoped, minimal-impact testing only. The manifest records authorization; it
does not grant it, and it never overrides program exclusions, rate limits, or prohibited
actions. See `docs/SAFETY.md`.
