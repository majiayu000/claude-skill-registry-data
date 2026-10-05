---
name: decision-journal
description: Extracts and structures development decisions from diffs, manages decision journal entries, and detects human gate triggers. Use when logging decisions during gh-start, gh-commit, or gh-address. Use when summarizing decisions for PR bodies or when checking for gate-triggering changes like new dependencies, security modifications, or scope deviations.
allowed-tools: Bash, Read, Grep, Glob
context: fork
agent: Explore
---

# Decision Journal

Captures, structures, and persists significant decisions made during AI-driven workflow execution. Uses post-hoc extraction from diffs rather than AI self-reporting during execution.

## Purpose

In a fully AI-driven workflow, decisions happen invisibly. This skill makes them visible by:
- Extracting decisions from completed diffs (what changed vs. what was expected)
- Detecting high-stakes changes that warrant human approval (gates)
- Structuring decisions into a machine-parseable journal format
- Condensing journals into PR-body-ready summaries

## Mode Routing

This skill operates in one of three modes. The calling command specifies the mode in its invocation prompt.

| Mode | When Used | What It Does |
|------|-----------|-------------|
| `init` | gh-start after branch creation | Creates journal file header |
| `log` | gh-start, gh-commit, gh-address after changes | Extracts decisions from diff + evaluates gate triggers |
| `summarize` | gh-pr during PR content generation | Condenses journal for PR body |

Read the mode from the invocation prompt and execute only that mode's instructions. If the mode is not one of `init`, `log`, or `summarize`, return an error: `"Unknown mode: {mode}. Expected one of: init, log, summarize."`

## Mode: init

**Input** (from invocation prompt): Issue number, branch name, issue title, issue body.

**Process:**

### Step 1: Read Configuration

```bash
# Read journal directory from settings (local > project > user > default)
JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=".decisions"
echo "Journal directory: $JOURNAL_DIR"
```

### Step 2: Generate Header

Generate the journal file header:

```markdown
# Decision Journal: Issue #{N} — {issue title}

**Issue**: #{N}
**Branch**: {branch-name}
**Started**: {YYYY-MM-DD}

---
```

**Output:** Return the header markdown and the resolved journal directory (from `.journal.dir` in settings, default `.decisions`). The calling command writes it to `{journal-dir}/issue-{N}.md`.

## Mode: log

**Input** (from invocation prompt): Description of what phase just completed (e.g., "task breakdown", "staged changes for commit", "addressed review feedback"). The calling command provides the relevant context.

**Process:**

### Step 1: Gather Context

```bash
# Get current branch and issue number
BRANCH=$(git branch --show-current)
ISSUE_NUM=$(echo "$BRANCH" | grep -oE 'issue-[0-9]+' | grep -oE '[0-9]+')

# Get the default branch
DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH=$(git rev-parse --verify origin/main >/dev/null 2>&1 && echo "main" || echo "master")
```

```bash
# Read all comprehension config from settings (local > project > user > default)
# Single merge for both journal and gates — used in Steps 1-3
GHW_CONFIG=$(jq -n '
  def defaults: {
    gates: {
      newDependencies:"on", securityChanges:"on", schemaChanges:"on",
      apiSurfaceChanges:"on", scopeDeviations:"on", ambiguousRequirements:"on",
      customTriggers:[], customTriggersMode:"on"
    },
    journal: { dir:".decisions", sensitivityDefault:"public" }
  };
  defaults
    * (try input catch {})
    * (try input catch {})
    * (try input catch {})
' "$HOME/.claude/settings.gh-workflow.json" \
  ".claude/settings.gh-workflow.json" \
  ".claude/settings.gh-workflow.local.json" 2>/dev/null)

JOURNAL_DIR=$(echo "$GHW_CONFIG" | jq -r '.journal.dir')
SENSITIVITY_DEFAULT=$(echo "$GHW_CONFIG" | jq -r '.journal.sensitivityDefault')
echo "Journal directory: $JOURNAL_DIR"
echo "Default sensitivity: $SENSITIVITY_DEFAULT"
```

Use `$JOURNAL_DIR` instead of `.decisions` for all journal file paths in this mode. Use `$SENSITIVITY_DEFAULT` as the default sensitivity for new entries.

