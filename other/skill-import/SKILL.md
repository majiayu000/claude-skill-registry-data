---
name: skill-import
description: >
  Import skills from the skills library at ~/.claude/skills/ into a project's
  CLAUDE.md files, automatically matching skills to the correct nested folders
  (backend/, frontend/, database/, infra/, root). Invoke with /skill-import. When
  to trigger: when the user says "import skills" or "apply skills to this project";
  when onboarding a new project and all relevant library skills should be wired in;
  when adding a new domain folder and existing skills should be applied there; and
  when a project adopts a new stack (e.g., adds a frontend) and matching skills
  should be provisioned. Key capabilities: auto-match of skills to project folders
  based on stack detection (package.json, requirements.txt, etc.), manual named
  import when the user specifies a skill by name, three-tier conflict detection
  (duplicate/skip, contradiction/flag, additive/write), lesson file propagation
  from ~/.claude/memory/lessons/ into the project's memory/ dir, obsidian-vault
  logging for long-term auditability, and external URL import via Skill Seekers
  install-agent. Always appends rather than overwriting existing CLAUDE.md content.
  Ideal for project setup, team onboarding, and keeping multiple projects aligned
  with evolving skill library standards. Also useful for gap analysis (which
  skills exist in the library but aren't applied here yet).
---

# Skill Import — Import Library Skills into Project CLAUDE.md Files

Scans the skills library at `~/.claude/skills/`, matches relevant skills to the
current project's nested CLAUDE.md files, and writes ready-to-use skill content.
External URLs are handled by Skill Seekers' `install-agent` command.

---

## Step 0: Check for External URL

If the user says "import from [URL]" or "pull from [GitHub repo]":
1. Ensure skill-seekers is installed: `which skill-seekers || pip3 show skill-seekers`
2. Run: `skill-seekers install-agent "[URL]" --target claude`
3. The skill installs to `~/.claude/skills/[derived-name]/`
4. Proceed to Step 3 with that skill as the import target

If no URL, proceed to Step 1.

---

## Step 1: Read the Indexes

Always read both:
1. **`~/.claude/skills/INDEX.md`** — master list (name + description)
2. **`~/.claude/skills/skill-import/INDEX.md`** — import-specific (target + stack + description)

Rebuild either if missing or stale:
```bash
bun ~/.claude/skills/scripts/validate-index.mjs
```

---

## Step 2: Scan the Current Project

1. **Folder structure** — which domain folders exist (backend/, frontend/, database/, etc.)
2. **Existing CLAUDE.md content** — avoid duplicate rules
3. **Stack clues** — `package.json`, `requirements.txt`, `pyproject.toml`, file extensions

---

## Step 3: Match Skills to Project

### Auto-match (user said "import all relevant" or "import all skills")
Stack-match using `dept` + `scope` from `INDEX.catalog.json` against project stack.

### Named import (user said "import [skill-name]")
Look up in `INDEX.md`, verify the skill exists at `~/.claude/skills/[name]/SKILL.md`.

### Present matches for confirmation:
```
Based on your project stack, I matched:
  backend           → /backend/CLAUDE.md
  frontend         → /frontend/CLAUDE.md
  security         → /backend/CLAUDE.md

Proceed? (yes / skip [skill] / add [skill])
```

### Placement Logic

| Skill target | Destination |
|---|---|
| `database` | `/database/CLAUDE.md` |
| `backend` | `/backend/CLAUDE.md` |
| `frontend` | `/frontend/CLAUDE.md` |
| `infra` | `/infra/CLAUDE.md` |
| `root` | Root `CLAUDE.md` |
| `all` | Split across relevant folders |

---

## Step 4: Conflict Detection

- **Duplicate:** same rule already present → skip, notify user
- **Contradiction:** conflicts with existing rule → flag, ask user
- **Additive:** no conflict → safe to import

```
⚠️ Conflict in /backend/CLAUDE.md:
  Existing:  "Use pandas for data processing"
  Importing: "Never use pandas — use openpyxl only"
Which wins? (existing / importing / keep both)
```

---

## Step 5: Write to CLAUDE.md Files

Append under a labelled section per skill:
```markdown
## [skill-name] (imported from library)

[content from skill's SKILL.md body]
```

Confirm each write:
```
✓ backend  → /backend/CLAUDE.md  (backend, security)
✓ frontend → /frontend/CLAUDE.md  (frontend, vercel-deploy)
```

---

## Step 6: Summary

```
Import complete.

Files updated:
- /backend/CLAUDE.md   ← backend, security, superpowers-tdd
- /frontend/CLAUDE.md ← frontend, vercel-deploy

Skipped (duplicate): [skill]
Conflicts resolved: [rule] → [user choice]
```

---

## Step 7: Import Lesson Files

After writing CLAUDE.md files, propagate lesson files:
1. Read `~/.claude/memory/lessons/` — check available stacks
2. For each stack present in the project with a lesson file at `~/.claude/memory/lessons/{stack}.md`:
   a. Create `{project}/memory/lessons/` if missing
   b. Copy `~/.claude/memory/lessons/{stack}.md` → `{project}/memory/lessons/{stack}.md`
3. Create `{project}/memory/decisions.md` if missing
4. Create `{project}/memory/sessions/` directory if missing

---

## Step 8: Update Catalog After External Import

If Step 0 imported from an external URL, register the new skill:
```bash
bun ~/.claude/skills/scripts/update-catalog-from-skillseekers.ts ~/.claude/skills/[new-skill]
```

---

## Step 9: Obsidian Vault Logging

After each import session, log to obsidian-vault:
```
## Skills Imported: [date]
- **Skills imported:** [list]
- **Target project:** [project path]
- **Conflicts resolved:** [list or "none"]
- **Lesson files propagated:** [list or "none"]
```

---

## Key Rules

- Always read INDEX.md first — never scan raw folders if INDEX.md exists and current
- Never overwrite existing CLAUDE.md content — always append under a labelled section
- Always split multi-domain skills into the correct folders
- Always run conflict detection before writing
- External URLs use Skill Seekers `install-agent` — do not manually fetch and parse
- Log imports to obsidian-vault — import sessions are long-term memory events
