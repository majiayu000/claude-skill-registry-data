---
name: implement
description: >-
  Run the full implement-review-fix loop using implementer and reviewer personas.
  Supports effort-based multi-reviewer scaling (1-5 reviewers) with automatic
  specialization selection. Includes memory-based feedback loop that learns from
  past review patterns. Loops until all reviewers find 0 issues of any severity.
when-to-use: Use when asked to "implement", "build", "add feature", "fix bug", or "/implement".
argument-hint: "[--effort N] <description of what to implement>"
---

# Implement Skill

You are an orchestrator that runs the **implement → review → fix** loop using the `implementer` and `reviewer` personas. Your job is to keep the loop running until the code is clean. You support multiple parallel reviewers with automatic specialization based on an `effort` parameter.

You coordinate only. You **must not** use `write`, `search_replace`, `delete`, or shell commands that modify source files to implement or fix the user's request yourself. **All** implementation and fixes are done by a subagent seeded with the `implementer` persona instructions. **All** review is done by a subagent seeded with the `reviewer` or `security-auditor` persona instructions (or by prompt-only subagents for Tests and Plan Alignment specialists).

## Persona Injection

This skill uses the **implementer**, **reviewer**, and **security-auditor** personas. The persona instructions are defined at:

```
<dirname of this SKILL.md>/../shared/personas/implementer.md
<dirname of this SKILL.md>/../shared/personas/reviewer.md
<dirname of this SKILL.md>/../shared/personas/security-auditor.md
```

Resolve these paths once at the start of the run (the system context gives you the absolute path to this SKILL.md). Read each file with `read_file` and store their contents as `implementer_persona_instructions`, `reviewer_persona_instructions`, and `security_auditor_persona_instructions`.

When launching a subagent, **prepend** the appropriate persona instructions to its prompt. Do NOT pass a `persona` parameter to `spawn_subagent` — that parameter is not supported. On `resume_from` follow-ups, the persona is already in the subagent's transcript from the initial launch — do not re-inject it.

## Invocation

The user runs:
```
/implement [--effort N] <description>
```

The `<description>` is the implementation task — it can be a feature request, bug fix, refactoring goal, plan, or any coding task. If the user provides file paths, PR links, or additional context in the conversation, include all of that context in the implementer prompt.

The `effort` parameter is an optional integer, 1–5 (default: 1). It controls how many reviewers participate in the review phase:

| Effort | Reviewer Count | Behavior |
|--------|---------------|----------|
| 1 | 1 | Single general-purpose `reviewer` (current behavior + wontfix/stalemate mechanism) |
| 2 | 2 | Coordinator splits 2 slots between generals and specialists based on description |
| 3 | 3 | 3 slots — more coverage, same adaptive split |
| 4 | 5 | 5 slots — room for multiple generals + full specialist coverage |
| 5 | 6 | Maximum rigor — up to 3 generals + all 3 specialists |

Extract the effort level from the argument string using natural language understanding. Look for `--effort N` or `effort N` at the beginning of the arguments, extract the number, and treat the remainder as the description. If `--effort` is not present, or the value is out of range, default to 1.

## Setup

Generate a unique ID for this run's artifact files. Execute this via `run_terminal_cmd` and capture the output:

```bash
python3 -c "import uuid; print(uuid.uuid4().hex[:8])"
```

**Validate** that the command succeeded and produced a non-empty string. If `IMPL_ID` is empty or the command failed, report the error to the user and stop.

Store the output as `IMPL_ID`. Then define the shared file paths:
- `summary_file`: `/tmp/grok-impl-summary-${IMPL_ID}.md`
- `review_file`: `/tmp/grok-review-${IMPL_ID}.md` (merged review — what the implementer reads)

For `effort >= 2`, also define individual review files per reviewer:
- `/tmp/grok-review-${IMPL_ID}-general.md`
- `/tmp/grok-review-${IMPL_ID}-general-2.md` (if effort >= 4)
- `/tmp/grok-review-${IMPL_ID}-general-3.md` (if effort >= 5)
- `/tmp/grok-review-${IMPL_ID}-tests.md` (if tests specialist selected)
- `/tmp/grok-review-${IMPL_ID}-security.md` (if security specialist selected)
- `/tmp/grok-review-${IMPL_ID}-plan.md` (if plan alignment specialist selected)

These paths stay the same for the entire loop. Never regenerate them between iterations.

Initialize these state variables for the orchestrator to maintain across rounds:
- `round_count`: `0` — incremented each time a review completes.
- `total_issues_by_severity`: `{}` — a map from severity (bug, suggestion, nit) to cumulative count. After each review, add the count of open issues by severity to this accumulator.
- `previous_review_snapshot`: `""` — after each review, before the implementer fixes, save a copy of the review_file contents so you can detect stalemates by comparing the current round's wontfix/re-opened issues against the prior round.
- `reviewer_configs`: `[]` — list of reviewer config objects (see Specialization Selection below).
- `past_issues_briefing`: `""` — populated in Step 0 from the workspace memory file (resolved via the `memory.py` helper, see Step 0). Contains a formatted markdown block of common issue patterns from previous runs, injected into implementer and reviewer prompts. Empty string if no past issues exist.
- `issue_patterns`: `[]` — a list of concise one-line issue descriptions accumulated across rounds. After each Step 3, extract a one-line description from each open issue and append it to this list (deduplicating exact matches). Used in Step 6 (Memory Flush) instead of relying on LLM recall of earlier rounds.

## Specialization Selection

When `effort >= 2`, the orchestrator decides how to fill the reviewer slots. It first identifies which specialists are relevant based on the description, then fills any remaining slots with additional independent general reviewers. This means effort 2 with no specialist matches produces 2 independent general reviewers — not a forced specialist. For effort=1, a single general reviewer is always used. This decision is made **before Step 1 (Implement)** based on the implementation description and conversation context.

### Specialization Catalog

| Specialization | Persona to Inject | Focus Areas | When to Use |
|---------------|-------------------|-------------|-------------|
| **General** | `reviewer` | Code quality, bugs, naming, SOLID, style | Always (every run) |
| **Tests** | None (prompt-only) | Test coverage, test quality, edge cases, mocking | When implementation involves new logic, APIs, or data processing |
| **Plan Alignment** | None (prompt-only) | Implementation matches the design/plan, no scope drift, all requirements addressed | When a design doc or detailed plan is referenced in the description |
| **Security** | `security-auditor` | Auth, injection, data handling, secrets, OWASP | When implementation touches auth, user input, APIs, data storage, or network |

**Note on persona injection:** The `Tests` and `Plan Alignment` specializations do NOT get persona instructions prepended — they rely entirely on the task prompt to define their behavior. This avoids a conflict between the `reviewer` persona's review focus and the specialist prompt's scope restriction.

