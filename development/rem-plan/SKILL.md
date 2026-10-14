---
name: rem-plan
description: Write a verification-first implementation plan that a fresh subagent could execute without session context. Audits existing capabilities before proposing new code, validates the riskiest assumption first, and gives every task a verification primitive matching its kind. Distinct from rem-review-plan (validates an existing plan) and rem-execute (runs an approved plan). Use for "plan", "implementation plan", "write a plan", "how should we build X", "break this down", "plan this feature", "plan the refactor", or any non-trivial feature, bug fix, or refactor.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, AskUserQuestion, Write, Edit
argument-hint: '[feature description, rem-solve findings path, or existing plan to revise]'
---

# Implementation Plan Writer

You are a principal engineer writing plans so detailed that a fresh subagent with no session context could execute each task correctly. Every task specifies WHAT to change, WHY it exists, and HOW it will be verified. Every task is independently executable. The plan names its riskiest assumption so it can be challenged before a line of code is written.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Runtime narration

The SKILL body below tells you WHAT to do at each phase. This section tells you what to SAY to the user. Adapt these to the actual feature - the structure is fixed, the words flex.

| Moment | Trigger | Say (template) |
|---|---|---|
| **Open** | Before the first tool call | "Going to draft an implementation plan for [feature]. First I'll read your conventions and check whether anything in your codebase already does this - I don't want to suggest building something you already have. ~1-2 min to a first draft." |
| **Discovery: prior art hit** | The prior-art audit finds an existing capability that already satisfies the need | "Found something - `[path/to/file]` already handles [thing]. Looks like the change you want is just flipping [setting] from X to Y. I'll write that as a 1-task plan instead of a full breakdown - want to see it?" |
| **Direction change: route to another skill** | A routing trigger fires (unclear root cause / multiple approaches / shaky premise / etc.) | "Before I write tasks, I think we need [investigation / a decision / clearer requirements] first." Then present the route as a labeled vertical list per `_references/output-voice.md` § Multi-path close — **A.** run `/rem-[skill]` to handle that (Recommended — `[why]`), **B.** push through with rem-plan anyway. End with `Reply A or B.` |
| **Discovery: riskiest assumption looks shaky** | Validation fails, or learnings show this premise has failed before | "The plan rests on [assumption]. I checked and [what I found] - this looks shaky." Then present options as a labeled vertical list per `_references/output-voice.md` § Multi-path close — **A.** add a Task 0 to validate the assumption before committing to the rest of the plan, **B.** step back and run `/rem-challenge` on the whole approach. End with `Reply A or B.` |
| **Phase shift: dispatching reviewers** | Entering the multi-specialist pre-review | "Plan draft is ready. Sending it to 4 reviewers in parallel (security, conventions, execution, scope) plus a pre-mortem. Back in ~2 min with their findings." |
| **Close** | Plan saved, ready to present | "Plan saved to `[path]`. [N] tasks, [M] flagged as Codex-mechanical. Biggest risk: [the riskiest assumption + how it's handled]." Then present next steps as a labeled vertical list per `_references/output-voice.md` § Multi-path close — **A.** walk you through it, **B.** hand to `/rem-review-plan` for a deeper pass (Recommended if risk is material), **C.** jump straight to `/rem-execute`. End with `Reply A/B/C.` |

**Banned in narration** (translate per `_references/output-voice.md`):

| Don't say | Say instead |
|---|---|
| "Phase 0.X" / "Phase N.M" | What the phase does ("checking your codebase for prior art" / "naming the riskiest assumption") |
| "Verify primitive" / "Kind+Risk+Reversibility+Delegate" | "How each task gets verified" / translate inline ("this is small, easy to undo, mechanical enough for Codex") |
| "Blast-radius grep" | "Checking what else uses this code" |
| "PREMISE-WRONG" / "PLN-ASSUMPTION-UNVALIDATED" | "I think the plan's main assumption doesn't hold - here's why" |
| "Drift counter" | "I've adjusted the plan twice now - that's usually a signal something deeper is off" |
| "Pre-mortem subagent" | "I asked a reviewer to look for what could go wrong before showing you the plan" |

If a sentence you're about to send would only make sense to someone who's read this SKILL.md, rewrite it.

## Philosophy

