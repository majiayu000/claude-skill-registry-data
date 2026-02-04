---
name: ext-outline-plugin
description: Outline extension skill for plugin development domain - discovery, analysis, deliverable creation
implements: pm-workflow:workflow-extension-api/standards/extensions/outline-extension.md
user-invocable: false
allowed-tools: Read, Bash, AskUserQuestion, Task
---

# Plugin Outline Extension

Domain-specific outline workflow for marketplace plugin development. Handles discovery, analysis, uncertainty resolution, and deliverable creation for Complex Track requests.

**Loaded by**: `pm-workflow:phase-3-outline` (Complex Track)

---

## Input

```toon
plan_id: {plan_id}
```

All other data read from sinks (references.toon, request.md).

---

## Workflow Overview

```
Step 1: Load Context      → Read request, module_mapping, domains, compatibility
Step 2: Discovery         → Spawn ext-outline-inventory-agent
Step 3: Determine Type    → Extract change_type from request
Step 4: Execute Workflow  → Route based on change_type (Create/Modify Flow)
Step 5: Write Solution    → Persist solution_outline.md
```

**Detailed workflow**: Load `standards/workflow.md` for Create Flow and Modify Flow logic.

---

## Step 1: Load Context

Read request (uses clarified_request if available):

```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents request read \
  --plan-id {plan_id} \
  --section clarified_request
```

Read module_mapping from work directory (for bundle filtering hints):

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files read \
  --plan-id {plan_id} \
  --file work/module_mapping.toon
```

Read domains:

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get \
  --plan-id {plan_id} --field domains
```

Read compatibility from marshal.json project configuration:

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-2-refine get --field compatibility --trace-plan-id {plan_id}
```

Derive the long description from the compatibility value:
- `breaking` → "Clean-slate approach, no deprecation nor transitionary comments"
- `deprecation` → "Add deprecation markers to old code, provide migration path"
- `smart_and_ask` → "Assess impact and ask user when backward compatibility is uncertain"

Store as `compatibility` and `compatibility_description` for inclusion in the solution outline header metadata.

Log context:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Context loaded: domains={domains}, compatibility={compatibility}"
```

---

## Step 1.5: Determine Component Scope

Analyze the request to determine which component types are affected.

### Component Types (all must be considered)

