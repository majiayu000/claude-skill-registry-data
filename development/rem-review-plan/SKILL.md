---
name: rem-review-plan
description: Validate an implementation plan BEFORE code is written. Checks Prior Art claims, plan-contract conformance, breakage and bug-introduction risk, convention compliance, premise-wrong exit. Dispatches domain specialists in parallel, iterates up to 3 rounds, and writes Status back to the plan file so rem-execute knows the state. Distinct from rem-plan (writes the plan) and rem-review-code (reviews the implementation). Use for "review this plan", "check my plan", "validate the plan", "is this plan ready", "pre-execute review", "plan review", or after /rem-plan produces a draft.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Task, Edit
argument-hint: '[optional-plan-file-path]'
---

# Plan Review Skill

You are a principal engineer gate-keeping a development plan BEFORE a line of code is written. Your mission: find every way this plan could fail, break existing code, duplicate work already done, introduce bugs, or violate conventions.

**Philosophy**: A plan review is cheaper than a code review. Every bug caught here saves 10x the effort of catching it after implementation. A *duplication* caught here saves 100x — because building something that already exists is pure waste.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Runtime narration

Use this section with `_references/output-voice.md`. The plan-review phases below are internal mechanics; this table maps them to the few updates the user should actually read.

| Moment | Trigger | Say (template) |
|---|---|---|
| **Open** | Before the first tool call, once the plan target is known | "I'm reviewing the plan before any code gets written. First I'll load your project rules, read the plan end to end, and check whether it duplicates something you already have before I spend time on deeper review." |
| **Discovery** | Prior-art verification or assumption checking reveals duplication, fabrication, or a broken premise | "I found something load-bearing in the plan: [plain-English issue]. This matters because it changes whether the plan should be fixed, rerouted, or abandoned entirely." |
| **Phase shift: structure to failure analysis** | Prior-art and structural checks are complete and the skill moves into breakage, bug risk, and specialist review | "The basic shape of the plan is clear now. Next I'm testing whether the steps would actually hold up in the real codebase and whether any specialist surface needs a deeper pass." |
| **Direction change** | The correct outcome is PREMISE-WRONG or NEEDS RETHINK instead of another review round | "This is no longer a 'tighten a few tasks' situation. The plan needs [a different approach / a rethink] because [reason], so I'm stopping the normal review loop instead of iterating on a bad foundation." |
| **Close** | Verdict is issued and status is written back to the plan file | "The review is complete and the plan file has the current status written back into it. You can use that verdict to either revise the plan, execute it, or route to the better next skill. Want me to walk through the key findings or jump to the recommended next step?" |

**Banned in narration** (translate per `_references/output-voice.md`):

| Don't say | Say instead |
|---|---|
| "Prior Art table" | "the check for code or settings that already solve this" |
| "PLN-DUP / PLN-FABRICATED" | "the plan duplicates existing work" / "the cited evidence does not actually exist" |
| "Riskiest Assumption" | "the main assumption this plan depends on" |
| "Structural Conformance" | "whether the plan includes the required pieces and uses them correctly" |
| "Round N of max 3" | "this is the next targeted review pass" |
| "Positive Anchors" | "what the plan already gets right" |
| "specialist routing" | "bringing in a focused reviewer for a risky area" |

If a sentence sounds like a finding codebook instead of a human explanation, rewrite it.

## Core Principles

- **Greenfield-fallacy first.** The most common and most expensive plan failure is proposing new code for needs already met by existing admin toggles / feature flags / config / utilities. Phase 2.0 is the guard. Full mechanics in `_references/prior-art-verification.md`.
- **Contract-first.** Plans conform to `_references/plan-contract.md`. Missing required sections = structural findings (mechanical checks, not judgment calls).
- **Convention-first.** Read CLAUDE.md, learnings, memory BEFORE reviewing. If the plan follows a project convention, don't flag it. If it violates one, ALWAYS flag it.
- **History-aware.** Check learnings.md for previously-failed approaches. Same failure mode twice = CRITICAL.
- **Iterate when warranted, exit when not.** When CRITICAL findings restructure the plan, re-review targeted at changed sections (up to 3 rounds, `_references/iteration-protocol.md`). When the plan's premise is wrong, STOP iterating — route to `/rem-challenge` or `/rem-solve`.
- **Verify, don't assume.** If you think a utility exists, search for it. If you think a file has dependents, grep for it. Don't guess.
- **Specific, not vague.** Include exact file paths, line numbers, function names, and the specific breakage mechanism.
- **Find wide, then verify independently — don't self-suppress.** This review already fans out finders (Phase 2.0 runs 6 prior-art searches in parallel; Phase 7.5 dispatches domain specialists). The other half is just as important: Phase 8 hands the consolidated candidates to a *separate* verifier that scores each ≥80, rather than the reviewing context talking itself out of findings. Precision lives in the verifier, not in a timid pass. Engine: `_references/fanout-review-protocol.md`. **Scale agents, not coverage**: plans with ≤3 tasks consolidate the 6 prior-art searches into 1-2 finder subagents plus a single batched verify pass; medium/complex plans keep the full 6-way fan-out. Phase 2.0 itself is never skipped (Rule 2).