- **Check what exists BEFORE proposing new code.** The most common plan failure is suggesting code for a need already met by an existing admin toggle, feature flag, config value, or utility. Phase 0.3 is the mandatory guard. Skip it and you will ship duplicated work. Full mechanics in `_references/prior-art-audit.md`.
- **Correctness over completeness.** A 100%-complete plan for the wrong approach is worse than a 30%-complete plan for the right approach. Name the riskiest assumption explicitly (Phase 0.5). If it's cheap to validate, validate it before writing tasks.
- **Plans are contracts, not essays.** Each task describes exactly what to build, what to verify, and how. Ambiguity in the plan becomes bugs in the code. The shared contract lives at `_references/plan-contract.md`.
- **Verification is non-negotiable.** Every task must specify HOW it will be verified. TDD (test-first) is the preferred mode when the task produces deterministic, testable behavior. For other task kinds (migrations, browser APIs, visual UI, config), use the appropriate verification primitive. Never fake a test that can't meaningfully fail.
- **Route to the right skill.** rem-plan is for structured implementation planning. When the problem needs investigation (unclear root cause, unknown codebase area, unchallenged premises), route first — see Phase 0.4.
- **Review before presenting.** The user should never see a plan with obvious gaps. Dispatch a parallel reviewer (Phase 2.8 + 3) before showing it.
- **Plans survive context loss.** A subagent executing this plan should need nothing beyond the plan file, CLAUDE.md, and the codebase.

## Input

`$ARGUMENTS` can be:
- A feature description ("add user avatar upload")
- A path to a rem-solve findings file (`SOLVE-avatar-upload-2026-03-20.md`)
- A path to an existing plan to revise
- No arguments: plan whatever was discussed in conversation

---

## Phase 0: Load Context (MANDATORY)

Before writing any plan:

1. **Read CLAUDE.md** — conventions, patterns, architectural rules.
2. **Read learnings.md** from project memory — known gotchas, failed approaches.
3. **Read feedback files** — user corrections on approach.
4. **Read `~/.claude/memory/feedback_plan_vs_reality_gaps.md`** — 6 systematic gaps from prior plans (full detail lives there). Check EACH against this plan, even if the match seems unlikely; transitive imports hit gaps you didn't expect (a "backend-only" plan importing a shared util rendered in a server page still triggers Gap 2) — default to defending, not skipping:
   - **Gap 1 (API verification)**: verify installed library APIs by reading actual source; add an investigation task for ANY API the plan depends on.
   - **Gap 2 (yarn build)**: for server-page changes, verification = `yarn build`, not `tsc`.
   - **Gap 3 (distribution)**: for user-generated artifacts, document share mechanism + access control + URL structure BEFORE API design.
   - **Gap 4 (deploy readiness)**: add a deploy-readiness task (migrations, CSP, assets, env vars, computed CSS).
   - **Gap 5 (CSS variables)**: after setting custom theme colors, verify with `getComputedStyle`.
   - **Gap 6 (test infra)**: tasks specifying test commands need the runtime + libraries present — see the MANDATORY **Test Infra Audit** step below.
5. **Test-coverage gap analysis (MANDATORY)** — for every file the plan will modify, check its test coverage:

   ```bash
   find . -name "$(basename file.ts .ts).test.ts" -o -name "$(basename file.ts .ts).spec.ts"
   ```

   If missing OR thin coverage → prepend a **characterization test task** before modifications. Rationale: you cannot safely change behavior you don't understand. The characterization test captures current behavior as a baseline; if the plan accidentally breaks it, you catch it at task-level, not production.

6. **Blast-radius grep (MANDATORY)** — for every modified file, grep for importers. Every importer goes in the File Map under "No-change files that depend on modified files". Grep results are PASTED into the plan (file:line), not claimed. A reviewer can re-run the same grep and verify.

7. **If resuming from rem-solve findings**: read the findings file, extract the chosen approach + decision log.

8. **Read every file the plan will modify** — understand what exists NOW.

9. **Search for existing patterns** — if building something similar to existing code, find the template.

10. **Mark uncertainties explicitly** — when requirements are ambiguous, don't guess. Insert `[NEEDS CLARIFICATION: specific question]` markers in notes.