| Type | Sub-documents | Include if... |
|------|---------------|---------------|
| skills | standards/, templates/, scripts/, references/ | Request mentions skill, standard, workflow, template |
| agents | (none) | Request mentions agent, task executor |
| commands | (none) | Request mentions command, slash command, user-invokable |
| scripts | (none) | Request mentions script, Python, automation |
| plugin.json | (none) | Components added/removed/renamed |
| tests | conftest.py, test_*.py | Request mentions test, testing, coverage, pytest |
| project-skills | .claude/skills/* | Request mentions verify-workflow, project skill, sync-plugin-cache |

### Decision Logic

FOR EACH component_type IN [skills, agents, commands, scripts, plugin.json, tests, project-skills]:
  ANALYZE request for explicit OR implicit mentions
  LOG decision with evidence

### Log Decisions

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Component scope: [{component_types_list}]"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Skills: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Agents: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Commands: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Scripts: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) plugin.json: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Tests: {AFFECTED|NOT_AFFECTED} - {evidence}"

python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Project-skills: {AFFECTED|NOT_AFFECTED} - {evidence}"
```

### Skill Sub-Documents

IF skills are in scope:
  ALSO include skill sub-documents:
  - standards/*.md
  - templates/*
  - references/*
  - knowledge/*

This uses --full mode in inventory scan to enumerate sub-documents.

---

## Step 1.6: Derive Content Filter Criteria (if applicable)

For certain change_types, derive a content filter pattern to reduce LLM analysis load.

### When to Apply

| change_type | Apply Content Filter? |
|-------------|----------------------|
| create | NO - files don't exist yet |
| modify | MAYBE - if request mentions specific content |
| migrate | YES - migration targets specific patterns |
| refactor | MAYBE - if request mentions specific patterns |

### Pattern Derivation Examples

| Request Keywords | Derived Pattern | Rationale |
|-----------------|-----------------|-----------|
| "JSON to TOON", "migrate JSON" | `` ```json `` | Files with JSON code blocks |
| "TOON output", "add TOON" | `` ```toon `` | Files with TOON code blocks |
| "update imports", "refactor imports" | `^import\|^from` | Files with import statements |
| "change output format" | `## Output` | Files with Output sections |

### Log Decision

IF content filter is derived:
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO '(pm-plugin-development:ext-outline-plugin) Content filter: pattern={pattern}, derived from {request_keywords}'
```

IF no content filter applicable:
```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Content filter: NONE (change_type={change_type} does not benefit from content filtering)"
```

---

## Step 2: Discovery

Spawn ext-outline-inventory-agent with component scope and content filter from Steps 1.5/1.6:

```
Task: pm-plugin-development:ext-outline-inventory-agent
  Input:
    plan_id: {plan_id}
    component_types: [{component_types from Step 1.5}]
    content_pattern: "{pattern from Step 1.6 or empty}"
    bundle_scope: {from module_mapping or "all"}
  Output:
    inventory_file: work/inventory_filtered.toon
    scope: affected_artifacts, bundle_scope
    counts: skills, commands, agents, total
```

The agent:
- Runs `scan-marketplace-inventory` with `--resource-types` from component_types
- Uses `--content-pattern` if provided (enables pre-filtering)
- Uses `--bundles` filter if module_mapping specifies specific bundles
- Persists inventory to `work/inventory_filtered.toon`
- Stores reference as `inventory_filtered` in references.toon

**Contract**: After agent returns, `work/inventory_filtered.toon` exists.

### Filter Result Logging

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  work {plan_id} INFO '[PROGRESS] (pm-plugin-development:ext-outline-plugin) Inventory: {total} files, content filter: {input} → {matched} ({excluded} excluded)'
```

### Error Handling

**CRITICAL**: If agent fails due to API errors, **HALT immediately**.

```
IF agent returns API error (529, timeout, connection error):
  HALT with error:
    status: error
    error_type: api_unavailable
    message: "Discovery agent failed. Retry later."

  DO NOT:
    - Fall back to grep/search
    - Continue with partial data
```

---

## Step 3: Determine Change Type

Extract `change_type` from request:

| Request Pattern | change_type |
|-----------------|-------------|
| "add", "create", "new" | create |
| "fix", "update" (localized) | modify |
| "rename", "migrate" | migrate |
| "refactor", "restructure" | refactor |

Log decision:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Change type: {change_type}"
```

### Validation

```
IF affected_artifacts is empty:
  ERROR: "No artifacts affected - clarify request"
```

---

## Step 4: Execute Workflow

Load detailed workflow:

```
Read standards/workflow.md
```

The workflow routes based on `change_type`:

| change_type | Flow | Description |
|-------------|------|-------------|
| create | Create Flow | Build deliverables directly (files don't exist) |
| modify, migrate, refactor | Modify Flow | Analysis → Uncertainty → Grouping → Deliverables |

### Create Flow Summary

- No analysis needed (files don't exist yet)
- Build deliverables directly from request
- One deliverable per component to create

### Modify Flow Summary

- Load persisted inventory
- Spawn analysis agents per bundle/type
- Persist assessments to `artifacts/assessments.jsonl`
- Resolve uncertainties via AskUserQuestion
- Group into deliverables
- Write solution_outline.md

### Test Deliverables (CRITICAL)

**MANDATORY**: Test deliverables MUST list explicit file paths, not descriptive text.

When tests are in component scope:

1. **Discover test files** from inventory `tests` section
2. **For each affected script**, find corresponding test files:
   ```bash
   # Pattern: test/{bundle}/{skill}/test_*.py
   # Example: test/pm-workflow/manage-tasks/test_manage_tasks.py
   ```
3. **List explicit paths** in the deliverable's `Affected files:` section

**INVALID** (descriptive text):
```markdown
**Affected files:**
- Tests that assert on JSON output format
- Tests that use json.loads() to parse output
```

**VALID** (explicit paths):
```markdown
**Affected files:**
- `test/pm-workflow/manage-tasks/test_manage_tasks.py`
- `test/pm-plugin-development/plugin-doctor/test_doctor_marketplace.py`
```

**Note**: Task contract validation rejects non-file-path steps. Descriptive text will cause task creation to fail.

---

## Step 5: Write Solution Outline

After deliverables are built, write solution_outline.md. The header MUST include `compatibility: {compatibility} -- {compatibility_description}` (read from references.toon in Step 1).

**CRITICAL - Plugin-Doctor Verification**: Every deliverable's Verification section MUST include `/plugin-doctor` for each affected component path:
- For skills: `/pm-plugin-development:plugin-doctor --component {skill_path}`
- For agents: `/pm-plugin-development:plugin-doctor --component {agent_path}`
- For commands: `/pm-plugin-development:plugin-doctor --component {command_path}`

Additional domain-specific checks (like grep for format validation) may be included but do NOT replace plugin-doctor.

```bash
python3 .plan/execute-script.py pm-workflow:manage-solution-outline:manage-solution-outline write \
  --plan-id {plan_id} <<'EOF'
# Solution: {title}

plan_id: {plan_id}
compatibility: {compatibility} — {compatibility_description}

## Summary

{2-3 sentence summary}

## Deliverables

{deliverables content}
EOF
```

Log completion:

```bash
python3 .plan/execute-script.py plan-marshall:manage-logging:manage-log \
  decision {plan_id} INFO "(pm-plugin-development:ext-outline-plugin) Complete: {N} deliverables"
```

---

## Output

Return minimal status - all data in sinks:

```toon
status: success
plan_id: {plan_id}
deliverable_count: {N}
```

---

## Sinks Written

| Sink | Content | API |
|------|---------|-----|
| `work/inventory_filtered.toon` | Filtered marketplace inventory | via ext-outline-inventory-agent |
| `artifacts/assessments.jsonl` | Component assessments (Modify Flow) | `artifact_store assessment add` |
| `logs/decision.log` | All decisions | `manage-log decision` |
| `solution_outline.md` | Final deliverables | `manage-solution-outline write` |

---

## Impact Analysis (Optional)

**Condition**: Run if inventory has < 20 files AND change_type is "modify", "migrate", or "refactor".

**Purpose**: Discover components that depend on affected components.

```bash
python3 .plan/execute-script.py pm-plugin-development:ext-outline-plugin:filter-inventory \
  impact-analysis --plan-id {plan_id}
```

For detailed rules, see `standards/impact-analysis.md`.

---

## Uncertainty Resolution

**Trigger**: Run if `uncertain > 0` after analysis.

**Purpose**: Convert UNCERTAIN findings to CERTAIN through user clarification.

### Grouping Patterns

| Pattern | Question Type |
|---------|---------------|
| JSON in workflow context vs output spec | "Should workflow-context JSON be included?" |
| Script output documentation vs skill output | "Should documented script outputs count?" |
| Example format vs actual output format | "Should example formats be treated as outputs?" |

### Resolution Application

1. Query UNCERTAIN assessments:
```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  assessment query {plan_id} --certainty UNCERTAIN
```

2. Use AskUserQuestion with specific file examples
3. Log resolutions as new assessments:
```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-artifacts:manage-artifacts \
  assessment add {plan_id} {file_path} {new_certainty} 85 \
  --agent pm-plugin-development:ext-outline-plugin \
  --detail "User clarified: {user_choice}" --evidence "From: {original_hash_id}"
```

4. Store clarifications in request.md:
```bash
python3 .plan/execute-script.py pm-workflow:manage-plan-documents:manage-plan-documents \
  request clarify \
  --plan-id {plan_id} \
  --clarifications "{formatted Q&A}" \
  --clarified-request "{synthesized request}"
```

---

## Error Handling

**CRITICAL**: If any operation fails, HALT immediately.

| Failure | Action |
|---------|--------|
| Discovery fails | `status: error, error_type: discovery_failed` |
| Analysis agent fails | `status: error, error_type: api_unavailable` |
| Write fails | `status: error, error_type: write_failed` |

**DO NOT**: Fall back to grep/search, skip failed bundles, continue with partial data.

---

## Conditional Standards

| Condition | Standard |
|-----------|----------|
| Deliverable involves Python scripts | `standards/script-verification.md` |
| Impact analysis enabled | `standards/impact-analysis.md` |
| Component analysis details | `standards/component-analysis-contract.md` |

---

## Related

- [workflow.md](standards/workflow.md) - Create Flow and Modify Flow details
- [outline-extension.md](../../../pm-workflow/skills/workflow-extension-api/standards/extensions/outline-extension.md) - Contract this skill implements
- [component-analysis-contract.md](standards/component-analysis-contract.md) - Analysis agent contract
