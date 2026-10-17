---
name: notebooklm
description: Interact with Google NotebookLM to create notebooks, add YouTube sources, analyze content, and generate artifacts (infographics, slide-decks, flashcards, reports, etc.). Use when the user wants to send content to NotebookLM or generate deliverables from it.
allowed-tools: Bash Read
argument-hint: <action to perform>
---

## NotebookLM Skill

Create notebooks, add sources, analyze content, and generate deliverables via Google NotebookLM.

### Prerequisites

- Virtual environment must be set up: `bash setup.sh` (from project root)
- User must have authenticated: `notebooklm login` (run in a separate terminal)

### Always activate the venv first

```bash
cd /home/user/Sneha && source .venv/bin/activate
```

### Available Commands

#### 1. Create a Notebook

```bash
python .claude/skills/notebooklm/scripts/create_notebook.py --title "Notebook Title"
```

Returns JSON: `{"notebook_id": "...", "title": "..."}`. **Save the `notebook_id`** for all subsequent commands.

#### 2. Add YouTube Sources (batch)

```bash
python .claude/skills/notebooklm/scripts/add_sources.py \
  --notebook-id <ID> \
  --urls https://youtube.com/watch?v=abc https://youtube.com/watch?v=def ...
```

Accepts multiple URLs in one call. Adds a 1.5s delay between each to avoid rate limits. Returns summary of added/failed counts.

#### 3. Ask a Question / Analyze

```bash
python .claude/skills/notebooklm/scripts/ask_question.py \
  --notebook-id <ID> \
  --question "Summarize the key themes and insights across all sources"
```

Returns JSON with the analysis answer.

#### 4. Generate an Artifact

```bash
python .claude/skills/notebooklm/scripts/generate_artifact.py \
  --notebook-id <ID> \
  --type <ARTIFACT_TYPE> \
  --style "optional style description"
```

**Supported artifact types:**
- `infographics` - Visual infographic
- `slide-deck` - Presentation slides
- `flashcards` - Study flashcards
- `quiz` - Quiz questions
- `report` - Written report
- `mind-map` - Mind map diagram
- `audio` - Audio overview (podcast-style)
- `video` - Video summary
- `data-table` - Structured data table

**Style examples:**
- `"handwritten / chalkboard"` - Chalkboard aesthetic
- `"modern and minimalist"` - Clean design
- `"colorful and engaging"` - Vibrant visuals

### End-to-End Workflow (when chaining with yt-research)

1. Receive video list JSON from `/yt-research`
2. Extract all `url` values from the results
3. Create a notebook: `create_notebook.py --title "[Topic] Research"`
4. Add all URLs: `add_sources.py --notebook-id <ID> --urls <all URLs>`
5. Wait a moment for source processing, then analyze: `ask_question.py --notebook-id <ID> --question "..."`
6. Generate requested artifact: `generate_artifact.py --notebook-id <ID> --type infographics --style "..."`
7. Present the analysis and artifact info to the user

### Error Handling

If you see an auth error like "session expired" or "not authenticated", tell the user to run `notebooklm login` again in a separate terminal to re-authenticate.