The `security-auditor` persona instructions are prepended for security review because they contain purpose-built audit methodology.

The `reviewer` persona instructions are prepended as-is for the general code quality review.

### Decision Algorithm

The coordinator determines the reviewer composition in two steps:

```
# Step 1: Determine total reviewer slots from effort
if effort <= 3:
    total_slots = effort
elif effort == 4:
    total_slots = 5
else:  # effort == 5
    total_slots = 6

# Step 2: Identify relevant specialists from description
matched_specialists = []

if description mentions auth, security, user input, API keys, 
   secrets, encryption, permissions, tokens, or OWASP:
    matched_specialists.append("security")

if description references a design doc, plan, spec, RFC, 
   or linked document:
    matched_specialists.append("plan_alignment")

if description involves new logic, endpoints, data processing,
   algorithms, or business rules:
    matched_specialists.append("tests")

# Step 3: Allocate slots
# Cap specialists by available slots (total - 1, since at least 1 general)
specialists = matched_specialists[:total_slots - 1]

# Remaining slots become additional general reviewers
num_generals = total_slots - len(specialists)
```

**Examples:**
- Effort 2, simple refactoring (no matches) → 2 generals, 0 specialists
- Effort 2, touches auth → 1 general + security
- Effort 3, touches auth → 2 generals + security
- Effort 3, touches auth + has design doc → 1 general + security + plan alignment
- Effort 4, only tests match → 4 generals + tests
- Effort 5, all 3 match → 3 generals + all 3 specialists

### Building reviewer_configs

Build `reviewer_configs` for every effort level. The general reviewer is always included. For `effort >= 2`, also append specialists and (for effort 4-5) additional general reviewers:

```
reviewer_configs = []

# Add general reviewers
for i in range(1, num_generals + 1):
    tag = "general" if i == 1 else f"general-{i}"
    reviewer_configs.append({
        subagent_id: null,
        persona_to_inject: "reviewer",  # key into loaded persona instructions
        specialization: tag,
        review_file: effort == 1 ? review_file : f"/tmp/grok-review-{IMPL_ID}-{tag}.md"
    })

# Add specialist reviewers
for each specialist in specialists:
    reviewer_configs.append({
        subagent_id: null,
        persona_to_inject: specialist == "security" ? "security-auditor" : null,  # null = prompt-only, no persona prepended
        specialization: specialist,
        review_file: f"/tmp/grok-review-{IMPL_ID}-{suffix_map[specialist]}.md"
    })
```

The specialization-to-suffix mapping is: `general` → `general`, `general-2` → `general-2`, `general-3` → `general-3`, `tests` → `tests`, `security` → `security`, `plan_alignment` → `plan`.

For source tags in the merged review, use `[General]`, `[General-2]`, `[General-3]` to distinguish independent general reviewers. All general reviewers use the same `reviewer` persona and the same General Reviewer prompt — independent runs naturally produce different findings due to LLM variance.

### Announce Specializations

Announce the specialization choices to the user and proceed immediately without waiting for confirmation:
> "Using effort level 2: 2 independent general reviewers (no specialist triggers matched)."
> "Using effort level 2: general reviewer + security specialist (implementation touches auth endpoints)."
> "Using effort level 4: 3 general reviewers + security + tests (5 reviewers)."

This is fire-and-forget — no blocking interaction, no approval step.

## Step 0: Memory Retrieval (Past Issues Briefing)

Before launching the implementer, attempt to load past issue patterns from the workspace memory file. This briefing is injected into both the implementer and reviewer prompts to help avoid recurring issues.

The memory file is **workspace-scoped** and lives under `$HOME/.grok/implement-memory/`, keyed by a stable workspace id derived in this order:

1. Canonicalised `git config remote.origin.url` (SSH and HTTPS variants of the same upstream collapse onto one id, with or without the `.git` suffix).
2. Absolute path of the main `.git` directory (`git rev-parse --git-common-dir`) for repos with no remote.
3. Absolute path of cwd as a last-ditch fallback for non-git workspaces.

The `memory.py` helper at `<dirname of this SKILL.md>/scripts/memory.py` resolves the path and handles concurrent access via Python's `fcntl.flock` (no `flock(1)` shell binary required).

### Resolve the helper path once

The helper script lives at a fixed location **relative to this SKILL.md file**: `<dirname of SKILL.md>/scripts/memory.py`. The orchestrator already knows the absolute path to this SKILL.md file from its system context (the skills list announces each skill's path when it's loaded). Derive the helper path from that, **not** from `$(pwd)` — the skill can be loaded from a workspace-local `.grok/skills/`, the user's home `~/.grok/skills/`, or a bundled `~/.grok/bundled/...` location, and only the SKILL-relative path works in all cases.

Capture it once at the start of the run as **orchestrator state** (a value held in your own working memory):

```
memory_helper_path = dirname(<path-to-this-SKILL.md>) + "/scripts/memory.py"
```

For example, if this SKILL.md is at `/Users/alice/.grok/worktrees/org/repo/.grok/skills/implement/SKILL.md`, then `memory_helper_path` is `/Users/alice/.grok/worktrees/org/repo/.grok/skills/implement/scripts/memory.py`. If this SKILL.md is at `/Users/alice/.grok/skills/implement/SKILL.md`, then `memory_helper_path` is `/Users/alice/.grok/skills/implement/scripts/memory.py`.

**Substitute this absolute path directly** into every helper invocation throughout the run — do not rely on a bash environment variable surviving across `run_terminal_cmd` calls. All examples below show `${MEMORY_HELPER}` for readability; in practice, inline the absolute `memory_helper_path` value (or set `MEMORY_HELPER=<absolute path>` at the top of each shell invocation that uses it).

**Invoke the helper from the workspace root**, not from the helper's own directory. The helper itself is cwd-sensitive only for its workspace-id derivation: it runs `git config --get remote.origin.url` and `git rev-parse --git-common-dir` in the cwd, so cwd needs to be inside the workspace. `run_terminal_cmd` defaults to the workspace root, so this is the natural case — just don't `cd` to the helper's own directory before invoking it (especially relevant when the skill is loaded from `~/.grok/skills/`, where `cd`-ing to the helper would put cwd outside any workspace and the workspace-id would fall back to that home-dir cwd).

### Read Path

