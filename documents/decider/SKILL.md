---
name: decider
description: Decider is an intelligent skill router and orchestrator. It detects the current project phase (planning, implementing, debugging, testing, shipping, etc.), flags quality gaps in completed phases, and routes to the right skills for where the project actually is — not just what the user asked for. Use it whenever a situation needs to be analysed to decide which skill(s) should handle it — whether called by another skill (like thinker) or triggered directly. Trigger on phrases like "what skill should I use", "figure out what to do with this", "handle this", "which skill fits here", "use the right skill for this", or any time a task arrives without a clear single skill owner. Also trigger automatically when any other skill delegates a decision to decider.
---

# Decider

Decider analyses a situation, detects the current project phase, flags quality gaps in what's already been done, and routes to the right skill(s). It can be called by the user directly or invoked by another skill (thinker calls it at Phase 3 and Phase 5).

For any task that **changes code**, decider's output is a **Role Ledger** — a fixed role-staged pipeline (`PLAN → EXECUTE → [SECURE/A11Y/PERF] → REVIEW → TEST → VERIFY`) with a status per role, where the closing trio (REVIEW → TEST → VERIFY) is **always mandatory** and may never be silently dropped. See "The role-staged pipeline" below.

For non-code tasks (research, a doc, a decision, a conversational answer), the output is simpler — one of three things:
- A confident pick → announce + proceed
- An uncertain pick → show the options, ask the user
- No fit → say so clearly, then handle directly without a skill

---

## How decider thinks

Every time decider is called, it works through five steps in order:

---

### Step 0 — Detect project phase

Before picking any skills, determine where the project currently is. Read all available signals: git log, file structure, README, test files, conversation context, what the user just said.

**Phase signal table:**

| Signals present | Detected phase |
|---|---|
| No code yet, only ideas/notes/conversation | `PLANNING` |
| Architecture docs or spec exist, minimal code | `DESIGNING` |
| Active commits, new files being added, TODOs in code | `IMPLEMENTING` |
| Error messages, "it's broken", stack traces, failed tests | `DEBUGGING` |
| Test files being written or run, "does this work?", QA notes | `TESTING` |
| Security scan, code review comments, audit request | `AUDITING` |
| Deployment config being touched, "ready to ship?", final PR | `SHIPPING` |
| Live project, small patches, version bumps, hotfixes | `MAINTAINING` |
| Existing live project + new feature request | `UPDATING` |

If signals point clearly to one phase → state it confidently and proceed. If genuinely ambiguous → ask one short question to confirm. Do not ask if you're more than 80% confident.

**Announce the detected phase:**
```
→ Detected phase: IMPLEMENTING — active development in progress, no test files found yet.
```

---

### Step 1 — Flag quality gaps

After detecting the phase, check whether earlier phases were completed adequately. Raise flags for anything missing:

| Situation | Flag |
|---|---|
| IMPLEMENTING/later, but no spec or architecture doc | ⚠ No Technical Specification found — code has no written contract |
| IMPLEMENTING/later, but no system design | ⚠ No architecture diagram — structural decisions may be implicit |
| TESTING/later, but no test files | ⚠ No tests found — implementation is unverified |
| SHIPPING/later, but no security audit | ⚠ No security review before shipping |
| SHIPPING/later, but no QA pass | ⚠ No QA documentation found |
| TODO/FIXME comments in production paths | ⚠ Unresolved TODOs in critical code paths |

In **normal mode**: surface the flags, ask permission before addressing them. "I found these issues — address them first, or skip and continue?"

In **autonomous mode** (user said "act on your own" / "don't ask"): log the flags, proceed. Fix inline if it doesn't derail the main task; note as follow-up if it would.

---

### Step 2 — What is the actual task?

Strip the user's phrasing down to what needs to happen. Identify: the verb (build, analyse, write, debug, plan, research…), the object (a doc, a dashboard, a system, a spec, an idea…), and any constraints (language, format, audience, tech stack).

---

### Step 3 — What signals narrow the field?

Look for domain signals: engineering terms, ML language, design intent, data work. Look for output signals: does it need a file? A decision? A plan? A running app? Look for size signals: one-skill job or multi-domain?

Now combine with the detected phase — the phase is the strongest signal. A task in `DEBUGGING` routes differently than the same words in `IMPLEMENTING`.

---

