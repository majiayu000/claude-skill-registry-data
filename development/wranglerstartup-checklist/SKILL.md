---
name: wrangler:startup-checklist
description: Validates project wrangler version on session start, detects breaking changes, and recommends updates
---

# Startup Checklist Skill

## Skill Usage Announcement

**MANDATORY**: When using this skill, announce it at the start with:

```
🔧 Using Skill: wrangler:startup-checklist | [brief purpose based on context]
```

**Example:**
```
🔧 Using Skill: wrangler:startup-checklist | [Provide context-specific example of what you're doing]
```

This creates an audit trail showing which skills were applied during the session.



## Purpose

Run automatically on session start to ensure project is using current wrangler version. Detects breaking changes and provides clear upgrade path.

## When to Use

This skill runs automatically via session hooks. DO NOT manually invoke unless debugging version detection.

**Auto-execution**: Triggered by `hooks/session-start.sh` after workspace initialization.

## Workflow

### Phase 1: Read Project Version

**Goal**: Determine which version of wrangler the project is currently using.

1. **Locate Constitution File**

   Check locations in priority order:

   ```bash
   # Priority 1: New location (v1.1.0+)
   if [ -f ".wrangler/governance/CONSTITUTION.md" ]; then
     PROJECT_CONSTITUTION=".wrangler/governance/CONSTITUTION.md"

   # Priority 2: Legacy location (v1.0.0)
   elif [ -f "specifications/_CONSTITUTION.md" ]; then
     PROJECT_CONSTITUTION="specifications/_CONSTITUTION.md"

   # No constitution found
   else
     echo "⚠️ No constitution found. Initialize governance first."
     echo "   Run: /wrangler:initialize-governance"
     exit with WARN status
   fi
   ```

2. **Extract Version from Frontmatter**

   Read YAML frontmatter and extract `wranglerVersion` field:

   ```yaml
   ---
   wranglerVersion: "1.1.0"
   lastUpdated: "2025-11-18"
   ---
   ```

   **Fallback behavior**:
   - If `wranglerVersion` field missing → Assume `v1.0.0` (pre-versioning era)
   - If frontmatter entirely missing → Assume `v1.0.0`
   - If file exists but is empty → WARN and exit

3. **Validate Version Format**

   Ensure version follows semantic versioning (e.g., "1.1.0", "2.0.0"):
   - Pattern: `MAJOR.MINOR.PATCH`
   - Valid: "1.0.0", "1.1.0", "2.0.0"
   - Invalid: "1", "1.1", "v1.0.0", "latest"

   If invalid:
   ```
   ⚠️ Invalid version format in constitution: {version}
      Expected: X.Y.Z (e.g., 1.1.0)
      Fix constitution frontmatter and restart session
   ```

### Phase 2: Read Current Wrangler Version

**Goal**: Determine latest available wrangler version.

1. **Locate Plugin Directory**

   Find wrangler plugin installation:
   - Read `.claude-plugin/plugin.json` to get plugin path
   - Navigate to plugin root directory
   - Locate `skills/.wrangler-releases/CURRENT_VERSION`

2. **Read CURRENT_VERSION File**

   ```bash
   # Expected location (relative to plugin root)
   CURRENT_VERSION_FILE="skills/.wrangler-releases/CURRENT_VERSION"

   if [ ! -f "$CURRENT_VERSION_FILE" ]; then
     echo "⚠️ Cannot detect wrangler version. Plugin may be corrupted."
     echo "   Expected: $CURRENT_VERSION_FILE"
     echo "   Action: Reinstall wrangler plugin"
     exit with WARN status
   fi

   CURRENT_VERSION=$(cat "$CURRENT_VERSION_FILE" | tr -d '[:space:]')
   ```

3. **Validate Current Version**

   Same validation as project version (semantic versioning check).

### Phase 3: Compare Versions

**Goal**: Determine if project is up to date, behind, or ahead.