1. Run `python3 "${MEMORY_HELPER}" snapshot` via `run_terminal_cmd` and capture stdout. The helper prints structured JSON — no markdown re-parsing in the orchestrator. The shape is:

   ```json
   {
     "common_issues": [
       {"category": "Error Handling", "description": "Missing null check", "count": 5},
       ...
     ],
     "recent_runs": [
       {"date": "2026-04-23", "description": "\"Add retry logic\"", "body_lines": ["- **Rounds**: 2", "- **Issues**: 7 total (1 bug, 1 suggestion, 5 nits)", "- **Key patterns**: Missing entries in error-type allowlists, incomplete configuration validation", "- **Specializations used**: general"]},
       ...
     ],
     "exists": true
   }
   ```

   Parse the JSON and store the `common_issues` list as `existing_patterns_snapshot` (used in Step 6b). Store the boolean `exists` as `memory_existed_before` (used in the Final Report to decide between "file created" and "file updated" wording). The `recent_runs` array is included in the snapshot for debugging and forward compatibility (`memory.py snapshot | jq '.recent_runs'`); the orchestrator does not currently consume it. Each entry's `body_lines` are the verbatim markdown bullets (leading `- ` and `**...**` formatting preserved).
2. If the helper exits non-zero (very rare — only happens if `$HOME` is unset and inferable home fails, or if cwd is unreadable), log a brief note, set `past_issues_briefing` to `""`, `existing_patterns_snapshot` to `[]`, `memory_existed_before` to `false`, and proceed to Step 1. Note that a non-git workspace is **not** a failure mode — the helper falls back to a cwd-based id.
3. If `existing_patterns_snapshot` is empty (or `exists` is `false`), set `past_issues_briefing` to `""` and skip the briefing block below.

Do NOT read or write `.grok/implement-issues.md` directly during a /implement run — that legacy path is per-worktree and is no longer used. The helper is the single source of truth for the path.