### Step 4 — Which skills match, and how confidently?

Read `references/skill-catalogue.md` and map the task to candidates. Use detected phase to narrow the default skill set:

**Phase → default skill set:**

| Phase | Default skills to consider first |
|---|---|
| `PLANNING` | `thinker`, `brainstorming`, `what-if-oracle`, `writing-plans`, `idea-loop`, `sys-design` + `excalidraw-diagram` |
| `DESIGNING` | `arch` (code/folder structure), `sys-design` + `excalidraw-diagram`, `writing-plans`, `frontend-design`, `api-and-interface-design`, `database-schema-designer`, `documentation-and-adrs` |
| `IMPLEMENTING` | `executing-plans`, `test-driven-development`, `frontend-ui-engineering`, `backend-engineering`, `auth-and-authorization`, `api-communication`, `ai-app-engineering`, `security-and-hardening`, `git-workflow-and-versioning`, stack library skills (`zustand`, `framer-motion`, `threejs`, `stripe-integration-expert`, `localization`, `mcp-server-builder`…) |
| `DEBUGGING` | `systematic-debugging` (reproducible) or `debugging-and-error-recovery` (non-repro / triage), `observability-and-monitoring` (prod visibility — instrument to see the bug), `browser-testing-with-devtools`, `cybersec-web-security` / `security-and-hardening` (if security-related), `pi-agent` |
| `TESTING` | `qa-tester`, `test-driven-development`, `browser-testing-with-devtools`, `a11y-audit`, `flutter-tester` (if mobile), `verification-before-completion` |
| `AUDITING` | `tob-audit-context`, `tob-static-analysis`, `tob-semgrep`, `cybersec-web-security`, `cybersec-vuln-scanner`, `tob-supply-chain`, `env-secrets-manager`, `tob-second-opinion` |
| `SHIPPING` | `finishing-a-development-branch`, `verification-before-completion`, `requesting-code-review`, `ci-cd-and-automation`, `containerization-and-iac`, `observability-and-monitoring`, `shipping-and-launch`, `performance-optimization` |
| `MAINTAINING` | `systematic-debugging`, `debugging-and-error-recovery`, `receiving-code-review`, `feature-flags-architect`, `verification-before-completion` |
| `UPDATING` | `thinker` (scoped to the delta), then IMPLEMENTING defaults |

High-stakes, irreversible, or security-sensitive work in any phase → add `doubt-driven-development` as an adversarial check.

Confidence levels:
- **HIGH** — one skill clearly owns this given the phase and task. No real alternative. → Pick it, announce it, proceed.
- **MEDIUM** — two or three plausible skills, but one is probably better. → Pick the top one, mention alternatives in one line.
- **LOW** — genuinely ambiguous; depends on what the user actually wants. → Show 2–3 options, ask the user to choose.

---

### Step 4b — The role-staged pipeline (the default output for any code change)

A real bug or feature almost never belongs to a single skill, and the closing quality steps must never be optional. So for **any task that changes code**, decider does not emit a loose bundle — it maps the task onto a **fixed role sequence** and fills each role with skills. The roles never change; only which skills fill them does.

```
PLAN → EXECUTE → [SECURE] → [A11Y] → [PERF] → REVIEW → TEST → VERIFY
```

- **PLAN** — from `thinker` (or inline, if scope is already clear). The plan decider executes against.
- **EXECUTE** — the domain skill(s) that do the actual work, chosen by detected phase + surface signal (table below).
- **SECURE** *(conditional gate)* — `security-and-hardening` (+ `cybersec-web-security` for auditing existing code). **Mandatory** when the surface touches auth / tokens / sessions, untrusted input, money, PII, or irreversible actions.
- **A11Y** *(conditional gate)* — `a11y-audit`. **Mandatory** when the change touches user-facing UI.
- **PERF** *(conditional gate)* — `performance-optimization`. **Mandatory** on perf-sensitive paths, bundle size, or Core Web Vitals surface.
- **REVIEW** *(always)* — `code-review` (use `simplify` for cleanup-only passes).
- **TEST** *(always)* — `test-driven-development` (write/extend tests) and/or `qa-tester` (exercise the feature).
- **VERIFY** *(always)* — `verify` / `run` — actually run the app and observe the change.

High-stakes / irreversible / security-sensitive work in any phase → insert `doubt-driven-development` immediately before REVIEW.

