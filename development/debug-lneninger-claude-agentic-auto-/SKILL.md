---
name: debug
description: "Systematic 4-phase debugging protocol — REPRODUCE → ISOLATE → HYPOTHESIZE → VERIFY before any fix is written. Forces root-cause analysis instead of symptom patching. Writes findings to .claude/debug-notes-<slug>.md. Use when: user says /debug, 'debug this', 'why is X failing', 'fix this bug', or when a symptom is reported. Mandatory for bugs under any root named by the safety-critical.roots, auth.roots or migration.root slots of .claude/project-profile.md. Produces a HANDOFF suitable for dotnet-backend-architect or angular-senior-dev to implement the fix."
user_invocable: true
---

# /debug — Systematic Debugging Protocol

When invoked, work through four phases in order. **No fix code is written until Phase 4 completes.** The goal is to identify the *root cause* (a specific invariant violation or incorrect assumption) — not just make the symptom go away.

## Context — why this skill exists

Bug fixes that skip root-cause analysis either (a) patch the symptom and leave the bug to resurface elsewhere, or (b) introduce new bugs because the "fix" was guessed. For a trading app where bugs can cost real money (missed fills, duplicate orders, incorrect PnL), the cost of a shortcut fix is outsized. This skill enforces the discipline.

## Step 0: Capture the bug report

**Work in a worktree.** In the main checkout, run `/task` first: it cuts and enters a worktree, and the main-checkout guard refuses the scratch file below and every later edit in the shared tree. `py -3 .claude/scripts/flat_worktree.py --describe` reports `current_tree`; `main-checkout` means stop and run `/task`.

Ask the user if not already stated:

1. **Symptom** — what does the user observe? (error message, wrong value, missing behavior, crash, hang)
2. **Trigger** — what action reproduces it? (click X, run strategy Y, data Z, schedule W)
3. **Expected** — what should happen instead?
4. **Scope** — always / sometimes / only on live / only on paper / only for user X / only after deploy on date D

Open a scratch file at `.claude/debug-notes-<short-slug>.md` and write these four fields as a header block. Every subsequent phase appends to this file.

---

## Phase 1: REPRODUCE

The bug must be reproducible deterministically before any hypothesis is valid. An intermittent bug with no repro case is not debuggable — it's guessable.

### 1a. Find or write a repro

- **Deterministic repro** — specific input + specific sequence always produces the symptom.
- **Probabilistic repro** — symptom appears in N of M runs with the same input.
- **Known-intermittent** — races, GC timing, network flakes. Document the frequency.

### 1b. Capture the repro evidence

In the scratch file, append:

```
## Phase 1: REPRODUCE
- Repro type: deterministic | probabilistic (X of Y) | intermittent
- Minimum steps:
  1. <step>
  2. <step>
  ...
- Observed symptom: <exact error / log line / screen state>
- Environment: local | staging | prod, paper | live, .NET debugger attached? SQL LocalDB state?
- First occurrence: commit SHA / date if known
- Captured evidence: <log paths, screenshot paths, stack trace>
```

### 1c. Halt if you cannot reproduce

If the bug can't be reproduced, the skill STOPS here. Options:

- Ask the user for more detail (exact input, timing, env state).
- Add instrumentation (structured logs, SignalR hub trace) and wait for the symptom to recur.
- Treat as "unreproducible — monitoring" and close the debug session.

**Never proceed to Phase 2 without a repro.** Fixing a bug you can't reproduce means you can't prove the fix worked.

---

## Phase 2: ISOLATE

Narrow the failure to the smallest possible code region. The goal of this phase is to name the single function, line, or interaction where the invariant breaks.

### 2a. Pick an isolation technique based on the bug type

| Bug type | Technique |
|---|---|
| Regression (worked, now broken) | `git bisect` between last-good and first-bad SHA |
| Unknown code path | Add structured logging on entry/exit of suspected services, replay the repro |
| Frontend rendering / signal | Open DevTools, set breakpoints on signal setters, replay |
| SignalR message loss | Tail both hub and client with correlation IDs |
| Async / timing | Add stopwatch logs around the suspect `await`s — look for >N ms waits |
| SQL perf / wrong result | Capture the actual SQL + parameters via EF logging, run manually |
| External API (any third-party service client) | Capture the exact request and response — don't infer, observe |
| Memory / GC / leak | `dotnet-counters` + `dotnet-gcdump` |

