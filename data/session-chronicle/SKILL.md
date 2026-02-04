---
name: session-chronicle
description: Session log provenance tracking. TRIGGERS - who created, trace origin, session archaeology, ADR reference.
allowed-tools: Read, Grep, Glob, Bash, AskUserQuestion
---

# Session Chronicle

Excavate Claude Code session logs to capture **complete provenance** for research findings, ADR decisions, and code contributions. Traces UUID chains across multiple auto-compacted sessions.

**CRITICAL PRINCIPLE**: Registry entries must be **self-contained**. Record ALL session UUIDs (main + subagent) at commit time. Future maintainers should not need to run archaeology to understand provenance.

**S3 Artifact Sharing**: Artifacts can be uploaded to S3 for team access. See [S3 Sharing ADR](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md).

## When to Use This Skill

- User asks "who created this?" or "where did this come from?"
- User says "document this finding" with full session context
- ADR or research finding needs provenance tracking
- Git commit needs session UUID references
- Tracing edits across auto-compacted sessions
- **Creating a registry entry for a research session**

---

## File Ownership Model

| Directory                                 | Committed? | Purpose                                  |
| ----------------------------------------- | ---------- | ---------------------------------------- |
| `findings/registry.jsonl`                 | YES        | Master index (small, append-only NDJSON) |
| `findings/sessions/<id>/iterations.jsonl` | YES        | Iteration records (small, append-only)   |
| `outputs/research_sessions/<id>/`         | NO         | Research artifacts (large, gitignored)   |
| `tmp/`                                    | NO         | Temporary archives before S3 upload      |
| S3 `eonlabs-findings/sessions/<id>/`      | N/A        | Permanent team-shared archive            |

**Key Principle**: Only `findings/` is committed. Research artifacts go to gitignored `outputs/` and S3.

---

## Part 0: Preflight Check

### Step 1: Verify Session Storage Location

```bash
/usr/bin/env bash << 'PREFLIGHT_EOF'
set -euo pipefail

# Check Claude session storage
PROJECT_DIR="$HOME/.claude/projects"
if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "ERROR: Session storage not found at $PROJECT_DIR" >&2
  echo "  Expected: ~/.claude/projects/" >&2
  echo "  This directory is created by Claude Code on first use." >&2
  exit 1
fi

# Count project folders (0 is valid - just means no sessions yet)
PROJECT_COUNT=$(ls -1d "$PROJECT_DIR"/*/ 2>/dev/null | wc -l || echo "0")
if [[ "$PROJECT_COUNT" -eq 0 ]]; then
  echo "WARNING: No project sessions found in $PROJECT_DIR"
  echo "  This may be expected if Claude Code hasn't been used in any projects yet."
else
  echo "✓ Found $PROJECT_COUNT project folders in $PROJECT_DIR"
fi
echo "Ready for session archaeology"
PREFLIGHT_EOF
```

### Step 2: Find Current Project Sessions

```bash
/usr/bin/env bash << 'FIND_SESSIONS_EOF'
set -euo pipefail

# Encode current working directory path (Claude Code path encoding)
CWD=$(pwd)
ENCODED_PATH=$(echo "$CWD" | tr '/' '-')
PROJECT_SESSIONS="$HOME/.claude/projects/$ENCODED_PATH"

if [[ -d "$PROJECT_SESSIONS" ]]; then
  # Count main sessions vs agent sessions (handle empty glob safely)
  MAIN_COUNT=$(ls -1 "$PROJECT_SESSIONS"/*.jsonl 2>/dev/null | grep -v "agent-" | wc -l | tr -d ' ' || echo "0")
  AGENT_COUNT=$(ls -1 "$PROJECT_SESSIONS"/agent-*.jsonl 2>/dev/null | wc -l | tr -d ' ' || echo "0")

  if [[ "$MAIN_COUNT" -eq 0 && "$AGENT_COUNT" -eq 0 ]]; then
    echo "ERROR: Session directory exists but contains no .jsonl files" >&2
    echo "  Location: $PROJECT_SESSIONS" >&2
    exit 1
  fi

  echo "✓ Found $MAIN_COUNT main sessions + $AGENT_COUNT subagent sessions"
  echo "  Location: $PROJECT_SESSIONS"

  # Show main sessions with line counts
  echo -e "\n=== Main Sessions ==="
  for f in "$PROJECT_SESSIONS"/*.jsonl; do
    [[ ! -f "$f" ]] && continue
    name=$(basename "$f" .jsonl)
    [[ "$name" =~ ^agent- ]] && continue
    lines=$(wc -l < "$f" | tr -d ' ')
    echo "  $name ($lines entries)"
  done

  # Show agent sessions summary
  echo -e "\n=== Subagent Sessions ==="
  for f in "$PROJECT_SESSIONS"/agent-*.jsonl; do
    [[ ! -f "$f" ]] && continue
    name=$(basename "$f" .jsonl)
    lines=$(wc -l < "$f" | tr -d ' ')
    echo "  $name ($lines entries)"
  done
else
  echo "ERROR: No sessions found for current project" >&2
  echo "  Expected: $PROJECT_SESSIONS" >&2
  echo "" >&2
  echo "Available project folders:" >&2
  ls -1 "$HOME/.claude/projects/" 2>/dev/null | head -10 || echo "  (none)"
  exit 1
fi
FIND_SESSIONS_EOF
```