11. **Test Infra Audit (MANDATORY when any task will specify a test command)** — defends Plan-vs-Reality Gap #6. Before writing ANY task whose `Verify` primitive is a test command (`yarn test`, `jest`, `pytest`, `go test`, etc.), run BOTH of these reads:

    a. **Test config**: read `vitest.config.ts` / `jest.config.js` / `pytest.ini` / equivalent. Note the `environment` (node / jsdom / happy-dom / browser), the `setupFiles`, and the `include` pattern.

    b. **Devdep audit**: read `package.json` `devDependencies` (or `requirements-dev.txt`, `Cargo.toml [dev-dependencies]`). Verify EVERY library the plan's tests will import is present:
       - DOM rendering: `jsdom` OR `happy-dom` installed?
       - Component testing: `@testing-library/react` (or vue/svelte equivalent) installed?
       - Custom matchers: `@testing-library/jest-dom`, `vitest-mock-extended`, etc.?
       - Mock utilities: `msw`, `nock`, etc.?

    Cross-reference: every `import` in your planned test files must map to either a present devdep OR a built-in. If a gap exists, add a **prepended infra-setup task** to the plan (Kind: `infra`, installs the missing deps, adds a sentinel test that proves the env works). Do NOT defer this to "I'll add it during execution" — that triggers the `plan adjustment needed` drift counter at execute time.

    **Skip only if** zero plan tasks specify test commands (rare — most plans have at least one).

After investigation, if ANY `[NEEDS CLARIFICATION]` markers exist, use **AskUserQuestion** to resolve them ALL before proceeding to Phase 1. The 2 minutes spent asking saves 2 hours of wrong-direction work.

---

## Phase 0.3: Prior Art & Existing Capabilities Audit (MANDATORY)

**The single highest-value phase. Do not skip.**

Answer before writing any task:

> "Does this need already have a solution in the codebase — an admin panel toggle, a feature flag, a config value, an env var, an existing utility, a similar feature that can be extended, or a deprecated-but-live implementation that can be revived?"

### Execute in 3 steps

1. **Classify the plan type** — new-capability / behavior-change / config-toggle / revival / refactor / bug-fix / migration / other. Full table in `_references/prior-art-audit.md`.
2. **Run ALL 6 searches** regardless of type — admin panel · feature flags & env · existing utilities · similar features · deprecated-but-live · recent git history. Searches + example greps + reviewer-verification rules in `_references/prior-art-audit.md`.
3. **Produce the Prior Art table** in the plan header with each search's findings pasted in (file:line). rem-review-plan re-runs the same searches and flags discrepancies.

### Decision gate

| Search result | Action |
|---------------|--------|
| Existing capability fully satisfies the need | **STOP.** Plan = 1 task ("change setting X from A to B"). Surface to user. Don't write a full plan. |
| Existing capability partially satisfies | Extend — every new file/abstraction must justify why extension was rejected (Complexity Check) |
| Nothing relevant exists | Proceed to Phase 0.4 — but cite the searches so reviewers can verify |

**Anti-pattern (never do this)**: writing a full plan for "new install-prompt timing config" when `SiteConfig.installPromptDismissHours` already exists. See `_references/prior-art-audit.md` § Greenfield-fallacy anti-patterns for 4 concrete failure examples.

---

## Phase 0.4: Route to Another Skill If Needed

rem-plan formalizes a known approach into executable tasks. When the problem is something else, route first:

| If... | Route to | Why |
|---|---|---|
| Bug root cause unclear or guessed | `/rem-root-cause` → rem-plan | Fix for the wrong cause = wasted work |
| Multiple valid approaches, tradeoffs unclear | `/rem-solve` → rem-plan | Compare before committing |
| Premise shaky / approach may be fundamentally wrong | `/rem-challenge` | Stress-test before formalizing |
| Codebase area large and unfamiliar | `/rem-audit` or `/rem-onboard` | Plan without understanding = high review-round count |
| External research needed (library choice, pattern) | `/rem-research` | Inject evidence before planning |
| Requirements unclear / feature under-specified | `/rem-prd` | Plan formalizes known requirements, doesn't discover them |
| Touches UX/design decisions | `/rem-review-ux` on existing flows | Understand existing UX first |

If any trigger applies, surface it using the **Direction change** template in the Runtime narration section above. Don't paste a generic "I recommend..." line - adapt the template to the actual situation so the user understands WHY routing first is the better move.

---

## Phase 0.5: Riskiest Assumption (MANDATORY validation — not optional)

Name ONE assumption that, if wrong, breaks this plan. Not "edge cases" — the *load-bearing* premise.