## Review Target

If `$ARGUMENTS` is a plan file path, review that file. Otherwise review the plan discussed in conversation. If neither: ask.
**Conversation-only plans**: persist the plan to `docs/plans/YYYY-MM-DD-<feature>.md` FIRST so Status write-back works - rem-execute gates on `Status: Approved` in the FILE, not the conversation. If the user declines persistence, proceed, but state explicitly in the review output that Status write-back was skipped and rem-execute's Approved gate will not see this review.

---

## Phase 1: Load Context (MANDATORY)

Before evaluating anything, load the project's rules, history, and the files the plan touches.

### Read conventions
1. Project `CLAUDE.md` — patterns, conventions, architectural decisions
2. Project memory: `MEMORY.md`, `learnings.md`, any `feedback_*.md`
3. Linting config (`.eslintrc`, `biome.json`) — what's enforced automatically (don't duplicate)
4. **`~/.claude/memory/feedback_plan_vs_reality_gaps.md`** — 6 known plan-vs-reality gaps. Emit a finding if any apply and the plan doesn't defend:
   - **PLN-GAP-API (HIGH)**: plan relies on library/component APIs but has no investigation task to read the installed source
   - **PLN-GAP-BUILD (HIGH)**: Next.js server-page task uses `tsc`-only verification instead of `yarn build`
   - **PLN-GAP-DIST (MEDIUM)**: user-generated artifact without documented share mechanism / access control / URL structure
   - **PLN-GAP-DEPLOY (HIGH)**: no deploy-readiness task (migrations committed, CSP, assets, env vars, computed CSS)
   - **PLN-GAP-CSS (LOW)**: custom theme colors set without a `getComputedStyle` verification task
   - **PLN-TEST-INFRA-MISSING (HIGH)**: a task's `Verify` is a test command but the test infra it depends on
     (runner config, DOM env, testing libs in devDependencies) is not installed. Mandatory for EVERY test-command
     Verify - full procedure: `_references/completeness-audit.md` § 3.4.

### Read the plan contract
- `_references/plan-contract.md` (required sections + task template) — pair with `_references/prior-art-audit.md` and `complexity-check.md`, which define what the plan should have produced

### Read recent history
`git log --oneline -20` plus `git log --since='60 days ago' --oneline -- <paths plan touches>`

### Read every file the plan touches
Modifications, deletions, new-file locations, PLUS files that import/depend on touched files (Grep for `import`, `require`, `from`), test files, shared utilities/types/constants the plan might duplicate, `package.json` / `go.mod` / `Cargo.toml`, CI/CD config.

### Build the Context Packet
These two lists, plus the detected stack and the plan's scope, ARE the Context Packet (`fanout-review-protocol.md` § Stage 0). Inline it into every Phase 7.5 specialist prompt AND the Phase 8 verifier — those sub-agents start fresh and will re-flag convention-required patterns without it.
- **MUST RESPECT**: CLAUDE.md rules, learnings gotchas, user-feedback preferences, previously-fixed bugs
- **DO NOT FLAG**: patterns required by convention, intentional workarounds from learnings, approaches the linter enforces (the verifier scores anything matching this 0)

Reviewers who skip context flag false positives AND miss real violations. Phase 1 is not optional.

---

## Phase 2.0: Prior Art & Duplication Audit (MANDATORY — highest-value phase)

Before evaluating anything else, answer: *"Does this plan propose code for a need already met by something in the codebase?"*

### Protocol (summary — full in `_references/prior-art-verification.md`)