```bash
compare_versions() {
  local project_ver="$1"
  local current_ver="$2"

  # Parse versions (split on '.')
  IFS='.' read -r -a project <<< "$project_ver"
  IFS='.' read -r -a current <<< "$current_ver"

  # Compare major version
  if [ "${project[0]}" -lt "${current[0]}" ]; then
    return 1  # project < current
  elif [ "${project[0]}" -gt "${current[0]}" ]; then
    return 2  # project > current
  fi

  # Compare minor version
  if [ "${project[1]}" -lt "${current[1]}" ]; then
    return 1  # project < current
  elif [ "${project[1]}" -gt "${current[1]}" ]; then
    return 2  # project > current
  fi

  # Compare patch version
  if [ "${project[2]}" -lt "${current[2]}" ]; then
    return 1  # project < current
  elif [ "${project[2]}" -gt "${current[2]}" ]; then
    return 2  # project > current
  fi

  return 0  # project == current
}

compare_versions "$PROJECT_VERSION" "$CURRENT_VERSION"
result=$?

case $result in
  0)
    # Versions match - SUCCESS
    → Skip to Phase 5 (report SUCCESS)
    ;;
  1)
    # Project behind current - check breaking changes
    → Continue to Phase 4
    ;;
  2)
    # Project ahead of current - unusual case
    → Skip to Phase 5 (report WARN - unusual state)
    ;;
esac
```

### Phase 4: Check for Breaking Changes

**Goal**: Determine if version gap includes breaking changes requiring migration.

1. **List Version Gap**

   Generate list of all versions between project and current:

   ```bash
   # Example: If project=1.0.0, current=1.3.0
   # Gap versions: [1.1.0, 1.2.0, 1.3.0]

   get_version_gap() {
     local start="$1"
     local end="$2"

     # Parse versions
     IFS='.' read -r -a start_parts <<< "$start"
     IFS='.' read -r -a end_parts <<< "$end"

     # Simple approach: List all release notes between versions
     # (Assumes sequential versioning - minor version increments)

     versions=()

     # For each potential version, check if release note exists
     for minor in $(seq $((start_parts[1] + 1)) ${end_parts[1]}); do
       candidate="${start_parts[0]}.${minor}.0"
       if [ -f "skills/.wrangler-releases/${candidate}.md" ]; then
         versions+=("$candidate")
       fi
     done

     echo "${versions[@]}"
   }

   GAP_VERSIONS=$(get_version_gap "$PROJECT_VERSION" "$CURRENT_VERSION")
   ```

2. **Parse Release Notes**

   For each version in gap, read frontmatter and check `breakingChanges` field:

   ```bash
   check_breaking_changes() {
     local versions=("$@")
     local breaking_versions=()

     for version in "${versions[@]}"; do
       release_note="skills/.wrangler-releases/${version}.md"

       if [ ! -f "$release_note" ]; then
         echo "⚠️ Missing release note: $release_note"
         continue
       fi

       # Extract frontmatter 'breakingChanges' field
       breaking=$(grep "^breakingChanges:" "$release_note" | awk '{print $2}')

       if [ "$breaking" = "true" ]; then
         breaking_versions+=("$version")
       fi
     done

     echo "${breaking_versions[@]}"
   }

   BREAKING_VERSIONS=$(check_breaking_changes $GAP_VERSIONS)
   ```

3. **Categorize Status**

   ```bash
   if [ -z "$BREAKING_VERSIONS" ]; then
     # No breaking changes - optional updates
     STATUS="WARN"
     MESSAGE="Non-breaking updates available"
   else
     # Breaking changes exist - migration required
     STATUS="OUTDATED"
     MESSAGE="Breaking changes detected - migration required"
   fi
   ```

### Phase 5: Report Status

**Goal**: Provide clear, actionable output to user.

#### SUCCESS Output

```
✅ Wrangler version up to date (v1.1.0)
   All systems ready.
```

**When**: Project version == Current version

**Exit code**: 0

---

#### WARN Output (Non-Breaking Updates)

```
⚠️ New wrangler version available
   Project: v1.1.0
   Latest:  v1.2.0
   Releases behind: 1

   Updates include:
   - New skills: [list from release notes]
   - Enhancements: [summary from release notes]

   No breaking changes detected.
   Update is optional but recommended.

   To update: Run /update-yourself
```

**When**: Project version < Current version AND no breaking changes in gap

**Exit code**: 0

**Details to include**:
- Specific versions being compared
- Number of releases behind
- High-level summary of new features (from release notes)
- Clear call to action