Examples:
- "We assume existing `prompt.prompt()` fires reliably on Android Chrome 120+. If not, the whole gate logic is moot."
- "We assume we can add `DTSTAMP` to existing ICS output without breaking calendar subscribers. If strict clients reject, we orphan existing subs."
- "We assume Prisma 7's adapter-pg handles this transaction pattern. If not, all DB tasks need rework."

### Decision gate

Every plan MUST validate its riskiest assumption BEFORE task 1, not during task 7.

| Case | Action |
|------|--------|
| Validatable in <30min (read code, check docs, run experiment) | Validate NOW. Paste evidence into plan header: `Validation: <what-you-did>. Result: <what-you-found>. Confidence: <level>.` |
| Validation requires >30min | Add **Task 0 — Validate Riskiest Assumption** as the first task. Kind=`refactor` (investigation producing written finding). All subsequent tasks depend on Task 0 succeeding. |
| Assumption can't be formulated as a validation task | Too speculative for planning — route to `/rem-solve` or `/rem-research` first |
| learnings.md shows this assumption failed before | Premise is wrong. STOP. Route to `/rem-challenge` or `/rem-solve` |

Plans entering rem-execute without a validated (or Task 0-pending) Riskiest Assumption are rejected by rem-review-plan as `PLN-ASSUMPTION-UNVALIDATED (CRITICAL)`.

**This phase prevents the most expensive failure mode**: a fully-formed plan built on a wrong premise, discovered at task 7 of 12.

---

## Phase 0.6: Codex Adversarial Analysis (multi-file or architecture-impact plans)

Get a second perspective at flat rate before writing tasks. Two parallel `cxd` queries, ~30 seconds wall clock, $0 beyond subscription.

**Check availability:**
```bash
which cxd > /dev/null 2>&1 && echo "available" || echo "skip"
```

If available, run BOTH simultaneously (background):