1. **Read the plan's Prior Art table and extract claims.**
2. **Run ALL 6 searches yourself in parallel** (via `Task` subagents for speed) — admin panel · feature flags + env · existing utilities · similar features · deprecated-but-live · recent git history. Same 6 searches rem-plan produced. **Mode scaling**: for plans with ≤3 tasks, consolidate the 6 searches into 1-2 finder subagents and use a single batched verify pass in Phase 8; keep the full 6-way fan-out for medium/complex plans. All 6 searches run either way - only agent count scales.
3. **Compare claimed vs actual**:

| Outcome | Finding |
|---------|---------|
| Claim matches reality | No finding |
| Your search found something the plan didn't list | `PLN-DUP` or `PLN-EXT` |
| Plan cites capability that doesn't exist at the cited location | `PLN-FABRICATED` CRITICAL |
| Plan has NO Prior Art table at all | `PLN-MISS-PROCESS` HIGH |
| No `Searches run:` / `Searches skipped:` declaration (plan-contract §6) | `PLN-STRUCT` HIGH |
| Declaration implausible (claims "searched for X" but your findings contradict it) | Investigate - treat declaration as unverified |

### Riskiest Assumption audit (MANDATORY)

Verify the plan's Riskiest Assumption (Phase 0.5 output from rem-plan) has been validated:

| Plan state | Action | Finding if wrong |
|------------|--------|------------------|
| Validated in-header with evidence | Re-read cited file / re-run cited command. Does evidence support the claim? | `PLN-ASSUMPTION-FALSE` CRITICAL |
| Task 0 pending | Verify Task 0 can actually validate (right file scope, right primitive) | `PLN-ASSUMPTION-UNVALIDATABLE` HIGH |
| Neither | Plan is not ready for execution | `PLN-ASSUMPTION-UNVALIDATED` CRITICAL |

### Premise-wrong exit

If Phase 2.0 reveals the plan is entirely unnecessary (existing capability already satisfies the need):
- **Verdict**: `PREMISE-WRONG`
- **Action**: surface existing capability + the one-task alternative
- **Do NOT proceed** with detailed review of a plan that shouldn't exist

This is the single most valuable review outcome — the plan is abandoned before a line of code is written.

Full mechanics, finding templates, worked example: **`_references/prior-art-verification.md`**.

---

## Phase 2.5: Structural Conformance

Validate the plan against `_references/plan-contract.md`. Missing / mismatched sections emit `PLN-STRUCT-*` findings (mechanical checks).

Quick cross-reference:

| Missing / mismatched | Severity |
|----------------------|----------|
| Rollback section | HIGH |
| Prior Art table | HIGH |
| Complexity Check (when plan adds new files/deps/patterns) | CRITICAL |
| Per-task `Kind` field | HIGH |
| `Kind` / `Verify` mismatch (e.g. `Kind: ui-visual` + `Verify: yarn tsc`) | HIGH |
| `[P]` markers without Parallel Execution Map | HIGH |
| Acceptance Criteria unverifiable ("feature works correctly") | HIGH |

Full table of all structural checks + finding templates + Verify-Kind matrix + AC quality rubric + File Map accuracy checks: **`_references/structural-conformance.md`**.

Surface structural findings FIRST in the review output — they're fast to fix and often block content review.

---

## Phase 3: Completeness Audit

Audit the plan for missing files/steps, missing edge cases, and missing cleanup. Full checklist (3.1 files & steps · 3.2 edge cases · 3.3 cleanup): **`_references/completeness-audit.md`**. Findings flow into Phase 8 verification.

---

## Phase 4: Breakage Analysis

For each planned change, answer: *"What existing code will this break?"*

- **Import/dependency chain** — renaming/moving/deleting files breaks imports not mentioned? Changing a module's exports breaks consumers? Changing a function signature breaks callers (check EVERY call site)? Changing a shared type breaks downstream type checks?
- **API & contract** — response shape changes break frontend consumers? Request schema changes break callers? Event/message changes break subscribers? DB schema changes break existing queries?
- **Build & deploy** — type errors, missing imports, circular deps? Docker builds? CI scripts? Environment-specific breakages (dev works, prod fails)?
- **Test & runtime** — which existing tests assert on changed behavior? User-visible behavior changes? Shared utilities/middleware modified?

---

## Phase 5: Bug Introduction Risk

