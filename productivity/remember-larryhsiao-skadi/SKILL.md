---
name: remember
description: Use when the user wants to save knowledge to their personal knowledge-base repo — from any repo, not just that repo itself. Determines category, suggests sub-categories, and writes the note into the knowledge-base repo (its location is machine-specific, read from ~/.skadi/memory-repo.md — never hardcoded).
purpose: Saves knowledge to the personal knowledge-base repo.
user_invocable: true
args: "[topic or content to remember]"
stage: desk
composes: handoff:dispatch
---

# Remember — Save Knowledge to the Knowledge Base

This skill writes into the personal **knowledge-base repo** — the same repo the
Memory Bootstrap rule in CLAUDE.md reads from — regardless of the current
working directory. Every search, write, and git action below targets that
repo's root, resolved in Step 0, never the cwd. The repo's location and name
are per-machine detail, never hardcoded here.

## Arguments

- Optional free-text: the topic or content the user wants to remember

## Workflow

### Step 0: Resolve the knowledge-base root, and check whether this session is rooted there

Before anything else, resolve the absolute path to the knowledge-base repo —
the same pointer file the Memory Bootstrap rule in CLAUDE.md uses, so the two
never drift apart:

```bash
MEMORY_REPO_ROOT="${MEMORY_REPO_ROOT:-$(cat ~/.skadi/memory-repo.md 2>/dev/null)}"
```