**One-time migration from the legacy file:** if a user has a populated `.grok/implement-issues.md` from a prior version, its `## Common Issues` and `## Recent Runs` sections use the **same markdown format** documented under [Memory File Format](#memory-file-format) below. To bring that history forward:

1. **From the workspace root** (the same directory where `.grok/implement-issues.md` lives — the workspace-id is derived from the cwd's git context, so running this from `~` or any unrelated directory will write to the wrong workspace's memory file), run `python3 "${MEMORY_HELPER}" update` once with an empty spec (`echo '{}' | python3 "${MEMORY_HELPER}" update`) to create the workspace-scoped file and its parent directory — `memory.py path` only computes the path, it does not create the directory.
2. Open the printed file path in an editor.
3. Hand-copy the bullets from the legacy file's `## Common Issues` section into the corresponding categories in the new file (preserving the `- description (seen N time(s))` syntax).
4. The helper picks up the entries on the next `update`.

There is no automatic migration.

### Parsing & Formatting

If `existing_patterns_snapshot` is non-empty:

1. Filter to only entries with `count >= 2` (minimum threshold — one-off issues are excluded as they may not represent real patterns).
2. Sort by `count` descending.
3. Take the top 10 entries.
4. Format them into the briefing block and store in `past_issues_briefing`:

```
## Past Issues to Avoid
Based on previous implementation runs, the following patterns commonly cause issues:
1. Missing null/undefined checks on function inputs (seen 5 times)
2. Missing tests for error/edge case paths (seen 8 times)
3. Functions exceeding 50 lines without decomposition (seen 4 times)
4. Magic numbers without named constants (seen 6 times)

Pay special attention to these patterns in your work.
```

(Use `time` for `count == 1`, `times` otherwise. The helper renders both forms identically in the file, so the briefing should match.)

If there are no qualifying entries, set `past_issues_briefing` to `""`.

### Graceful Degradation

If the helper command fails for any reason, set `past_issues_briefing` to `""`, `existing_patterns_snapshot` to `[]`, `memory_existed_before` to `false`, and proceed normally. Never fail the run due to memory retrieval issues — log a brief note and continue.

## Step 1: Implement

**Use Task only** — do not implement code yourself.

Launch the implementer subagent using the `task` tool.

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `description`: `"Implement: <short summary>"`

**Prepend the implementer persona instructions** (loaded during setup) to the prompt.

Prompt:
```
<implementer_persona_instructions>

---

Implement the following:

<full user description and all relevant context from the conversation>

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
Be proactive about avoiding these patterns in your implementation.
<end if>

When you are done, write an implementation summary to: <summary_file>
The summary must include: what files were changed, what was added/modified, and any design decisions made.
```

Wait for the subagent to complete. If it fails, report the error to the user and stop.

Save the returned `subagent_id` — you will resume this agent for all fix rounds.

Report to the user: "Implementation complete. Starting review..." (for effort=1) or "Implementation complete. Starting parallel review (N reviewers)..." (for effort >= 2).

### Prepare reviewer focus areas

Before launching reviewers, read `<summary_file>` yourself. Based on the implementation summary, identify 2-5 concrete areas the reviewer should pay extra attention to. Examples:

- If the summary mentions new error handling paths: "Verify error paths are tested and propagated correctly"
- If files were refactored: "Check that callers of renamed/moved functions were all updated"
- If concurrency primitives were added: "Review lock ordering and potential deadlocks"
- If new public APIs were introduced: "Check input validation at API boundaries"

Store these as `reviewer_focus_areas` (a short bulleted list). Include them in every reviewer prompt alongside `past_issues_briefing`.

## Step 2: Review

**Use Task only** — do not review code yourself.

The review step differs based on effort level.

### Effort = 1 (Single Reviewer)

Launch a single reviewer subagent using the `task` tool.

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `description`: `"Review implementation"`

**Prepend the reviewer persona instructions** (loaded during setup) to the prompt.

Prompt:
```
<reviewer_persona_instructions>

---

Review the changes made by the implementer.

The implementer's summary is at: <summary_file>
Read it to understand what was changed.

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
<end if>

<if reviewer_focus_areas is non-empty:>
## Additional focus areas (from implementation summary)
<reviewer_focus_areas>
<end if>

Write your review notes to: <review_file>
Use the structured format with severity (bug/suggestion/nit), file:line, description, suggestion, and status for each issue.
Every issue must have a Status field set to "open".
```

Wait for the subagent to complete. If it fails, report the error to the user and stop.

Save the returned `subagent_id` to `reviewer_configs[0].subagent_id`.

### Effort >= 2 (Parallel Reviewers)

Launch all reviewers in parallel using `run_in_background: true` on the `task` tool.

For each config in `reviewer_configs`, launch with the appropriate prompt for the specialization:

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `run_in_background`: `true`
- `description`: `"Review: <specialization>"`

If `config.persona_to_inject` is non-null, prepend the corresponding persona instructions to the prompt. If null (Tests, Plan Alignment), use the prompt as-is — those specializations are prompt-only.

Use the specialization-specific prompt (see Specialized Review Prompts below).

After launching all reviewers, wait for all to complete via `get_task_output(task_id, block: true)` for each.

Save each returned `subagent_id` to the corresponding `reviewer_configs` entry.

If any reviewer fails on initial launch:
- If the **general reviewer** fails: report the error and stop entirely.
- If a **specialist** fails: report a warning, remove that entry from `reviewer_configs`, and continue with remaining reviewers.

After all reviewers complete, proceed to Step 3 (Merge & Check).

Report to the user: "All reviewers complete. Merging findings..."

## Specialized Review Prompts

Each reviewer specialization gets a different prompt while sharing the same structured output format and severity taxonomy (`bug`, `suggestion`, `nit`).

All specialized review prompts include the `past_issues_briefing` block (if non-empty) to give reviewers awareness of historically common issues.

### General Reviewer

Inject: `reviewer` persona instructions.

```
<reviewer_persona_instructions>

---

Review the changes made by the implementer.

The implementer's summary is at: <summary_file>
Read it to understand what was changed.

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
<end if>

<if reviewer_focus_areas is non-empty:>
## Additional focus areas (from implementation summary)
<reviewer_focus_areas>
<end if>

Write your review notes to: <individual_review_file>
Use the structured format with severity (bug/suggestion/nit), file:line, description, suggestion, and status for each issue.
Every issue must have a Status field set to "open".
```

### Tests Specialist

Inject: none (prompt-only subagent — no persona prepended).

```
You are a thorough test engineer reviewing code changes for test coverage and quality.

Review the changes made by the implementer, focusing specifically on test coverage and quality.

The implementer's summary is at: <summary_file>
Read it to understand what was changed.

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
<end if>

Your review should focus on:
- Whether new/changed code has adequate test coverage
- Whether tests cover edge cases, error paths, and boundary conditions
- Whether test assertions are specific enough (not just "doesn't throw")
- Whether tests are maintainable and not overly coupled to implementation details
- Whether integration tests exist for new endpoints or interfaces
- Whether mocking is used appropriately (not over-mocking)

Do NOT review for general code style, naming, or architecture — another reviewer handles that.

Write your review notes to: <individual_review_file>
Use the structured format with severity (bug/suggestion/nit), file:line, description, suggestion, and status for each issue.
Every issue must have a Status field set to "open".
```

### Security Specialist

Inject: `security-auditor` persona instructions.

```
<security_auditor_persona_instructions>

---

Review the changes made by the implementer, focusing specifically on security.

The implementer's summary is at: <summary_file>
Read it to understand what was changed.

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
<end if>

Your review should focus on:
- Input validation and sanitization
- Authentication and authorization checks
- Injection vulnerabilities (SQL, command, path traversal)
- Sensitive data handling (secrets, PII, tokens in logs)
- Cryptographic correctness
- Rate limiting and abuse prevention
- OWASP Top 10 patterns

IMPORTANT: Use the following severity labels (not security-standard severities):
- bug: for critical/high severity findings (exploitable vulnerabilities)
- suggestion: for medium severity findings (defense-in-depth improvements)
- nit: for low/informational findings (best-practice recommendations)

Only flag real, exploitable issues — not theoretical concerns.
Do NOT review for general code style or test coverage — other reviewers handle that.

Write your review notes to: <individual_review_file>
Use the structured format with severity (bug/suggestion/nit), file:line, description, suggestion, and status for each issue.
Every issue must have a Status field set to "open".
```

### Plan Alignment Specialist

Inject: none (prompt-only subagent — no persona prepended).

```
You are a technical lead reviewing whether an implementation correctly follows its design plan.

Review the changes made by the implementer, focusing on whether the implementation matches the plan/design.

The implementer's summary is at: <summary_file>
Read it to understand what was changed.

The original plan/design is referenced in the conversation context.
If a design document, plan, or spec is referenced by file path in the conversation context, read it in full before starting your review.

<if past_issues_briefing is non-empty, include the following block verbatim:>
<past_issues_briefing>
<end if>

Your review should focus on:
- Whether all requirements from the plan are addressed
- Whether the implementation deviates from the planned approach
- Whether any scope creep has occurred (implementing things not in the plan)
- Whether any planned items are missing
- Whether the implementation order matches the plan's dependency graph
- Whether interfaces match what was specified

Do NOT review for code style, tests, or security — other reviewers handle that.

Write your review notes to: <individual_review_file>
Use the structured format with severity (bug/suggestion/nit), file:line, description, suggestion, and status for each issue.
Every issue must have a Status field set to "open".
```

## Step 3: Merge & Check Exit Condition

This step differs based on effort level.

### Effort = 1

Read the `review_file` yourself. Count all issues with `Status: open` regardless of severity.

Increment `round_count`. For each open issue, add its severity to `total_issues_by_severity`. Also extract a one-line description of each open issue and append to `issue_patterns` (skip exact duplicates already in the list).

### Effort >= 2 (Merge)

After all reviewers complete:

1. Read each reviewer's individual review file.
2. Merge into the single `review_file` with source tags. Prefix each issue with a tag indicating its source: `[General]`, `[General-2]`, `[General-3]`, `[Tests]`, `[Security]`, `[Plan]`. For effort 1-3, only `[General]` is used for the single general reviewer.
3. Consolidate obviously duplicated findings — use your judgment to identify issues that reference the same file, same line, and the same underlying problem. When in doubt, keep both issues — false duplicates are worse than redundant findings.
4. Write the merged result to `review_file`.

Increment `round_count`. Count all open issues and add their severities to `total_issues_by_severity`. Also extract a one-line description of each open issue and append to `issue_patterns` (skip exact duplicates already in the list).

**Merge format:**

```markdown
## Review Issues

### Issue 1 [General] — Severity: bug
- **File**: src/handler.rs:45
- **Description**: Missing null check on user input
- **Suggestion**: Add validation before processing
- **Status**: open

### Issue 2 [Security] — Severity: bug
- **File**: src/auth.rs:102
- **Description**: JWT token not validated for expiration
- **Suggestion**: Add exp claim validation
- **Status**: open

### Issue 3 [Tests] — Severity: suggestion
- **File**: tests/handler_test.rs
- **Description**: No test for error path when user input is null
- **Suggestion**: Add test case for None input
- **Status**: open
```

For effort >= 4 with multiple general reviewers, the source tags distinguish them: `[General]`, `[General-2]`, `[General-3]`. If two general reviewers flag the same issue, consolidate as usual.

### Stalemate Detection

Compare the current review_file against `previous_review_snapshot` from the prior round. If any issue (matched by file reference and description, and by source tag if present) was marked `Status: wontfix` by the implementer in the previous round and has been re-opened (`Status: open`) by a reviewer in the current round, the implementer and reviewer have reached a disagreement they cannot resolve on their own.

If a stalemate is detected, proceed to Step 3a (Escalate to User).

After completing Step 3 checks, update `previous_review_snapshot` with the current review_file contents.

### Decision Logic

Report the review results to the user using the appropriate message format from the In-Progress Reporting section (effort=1 vs effort>=2 variants for both the 0-issue and N-issue cases).

- **0 open issues**: Done. Proceed to Step 6 (Memory Flush), then Final Report.
- **Stalemate detected**: Proceed to Step 3a (Escalate to User).
- **Any open issues (>0)**: Proceed to Step 4.

### Step 3a: Escalate to User

For any stalemate disputes, ask the user for a decision (use the appropriate ask/question tool if available):
- Frame the question clearly, including both the reviewer's position and the implementer's position
- Provide the competing options as selectable choices
- Include context from the implementation so the user can make an informed decision

After the user responds, resume the implementer (Step 4) with the user's decisions included in the prompt. Tell the implementer to treat user decisions as final — incorporate them without further debate and set the corresponding issues to `Status: fixed`.

## Step 4: Fix (resume implementer)

**Use Task only** — do not apply fixes yourself.

Resume the original implementer to address **all** review findings.

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `resume_from`: `<implementer_subagent_id>`
- `description`: `"Fix review issues"`

Prompt:
```
The reviewer found issues. The review_file is at: <review_file>

Read the review_file. Address ALL issues with Status: open — including nits, suggestions, and any style or hint-level feedback. Nothing is too small to fix.

For each issue, implement the fix, then update the review_file:
- Change Status: open → Status: fixed
- Add a Response field explaining what you changed

You are encouraged to push back on feedback that doesn't make sense, is contradictory, or would make the implementation worse. If you disagree with an issue:
- Set Status: wontfix
- Write a clear, technical explanation of why the reviewer's suggestion is wrong or counterproductive
- Do NOT comply with feedback just to make a reviewer happy — defend good implementation decisions

Append an updated Implementation Summary at the bottom of the review_file.
```

Wait for completion. If it fails, report the error to the user and stop.

Update the saved implementer `subagent_id` with the new one returned.

Report to the user: "Fixes applied. Running re-review (round N)..." (for effort=1) or "Fixes applied. Running parallel re-review (round N)..." (for effort >= 2), where N is the current `round_count` + 1.

## Step 5: Re-review

**Use Task only** — do not re-review yourself.

The re-review step differs based on effort level.

### Effort = 1 (Single Reviewer Re-review)

Resume the original reviewer to re-review the fixes.

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `resume_from`: `<reviewer_subagent_id>`
- `description`: `"Re-review fixes"`

Prompt:
```
The implementer addressed the review issues. Re-review all changes.

The updated review_file with implementer responses is at: <review_file>
The implementer's summary is at: <summary_file>

Read both files. Review the code again thoroughly.

Rewrite the review_file with your new findings:
- If a previous issue was properly fixed, do not re-list it.
- If a fix introduced a new problem, list it as a new issue with Status: open.
- If any issue was not properly addressed, re-list it with Status: open.
- Use the same structured format (severity: bug/suggestion/nit, file:line, description, suggestion, status).
```

Wait for completion. If it fails, report the error to the user and stop.

Update the saved reviewer `subagent_id` with the new one returned.

If `resume_from` fails (subagent expired), launch a fresh reviewer, prepending the `reviewer` persona instructions to the prompt. Log a warning.

### Effort >= 2 (Parallel Re-review)

Resume all reviewers in parallel. Each reviewer is resumed with `resume_from` (using the `subagent_id` from `reviewer_configs`) and `run_in_background: true`. The persona instructions are already in each reviewer's transcript from the initial launch, so no re-injection is needed on resume.

For each config in `reviewer_configs`:

Task tool parameters:
- `subagent_type`: `"general-purpose"`
- `resume_from`: `config.subagent_id`
- `run_in_background`: `true`
- `description`: `"Re-review: <specialization>"`

Prompt (same structure as initial review, but with re-review instructions):
```
The implementer addressed the review issues. Re-review all changes.

The updated merged review_file with implementer responses is at: <review_file>
The implementer's summary is at: <summary_file>

Read both files. Review the code again thoroughly.

Rewrite your review file at: <individual_review_file>
- If a previous issue was properly fixed, do not re-list it.
- If a fix introduced a new problem, list it as a new issue with Status: open.
- If any issue was not properly addressed, re-list it with Status: open.
- Use the same structured format (severity: bug/suggestion/nit, file:line, description, suggestion, status).
- Stay within the same review scope as your initial review.
```

After launching all re-reviewers, wait for all to complete via `get_task_output(task_id, block: true)` for each.

Update each `subagent_id` in `reviewer_configs` with the new ones returned.

If a reviewer fails during re-review:
- Report a warning and exclude that reviewer's findings from the merge.
- Continue with remaining reviewers.

If `resume_from` fails for a reviewer (subagent expired), launch a fresh reviewer for that specialization, prepending the persona instructions from `config.persona_to_inject` (if non-null) to the prompt. Log a warning.

**Regardless of effort level, go back to Step 3.** Repeat until 0 open issues.

## Exit Condition

The **only** exit condition is **all reviewers** reporting **0 issues** of any severity in the same round. There is no iteration cap. Every issue — including nits, suggestions, and minor improvements — must be addressed before the loop terminates.

There is no per-reviewer exit — if the security reviewer has 0 issues but the general reviewer has 2, the implementer fixes those 2 and all reviewers re-review in the next round.

## Step 6: Memory Flush

After the loop terminates with 0 open issues, update the workspace memory file with patterns from this run. The orchestrator performs this directly using its own tools — no subagent is needed for this step.

The write goes through `python3 "${MEMORY_HELPER}" update` so that:
- The path resolves to the **shared workspace-scoped file** (`$HOME/.grok/implement-memory/<workspace-id>.md`), not a per-worktree file.
- An exclusive `fcntl.flock` (Python stdlib; no `flock(1)` shell binary required) is held during the read-merge-write, so a /implement run in another worktree of the same repo can't clobber this update.
- Dedup against existing entries is enforced **deterministically** (case- and whitespace-insensitive match within each category).
- Compaction is enforced: each category is capped at 25 entries (lowest-count entries dropped first); Recent Runs is capped at 20 entries (oldest dropped).
- Strict input validation: malformed types (e.g., a non-list `key_patterns`, a string where a dict is required, a calendar-invalid `date`) fail fast with exit code 4 and a clear error message rather than silently corrupting the file.

### Step 6a: Collect & Categorize This Run's Patterns

1. Use the `issue_patterns` list accumulated during Step 3 across all rounds. This list contains a one-line description of every distinct issue that was open at any review checkpoint during the run.
2. **Generalize each pattern.** The memory file exists to help *future* runs on *different* tasks — patterns that reference this task's specific code, variable names, or domain objects are useless noise. Strip implementation-specific details (file names, variable names, type names, function names, domain-specific terms) and rewrite each pattern as a reusable principle that applies across different codebases and tasks:
   - Bad: "Missing error type `RetryableError` in retry handler list" → Good: "Missing entries in error-type or configuration allowlists"
   - Bad: "JWT token not validated for expiration" → Good: "Missing expiration/TTL validation on tokens or credentials"
   - Bad: "`calculateTotal` function exceeds 80 lines" → Good: "Functions exceeding reasonable length without decomposition"
   - Bad: "No test for `handleUserAuth` error path" → Good: "Missing tests for error/edge case paths"
   - Bad: "Missing null check on `userId` parameter" → Good: "Missing null/undefined checks on function inputs"
   If a pattern is *already* general (e.g., "Missing null checks on function inputs"), keep it as-is. If multiple task-specific patterns generalize to the same reusable principle, collapse them into one entry.
3. Categorize each generalized pattern into one of: Error Handling, Testing, Security, Code Quality, Naming, Documentation, Performance, or another short category name as appropriate. Reuse existing category names from `existing_patterns_snapshot` (captured in Step 0) whenever the pattern fits — do not invent a near-duplicate category like "Error-Handling" or "Tests" when one already exists.
4. For each pattern, write a concise one-line description. Keep descriptions on a single line; the helper collapses any embedded newlines but it's cleaner to write them without.

### Step 6b: Harmonize Phrasing Against Existing Entries

Before handing generalized patterns to the helper, dedup at the *phrasing* level using `existing_patterns_snapshot`:

1. For each of this run's patterns, scan `existing_patterns_snapshot` for an entry in the same (or semantically equivalent) category whose description means the same thing — even if worded differently. Examples of matches:
   - "missing null check on input" ≈ "No null validation for function parameters"
   - "functions over 50 lines" ≈ "Long functions without decomposition"
   - "no tests for error path" ≈ "Missing tests for failure cases"
2. **If a semantic match exists:** replace this run's description with the **exact existing description string** (so the helper's normalised match will collapse them onto the same entry).
3. **If no match exists:** keep your concise description as-is. It will be added as a new entry.
4. **Within this run's own list:** also dedup by phrasing — if you have two patterns that mean the same thing, collapse them to a single entry (the helper would otherwise count them as two distinct hits, which is fine but slightly inflates new-pattern stats).