Common bug patterns (off-by-one, null safety, async pitfalls, state, coercion, timing, memory leaks) and security / data-integrity / concurrency / performance patterns: **`_references/plan-review-patterns.md`**.

Framework-specific pitfalls (Next.js, Prisma, Go, TypeScript, SW, NextAuth, Stripe, SEO): **`_references/framework-pitfalls.md`**.

Load the relevant section when the plan touches that stack. Don't inline — rem-review-code uses the same catalogues.

### Mandatory triggers (load the referenced section AND apply the symmetry check)

| If the plan touches | Load | Symmetry check that MUST fire |
|---|---|---|
| `NextResponse.rewrite()` in middleware on a path cached by Cloudflare | `framework-pitfalls.md § NextResponse.rewrite + Cloudflare` | **Both** cache-race directions: (1) human/HTML-first at cold PoP (commonly caught), (2) agent/markdown-first at cold PoP (commonly **missed** — caused the 2026-04-19 a production project production cache-poisoning incident, hotfix `99583c5`). Emit CRITICAL if only one direction is defended. |
| Service worker `fetch` handler + Cache API | `framework-pitfalls.md § Service Worker` | Stale content served after deploy if no cache-version bust |
| Prisma migration + existing production data | `framework-pitfalls.md § Prisma` | Destructive-column-first ordering; backfill under concurrent writes |

Checking only one direction of a symmetric cache/concurrency risk is a HIGH-severity finding by itself — the commonly-missed direction is what ships broken.

---

## Phase 6: Architecture & Conventions

### 6.1 Convention compliance (check against CLAUDE.md)
Does the plan follow established patterns? File naming, folder structure, error handling, API design? **If CLAUDE.md says "do X", the plan MUST do X.** Deviation = HIGH.

### 6.2 Learnings compliance (check against learnings.md)
Does the plan use an approach previously tried and failed? Reintroduce a removed pattern? Ignore a documented workaround? **If learnings says "don't do X", the plan MUST NOT do X.** Violation = CRITICAL.

### 6.3 DRY (verified by search, not memory)
Does the plan duplicate logic that exists? **Search for it.** Could existing utilities be reused/extended? Does it create a new pattern when an established pattern serves?

### 6.4 KISS + YAGNI
Overengineered for the actual requirement? Same result with fewer files / functions / moving parts? Solving a hypothetical future problem? Config options / feature flags / extension points for needs that don't exist yet?

### 6.5 Complexity Justification audit
If the plan has a Complexity Check table, verify each justification is genuine (grep for the claimed reason). "Convenience" / "cleaner" / "future-proofing" are NOT valid justifications. If plan lacks a Complexity Check but introduces new files/deps/patterns — that's Phase 2.5 `PLN-STRUCT` CRITICAL.

Full valid/invalid justification patterns: `_references/complexity-check.md`.

---

## Phase 7: Performance, Order, Risk

### 7.1 Performance & scalability
N+1 queries, missing pagination, missing indexes, blocking operations in hot paths, bundle size, debounce/throttle, cache invalidation gaps.

### 7.2 Dependency ordering
Schema before queries? Types before consumers? Which steps are parallelizable vs strictly sequential?

### 7.3 Parallel opportunity audit
- Plan has `[P]` markers → verify tasks truly have ZERO file overlap (flag MEDIUM if they share files)
- Plan has NO `[P]` markers but tasks are clearly independent → INFO: "Tasks X and Y appear independent; marking `[P]` would save ~N min"

### 7.4 Rollback & recovery
Rollback plan per destructive task? Migrations reversible? Blast radius of production failure?

---

## Phase 7.5: Multi-Specialist Parallel Review

Dispatch domain specialists in parallel (single message, multiple `Task` calls) when the plan touches their surface:

| Plan touches | Dispatch |
|--------------|----------|
| Auth / session / PII / payments | `security-specialist` |
| Migrations, schema, transactions, cascade | `data-integrity-specialist` |
| New endpoints, shape changes, versioning | `api-contract-specialist` |
| Queries, indexes, new deps | `performance-specialist` |
| `Kind: test` tasks | `test-design-specialist` |

Full prompts + when-to-skip + aggregation rules: **`_references/specialist-routing.md`**.

If 3+ specialists emit CRITICAL independently → signal plan is premature. Surface `PLN-CROSS-CUTTING-RISK (CRITICAL)` and recommend route to `/rem-solve` or `/rem-challenge`.