### Step 3: Verify Required Tools

```bash
/usr/bin/env bash << 'TOOLS_EOF'
set -euo pipefail

# All tools are REQUIRED - fail loudly if missing
MISSING=0

# Check for jq (required for JSONL parsing)
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq not installed (brew install jq)" >&2
  MISSING=1
fi

# Check for brotli (required for compression)
if ! command -v brotli &>/dev/null; then
  echo "ERROR: brotli not installed (brew install brotli)" >&2
  MISSING=1
fi

# Check for aws (required for S3 upload)
if ! command -v aws &>/dev/null; then
  echo "ERROR: aws CLI not installed (brew install awscli)" >&2
  MISSING=1
fi

# Check for op (required for 1Password credential injection)
if ! command -v op &>/dev/null; then
  echo "ERROR: 1Password CLI not installed (brew install 1password-cli)" >&2
  MISSING=1
fi

if [[ $MISSING -eq 1 ]]; then
  echo "" >&2
  echo "PREFLIGHT FAILED: Missing required tools. Install them and retry." >&2
  exit 1
fi

echo "✓ All required tools available: jq, brotli, aws, op"
TOOLS_EOF
```

---

## Part 1: AskUserQuestion Flows

### Flow A: Identify Target for Provenance

When the skill is triggered, first identify what the user wants to trace:

```
AskUserQuestion:
  question: "What do you want to trace provenance for?"
  header: "Target"
  multiSelect: false
  options:
    - label: "Research finding/session"
      description: "Document a research session with full session context for reproducibility"
    - label: "Specific code/feature"
      description: "Trace who created a specific function, feature, or code block"
    - label: "Configuration/decision"
      description: "Trace when and why a configuration or architectural decision was made"
    - label: "Custom search"
      description: "Search session logs for specific keywords or patterns"
```

### Flow B: Confirm GitHub Attribution

**CRITICAL**: Every registry entry MUST have GitHub username attribution.

```
AskUserQuestion:
  question: "Who should be attributed as the creator?"
  header: "Attribution"
  multiSelect: false
  options:
    - label: "Use git config user (Recommended)"
      description: "Attribute to $(git config user.name) / $(git config user.email)"
    - label: "Specify GitHub username"
      description: "I'll provide the GitHub username manually"
    - label: "Team attribution"
      description: "Multiple contributors - list all GitHub usernames"
```

### Flow C: Confirm Session Scope

**CRITICAL**: Default to ALL sessions. Registry must be self-contained.

```
AskUserQuestion:
  question: "Which sessions should be recorded in the registry?"
  header: "Sessions"
  multiSelect: false
  options:
    - label: "ALL sessions (main + subagent) (Recommended)"
      description: "Record every session file - complete provenance for future maintainers"
    - label: "Main sessions only"
      description: "Exclude agent-* subagent sessions (loses context)"
    - label: "Manual selection"
      description: "I'll specify which sessions to include"
```

**IMPORTANT**: Always default to recording ALL sessions. Subagent sessions (`agent-*`)
contain critical context from Explore, Plan, and specialized agents. Omitting them
forces future maintainers to re-run archaeology.

### Flow D: Preview Session Contexts Array

Before writing, show the user exactly what will be recorded:

```
AskUserQuestion:
  question: "Review the session_contexts array that will be recorded:"
  header: "Review"
  multiSelect: false
  options:
    - label: "Looks correct - proceed"
      description: "Write this to the registry"
    - label: "Add descriptions"
      description: "Let me add descriptions to some sessions"
    - label: "Filter some sessions"
      description: "Remove sessions that aren't relevant"
    - label: "Cancel"
      description: "Don't write to registry yet"
```

