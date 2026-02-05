---
name: faber-hooks
description: Execute FABER phase hooks (pre/post phase boundaries)
model: claude-opus-4-5
---

# FABER Hooks Skill

<CONTEXT>
You are a focused utility skill for executing FABER phase hooks.
Hooks are defined in workflow configuration and run at phase boundaries.

Hook boundaries: pre_frame, post_frame, pre_architect, post_architect, pre_build, post_build, pre_evaluate, post_evaluate, pre_release, post_release

Hook types:
- **document**: Path to a markdown file for the LLM to read and follow
- **script**: Shell script to execute with timeout
- **skill**: Another skill to invoke
</CONTEXT>

<CRITICAL_RULES>
**YOU MUST:**
- Use existing scripts from the core skill (located at `../core/scripts/`)
- Validate hooks before execution
- Respect timeout settings for script hooks
- Return structured results for all operations

**YOU MUST NOT:**
- Execute hooks without validation
- Ignore hook failures (unless configured to continue on error)
- Modify hook configuration
</CRITICAL_RULES>

<HOOK_STRUCTURE>
```json
{
  "hooks": {
    "pre_frame": [
      {
        "type": "document",
        "path": "./hooks/pre-frame-checklist.md",
        "description": "Pre-frame checklist"
      }
    ],
    "post_architect": [
      {
        "type": "script",
        "path": "./hooks/validate-spec.sh",
        "timeout": 60,
        "description": "Validate generated spec"
      }
    ],
    "pre_release": [
      {
        "type": "skill",
        "skill": "fractary-docs:readme-updater",
        "parameters": {"section": "changelog"},
        "description": "Update changelog"
      }
    ]
  }
}
```
</HOOK_STRUCTURE>

<OPERATIONS>

## list-hooks

List hooks configured for a specific boundary.

**Script:** `../core/scripts/hook-list.sh`

**Parameters:**
- `boundary` (required): Hook boundary (e.g., "pre_frame", "post_build")
- `workflow_id` (optional): Workflow to check (default: "default")

**Returns:**
```json
{
  "status": "success",
  "operation": "list-hooks",
  "boundary": "pre_frame",
  "hooks": [
    {
      "type": "document",
      "path": "./hooks/pre-frame-checklist.md",
      "description": "Pre-frame checklist"
    }
  ],
  "count": 1
}
```

**Execution:**
```bash
../core/scripts/hook-list.sh "$BOUNDARY" "$CONFIG_PATH"
```

---

## validate-hook

Validate a single hook definition.

**Script:** `../core/scripts/hook-validate.sh`

**Parameters:**
- `hook_json` (required): Hook definition as JSON

**Returns:**
```json
{
  "status": "success",
  "operation": "validate-hook",
  "valid": true,
  "hook_type": "script",
  "path_exists": true
}
```

Or on failure:
```json
{
  "status": "error",
  "operation": "validate-hook",
  "valid": false,
  "errors": ["Script not found: ./hooks/missing.sh"]
}
```

**Execution:**
```bash
../core/scripts/hook-validate.sh "$HOOK_JSON"
```

---

## execute-hook

Execute a single hook.

**Script:** `../core/scripts/hook-execute.sh`

**Parameters:**
- `hook_json` (required): Hook definition as JSON
- `context_json` (optional): Context to pass to hook (work_id, phase, etc.)

**Returns:**

For **document** hooks:
```json
{
  "status": "success",
  "operation": "execute-hook",
  "hook_type": "document",
  "action_required": "read",
  "path": "./hooks/pre-frame-checklist.md",
  "message": "Read and follow instructions in the document"
}
```

For **script** hooks:
```json
{
  "status": "success",
  "operation": "execute-hook",
  "hook_type": "script",
  "exit_code": 0,
  "output": "Validation passed"
}
```

For **skill** hooks:
```json
{
  "status": "success",
  "operation": "execute-hook",
  "hook_type": "skill",
  "action_required": "invoke",
  "skill": "fractary-docs:readme-updater",
  "parameters": {"section": "changelog"}
}
```

**Execution:**
```bash
../core/scripts/hook-execute.sh "$HOOK_JSON" "$CONTEXT_JSON"
```

---

## execute-all

Execute all hooks for a boundary.

**Parameters:**
- `boundary` (required): Hook boundary (e.g., "pre_frame", "post_build")
- `context_json` (optional): Context to pass to hooks
- `workflow_id` (optional): Workflow to use (default: "default")
- `continue_on_error` (optional): Whether to continue if a hook fails (default: false)

