---
name: rem-handoff
description: 'Session continuity and handoff. Saves current session state for future resumption, or resumes from a previous handoff. Use for handoff, session handoff, context transfer, resume, continue, pick up where I left off, save progress, session state, or context preservation.'
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, AskUserQuestion
argument-hint: '''["create" or "resume" or path to handoff file]'''
---

# Session Handoff

You are a session continuity engineer. Your job: capture the full mental model and implementation state so a fresh session can resume without the 10-30 minutes of "where was I?" and "why did I do that?" context rebuilding.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful (5 moments only); CTAs are invitational, not declarative; banned vocabulary translates per the table in that file.

## Philosophy

- **"Approaches tried and abandoned" is the most valuable section.** This is the context that's permanently lost between sessions. Code shows what WAS done, git shows what WAS committed, but nothing captures what was TRIED and WHY it failed.
- **Auto-capture before interview.** Show the developer what you found to trigger memory. Don't make them reconstruct from scratch.
- **Verify everything.** No stale file references, no TODO placeholders, no secrets.
- **Handoffs are cheap insurance.** 2 minutes now saves 20 minutes next session.
- **Chain, don't delete.** Previous handoffs are superseded, not removed.

---

## Phase 0: Determine Mode

Parse `$ARGUMENTS` to determine the mode:

| Argument | Mode |
|----------|------|
| `create` or `save` | CREATE - save current state |
| `resume` or `load` | RESUME - load previous state |
| Path to a `.md` file | RESUME - load that specific handoff |
| No arguments | AUTO-DETECT (see below) |

### AUTO-DETECT (no arguments):

```bash
ls docs/handoffs/*.md 2>/dev/null | sort -r | head -5
```

If handoffs exist, use AskUserQuestion:

```json
{
  "questions": [{
    "question": "What would you like to do?",
    "header": "Handoff",
    "multiSelect": false,
    "options": [
      { "label": "Create new handoff", "description": "Save current session state for later" },
      { "label": "Resume from latest", "description": "[latest handoff filename]" },
      { "label": "Browse handoffs", "description": "See all available handoff files" }
    ]
  }]
}
```

If no handoffs exist: default to CREATE mode.

---

## CREATE WORKFLOW

### Phase 1: Auto-Capture (SILENT - gather before asking)

Run all of these in parallel. Failures are fine - not every project has all of these.

#### Git state:
```bash
git branch --show-current
git status -s
git log --oneline -10
git log --oneline main..HEAD 2>/dev/null
git stash list
git diff --stat HEAD 2>/dev/null
```

#### Project artifacts:
```bash
# Active plans
ls docs/plans/*.md 2>/dev/null

# Existing handoffs (for chaining)
ls docs/handoffs/*.md 2>/dev/null | sort -r | head -3

# Recently modified source files (proxy for "what was being worked on")
find . -name '*.ts' -o -name '*.tsx' -o -name '*.go' -o -name '*.py' -o -name '*.js' -o -name '*.jsx' -o -name '*.rs' | head -300 | xargs ls -lt 2>/dev/null | head -20
```

#### Build health:
```bash
# Quick build check - detect project type and run appropriate command
# Next.js / Node
[ -f package.json ] && npx tsc --noEmit 2>&1 | tail -5

# Go
[ -f go.mod ] && go build ./... 2>&1 | tail -5

# Rust
[ -f Cargo.toml ] && cargo check 2>&1 | tail -5
```

#### Organize auto-captured data:
- **Branch**: current branch name
- **Uncommitted**: count and list of modified files
- **Recent commits**: last 5-10, grouped by topic
- **Unpushed**: commits ahead of main
- **Active plan**: if a plan file exists in `docs/plans/`, read the header status block per `_references/plan-contract.md`:
  - `Status:` value (Draft / In Review / Approved / Executing / Ready for merge / Deployed / Abandoned)
  - Current task number (find last checked item in `## Execution Tracker` or last commit matching a Task N)
  - Review round count and last finding IDs