Display the full session_contexts array before this question:

```json
{
  "session_contexts": [
    {
      "session_uuid": "abc123",
      "type": "main",
      "entries": 980,
      "description": "..."
    },
    {
      "session_uuid": "agent-xyz",
      "type": "subagent",
      "entries": 113,
      "description": "..."
    }
  ]
}
```

### Flow E: Choose Output Format

```
AskUserQuestion:
  question: "What outputs should be generated?"
  header: "Outputs"
  multiSelect: true
  options:
    - label: "registry.jsonl entry (Recommended)"
      description: "Master index entry with ALL session UUIDs and GitHub attribution"
    - label: "iterations.jsonl entries"
      description: "Detailed iteration records in sessions/<id>/"
    - label: "Full session chain archive (.jsonl.br)"
      description: "Compress sessions with Brotli for archival"
    - label: "Markdown finding document"
      description: "findings/<name>.md with embedded provenance table"
    - label: "Git commit with provenance"
      description: "Structured commit message with session references"
    - label: "Upload to S3 for team sharing"
      description: "Upload artifacts to S3 with retrieval command in commit"
```

### Flow F: Link to Existing ADR

When creating a research session registry entry:

```
AskUserQuestion:
  question: "Link this to an existing ADR or design spec?"
  header: "ADR Link"
  multiSelect: false
  options:
    - label: "No ADR link"
      description: "This is standalone or ADR doesn't exist yet"
    - label: "Specify ADR slug"
      description: "Link to an existing ADR (e.g., 2025-12-15-feature-name)"
    - label: "Create new ADR"
      description: "This finding warrants a new ADR"
```

---

## Part 2: Session Archaeology Process

### Step 1: Full Project Scan

Scan ALL session files (main + subagent) to build complete index:

```bash
/usr/bin/env bash << 'SCAN_EOF'
set -euo pipefail

CWD=$(pwd)
ENCODED_PATH=$(echo "$CWD" | tr '/' '-')
PROJECT_SESSIONS="$HOME/.claude/projects/$ENCODED_PATH"

if [[ ! -d "$PROJECT_SESSIONS" ]]; then
  echo "ERROR: Project sessions directory not found: $PROJECT_SESSIONS" >&2
  exit 1
fi

echo "=== Building Session Index ==="
MAIN_COUNT=0
AGENT_COUNT=0

# Main sessions
echo "Main sessions:"
for f in "$PROJECT_SESSIONS"/*.jsonl; do
  [[ ! -f "$f" ]] && continue
  name=$(basename "$f" .jsonl)
  [[ "$name" =~ ^agent- ]] && continue

  lines=$(wc -l < "$f" | tr -d ' ')
  first_ts=$(head -1 "$f" | jq -r '.timestamp // "unknown"') || first_ts="parse-error"
  last_ts=$(tail -1 "$f" | jq -r '.timestamp // "unknown"') || last_ts="parse-error"

  if [[ "$first_ts" == "parse-error" ]]; then
    echo "  WARNING: Failed to parse timestamps in $name" >&2
  fi

  echo "  $name|main|$lines|$first_ts|$last_ts"
  ((MAIN_COUNT++)) || true
done

# Subagent sessions
echo "Subagent sessions:"
for f in "$PROJECT_SESSIONS"/agent-*.jsonl; do
  [[ ! -f "$f" ]] && continue
  name=$(basename "$f" .jsonl)

  lines=$(wc -l < "$f" | tr -d ' ')
  first_ts=$(head -1 "$f" | jq -r '.timestamp // "unknown"') || first_ts="parse-error"

  echo "  $name|subagent|$lines|$first_ts"
  ((AGENT_COUNT++)) || true
done

echo ""
echo "✓ Indexed $MAIN_COUNT main + $AGENT_COUNT subagent sessions"

if [[ $MAIN_COUNT -eq 0 && $AGENT_COUNT -eq 0 ]]; then
  echo "ERROR: No sessions found to index" >&2
  exit 1
fi
SCAN_EOF
```

### Step 2: Build session_contexts Array

**CRITICAL**: This array must contain ALL sessions. Example output:

```json
{
  "session_contexts": [
    {
      "session_uuid": "8c821a19-e4f4-45d5-9338-be3a47ac81a3",
      "type": "main",
      "entries": 980,
      "timestamp_start": "2026-01-03T21:25:07.435Z",
      "description": "Primary session - research iterations, PR preparation"
    },
    {
      "session_uuid": "agent-a728ebe",
      "type": "subagent",
      "entries": 113,
      "timestamp_start": "2026-01-02T07:25:47.658Z",
      "description": "Explore agent - codebase analysis"
    }
  ]
}
```