```bash
# Get the diff to analyze (staged changes for commit, or branch diff for other phases)
git diff --stat "$DEFAULT_BRANCH"...HEAD
git diff --name-only "$DEFAULT_BRANCH"...HEAD
```

```bash
# Get issue context
gh issue view "$ISSUE_NUM" --json title,body,labels 2>/dev/null
```

### Step 2: Extract Decisions (Post-Hoc)

Analyze the completed diff against the issue context. Identify decisions by comparing:
- **What changed** vs. **what the issue requested** — scope decisions, requirement interpretations
- **Patterns chosen** vs. **alternatives available** — architecture, implementation trade-offs
- **Files touched** vs. **expected impact area** — scope deviations

For each significant decision found, generate a journal entry:

```markdown
### {YYYY-MM-DD HH:MM} [{CATEGORY}] {Decision Title}

**Command**: {gh-start | gh-commit | gh-address}
**Decision**: {What was decided}
**Alternatives**: {What else was considered, or "N/A" for obvious choices}
**Rationale**: {Why this choice was made}
**Risk**: {Low | Medium | High | Critical}
**Sensitivity**: {public | internal}
**Gate**: {No — AI decision}
**References**: {#M, #K — cross-issue refs, or "None"}

---
```

**Categories**: `architecture`, `requirements`, `trade-off`, `implementation`, `risk`, `scope`

**Sensitivity rules:**
- Default: Use the `$SENSITIVITY_DEFAULT` value from Step 1 config (falls back to `public` if not configured)
- Use `internal` for decisions involving: security rationale, credential/secret handling, vulnerability remediation, access control logic
- Never document specific vulnerability details, exploitation vectors, previous insecure states, or secret values/locations — even in `internal` entries

### Step 3: Evaluate Gate Triggers

Extract gate configuration from the `$GHW_CONFIG` loaded in Step 1:

```bash
# Extract gates from the config already loaded in Step 1
echo "$GHW_CONFIG" | jq '.gates'
```

If no configuration found, all gates default to `on`.

Check the diff against these gate detection heuristics:

| Trigger | Detection Method | Config Key |
|---------|-----------------|------------|
| New dependency | New entries in `package.json`, `requirements.txt`, `Gemfile`, `go.mod`, `Cargo.toml`, or new git submodule | `.gates.newDependencies` |
| Security changes | Files matching `*auth*`, `*security*`, `*permission*`, `*token*`, `*secret*`, `*crypto*`, `*session*`; changes to `.env*`, CORS/TLS config | `.gates.securityChanges` |
| Schema changes | Database migration files, changes to `schema.*`, `*model*` definitions, API type definitions | `.gates.schemaChanges` |
| API surface changes | New route/endpoint definitions, changed function signatures in public modules, new command/skill files | `.gates.apiSurfaceChanges` |
| Scope deviations | Files modified outside the expected impact area from the issue | `.gates.scopeDeviations` |
| Ambiguous requirements | Acceptance criteria containing vague terms ("should be fast", "user-friendly", "appropriate"), contradictory criteria | `.gates.ambiguousRequirements` |

```bash
# Example detection for new dependencies
git diff "$DEFAULT_BRANCH"...HEAD --name-only | grep -E "(package\.json|requirements\.txt|Gemfile|go\.mod|Cargo\.toml|\.gitmodules)" 2>/dev/null
```

```bash
# Example detection for security-related files
git diff "$DEFAULT_BRANCH"...HEAD --name-only | grep -iE "(auth|security|permission|token|secret|crypto|session|\.env)" 2>/dev/null
```

```bash
# Evaluate custom trigger patterns (glob patterns from config)
CUSTOM_TRIGGERS=$(echo "$GHW_CONFIG" | jq -r '.gates.customTriggers[]' 2>/dev/null)
if [ -n "$CUSTOM_TRIGGERS" ]; then
  CHANGED_FILES=$(git diff "$DEFAULT_BRANCH"...HEAD --name-only)
  echo "$CUSTOM_TRIGGERS" | while read -r pattern; do
    echo "$CHANGED_FILES" | grep -E "$pattern" 2>/dev/null
  done
fi
```

Custom trigger matches use the `.gates.customTriggersMode` config key (`on`/`log`/`off`), following the same behavior as the named gates.