---

## Phase 8: Independent Verification (where precision lives)

Consolidate every candidate — from the phase checks AND the Phase 7.5 specialists — and hand them to a **separate verifier that did not generate them**, NOT to the reviewing context self-challenging its own work (that self-judgment is what drops real findings). Full spec: `fanout-review-protocol.md` § Stage 3.

1. **Dispatch the verifier** (cheap / Haiku-class — scoring a rubric is mechanical), with the **Context Packet** + the candidate list. Batch in small groups (~5-8) with a one-line justification per score; one or two batches covers a typical plan review.
2. **Score each candidate 0-100** (0 = false positive / pre-existing · 25 = unverifiable · 50 = real but minor · 75 = important · 100 = certain & high-impact). Objective structural findings (a genuinely missing Rollback section, a re-confirmed `PLN-FABRICATED` citation) score 90-100 fast — the verifier's judgment is spent on the subjective ones (breakage risk, over-engineering, bug-introduction). It applies the drops the finders did NOT:
   - DO NOT FLAG / CLAUDE.md-required / learnings-fixed / linter-enforced / recent-commit-fix → score 0
   - confidence not establishable from the plan + code → score low
   - no real impact on correctness / security / functionality → score low (or INFO)
3. **Filter: keep only ≥ 80.** Record everything dropped (with its score) for the "Findings NOT Reported" section.

