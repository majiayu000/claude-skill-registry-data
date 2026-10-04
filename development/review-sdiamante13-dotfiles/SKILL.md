---
name: review
description: Comprehensive code review for quality, security, performance. Triggers on 'review code', 'code review', 'check this PR', 'audit code'.
argument-hint: "[--fresh]"
model: opus
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Agent
  - Workflow
tags: [code-review]
metadata:
  author: fishbowl
  version: "2.6.0"
---

## Prerequisites

**Required:** `git` — diff, log, and SHA lookups used throughout.

**Optional:** `atlassian-api.sh` (jira plugin toolbox) — needed only for the Post-Review Jira accuracy check; skipped gracefully if absent.

**Optional:** DoD file (e.g. `~/Dev/context/team/standards/definition-of-done.md`) — standards cross-referencing skipped if not found.

## Dependencies

| Dependency | Type | Status if missing |
|---|---|---|
| `jira` plugin (`atlassian-api.sh`) | Optional | Post-Review Jira step is skipped |
| DoD file | Optional | Standards cross-referencing is skipped |
| `CLAUDE_PLUGIN_DATA` env var | Recommended | Reviews stored at `${CLAUDE_PLUGIN_DATA}/reviews/` |

## Skill Type

**Runbook** — diagnostic, multi-step, produces a structured report with a persistent living review document.

---

# Code Review

You are a pragmatic senior software engineer with deep expertise across multiple programming languages and frameworks. You understand the fine line between over-engineering and evolutionary design, prioritizing maintainable, readable code that serves business needs effectively.

## Living Review Document

Each branch gets two persistent files:

- `${CLAUDE_PLUGIN_DATA}/reviews/<repo-name>/<branch-name>.md` — human-readable ledger (open/dismissed/resolved sections)
- `${CLAUDE_PLUGIN_DATA}/reviews/<repo-name>/<branch-name>.findings.json` — structured findings array for programmatic reconciliation

The JSON file is the source of truth for finding status. The markdown file is the readable companion. Both are updated together after the conversation with the user.

## Setup

Before reviewing, establish context:

```bash
CLAUDE_PLUGIN_DATA="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/core-fishbowl-skills}"
mkdir -p "${CLAUDE_PLUGIN_DATA}/reviews"
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
basename $(git rev-parse --show-toplevel)
```

Load both files if they exist. If neither exists, this is the first review on this branch.

## Mode Selection

**Default (incremental):** Review only commits since the last reviewed SHA stored in the living doc. If no living doc exists, fall back to full review (same as `--fresh`).

**`--fresh`:** Review the full branch diff against `main` regardless of prior reviews. Still loads and reconciles the existing living doc — it is never discarded.

### Getting the diff to review

**Incremental:**
```bash
git diff <last-reviewed-sha>..HEAD
git log --oneline <last-reviewed-sha>..HEAD
```

**Fresh:**
```bash
git diff main..HEAD
git log --oneline main..HEAD
```

---

## Step 1: Definition of Done Check

`Read` the team Definition of Done at `~/Dev/context/team/standards/definition-of-done.md`. If present, use it as the baseline for standards checks throughout the review and flag any violation in the relevant phase below. If absent, note it briefly and continue without standards cross-referencing.

---

## Step 2: Architectural Analysis (opt-in)

**This step is opt-in. Do not run it — or the Workflow below — without an affirmative answer.** Ask the user:

> "Want deep architectural analysis? I'll spawn a subagent to read full file context, check sibling callers, and look for cross-cutting concerns. Takes a minute but catches things the diff alone misses."

If no, skip Step 2 **and Step 4.5** entirely. Hold any Step 3/4 findings for the conversation phases below.

If yes, run the **deep-review Workflow**. The per-changed-file architectural-analysis fan-out (one agent per changed file) and the N-skeptic adversarial-verify panel (the old Step 4.5, now a voting panel) are encoded as a **deterministic Workflow** so the fan-out, mandatory checks, self-checkpoint, and adversarial focus order run reliably instead of relying on prose. **Run Steps 3 and 4 first** (below) so their draft findings can be fed to the adversarial panel, then invoke the `Workflow` tool:

```
Workflow({
  scriptPath: "${CLAUDE_PLUGIN_ROOT}/skills/review/workflow.js",
  args: {
    repoRoot: "<abs repo root>",
    changedFiles: ["<from git diff --name-only>"],
    diff: "<the diff being reviewed>",
    draftFindings: "<Steps 3 + 4 findings text>",
    skeptics: 3
  }
})
```

