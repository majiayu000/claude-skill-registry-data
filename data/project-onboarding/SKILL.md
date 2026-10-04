---
name: project-onboarding
description: "Full project onboarding for Claude Cowork: generates context.md, folder-instructions.md, file map, and starter prompts in one session. Triggers RU: «создай проект», «onboarding проекта», «новый проект», «настрой проект», «создай контекст проекта», «быстрый контекст», «обнови карту файлов», «пересканируй файлы». Triggers EN: 'create project', 'project onboarding', 'new project', 'set up project', 'quick context', 'update file map', 'rescan files'."
version: 1.0.0
---

# Skill: project-onboarding

Complete project onboarding for Claude Cowork in a single session.

---

## Triggers

**Russian:** «создай проект», «onboarding проекта», «новый проект», «настрой проект», «создай контекст проекта», «быстрый контекст», «обнови карту файлов», «пересканируй файлы»
**English:** "create project", "project onboarding", "new project", "set up project", "create project context", "quick context", "update file map", "rescan files"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

---

## Modes

| Mode | Triggers | Actions |
|------|----------|---------|
| `new` | "create project", "onboarding", "new project", "set up project" | Full interview → context.md + folder-instructions.md + file map + prompts |
| `quick` | "quick context", "create project context" | Blocks 1–3 + auto-scan → context.md |
| `scan` | "update file map", "rescan files" | File Map module only → update section in context.md |

---

## Instructions

### Step 1 — Determine Mode

If trigger matches `scan` → go directly to the File Map module.
If `quick` → interview blocks 1–3, then File Map.
Otherwise → `new`, all steps in sequence.

### Step 2 — Interview (modes: new / quick)

Ask questions in blocks. Wait for a response after each block. Keep questions concise.

#### Block 1 — Basics
```
1. Project name?
2. Type: analytics / content / business / personal / other?
3. Status: Active / On hold / Completed?
4. Start date? Deadline?
```

#### Block 2 — Project Overview
```
5. Describe the project in 2–4 sentences.
6. Vision — what outcome = success?
```

#### Block 3 — Current Phase
```
7. What are we working on right now?
8. What is the concrete deliverable for this phase?
```

*→ Mode `quick` stops here. Proceed to the File Map module.*

#### Block 4 — Structure
```
9. Key elements / components / layers of the project?
```

#### Block 5 — Stakeholders
```
10. Stakeholders, partners, external dependencies?
```

#### Block 6 — Constraints
```
11. Constraints: time, resources, risks?
```

#### Block 7 — Open Questions
```
12. Known unresolved tasks or questions?
```

#### Block 8 — Additional (optional)
```
13. Additional sections needed: market context / methodology / roadmap?
```
If yes — ask 1–2 clarifying questions for each selected section.

### Step 3 — File Map Module

Determine the project folder:
- If a user folder is mounted (mounted workspace) — use its root.
- If a path was mentioned during the interview — use it.
- Otherwise — ask: "Provide the path to the project folder."

Run:
```bash
find [project-folder] -type f \
  -not -path '*/.git/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/__pycache__/*' \
  -not -name '.DS_Store' \
  | head -200
```

For each file determine: path, extension, size.
For text files (.md, .txt, .csv) — read the first line as the description.
For all others — use `[auto]` based on filename or `[clarify]`.

Group by folder. Format the section as:

```markdown
# Data Structure

## [folder-name]/
| File | Type | Size | Description |
|------|------|------|-------------|
| filename.ext | EXT | X KB | description |
```

In `scan` mode — locate the existing `context.md` and replace the "Data Structure" section. Do not modify anything else.

### Step 4 — Generate context.md (modes: new / quick)

Rules:
- Do not copy answers verbatim — write coherent structured text
- Preserve the user's terminology
- Do not infer — use only facts from the answers
- Missing information → `[clarify]`
- Use the File Map module output for the "Data Structure" section

Template: `resources/context-template-ru.md` (Russian) or `resources/context-template-en.md` (English)

Output: `context.md`

### Step 5 — Rules Module (mode: new only)

Load the template from `resources/rules-templates-ru.md` or `resources/rules-templates-en.md` based on the detected language and project type (answer 2).
Add general rules (file discovery, language, behavior).
Adapt to the user's answers.

Output: `folder-instructions.md`

After generating, ask: "Rules are ready. Would you like to edit or add your own?"

### Step 6 — Starter Prompts Module (mode: new only)

Ask: "Generate starter prompt templates for this project type?"
If yes — load templates from `resources/prompt-templates-ru.md` or `resources/prompt-templates-en.md` based on the detected language and project type.
Adapt to the project context (project name, terminology).

Output: files in `resources/prompts/`

### Step 7 — Summary

Show the table:
```
| File | Status |
|------|--------|
| context.md | Created, X blocks filled, Y [clarify] |
| folder-instructions.md | Created / Skipped |
| resources/prompts/*.md | N templates created / Skipped |
```

Provide all files for download.

---

## Constraints

- Maximum 200 files in auto-scan (if more → warn and show top-level only)
- This skill does not generate prompt-builder prompts — that is a separate skill
- Do not modify project files other than context.md (in scan mode)