#### The Role Ledger — how the pipeline is enforced

Decider announces a ledger up front and keeps it visible, with a status per role (`✅` done · `⏳` pending · `⏭` skipped-with-reason):

```
ROLE LEDGER
  PLAN     ✅ scope clear from the ticket
  EXECUTE  ⏳ systematic-debugging → frontend-ui-engineering + zustand
  SECURE   ⏭ skipped — no auth/untrusted-input surface touched
  A11Y     ⏳ a11y-audit (UI changed)
  PERF     ⏭ skipped — not a perf-sensitive path
  REVIEW   ⏳ code-review
  TEST     ⏳ test-driven-development → qa-tester
  VERIFY   ⏳ verify
```

Enforcement rules:
- **REVIEW / TEST / VERIFY may never be `⏭ skipped`** for a task that changes code — they are the default closing move, the way launching `Explore` is the default opening move.
- **Conditional gates (SECURE / A11Y / PERF)** are `⏭ skipped` only on a genuine surface mismatch, and the one-line reason must say why.
- A task is **not "done"** until every non-skipped role is `✅`.
- Execute role by role; re-read each skill's `SKILL.md` immediately before its stage (conditions change between steps); update the ledger after each role. Independent legs (e.g. two EXECUTE domains, or supply-chain + secret scan) may run in parallel; dependent legs run as a pipeline.

#### Surface-signal → EXECUTE + mandatory-gate table

Match the strongest signal to pick the EXECUTE skill(s) and which conditional gates become mandatory. **REVIEW + TEST + VERIFY append to every row** — they are not listed because they are never optional.

| Surface signal | EXECUTE (domain) | Mandatory conditional gate(s) |
|---|---|---|
| User-facing UI / layout / component | `frontend-ui-engineering` (+ `frontend-design`) | A11Y |
| Client state / React / Zustand store | `zustand` (+ `frontend-ui-engineering`) | — |
| Animation / motion | `framer-motion` (or `threejs`) | A11Y (reduced-motion) |
| HTTP / data-fetch / auth tokens | `api-communication` | SECURE |
| Auth / session / login bug | `systematic-debugging` → `auth-and-authorization` (+ `cybersec-web-security` to audit) | SECURE |
| Login / sign-up / session / roles / permissions / SSO / MFA (building it) | `auth-and-authorization` | SECURE (mandatory) |
| API contract / endpoint shape | `api-and-interface-design` (contract) → `backend-engineering` (impl) + `api-communication` (client) | SECURE |
| Server endpoint / handler / mutation / background job / queue / cron / webhook receiver | `backend-engineering` | SECURE (untrusted input / money / PII / irreversible) |
| Add AI / LLM / chat / RAG / agent / streaming feature | `ai-app-engineering` (→ `15-rag`/`14-agents` deep technique, `claude-api` model specifics) | SECURE (LLM output-trust) |
| i18n / locale text | `localization` | — |
| Slow page / latency / large bundle / CWV | `performance-optimization` *(is EXECUTE)* → `browser-testing-with-devtools` (measure) | PERF |
| Data / DB / query | `database-schema-designer` | SECURE (if untrusted input) |
| Payment / Stripe / billing | `stripe-integration-expert` | SECURE |
| Reproducible bug | `systematic-debugging` (→ owning domain skill) | per surface above |
| Flaky / CI-only bug | `debugging-and-error-recovery` (→ owning domain skill) | per surface above |
| Build / CI / deploy failure | `debugging-and-error-recovery` → `ci-cd-and-automation` → `containerization-and-iac` (if packaging/runtime) → `shipping-and-launch` | — |
| Containerize / Dockerfile / deploy target / Terraform / IaC / provision infra | `containerization-and-iac` | SECURE (IAM / secrets / public resources) |
| Logging / tracing / metrics / alerts / SLO / prod "flying blind" | `observability-and-monitoring` | — (companion to PERF) |
| Dependency vuln / leaked secret | `tob-supply-chain` + `cybersec-vuln-scanner` + `env-secrets-manager` → `tob-second-opinion` | SECURE |
| Failing test (QA-suite handoff) | entry `qa-automation-engineer` → `systematic-debugging`/`debugging-and-error-recovery` → owning domain skill | per surface above |

These are starting points, not a closed list — compose the same way for any signal: pick the EXECUTE skill(s), add the conditional gates the surface demands, and always append the REVIEW → TEST → VERIFY closing trio.

