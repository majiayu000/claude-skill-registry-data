---
name: session-guidance
description: Configure Ralph loop guidance. TRIGGERS - session guidance, loop configuration, forbidden items.
allowed-tools: Bash, Read, AskUserQuestion, Write
---

# Session Guidance Skill

Configure Ralph loop session guidance through AskUserQuestion flows. Loads constraint scan results, presents dynamic options based on severity, and writes guidance to config.

## When to Use

- Invoked by `/ralph:start` Step 1.6 via Skill tool
- User asks to reconfigure Ralph guidance
- User mentions "forbidden items" or "encouraged items"

## Prerequisites

- Step 1.4 constraint scan completed (`.claude/ralph-constraint-scan.jsonl` exists)
- Step 1.5 preset confirmation completed

## Workflow Overview

```
1.6.1: Check for Previous Guidance
         ↓
1.6.2: Binary Keep/Reconfigure (if guidance exists)
         ↓
1.6.2.5: Load Constraint Scan Results (NDJSON)
         ↓
1.6.3: Forbidden Items (multiSelect, DYNAMIC from constraints)
         ↓
1.6.4: Custom Forbidden (follow-up)
         ↓
1.6.5: Encouraged Items (multiSelect, closed list)
         ↓
1.6.6: Custom Encouraged (follow-up)
         ↓
1.6.7: Update Config (with validation + learned behavior)
```

---

## Step 1.6.1: Check for Previous Guidance

Check if guidance exists in the config file:

```bash
/usr/bin/env bash << 'CHECK_GUIDANCE_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
GUIDANCE_EXISTS="false"
if [[ -f "$PROJECT_DIR/.claude/ralph-config.json" ]]; then
    GUIDANCE_EXISTS=$(jq -r 'if .guidance then "true" else "false" end' "$PROJECT_DIR/.claude/ralph-config.json" 2>/dev/null || echo "false")
fi
echo "GUIDANCE_EXISTS=$GUIDANCE_EXISTS"
CHECK_GUIDANCE_SCRIPT
```

---

## Step 1.6.2: Binary Keep/Reconfigure (Conditional)

**If `GUIDANCE_EXISTS == "true"`:**

Use AskUserQuestion:

- question: "Previous session had custom guidance. Keep it or reconfigure?"
  header: "Guidance"
  options:
  - label: "Keep existing guidance (Recommended)"
    description: "Use stored forbidden/encouraged lists from last session"
  - label: "Reconfigure guidance"
    description: "Set new forbidden/encouraged lists"
    multiSelect: false

- If "Keep existing" → **STOP skill execution** (guidance already in config, return to start.md Step 2)
- If "Reconfigure" → Continue to Step 1.6.2.5

**If `GUIDANCE_EXISTS == "false"` (first run):**

Proceed directly to Step 1.6.2.5. No user prompt needed.

---

## Step 1.6.2.5: Load Constraint Scan Results (NDJSON)

**Purpose**: Load constraint scan results in NDJSON format, filtering out previously acknowledged constraints.

**Learned behavior**: Constraints the user previously selected as "forbidden" are stored in `.claude/ralph-acknowledged-constraints.jsonl` and filtered from future displays.

