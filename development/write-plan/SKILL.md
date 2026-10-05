---
name: write-plan
description: >-
  Write a technical implementation plan to thoughts/plans/ before coding starts (separate from the
  harness's plan mode). Use when someone says "create a plan", "plan this", "plan this ticket",
  "how should we implement this", "technical design", "architect this", "plan the migration",
  "refactor plan", or when a shape or groomed ticket needs phases, layers, and agent-runnable checks.
effort: high
---

# Write Plan

Turn a shape, ticket, or technical challenge into a plan that any developer or agent can execute with `/dev-skills:execute-plan` — and that a human can read, understand, and defend.

## Workflow

Every plan follows the same arc: **research → validate → write → present**.

1. **Research** the codebase until grounded — never plan from assumptions (see Process).
2. **Write** the plan to `thoughts/plans/YYYY-MM-DD-descriptive-name.md`, using today's date from context.
3. **Present** it for approval, closing with the ★ Plan View block.

This skill is independent of any harness plan mode — always write the `thoughts/plans/` file. The gate is the user's approval of that file. Approval hands `execute-plan` a contract: it runs every phase to DONE or stops BLOCKED, without check-ins — so the plan must contain everything needed to get there unattended.

## Design Philosophy

Before writing plans, read [references/software-design-philosophy.md](references/software-design-philosophy.md). Apply it to module boundaries, interfaces, and decomposition. Key checks: deep modules, information hiding, define errors out of existence, design it twice.

## Rollout & Rollback

Every plan must specify how the change ships and to whom. Read [references/rollout-primitives.md](references/rollout-primitives.md) before writing the plan and walk the three decision questions:

1. **Contract test:** is a shared contract changing? (schema, public API, multi-consumer interface) → plan expand-contract on the affected surface.
2. **Launch-strategy test:** who should see this, and when? Cohort, tier, geo, timing, %-rollout, A/B, dogfooding → flag (launch flag).
3. **Kill-switch test:** if this went bad in prod, what would I do? Flip a flag → flag (risk flag). Revert + redeploy is fine → no risk flag.

Flags serve two purposes — **launch control** (who/when) and **reversibility** (turn-off). Either test saying "flag" justifies one. Same flag covers both if both apply.

Default is **no flag, no expand-contract**. Pick the lightest mechanism(s) that produce the launch control AND reversibility actually needed. One flag per feature (at the user-visible boundary), never one flag per phase. Bug fixes never get flags. The flag system itself is discovered from `.tap/architecture.md` or by grepping known imports — do not invent one.

## Layers & Dev Harness

Every plan states how the work decomposes and how an implementer proves each part without walking the full user flow. Read [references/dev-harness.md](references/dev-harness.md), then:

- **Map the layers** — outbound I/O (3rd-party clients), State, Function, inbound I/O (endpoints, jobs), UI (I/O to a human). Order phases so each layer is proven at its own boundary before anything composes on it: client before endpoint, endpoint before UI.
- **Every check is agent-callable** — a command, test, curl, or MCP call with observable output. "Manually verify" is not a check. Human-only steps (login, OAuth, 2FA, sandbox keys) get a bypass in the plan or go under **Pre-flight blockers** so they're cleared before implementation, not discovered mid-run.
- **Name the loop ladder** (L1 fixture-fed logic → L2 direct trigger → L3 seeded/direct UI → L4 full flow). The riskiest logic gets the fastest loop; L4 is never the only loop.
- **Harness artifacts are phase-1 deliverables** — fixtures, goldens/evals, seed & reprocess commands — built before the logic they exercise is tuned, and exercising the same code path production uses.
- **Inspection surfaces** when outputs are judged rather than diffed, or land in data models whose UI ships later: a disposable out-of-app viewer — see the reference.

## Whiteboard Defense (customer-facing work)

If the shape's `Stakes:` is customer-facing — or there's no `Stakes:` line (bug-fix shapes) or no shape at all, and the change reaches customers — the plan carries a `## Whiteboard Defense` section: what the developer needs to explain the system at a whiteboard and defend it to their team — without line-level knowledge. Keep it ≤ 20 lines, in plain words (the `/dev-skills:explain` register: simple, direct, no jargon without a gloss):

- **Sketch** — ASCII of the layer map: data flowing I/O → Function → State.
- **Why X, not Y** — the 2–3 decisions that matter, each with the discarded option.
- **Bad actor** — how a malicious or misbehaving actor abuses this (authz, tenancy, input, replay, rate) and what stops them.
- **Data** — the key structures/tables and why that shape.
- **Where it fails** — failure modes, what the user sees, how we'd notice.

If you can't fill a line, that's a planning gap — resolve it rather than leaving it blank. PoC and internal-only work skip this section.

## Principles

- **Research first** — understand the codebase before proposing solutions
- **Layers first** — prove each layer at its boundary before building on it
- **Harness-first** — the fastest iteration loop is a deliverable, not an afterthought
- **Decisions, not transcripts of code** — the plan pins down contracts (signatures, schemas, API shapes, key types), decisions, layers, and checks. Include code only where its exact form *is* the decision: a migration, a public type, a subtle algorithm. The implementer writes the rest; full-code plans go stale on first contact and bury the decisions a reviewer needs to see
- **Be specific** — real file paths, function names, commands, expected outputs
- **Be skeptical** — question assumptions, identify risks early
- **Decide, don't ask** — every open question gets a recommended resolution with reasoning
- **Follow patterns** — match existing codebase conventions
- **Agent-agnostic** — any implementer can execute it

## Process

### 1. Research (mandatory — depth scales to blast radius)

Never plan from assumptions. Cover all four goals; a one-file change gets a quick pass, a cross-package feature gets the full sweep.

- **LOCATE** — where the relevant files live (routes, business logic, components, schema, tests).
- **PATTERNS** — how similar things are already done here: naming, file organization, error handling.
- **ANALYZE** — trace the relevant path end-to-end (entry point → data/API), mapping key functions and their inputs/outputs.
- **VALIDATE** — confirm the premises the plan rests on. When it depends on runtime or data facts ("X drives Y", "this field is always set"), check the live data/behavior — don't infer from static code.

Before narrowing in, look broadly for context the request didn't name: related docs in `thoughts/shapes/`, `thoughts/plans/`, `thoughts/research/`, `.tap/architecture.md`, `.tap/product.md`, open issues and PRs on the topic.

If sub-agents are available, fan the four goals out in parallel. The requirement is the outcomes, not the mechanism.

Also capture the stack (package manager, build tool, language/strictness, runtime, framework, database/ORM, test runner) and the existing implementations to follow.

### 2. Present Options (if multiple approaches exist)

- Option A: [approach] — pros/cons
- Option B: [approach] — pros/cons
- Recommendation: [which and why]

Put the options in Implementation Approach with the recommendation and write the full plan. Stop for alignment first only if the options differ in user-visible scope or acceptance criteria.

### 3. Write the Plan

Follow the output format below.

## Output Format

```markdown
# [Title] - Implementation Plan

## Overview
[1-2 sentences: what we're building and why]

## Acceptance Criteria
[Link to the shape doc: `thoughts/shapes/YYYY-MM-DD-name.md`]
[The shape doc is canonical. Do NOT restate or reinterpret criteria here — qa-test consumes them from the shape doc verbatim.]
[No shape (tiny/unshaped work)? List criteria here using shaping-work's rules: independently testable, observable behavior, no vague language.]

## Current State
[What exists now, what's missing, relevant code locations]

## Desired End State
[What works when done, and the commands that show it]

## Out of Scope
[What we're NOT doing]

## Rollout & Rollback

**Reversibility mechanism:** [expand-contract / flag / both / neither — walk the decision tree in [references/rollout-primitives.md](references/rollout-primitives.md)]

**If expand-contract:** surface [schema / API / interface]; phases expand → migrate → contract, each its own plan phase; why (no) flag on top.

**If flag:** name (one per feature) · purpose (launch control / reversibility / both) · flag system (from `.tap/architecture.md` or grep; "none detected" → flag infra is a prerequisite, don't invent one) · gate location (user-perceived entrypoint) · lifecycle (short-lived + removal task / long-lived) · rollback lever: flag flip.

**If neither:** direct deploy. Blast radius: [scope]. Rollback: revert + redeploy.

## Layers & Dev Harness

**Layer map:**
| Part | Layer | Proven by (agent-runnable) | Phase |
|---|---|---|---|
| [e.g. Stripe client] | outbound I/O | [`pnpm vitest client.test.ts` against recorded fixtures] | 1 |
| [e.g. invoices table] | State | [`pnpm db:migrate && pnpm vitest invoices.repo.test.ts`] | 1 |
| [e.g. syncInvoices use-case] | Function | [...] | 2 |
| [e.g. GET /api/invoices] | inbound I/O | [`curl -s localhost:3000/api/invoices -H "$DEV_AUTH" \| jq length`] | 3 |
| [e.g. Billing page] | UI | [`/dev-skills:qa-test` on /billing with seeded account] | 4 |

**Fastest loop:** [one command, or "trivial: direct route + seeded data"]
**Fixtures:** [which real-world inputs, where | "N/A"]
**Direct trigger:** [re-run the workflow/job/endpoint against stored state | "N/A"]
**Reachability:** [open the surface without prerequisites — route + seed command]
**Inspection:** [viewer for judged-not-diffed outputs | "N/A"]
**Pre-flight blockers:** [human-only steps the agent can't do + how they're cleared before implementation (seeded token, test keys in `.env.local`); if there's a UI layer, browser MCP reachable | "none"]

## Whiteboard Defense
[Customer-facing only — see the section above. ≤ 20 lines, plain words.]

## Implementation Approach
[Strategy and the reasoning behind it]

---

## Phase 1: [Layer or slice name]

**Layer:** [which layer(s) this phase builds]  ·  **Proves:** [what is true once the checks pass]

### Changes
- `path/to/file.ext` — [what changes and why]
- `path/to/new-file.ext` (new) — [responsibility]; contract:
  ```ts
  export function syncInvoices(customerId: CustomerId): Promise<SyncResult>
  ```

### Phase Checks
- [ ] `[agent-runnable command]` → [expected output]
- [ ] `[agent-runnable command]` → [expected output]

*Phase checks are technical gates for this layer. Acceptance criteria are verified at the end against the shape doc.*

---

## Phase 2: [Layer or slice name]
[Same structure]

---

## Final Verification
- [ ] `[full test suite]`, `[typecheck]`, `[lint]` → clean
- [ ] Acceptance criteria: [how each is verified — `/dev-skills:qa-test` for UI behavior, command/query for the rest]

## Related Docs
- `thoughts/shapes/YYYY-MM-DD-name.md` — [shape]
- `thoughts/research/YYYY-MM-DD-name.md` — [what it covers]

## Open Questions

Each has a recommended resolution; execution proceeds with it unless the user steers otherwise.

- **[Question]**
  Recommend: [option] — [why]
  Discarded: [option] ([why not])
```

## Plan View — signature block (always close with this)

After writing the plan to file, close your response with a **★ Plan View** block: a short summary, then an ASCII map of the plan's structure. This is the default — the user shouldn't have to ask for an ASCII explanation. It's the at-a-glance view; the file holds the detail.

The ASCII is a structural **map**, not a re-render of the plan body — show phases in sequence, the layer each proves, the files each touches, dependencies between phases, and the verification gate per phase. Nothing else.

```
★ Plan View ─────────────────────────────────────
- Building: [what, one line]
- Approach: [the strategy, one line]
- Blast radius: [N files / surfaces]  ·  Rollout: [flag / expand-contract / direct]
- Iterate via: [fastest loop, one command]
- Pre-flight: [human-only steps to clear before execute-plan | none]
- Risk: [the thing most likely to bite]
──────────────────────────────────────────────────

Plan: [title]
│
├─ Phase 1: [name]            [layer: outbound I/O]
│    ├─ path/to/file.ext
│    └─ ✓ [phase check]
├─ Phase 2: [name]            [layer: Function]  (depends on P1)
│    ├─ path/to/other.ext
│    └─ ✓ [check]
└─ Phase 3: [name]            [layer: UI]
     └─ ✓ [check]

Full plan → thoughts/plans/YYYY-MM-DD-name.md
```

Rules:
- Block leads the closing response — consistent with `product-thinker` (★ Product View), `shaping-work` (★ Shaped View), `strategic-thinker` (★ Strategic View)
- Summary bullets are assertions, not hedges
- ASCII shows structure only — never duplicate the markdown body

## Phase Guidelines

- **One layer (or one thin slice across layers) per phase**, in dependency order — a phase's checks only touch layers already proven.
- Earlier phases don't break existing functionality.
- Each phase ends in green, agent-runnable checks — `execute-plan` moves straight on to the next phase.
- Typically 1–3 files per phase; large enough to be meaningful, small enough to prove quickly.

## What Makes a Good Plan

**Good:**
- Real file paths; contracts (signatures, schemas, request/response shapes) spelled out
- Every check is a command with an expected output
- Human-only steps surfaced as pre-flight blockers
- Decisions carry the discarded alternative

**Bad:**
- "Update the relevant components", "add appropriate error handling"
- "Manually verify", "test thoroughly"
- Pages of implementation code that restate what the implementer will write anyway
- A UI phase whose check depends on an API no earlier phase proved

## Example (abbreviated)

**Input:** shape `thoughts/shapes/2026-03-02-billing-invoices.md` — show a customer's Stripe invoices on the Billing page.

```markdown
# Billing invoices - Implementation Plan

## Layers & Dev Harness
| Part | Layer | Proven by | Phase |
|---|---|---|---|
| `StripeInvoices` client | outbound I/O | `pnpm vitest stripe-invoices.test.ts` (recorded fixtures in `fixtures/stripe/`) | 1 |
| `invoices` table | State | `pnpm db:migrate && pnpm vitest invoices.repo.test.ts` | 1 |
| `syncInvoices` | Function | `pnpm vitest sync-invoices.test.ts` | 2 |
| `GET /api/invoices` | inbound I/O | `curl -s localhost:3000/api/invoices -H "$DEV_AUTH" \| jq length` → 3 | 3 |
| Billing page | UI | `/dev-skills:qa-test` on `/billing` (seed: `pnpm seed:billing`) | 4 |

**Pre-flight blockers:** Stripe test key in `.env.local` (`STRIPE_SECRET_KEY=sk_test_…`) — needed once to record fixtures.

## Whiteboard Defense
Stripe ──► StripeInvoices ──► syncInvoices ──► invoices table ──► GET /api/invoices ──► Billing page
- Why cache in our DB, not call Stripe per page view: Stripe rate limits + page latency. Discarded: live fetch.
- Bad actor: another tenant's invoices via `?customerId=` → endpoint ignores params, derives customer from session.
- Data: one row per invoice, keyed by Stripe id — upsert makes re-sync idempotent.
- Where it fails: Stripe down → page shows last-synced data + "updated N min ago"; sync errors alert via existing job monitor.

## Phase 1: Stripe client + invoices table
**Layer:** outbound I/O, State  ·  **Proves:** we can fetch and store invoices without the app running
### Changes
- `src/billing/stripe-invoices.ts` (new) — `listInvoices(customerId: StripeCustomerId): Promise<Invoice[]>`; pages through Stripe's cursor
- `src/db/schema/invoices.ts` (new) — `invoices(id pk = stripe id, customer_id, amount_cents, status, issued_at)`
### Phase Checks
- [ ] `pnpm vitest stripe-invoices.test.ts` → pass (pagination + error mapping on fixtures)
- [ ] `pnpm db:migrate && pnpm vitest invoices.repo.test.ts` → pass
```

## Handoffs

- After approval → `/dev-skills:execute-plan` runs it to DONE or BLOCKED.
- Customer-facing, and the developer wants to be able to explain it → `/dev-skills:explain thoughts/plans/<file>.md`.
- The plan in `thoughts/plans/` is the source of truth during execution.
- Offer to publish for team review: `/tap-skills:render-doc` then `/tap-skills:dossier-publish` (md stays source of truth; republish after edits).