### 2b. Drill until the breakpoint is a single scope

Keep asking: "Is the state wrong *entering* this function, or does this function produce the wrong state?" Repeat inward until you can name the function/line where the state first becomes wrong.

### 2c. Append to the scratch file

```
## Phase 2: ISOLATE
- Technique used: <bisect | logging | debugger | DB trace | ...>
- Suspect region (narrowest): <file.cs:line or file.ts:line>
- State-entering-function: <values of relevant vars>
- State-leaving-function: <values — the divergence from expected>
- Upstream producers of the wrong state: <list if multi-step corruption>
```

### 2d. Halt if isolation fails

If you can't narrow below "somewhere in module X", the fix will be a shotgun. Return to Phase 1 and capture more evidence (more logs, different repro inputs).

---

## Phase 3: HYPOTHESIZE

Name the root cause as a specific invariant that is being violated. A good hypothesis is falsifiable — you can design a test that will disprove it if wrong.

### 3a. Write the hypothesis

In the scratch file:

```
## Phase 3: HYPOTHESIZE
- Root cause (one sentence): <specific invariant violated>
  Good example: "Record IDs from the upstream service are 64-bit but the DB column is int32, so records with IDs > 2^31-1 fail to persist and the retry logic silently drops them."
  Bad example: "The order persistence is broken."
- Why this explains the symptom: <causal chain>
- Predictions this hypothesis makes:
  - If true, we should ALSO see: <behavior A>
  - If true, we should NOT see: <behavior B>
  - If false, the alternative is: <alternative hypothesis>
```

### 3b. Rank against alternatives

For non-trivial bugs, list 2-3 alternative hypotheses and rank by likelihood. Pick the most likely to verify first. Keep the alternatives documented — if Phase 4 disproves the top hypothesis, you already have your next candidate.

### 3c. Avoid these hypothesis anti-patterns

- **"It's probably a race condition"** without naming the two participants racing → not a hypothesis, a shrug.
- **"The library has a bug"** — almost never true. Assume your usage is wrong until proven otherwise.
- **"Something in config"** — name which setting and which value.
- **Hypothesis that's impossible to disprove** — if no test can fail when you're wrong, you don't have a hypothesis, you have a feeling.

---

## Phase 4: VERIFY

Prove the hypothesis with a targeted test or observation BEFORE writing the fix. If the hypothesis is wrong, you'll catch it here instead of after deploy.

### 4a. Design the verification

Pick the cheapest observation that would disprove the hypothesis:

- **Unit test that fails** — write a test that encodes the hypothesis. If the test passes when you expect it to fail, the hypothesis is wrong.
- **Targeted logging** — instrument the one line you predicted would show the wrong value; run the repro; check.
- **Direct database query / API call** — inspect the actual state instead of trusting an abstraction.
- **Counter-example search** — if the hypothesis is "nulls aren't handled", find a real null that triggers the symptom.

### 4b. Execute the verification

Run the test / run the repro / execute the query. Capture the output.

### 4c. Evaluate

