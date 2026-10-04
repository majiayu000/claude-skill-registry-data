---
name: pii-detector
description: >
  Proactive PII add-on — augments the main response with PII guidance.
  Auto-trigger on any form, schema, migration, model, API route, GraphQL
  resolver, auth flow, or data design discussion. Also fires on: middleware,
  webhooks, workers, seed/fixture/factory files, delete/export/purge/anonymize
  functions, cron jobs, HTTP clients, controllers, services, resolvers.

  Trigger phrases: "build a form", "collect X data", "what fields should
  I include", "how should I design the schema", "POC / lead / contact /
  user / customer information", "store / save / persist X", "sign up /
  login / auth / registration", "share thoughts on how to build".

  Trigger on field names: email, phone, name, dob, ssn, card, cvv, password,
  token, secret, api_key, health, biometric, ip_address, salary, session,
  device_id, notes, metadata (on user-facing models).
---

# PII Developer Skill — USA Focus

Automatic PII checks during development. Fires on both what the user asks for
AND what Claude is about to generate — not just on keyword matching.

---

## Core Principle

Check before generating. Never produce code and then suggest fixes.
The sequence is always: detect intent → run relevant checks → generate correct code.

If there is ANY ambiguity — check it. False positives are cheap.
Missed PII in production is a breach, a fine, or both.

When suggesting fixes, use the language, framework, and idioms of the code
being reviewed. Never suggest a fix in a different language than the one
being written. If the codebase is Python, fix in Python. If Rails, fix in
Ruby. If Go, fix in Go. Claude infers the language from context — no need
to specify.

---

## Step 1 — Detect the Mode

Read the user's request AND what Claude is about to produce.
Choose the mode first — this determines everything else.

**Planning / Review mode** — user is discussing, designing, reviewing,
or asking Claude to read/check existing code. No new code being generated.
→ Load: `modes/planning.md`
→ Enrich Claude's natural response with PII notes. No standalone report.

Signals: "review", "read", "look at", "check this", "share thoughts",
"how should I build", "I want to build X", "help me design", "feedback on",
"thoughts on", reading or analyzing an existing file without generating new code.

**Generation mode** — Claude is about to write new code from scratch.
→ Load relevant layer(s) from the table below. Check first, generate second.

Signals: "build it", "create", "generate", "write", "implement",
"scaffold", "make", "add this feature" — active code production.

**Repo scan mode** — user explicitly requests a full audit.
→ Load: `modes/repo-scan.md` + all layers.

Signals: "scan my repo", "full audit", "PII report", "check all my models",
"audit my codebase".

When in doubt between planning/review and generation: default to planning/review.
Enriching a response is always safer than running a check that wasn't needed.

---

## Step 2 — Generation Mode: Map to Layers

Only applies when generating new code. Multiple layers can apply simultaneously.

| What's being built | Layers to load |
|---|---|
| Database model / schema / migration | `patterns/fields.md` + `rules/non-negotiables.md` + `modes/inline.md` |
| Login / signup / auth / registration | `layers/auth-sessions.md` + `rules/non-negotiables.md` |
| Frontend form / page / component | `layers/frontend.md` |
| API route / controller / serializer | `layers/api-layer.md` |
| Middleware / request handler / logger | `layers/data-in-transit.md` |
| JWT / token / session / cookie code | `layers/auth-sessions.md` |
| Webhook handler | `layers/data-in-transit.md` + `layers/api-layer.md` |
| Seed file / fixture / factory / test helper | `layers/testing-seeding.md` |
| Delete / purge / anonymize / export function | `layers/data-lifecycle.md` |
| Cron job / background worker / cleanup task | `layers/data-lifecycle.md` |
| External API client / HTTP call | `layers/data-in-transit.md` |
| Analytics / tracking integration | `rules/leakage-vectors.md` |
| Error handling / monitoring setup | `rules/leakage-vectors.md` |
| Full repo / codebase submitted | ALL layers — load `modes/repo-scan.md` |

When multiple layers apply (e.g. building an auth API endpoint):
load all relevant layers and merge the checks.

Always load `patterns/fields.md` when a model or schema is involved.
Always load `rules/non-negotiables.md` when any PII field is detected.

---

## Step 3 — Regulations (Always Apply All, Never Ask)

| Regulation | What It Means for Code |
|---|---|
| **CCPA/CPRA** | Every PII field must be deletable on request |
| **HIPAA** | Health data encrypted at rest + in transit; access logged on every read |
| **PCI-DSS** | Never store CVV; tokenize card numbers; never log payment bodies |
| **COPPA** | Flag age/dob fields; under-13 = parental consent, no behavioral tracking |
| **GLBA** | Financial data: encrypt, access control, audit logs |
| **BIPA** | Biometric: written consent before storage; retention limit required |
| **FERPA** | Student records: strict access controls, no sharing without consent |
| **FTC Act** | Do exactly what your privacy policy says |

---

## Step 4 — Run Checks, Then Generate (Inline Mode Only)

1. Load the relevant layer file(s) from Step 1
2. Run all checks defined in those layers against what's about to be built
3. Output findings in the standard format (see below)
4. Generate corrected code immediately — with all fixes already applied

Never generate broken code first. Never suggest fixes as an afterthought.
The check and the corrected output happen in a single pass.

---

## Output Format

**Inline (any single-task coding):**
```
⚡ PII Check — [what's being built]

🔴 Fix now:
  [specific issue] → [exact fix]

🟡 Fix soon:
  [specific issue] → [exact fix]

🟢 Consider:
  [suggestion]

Regulations: [only ones actually triggered]
```

Then generate the corrected code immediately after.

**Repo scan:** structured report with file + line references. Load `modes/repo-scan.md`.

Rules for all output:
- Reference actual field names, file names, and line numbers — never be generic
- "Encrypt `ssn` with AES-256, store as BYTEA" not "encrypt sensitive fields"
- Skip empty sections — don't pad with N/A categories
- List only regulations actually triggered by findings
