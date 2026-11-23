---
name: ck-migrate
description: "Update an existing ContextKit project to this hub's version. Scripts, skills, and VERSION are refreshed; config, the index cache, and unrelated files stay. Run from the hub: /ck-migrate"
disable-model-invocation: true
---

# ck-migrate

Only useful in the **hub**. Brings an installed project up to this blueprint, and keeps its configuration, index, and own files.

## Resolve project root

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
echo "$CK_ROOT"
```

## Step 1 — Confirm the hub

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/contextkit_config.py" | grep isHub
```

Expect `isHub: True`. Otherwise stop: `/ck-migrate` runs from a session on the ContextKit hub, not inside the project.

## Step 2 — Target path

If the user already passed a path (`/ck-migrate <path>`), use it. Otherwise ask for the **absolute path** of the project to update. Check that the path exists.

## Step 3 — Update

```bash
CK_ROOT="${CLAUDE_PROJECT_DIR:-}"; [ -d "$CK_ROOT/.claude/contextkit" ] || CK_ROOT="$(d="$PWD"; while [ "$d" != "/" ] && [ ! -d "$d/.claude/contextkit" ]; do d="$(dirname "$d")"; done; echo "$d")"; [ -d "$CK_ROOT/.claude/contextkit" ] || { echo "ContextKit not found: no .claude/contextkit in this directory or any parent"; exit 1; }
python3 "$CK_ROOT/.claude/contextkit/scripts/install.py" "<target-path>" --update
```

Refreshes `contextkit/scripts/`, `VERSION`, and the skills **ContextKit installed** (from the manifest `.installed.json`). **Left in place:** `contextkit.config.json`, `cache/`, skills that are not ContextKit's, `settings*.json`. The script reports `version old → new`.

## Step 4 — Verify

Run the target's doctor (that script self-locates, so the root is the target project):

```bash
python3 "<target-path>/.claude/contextkit/scripts/doctor.py"
```

Summarize the findings. If the schema changed between versions, point the user at the adjustments they need (if useful, `/ck-setup` in project mode to reconfigure).

## Before the next version bump — trim the harness

Before `VERSION` is raised in the hub: skim the skills and ask whether each instruction or workaround is still needed, or whether a newer model now does it unaided (for example an explicit step-by-step that the model now gets right without the guide). Delete what is redundant. Do not let the harness grow. No new automation — one deliberate check per bump.