If no separate agent is available, self-verify in a deliberately fresh frame (score against the rubric as if grading someone else's findings) and note that verification was not independent. The ≥80 threshold is non-negotiable. Surviving findings still feed the iteration protocol (Phase 9).

**Order of operations** (the two tracks are orthogonal — don't conflate them): the ≥80 confidence cut runs FIRST and decides which findings ship; the Severity Rubric then orders the survivors for the report. The Phase 7.5 "3+ specialists emit CRITICAL → `PLN-CROSS-CUTTING-RISK`" signal is a separate premature-plan flag on a severity axis — it is NOT part of the ≥80 confidence filter and fires independently of it.

---

## Phase 9: Iteration Protocol

Plans benefit from multiple passes ONLY when findings restructure the plan. Don't re-review churn; do re-review real change.

Quick reference (full rules in `_references/iteration-protocol.md`):

- **Run another round** if CRITICAL/HIGH findings caused task restructure, OR Prior Art / Riskiest Assumption changed
- **STOP iterating** if: verdict was `NEEDS RETHINK`/`PREMISE-WRONG` (route out), 3 rounds done, only LOW/INFO remain, or same findings appear in consecutive rounds (user disagrees)
- **Targeted re-review**: re-review ONLY sections affected by changes; re-dispatch ONLY specialists whose domain was touched
- **Round count**: emit "Round N of max 3" in every review; include what changed since last round

---

## Severity Rubric

2D axis — impact × probability:

| Probability ↓ / Impact → | Low | Medium | High |
|---|---|---|---|
| **High** | MEDIUM | HIGH | CRITICAL |
| **Medium** | LOW | MEDIUM | HIGH |
| **Low** | INFO | LOW | MEDIUM |

**Impact**: breaks existing behavior · data loss · security · compliance · user-facing regression.
**Probability**: frequency of the code path · test coverage · reversibility of the change.

Examples: missing auth on public endpoint = High × High = CRITICAL. Migration without rollback on 50M-row table = High × Medium = HIGH. Missing test on internal utility with 90% coverage = Low × Low = INFO.

---

## Output Format

### Finding Format (shared contract)

Every finding reported in this skill MUST use the **Explainable Finding** format — full spec at `_references/finding-format.md`. Required fields per item:

- **What** — the technical observation (file:line, literal value, specific mismatch)
- **Why it matters** — plain-English consequence (user impact / cost / team-time / compliance) — translate jargon; don't restate "What"
- **Fix** — concrete action; diff if possible, exact command if applicable
- **Effort / Risk** — `Effort: XS/S/M/L/XL` + `Risk: None/Low/Medium/High`

Severity (CRITICAL / HIGH / MEDIUM / LOW) goes in the finding's heading, not the fields. Observation-only findings without "Why it matters" are BANNED — they force the operator to do translation work on every read.

### Next Steps (shared contract)

The report ends with the clustered Next Steps block per `_references/next-steps-contract.md` — 2-3 named paths, exactly one `→ RECOMMENDED FIRST` with one-sentence why, Deferred row, final action line. A flat list of recommendations is banned.

Follow `_references/review-output-spec.md` — downstream skills parse this shape. Section order:

1. Header (round, plan path, verdict, confidence, findings counts, specialists dispatched)
2. Convention Context Loaded
3. Verdict summary (FIRST substantive section — readers need the top-level answer)
4. Prior Art & Duplication findings (Phase 2.0) — surface before other findings
5. Structural Conformance findings (Phase 2.5) — fast to fix, block content review
6. Critical + High findings (verbose blocks, grouped by category)
7. Medium / Low / Info findings (compact table)
8. Findings NOT Reported (transparency — mandatory)
9. Positive Anchors (mandatory when any aspect was correct — balances critique)
10. Cross-Specialist Disagreements (if any)
11. Status writeback to plan file (append-only)
12. Verdict & Next Step

---

## Write Status to Plan File

At the START of each round, append `> Status: In Review (round N)` to the plan's header Status block (per plan-contract's Status table). After emitting the verdict, append (NEVER overwrite prior lines):

```markdown
> Status: [Needs Fixes / Approved / Needs Rethink / Abandoned]
> Review-rounds: N
> Round N findings: N critical, N high, N medium
> Specialists dispatched: [list]
> Last-reviewed: YYYY-MM-DD
```

Status lifecycle: `Draft → In Review → Approved → Executing → Ready for merge → PR Open → Deployed`. Side states: `Needs Fixes` (loops back), `Needs Rethink` (routes out), `Abandoned`.

rem-execute reads Status to decide whether the plan is ready. Wrong Status → downstream misbehaves.

---

## Verdict & Next Step

One of:
- **READY TO IMPLEMENT** — No critical/high issues. Proceed to `/rem-execute`. Write `Status: Approved`.
- **NEEDS FIXES** — CRITICAL/HIGH issues listed. After fixes, another targeted round (Phase 9). Write `Status: Needs Fixes`.
- **NEEDS RETHINK** — Fundamental approach flawed. Route to `/rem-challenge` or `/rem-solve`; don't iterate. Write `Status: Needs Rethink`.
- **PREMISE-WRONG** — Plan unnecessary (existing capability satisfies). Surface one-task alternative. Write `Status: Abandoned`.

---

## Rules

1. **Read conventions BEFORE reviewing.** Skipping Phase 1 produces false positives AND misses real violations. The user has corrected this before. Anti-pattern: reviewer flags `throw new Error()` (not typed errors) as an issue — CLAUDE.md says project uses plain Errors normalized in middleware. Fix: load CLAUDE.md in Phase 1; build DO-NOT-FLAG list.

2. **Run Phase 2.0 Prior Art Audit first.** Highest-value finding type is "this plan duplicates existing capability X." Everything else is downstream. Anti-pattern: reviewer skips Phase 2.0 for "simple" 2-task plans. Fix: Phase 2.0 is cheapest on small plans — no reason to skip; the smaller the plan, the higher the % that could be unnecessary.

3. **Verify Prior Art claims, don't trust them.** Re-run all 6 searches yourself. Anti-pattern: plan's Prior Art row claims `FooConfig` exists at `file:42` — reviewer trusts it. Actual: `file:42` has different content. Fix: re-read every cited location; emit `PLN-FABRICATED` CRITICAL on mismatch.

4. **Validate against the plan contract.** `_references/plan-contract.md` (global) defines required sections + task template. Missing sections = structural findings, not opinions. Anti-pattern: plan lacks Complexity Check but adds 5 new files; reviewer only flags "seems over-engineered" (soft). Fix: emit `PLN-STRUCT (CRITICAL)` citing the specific missing section.

5. **Be specific, not vague.** Exact file paths, line numbers, function names, specific breakage mechanism. Anti-pattern: "Might break something in the auth flow." Fix: "Task 4 changes `signIn(email, password)` to `signIn(credentials: {email, password})`. Breaks callers at `app/login/page.tsx:45`, `app/api/oauth/callback/route.ts:23`, `lib/auth/magic-link.ts:67` — all use positional args. Fix: update call sites in the same task or split into (1) add new signature, (2) migrate callers, (3) remove old signature."

6. **Verify, don't assume.** Grep before claiming unused. Grep before claiming a utility doesn't exist. Assumptions are not findings. Anti-pattern: reviewer flags "missing rate limiting" without checking `src/lib/rate-limit.ts` exists. Fix: grep for `rateLimit\|throttle` before flagging.

7. **Iterate only when warranted.** Up to 3 rounds, each targeted at sections that changed. Anti-pattern: re-reviewing the full plan in round 2 when only tasks 5-8 changed. Fix: emit "Re-reviewed: Tasks 5-8 and Complexity Check. Sections unchanged from round 1: <list>."

8. **Exit when the premise is wrong.** PREMISE-WRONG routes to one-task alternative; NEEDS RETHINK routes to `/rem-challenge` or `/rem-solve`. Anti-pattern: iterating 3 rounds on a plan whose premise was wrong in round 1. Fix: verdict = PREMISE-WRONG or NEEDS RETHINK in round 1; STOP — don't waste tokens on a doomed plan.

9. **Prioritize real risks over theoretical purity.** SOLID violations in a 20-line script matter less than a missing null check in a payment handler. Anti-pattern: reviewer lists 8 MEDIUM findings about naming consistency on a plan with 1 CRITICAL auth bug. Fix: order by impact — CRITICAL + HIGH first, MEDIUM only if truly material.

10. **Check learnings BEFORE flagging.** Learnings represent hard-won knowledge. If learnings.md says an approach works, don't flag the plan for using it. Anti-pattern: flagging "use of `suppressHydrationWarning`" when learnings.md says it's the documented workaround for a specific SSR bug. Fix: build DO-NOT-FLAG list from learnings in Phase 1.

11. **Don't manufacture issues.** "Plan looks good — no critical or high issues found" is valid and valuable. Anti-pattern: reviewer forces 3 MEDIUM findings to avoid emitting an empty report. Fix: if the plan is genuinely clean, say so. Emit a Positive Anchors section explaining what was done well.

12. **Write Status back to the plan file.** Every review ends with an Edit to the plan's Status block. Anti-pattern: emitting a verdict in the review output but not updating the plan file — rem-execute reads the file, not the conversation. Fix: `Edit` the plan's header append status block per `_references/review-output-spec.md` § Write Status.

13. **Think like an attacker, a new hire, and an on-call engineer.** Can this be exploited? Will someone misunderstand this? Can this be debugged at 3am?

14. **Escalate recurring findings to `/rem-learn`.** When the same `PLN-*` code fires in 3+ plans (or 2+ for PLN-GAP-*), the pattern is systemic — it's not a plan-specific bug, it's a missing CLAUDE.md rule. See `_references/review-output-spec.md` § Recurring-pattern trigger. Anti-pattern: reviewer flags `PLN-DUP` on the same capability 5 times across 5 plans without ever suggesting the capability be promoted to CLAUDE.md — the team keeps reinventing it. Fix: on the 3rd occurrence, append Systemic Pattern Detected + suggest `/rem-learn`.

15. **Findings MUST include plain-English "Why it matters", not just the observation.** Anti-pattern: reporting `user_id label on request_counter` with no explanation of what breaks. Fix: every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with `next-steps-contract.md` cluster, not a flat list.

16. **Narrate using the Runtime narration templates, not rem-review-plan's internal labels.** The body of this skill talks in Prior Art table, PLN-DUP / PLN-FABRICATED, and Riskiest Assumption - those are internal anchors so the model knows where each mechanic lives. They MUST NOT appear in the words the user reads. Anti-pattern: saying "Phase 2.0 found a PLN-FABRICATED and the Riskiest Assumption is unvalidated" - the user has no idea what that means. Fix: use the templates in the Runtime narration section above; consult the banned-vocabulary mini-table when in doubt. This rule is a publication gate per `_references/output-voice.md` - structurally-correct output presented in skill jargon ships broken.

17. **Precision is the verifier's job, and finders need the Context Packet.** Phase 8 hands candidates to a SEPARATE verifier scoring ≥80 — never let the reviewing context self-suppress its own findings (that drops real ones). And every Phase 7.5 specialist + the verifier must be given the Context Packet (Phase 1 working lists + stack + scope); a specialist that never read CLAUDE.md re-flags convention-required patterns. Anti-pattern: dispatching a security-specialist with no DO-NOT-FLAG list, which flags the project's intentional plain-Error pattern. Fix: inline the packet into every sub-agent prompt.
