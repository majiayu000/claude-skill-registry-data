---
name: new-project
description: >
  Scaffold a complete project + PD in one command. Use when creating a new project,
  starting a new repo, or setting up a PD for an existing project. Spawns the
  project-scaffolder agent which creates all files and registries autonomously.
  Main session receives only a confirmation. Also triggers on: "tạo project mới",
  "scaffold project", "setup project and pd", "create pd".
---

# /new-project

Scaffold a complete project + PD setup via the `project-scaffolder` agent.
Main session stays clean — all work happens in the subagent.

## Step 0 — Pre-flight

Check for existing slugs to warn about conflicts:

```bash
python3 -c "
import json, pathlib
p = pathlib.Path.home() / 'projects/index.json'
if p.exists():
    d = json.loads(p.read_text())
    slugs = [x.get('name','') for x in d.get('projects', [])]
    print('Existing:', ', '.join(slugs))
else:
    print('Existing: none')
"
```

Store the output for conflict detection in Step 1.

## Step 1 — Collect inputs

Use AskUserQuestion with these 4 questions in a single call:

**Question 1 — "Project identity"**
- Question: "What's the project slug, display name, and one-line description? (e.g. content-agency | Content Agency | Content production and delivery service)"
- Header: "Identity"
- Options: Let user type freely (use "Other" as the only real option path — present 2 example options as templates)
  - Option A: label "Example: content-agency", description "content-agency | Content Agency | Content production and delivery service"
  - Option B: label "Example: my-saas", description "my-saas | My SaaS | B2B SaaS platform for X"

**Question 2 — "Project location"**
- Question: "Where should the project live?"
- Header: "Location"
- Options:
  - "~/projects/ (Recommended)" — Standard location for code/business projects
  - "~/.claude/projects/" — For system/infrastructure projects

**Question 3 — "Department"**
- Question: "Which department should the PD belong to?"
- Header: "Department"
- Options:
  - "specialized (Recommended)" — Default for most projects
  - "project-management" — For the operator's own products/services
  - "engineering" — For technical infrastructure projects

**Question 4 — "Tech stack"**
- Question: "Tech stack, hex color, and extra skills? (e.g. Next.js 15, Supabase | #6366f1 | backend, vercel-deploy)"
- Header: "Stack"
- Options: Let user type freely
  - Option A: label "Next.js + Supabase", description "Next.js 15, Supabase, Vercel | #6366f1 | backend, supabase-deploy"
  - Option B: label "Decide later", description "TBD | #10b981 | (none)"

## Step 2 — Parse and validate

From the answers:
1. Parse identity: split on `|` to get SLUG, NAME, DESCRIPTION (trim whitespace)
2. Parse location: expand to full path (`~/projects/{SLUG}` or `~/.claude/projects/{SLUG}`)
3. Parse department: use the selected value
4. Parse stack line: split on `|` to get STACK, COLOR, EXTRA_SKILLS (trim whitespace)
5. Build SKILLS = `save-state, recall` + any EXTRA_SKILLS
6. Set TODAY = current date (YYYY-MM-DD)
7. Normalize all `~` to the current user's home directory (`$HOME`)

Validate:
- SLUG is kebab-case (lowercase, hyphens only)
- COLOR is valid hex (#XXXXXX)
- PATH does not contain spaces

If SLUG appears in existing slugs from Step 0, warn the user via a follow-up AskUserQuestion:
"Slug `{SLUG}` already exists. Continue anyway or pick a new slug?"

## Step 3 — Spawn project-scaffolder agent

```
Agent({
  subagent_type: "project-scaffolder",
  description: "Scaffold {SLUG} project + PD",
  prompt: "Create the complete project and PD setup with these inputs:\n\nSLUG: {SLUG}\nNAME: {NAME}\nDESCRIPTION: {DESCRIPTION}\nPATH: {PATH}\nSTACK: {STACK}\nDEPARTMENT: {DEPARTMENT}\nCOLOR: {COLOR}\nSKILLS: {SKILLS}\nTODAY: {TODAY}\n\nFollow your agent definition exactly. Work through all 5 steps. Output only the confirmation block at the end."
})
```

## Step 4 — Report

Relay the agent's confirmation to the user. Add:
"Run `/recall {SLUG}` to start working with the new PD."