```bash
/usr/bin/env bash << 'LOAD_SCAN_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
SCAN_FILE="$PROJECT_DIR/.claude/ralph-constraint-scan.jsonl"
ACK_FILE="$PROJECT_DIR/.claude/ralph-acknowledged-constraints.jsonl"

if [[ -f "$SCAN_FILE" ]]; then
    # Load acknowledged constraint IDs (if file exists)
    ACKNOWLEDGED_IDS=""
    if [[ -f "$ACK_FILE" ]]; then
        ACKNOWLEDGED_IDS=$(jq -r 'select(._type == "constraint") | .id' "$ACK_FILE" 2>/dev/null | tr '\n' '|' | sed 's/|$//')
        ACK_COUNT=$(grep -c '"_type":"constraint"' "$ACK_FILE" 2>/dev/null || echo "0")
        echo "=== ACKNOWLEDGED CONSTRAINTS ==="
        echo "Previously acknowledged: $ACK_COUNT constraints (filtered from display)"
        echo ""
    fi

    # NDJSON format: each line is a JSON object with _type field
    # Filter out acknowledged constraints and count by severity
    if [[ -n "$ACKNOWLEDGED_IDS" ]]; then
        FILTERED=$(grep '"_type":"constraint"' "$SCAN_FILE" 2>/dev/null | \
            jq -c --arg ack_pattern "$ACKNOWLEDGED_IDS" 'select(.id | test($ack_pattern) | not)' 2>/dev/null)
    else
        FILTERED=$(grep '"_type":"constraint"' "$SCAN_FILE" 2>/dev/null)
    fi

    # Count by severity (from filtered NDJSON lines)
    CRITICAL_COUNT=$(echo "$FILTERED" | jq -s '[.[] | select(.severity == "critical")] | length' 2>/dev/null || echo "0")
    HIGH_COUNT=$(echo "$FILTERED" | jq -s '[.[] | select(.severity == "high")] | length' 2>/dev/null || echo "0")
    MEDIUM_COUNT=$(echo "$FILTERED" | jq -s '[.[] | select(.severity == "medium")] | length' 2>/dev/null || echo "0")
    LOW_COUNT=$(echo "$FILTERED" | jq -s '[.[] | select(.severity == "low")] | length' 2>/dev/null || echo "0")
    TOTAL_COUNT=$((CRITICAL_COUNT + HIGH_COUNT + MEDIUM_COUNT + LOW_COUNT))
    BUSYWORK_COUNT=$(grep -c '"_type":"busywork"' "$SCAN_FILE" 2>/dev/null || echo "0")

    echo "=== CONSTRAINT SCAN SUMMARY ==="
    echo "SEVERITY_COUNTS: critical=$CRITICAL_COUNT high=$HIGH_COUNT medium=$MEDIUM_COUNT low=$LOW_COUNT total=$TOTAL_COUNT"
    echo "BUSYWORK_COUNT: $BUSYWORK_COUNT"
    echo ""
    echo "=== CONSTRAINTS (NDJSON) ==="
    echo "$FILTERED"
    echo ""
    echo "=== BUSYWORK CATEGORIES (NDJSON) ==="
    grep '"_type":"busywork"' "$SCAN_FILE" 2>/dev/null
    echo ""
    echo "=== END SCAN RESULTS ==="
else
    echo "=== CONSTRAINT SCAN SUMMARY ==="
    echo "SEVERITY_COUNTS: critical=0 high=0 medium=0 low=0 total=0"
    echo "BUSYWORK_COUNT: 0"
    echo "=== NO SCAN FILE FOUND ==="
fi
LOAD_SCAN_SCRIPT
```

**Claude MUST parse this output**:

1. **Extract severity counts** from `SEVERITY_COUNTS:` line for question text
2. **Parse NDJSON constraints** between `=== CONSTRAINTS (NDJSON) ===` and `=== BUSYWORK CATEGORIES ===`
3. **Parse NDJSON busywork** between `=== BUSYWORK CATEGORIES (NDJSON) ===` and `=== END SCAN RESULTS ===`
4. **Build dynamic AUQ options** with constraint-derived items first, then static fallbacks

**NDJSON constraint format** (one per line):

```json
{
  "id": "hardcoded-001",
  "severity": "high",
  "category": "hardcoded_path",
  "description": "Hardcoded path: /Users/terryli/...",
  "file": "pyproject.toml",
  "line": 15,
  "recommendation": "Use environment variable"
}
```

---

## Step 1.6.3: Forbidden Items (multiSelect, DYNAMIC)

**MANDATORY: Build options dynamically from Step 1.6.2.5 output**