**Pass 1 — Adversarial** (what breaks if the plan's premise is wrong):
```
cxd 'Adversarial review: what is the single riskiest assumption in this plan, and what exactly breaks if it is wrong? Be specific about the failure mode. Plan: [2-sentence summary]' </dev/null > /tmp/claude-codex-pass1.txt 2>&1
```

**Pass 2 — Simpler path** (what the plan might be overlooking):
```
cxd 'Is there a simpler way to achieve [GOAL] that this plan overlooks? Consider: existing code already doing this, config-only solutions, extending vs. building. Plan: [2-sentence summary]' </dev/null > /tmp/claude-codex-pass2.txt 2>&1
```
Never run cxd/cx/cxf backgrounded without `</dev/null` - it hangs forever on stdin.

**Integrate into plan header as "Risks & Alternatives":**
- Pass 1: does the risk overlap Phase 0.5 (note "Codex corroborates") or name a NEW one (add it alongside Phase 0.5)?
- Pass 2: note the alternative + one sentence why the chosen approach is still preferred — or pivot if the alternative is genuinely better.

Skip this phase and note in header if: `cxd` unavailable, the plan touches only 1 file with no API/schema changes, or the plan is purely config/docs with no architecture impact.

**Anti-pattern**: running this phase but burying a Pass 1 risk because it's inconvenient. If Codex names a conflict with the plan's architecture, validate it or add it to Phase 0.5 — don't ignore it.

---

## Phase 0.7: Production Readiness Gate (deploy-adjacent plans)

**Trigger**: plan touches deployment, infrastructure, environment config, or any user-facing release path.

For deploy-adjacent plans, add a **Production Readiness task block** as the final task group. Five domains — each gets specific tasks only if the plan's scope touches it:

| Domain | Add tasks when | Specific checks |
|---|---|---|
| **Application** | Any server-side code ships | Structured JSON logging without PII; health endpoint returns meaningful status (not just 200) |
| **Infrastructure** | Dockerfile, CI config, env vars, or hosting config touched | Reproducible builds (pinned deps); env vars documented and validated at startup; resource limits set |
| **Monitoring** | New service, new job, or new user-facing flow | Metric export for the new path; error-rate alert threshold defined |
| **Security** | Public endpoint added, auth changed, or new dependency | CVE scan on new deps; CORS origin list correct; rate limiting on auth endpoints; security headers present |
| **Operations** | Schema migration or infrastructure change | Rollback procedure documented and tested at production-data scale; failure runbook exists |

**Decision gate**: if the plan has NO deploy-adjacent tasks (pure internal refactor, docs-only, test-only), skip this phase and note "Phase 0.7: N/A — no deployment scope."

This supersedes Gap 4 from Phase 0 for deploy-adjacent plans — Phase 0.7 is the full gate; Gap 4's deploy-readiness checklist is the abbreviated version for non-deploy plans.

---

## Phase 1: Plan Header

Every plan needs: Goal, Non-Goals, Riskiest Assumption (from 0.5), Prior Art (from 0.3), Plan Type, Acceptance Criteria, Architecture Impact, Conventions Applied, Rollback & Reversibility, File Map.

Full markdown template + field definitions: **`_references/plan-templates.md`**. Copy the header block from there and fill in.

Missing required sections = structural findings from rem-review-plan.

---

## Phase 1.5: Complexity Check (MANDATORY)

Audit the plan for its own over-engineering BEFORE writing tasks. For EVERY new file / dependency / pattern / abstraction, justify why the simpler alternative doesn't work.

Full table format + red-flag list + valid/invalid justification patterns + 3 worked examples: **`_references/complexity-check.md`**.

Quick summary:

| If the plan has... | Complexity Check row... |
|--------------------|-------------------------|
| No new files, deps, or patterns | Write "No complexity deviations — all tasks follow established patterns." |
| New wrapper with one consumer | Usually REMOVE — rule of three not met |
| New dep for runtime validation TS can't do | Justified — valid pattern |
| "Config-driven" / "pluggable" design | Usually REMOVE — YAGNI |
| "Future-proofing" / "easier to extend later" | Invalid justification — REMOVE |

If you can't justify a row, remove that complexity from the plan. Simpler alternative wins.

---

## Phase 2: Task Breakdown

Break work into sequential tasks. Each task picks a **Kind** and uses the matching verification primitive.

### Verification primitives (inline quick reference)

| Kind | Verify with | When to use |
|------|-------------|-------------|
| `test` | RED → GREEN unit / integration test | Deterministic, testable behavior. Preferred default. |
| `migration` | Forward + reverse SQL dry-run; row-count/shape diff | Schema / data changes. Idempotency > tests. |
| `config` | `yarn types` + grep for stale refs | No runtime behavior to assert. |
| `ui-visual` | Playwright screenshot OR `yarn dev` + explicit "look for X" | Subjective — state what a human should see. |
| `browser-api` | Manual dev-server verification with steps OR integration harness | SW, `beforeinstallprompt`, clipboard, notifications. |
| `infra` | Exit code 0 from explicit verify command (`yarn build`, etc.) | Build / CI / Docker / env setup. |
| `refactor` | Full test suite passes (behavior-preserving) | No new tests if coverage was adequate pre-refactor. |
| `docs` | Build / link-check passes | Content is the deliverable. |

A mismatched `Kind` and `Verify` is a planning error — rem-review-plan flags it.

### Task template + rules + parallel-execution markers

Full canonical task template (with Kind / Risk / Reversibility / Delegate / Do / Why / Verify / Commit fields), ordering rules, and Parallel Execution Map format: **`_references/plan-templates.md`**.

### Core task rules (inline)

1. **Each task = one behavior or one commit-worthy unit.** Size is bounded by what makes sense to revert together.
2. **Order by dependency.** Schema before queries. Types before consumers. Backend before frontend. Shared utilities before features that use them. Migration / schema tasks FIRST.
3. **Pick the honest Kind.** Don't force `Kind: test` on visual changes or migrations — use the primitive that matches. If a task can't be verified, it shouldn't be a task — split until each piece has a verification primitive.
4. **Include cleanup tasks explicitly.** If a task leaves old code dead/broken, add a cleanup task at the end of its chain.
5. **Destructive / high-risk tasks need explicit rollback notes** in the task body, not just the header.
6. **`Delegate: codex`** marks tasks safe for Codex dispatch — mechanical, pattern-matching, no business judgment. `claude` = requires reasoning / conventions / security / business logic.

---

## Phase 2.8: Pre-Mortem (MANDATORY — catches what structured review misses)

Before pre-review, dispatch ONE subagent (model: **opus**) that works BACKWARD from a hypothetical production incident, generating 5 distinct failure modes given what the plan does AND does not do.

Full prompt + integration rules: **`_references/specialist-prompts.md`** § Pre-Mortem.

If 2+ findings require restructuring tasks → signal the plan is premature. Route back to `/rem-solve`.

---

## Phase 3: Multi-Specialist Pre-Review (MANDATORY before showing user)

Dispatch **4 specialist subagents in parallel** (single message, 4 `Agent` tool calls). Generalist single-reviewer misses domain-specific issues.

| Specialist | Model | Focus |
|------------|-------|-------|
| **Security & data integrity** | opus | Auth, input validation, IDOR, mass assignment, migration safety, transactions, idempotency |
| **Convention & prior failure** | sonnet | CLAUDE.md compliance, learnings respected, plan-vs-reality gaps, Prior Art verification |
| **Execution readiness** | sonnet | Kind+Verify match, dependency order, blast radius in File Map, `[P]` markers safe |
| **Scope & complexity** | sonnet | Complexity Check justified, Non-Goals respected, task collapse opportunities |

Full prompts + aggregation + skip-rules: **`_references/specialist-prompts.md`** § Phase 3.

**Aggregation**: dedupe findings, fix CRITICAL / HIGH in place, re-dispatch only specialists whose findings restructured tasks. If 3+ specialists emit CRITICAL independently → surface to user; offer route to `/rem-solve` or `/rem-challenge`.

---

## Phase 4: Present Plan + Offer Review

### Finding Format (shared contract)

Every risk or concern noted in this skill MUST use the **Explainable Finding** format — full spec at `_references/finding-format.md`. Required fields per item:

- **What** — the technical observation (file:line, literal value, specific mismatch)
- **Why it matters** — plain-English consequence (user impact / cost / team-time / compliance) — translate jargon; don't restate "What"
- **Fix** — concrete action; diff if possible, exact command if applicable
- **Effort / Risk** — `Effort: XS/S/M/L/XL` + `Risk: None/Low/Medium/High`

Severity (CRITICAL / HIGH / MEDIUM / LOW) goes in the finding's heading, not the fields. Observation-only risks without "Why it matters" are BANNED — they force the operator to do translation work on every read.

### Next Steps (shared contract)

The report ends with the clustered Next Steps block per `_references/next-steps-contract.md` — 2-3 named paths, exactly one `→ RECOMMENDED FIRST` with one-sentence why, Deferred row, final action line. A flat list of recommendations is banned.

Save to `docs/plans/YYYY-MM-DD-[feature].md`. Show a summary, NOT the whole plan — user can read the file.

### Codex dispatch check (before offering next step)

If ≥60% of tasks are `Delegate: codex` AND no `Risk: high` AND no `Reversibility: destructive` → surface Codex as a faster/cheaper execution path.

### Next-step flow

Use **AskUserQuestion** with 3 options: "Yes, review (recommended)" / "Skip review, execute directly" / "Save and exit". Review is the default for any plan touching: multiple files, schema, auth/payments/PII, new patterns.

Full Phase 4 flow (Codex criteria, warning messages, status-block updates, 1-task-plan shortcut): **`_references/present-flow.md`**.

---

## Gotchas

Load `_references/plan-gotchas.md` when the plan touches:
- **migrations / schema** → migration ordering, reverse SQL discipline
- **Next.js App Router** → server/client boundary, data export visibility
- **tests** → error-message brittleness, TDD discipline
- **shared types or new API endpoints** → blast radius, auth middleware

Cross-cutting gotchas (shared-type blast radius, signature+call-site adjacency, horizontal-vs-vertical plans) always apply.

---

## Rules

1. **Audit existing capabilities BEFORE proposing new code.** Phase 0.3 is mandatory. The single most common failure is suggesting code for needs already met by admin toggles / feature flags / config / utilities. Anti-pattern: writing a 15-task plan for "configurable install-prompt timing" when `SiteConfig.installPromptDismissHours` already exists. Fix: grep the admin schema first — Phase 0.3 search 1.

2. **Read the codebase BEFORE writing the plan.** You cannot plan modifications to files you haven't read. Phase 0 is not optional. Plans must cite specific files and lines — "based on the pattern" without a file:line reference is a smell. Anti-pattern: plan says "follow the existing middleware pattern" but never names the file. Reviewer re-runs the grep, finds the author never looked.

3. **Route to the right skill.** rem-plan formalizes an approach into executable tasks. Unclear root cause → `/rem-root-cause`. Multiple approaches → `/rem-solve`. Shaky premise → `/rem-challenge`. Unknown codebase → `/rem-audit`. Unclear requirements → `/rem-prd`. Planning a wrong approach with extreme rigor is still a wrong approach.

4. **Name the riskiest assumption and validate it.** Every plan has ONE load-bearing premise. Name it (Phase 0.5). Validate in <30min if possible. If not, document Task 0. If not even that, route to `/rem-solve`. Anti-pattern: "we assume the third-party API supports pagination" as assumption, no validation task, no fallback. 7 tasks later someone discovers it doesn't — plan discarded.

5. **Follow the plan contract.** See `_references/plan-contract.md` for required sections, task template, verification primitives by Kind, status states. rem-review-plan validates against this contract.

6. **Verification is non-negotiable; TDD is preferred when feasible.** Every task specifies a verification primitive matching its Kind. For deterministic behavior: RED → GREEN test (`_references/tdd-discipline.md`). For migrations / browser APIs / visual UI / config — use the primitive appropriate to that Kind. Anti-pattern: `Kind: ui-visual` task with `Verify: yarn tsc --noEmit`. tsc can't see pixels — mismatched primitive, planning error.

7. **Every task must be independently executable.** A subagent reading only this task (plus the codebase) should be able to complete it. Include pointers (file:line + pattern to match), not inline code dumps. Anti-pattern: task body says "implement the function" with 80 lines of inline code. Strip to "Implement `foo()` in `src/bar.ts` matching the `baz()` pattern at `src/qux.ts:42`. Signature: `(x: X) => Y`. Edge cases: empty array, null input."

8. **Match existing patterns.** If the codebase does X, your plan does X. Don't introduce new patterns when existing ones work. Complexity Check justifies every deviation. Anti-pattern: plan says "use React Query for this mutation" when the entire codebase uses direct `fetch()` + `useState`. Either the plan is wrong or the project is mid-migration — if the latter, CLAUDE.md should say so.

9. **Account for blast radius and rollback.** Every modified file has dependents — list them. Every destructive / one-way task has rollback — specify it. Anti-pattern: plan changes a shared type signature without listing the 14 importers. 14 TypeScript errors at execute time, blast radius discovered in frustration.

10. **Pre-review before presenting; offer rem-review-plan next.** Phase 2.8 (pre-mortem) + Phase 3 (4 specialists) catch gaps before the user sees them. Phase 4 offers `/rem-review-plan` as default. Plans benefit from a second deeper pass — especially for schema / security / multi-file work.

11. **Plans are living documents with an append-only status log.** When the plan is adjusted during review or execution, update in place AND append to the header's status block (round N findings, what changed, why). Don't overwrite history — preserving it lets future readers understand how the plan evolved.

12. **When Phase 0.3 finds existing capability, plan = 1 task.** Don't build a 15-task greenfield plan when the prior-art audit found a satisfying capability. Surface the one-task alternative to the user and ask to proceed. `_references/present-flow.md` § 1-task shortcut handles the output.

13. **Offer `/rem-learn` at terminal states.** PREMISE-WRONG, NEEDS RETHINK after specialists, Approved-after-3-rounds, and wrong-Riskiest-Assumption are the moments that produce durable lessons. The reasoning gap that caused the failure is more valuable to capture than the plan that succeeded. See `_references/present-flow.md` § Post-plan learning hook. Anti-pattern: plan is abandoned with PREMISE-WRONG; the insight that "we almost reinvented X" never makes it to CLAUDE.md; three weeks later someone drafts another plan to reinvent X. Fix: suggest `/rem-learn` at the terminal state.

14. **Findings MUST include plain-English "Why it matters", not just the observation.** Anti-pattern: reporting `user_id label on request_counter` with no explanation of what breaks. Fix: every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with `next-steps-contract.md` cluster, not a flat list.

15. **Narrate using the Runtime narration templates, not the SKILL's internal labels.** The body of this skill talks in "Phase 0.3", "Riskiest Assumption", "Pre-Mortem" - those are internal anchors so the model knows where each mechanic lives. They MUST NOT appear in the words the user reads. Anti-pattern: saying "Running Phase 0.3 Prior Art audit now" - the user has no idea what 0.3 is. Fix: use the Open / Discovery / Phase shift / Direction change / Close templates in the Runtime narration section above; consult the banned-vocabulary mini-table when in doubt. This rule is a publication gate per `_references/output-voice.md` - a structurally-correct plan presented in skill jargon ships broken.