The `MEMORY_REPO_ROOT` env var is the override; `~/.skadi/memory-repo.md` is the
source when it is unset. If neither yields a path, ask the user once where
their knowledge-base repo lives, then write the answer into
`~/.skadi/memory-repo.md` — never guess the path, and never ask again once
recorded (mirrors CLAUDE.md's Memory Bootstrap). Confirm the resolved path
exists (`test -d "$MEMORY_REPO_ROOT"`); if it does not, tell the user plainly
and stop — do not write the note into the cwd.

**Then check the session's own root against it:**

```bash
SESSION_ROOT=$(cd "${CLAUDE_PROJECT_DIR:-$PWD}" 2>/dev/null && pwd)
```

- **If `$SESSION_ROOT` is `$MEMORY_REPO_ROOT` or nested under it** — proceed with
  Steps 1–5 below exactly as written; every file and git operation targets
  `$MEMORY_REPO_ROOT`.
- **Otherwise** — this session is rooted outside the knowledge-base repo, so a
  direct write is `dir-guard.sh`'s to refuse, and `protected-repo-guard.sh`
  names the channel to route through instead. Skip straight to **Step 0b**
  below instead of Steps 1, 4, and 5.

All paths named below (`work/…`, `personal/…`) are **relative to
`$MEMORY_REPO_ROOT`**. Read, write, and commit against the absolute path;
never against the working directory the session happens to sit in.

### Step 0b: Redirect through /handoff (only when outside the knowledge-base repo)

Still run **Step 2 (category)** and **Step 3 (sub-category)** below to shape the
note correctly — that judgment doesn't need the repo's tree, only the user's
input. Skip **Step 1** (duplicate check — it greps the live repo, unreachable
from here) and **Steps 4–5** (the direct write/commit/push).

Compose the note body exactly as Step 4 describes (title, company blockquote if
under `work/`, content, date line) but prefix it with the intended path as a
heading, so the receiving session knows where to file it:

```markdown
# Intended path: <category>/<sub-folder>/<filename>.md

<the note content, per Step 4>
```

Send it, over the same handoff channel `~/.skadi/protected_repos.md` maps this
repo to:

```bash
printf '%s' "<composed note>" | ~/.claude/hooks/handoff.sh send memory
```

Tell the user plainly: *"Not rooted in the knowledge-base repo — queued this
note on the `memory` handoff channel instead of writing directly. Open a
session there and run `/handoff read memory` to file it."* Do not proceed to
Steps 4–5.

### Step 1: Check for Duplicates

Before creating anything, search the knowledge-base repo for existing notes on
the same topic:

1. Use Grep over `$MEMORY_REPO_ROOT` to search for key terms from the user's
   input across all `.md` files.
2. If a relevant note already exists, ask the user using AskUserQuestion:

```
question: "Found an existing note at <path>. Update it or create a new one?"
header: "Existing note found"
options:
  - label: "Update existing"
    description: "Append or modify <path>"
  - label: "Create new"
    description: "Create a separate note"
```

3. If updating, edit the existing file and skip to the end (show the path).

### Step 2: Determine Main Category

Check if the user's input clearly belongs to one of these top-level categories:

| Category | Purpose |
|----------|---------|
| `work/` | Engineering, tools, processes, debugging, management |
| `personal/` | Finance, health, learning, home |

If the category is **not obvious** from context, ask the user using AskUserQuestion:

```
question: "Which category does this belong to?"
header: "Category"
options:
  - label: "Work"
    description: "Engineering, tools, processes, debugging, management"
  - label: "Personal"
    description: "Finance, health, learning, home"
```

### Step 3: Determine Sub-Category

Each top-level category has sub-folders, plus shared `projects/` and `resources/` folders:

**work/**
| Sub-folder | What goes here |
|------------|---------------|
| `engineering/` | Architecture, design patterns, code review, language knowledge |
| `tools/` | IDE setup, CLI tools, CI/CD, Docker, Git workflows |
| `processes/` | Team workflows, agile/sprint, on-call, incident response |
| `debugging/` | Debugging techniques, postmortems, failure modes |
| `management/` | 1:1s, career growth, hiring, feedback, people & roles |
| `projects/active/` | Active project notes |
| `projects/archive/` | Archived project notes |
| `resources/bookmarks/` | Bookmarked links |
| `resources/cheatsheets/` | Quick reference sheets |
| `resources/reading-notes/` | Notes from articles, books, talks |

**personal/**
| Sub-folder | What goes here |
|------------|---------------|
| `finance/` | Budgeting, taxes, investments, insurance |
| `health/` | Exercise, nutrition, medical, mental health |
| `learning/` | Courses, skill-building, language learning |
| `home/` | Home maintenance, cooking, travel, local services |
| `projects/active/` | Active personal project notes |
| `projects/archive/` | Archived personal project notes |
| `resources/bookmarks/` | Bookmarked links |
| `resources/cheatsheets/` | Quick reference sheets |
| `resources/reading-notes/` | Notes from articles, books, talks |

1. Pick the best-fitting sub-folder from the tables above.
2. If none fits, suggest a new sub-folder name using AskUserQuestion:

```
question: "No existing sub-folder fits. Create a new one?"
header: "Sub-folder"
options:
  - label: "<suggested-name>"
    description: "New sub-folder for this topic"
  - label: "Place in <category>/ root"
    description: "Skip sub-folder, put it directly in the category"
```

If a new sub-folder is created, also create a `README.md` in it following the pattern of existing READMEs.

### Step 4: Write the Note

1. Pick a `kebab-case.md` filename that captures the topic.
2. Write the file under `$MEMORY_REPO_ROOT/<category>/<sub-folder>/<filename>.md` with:
   - A top-level `# Title` heading
   - If the note belongs under `work/`, a `> **Company:** <employer>` blockquote near the top identifying which employer the content pertains to (default: Jubo Health — confirm with the user if the content looks cross-company or generic)
   - The knowledge content, organized clearly
   - A date line if the content is time-sensitive: `*Captured: YYYY-MM-DD*`
3. Show the user the full file content and path.

### Step 5: Confirm and Commit

Ask the user using AskUserQuestion:

```
question: "Save this note to the knowledge base?"
header: "Confirm"
options:
  - label: "Save"
    description: "Commit and push to remote"
  - label: "Discard"
    description: "Delete the file, nothing saved"
```

- If **Save**: run the git steps against the knowledge-base repo, not the cwd —
  `git -C "$MEMORY_REPO_ROOT" add <relative-path> && git -C "$MEMORY_REPO_ROOT" commit -m "Add note: <filename>" && git -C "$MEMORY_REPO_ROOT" push`
- If **Discard**: delete the file and notify the user.

## Rules

- One focused topic per file.
- File names use `kebab-case.md`.
- Use relative paths for cross-references between notes.
- Don't over-structure — keep notes concise and scannable.
- If the user provides multiple unrelated things to remember, create separate files for each.
- Every file and git operation targets `$MEMORY_REPO_ROOT` (Step 0), never the working directory.
