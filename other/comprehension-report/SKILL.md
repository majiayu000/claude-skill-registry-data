---
name: comprehension-report
description: Generates architecture narratives and requirements adherence reports from diffs, decision journals, and issue context. Use when creating PR bodies that need comprehension reports. Use when validating that implementation meets acceptance criteria or when humans need to understand what AI built and why.
allowed-tools: Bash, Read, Grep, Glob
context: fork
agent: Explore
---

# Comprehension Report

Generates a structured narrative that helps humans understand what AI built, why it made the choices it did, and whether those choices align with the original intent.

## Purpose

In a fully AI-driven workflow, code is produced faster than humans can read it. This skill bridges the gap by:
- Translating diffs into plain-language summaries
- Mapping acceptance criteria to implementation evidence
- Surfacing architecture decisions from the decision journal
- Identifying what humans should verify manually

## Report Tiers

The report scales based on diff complexity. Complexity is determined from `git diff --stat` output.

| Diff Complexity | Report Level | Sections |
|----------------|-------------|----------|
| < threshold lines, single area, docs/config only | **Minimal** — Summary + Requirements Adherence | 2 sections |
| threshold+ lines or multi-area or new modules | **Full** — All sections | 5 sections |

The threshold is configurable via `.report.thresholdFull` in settings. Default: `100` lines changed.

## Process

### Step 1: Gather Context

```bash
# Get current branch and issue number
BRANCH=$(git branch --show-current)
ISSUE_NUM=$(echo "$BRANCH" | grep -oE 'issue-[0-9]+' | grep -oE '[0-9]+')

# Get the default branch (consistent with gh-workflow commands)
DEFAULT_BRANCH=$(gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name' 2>/dev/null)
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH="main"
```

```bash
# Get diff statistics to determine report tier
git diff --stat "$DEFAULT_BRANCH"...HEAD
git diff --numstat "$DEFAULT_BRANCH"...HEAD | awk '{ added += $(1); removed += $(2) } END { print "Lines added:", added, "Lines removed:", removed, "Total:", added + removed }'
```

```bash
# Get changed files with directory breakdown
git diff --name-only "$DEFAULT_BRANCH"...HEAD
```

```bash
# Get issue context
gh issue view "$ISSUE_NUM" --json title,body,labels 2>/dev/null
```

```bash
# Read journal directory from settings (local > project > user > default)
JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=".decisions"

# Read decision journal if it exists
cat "$JOURNAL_DIR/issue-$ISSUE_NUM.md" 2>/dev/null
```

### Step 2: Read Report Configuration

```bash
# Read report threshold from settings (local > project > user > default)
THRESHOLD=$(jq -r '.report.thresholdFull // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$THRESHOLD" ] && THRESHOLD=$(jq -r '.report.thresholdFull // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$THRESHOLD" ] && THRESHOLD=$(jq -r '.report.thresholdFull // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$THRESHOLD" ] && THRESHOLD=100
```

### Step 3: Determine Report Tier

Evaluate diff complexity:

1. **Count total lines changed** from `git diff --numstat`
2. **Count distinct directories** touched (top-level grouping)
3. **Check for new modules** — files in directories that don't exist on the default branch

**Minimal tier** when ALL of these are true:
- Total lines changed < threshold (default 100)
- Changes touch a single top-level directory
- No new modules or directories created
- Changes are limited to docs, config, or existing file modifications

**Full tier** when ANY of these are true:
- Total lines changed >= threshold
- Changes span multiple top-level directories
- New modules or directories created
- New dependencies added

### Step 4: Generate Report

#### Minimal Report

```markdown
## Comprehension Report

**Tier**: Minimal ({N} lines changed, single area)

### Summary

{2-3 sentence plain-language description of what changed and why. Reference the issue objective. Written for a human who hasn't seen the code.}

### Requirements Adherence

| # | Acceptance Criterion | Status | Evidence |
|---|---------------------|--------|----------|
| 1 | {criterion from issue} | Met | {file:line or brief description} |
| 2 | {criterion from issue} | Met | {file:line or brief description} |
```

#### Full Report

```markdown
## Comprehension Report

**Tier**: Full ({N} lines changed, {M} areas)

### Summary

{2-3 sentence plain-language description of what changed and why. Reference the issue objective. Written for a human who hasn't seen the code.}

### Architecture Decisions

{Key structural choices extracted from the decision journal. For each significant decision:}

{**Sensitivity filtering**: Parse each journal entry's `Sensitivity:` field. Only include entries with `Sensitivity: public`. For entries with `Sensitivity: internal`, emit: `- **[Internal decision]** — [See decision journal for details]`. Never include internal decision details, rationale, or context in the PR body.}

- **{Decision title}** — {What was decided and why}. Risk: {risk level}. {If alternatives were considered, mention them briefly.}

{If no decision journal exists: "No decision journal found — decisions inferred from diff analysis."}

### How It Connects

{Relationship to existing system components. What existing code does this interact with? What patterns does it follow or extend? Are there new integration points?}

- **Extends**: {existing module/pattern}
- **Integrates with**: {existing component}
- **New entry point**: {if applicable}

### Requirements Adherence

| # | Acceptance Criterion | Status | Evidence |
|---|---------------------|--------|----------|
| 1 | {criterion from issue} | Met | {file:line or brief description} |
| 2 | {criterion from issue} | Interpreted | {what was interpreted and how} |
| 3 | {criterion from issue} | Partially Met | {what's done, what's missing} |
| 4 | {criterion from issue} | Not Addressed | {reason — deferred, out of scope, blocked} |

**Status definitions:**
- **Met** — Criterion directly implemented and testable
- **Interpreted** — Criterion was ambiguous; implementation reflects a specific interpretation
- **Partially Met** — Some aspects implemented, others pending
- **Not Addressed** — Not implemented in this change

### What to Verify

{Specific things a human should check. Not generic advice — concrete actions based on this specific diff.}

- [ ] {Specific verification action 1}
- [ ] {Specific verification action 2}
- [ ] {Specific verification action 3}
```

### Step 5: Return Output

Return the complete report markdown. The calling command (gh-pr) includes it in the PR body.

## Output Format

| Input | Returns |
|-------|---------|
| Diff + issue + journal | Structured comprehension report markdown (minimal or full tier) |

## Graceful Degradation

| Missing Capability | Fallback |
|-------------------|----------|
| No decision journal | Generate report from diff + issue only, note "decisions inferred from diff analysis" |
| No issue context (gh issue view fails) | Generate report from diff only, skip requirements adherence |
| Empty diff | Return "No changes to analyze" notice |
| Branch has no issue number | Use branch name as context, skip issue-specific sections |
| Report threshold not configured | Default to 100 lines |

## Integration Points

This skill is invoked by:
- `gh-pr` — Phase 3 (parallel with code review agents), output included in Phase 7 PR body
- `gh-address` — After fixes applied, to regenerate stale reports