### Step 3: Trace UUID Chain (Optional)

For detailed provenance of specific edits:

```bash
/usr/bin/env bash << 'TRACE_EOF'
set -euo pipefail

trace_uuid_chain() {
  local uuid="$1"
  local session_file="$2"
  local depth=0
  local max_depth=100

  if [[ -z "$uuid" ]]; then
    echo "ERROR: UUID argument required" >&2
    return 1
  fi

  if [[ ! -f "$session_file" ]]; then
    echo "ERROR: Session file not found: $session_file" >&2
    return 1
  fi

  echo "Tracing UUID chain from: $uuid"

  while [[ -n "$uuid" && $depth -lt $max_depth ]]; do
    # Use jq with explicit error handling
    entry=$(jq -c "select(.uuid == \"$uuid\")" "$session_file" 2>&1) || {
      echo "ERROR: jq failed parsing $session_file" >&2
      return 1
    }

    if [[ -n "$entry" ]]; then
      parent=$(echo "$entry" | jq -r '.parentUuid // empty') || parent=""
      timestamp=$(echo "$entry" | jq -r '.timestamp // "unknown"') || timestamp="unknown"
      type=$(echo "$entry" | jq -r '.type // "unknown"') || type="unknown"

      echo "  [$depth] $uuid ($type) @ $timestamp"
      echo "       -> parent: ${parent:-<root>}"

      uuid="$parent"
      ((depth++)) || true
    else
      echo "  UUID $uuid not in current session, searching others..."
      found=false
      for session in "$PROJECT_SESSIONS"/*.jsonl; do
        [[ ! -f "$session" ]] && continue
        if grep -q "\"uuid\":\"$uuid\"" "$session"; then
          session_file="$session"
          echo "  ✓ Found in $(basename "$session")"
          found=true
          break
        fi
      done
      if [[ "$found" == "false" ]]; then
        echo "  WARNING: UUID chain broken - $uuid not found in any session" >&2
        break
      fi
    fi
  done

  if [[ $depth -ge $max_depth ]]; then
    echo "WARNING: Reached max chain depth ($max_depth) - chain may be incomplete" >&2
  fi

  echo "✓ Chain depth: $depth"
}
TRACE_EOF
```

---

## Part 3: Registry Schema

### registry.jsonl (Master Index)

Each line is a complete, self-contained JSON object:

```json
{
  "id": "2026-01-01-multiyear-momentum",
  "type": "research_session",
  "title": "Multi-Year Cross-Sectional Momentum Strategy Validation",
  "project": "alpha-forge",
  "branch": "feat/2026-01-01-multiyear-cs-momentum-research",
  "created_at": "2026-01-03T01:00:00Z",
  "created_by": {
    "github_username": "terrylica",
    "model": "claude-opus-4-5-20251101",
    "session_uuid": "8c821a19-e4f4-45d5-9338-be3a47ac81a3"
  },
  "strategy_type": "cross_sectional_momentum",
  "date_range": { "start": "2022-01-01", "end": "2025-12-31" },
  "session_contexts": [
    {
      "session_uuid": "8c821a19-...",
      "type": "main",
      "entries": 1128,
      "description": "Primary session - research iterations, PR preparation"
    },
    {
      "session_uuid": "agent-a728ebe",
      "type": "subagent",
      "entries": 113,
      "timestamp_start": "2026-01-02T07:25:47.658Z",
      "description": "Explore agent - codebase analysis"
    }
  ],
  "metrics": {
    "sharpe_2bps": 1.05,
    "sharpe_13bps": 0.31,
    "max_drawdown": -0.18
  },
  "tags": ["momentum", "cross-sectional", "multi-year", "validated"],
  "artifacts": {
    "adr": "docs/adr/2026-01-02-multiyear-momentum-vs-ml.md",
    "strategy_config": "examples/02_strategies/cs_momentum_multiyear.yaml",
    "research_log": "outputs/research_sessions/2026-01-01-multiyear-momentum/research_log.md",
    "iteration_configs": "outputs/research_sessions/2026-01-01-multiyear-momentum/",
    "s3": "s3://eonlabs-findings/sessions/2026-01-01-multiyear-momentum/"
  },
  "status": "validated",
  "finding": "BiLSTM time-series models show no predictive edge (49.05% hit rate). Simple CS momentum outperforms.",
  "recommendation": "Deploy CS Momentum 120+240 strategy. Abandon ML-based approaches for this market regime."
}
```