**AUQ Limit**: Maximum 4 options total. Priority order:

1. CRITICAL severity constraints (up to 2)
2. HIGH severity constraints (up to 2)
3. If <4 constraint options, fill with static categories

**Algorithm** - Claude MUST execute this logic:

```
Step 1: Parse severity counts from SEVERITY_COUNTS line
  - Extract: critical=N, high=M, total=T

Step 2: Build constraint options (max 4, severity priority)
  options = []

  # First: CRITICAL constraints (max 2)
  for each NDJSON line where severity == "critical":
    if len(options) >= 2: break
    options.append({
      label: description[:55] + "..." if len > 55 else description,
      description: "(CRITICAL) " + file + ":" + line + " - " + recommendation[:40]
    })

  # Second: HIGH constraints (max 2 more)
  for each NDJSON line where severity == "high":
    if len(options) >= 4: break
    options.append({
      label: description[:55] + "..." if len > 55 else description,
      description: "(HIGH) " + file + ":" + line + " - " + recommendation[:40]
    })

  # Third: Fill remaining with static categories
  static_categories = ["Documentation updates", "Dependency upgrades", "Refactoring", "CI/CD modifications"]
  while len(options) < 4 and static_categories:
    options.append(static_categories.pop(0))

Step 3: Build question text
  if critical > 0 or high > 0:
    question = "What should Ralph avoid? ({critical} critical, {high} high detected)"
  else:
    question = "What should Ralph avoid? (no high-severity constraints)"
```

**Example transformation**:

NDJSON input:

```
{"severity":"critical","description":"Hardcoded API key in config.py","file":"config.py","line":42,"recommendation":"Move to env var"}
{"severity":"high","description":"Circular import: core ↔ utils","file":"core.py","line":1,"recommendation":"Extract interface"}
```

Becomes AUQ options:

```yaml
options:
  - label: "Hardcoded API key in config.py"
    description: "(CRITICAL) config.py:42 - Move to env var"
  - label: "Circular import: core ↔ utils"
    description: "(HIGH) core.py:1 - Extract interface"
  - label: "Documentation updates"
    description: "README, CHANGELOG, docstrings, comments"
  - label: "Dependency upgrades"
    description: "Version bumps, renovate PRs, package updates"
```

Use AskUserQuestion with the dynamically built options above.

**Static fallback categories** (used when no constraints or to fill remaining slots):

- "Documentation updates" - "README, CHANGELOG, docstrings, comments"
- "Dependency upgrades" - "Version bumps, renovate PRs, package updates"
- "Refactoring" - "Code restructuring without behavior change"
- "CI/CD modifications" - "Workflow files, GitHub Actions, pipelines"

**If total=0**: Show only 4 static categories with question `"What should Ralph avoid? (no constraints detected)"`

---

## Step 1.6.4: Custom Forbidden (Follow-up)

After multiSelect, ask for custom additions:

Use AskUserQuestion:

- question: "Add custom forbidden items? (comma-separated)"
  header: "Custom"
  multiSelect: false
  options:
  - label: "Enter custom items"
    description: "Type additional forbidden phrases, e.g., 'database migrations, API changes'"
  - label: "Skip custom items"
    description: "Use only selected categories above"

If "Enter custom items" selected → Parse user's "Other" input, split by comma, trim whitespace.

---

## Step 1.6.5: Encouraged Items (multiSelect, closed list)

Use AskUserQuestion:

- question: "What should Ralph prioritize? (Select all that apply)"
  header: "Encouraged"
  multiSelect: true
  options:
  - label: "ROADMAP P0 items"
    description: "Highest priority tasks from project roadmap"
  - label: "Performance improvements"
    description: "Speed, memory, efficiency optimizations"
  - label: "Bug fixes"
    description: "Fix known issues and regressions"
  - label: "Research experiments"
    description: "Try new approaches (Alpha Forge /research)"

---

## Step 1.6.6: Custom Encouraged (Follow-up)