- **Hypothesis confirmed** — the observation matches the prediction. Proceed to "Write the fix".
- **Hypothesis disproven** — the observation contradicts the prediction. Return to Phase 3 with the next candidate. Do NOT adjust the hypothesis to fit the data (that's how bad fixes happen).

### 4d. Append to the scratch file

```
## Phase 4: VERIFY
- Verification design: <what test / what query / what log>
- Observation: <actual output>
- Verdict: CONFIRMED | DISPROVEN | INCONCLUSIVE
- If disproven: falling back to hypothesis <next candidate>
```

---

## After Phase 4: Write the fix (via the right implementer)

With the root cause confirmed, hand off to the appropriate implementer agent:

```
TASK: Fix <specific root cause from Phase 3>.
  The failing verification in `.claude/debug-notes-<slug>.md` Phase 4 is the authoritative repro.
CONTEXT: <one-line symptom summary from Phase 0>
FILES: <the narrowest region from Phase 2>
CONSTRAINTS:
  - Make the minimal change that satisfies the verification
  - Do NOT change behavior unrelated to the root cause
  - If a new invariant needs to be enforced, add an assertion / guard
PRIOR_FINDINGS:
  debug_notes_path: .claude/debug-notes-<slug>.md
  root_cause: <one sentence>
  verification_type: <unit test | log observation | db query | ...>
```

Choose the agent by area:

- Backend C# → `dotnet-backend-architect`
- Angular frontend → `angular-senior-dev`
- Third-party service integration → the project's own integration agent for that service, if it declares one
- Ingestion jobs → `ingestion-data-architect`
- SQL / index / migration perf → `dotnet-backend-architect` with `/sql-server-patterns` skill (+ `sql-performance-reviewer` to audit)
- Docker / container lifecycle, Kubernetes, Terraform, Bicep or cloud infrastructure → `cloud-engineer` (active when `cloud.providers` is set in the project profile). It refuses to run without an approved contract: pass `PRIOR_FINDINGS` with the `contract_path` and `contract_status: approved` when one exists. When none exists, do not invoke the agent: say a contract is required first and run `/design-first`.
- LLM pipeline / Python sidecar → `python-ai-developer` or `llm-training-engineer`

### Safety-critical path bugs require escalation

If the root cause sits under a root named by the `safety-critical.roots` slot of `.claude/project-profile.md`, the implementer's HANDOFF must recommend the project's live-action safety reviewer next. Do NOT let a fix in these paths ship without that review.

## After the fix: close the loop

1. Re-run the Phase 4 verification — it should now pass (or the failing test should now be green).
2. Run the original Phase 1 repro — the symptom must be gone.
3. Invoke `/verify-before-done` to run the build + test gauntlet.
4. Update the scratch file with a final section:

```
## Resolution
- Fix summary: <one sentence>
- Files changed: <paths>
- Test added: <path>  # for regression prevention
- Verified: <date/time>
```

5. Move `.claude/debug-notes-<slug>.md` to `.claude/debug-history/` if you want to keep the audit trail.

## Anti-patterns (halt and restart if you catch yourself doing these)

- **Guess-and-check fixing** — changing code hoping the symptom disappears. That's not debugging.
- **"I'll just add a try/catch"** — catches the symptom but the root cause still corrupts state. Only acceptable if the root cause is "this external call can legitimately throw and we must degrade gracefully" AND you've written the hypothesis down.
- **Skipping Phase 1** — fixing a bug you can't reproduce means you can't prove the fix worked. Future-you will curse present-you.
- **Skipping Phase 4** — implementing the fix based on an unverified hypothesis wastes everyone's time when the hypothesis was wrong.
- **Silent hypothesis mutation** — adjusting the hypothesis to match the data without noticing. Keep the original hypothesis documented and add a new one if needed.
- **Blaming the library / framework** — 99% of the time it's your usage. Verify library behavior is actually what you claim before blaming it.

## When to NOT use this skill

- **Obvious typo / one-line fix where the root cause IS the typo** — you don't need 4 phases to fix a misspelled property name that's throwing a runtime error.
- **Exploratory performance tuning** — use profiler output + hypothesis directly; this skill's phase separation adds overhead for unclear wins.
- **UI polish / CSS tweaks** — use `ui-ux-designer` directly.
- **Build / compile errors** — the error message usually IS the root cause. Fix and move on.

## Skill interactions

- Usually runs **before** `/tdd-first` — Phase 4's verification often becomes the first test in the RED phase, guaranteeing regression protection.
- Always runs **before** any implementer agent is invoked — the 4 phases are the prep work that turns an unclear bug report into an actionable implementation task.
- Integrates with `test-strategy-critic` — if Phase 4's verification is a test, `test-strategy-critic` can assess whether it actually proves the root cause.
