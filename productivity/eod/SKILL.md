---
name: eod
description: Use when the user runs /eod or says they're calling it a day. Scans configured project repos for uncommitted/unpushed work so nothing gets left behind. Asks once for the project list, remembers it.
purpose: Scans configured repos for uncommitted or unpushed work before calling it a day.
user_invocable: true
stage: desk
composes: commit:dispatch
---

# End of Day

Quick sweep across your active repos for anything that shouldn't be left overnight. Right now the only check is git state (uncommitted + unpushed). More checks can be added later.

## Workflow

### 1. Resolve project roots

Read the memory file `eod_project_roots.md`. It should contain a list of absolute (or `~`-relative) directory paths, one per line, possibly bulleted.

**If the memory exists and has paths**, use them.

**If the memory is missing or empty**, ask via AskUserQuestion:

```
question: "Which project directories should /eod scan?"
options:
  - label: "Current directory only"
    description: "Just the cwd this time. Don't save."
  - label: "Pick from ~ subdirs"
    description: "List git repos under ~ and let me multi-select."
```

The "Other" option lets the user paste paths (comma-separated).

If the user picks the "pick from ~ subdirs" path, list git repos with:

```bash
find ~ -maxdepth 3 -name .git -type d 2>/dev/null | sed 's|/.git$||' | sort
```

Then present them via a multi-select AskUserQuestion (cap at the first ~20; tell the user to edit the memory file directly for more).

After the user picks, save the chosen roots to `eod_project_roots.md`:

```markdown
---
name: EOD Project Roots
description: Filesystem paths scanned by /eod for uncommitted/unpushed git work.
type: reference
---

Roots:
- <path1>
- <path2>
```

Add a pointer line to `MEMORY.md`:

```
- [EOD Project Roots](eod_project_roots.md) — paths scanned by /eod
```

If the user picked "current directory only", skip the save and use `pwd`.

### 2. Run the git check

Use the pre-approved hook to avoid permission prompts:

```bash
~/.claude/hooks/eod-git-check.sh <root1> <root2> ...
```

Output is pipe-delimited, one line per root:

```
DIR|STATE|DIRTY|UNTRACKED|AHEAD|BRANCH|REMOTE
```

States: `ok`, `dirty`, `unpushed`, `both`, `no-git`, `no-remote`, `error`.

### 3. Render the report

Group rows by state, in this order: `both` → `dirty` → `unpushed` → `no-remote` → `error` → `ok` (collapse `ok` into a single tally line at the bottom).

**Header:**
```
EOD Sweep — N repos scanned
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Per-repo lines** (omit empty groups):

- `dirty` / `both`:  `⚠️  <dir>  ·  <branch>  ·  <D> modified, <U> untracked`
- `unpushed` / `both`:  `↑  <dir>  ·  <branch> → <remote>  ·  <A> ahead`
- `no-remote`:  `◌  <dir>  ·  <branch>  ·  no upstream set`
- `no-git`:  `?  <dir>  ·  not a git repo`
- `error`:  `✕  <dir>  ·  git error`

If a repo is in `both` state, render two lines (one under `dirty`, one under `unpushed`) so the user sees both signals.

**Footer:**

```
─────────────────────────────────────────
  N clean · N dirty · N unpushed · N other
```

If everything is clean:

```
EOD Sweep — N repos scanned
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓  All clear. Go home.
```

### 4. Suggest next step

If there are any `dirty` or `unpushed` rows, end with one short line — no checklist, no nagging:

> Worth a `/commit --push` in those before you log off.

Skip the suggestion when everything is clean.

## Rules

- Never commit, push, or modify any repo automatically — this skill only reports.
- Don't ask the user to confirm before running the scan; just run it.
- If the memory file lists a path that doesn't exist anymore, treat it as `no-git` and continue — don't fail the whole sweep.
- To change the scanned roots, the user can edit `eod_project_roots.md` or delete it to re-prompt.
