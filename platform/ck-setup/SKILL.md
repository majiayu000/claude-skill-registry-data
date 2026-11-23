---
name: ck-setup
description: "Conversational ContextKit setup assistant. In the hub: install (merge-safe) into a project and configure it. In an installed project: reconfigure only. Run: /ck-setup"
disable-model-invocation: true
---

# ck-setup

Conversational setup assistant (questions happen in the session, not over stdin).

> `/ck-setup` runs in the **hub** (fresh install) or in an already **installed project** (reconfigure). If the mode check below fails with "file not found", or the root walk reports that ContextKit is not found, you are in some other project that does not have ContextKit installed: stop, and say that a fresh install starts from the **ContextKit hub** (run `/ck-setup` there, then give this project's path). Do not suggest running `/ck-setup` here again — that would loop.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

Then detect the mode:

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/contextkit_config.py" | grep isHub
```

- `isHub: True` → section **A** (install + configure)
- otherwise → section **B** (reconfigure only)

---

## A) Hub mode — merge-safe install + configure

### A1 — Ask for the target project and the platform

Ask the user for the **absolute path of the project**. Check that it exists.

Ask which platform to store. Known values: `generic` (default), `ios`, `android`, `web`.

#### Only when platform=ios

Also check that the project folder contains a `.xcodeproj` or `.xcworkspace`.

### A2 — Ask where to install the skills

Ask for the skill location: **global** (`~/.claude/skills/`, recommended — private, not in git, available in every project) or **local** (`<project>/.claude/skills/`, git-excluded). Always copies, never symlinks — the target project does not depend on where the hub sits.

### A3 — Install (merge-safe)

Global (recommended):

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/install.py" "<target-path>" --skills-global
```

Local:

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/install.py" "<target-path>" --skills-local
```

The script reports what it does. If it stops because ContextKit is already there → offer `/ck-migrate`.

### A4 — Configure — **with the target project's scripts**

From here on, call `<target-path>/.claude/contextkit/scripts/...` (those scripts self-locate, so the root is the target project, not the hub). Ask for the reference folder (default `../references`), then:

```bash
python3 "<target-path>/.claude/contextkit/scripts/setup.py" --scan --references-path "<rel>"
```

Let the user pick the git repos it found (JSON) with a **multi-select**. If the scan finds nothing → ask for the correct path, or whether the repos still need to be cloned. Ask for the knowledge folder (default `../project-knowledge`) and confirm the ticket pattern (default `[A-Z][A-Z0-9]+-\d+`). Write, including the platform from A1:

```bash
python3 "<target-path>/.claude/contextkit/scripts/setup.py" --write \
  --references-path "<rel>" --repos "<a,b>" \
  --knowledge-path "<rel>" --ticket-pattern "<pattern>" \
  --platform "<platform>" --create-knowledge
```

`--create-knowledge` creates the knowledge folder when it is missing. `setup.py` then runs `git init` in that folder when it is not already a git repo.

### A5 — Verify and finish

```bash
python3 "<target-path>/.claude/contextkit/scripts/doctor.py"
```

Summarize the findings briefly. Then tell the user:

- Work **in the project** from here on (Claude Code).
- Build the first reference index: in the project, `/ck-refs-sync`.

#### Only when platform=ios

In Xcode, once: **Intelligence → Plug-ins → Add Plug-in → Import from Claude Code** (imports the skills, not the SessionStart hook — branch-ticket and hygiene reminders in the Xcode agent come from running `/ck-doctor` manually).

---

## B) Project mode — reconfigure only

The session is already in an installed project. `$CK_ROOT` from the resolve step is that project. Ask for the platform (`generic` by default, or `ios`, `android`, `web`), then the reference folder, scan, multi-select, knowledge folder, and ticket pattern — the same questions as A4.

#### Only when platform=ios

If the user switches the platform to `ios`, check that `$CK_ROOT` contains a `.xcodeproj` or `.xcworkspace`.

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/setup.py" --scan --references-path "<rel>"
```

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/setup.py" --write \
  --references-path "<rel>" --repos "<a,b>" \
  --knowledge-path "<rel>" --ticket-pattern "<pattern>" \
  --platform "<platform>" --create-knowledge
```

`--create-knowledge` creates the knowledge folder when it is missing, and `setup.py` runs `git init` there when it is not already a git repo.

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/doctor.py"
```

#### Only when platform=ios

After doctor, mention the one-time Xcode step: **Intelligence → Plug-ins → Add Plug-in → Import from Claude Code**. Skills transfer; the SessionStart hook does not — use `/ck-doctor` in the Xcode agent for branch-ticket and hygiene reminders.