Same pattern as 1.6.4:

Use AskUserQuestion:

- question: "Add custom encouraged items? (comma-separated)"
  header: "Custom"
  multiSelect: false
  options:
  - label: "Enter custom items"
    description: "Type additional encouraged phrases, e.g., 'Sharpe ratio, feature engineering'"
  - label: "Skip custom items"
    description: "Use only selected categories above"

---

## Step 1.6.7: Update Config (with Validation + Learned Behavior)

**IMPORTANT**: After collecting responses from Steps 1.6.3-1.6.6, you MUST:

1. Write guidance to config WITH validation
2. Append constraint-derived selections to `.jsonl` for learned filtering

3. **Collect responses** from the AUQ steps above:
   - `FORBIDDEN_ITEMS`: Selected labels from 1.6.3 + custom items from 1.6.4 (if any)
   - `ENCOURAGED_ITEMS`: Selected labels from 1.6.5 + custom items from 1.6.6 (if any)
   - `SELECTED_CONSTRAINT_IDS`: IDs of constraint-derived options user selected (from NDJSON parsing)

4. **Write to config with post-write validation** using the Bash tool (substitute actual values):

```bash
/usr/bin/env bash << 'GUIDANCE_WRITE_SCRIPT'
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
CONFIG_FILE="$PROJECT_DIR/.claude/ralph-config.json"
SCAN_FILE="$PROJECT_DIR/.claude/ralph-constraint-scan.jsonl"
ACK_FILE="$PROJECT_DIR/.claude/ralph-acknowledged-constraints.jsonl"
BACKUP_FILE="${CONFIG_FILE}.backup"

# Substitute these with actual AUQ responses:
FORBIDDEN_JSON='["Documentation updates", "Dependency upgrades"]'  # From 1.6.3 + 1.6.4
ENCOURAGED_JSON='["ROADMAP P0 items", "Research experiments"]'     # From 1.6.5 + 1.6.6

# Substitute with constraint IDs user selected (from NDJSON constraint options)
SELECTED_CONSTRAINT_IDS="hardcoded-001 hardcoded-002"  # From 1.6.3 constraint-derived selections

# Generate timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Load constraint scan data (if exists) for persistence
CONSTRAINT_SCAN_JSON='null'
if [[ -f "$SCAN_FILE" ]]; then
    METADATA=$(grep '"_type":"metadata"' "$SCAN_FILE" 2>/dev/null | head -1)
    CONSTRAINTS=$(grep '"_type":"constraint"' "$SCAN_FILE" 2>/dev/null | jq -s '.' 2>/dev/null || echo '[]')
    BUSYWORK=$(grep '"_type":"busywork"' "$SCAN_FILE" 2>/dev/null | jq -s '.' 2>/dev/null || echo '[]')

    CONSTRAINT_SCAN_JSON=$(jq -n \
        --argjson metadata "$METADATA" \
        --argjson constraints "$CONSTRAINTS" \
        --argjson busywork "$BUSYWORK" \
        '{
            scan_timestamp: $metadata.scan_timestamp,
            project_dir: $metadata.project_dir,
            worktree_type: $metadata.worktree_type,
            constraints: $constraints,
            builtin_busywork: $busywork
        }' 2>/dev/null || echo 'null')
fi

# Create backup before write
mkdir -p "$PROJECT_DIR/.claude"
if [[ -f "$CONFIG_FILE" ]]; then
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# Write config
if [[ -f "$CONFIG_FILE" ]]; then
    jq --argjson forbidden "$FORBIDDEN_JSON" \
       --argjson encouraged "$ENCOURAGED_JSON" \
       --arg timestamp "$TIMESTAMP" \
       --argjson constraint_scan "$CONSTRAINT_SCAN_JSON" \
       '.guidance = {forbidden: $forbidden, encouraged: $encouraged, timestamp: $timestamp} | .constraint_scan = $constraint_scan' \
       "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
else
    jq -n --argjson forbidden "$FORBIDDEN_JSON" \
          --argjson encouraged "$ENCOURAGED_JSON" \
          --arg timestamp "$TIMESTAMP" \
          --argjson constraint_scan "$CONSTRAINT_SCAN_JSON" \
          '{version: "3.0.0", guidance: {forbidden: $forbidden, encouraged: $encouraged, timestamp: $timestamp}, constraint_scan: $constraint_scan}' \
          > "$CONFIG_FILE"
fi

# === LEARNED BEHAVIOR: Append to .jsonl ===
if [[ -n "$SELECTED_CONSTRAINT_IDS" && -f "$SCAN_FILE" ]]; then
    for CONSTRAINT_ID in $SELECTED_CONSTRAINT_IDS; do
        if [[ -f "$ACK_FILE" ]] && grep -q "\"id\":\"$CONSTRAINT_ID\"" "$ACK_FILE" 2>/dev/null; then
            continue
        fi
        CONSTRAINT_DATA=$(grep "\"id\":\"$CONSTRAINT_ID\"" "$SCAN_FILE" 2>/dev/null | head -1 | \
            jq -c --arg ts "$TIMESTAMP" '. + {acknowledged_at: $ts}' 2>/dev/null)
        if [[ -n "$CONSTRAINT_DATA" ]]; then
            echo "$CONSTRAINT_DATA" >> "$ACK_FILE"
        fi
    done
    NEW_ACK_COUNT=$(echo "$SELECTED_CONSTRAINT_IDS" | wc -w | tr -d ' ')
    echo "=== LEARNED BEHAVIOR ==="
    echo "Appended $NEW_ACK_COUNT constraint(s) to $ACK_FILE"
fi

# === POST-WRITE VALIDATION ===
validate_config() {
    local file="$1"
    [[ -f "$file" && -r "$file" ]] || return 1
    jq empty "$file" >/dev/null 2>&1 || return 2
    jq -e '.guidance.forbidden and .guidance.encouraged and .guidance.timestamp' "$file" >/dev/null 2>&1 || return 3
    jq -e '.guidance.forbidden | type == "array"' "$file" >/dev/null 2>&1 || return 4
    jq -e '.guidance.encouraged | type == "array"' "$file" >/dev/null 2>&1 || return 5
    return 0
}

if validate_config "$CONFIG_FILE"; then
    echo "✓ Guidance saved to $CONFIG_FILE"
    echo ""
    echo "=== VALIDATION PASSED ==="
    jq '{guidance: .guidance}' "$CONFIG_FILE"
    rm -f "$BACKUP_FILE"
else
    VALIDATION_ERROR=$?
    echo "✗ VALIDATION FAILED (error code: $VALIDATION_ERROR)"
    echo "=== ROLLING BACK ==="
    if [[ -f "$BACKUP_FILE" ]]; then
        mv "$BACKUP_FILE" "$CONFIG_FILE"
        echo "Restored previous config from backup"
    else
        rm -f "$CONFIG_FILE"
        echo "Removed invalid config"
    fi
    exit 1
fi
GUIDANCE_WRITE_SCRIPT
```

**Key substitutions Claude MUST make**:

- `FORBIDDEN_JSON`: Array of selected forbidden labels
- `ENCOURAGED_JSON`: Array of selected encouraged labels
- `SELECTED_CONSTRAINT_IDS`: Space-separated list of constraint IDs from NDJSON options user selected

---

## Output

After completing all steps, the skill returns control to `/ralph:start` Step 2 (Execution).

The config file `.claude/ralph-config.json` will contain:

```json
{
  "version": "3.0.0",
  "guidance": {
    "forbidden": ["Documentation updates", "..."],
    "encouraged": ["ROADMAP P0 items", "..."],
    "timestamp": "2026-01-01T00:00:00Z"
  },
  "constraint_scan": { ... }
}
```
