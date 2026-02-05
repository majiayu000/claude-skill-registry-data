---
name: Skill Create
description: Generates a new Betty Framework Skill directory and manifest. Use when you need to bootstrap a new skill in the Betty Framework.
---

# Skill Create

## Purpose
This skill automates the creation of a new Claude Code-compatible Skill inside the Betty Framework. It scaffolds the directory structure, generates the `skill.yaml` manifest file, and registers the skill in the internal registry. Use this when you want to add a new skill quickly and consistently.

## Instructions
1. Run the script `skill_create.py` with the following arguments:
   ```bash
   python skill_create.py <skill_name> "<description>" [--inputs input1,input2] [--outputs output1,output2]
2. The script will create a folder under /skills/<skill_name>/ with:
   * skill.yaml manifest (populated with version 0.1.0 and status draft)
   * SKILL.md containing the description 
   * A registration entry added to registry/skills.json

3. The new manifest will be validated via the skill.define skill.

4. After creation, review the generated skill.yaml for correctness, edit if necessary, and then mark status: active when ready for use.

## Example

```bash
python skill_create.py workflow.compose "Compose and orchestrate multi-step workflows" --inputs workflow.yaml,context.schema --outputs execution_plan.json
```

This will generate:

```
skills/
  workflow.compose/
    skill.yaml
    README.md
registry/skills.json  ← updated with workflow.compose entry
```

## Implementation Notes

* The script uses forward-slash paths (e.g., `skills/workflow.compose/skill.yaml`) to remain cross-platform.
* The manifest file format must include fields: `name`, `version`, `description`, `inputs`, `outputs`, `dependencies`, `status`.
* This skill depends on `skill.define` (for validation) and `context.schema` (for input/output schema support).
* After running, commit the changes to Git; version control provides traceability of new skills.