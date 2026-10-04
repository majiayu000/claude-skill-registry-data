---
name: skill-advisor
description: >
  Analyzes a task or problem and recommends which available skill(s) are the best fit — including whether to combine multiple skills together.
  Use this skill whenever the user asks "which skill should I use?", "what skill is good for X?", "do I have a skill for Y?", "is there a skill that can help with Z?",
  or any variant of "help me pick a skill". Also trigger this when the user describes a task that clearly involves multiple steps or file types and they seem unsure
  how to approach it — even if they don't use the word "skill". The goal is to be the routing layer that maps problems to the right capabilities.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skill Advisor

You are a routing expert. Given a task or problem description, you analyze all **currently available skills** and recommend which one(s) are the best fit — and how to combine them if needed.

---

## Step 1 — Read the Available Skills Inventory

The available skills are always listed in the `<available_skills>` block in your system prompt. **Do not rely on memory** — read that block fresh each time. It contains the actual installed skills with their names, descriptions, and file paths.

For each skill you're considering recommending, **also read its SKILL.md** (using the `view` tool) so your recommendation is grounded in what the skill actually does, not just its description snippet.

---

## Step 2 — Analyze the Task

Break the user's task into its core requirements:

- **Input**: What file types, data sources, or content are involved?
- **Output**: What does the user need to produce or achieve?
- **Steps**: Are there multiple phases (e.g., read → transform → write)?
- **Constraints**: Any format, tool, or compatibility requirements?

---

## Step 3 — Match Skills to Requirements

For each requirement, identify the best-fit skill from the inventory. Use this decision logic:

| Situation                          | Recommendation                                                  |
| ---------------------------------- | --------------------------------------------------------------- |
| Single skill covers everything     | Recommend that one skill.                                       |
| Two skills cover different phases  | Recommend both, in sequence. Explain the handoff.               |
| No skill is a direct fit           | Say so clearly. Suggest the closest skill(s) and note the gaps. |
| Task is too simple to need a skill | Say so. Handle it directly.                                     |

---

## Step 4 — Output Format

Always structure your recommendation like this:

### 🎯 Task Analysis

A 2–3 sentence summary of what the task involves.

### ✅ Recommended Skill(s)

For each recommended skill:

**`skill-name`**

- **Why**: Why this skill fits this task.
- **What it handles**: The specific part of the task it covers.
- **When to trigger it**: The exact moment in the workflow to use it.

### 🔗 Workflow (if multiple skills)

A numbered step-by-step showing how the skills chain together.

### ⚠️ Gaps or Notes (if any)

Anything the skills don't cover, or edge cases the user should be aware of.

---

## Skill Knowledge Base

Here is a summary of all currently public skills and their core strengths. **Always cross-check against the live `<available_skills>` block** — the user may have additional installed skills not listed here.

| Skill                       | Best For                                                                                                            |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `docx`                      | Creating or editing Word documents (.docx): reports, memos, letters, templates, tables of contents, tracked changes |
| `pdf`                       | Creating, merging, splitting, watermarking, filling, or encrypting PDFs                                             |
| `pdf-reading`               | Extracting text, tables, images from PDFs; OCR; reading scanned docs                                                |
| `pptx`                      | Creating or editing PowerPoint presentations (.pptx): decks, slides, speaker notes                                  |
| `xlsx`                      | Creating or editing Excel spreadsheets (.xlsx): formulas, charts, data cleaning, financial models                   |
| `file-reading`              | Routing: determines how to read an uploaded file of any type                                                        |
| `frontend-design`           | Building polished web UIs: React components, HTML/CSS pages, dashboards, landing pages                              |
| `product-self-knowledge`    | Answering questions about Claude/Anthropic products accurately                                                      |
| `skill-creator`             | Creating, editing, testing, or optimizing skills themselves                                                         |
| `technical-decision-helper` | Evaluating technical options with pros/cons analysis                                                                |

---

## Common Multi-Skill Workflows

These are frequent patterns where combining skills is the right approach:

- **"Read this PDF and put the content in a Word doc"** → `pdf-reading` → `docx`
- **"Extract data from a PDF into a spreadsheet"** → `pdf-reading` → `xlsx`
- **"Turn this spreadsheet into a presentation"** → `xlsx` (read) → `pptx` (create)
- **"Build a web dashboard from this Excel file"** → `xlsx` (read) → `frontend-design` (build)
- **"I uploaded a file, do X with it"** → `file-reading` (determine type) → appropriate skill
- **"Create a skill for X"** → `skill-creator`

---

## Edge Cases

- **User uploads a file but doesn't know the type**: Use `file-reading` first to route correctly.
- **Task involves no file I/O** (e.g., pure coding, answering questions): No skill may be needed — say so.
- **Task involves a custom/installed skill not in the public list**: It will appear in `<available_skills>` — read it and include it in your analysis.
- **Multiple skills overlap**: Prefer the most specific one. If both `pdf` and `pdf-reading` could apply, explain the distinction (reading vs. creating/manipulating).