---

#### OUTDATED Output (Breaking Changes)

```
❌ Wrangler version outdated - breaking changes detected
   Project: v1.0.0
   Latest:  v1.1.0
   Releases behind: 1

   Breaking changes in:
   - v1.1.0: Directory structure refactored to .wrangler/

   MIGRATION REQUIRED

   Summary of breaking changes:
   • All governance files moved from root to .wrangler/
   • Constitution now requires wranglerVersion frontmatter
   • MCP server paths updated

   To migrate: Run /update-yourself
   To skip version check: Set WRANGLER_SKIP_VERSION_CHECK=true

   WARNING: Skipping migration may cause governance features to fail.
```

**When**: Project version < Current version AND breaking changes exist in gap

**Exit code**: 0 (still allow session to start)

**Details to include**:
- Specific versions being compared
- Number of releases behind
- List of versions with breaking changes
- High-level summary of WHAT broke (from release notes)
- Clear migration path
- Escape hatch (skip flag) for emergencies

---

#### WARN Output (Project Ahead of Plugin)

```
⚠️ Unusual version state detected
   Project: v2.0.0
   Plugin:  v1.1.0

   Your project reports a newer wrangler version than the plugin.

   Possible causes:
   - Plugin needs updating (check for new plugin version)
   - Constitution frontmatter manually edited incorrectly
   - Project uses unreleased wrangler features

   Recommended actions:
   1. Check if wrangler plugin has updates available
   2. Verify constitution frontmatter is correct
   3. Report issue if problem persists
```

**When**: Project version > Current version

**Exit code**: 0

---

#### ERROR Output (Constitution Missing)

```
⚠️ No constitution found. Initialize governance first.

   Expected locations:
   - .wrangler/governance/CONSTITUTION.md (v1.1.0+)
   - specifications/_CONSTITUTION.md (v1.0.0)

   To initialize: Run /wrangler:initialize-governance

   Skipping version check until governance initialized.
```

**When**: No constitution found in either location

**Exit code**: 0 (allow session to start)

---

#### ERROR Output (Plugin Corrupted)

```
⚠️ Cannot detect wrangler version. Plugin may be corrupted.
   Expected: skills/.wrangler-releases/CURRENT_VERSION
   Found: [none]

   Recommended actions:
   1. Reinstall wrangler plugin
   2. Check plugin installation directory
   3. Report issue if reinstall doesn't fix

   Skipping version check until plugin repaired.
```

**When**: CURRENT_VERSION file missing from plugin

**Exit code**: 0

## Completion Signals

Return one of three statuses:

1. **SUCCESS**: Project fully upgraded, no action needed
2. **WARN**: Updates available OR unusual state, but not critical
3. **OUTDATED**: Breaking changes detected, migration strongly recommended

**All statuses exit with code 0** to allow session to start normally.

## Error Handling

### Constitution Missing

**Scenario**: Neither `.wrangler/governance/CONSTITUTION.md` nor `specifications/_CONSTITUTION.md` exists

**Output**: ERROR message (see Phase 5)

**Signal**: WARN

**Action**: Recommend `/wrangler:initialize-governance`

**Allow session**: Yes (exit 0)

---

### CURRENT_VERSION Missing

**Scenario**: Plugin installation missing `skills/.wrangler-releases/CURRENT_VERSION`

**Output**: ERROR message (see Phase 5)

**Signal**: WARN

**Action**: Recommend reinstalling plugin

**Allow session**: Yes (exit 0)

---

### Invalid Version Format

**Scenario**: Constitution has `wranglerVersion: "invalid"` or `wranglerVersion: "v1.0.0"` (leading 'v')

**Output**:
```
⚠️ Invalid version format in constitution: {version}
   Expected: X.Y.Z (e.g., 1.1.0)
   Found: {actual_value}

   Fix constitution frontmatter:
   ---
   wranglerVersion: "1.1.0"  # Correct format
   ---

   Assuming v1.0.0 for now.
```

**Signal**: WARN

**Fallback**: Assume v1.0.0

**Allow session**: Yes (exit 0)

---

### Missing Release Note

**Scenario**: Gap version (e.g., 1.2.0) detected but `skills/.wrangler-releases/1.2.0.md` missing