- **Build status**: passing or failing (with error summary)
- **Previous handoff**: most recent, for chaining

---

### Phase 2: Structured Handoff Interview

Use AskUserQuestion for each question. Show auto-captured data to trigger memory.

#### Question 1: What were you working on?

Present the auto-captured git data and ask for confirmation/expansion:

```
"I found this activity:
- Branch: [branch]
- Recent commits: [grouped summary]
- Modified files: [list]
- Active plan: [if found]

Is this accurate? What's the high-level goal?"
```

Free-form text response.

#### Question 2: Current state

```json
{
  "question": "What's the current state of this work?",
  "header": "Status",
  "multiSelect": false,
  "options": [
    { "label": "In progress - on track", "description": "Making steady progress, no issues" },
    { "label": "In progress - stuck", "description": "Hit a wall, need to rethink something" },
    { "label": "Blocked", "description": "Waiting on something external" },
    { "label": "Ready for review", "description": "Code is done, needs review/testing" },
    { "label": "Pausing mid-task", "description": "Stopping in the middle of something" }
  ]
}
```

Follow up with: "What's done, what's partially done, and what's remaining?"

#### Question 3: Approaches tried and abandoned (CRITICAL - never skip)

```
"This is the most valuable part of the handoff - it prevents re-investigation.

Were there any approaches, solutions, or ideas you tried that DIDN'T work?
Include: what you tried, why it failed, and what you learned from it.

(If nothing was abandoned, say 'none' - but think hard. Even small dead ends count.)"
```

Free-form text response.

#### Question 4: Current hypothesis / mental model

```
"What's your current understanding or hypothesis about the problem/solution?
What does the next session need to know that ISN'T in the code?"
```

Free-form text response.

#### Question 5: Immediate next steps

```json
{
  "question": "What should the next session do FIRST?",
  "header": "Next Steps",
  "multiSelect": false,
  "options": [
    { "label": "Continue implementing", "description": "Pick up where I left off on [current task]" },
    { "label": "Fix the failing build/tests", "description": "Build is broken, fix that first" },
    { "label": "Try a different approach", "description": "Current approach isn't working" },
    { "label": "Review and refactor", "description": "Code works but needs cleanup" }
  ]
}
```

Follow up: "Any specific steps? (e.g., 'start with file X, then do Y')"

#### Question 6: Key decisions

```
"Were any important decisions made during this session?
Include the decision AND the reasoning - the 'why' is what gets lost.

(e.g., 'Chose Approach A over B because B had a race condition with concurrent writes')"
```

Free-form text response.

---

### Phase 3: Generate Handoff Document

Compose the handoff from auto-captured data + interview answers.

Determine a short slug from the work description (e.g., `auth-token-refresh`, `search-pagination-fix`).

```markdown
# Session Handoff: [Brief Description]
> Created: [YYYY-MM-DD HH:MM] | Branch: [branch] | Status: [in-progress/blocked/ready-for-review]
> Continues-from: [path to previous handoff, if chaining]

## What Was Being Done
[1-3 sentences from Q1 - high-level goal and context]

## Current State
- **Done**: [completed items from Q2]
- **In Progress**: [partially done items with current state from Q2]
- **Not Started**: [remaining items from Q2]

## Important Context
[From Q4 - things the next session MUST know that aren't in the code.
Mental models, hypotheses, understanding of the problem space.]

## Approaches Tried & Abandoned
[From Q3 - what was tried, why it didn't work.
This section prevents re-investigation and is the highest-value part of the handoff.]

## Decisions Made
[From Q6 - key decisions with rationale.
Format: "Decision: X. Reason: Y. Alternative considered: Z."]

## Immediate Next Steps
1. [First thing to do - from Q5]
2. [Second thing]
3. [Third thing]

## Environment State
- **Branch**: [branch name]
- **Uncommitted changes**: [yes/no, what files]
- **Unpushed commits**: [count, if any]
- **Build status**: [passing/failing - with error summary if failing]
- **Active plan**: [path to plan file, if any] — include `Status: X`, `Task N/M complete`, `Review-rounds: N` from the plan header per plan-contract.md
- **Stashes**: [list, if any]
- **Blockers**: [any blockers with who can unblock]

## Files of Interest
[Key files that were being worked on - with brief notes on what was being changed.
Only files relevant to the current work, not every file in the project.]

| File | Status | Notes |
|------|--------|-------|
| `path/to/file` | Modified | [what was being changed] |
| `path/to/file` | Created | [purpose] |
| `path/to/file` | Read-only | [why it matters - dependency, reference] |
```