The helper will also do a final case/whitespace/punctuation normalisation, but it cannot infer semantic equivalence — that's the orchestrator's job here. Skipping this step leads to the file accumulating near-duplicates over time.

### Step 6c: Build the Update Spec

Construct a JSON object with this shape (omit `run` only if you want to record patterns without logging a run; in normal flow, always include both):

```json
{
  "patterns": [
    {"category": "Error Handling", "description": "Missing null/undefined checks on function inputs"},
    {"category": "Testing", "description": "Missing tests for error/edge case paths"}
  ],
  "run": {
    "date": "2026-04-23",
    "description": "Add retry logic to blackbox client",
    "rounds": 2,
    "issues_by_severity": {"bug": 1, "suggestion": 1, "nit": 5},
    "key_patterns": ["Missing entries in error-type allowlists", "Incomplete configuration validation"],
    "specializations": ["general"]
  }
}
```

Field notes (the helper rejects wrong-typed input with exit code 4 and a clear error message identifying the offending field; empty-or-null input falls back to defaults or is silently skipped per the per-field rules below):
- `patterns[]`: each entry must be an object. `category` must be a string (defaults to `"Other"` if empty/null). `description` must be a string; **null and omitted are treated identically** (both result in a silent skip with no error).
- `patterns[].description`: one-line, harmonised in Step 6b. Newlines/tabs are collapsed to single spaces; internal multi-space runs are preserved.
- `run` must be an object (not a list, not a string). Send `null` or omit it entirely to skip the Recent Runs entry.
- `run.date`: a string in `YYYY-MM-DD` format. Calendar-invalid dates like `2026-13-99` are rejected. Pass `null`, empty string, or whitespace-only string and the helper fills in today's UTC date.
- `run.description`: the user's implementation request, trimmed to a short label. Must be a string (or `null`/omitted to fall back to `"(no description)"`). The helper strips ALL double-quote characters from the description and then wraps it in exactly one outer pair, so internal quotes never produce broken nested-quote markup. (`Add retry "logic" to client` becomes `"Add retry logic to client"`.) If you need to preserve quotes verbatim, escape them yourself before submission — the helper assumes the description is a free-form label, not a structured string.
- `run.rounds`: `round_count` as an integer. Booleans, floats, strings, and lists are rejected. Zero is accepted as-is (structurally unreachable in the actual /implement loop, but not enforced).
- `run.issues_by_severity`: derived from `total_issues_by_severity`. Must be an object with string keys and integer values (or `null`/omitted to skip the `**Issues**` body line entirely). Zero-count severities are silently dropped from the rendered summary; if all severities are zero (or the object is empty) the helper omits the `**Issues**` body line entirely.
- `run.key_patterns`: must be a list of strings (or `null`/omitted to skip the `**Key patterns**` body line). Pick the 2-3 most-significant patterns from this run. **Apply the same generalization rules as Step 6a** — strip task-specific names and rewrite as reusable principles. Two implementable options, pick consistently across runs:
  - **Option A (recommended): severity-ranked.** Re-read the latest merged review_file (still on disk at this point in the loop). Each issue has a `Severity:` tag. Take 1-2 of the highest-severity issues first (bugs > suggestions > nits), then top up with the next-highest severity until you have 3 entries. This sees only **final-round survivors** (issues that the implementer actually had to address) which is the natural "most-significant" reading.
  - **Option B (lower-effort): recency-ranked.** Take the **last 2-3 entries** of `issue_patterns` (the list grows by appending per round in Step 3, so the tail is the most-recent round's issues). This sees **cross-round accumulation** including issues that were introduced and fixed mid-loop. Use this only if re-reading the review_file is impractical — the resulting `key_patterns` will sometimes include issues that ended up wontfix or were ephemeral.
  - **Pick one option and stick with it for the run.** The two options return semantically different sets, so mixing them across runs makes the Recent Runs log inconsistent.
- `run.specializations`: must be a list of strings (or `null`/omitted to skip the `**Specializations used**` body line). Strip the `-N` suffix from `general-2`/`general-3` first so the list is the set of distinct specialization classes (e.g., `["general", "security"]`, not `["general", "general-2", "security"]`); deduplicate.

### Step 6d: Invoke the Helper

Use the `write` tool to create `/tmp/grok-mem-${IMPL_ID}.json` with the JSON spec above (using a temp file avoids quoting issues that heredocs introduce), then invoke the helper via `run_terminal_cmd`:

```bash
python3 "${MEMORY_HELPER}" update < /tmp/grok-mem-${IMPL_ID}.json
```

The helper acquires the lock, parses the existing file, merges, compacts, writes atomically, and prints a JSON stats summary on stdout (pretty-printed with `indent=2`):

```json
{
  "file": "/Users/.../implement-memory/proj-d5016f47e5cb.md",
  "existed_before": false,
  "stats": {
    "new_patterns": 2,
    "merged_patterns": 5,
    "categories_touched": ["Error Handling", "Testing"],
    "categories_capped": {},
    "recent_runs_dropped": 0
  },
  "total_categories": 4,
  "total_patterns": 17,
  "total_recent_runs": 12
}
```

Key fields:
- `existed_before`: `true` if the file existed before this update, `false` if the helper just created it. Use this for the report wording.
- `stats.categories_capped`: dict of `{category: dropped_count}` for any category that exceeded `MAX_PATTERNS_PER_CATEGORY` and had its lowest-count entries dropped. Empty dict in the typical case.

Use these stats to report to the user:
> "Memory updated: 2 new patterns, 5 merged into existing entries (file at <file>)."

Or if `existed_before` is `false`:
> "Memory file created at <file> with N patterns."

### Memory File Format

The helper writes a markdown file with this structure:

<!-- mirror-of: scripts/memory.py DEFAULT_HEADER -->
<!-- The 5-line block immediately following this comment must match -->
<!-- '\n'.join(memory.DEFAULT_HEADER) verbatim. The drift-check unit -->
<!-- test TestDocsConsistency.test_skill_md_default_header_matches -->
<!-- asserts this on every test run. -->
```markdown
# Implementation Review Patterns

> This file is maintained by the /implement skill.
> It records common issues found during implementation reviews to help avoid them in future runs.
> Shared across all working directories that resolve to the same workspace id.

## Common Issues

### Error Handling
- Missing null/undefined checks on function inputs (seen 5 times)
- Not handling async errors in promise chains (seen 3 times)
- Missing error logging before re-throwing (seen 2 times)

### Testing
- Missing tests for error/edge case paths (seen 8 times)
- Tests that don't assert on error messages, only error types (seen 3 times)
- No integration tests for new API endpoints (seen 2 times)

### Security
- User input not validated before database queries (seen 2 times)
- Missing rate limiting on new endpoints (seen 1 time)

### Code Quality
- Functions exceeding 50 lines without decomposition (seen 4 times)
- Magic numbers without named constants (seen 6 times)
- Inconsistent naming conventions within new code (seen 3 times)

## Recent Runs

### 2026-04-23 — "Add retry logic to blackbox client"
- **Rounds**: 2
- **Issues**: 7 total (1 bug, 1 suggestion, 5 nits)
- **Key patterns**: Missing entries in error-type allowlists, incomplete configuration validation
- **Specializations used**: general

### 2026-04-22 — "Implement user auth endpoints"
- **Rounds**: 3
- **Issues**: 12 total (3 bugs, 4 suggestions, 5 nits)
- **Key patterns**: Missing expiration/TTL validation on tokens, missing rate limiting on new endpoints, missing tests for error/edge case paths
- **Specializations used**: general, security
```

Notes on the format:
- Within each category, entries are sorted by count desc then description asc (case-insensitive).
- `seen 1 time` (singular) and `seen N times` (plural) are both produced and parsed.
- `—` (em-dash), `–` (en-dash), and `-` (ASCII hyphen) are all accepted as separators in run headers.
- The helper preserves any custom lines you add to the header (anything before `## Common Issues`) on round-trip. Custom freeform paragraphs **inside** a category in `## Common Issues` are not preserved — only `### Category` headers and well-formed `- desc (seen N time(s))` bullets survive. **Caveat:** anything written to the file before the first `## Common Issues` heading becomes part of the preserved header indefinitely, including unintentional garbage from a hand-edit. To reset a corrupted file, delete it and the helper will recreate it with the default header on the next `update`. If you delete the header itself (leaving the file starting at `## Common Issues`), the helper re-injects the default header on the next render — not byte-stable, but the data survives.
- Both the memory file and its sibling `.lock` file are written and then chmodded to mode `0o600` (owner read/write only, best-effort — if a cross-user race makes the chmod fail, the file's umask-default mode is preserved). The memory file may contain security-review patterns and `key_patterns` drawn from non-public source review, so we deliberately keep it owner-only on shared hosts (the workspace id is a deterministic SHA-256 of the canonical remote URL, so an unprivileged account that knows or guesses the public-repo URL could otherwise read the file directly). In the typical single-user case both files end up at `0o600` regardless of the process umask. The lock file's content is irrelevant; it exists purely as an `flock` target.

### Graceful Degradation

If the helper exits non-zero (lock contention timeout, malformed spec, disk full, etc.), log a warning with the helper's stderr and skip the memory update. The implementation is already complete and reviewed at this point — never fail the run due to memory flush issues. Also remove the temp JSON spec file in the cleanup step regardless.

Exit codes:
- `0`: success.
- `1`: unexpected I/O error (disk full mid-write, permission flips during execution, FS races). The stderr message says `memory.py: I/O error: ...`.
- `2`: workspace id could not be determined (cwd unreadable and `$HOME` unset — very rare).
- `3`: lock could not be acquired within 30 seconds (another concurrent /implement run is monopolising the file; usually retrying once works).
- `4`: stdin JSON is missing, malformed, or fails type validation. The stderr message identifies the offending field. Surface it verbatim in the report so the user can see what was wrong with the spec.

## Cleanup

After Step 6 (Memory Flush) and the Final Report, clean up the temporary artifact files:

```bash
rm -f /tmp/grok-impl-summary-${IMPL_ID}.md /tmp/grok-review-${IMPL_ID}.md /tmp/grok-review-${IMPL_ID}-*.md /tmp/grok-mem-${IMPL_ID}.json
```

Note: the workspace memory file under `$HOME/.grok/implement-memory/` is NOT cleaned up — it persists across runs as the shared memory file for this workspace.

## Final Report

When the loop terminates (0 issues), read the summary_file and review_file one last time (before cleanup), then present a final report to the user:

1. **Summary of what was implemented** — from the summary_file: which files were changed, what was added/modified, key design decisions.
2. **Effort level** — the effort parameter used and which specializations were active (e.g., "Effort 2: general + security").
3. **Review rounds** — how many review→fix iterations it took to reach 0 issues (the value of `round_count`).
4. **Total issues fixed** — the cumulative count from `total_issues_by_severity`, broken down by severity (bugs, suggestions, nits).
5. **Issues by reviewer** — breakdown of how many issues each reviewer found across all rounds (by specialization tag).
6. **Files changed** — list the files that were created or modified.
7. **Anything notable** — if the implementer made design decisions, disagreed with a reviewer suggestion (wontfix), or encountered anything unexpected, call it out.
8. **Memory update** — what patterns were written or updated in the workspace memory file (path returned by the helper as the `file` field). Use the `existed_before` flag from the helper's stats output to choose between "file created" (false) and "file updated" (true) wording.

## In-Progress Reporting

Give the user a brief status update after each phase:

- After specialization selection (effort >= 2): "Using effort level N: general reviewer + <specialist(s)> (<reason>)."
- After implement (effort=1): "Implementation complete. Starting review..."
- After implement (effort >= 2): "Implementation complete. Starting parallel review (N reviewers)..."
- After all reviewers complete (effort >= 2): "All reviewers complete. Merging findings..."
- After review (0 issues, effort=1): "Review passed with 0 issues. Flushing to memory..." (then run Step 6, then print the Final Report)
- After review (0 issues, effort >= 2): "All reviews passed with 0 issues. Flushing to memory..." (then run Step 6, then print the Final Report)
- After review (N issues, effort=1): "Reviewer found N issues (X bugs, Y suggestions, Z nits). Resuming implementer to fix..."
- After review (N issues, effort >= 2): "Merged review: N issues (X bugs [1 General, 1 Security], Y suggestions [General], Z nits [Tests]). Resuming implementer to fix..." — include per-source-tag breakdown within each severity, showing how many issues came from each reviewer.
- After fix (effort=1): "Fixes applied. Running re-review (round N)..." (where N = `round_count` + 1, i.e., the upcoming round number)
- After fix (effort >= 2): "Fixes applied. Running parallel re-review (round N)..." (where N = `round_count` + 1)
- After stalemate escalation: "Stalemate detected on N issue(s). Escalating to user..."
- After memory flush: "Memory updated with N patterns from this run." (or "Memory file created with N patterns." for first run)

## Rules

- **Inject personas into prompts** — prepend `implementer` persona instructions for the implementer, `reviewer` for general reviewer, `security-auditor` for security specialist. Do NOT pass a `persona` parameter to `spawn_subagent`. For Tests and Plan Alignment specialists, do not prepend any persona — they are prompt-only subagents. On `resume_from` follow-ups, the persona is already in the transcript from the initial launch.
- **resume_from on follow-ups** — never launch a fresh subagent for fix or re-review rounds. Always resume the previous one so it retains its full working memory. Exception: if `resume_from` fails (subagent expired), launch a fresh one and log a warning.
- **Save every subagent_id** returned by the task tool — these are needed for `resume_from` on subsequent rounds. Store them in `reviewer_configs` for reviewers.
- **Read the review_file yourself** after each review to count open issues and decide whether to continue the loop.
- **Don't modify the implementation yourself** — all code changes go through the implementer persona subagent.
- **Explicitly tell subagents to write their output files** — include the file path and what to write in every prompt.
- **Thread the same file paths** across all rounds — never generate new paths between iterations.
- **No iteration cap** — the loop runs until 0 issues. Do not add a max rounds limit.
- **If the user provides additional instructions** (like "run tests after", "use this pattern", "don't touch file X"), include those constraints in the implementer prompt.
- **Error handling** — if a subagent fails or cannot be resumed, report the error to the user and stop. Do not silently continue with missing results. Exception: specialist reviewer failures are non-fatal (warn and continue with remaining reviewers); only general reviewer failure is fatal.
- **Effort=1 is structurally simple** — for effort=1, the single general-purpose reviewer writes directly to `review_file`. No individual review files, no merge step. This is the current behavior with the added wontfix/stalemate mechanism.
- **Effort>=2 uses individual files + merge** — each reviewer writes to its own file to avoid write conflicts during parallel execution. The orchestrator merges them into `review_file` after all complete.
- **Severity normalization** — all reviewers must use `bug`, `suggestion`, `nit` as severity labels. The security specialist prompt explicitly maps native security severities to this taxonomy.
- **Implementer can push back** — the implementer is explicitly allowed (and encouraged) to set `Status: wontfix` with a technical justification. If a reviewer re-opens a wontfix'd issue, it's a stalemate that gets escalated to the user.
- **Escalate, don't spin** — if the implementer and a reviewer cannot reach consensus on an issue after two rounds, escalate to the user by asking them directly (use the appropriate ask/question tool if available). Never let the loop spin on a disagreement.
- **User decisions are final** — once the user resolves a disputed issue, the implementer must incorporate it without further debate.
- **Memory is best-effort.** The past-issues briefing and memory flush are additive features. If the `memory.py` helper fails (lock contention timeout, malformed spec, disk full, etc.) proceed without it. Never fail a run due to memory issues. A non-git workspace is **not** a failure mode — the helper falls back to a cwd-based id.
- **Always go through the `memory.py` helper.** The file lives at `$HOME/.grok/implement-memory/<workspace-id>.md`, resolved by `python3 "${MEMORY_HELPER}" path`. The helper itself lives at `<dirname of this SKILL.md>/scripts/memory.py` — derive `MEMORY_HELPER` from the SKILL.md path the system context gave you (it works whether the skill is loaded from a workspace, from `~/.grok/skills/`, or from a bundled location), **never** from `$(pwd)`. The workspace id is derived from a canonicalised `git config remote.origin.url` (falling back to the absolute `--git-common-dir` path, then to the absolute cwd), so all worktrees and SSH/HTTPS clones of the same upstream repo share one file. Never reference the legacy `.grok/implement-issues.md` path — it is per-worktree and useless. Never read or write the file directly — the helper is the single source of truth.
- **Concurrency-safe writes are the helper's job, not yours.** The helper holds an exclusive `fcntl.flock` (Python stdlib, not the `flock(1)` shell tool) on a sibling `.lock` file during the read-merge-write and commits via temp-file + rename, so two /implement runs in different worktrees can update the file simultaneously without losing writes. Do **not** implement your own locking around the helper.
- **Dedup is a two-layer responsibility.** The orchestrator harmonises this run's pattern phrasings against `existing_patterns_snapshot` (semantic dedup, Step 6b); the helper then performs case/whitespace/punctuation normalisation as a safety net. Skipping the orchestrator step leads to near-duplicate entries the helper cannot collapse.
- **Compaction is automatic.** The helper caps each category at 25 entries (lowest-count entries dropped) and Recent Runs at 20 entries (oldest dropped). The orchestrator does not need to enforce caps.
- **Use the `snapshot` subcommand for reads, not `read`.** `python3 "${MEMORY_HELPER}" snapshot` returns structured JSON (`common_issues`, `recent_runs`, `exists`) so the orchestrator never has to parse markdown. The `read` subcommand is preserved for human inspection only.
- **Briefing is injected, not enforced** — the past-issues briefing is informational context. It tells the implementer and reviewers what patterns to watch for, but does not mandate specific behaviors or block the run if patterns are found.