**Output**:
```
⚠️ Missing release note: skills/.wrangler-releases/1.2.0.md
   Version gap contains undocumented release

   Cannot determine if v1.2.0 has breaking changes.
   Assuming breaking changes exist for safety.

   Plugin may be corrupted. Consider reinstalling.
```

**Signal**: OUTDATED (assume breaking changes for safety)

**Allow session**: Yes (exit 0)

## Environment Variables

### WRANGLER_SKIP_VERSION_CHECK

**Type**: Boolean (true/false)

**Purpose**: Completely skip version detection

**Usage**:
```bash
export WRANGLER_SKIP_VERSION_CHECK=true
```

**Effect**:
- Startup skill exits immediately without any checks
- No output (silent skip)
- Useful for emergency situations or CI/CD

---

### WRANGLER_DEBUG_VERSION

**Type**: Boolean (true/false)

**Purpose**: Enable verbose version detection output

**Usage**:
```bash
export WRANGLER_DEBUG_VERSION=true
```

**Debug output includes**:
- Constitution file location used
- Raw version strings extracted
- Version comparison results
- List of release notes checked
- Frontmatter parsing details

**Example**:
```
[DEBUG] Constitution found: .wrangler/governance/CONSTITUTION.md
[DEBUG] Extracted version: "1.1.0"
[DEBUG] Current version: "1.2.0"
[DEBUG] Comparison: 1.1.0 < 1.2.0
[DEBUG] Checking release note: skills/.wrangler-releases/1.2.0.md
[DEBUG] Breaking changes: false
[DEBUG] Status: WARN (non-breaking updates)
```

## Integration with Session Start

This skill is invoked automatically in `hooks/session-start.sh`:

```bash
#!/bin/bash
# Session start hook for wrangler projects

# ... workspace initialization ...

# Run version check (unless skipped)
if [ "$WRANGLER_SKIP_VERSION_CHECK" != "true" ]; then
  # Invoke startup-checklist skill
  # (Implementation note: skills are invoked via Claude Code's Skill tool)
  # This would be done by Claude Code automatically based on skill metadata

  # For now, this is a placeholder showing the integration point
  echo "Running startup checklist..."
fi
```

**Note**: The actual invocation mechanism depends on how Claude Code plugins can trigger skills from bash hooks. This may require:
- A CLI command to invoke skills (e.g., `wrangler-cli run-skill startup-checklist`)
- Or Claude Code automatically running skills marked with `autoRun: true` metadata
- Or session hook outputting a marker that Claude Code picks up

## Testing

### Test Cases

**1. Project at v1.1.0, current v1.1.0 → SUCCESS**

Setup:
- Constitution: `wranglerVersion: "1.1.0"`
- CURRENT_VERSION: `1.1.0`

Expected output:
```
✅ Wrangler version up to date (v1.1.0)
   All systems ready.
```

Status: SUCCESS

---

**2. Project at v1.0.0, current v1.1.0 (breaking) → OUTDATED**

Setup:
- Constitution: `wranglerVersion: "1.0.0"`
- CURRENT_VERSION: `1.1.0`
- 1.1.0.md: `breakingChanges: true`

Expected output:
```
❌ Wrangler version outdated - breaking changes detected
   Project: v1.0.0
   Latest:  v1.1.0
   ...
```

Status: OUTDATED

---

**3. Project at v1.1.0, current v1.2.0 (non-breaking) → WARN**

Setup:
- Constitution: `wranglerVersion: "1.1.0"`
- CURRENT_VERSION: `1.2.0`
- 1.2.0.md: `breakingChanges: false`

Expected output:
```
⚠️ New wrangler version available
   Project: v1.1.0
   Latest:  v1.2.0
   ...
```

Status: WARN

---

**4. Project at v1.0.0, current v1.3.0 (multiple releases) → OUTDATED**

Setup:
- Constitution: `wranglerVersion: "1.0.0"`
- CURRENT_VERSION: `1.3.0`
- 1.1.0.md: `breakingChanges: true`
- 1.2.0.md: `breakingChanges: false`
- 1.3.0.md: `breakingChanges: true`

