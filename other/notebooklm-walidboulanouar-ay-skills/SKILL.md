---
name: notebooklm
description: Use this skill to query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini. Browser automation, library management, persistent auth. Drastically reduced hallucinations through document-only responses.
---

# NotebookLM Research Assistant Skill

Interact with Google NotebookLM to query documentation with Gemini's source-grounded answers. Each question opens a fresh browser session, retrieves the answer exclusively from your uploaded documents, and closes.

**Source:** https://github.com/PleasePrompto/notebooklm-skill

## Install

```bash
git clone https://github.com/PleasePrompto/notebooklm-skill ~/.claude/skills/notebooklm
```

The `run.py` wrapper auto-creates `.venv`, installs dependencies, and sets up Chromium on first run.

## When to Use This Skill

Trigger when user:
- Mentions NotebookLM explicitly
- Shares NotebookLM URL (`https://notebooklm.google.com/notebook/...`)
- Asks to query their notebooks/documentation
- Wants to add documentation to NotebookLM library
- Uses phrases like "ask my NotebookLM", "check my docs", "query my notebook"

## CRITICAL: Always Use run.py Wrapper

**NEVER call scripts directly. ALWAYS use `python scripts/run.py [script]`:**

```bash
# CORRECT
python scripts/run.py auth_manager.py status
python scripts/run.py notebook_manager.py list
python scripts/run.py ask_question.py --question "..."

# WRONG — fails without venv
python scripts/auth_manager.py status
```

## Core Workflow

### Step 1: Check Authentication
```bash
python scripts/run.py auth_manager.py status
```

### Step 2: Authenticate (One-Time Setup)
```bash
# Browser MUST be visible for manual Google login
python scripts/run.py auth_manager.py setup
```
Tell user: "A browser window will open for Google login."

### Step 3: Manage Notebook Library

```bash
# List all notebooks
python scripts/run.py notebook_manager.py list

# Add notebook — ALL parameters required
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/..." \
  --name "Descriptive Name" \
  --description "What this notebook contains" \
  --topics "topic1,topic2,topic3"

# Smart Add (discover content first, then add)
python scripts/run.py ask_question.py --question "What topics are covered in this notebook?" --notebook-url "[URL]"

# Search, activate, remove
python scripts/run.py notebook_manager.py search --query "keyword"
python scripts/run.py notebook_manager.py activate --id notebook-id
python scripts/run.py notebook_manager.py remove --id notebook-id
```

### Step 4: Ask Questions

```bash
# Basic query (uses active notebook)
python scripts/run.py ask_question.py --question "Your question here"

# Query specific notebook by ID
python scripts/run.py ask_question.py --question "..." --notebook-id notebook-id

# Query by URL directly
python scripts/run.py ask_question.py --question "..." --notebook-url "https://..."

# Debug mode
python scripts/run.py ask_question.py --question "..." --show-browser
```

## Follow-Up Mechanism (CRITICAL)

Every NotebookLM answer ends with: **"Is that ALL you need to know?"**

Required behavior:
1. STOP — do not immediately respond to user
2. ANALYZE — compare answer to original request
3. IDENTIFY GAPS — determine if more info needed
4. ASK FOLLOW-UP — if gaps exist, query again with context
5. SYNTHESIZE — combine all answers before responding

## Script Reference

```bash
# Auth
python scripts/run.py auth_manager.py setup|status|reauth|clear

# Notebooks
python scripts/run.py notebook_manager.py add|list|search|activate|remove|stats

# Questions
python scripts/run.py ask_question.py --question "..." [--notebook-id ID] [--notebook-url URL]

# Cleanup
python scripts/run.py cleanup_manager.py [--confirm] [--preserve-library]
```

## Data Storage

All data in `~/.claude/skills/notebooklm/data/`:
- `library.json` — notebook metadata
- `auth_info.json` — auth status
- `browser_state/` — browser cookies/session

Protected by `.gitignore`. Never commit.

## Limitations

- No session persistence (each question = new browser session)
- Rate limit: ~50 queries/day on free Google accounts
- Manual upload required (user adds docs to NotebookLM)
- Requires Python 3.8+

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ModuleNotFoundError | Use `run.py` wrapper, never call scripts directly |
| Auth fails | Browser must be visible: `--show-browser` |
| Rate limit hit | Wait or switch Google account |
| Browser crashes | `python scripts/run.py cleanup_manager.py --preserve-library` |