---

### Phase 4: Validation

Before saving, run quality checks:

#### Security scan:
Grep the generated document for potential secrets:
- API keys, tokens, passwords (patterns: `sk-`, `ghp_`, `password`, `secret`, `token=`, `key=`)
- Connection strings, credentials
- If ANY found: redact and warn the developer

#### Reference verification:
For every file path mentioned in "Files of Interest":
```bash
test -f [path] && echo "EXISTS" || echo "MISSING"
```
Remove or flag any missing file references.

#### Completeness check:
Score the handoff (start at 100, deduct):

| Issue | Deduction |
|-------|-----------|
| TODO/TBD/FIXME placeholder remaining | -30 |
| Missing required section (any of the 8 sections) | -10 each |
| Secret/token/password detected | -20 |
| Referenced file doesn't exist | -5 each |
| "Approaches Tried" is empty or says "none" with 5+ commits | -10 |
| No immediate next steps | -15 |

**If score < 70**: Report the issues and ask the developer to fill gaps before saving. Do NOT save a low-quality handoff.

**If score >= 70**: Proceed to save.

---

### Phase 5: Save

```bash
mkdir -p docs/handoffs
```

Save to `docs/handoffs/YYYY-MM-DD-[slug].md`

If chaining from a previous handoff, the `continues-from` field in the new handoff links to the previous one. Do NOT delete or modify the previous handoff.

Confirm to the developer:
```
Handoff saved to docs/handoffs/YYYY-MM-DD-[slug].md (quality score: [N]/100)
Resume later with: /rem-handoff resume
```

---

## RESUME WORKFLOW

### Phase 1: Find Handoffs

```bash
ls -lt docs/handoffs/*.md 2>/dev/null
```

If `$ARGUMENTS` is a specific file path, use that directly.

If multiple handoffs exist and no specific one was requested, present them:

```json
{
  "questions": [{
    "question": "Which handoff would you like to resume?",
    "header": "Resume",
    "multiSelect": false,
    "options": [
      { "label": "[filename]", "description": "[first line / brief description] - [age]" }
    ]
  }]
}
```

If no handoffs found: "No handoffs found in docs/handoffs/. Create one with: /rem-handoff create"

---

### Phase 2: Staleness Check

Calculate the age of the selected handoff and gather drift data:

```bash
# Age of the handoff file
stat -f "%Sm" -t "%Y-%m-%d %H:%M" docs/handoffs/[file] 2>/dev/null || stat -c "%y" docs/handoffs/[file] 2>/dev/null

# Commits since the handoff was created
git log --oneline --since="[handoff date]" | wc -l

# Files changed since the handoff
git diff --stat HEAD@{[handoff date]} 2>/dev/null || git diff --name-only --since="[handoff date]" 2>/dev/null
```

Rate the staleness:

| Age | Rating | Action |
|-----|--------|--------|
| < 24 hours | FRESH | Load directly |
| 1-3 days | SLIGHTLY STALE | Load with advisory: "X commits since this handoff" |
| 3-7 days | STALE | Warn: "Significant drift likely. Review carefully." |
| > 7 days | VERY STALE | Suggest creating a new handoff instead: "This handoff is [N] days old with [N] commits since. Consider /rem-handoff create for a fresh snapshot." |

For STALE and VERY STALE, still allow loading if the developer insists.