Expected output:
```
❌ Wrangler version outdated - breaking changes detected
   Project: v1.0.0
   Latest:  v1.3.0
   Releases behind: 3

   Breaking changes in:
   - v1.1.0: [description]
   - v1.3.0: [description]
   ...
```

Status: OUTDATED

---

**5. Constitution missing → WARN**

Setup:
- No constitution at either location

Expected output:
```
⚠️ No constitution found. Initialize governance first.
   ...
```

Status: WARN

---

**6. wranglerVersion field missing → Assume v1.0.0**

Setup:
- Constitution exists but no frontmatter or missing `wranglerVersion` field
- CURRENT_VERSION: `1.1.0`

Expected behavior:
- Assume project is v1.0.0
- Proceed with version comparison as if `wranglerVersion: "1.0.0"`

Status: OUTDATED (if breaking changes in 1.1.0)

---

**7. CURRENT_VERSION file missing → WARN**

Setup:
- Constitution exists
- `skills/.wrangler-releases/CURRENT_VERSION` missing

Expected output:
```
⚠️ Cannot detect wrangler version. Plugin may be corrupted.
   ...
```

Status: WARN

## Example Execution Flow

### Scenario: User starts Claude Code session with v1.0.0 project

```
1. User opens Claude Code in project directory
   ↓
2. Session hook runs (hooks/session-start.sh)
   ↓
3. Workspace initialization completes
   ↓
4. Startup skill invoked (automatically)
   ↓
5. Read project version:
   - Check .wrangler/governance/CONSTITUTION.md → Not found
   - Check specifications/_CONSTITUTION.md → Found
   - Extract frontmatter → No wranglerVersion field
   - Assume: v1.0.0
   ↓
6. Read current version:
   - Read skills/.wrangler-releases/CURRENT_VERSION
   - Parse: "1.1.0"
   ↓
7. Compare versions:
   - 1.0.0 < 1.1.0
   - Project is behind
   ↓
8. Check for breaking changes:
   - Gap versions: [1.1.0]
   - Read skills/.wrangler-releases/1.1.0.md
   - breakingChanges: true
   ↓
9. Report status:
   - Status: OUTDATED
   - Output: ❌ message with migration instructions
   ↓
10. User sees output and runs /update-yourself
    ↓
11. Migration instructions displayed
```

## Implementation Notes

### Version Comparison Algorithm

Use semantic versioning comparison:
- Compare major versions first
- If equal, compare minor versions
- If equal, compare patch versions

**Edge cases**:
- Leading zeros: "1.01.0" → Invalid, warn user
- Extra components: "1.1.0.beta" → Invalid, warn user
- Leading 'v': "v1.1.0" → Invalid, strip and warn user

### Performance Considerations

**Target**: Complete version check in <1 second

**Optimizations**:
- Read only frontmatter (not entire release notes)
- Cache CURRENT_VERSION in session
- Skip gap analysis if versions match (early exit)
- Only parse release notes if project is behind

### Security Considerations

**Path Traversal**: Ensure release note paths are sanitized
- Valid: `skills/.wrangler-releases/1.1.0.md`
- Invalid: `skills/.wrangler-releases/../../etc/passwd`

**Validation**: Check file paths before reading

### Compatibility

**Backwards Compatibility**:
- v1.0.0 projects without frontmatter: Assume v1.0.0
- Legacy constitution location: Check `specifications/_CONSTITUTION.md`
- Missing version field: Graceful degradation

**Forward Compatibility**:
- Handle project versions newer than plugin
- Warn but don't block session start

## Rollback

If startup skill causes issues:

1. **Disable temporarily**:
   ```bash
   export WRANGLER_SKIP_VERSION_CHECK=true
   ```

2. **Report issue**: Include debug output (`WRANGLER_DEBUG_VERSION=true`)

3. **Workaround**: Manually update constitution frontmatter to match CURRENT_VERSION

## Future Enhancements

**Planned**:
- [ ] Cache version check results for 24 hours
- [ ] Support for pre-release versions (1.1.0-beta.1)
- [ ] Automatic migration (not just instructions)
- [ ] Integration with plugin update mechanism
- [ ] Telemetry (track version distribution across projects)

**Not Planned**:
- Downgrade support (only upgrade paths)
- Automatic rollback (too risky)
- Network-based version checks (offline-first approach)