---

### Step 5 — Is there a skill at all?

If nothing in the catalogue fits — the task is too narrow, too conversational, or genuinely outside skill scope — say so in one sentence, then handle the task directly using Claude's own capabilities. Do not force a skill where none belongs.

---

## Decision rules

### Code change → emit a Role Ledger (the default)
Any task that changes code gets the full pipeline as a ledger — even a one-line fix. The closing trio is never dropped:

```
→ Detected phase: DEBUGGING (cargo edit form not disabling after trips open)
→ Surface: user-facing UI + cargo status logic. ROLE LEDGER:
  PLAN     ✅ scope clear from the ticket
  EXECUTE  ⏳ systematic-debugging → frontend-ui-engineering
  SECURE   ⏭ skipped — no auth/untrusted-input/money surface touched
  A11Y     ⏳ a11y-audit — disabled-state contrast + aria-disabled on the edit action
  PERF     ⏭ skipped — not a perf-sensitive path
  REVIEW   ⏳ code-review
  TEST     ⏳ test-driven-development (status predicate) → qa-tester
  VERIFY   ⏳ verify
  Proceeding with EXECUTE.
```

For a trivial change the ledger is still emitted — domain skill in EXECUTE, conditional gates skipped with reasons, and REVIEW → TEST → VERIFY still run (TEST may collapse into VERIFY when no logic changed; say so in the ledger). It is never empty.

### Parallel legs within a role
When a role has independent legs, run them concurrently and note it in the ledger:

```
  EXECUTE  ⏳ (parallel) tob-static-analysis · tob-supply-chain
```

### Non-code task → simple pick
Research, a doc, a decision, a diagram — no code changes, so no ledger. Route to the single best skill (or 2–3 if it spans domains):

```
→ Detected phase: PLANNING
→ Using `sys-design` + `excalidraw-diagram` for the architecture diagram.
```

### Unsure (ask the user)
When confidence is LOW — two skills would produce meaningfully different outputs:

```
→ Detected phase: UPDATING — new feature on existing project.
→ This could go two ways:
  • `thinker` — if this feature needs full scoping and a spec before building
  • `executing-plans` — if the scope is already clear and you just want to build
  Which fits?
```

Keep the ask tight: two or three options maximum, one line each. No walls of text.

### No skill fits
```
→ No skill in the catalogue covers this directly. Handling it without one.
```
Then proceed with Claude's own capabilities. (This applies to non-code tasks; a code change always carries at least the REVIEW → TEST → VERIFY trio.)

---

## After picking — execute the ledger role by role

Once decider builds the ledger, it does not just invoke skill names — for each role it **reads that skill's `SKILL.md`** and follows its method. Decider is a router, not a summariser. Walk the ledger top to bottom:

1. Re-read the role's skill `SKILL.md` immediately before that stage — not all upfront. Conditions change between steps (a code-review finding can add an EXECUTE leg; a failing TEST sends you back to EXECUTE).
2. Run the role; update its ledger line to `✅` (or back to `⏳` with a note if it surfaced new work).
3. Do not declare the task done until every non-skipped role is `✅` — especially REVIEW → TEST → VERIFY.

---

## Being called by another skill

When thinker (or any other skill) calls decider mid-workflow:
1. Read the context passed to it (what has happened, what is needed, what phase thinker already detected)
2. Apply the same decision logic — but skip Step 0 phase detection if thinker already did it and passed the result
3. Return the **Role Ledger** (for code work) or the simple pick (non-code) to the calling skill — which then announces it and proceeds through the roles

Decider does not restart the whole workflow. It slots in where it was called, and the closing trio (REVIEW → TEST → VERIFY) still applies to any code the caller produces.

---

## Confidence calibration

Decider should be confident most of the time. Asking the user is the right move when the task genuinely has multiple valid interpretations — not as a hedge against being wrong. Over-asking shifts the thinking burden back to the user, which defeats the purpose.

Rule of thumb: if the detected phase + catalogue reading makes one skill clearly stand out, pick it. Reserve asking for cases where two skills would produce meaningfully *different* outputs and the user's preference determines which one they want.

---

## Skill catalogue

See `references/skill-catalogue.md` for the full list of installed skills with descriptions.
Always read it when deciding — do not rely on memory of skill names.