---

### Phase 3: Load & Verify

Read the handoff file, then verify its claims:

#### Branch check:
```bash
git branch --list [branch from handoff]
git branch --show-current
```
If the branch no longer exists, warn. If on a different branch, ask whether to switch.

#### File existence check:
For each file in "Files of Interest", verify it still exists. Flag any missing files.

#### Build check:
```bash
# Same project-type detection as CREATE workflow
```
Report if build is passing or failing.

#### Conflict check:
```bash
# Check if others have pushed to the same branch
git log --oneline [branch]..origin/[branch] 2>/dev/null
```
If there are remote commits not in the local branch, flag: "Remote has [N] commits not in your local branch. Pull before resuming."

---

### Phase 4: Present Briefing

Summarize the handoff in a concise briefing format:

```markdown
## Resuming: [Handoff Title]

**Created**: [date] ([staleness rating])
**Branch**: [branch] ([current/needs-switch])
**Build**: [passing/failing]

### What You Were Doing
[1-2 sentences from handoff]

### Current State
[Done / In Progress / Not Started summary]

### Key Context to Remember
[Important Context section - the mental model]

### What Was Already Tried (Don't Re-Investigate)
[Approaches Tried & Abandoned - HIGHLIGHT this section]

### Immediate Next Steps
1. [from handoff]
2. [from handoff]
3. [from handoff]

### Drift Since Handoff
- [N] commits since handoff
- [N] files changed
- [Any missing files or branch issues]
```

Then suggest starting:

```json
{
  "questions": [{
    "question": "How would you like to proceed?",
    "header": "Resume",
    "multiSelect": false,
    "options": [
      { "label": "Start with Next Step #1", "description": "[first immediate next step from handoff]" },
      { "label": "Review the full handoff first", "description": "Read the complete handoff document" },
      { "label": "Create a fresh handoff", "description": "This one is stale, start over" }
    ]
  }]
}
```

---

## Handoff Chaining

When creating a new handoff that continues from a previous one:

1. Set `continues-from: docs/handoffs/YYYY-MM-DD-previous.md` in the new handoff header
2. Do NOT delete or modify the previous handoff
3. The chain provides a history of how the work evolved across sessions
4. When resuming, if the selected handoff has a `continues-from`, mention it: "This continues from [previous handoff]. The chain shows [N] sessions on this work."

---

## Proactive Suggestion

After detecting these signals during a session, suggest creating a handoff:

| Signal | Trigger |
|--------|---------|
| 5+ file edits in one session | "You've touched many files. Save a handoff? /rem-handoff create" |
| Complex debugging (3+ hypotheses tested) | "Complex debugging session. Capture what you learned? /rem-handoff create" |
| Session running long (many tool calls) | "Long session. Want to save a checkpoint? /rem-handoff create" |
| User says "I'll continue tomorrow" | Auto-suggest: "Let me create a handoff before you go." |

---

## Rules

1. **Never include secrets.** Scan for API keys, tokens, passwords, connection strings before saving. Redact if found.
2. **All file references must be verified.** Every path in "Files of Interest" must exist. Remove or flag dead references.
3. **Quality score must pass.** Score < 70 = reject and ask for more information. No low-quality handoffs.
4. **Stale handoffs get flagged.** Never silently load a STALE or VERY STALE handoff without warning.
5. **"Approaches Tried & Abandoned" is mandatory.** This is the highest-value section. If the developer says "none" after a long session with many commits, push back gently - there's almost always something.
6. **Chain, don't delete.** Previous handoffs are superseded by new ones but never removed.
7. **Speed matters.** The CREATE flow should take under 3 minutes. Don't over-interview.
8. **Handoffs are not documentation.** They capture transient session state, not permanent knowledge. For permanent lessons, use /rem-learn.

## Related Skills

- `/rem-learn` - Capture permanent learnings, not transient implementation state
- `/rem-plan` - Structured implementation plans (handoffs reference active plans)