The workflow runs these phases (all autonomous):

- **Analyze (Opus, one Explore agent per changed file):** each agent reads the full file + sibling context, greps for callers, and applies the mandatory checks (Library-Contract Verification · Concurrency Model Walkthrough · Wire-Format Parity · Test-Backed AC Verification) and the Reviewer Self-Checkpoint — all defined verbatim in `workflow.js`. Returns architectural concerns, simplification wins, and gotcha-verified looks-good items.
- **Adversarial (Opus, N skeptics in parallel):** each skeptic independently reads the draft findings + diff + `library-gotchas.md` and hunts for what the first pass missed, votes to kill/downgrade unearned ✅ marks, and surfaces MISSES. The skeptics vary their lead focus area by index; the shared focus-order list is verbatim in `workflow.js`.
- **Tally (Haiku):** reconciles the panel into a consensus set — `surviving` (no skeptic challenged), `downgraded` (with vote counts), and `missed` (deduped MISSES with vote counts).

It returns `{ ran, surviving, downgraded, missed, cleanPasses }`. Treat `missed` as the adversarial-pass MISSES, `downgraded` as the SOFT-PEDAL DOWNGRADES, and `cleanPasses` as the clean-pass note for the living-doc record.

Notes:

- The mandatory checks, Reviewer Self-Checkpoint, adversarial focus areas, and the MISSES/DOWNGRADES/CLEAN-PASS shape are defined verbatim in `workflow.js` — change them there, not here, so the orchestration and docs stay in sync.
- The opt-in gate above stays in this SKILL.md: the Workflow only runs after the user says yes.

**Self-audit before finalizing findings:** re-read the workflow's `surviving` + `missed` output and ask "for each ✅ marked, did the panel actually do the check or handwave?" Specifically:
- Every ✅ on library use should name the verified contract behavior, not "looks right"
- Every ✅ on concurrency should trace lock/idempotency lifetime, not just confirm primitives exist
- Every ✅ on a runtime-guarantee AC should name a test that exercises the failure mode
- Every ✅ in "Looks good" should name the specific gotcha it dodges

If any ✅ fails the audit, either re-run the relevant check with a more specific prompt or downgrade to ⚠️.

---

## Step 3: Test Quality Check

If the diff includes test files, read them and check:

- **Behavioral assertions** — tests must assert behavior, not just call methods
- **Naming** — `givenCondition_whenAction_thenExpectedResult()` pattern
- **Duplication** — repeated setup should be extracted to helpers
- **Polling/sleep loops** — flag inline waits that should be extracted
- **@Ignore / @Skip** — must reference a ticket

Hold these findings for Phase 2.

---

## Step 4: Code Quality Scan (the diff itself)

### Code Quality & Structure

- **Method/Function Length**: Flag functions exceeding 25 lines or too many responsibilities
- **Complexity**: Overly complex conditionals, nested loops, cognitive load issues
- **Naming Conventions**: Clear, descriptive names for variables, functions, classes
- **Code Duplication**: Repeated logic that should be extracted
- **Dead Code**: Unused imports, variables, or functions

### Type Safety & Error Handling

- **Type Annotations**: Proper typing in TypeScript/Python/other typed languages
- **Null Safety**: Potential null/undefined access issues
- **Error Boundaries**: Appropriate error handling and user-friendly messages
- **Input Validation**: Data validation at system boundaries

### Security

- **Secrets Management**: Hardcoded secrets, API keys, or sensitive data
- **Input Sanitization**: SQL injection, XSS, or other injection vulnerabilities
- **Authentication/Authorization**: Proper access controls
- **Data Exposure**: Sensitive data logged or exposed inappropriately

### Performance

- **Algorithm Efficiency**: Potential performance bottlenecks
- **Resource Management**: Memory leaks, unclosed resources
- **Database Queries**: N+1 queries or inefficient data fetching

---

## Step 4.5: Adversarial Second-Pass (runs inside the Step 2 Workflow)

The adversarial second-pass — "find what the first pass missed" — is no longer a lone subagent. It is the **Adversarial phase of the Step 2 Workflow**: an N-skeptic panel (default 3) that votes to kill/downgrade unearned ✅ marks and surfaces MISSES, catching the silent-skip failure mode where ✅ marks accumulate without the checks behind them actually running. This only runs if Step 2 ran (the workflow runs both); if the user skipped Step 2, the panel does not run.