**Required Fields**:

- `id` - Unique identifier (format: `YYYY-MM-DD-slug`)
- `type` - `research_session` | `finding` | `decision`
- `created_at` - ISO8601 timestamp
- `created_by.github_username` - **MANDATORY** - GitHub username
- `session_contexts` - **MANDATORY** - Array of ALL session UUIDs

**Optional Fields**:

- `title` - Human-readable title
- `project` - Project/repository name
- `branch` - Git branch name
- `strategy_type` - Strategy classification (for research_session type)
- `date_range` - `{start, end}` date range covered
- `metrics` - Key performance metrics object
- `tags` - Searchable tags array
- `artifacts` - Object with paths (see Artifact Paths below)
- `status` - `draft` | `validated` | `production` | `archived`
- `finding` - Summary of what was discovered
- `recommendation` - What to do next

**Artifact Paths**:

| Key                 | Location                               | Purpose                     |
| ------------------- | -------------------------------------- | --------------------------- |
| `adr`               | `docs/adr/...`                         | Committed ADR document      |
| `strategy_config`   | `examples/...`                         | Committed strategy example  |
| `research_log`      | `outputs/research_sessions/.../`       | Gitignored research log     |
| `iteration_configs` | `outputs/research_sessions/.../`       | Gitignored config files     |
| `s3`                | `s3://eonlabs-findings/sessions/<id>/` | S3 archive for team sharing |

### iterations.jsonl (Detailed Records)

Located at `findings/sessions/<id>/iterations.jsonl`. For iteration-level tracking:

```json
{
  "id": "iter-001",
  "registry_id": "2026-01-01-multiyear-momentum",
  "type": "iteration",
  "created_at": "2026-01-01T10:00:00Z",
  "created_by": {
    "github_username": "terrylica",
    "model": "claude-opus-4-5-20251101",
    "session_uuid": "8c821a19-e4f4-45d5-9338-be3a47ac81a3"
  },
  "hypothesis": "Test BiLSTM with conservative clip",
  "config": { "strategy": "bilstm", "clip": 0.05 },
  "results": { "train_sharpe": 0.31, "test_sharpe": -1.15 },
  "finding": "BiLSTM shows no edge",
  "status": "FAILED"
}
```

---

## Part 4: Output Generation

### Compressed Session Context

For archival, compress sessions with Brotli:

```bash
/usr/bin/env bash << 'COMPRESS_EOF'
set -euo pipefail

# Validate required variables
if [[ -z "${TARGET_ID:-}" ]]; then
  echo "ERROR: TARGET_ID variable not set" >&2
  exit 1
fi

if [[ -z "${SESSION_LIST:-}" ]]; then
  echo "ERROR: SESSION_LIST variable not set" >&2
  exit 1
fi

if [[ -z "${PROJECT_SESSIONS:-}" ]]; then
  echo "ERROR: PROJECT_SESSIONS variable not set" >&2
  exit 1
fi

OUTPUT_DIR="outputs/research_sessions/${TARGET_ID}"
mkdir -p "$OUTPUT_DIR" || {
  echo "ERROR: Failed to create output directory: $OUTPUT_DIR" >&2
  exit 1
}
# NOTE: This directory is gitignored. Artifacts are preserved in S3, not git.

# Compress each session
ARCHIVED_COUNT=0
FAILED_COUNT=0

for session_id in $SESSION_LIST; do
  SESSION_PATH="$PROJECT_SESSIONS/${session_id}.jsonl"
  if [[ -f "$SESSION_PATH" ]]; then
    if brotli -9 -o "$OUTPUT_DIR/${session_id}.jsonl.br" "$SESSION_PATH"; then
      echo "✓ Archived: ${session_id}"
      ((ARCHIVED_COUNT++)) || true
    else
      echo "ERROR: Failed to compress ${session_id}" >&2
      ((FAILED_COUNT++)) || true
    fi
  else
    echo "WARNING: Session file not found: $SESSION_PATH" >&2
  fi
done

if [[ $ARCHIVED_COUNT -eq 0 ]]; then
  echo "ERROR: No sessions were archived" >&2
  exit 1
fi

if [[ $FAILED_COUNT -gt 0 ]]; then
  echo "ERROR: $FAILED_COUNT session(s) failed to compress" >&2
  exit 1
fi

# Create manifest with proper JSON
cat > "$OUTPUT_DIR/manifest.json" << MANIFEST
{
  "target_id": "$TARGET_ID",
  "sessions_archived": $ARCHIVED_COUNT,
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
MANIFEST

echo "✓ Archived $ARCHIVED_COUNT sessions to $OUTPUT_DIR"
COMPRESS_EOF
```

