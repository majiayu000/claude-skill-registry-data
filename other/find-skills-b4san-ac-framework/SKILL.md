---
name: find-skills
description: Build and maintain a custom project skill repertoire. Always use at new project bootstrap and when users ask for new domain capabilities. Detect active assistant folders first, recommend at least 5 skills per search batch, confirm installs, normalize install paths, and regenerate workflow files.
---

# Find Skills

Use this skill to discover, install, and operationalize reusable skills for the current project.

## Mandatory triggers

Run this skill automatically when:
1. A project is starting from zero and needs its initial skill repertoire.
2. The user explicitly asks to find/add/install skills.
3. The user says they are entering a new work area (for example: security, testing, deployment, data, mobile).

## Step 0: Detect active assistant targets first (required)

Before searching skills, list workspace root folders and detect which assistant folders exist.

```bash
ls -la
```

Look for folders such as:
- `.claude`
- `.opencode`
- `.cursor`
- `.windsurf`
- `.roo`
- `.github`
- `.gemini`
- `.continue`
- `.agents`

If multiple assistants exist, ask which target(s) should receive installed skills.

## Step 1: Scope the batch

Define one search batch per domain/request (for example: "testing", "api", "devops").
For each batch, recommend at least 5 candidate skills.

Minimum output per batch:
- 5 or more skills
- short reason per skill
- install source/package
- estimated trust signal (publisher quality, adoption)

## Step 2: Search from multiple sources (no API key required)

Primary source:

```bash
npx skills find <query>
```

Additional source (keyword API, anonymous mode):

```bash
curl -sS "https://skillsmp.com/api/v1/skills/search?q=<query>&page=1&limit=20&sortBy=recent"
```

Important:
- Do not require API keys.
- Do not block on authenticated endpoints.
- AI semantic search endpoint is optional only when user explicitly provides a key and asks for it.

## Step 3: Present and confirm selections

For each batch, present at least 5 options and then confirm exactly which skill(s) to install.

Required confirmation format:
1. Selected skill names
2. Target assistant folder(s)
3. Install order

## Step 4: Install selected skills

Use the standard install command pattern. Example:

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

If installer shows an interactive agent selector, choose the confirmed target assistant(s).

## Step 5: Normalize install location (required)

If installation creates a new folder (for example `.agentss`) instead of the intended target:
1. Detect where the skill was created.
2. Copy/move the skill into the original target assistant folder (for example `.claude/skills/`).
3. Remove temporary/unwanted folder after migration.

Example normalization flow:

```bash
mkdir -p .claude/skills
cp -R .agentss/skills/<skill-name> .claude/skills/
rm -rf .agentss
```

Repeat for each selected assistant target when needed.

## Step 6: Regenerate workflow files after installation

After final skill selection and installation, regenerate project workflow docs in this order:
1. `ac.md` (required)
2. `ac-lite.md` (if present)
3. `AGENTS.md` / `CLAUDE.md` / `GEMINI.md` / `copilot-instructions.md` (if present)

Use the custom workflow template and include only the selected skills plus the general baseline.

## Required output contract

When this skill runs, return:
1. Detected assistant folders
2. Search batches executed
3. At least 5 recommendations per batch
4. User-confirmed install list
5. Final installed skills by assistant target
6. Normalization actions performed (if any)
7. Confirmation that `ac.md` and companion instruction files were regenerated

## Quality rules

- Never install without explicit confirmation of skill names.
- Never leave skills stranded in unintended folders (for example `.agentss`).
- Always keep workflow docs synchronized with the installed skill repertoire.
- Keep suggestions relevant; avoid filler suggestions just to reach 5.