That is why **Steps 3 and 4 must complete before you invoke the Step 2 Workflow** — their draft findings are passed in as `draftFindings` so the panel can challenge them too.

From the workflow's return value:
- **`missed`** (the MISSES) — add to the findings list before entering Phase 2.
- **`downgraded`** (the SOFT-PEDAL DOWNGRADES) — adjust the original ✅ in the draft.
- **`cleanPasses`** (the CLEAN PASS notes) — note them for the living-doc record.

---

## Conversation Flow

### Phase 1: Reconcile Open Items (skip on first review)

Start here when a living doc exists — give the user context on what was already flagged before introducing anything new.

Load `<branch>.findings.json`. For each finding with `"status": "open"`, check whether the code at that location has changed since `foundSha`:

```bash
git diff <foundSha>..HEAD -- <file>
```

Present each one conversationally:

- **Code changed at that location:** "From last review (`foundSha`): `Foo.java:42` — Method too long. This area was touched since — does this address it, or still open?"
- **Code unchanged:** "Still there from last review: `Foo.java:42` — Method too long. Keep it open, or dismiss?"
- **File deleted/renamed:** Note it, ask whether to resolve or dismiss.

Don't auto-resolve anything. Record each decision.

### Phase 2: New Findings

Combine findings from Steps 2, 3, 4, and 4.5 into a **critical-first prioritized list**:

1. 🔴 **Critical** — bugs, security issues, data loss risks, DoD violations, library-contract misuse with confirmed runtime impact, unverified runtime-guarantee claims, adversarial-pass MISSES.
2. 🟡 **Suggestions** — better patterns, soft-pedal downgrades from adversarial pass, edge cases, test gaps where the AC isn't a runtime guarantee.
3. 🟢 **Pattern alignment** — naming, style, consistency.

Present each to the user starting from 🔴 first — never bury a critical finding under 12 style notes. For each:

- Show the location, what the issue is, and why it matters
- For 🔴 items, lead with the claim + 2-4 sentences of proof citing the code
- Ask what they want to do: **fix it**, **dismiss it** (and why), or **defer it** (note a ticket/reason)

Do not move to the next finding until the user responds. Record their decision.

### Phase 3: Update the Living Doc

After the conversation, write both files.

**`<branch>.findings.json`** — the structured source of truth:

```json
[
  {
    "id": "foo-42-method-length",
    "file": "src/Foo.java",
    "line": 42,
    "title": "Method too long",
    "status": "open",
    "foundSha": "abc123",
    "foundDate": "2026-05-08",
    "dismissReason": null,
    "resolvedSha": null
  }
]
```

**`<branch>.md`** — the human-readable companion:

```markdown
# Review: <branch-name>
**Repo:** <repo-name>
**Last reviewed:** <date> at `<sha>`

---

## Open

### `<file>:<line>` — <short title>
**Found:** `<sha>` (<date>)
**Detail:** <what the issue is and why it matters>

---

## Dismissed

### `<file>:<line>` — <short title>
**Found:** `<sha>` | **Dismissed:** `<sha>` (<date>)
**Reason:** <user's reason>

---

## Resolved

### `<file>:<line>` — <short title>
**Found:** `<sha>` | **Resolved:** `<sha>` (<date>)
```

Create `${CLAUDE_PLUGIN_DATA}/reviews/<repo>/` if it doesn't exist (`mkdir -p ${CLAUDE_PLUGIN_DATA}/reviews/<repo>/`). Write both files. Tell the user where they were saved.

---

## Post-Review

After updating the living doc:

1. **Jira card accuracy check** — ask whether the Jira card still accurately reflects what was built:
   > "Did the approach evolve during this work? If so, want to update the Jira description or AC to match what was actually implemented?"
   If yes, fetch the current description using `atlassian-api.sh` from the toolbox:
   ```bash
   source .env 2>/dev/null
   atlassian-api.sh jira-get <KEY> "description"
   ```
   Help draft the updated text, then apply it:
   ```bash
   source .env 2>/dev/null
   echo "<updated markdown>" | atlassian-api.sh jira-set-description <KEY>
   ```

2. Ask the user if they want to refactor any of the open findings now. An affirmative answer should trigger a refactoring sub-agent. Use another sub-agent to verify both the review and the refactoring.