### Git Commit Message Template

```
feat(finding): <short description>

Session-Chronicle Provenance:
registry_id: <registry_id>
github_username: <github_username>
main_sessions: <count>
subagent_sessions: <count>
total_entries: <total>

Artifacts:
- findings/registry.jsonl
- findings/sessions/<id>/iterations.jsonl
- S3: s3://eonlabs-findings/sessions/<id>/

## S3 Artifact Retrieval

# Download compressed artifacts from S3
export AWS_ACCESS_KEY_ID=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id")
export AWS_SECRET_ACCESS_KEY=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/secret access key")
export AWS_DEFAULT_REGION="us-west-2"
aws s3 sync s3://eonlabs-findings/sessions/<id>/ ./artifacts/
for f in ./artifacts/*.br; do brotli -d "$f"; done

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Part 5: Confirmation Workflow

### Final Confirmation Before Write

**ALWAYS** show the user what will be written before appending:

```
AskUserQuestion:
  question: "Ready to write to registry. Confirm the entry:"
  header: "Confirm"
  multiSelect: false
  options:
    - label: "Write to registry"
      description: "Append this entry to findings/registry.jsonl"
    - label: "Edit first"
      description: "Let me modify some fields before writing"
    - label: "Cancel"
      description: "Don't write anything"
```

Before this question, display:

1. Full JSON entry (pretty-printed)
2. Count of session_contexts entries
3. GitHub username attribution
4. Target file path

### Post-Write Verification

After writing, verify:

```bash
# Validate NDJSON format
tail -1 findings/registry.jsonl | jq . > /dev/null && echo "Valid JSON"

# Show what was written
echo "Entry added:"
tail -1 findings/registry.jsonl | jq '.id, .created_by.github_username, (.session_contexts | length)'
```

---

## Part 6: Workflow Summary

```
1. PREFLIGHT
   ├── Verify session storage location
   ├── Find ALL sessions (main + subagent)
   └── Check required tools (jq, brotli)

2. ASK: TARGET TYPE
   └── AskUserQuestion: What to trace?

3. ASK: GITHUB ATTRIBUTION
   └── AskUserQuestion: Who created this?

4. ASK: SESSION SCOPE
   └── AskUserQuestion: Which sessions? (Default: ALL)

5. BUILD session_contexts ARRAY
   ├── Enumerate ALL main sessions
   ├── Enumerate ALL subagent sessions
   └── Collect metadata (entries, timestamps)

6. ASK: PREVIEW session_contexts
   └── AskUserQuestion: Review before writing

7. ASK: OUTPUT FORMAT
   └── AskUserQuestion: What to generate?

8. ASK: ADR LINK
   └── AskUserQuestion: Link to ADR?

9. GENERATE OUTPUTS
   ├── Build registry.jsonl entry (with iterations_path, iterations_count)
   ├── Build iterations.jsonl entries (if applicable)
   └── Prepare commit message

10. ASK: FINAL CONFIRMATION
    └── AskUserQuestion: Ready to write?

11. WRITE & VERIFY
    ├── Append to registry.jsonl
    ├── Append to sessions/<id>/iterations.jsonl
    └── Validate NDJSON format

12. (OPTIONAL) S3 UPLOAD
    └── Upload compressed archives
```

---

## Success Criteria

1. **Complete session enumeration** - ALL main + subagent sessions recorded
2. **GitHub attribution** - `created_by.github_username` always present
3. **Self-contained registry** - Future maintainers don't need archaeology
4. **User confirmation** - Every step has AskUserQuestion confirmation
5. **Valid NDJSON** - All entries pass `jq` validation
6. **Reproducible** - Session UUIDs enable full context retrieval

---

## References

- [S3 Sharing ADR](/docs/adr/2026-01-02-session-chronicle-s3-sharing.md)
- [S3 Retrieval Guide](./references/s3-retrieval-guide.md)
- [NDJSON Specification](https://github.com/ndjson/ndjson-spec)
- [jq Manual](https://jqlang.github.io/jq/manual/)
- [Brotli Compression](https://github.com/google/brotli)