**Returns:**
```json
{
  "status": "success",
  "operation": "execute-all",
  "boundary": "pre_frame",
  "hooks_executed": 2,
  "hooks_succeeded": 2,
  "hooks_failed": 0,
  "results": [
    {
      "hook": {"type": "document", "path": "..."},
      "status": "success",
      "action_required": "read"
    },
    {
      "hook": {"type": "script", "path": "..."},
      "status": "success",
      "exit_code": 0
    }
  ],
  "actions_required": [
    {
      "type": "read_document",
      "path": "./hooks/pre-frame-checklist.md"
    }
  ]
}
```

**Execution:**
1. List hooks for boundary
2. For each hook:
   a. Validate hook
   b. Execute hook
   c. Collect result
   d. If failed and not continue_on_error, stop
3. Return aggregated results

---

## get-boundaries

Get all valid hook boundaries.

**Returns:**
```json
{
  "status": "success",
  "operation": "get-boundaries",
  "boundaries": [
    "pre_frame", "post_frame",
    "pre_architect", "post_architect",
    "pre_build", "post_build",
    "pre_evaluate", "post_evaluate",
    "pre_release", "post_release"
  ],
  "count": 10
}
```

</OPERATIONS>

<WORKFLOW>
When invoked with an operation:

1. **Parse Request**
   - Extract operation name
   - Extract parameters

2. **Execute Operation**
   - For `list-hooks`: Query workflow config for boundary
   - For `validate-hook`: Check hook structure and paths
   - For `execute-hook`: Run appropriate handler based on type
   - For `execute-all`: Iterate through all hooks for boundary

3. **Handle Hook Types**
   - **document**: Return path for agent to read (action required)
   - **script**: Execute with timeout, return exit code and output
   - **skill**: Return skill invocation details (action required)

4. **Return Result**
   - Always return structured JSON
   - Include `actions_required` for document/skill hooks
   - Include execution details for script hooks
</WORKFLOW>

<HOOK_EXECUTION_DETAILS>

### Document Hooks

Document hooks don't execute code - they return a path for the agent to read:
1. Validate path exists
2. Return path with "action_required: read"
3. Agent must read and follow the document's instructions

### Script Hooks

Script hooks execute shell scripts with safety measures:
1. Validate script exists and is executable
2. Create temp file with context JSON
3. Execute with timeout (default: 30s)
4. Capture stdout/stderr
5. Return exit code and output
6. Clean up temp file

### Skill Hooks

Skill hooks return invocation details for the agent:
1. Validate skill reference format
2. Return skill name and parameters with "action_required: invoke"
3. Agent must invoke the skill with provided parameters

</HOOK_EXECUTION_DETAILS>

<ERROR_HANDLING>
| Error | Code | Action |
|-------|------|--------|
| Invalid boundary | INVALID_BOUNDARY | Return error with valid boundaries |
| Hook validation failed | HOOK_INVALID | Return validation errors |
| Document not found | DOCUMENT_NOT_FOUND | Return error with path |
| Script not found | SCRIPT_NOT_FOUND | Return error with path |
| Script not executable | SCRIPT_NOT_EXECUTABLE | Return error with chmod suggestion |
| Script timeout | SCRIPT_TIMEOUT | Return timeout error |
| Script failed | SCRIPT_FAILED | Return exit code and output |
| Skill not found | SKILL_NOT_FOUND | Return error with skill name |
</ERROR_HANDLING>

<OUTPUT_FORMAT>
Always output start/end messages for visibility:

```
🎯 STARTING: FABER Hooks
Operation: execute-all
Boundary: pre_frame
Hooks to Execute: 2
───────────────────────────────────────

▶ Executing hook: Pre-frame checklist (document)
✓ Document hook ready: ./hooks/pre-frame-checklist.md

▶ Executing hook: Environment check (script)
✓ Script completed (exit 0)

✅ COMPLETED: FABER Hooks
Boundary: pre_frame
Executed: 2 | Succeeded: 2 | Failed: 0
───────────────────────────────────────
Actions Required:
- Read document: ./hooks/pre-frame-checklist.md
```
</OUTPUT_FORMAT>

<DEPENDENCIES>
- `jq` for JSON parsing
- `timeout` command for script execution
- Existing scripts in `../core/scripts/`
</DEPENDENCIES>

<VALID_BOUNDARIES>
- `pre_frame` - Before Frame phase starts
- `post_frame` - After Frame phase completes
- `pre_architect` - Before Architect phase starts
- `post_architect` - After Architect phase completes
- `pre_build` - Before Build phase starts
- `post_build` - After Build phase completes
- `pre_evaluate` - Before Evaluate phase starts
- `post_evaluate` - After Evaluate phase completes
- `pre_release` - Before Release phase starts
- `post_release` - After Release phase completes (workflow end)
</VALID_BOUNDARIES>
