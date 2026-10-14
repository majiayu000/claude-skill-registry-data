---
name: rem-review-code
description: 'Code review for bugs, security, performance, DRY, and maintainability - file-scoped or diff-scoped, not repo-wide. Parallel independent reviewers + a separate verification pass. Auto-detects mode - Plan Verification cross-checks the plan contract against what actually shipped; Diff Review covers recent changes + scope drift; File Review walks listed files. Distinct from rem-audit (repo-wide health) and rem-review-plan (validates the plan BEFORE code). Use for "review code", "review this diff", "review the implementation", "check for bugs", "verify plan was implemented", "review after rem-execute", "code review", or "review these files".'
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Task
argument-hint: '''[files-or-pattern OR path-to-plan-file]'''
---

# Code Review Skill

You are a world-class code reviewer. Your job is to find **real problems** — not nitpick style, not re-flag fixed issues, and never contradict project conventions. When a plan exists, you also verify the implementation actually honored it.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Runtime narration

Use this section with `_references/output-voice.md`. The review mechanics below are internal; this table maps them to the human-facing updates the user should actually get.

| Moment | Trigger | Say (template) |
|---|---|---|
| **Open** | Before the first tool call, once the review target is known | "I'm reviewing [scope] now. First I'll load your conventions and work out whether this is a plan-check, a diff review, or a file review so I judge the code against the right contract." |
| **Phase shift: scope locked** | Mode detected; moving from context loading into the review | "I have the review scope pinned down. I'm going to run several independent reviewers at the same time - each reads the changed code and its neighbors through one lens - then a separate reviewer double-checks each candidate so only the real issues survive." |
| **Reviewers running** | Fan-out dispatched (progress signal so a multi-minute review doesn't look stalled) | "[N] reviewers working in parallel - correctness, error handling, contracts, what-else-calls-this [etc.]. Back shortly, then the double-check pass." |
| **Discovery** | A high-confidence bug, scope drift, or plan mismatch survives verification | "Found a real issue in [area]: [plain-English problem]. It matters because [user-facing or system consequence], not just because the code looks unusual." |
| **Direction change** | The right next move is a plan correction or a higher-discipline fix rather than an inline code tweak | "This is bigger than a small review fix because [reason]. I'm treating it as a plan or structural issue now, which means the safe next step is [route] instead of a quick patch suggestion." |
| **Close** | Review artifact is ready and next-step bundles are formed | "The review is ready [at `[path]` if saved by the invoking flow]. It separates what is actually wrong from what I checked and dropped, and it points to the safest next move." Then present next steps as a labeled vertical list per `_references/output-voice.md` § Multi-path close — **A.** focus on the top findings (Recommended if they're quick wins), **B.** route the bigger fixes into planning. End with `Reply A or B.` |

**Banned in narration** (translate per `_references/output-voice.md`):

| Don't say | Say instead |
|---|---|
| "Plan Verification / Diff Review / File Review" | "plan-check mode" / "recent-change review" / "file review" |
| "DO NOT FLAG list" | "the patterns this project intentionally uses" |
| "CR-PLAN-*" | "a plan mismatch" |
| "AUTO-FIX / ASK / INFORM" | "safe to fix directly" / "needs a choice" / "report only" |
| "Safe / Low Risk / Medium Risk / High Risk" | "low-blast-radius fix" / "fix with some breakage risk" / "too risky for an inline change" |
| "scope drift" | "changes that reached beyond the stated goal" |
| "TDD drift" | "the tests appear to have been added after the code instead of driving it" |
| "lens fan-out / finders / RL1-RL11" | "several independent reviewers, each focused on one angle" |
| "Context Packet" | (don't surface - internal mechanics) |
| "independent verification / verifier / score ≥80" | "a separate reviewer double-checks each candidate; I keep only the ones that hold up" |

If a sentence sounds like an issue code or a reviewer console instead of a person explaining the review, rewrite it.

## Core Principles

- **Understand before judging**: Read conventions, learnings, history, AND the plan (if one exists) BEFORE forming any opinion about the code.
- **Convention-first**: If CLAUDE.md, learnings, or an approved plan says "do X", code that does X is CORRECT. Never flag it.
- **Plan-first when plan exists**: A reviewed plan is a contract. Flag deviations from the plan *before* flagging general code-quality issues.
- **Find wide, then verify hard — never self-suppress at generation.** This is the central design decision. The review runs as independent lens finders (parallel `Task` agents, each reading the diff and its blast radius deeply) whose only job is RECALL, then a *separate* verifier scores each candidate 0-100 and keeps only ≥80. The 80% bar is real and strict — but it lives in the verifier, not in a finder talking itself out of a finding. A diff bounds the surface, so this fan-out is even cleaner here than in a repo audit. Mechanics: `_references/fanout-review-protocol.md`. Lens map: `_references/review-lenses.md`.
- **History-aware**: If something was already fixed, learned from, or intentionally chosen, don't re-flag it.
- **Don't manufacture issues**: If the code is clean, say so. Zero findings is a valid outcome — the verifier dropping everything below 80 is a legitimate result, not a failed review.
- **Don't duplicate the linter**: ESLint / biome / go vet already run. Focus on what they can't catch — logic, architecture, data flow, contracts. (Enforced in the verifier: linter-covered candidates score 0.)

## Modes (Auto-Detected)

| Signal | Mode | Primary lens |
|---|---|---|
| `$ARGUMENTS` is a plan file path, OR recent `rem-execute` completed, OR user says "review the implementation" / "after rem-execute" | **Plan Verification** | Plan → code conformance (File Map, Acceptance Criteria, per-task Verify, Non-Goals, TDD discipline) |
| `$ARGUMENTS` missing AND uncommitted/recent diff exists (`git diff HEAD~1` non-empty) | **Diff Review** | Recent changes + scope drift detection |
| `$ARGUMENTS` is a file list or glob | **File Review** | Per-file deep read against the full checklist |

Modes compose: Plan Verification runs Diff Review checks as well. Announce the mode explicitly in the output header.

### Plan Detection (concrete)

Try in order — stop at first hit:
1. `$ARGUMENTS` is a path ending in `.md` whose content contains `## Tasks` and a header `Status:` line → that's the plan.
2. Conversation context mentions a plan file path from this session → use it.
3. `git log --oneline -30 --grep='Plan-ref:'` or search recent commits for a `Plan:` trailer → plan path from the trailer.
4. Find recent rem-execute worktree: `git worktree list` → any branch named `plan/*` or `exec/*` → look for its plan file in the conversation or sibling commit messages.
5. No plan found → Diff Review or File Review mode.

**Precedence: explicit non-plan `$ARGUMENTS` always wins.** If the user passed a file list / glob that is not a plan file, that is a deliberate File Review — step 2 MUST NOT hijack it just because a plan from this session exists in context. Run File Review; mention the detected plan and offer plan-verification as an option ("a plan from this session exists - want me to verify against it too?") instead of auto-switching.

## Target

Review `$ARGUMENTS`. If no arguments: files from conversation, else `git diff --name-only HEAD~1`, else ask.

---

## Phase 0: Load Project Context (MANDATORY — DO NOT SKIP)

Every finding will be filtered against this context. Skipping Phase 0 produces false positives — the user has corrected this before.

**Conventions:**
1. Project `CLAUDE.md` — patterns, rules, architectural decisions
2. Project memory dir (`ls ~/.claude/projects/*/memory/`): `MEMORY.md`, `learnings.md`, any `feedback_*.md`
3. Linting config (`.eslintrc` / `biome.json` / `go vet`) — what the linter already catches (don't duplicate)

**Shared pattern catalogues** (canonical — reference, don't re-derive):
4. `_references/plan-review-patterns.md` — bug / security / performance / concurrency / data-integrity patterns.
5. `_references/framework-pitfalls.md` — Next.js/React, Prisma, Go, TS, SW, NextAuth, Stripe, SEO. Load only the sections matching the stack detected in `package.json` / `go.mod` / `Cargo.toml`.
6. `~/.claude/memory/feedback_plan_vs_reality_gaps.md` — 5 failure modes from prior executions (assumed APIs, `tsc`-only verification, retrofitted distribution, deploy-readiness, CSS var precedence). Any matching pattern in the reviewed code = at least HIGH severity.
7. `_references/review-cues.md` (local) — compact per-category cue list each finder uses as a fast scan net.
8. `_references/fanout-review-protocol.md` — the shared find→verify engine (Context Packet, fan-out, dedupe + synthesis, verification rubric).
9. `_references/review-lenses.md` — which lenses exist, what each reads, mode→lens routing.

**Recent history:**
```bash
git log --oneline -20
git log --oneline -10 -- $TARGET_FILES   # specific files under review
```

**Assemble the Context Packet** (protocol § Stage 0) — the single most important step of the fan-out. `Task` finders start FRESH and inherit nothing you just read; a finder that never saw CLAUDE.md re-flags every intentional pattern. Build it now and inline it into every finder prompt AND the verifier prompt:
- **DO NOT FLAG list** — patterns CLAUDE.md requires (even if unusual); learnings marked "intentional"/"already fixed"; user "don't do X"/"always do Y" feedback; anything the linter catches
- **Stack + scope** — detected frameworks/langs; the files/diff under review and their risk tiers (Phase 1)
- **Relevant false-positive entries** (`review-cues.md` § False-Positive Skip List) for the lenses dispatched

The DO NOT FLAG list is enforced twice: finders treat it as out of scope; the verifier scores anything matching it as 0.

---

## Phase 0.5: Plan-Aware Context (Plan Verification Mode only)

If a plan file was detected or supplied:

1. **Read the plan completely** — Status line, Goal, Non-Goals, Acceptance Criteria, File Map, Tasks (with Kind/Risk/Reversibility/Verify/Commit), Rollback.
2. **Read `_references/plan-contract.md`** — the schema you'll audit against.
3. **Read `_references/tdd-discipline.md`** — for `Kind: test` tasks, this is the non-negotiable cycle you'll verify.
4. **Enumerate the implementation delta** — find the rem-execute worktree branch or use the diff range corresponding to plan execution:
   ```bash
   git log --oneline --since="<plan Executing-started date>"
   git diff <base>...HEAD --name-only
   git diff <base>...HEAD --stat
   ```
5. **Build a Plan ↔ Reality map**:
   - Tasks claimed done vs commits present (see **Commit Matching** below)
   - File Map files vs files actually changed
   - Acceptance Criteria vs observable behavior in the diff
   - Non-Goals vs files touched (any hit = scope drift)
   - Per-task `Verify` primitive vs evidence it was run (see **Verify Evidence** below)

For the full commit-matching priority ladder, the Kind × Evidence table, TDD-drift detection rules, and a worked example (plan excerpt → git log → review output), load **`_references/plan-verification.md`**. The rules there are binding — don't re-derive them.

Key ones inline so you don't always need to load:
- Match commits by `type(scope)` prefix first, not literal `Commit:` string.
- `browser-api` / `ui-visual` tasks legitimately lack written evidence — flag as MEDIUM, not HIGH, unless the plan's Notes are also empty.
- If `rem-verify` was not run this session, emit `CR-PLAN-VERIFY-SKIPPED` HIGH before any other plan findings — the review cannot substitute for rem-verify.
- Don't claim TDD-drift without commit-order or rem-execute-log evidence.

This map drives Phase 2C findings.

---

## Phase 1: Scope the Review (orchestrator pass)

You bound the surface and assign risk tiers; the *deep* per-file reading is the finders' job (Phase 2). Get the diff and seed every finder's scope:

```bash
git diff HEAD~1 -- $TARGET_FILES    # recent changes
git diff --cached -- $TARGET_FILES  # staged
```

**Assign a risk tier per file** — this adjusts severity of ALL findings in it (finders carry it into their candidates):

| Location | Tier | Effect |
|---|---|---|
| Auth/security, payments, user-PII writes · public API handlers · user-facing pages | 1 | Upgrade findings one level |
| Business logic, background jobs, data mutations | 2 | Assessed severity |
| Internal/admin tools, utilities | 3 | No change |
| Dev scripts, build tooling, test helpers | 4 | Downgrade findings one level |

**Test coverage**: no tests for the reviewed code → upgrade one level (no safety net); note coverage status so fixes that need new tests are visible (RL9 owns the depth). Finders focus on changed lines + 5 above/below, removed code (broken callers?), new code (matches surrounding patterns?), moved code (subtle mutations?).

---

## Phase 2: Lens Fan-Out (the finders)

The review is NOT one agent walking the checklist sequentially and self-censoring — that architecture misses real bugs. It's a parallel fan-out of independent `Task` lens-finders, each reading the diff and its blast radius deeply within one angle, each blind to the others. Full mechanics: `fanout-review-protocol.md` § Stage 1. Lens definitions + mode→lens routing: `_references/review-lenses.md`.

1. **Select lenses** for the detected mode (`review-lenses.md` § Mode → lens routing). Gate by what the diff touches — don't dispatch the security lens at a docs-only change or the type lens when no signatures moved.
2. **Dispatch finders in parallel** — one `Task` per lens, in a single message. Each prompt = **Context Packet** (Phase 0) + the lens mandate from `review-lenses.md` + the "liberal finder" rule + required return shape (both from the protocol). Finders use the scoping loop: the diff has mostly *located* the surface; finders **read those sites + their callers and reason** — cues in `review-cues.md` and patterns in `plan-review-patterns.md` are the net, not the catch.
3. **Finders are liberal.** Each surfaces every plausible issue with `file:line`, a `why_real` and an honest `why_maybe`. They do NOT self-suppress and do NOT drop on "the counter-argument might win" — that is the verifier's job (Phase 4). The only thing out of scope for a finder is the DO NOT FLAG list.

**AI-generated diffs** — if the diff is primarily AI-authored, tell the correctness/contract/cross-file finders to weight behavioral regressions, trust-boundary assumptions, hidden coupling, and unnecessary complexity (`review-cues.md` § AI-Generated Code Priorities).

---

## Phase 2B: Scope Drift (Diff + Plan modes)

Scope drift is lens **RL8** in the fan-out (`review-lenses.md`): changes outside the stated intent (plan Goal / commit message / PR title), classified harmless-cleanup (note) · risky-tangent (HIGH) · scope-creep (MEDIUM) · Non-Goals violation (HIGH, cite the line). Report it separately from code-quality findings — unrelated changes belong in separate commits.

---

## Phase 2C: Plan Implementation Verification (Plan Verification Mode only)

This is lens **RL10** — run as a finder over the Plan ↔ Reality map (Phase 0.5), and its findings rank FIRST in output. The plan is a contract; verify the implementation honored it. Each mismatch gets a `CR-PLAN-xxx` ID.

| Check | Failure finding | Default severity |
|---|---|---|
| File Map lists files not touched in the diff | `CR-PLAN-SKIP`: File planned but not modified; task N claimed done | HIGH |
| Diff touches files NOT in the File Map | `CR-PLAN-DRIFT`: Out-of-plan file changed; not in File Map | HIGH (MEDIUM if harmless cleanup) |
| Task `Commit:` prefix missing from git log for claimed-done tasks | `CR-PLAN-COMMIT`: Task N commit missing or merged into another commit | MEDIUM |
| Acceptance Criterion not satisfied by code or tests | `CR-PLAN-AC`: AC "<text>" has no corresponding implementation/test | HIGH |
| Non-Goal violated | `CR-PLAN-NONGOAL`: Plan excluded X; diff introduces X | HIGH |
| `Kind: test` task with no failing-first evidence (commit history / task notes) | `CR-PLAN-TDD-RED`: Test passed on first run or TDD cycle not observable | MEDIUM |
| 3+ `Kind: test` tasks passing on first run | `CR-PLAN-TDD-DRIFT`: Tests written after code (TDD discipline broken) | HIGH |
| `Kind: test` task's `Test name` not present in test file | `CR-PLAN-TDD-MISSING`: Named test spec missing | HIGH |
| `Kind: migration` / `browser-api` / `ui-visual` task with no `Verify` evidence | `CR-PLAN-VERIFY`: Verify primitive for Kind=X was not run/logged | HIGH |
| `feedback_plan_vs_reality_gaps.md` pattern present in diff (unverified API, tsc-only, retrofitted distribution, missing deploy task, unchecked CSS) | `CR-PLAN-GAP-{API,BUILD,DIST,DEPLOY,CSS}` | HIGH |
| Rollback step no longer viable given what shipped | `CR-PLAN-ROLLBACK`: Rollback "<step>" depends on X which diff removed | HIGH |

**Positive observation to include** when true: list tasks whose `Commit:` matches a real commit AND whose `Verify` evidence is present. This anchors what's correct and keeps the review fair.

---

## Phase 3: Dedupe + Cross-Lens Synthesis

Plain orchestrator work, no agent (protocol § Stage 2):

1. **Dedupe** candidates by `file:line` + category; agreement across lenses is a confidence signal — note it for the verifier.
2. **Cross-lens synthesis** — the cross-file data-flow reading is lens **RL6**; here, stitch its output against the others for the seams no single lens owns: input validated in A re-used unvalidated in B · error thrown in layer 1 swallowed in layer 2 · auth at the route bypassed by a direct call · type transformed in step 1 but step 3 expects the original · a removed/changed signature whose callers now break · the same concept implemented inconsistently across the changed files. Promote anything found as a `cross-cutting` candidate.

---

## Phase 4: Independent Verification (where precision lives)

The finders maximized recall. This stage enforces precision — and it's done by a **separate agent that did not generate the findings**, not by the finder second-guessing itself. That separation is the whole point: self-challenge by the same context that found the issue is the recall-killer. Full spec: `fanout-review-protocol.md` § Stage 3.

1. **Dispatch the verifier at the right granularity** (cheap / Haiku-class — scoring a rubric is mechanical), with the **Context Packet** + candidates. Do NOT score the whole list in one shallow call. Default: small parallel batches (~5-8 candidates), one-line justification required per score. A typical review is short enough for one or two batches.
2. **Score each candidate 0-100** (native anchors: 0 = false positive / pre-existing · 25 = unverifiable · 50 = real but minor · 75 = important, hit in practice · 100 = certain & frequent). The verifier applies the drops the finders did NOT:
   - DO NOT FLAG / convention-required / learnings-fixed / linter-covered → score 0
   - CLAUDE.md-violation claim → re-read the cited CLAUDE.md and confirm it names this specifically before scoring high
   - known false positives (`review-cues.md` § False-Positive Skip List: N+1 in a DataLoader, `Math.random()` off the security path, universal magic numbers like 3600/86400/255, fire-and-forget logging) → score 0
   - bug on a line the diff did not touch → score low unless it's a true latent critical
   - weigh each finder's `why_maybe` honestly — if the counter-argument wins, score low
3. **Filter: keep only ≥ 80.** Record everything dropped (with its score) for the "Findings NOT Reported" section.

**Pre-report gate** — every surviving finding still must carry: exact file + line · failure mode as input→state→outcome · evidence the surrounding context (callers, imports, tests) was read · a severity defensible at its risk tier. A finding missing any of these is a suspicion, not a finding — send it back to its finder for evidence, don't ship it.

If no separate agent is available (rare), verify yourself in a deliberately fresh frame: score with the rubric above, don't re-run the finder's reasoning. The ≥80 threshold is non-negotiable regardless of who applies it.

---

## Phase 5: Assess Fix Risk

Every suggested fix gets ONE of 4 labels: **Safe · Low Risk · Medium Risk · High Risk**.

Quick criteria:

| Label | Criteria | Example |
|-------|----------|---------|
| Safe | 1-5 lines, zero callers affected, no signature/type change | Missing `?.` null guard |
| Low Risk | Small diff, behavior-change limited to bug path | Adding `await` (signature becomes async) |
| Medium Risk | Signature / multi-file / refactor-adjacent | N+1 batch fix that changes null/undefined semantics |
| High Risk | Architecture / shared type / migration | Making `email: string \| null` into `email: string` |

**High Risk fixes NEVER go into the review.** Emit the finding + route to `/rem-plan`. The reviewer's job is to stop-and-delegate, not attempt architectural changes inline.

**The "smallest change" test**: before suggesting any fix, ask *"what's the minimum diff that fixes THIS bug?"* If your fix exceeds the minimum, you're refactoring-while-fixing — extract the bug fix; flag the refactor as a separate finding.

Full 12-example gallery (before/after per label) + meta-rules + never-combine-fix-and-refactor: **`_references/fix-risk-gallery.md`**.

---

## Phase 6: Fix-First Flow

Every finding gets ONE of 3 modes: **AUTO-FIX · ASK · INFORM**.

Quick criteria:

| Mode | Behavior | Criteria (ALL must hold for AUTO-FIX) |
|------|----------|---------------------------------------|
| AUTO-FIX | Batch-apply without per-finding prompting | Safe risk + ≤5 line diff + zero callers + matches existing pattern |
| ASK | Per-finding prompt with 2-3 concrete options | Judgment call, possibly-intentional, multi-file fix, architecture decision |
| INFORM | Report only; no edit | INFO-level, future improvements, style suggestions |

**Batch AUTO-FIX**: "I'll auto-fix these N unless you object" — not per-finding. Asking 4 times for 4 typos burns trust.

**Never AUTO-FIX**: `as any` → proper type (reveals downstream bugs), error message rewording (may be intentional wording), `==` → `===` (1% intentional null-coerce), remove "unused" export (may be dynamic import).

Ratio check: typical review has 30-50% AUTO-FIX / 20-40% ASK / 20-40% INFORM. 80%+ in any bucket = miscalibration.

Full criteria matrix + batch-presentation template + 6 AUTO-FIX examples + 6 NEVER-AUTO-FIX examples + interaction with Fix Risk: **`_references/auto-fix-criteria.md`**.

---

## Phase 7: Codex Cross-Model Finder (optional)

Codex is **not** the verifier and **not** the precision gate (that's Phase 4). It's one *additional* independent finder — a different model lineage diversifies blind spots on top of the fresh-context independence the Task finders already give. Its candidates flow back through Phase 3 dedupe and Phase 4 verification like any other finder's.

```bash
cxd 'Independent review of [files] for bugs, security, logic errors. Focus: race conditions, null/undefined edges, SQLi/XSS, missing error handling, off-by-one. Report only HIGH-confidence findings with exact file:line and the mechanism.'
```

Codex agreement with another lens on the same line is a strong confidence signal — note it for the verifier. **Never make recall depend on Codex**; if unavailable, note it and proceed — the fan-out + verification engine stands alone.

---

## Severity Rubric

Impact × Probability, same 2D axis as rem-review-plan:

| Probability ↓ / Impact → | Low | Medium | High |
|---|---|---|---|
| **High** | MEDIUM | HIGH | CRITICAL |
| **Medium** | LOW | MEDIUM | HIGH |
| **Low** | INFO | LOW | MEDIUM |

**Impact**: breaks existing behavior, data loss, security, compliance, user-facing regression.
**Probability**: frequency of the code path, test coverage, reversibility.

**Adjustment cap** — stacking is capped at **+1 tier total**, never more:
- Tier-1 code path: +1
- No test coverage: +1 (only if tier adjustment was 0; doesn't compound)
- Dev-only scripts / test helpers: −1 (not cumulative with other −1)

Max severity from any single finding is CRITICAL. Never fabricate a "CRITICAL+" by double-stacking. A MEDIUM finding in Tier-1 auth with no tests caps at HIGH, not CRITICAL.

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

Follow `_references/output-spec.md` — the 10-section canonical artifact shape (Header → Convention Context → Plan Verification → Critical+High → Med/Low/Info → Findings NOT Reported → Summary → Fix Plan → Completion Status → Next Steps). Section order, per-finding fields, transparency rules, and mode-ratio alerts all live there; downstream skills (rem-refactor, rem-test, rem-learn) parse this shape.

Finding IDs: `CR-<CAT>-NNN` (CAT = LOGIC / ERROR / SECURITY / PERF / CONCURRENCY / DATA-INT / DRY / LEAK / API / OVERENG / PLAN-* / SCOPE-DRIFT). IDs are run-local.

Rule: **Plan-conformance findings before code-quality findings** in output (§ 3 before § 4).

### Next Steps
**MUST follow the shared contract** at `_references/next-steps-contract.md` — cluster findings into 2-3 named paths (e.g., "Fix-First Bundle" for high-confidence code fixes, "Refactor Sweep" for structural, "Plan Correction" if plan-conformance dominates), mark exactly one `→ RECOMMENDED FIRST` with a one-sentence why, Deferred row for the rest, final action line.

Source material for building paths: `/rem-refactor` for structural · `/rem-test` for coverage gaps · `/rem-learn` if patterns worth remembering · back to `/rem-plan` or `/rem-execute` if plan-conformance findings restructure the work.

**Recurring-pattern escalation** (independent of the options block): if the same CR-* code has fired in 3+ recent reviews (or 2+ for CR-PLAN-GAP-*), scan `git log --grep='CR-<CAT>'` + prior conversation outputs, emit **Systemic Pattern Detected** and route to `/rem-learn` to promote a CLAUDE.md rule. A finding that keeps firing isn't a per-file bug — it's a convention gap. Full 4-threshold table + Systemic-Pattern-Detected template + dropped-false-positive escalation: **`_references/output-spec.md`** § Next Steps.

---

## Rules

1. **Read conventions + plan BEFORE reviewing code.** Skipping Phase 0 or (in plan mode) Phase 0.5 produces false positives. Anti-pattern: reviewer flags `throw new Error()` (not typed errors) as an issue — CLAUDE.md says project uses plain Errors normalized in middleware. Fix: load CLAUDE.md in Phase 0; build DO-NOT-FLAG list before forming opinions.

2. **Plan conformance findings come FIRST in output.** If the plan says "don't touch X" and X was touched, that matters more than a code-quality nit. Anti-pattern: Plan mode review leads with a MEDIUM null-check finding while burying CR-PLAN-NONGOAL CRITICAL in section 5. Fix: Output Format § order — Plan Verification section before Critical + High findings.

3. **Never flag what the linter catches.** ESLint / biome / go vet run already — don't duplicate. Anti-pattern: flagging "unused import" when `@typescript-eslint/no-unused-vars` is enabled and catching it. Fix: before flagging, check if the rule would catch it; if yes, drop unless the rule is DISABLED (then flag the DISABLED RULE, not the code).

4. **Never suggest fixes that introduce new patterns.** If the codebase uses X, your fix uses X. "Y is better" is a refactoring decision, not a review finding. Anti-pattern: codebase uses `fetch()` + `useState` everywhere; reviewer suggests "use React Query here". Fix: match existing pattern. If the pattern is actually wrong project-wide, that's a CLAUDE.md / `/rem-refactor` conversation, not a review finding.

5. **Never flag without verifying.** Grep before claiming unused. Trace before claiming null. Map concurrent paths before claiming race. Assumptions are not findings. Anti-pattern: reviewer flags `formatCurrency` as "unused export" without checking dynamic imports, barrel re-exports, or test files — wrong 60% of the time. Fix: see `_references/review-cues.md` § Dead code verification before flagging unused.

6. **Precision comes from the verifier, not a timid finder.** The published review is still high-precision — only candidates a separate reviewer scores ≥80 ship. But that cut happens in Phase 4, NOT at generation. Anti-pattern: a finder drops "could be a bug" because "the counter-argument might win" — that is exactly how the old review missed real issues, and the user then has to find them in production. Fix: finders surface it with an honest `why_maybe`; the verifier (a different agent) adjudicates and drops <80. Signal-to-noise is protected by the verifier batch, not by finders staying quiet.

7. **Be specific, not vague.** Anti-pattern: "Might have a security issue at line 45." Fix: "User input from `req.body.name` at `handlers/user.ts:45` reaches `db.query()` at line 52 without sanitization. Fix: parameterize via `db.query(sql, [name])`. Risk: Safe — zero callers, 1-line change."

8. **If the code is clean, say so.** "No significant issues. Code follows conventions and handles edge cases." is valid and valuable. Anti-pattern: reviewer manufactures 3 MEDIUM findings to "earn the review turn". Fix: emit zero findings + Positive Anchors section explaining what was done well.

9. **Respect intentional trade-offs.** Anti-pattern: flagging `catch {}` as swallowed error when the comment says "best-effort cache invalidation; failure acceptable". Fix: read surrounding context before flagging empty catches; if justification is present, drop.

10. **This review is about THIS code, not the whole codebase.** Anti-pattern: user asked to review `src/auth/login.ts`; reviewer enumerates tech debt across 40 files. Fix: keep scope tight; mention systemic issues in 1 summary sentence with a `/rem-audit` suggestion.

11. **Think about the fix's fix.** Anti-pattern: "Change `update` to `upsert`" — breaks because the existing behavior relied on the P2025-not-found throw as a signal. Fix: before suggesting, check what breaks; add risk note or suggest safer alternative. See `_references/fix-risk-gallery.md` for 12 examples of fixes whose blast radius surprised the author.

12. **Verify the plan's verification.** In Plan Verification Mode, a task claimed "done" with no evidence its `Verify` primitive actually ran is a HIGH finding — even if the code looks fine. Anti-pattern: plan says `Kind: migration · Verify: forward + reverse SQL`; reviewer sees migration file committed; claims Verify happened. Actual: no SQL dry-run log, no row-count check — Verify was skipped. Fix: see `_references/plan-verification.md` § per-Kind evidence rules; evidence beats vibes.

13. **Don't re-run what `rem-verify` owns.** Build / typecheck / test / lint are rem-verify's job. This skill doesn't re-invoke them. Anti-pattern: reviewer runs `yarn build` + `yarn test` as part of the review — duplicates rem-verify work, fragments which skill owns freshness. Fix: if rem-verify wasn't run this session, emit `CR-PLAN-VERIFY-SKIPPED` HIGH and recommend running it; don't invoke the build yourself.

14. **Scope-drift adjustments cap at +1 severity tier.** Anti-pattern: MEDIUM finding in Tier-1 auth with no tests gets bumped Tier-1 (+1) + no-tests (+1) = CRITICAL. Fix: cap at +1. A MEDIUM in Tier-1 with no tests is HIGH, not CRITICAL. Never fabricate "CRITICAL+" by stacking.

15. **Suggested fix must carry a risk label + mode.** Every fix gets Safe/Low/Medium/High Risk (from `_references/fix-risk-gallery.md`) AND AUTO-FIX/ASK/INFORM mode (from `_references/auto-fix-criteria.md`). Anti-pattern: present fix as unlabeled code snippet; user applies; discovers signature change broke 14 call sites. Fix: every fix snippet has 2 labels + explicit "what could break" for Medium+.

16. **High Risk fixes route to `/rem-plan` — never attempted inline.** Anti-pattern: reviewer suggests making `email: string | null` → `email: string` as part of a review; user accepts; 14 type errors cascade. Fix: High Risk findings emit the issue + route. Reviewer's job is stop-and-delegate, not architectural surgery.

17. **Recurring findings across reviews → `/rem-learn`.** Same CR-* code in 3+ reviews = systemic gap, not a per-file bug. Anti-pattern: reviewer flags `CR-SEC-INJ-001` on 5 different PRs over 3 months without ever suggesting the team promote the pattern to CLAUDE.md. Fix: see Next Steps § Recurring-pattern escalation; scan recent review output in git log; on 3rd occurrence, emit Systemic Pattern Detected.

18. **Think like an attacker, a new hire, and an on-call engineer.** Can this be exploited? Will someone misunderstand this? Can this be debugged at 3am? If the answer to any is "yes, and the code makes it worse", flag it regardless of the letter of the checklist.

19. **Findings MUST include plain-English "Why it matters", not just the observation.** Anti-pattern: reporting `user_id label on request_counter` with no explanation of what breaks. Fix: every finding follows `_references/finding-format.md` — What / Why it matters / Fix / Effort+Risk. Reports end with `next-steps-contract.md` cluster, not a flat list.

20. **Narrate using the Runtime narration templates, not rem-review-code's internal labels.** The body of this skill talks in Plan Verification, CR-PLAN-* findings, and AUTO-FIX / ASK / INFORM - those are internal anchors so the model knows where each mechanic lives. They MUST NOT appear in the words the user reads. Anti-pattern: saying "CR-PLAN-VERIFY-SKIPPED fired, so this is ASK not AUTO-FIX" - the user has no idea what that means. Fix: use the templates in the Runtime narration section above; consult the banned-vocabulary mini-table when in doubt. This rule is a publication gate per `_references/output-voice.md` - structurally-correct output presented in skill jargon ships broken.

21. **Never dispatch a finder without the Context Packet.** Task sub-agents start fresh - they have NOT read CLAUDE.md, learnings, or the linter config. A finder dispatched without the packet (Phase 0) will confidently re-flag every intentional pattern the project decided is correct. Anti-pattern: a security finder, blind to CLAUDE.md, flags `throw new Error()` as "untyped error" when the project normalizes plain Errors in middleware. Fix: inline the DO NOT FLAG list + stack + scope into every finder prompt AND the verifier prompt. A finder without the packet manufactures convincing noise - worse than no finder.

22. **Match finder count to the diff, don't over-fan.** A docs-only or one-line change does not need 9 reviewers. Gate lenses by what the diff actually touches (`review-lenses.md` § Mode → lens routing), and on multi-minute reviews emit the "Reviewers running" line so the user knows it's working. **Tiny tier (concrete)**: diff ≤ ~30 changed lines in ≤2 files → reduced lens set (RL1 + RL3 + RL7 only), single batched verifier pass, no Codex finder.
