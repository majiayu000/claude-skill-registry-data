---
name: product-antigravity-skill-activate
description: Use this skill to instruct the agent on how to correctly configure, register,
  and activate custom skills in Antigravity by placing files in the appropriate customization
  roots and updating skills.json registers.
category: meta
risk: safe
source: local
tags: '[configuration, skills, activation, registry]'
date_added: '2026-07-07'
user-invocable: true
---
# Skill: Antigravity Skill Activation (product-antigravity-skill-activate)

This skill should be used when the user wants to configure, register, or activate a newly created or modified skill within the Antigravity developer environment, ensuring it is recognized by the chat interface and the agent's runtime.

## 1. Core Workflow

To ensure a skill is fully activated and discovered by Antigravity, follow these steps:

### Step 1: File Location Audit
Ensure the skill files are placed in the appropriate customization roots:
- **Global Scope:** `~/.gemini/config/skills/<skill-name>/`
- **Workspace Scope:** `.agents/skills/<skill-name>/` (relative to the workspace root)
Every skill directory MUST contain:
- `SKILL.md` (the core system instructions for the skill)
- `README.md` (user-facing usage documentation)

### Step 2: Explicit Registration (`skills.json`)
If the skill is not being automatically discovered or is placed in a custom location, register it explicitly:
1. Locate or create `.agents/skills.json` in the workspace customization root.
2. Add a entry pointing to the relative path of the skill inside the customization root:
   ```json
   {
     "entries": [
       { "path": "skills/product-antigravity-skill-activate" }
     ]
   }
   ```
3. Maintain alphabetical order or append to the end of the `entries` array.

### Step 3: Verification
1. Validate the YAML frontmatter of the skill file.
2. Confirm all required folders (`references/`, `examples/`, `scripts/`) exist or have placeholder `.gitkeep` files.
3. Advise the user to reload their chat session/IDE window to reload the configuration.