For each trigger that fires:
1. Check the corresponding config key
2. If `on` — include in gate trigger output
3. If `log` — log the decision entry with `Gate: Logged (auto-approved)` but do not include in gate triggers
4. If `off` — skip entirely

### Step 4: Return Output

**Output format:**

```markdown
## Decision Entries

{One or more journal entries in the schema format above}

## Gate Triggers

{If any gates fired with config = `on`:}

| Category | Trigger | Reason | Recommended Action | Alternatives |
|----------|---------|--------|--------------------|-------------|
| security-changes | gates.securityChanges | Modified auth middleware | Review security implications | Proceed without review |

{If no gates fired:}

No gate triggers detected.
```

The calling command:
- Appends decision entries to `{journal-dir}/issue-{N}.md` (using the resolved `$JOURNAL_DIR` from Step 1)
- If gate triggers are present, presents AskUserQuestion with the gate format
- Logs gate responses (approved/bypassed) back to the journal

## Mode: summarize

**Input** (from invocation prompt): Issue number, sensitivity filter preference.

**Process:**

1. Extract the issue number from the invocation prompt and read journal configuration:

```bash
# Extract issue number from invocation prompt (the calling command provides this)
# Example invocation: "Mode: summarize. Issue number: 42. Sensitivity filter: redact internal entries."
# Parse the issue number from the prompt text.

# Read journal-dir from settings (local > project > user > default)
JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.local.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' .claude/settings.gh-workflow.json 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=$(jq -r '.journal.dir // empty' "$HOME/.claude/settings.gh-workflow.json" 2>/dev/null)
[ -z "$JOURNAL_DIR" ] && JOURNAL_DIR=".decisions"

# Read the specific journal file using the issue number from the invocation prompt
cat "$JOURNAL_DIR/issue-$ISSUE_NUM.md" 2>/dev/null
```

**Note**: `$ISSUE_NUM` should be set from the issue number provided by the calling command in the invocation prompt (e.g., `"Mode: summarize. Issue number: 42."`). If not provided, fall back to branch detection: `ISSUE_NUM=$(git branch --show-current | grep -oE 'issue-[0-9]+' | grep -oE '[0-9]+')`.

2. Parse entries by splitting on `---` separators
3. For each entry:
   - If `Sensitivity: public` — include full entry in summary
   - If `Sensitivity: internal` — replace with: `[Internal decision — see decision journal for details]`
4. Condense into a summary format:

**Output format:**

```markdown
## Decision Summary

**Total decisions**: {N} ({M} public, {K} internal)
**Gates triggered**: {X} ({Y} approved, {Z} bypassed)

### Key Decisions

| # | Category | Decision | Risk |
|---|----------|----------|------|
| 1 | architecture | {title} | {risk} |
| 2 | requirements | {title} | {risk} |

### Decision Details

{For each public entry, include a condensed version:}

**{Category}: {Title}** — {Decision}. {Rationale}. Risk: {risk}.

{For internal entries:}

**{Category}: [Internal decision]** — [See decision journal for details]

### Gate Activity

{Summary of gate triggers and responses}
```

## Output Format

All modes return structured markdown. The calling command handles file I/O.

| Mode | Returns |
|------|---------|
| `init` | Journal file header markdown |
| `log` | Decision entries + gate trigger table |
| `summarize` | Condensed summary for PR body |

## Graceful Degradation

| Missing Capability | Fallback |
|-------------------|----------|
| No gate config in settings | All gates default to `on` |
| No issue context (gh issue view fails) | Extract decisions from diff only, skip requirement comparison |
| No existing journal file (for summarize) | Return "No decision journal found" notice |
| Empty diff | Return "No changes to analyze" with no entries |
| Branch has no issue number | Use branch name as identifier, skip issue context |

## Integration Points

This skill is invoked by:
- `gh-start` — Phase 2 (`init` mode), Phase 5 (`log` mode)
- `gh-commit` — Phase 2 (`log` mode)
- `gh-pr` — Phase 3 (`summarize` mode)
- `gh-address` — After feedback aggregation (`log` mode)

The calling command handles all file persistence (Write/Edit to `{journal-dir}/issue-{N}.md`, where `journal-dir` is read from settings via `.journal.dir`, default `.decisions`) and AskUserQuestion presentation for gate triggers.
