---
name: writing-plans
description: Write a step-by-step Godot implementation plan — use after brainstorming produces an approved spec, before writing any code.
---

# Godot Writing Plans

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

Write an implementation plan from the approved spec. Every task must include exact file paths, key code patterns, and AgentBridge verification steps. Full code is written during execution, not here.

**The spec is already approved — do NOT re-research or re-read what was done in brainstorming.**

**Write the entire plan in a single `Write` tool call — do NOT output plan content as message text, do NOT use incremental Edits. Build the full content in your response, then write it to the file in one shot.**

## File Structure

Before writing tasks, map out which files will be created or modified and what each is responsible for. Include this map in the plan header. Each file should have one clear responsibility.

## Plan Header

Every plan starts with:

```markdown
# <Feature> Implementation Plan

> **For agentic workers:** Use `godot:subagent-driven-development` (recommended) or `godot:executing-plans` to implement this plan task-by-task.

**Goal:** <one sentence>
**Scenes:** <list of .tscn files>
**Scripts:** <list of .gd/.cpp files>
**AgentBridge:** `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh`

**File map:**
- Create `res://path/to/file.gd` — <one-line responsibility>
- Modify `res://path/to/existing.gd` — <what changes>

---
```

## Task Structure

```markdown
### Task N: <Name>

**Files:**
- Create/Modify: `res://path/to/file.gd`

- [ ] Write the file (class signature + key methods — full body written during execution)
- [ ] `bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --save-all`
- [ ] Smoke-test:
  ```bash
  bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --execute - <<'GD'
  print(EditorInterface.get_edited_scene_root().get_node_or_null("YourNode") != null)
  GD
  bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh --log 50
  ```
- [ ] Commit: `git commit -m "feat: <description>"`
```

## Rules

- Every task ends with `--save-all` + `--log` verification
- Every task ends with a git commit
- No "TBD" or "TODO" — show the key pattern, class signature, or critical snippet
- One task per script file, one task per scene modification
- Show the skeleton/interface — full implementations are written during execution

## AgentBridge Checkpoint Pattern

After every code task:
```bash
GDEXEC="bash ${CLAUDE_SKILL_DIR}/../runner/scripts/godot-exec.sh"
$GDEXEC --save-all
$GDEXEC --execute - <<'GD'
var root = EditorInterface.get_edited_scene_root()
# verify the thing you just added exists
print(root.get_node_or_null("YourNode") != null)
GD
$GDEXEC --log 50
```

## Self-Review

After writing the plan, check against the spec:

1. **Spec coverage:** Every requirement has a task. List any gaps and add tasks for them.
2. **Placeholder scan:** No "TBD", "TODO", or "similar to above".
3. **Consistency:** Method names and types match across tasks.

Fix inline — no need to re-review.

## Save Plan To

`docs/plans/YYYY-MM-DD-<feature>.md`

## After Writing

**"Plan complete and saved to `docs/plans/<filename>.md`. Ready to start implementation with `godot:subagent-driven-development`? (yes / no)"**

If yes — invoke `godot:subagent-driven-development`.
If no — stop and wait for further instructions.
