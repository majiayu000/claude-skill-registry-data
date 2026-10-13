---
name: generate-pr-description
description: "Generate structured Pull Request descriptions from git diffs (staged or branch) and commit history. Auto-detects .github/pull_request_template.md; falls back to Description/Impact/Task sections. Use when user says 'generate PR description', 'write PR description', 'create pull request description', 'draft the PR description', or 'summarize this branch for a PR'. Always asks user for output language if not specified."
argument-hint: "[language]: (Optional) Language for PR description (e.g., 'English', 'Portuguese'). Not provided → skill MUST ask user."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

MANDATORY: Use developer-specialist or reviewer-specialist agent.
MANDATORY: {language} arg not provided → MUST ask user: "Which language should I use for the PR description (e.g., English, Portuguese)?"

Objective: generate professional, comprehensive PR description by analyzing staged changes + recent commit history.

====================
PHASE 1 — TEMPLATE DETECTION
====================

1. Check if `.github/pull_request_template.md` exists in workspace.
2. Exists → read content, use as MANDATORY structure for PR description.
3. Not exist → use default topics as sections:
   - ## Description: High-level overview of what PR does.
   - ## Impact: Technical + functional impact of changes.
   - ## Task: List of specific tasks or user stories addressed.

====================
PHASE 2 — CONTEXT GATHERING
====================

1. Identify changes to describe:
   - Run `git diff --staged`. Not empty → use as primary source.
   - `git diff --staged` empty → run `git diff main...HEAD` (or default branch) for current branch changes.
   - Still empty → inform user, ask for source of changes.
2. Run `git log -n 10 --oneline` to understand commit sequence + intent.
3. Search `.taskmaster/` or `docs/` for relevant PRDs/task specs matching branch name or commit keywords.

====================
PHASE 3 — GENERATION
====================

Based on analysis, generate PR description:

1. Follow detected or default template strictly.
2. Tone professional, content accurate.
3. Language specified → generate entire description in that language.
4. No language specified → must have asked user in advance (see MANDATORY rule).

====================
PHASE 4 — VALIDATION
====================

Run `python3 skills/generate-pr-description/scripts/validate_pr_description.py --message "<generated description>"` before presenting it.
FAIL (exit 1) → fix flagged sections (missing/empty/placeholder text) and re-run until it passes.

====================
PHASE 5 — OUTPUT
====================

Present generated PR description to user in Markdown block.

Example Output (Default Template):

```markdown
## Description

This PR introduces a new skill for generating PR descriptions automatically...

## Impact

- Improves developer productivity by automating repetitive documentation tasks.
- Ensures consistent PR descriptions across the project.

## Task

- Create skills/generate-pr-description/SKILL.md
- Implement template detection logic.
- Add language selection support.
```

====================
WORKFLOW
====================

- Always verify PR template exists before proposing structure.
- `git diff --staged` empty → inform user no staged changes to analyze.
- Use commit history to add context not obvious from diff alone.
