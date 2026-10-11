---
name: graphify-setup
description: Graphify plugin — enable, detect paths, configure and rebuild via devteam plugin.
---

## Skip Conditions

Do not run this setup if any of the following are true:

- The project contains **no JavaScript, TypeScript, or Python source files** (check: `find . -name "*.js" -o -name "*.ts" -o -name "*.py" | grep -v node_modules | head -1`)
- `devteam plugin show graphify --json` already reports `enabled: true` and `configured: true`, and the project structure hasn't changed
- The user explicitly says graphify is not relevant to their stack (pure mobile, database-only, embedded, etc.)

If the project type is ambiguous, ask once with `AskUserQuestion` whether JavaScript, TypeScript, or Python is the primary language before Step 1.

---

## Purpose

Graphify is a plugin (`plugins/graphify/`, ADR-0019). Its settings live in the committed
`.dev-team-agents/plugin-settings/graphify.json`, and every step below goes through the `devteam plugin`
CLI — never write that file by hand. The desktop app's **Plugins** tab on the project screen does the
same steps with a form. Ask the user only when the CLI cannot proceed on its own.

---

## Step 1 — OS Detection

Run `uname -s`: `Darwin` → macOS, `Linux` → Linux or WSL. On `MINGW*` / `MSYS*` / other (Windows),
check `wsl --status 2>/dev/null || echo "WSL_NOT_FOUND"`:

- **WSL active** → run every later step inside WSL (`wsl bash -c "<command>"`)
- **WSL not found** → stop and tell the user that Windows without WSL is not supported, linking
  https://learn.microsoft.com/en-us/windows/wsl/install; resume once WSL is active

---

## Step 2 — Requirements

```bash
devteam plugin show graphify --json
```

If `ready` is `false`, run `/devteam:install` for every binary whose `found` is `false` (each entry's
`install_hint` names the command — `graphify` and `jq`) and wait for it to finish. That command owns
the cross-OS install logic; do not install them here. Do not continue until `ready` is `true`.

If `source` is `"legacy"`, run `devteam sync` first: it moves `.dev-team-agents/user-data/graphify.json`
into the settings file, and the rest of this skill then edits the moved config.

---

## Step 3 — Detect and Enable

```bash
devteam plugin run graphify detect --json   # proposes {targetPaths, manifestPaths}; writes nothing
devteam plugin enable graphify --json       # seeds the config from detect when none exists yet
```

`detect` maps root manifests to a stack and keeps the conventional source directories that exist
(`plugins/graphify/scripts/detect.py`). If `enable` reports `configured: false` — detect found no
source directory — show the user the top-level directories and ask once which ones belong in the
graph, then:

```bash
devteam plugin config set graphify targetPaths '["src","lib"]'
devteam plugin config set graphify manifestPaths '["package.json","package-lock.json"]'
```

Values are JSON arrays. A wrong type exits 2 without writing.

---

## Step 4 — .gitignore

```bash
grep -qxF "graphify-out/cache" .gitignore 2>/dev/null || echo "graphify-out/cache" >> .gitignore
```

`graphify-out/` itself is versioned; only its cache is ignored. The last-build marker lives in the
machine-local `state.json`, which is already ignored. The settings file is committed.

---

## Step 5 — First Build

```bash
devteam plugin run graphify rebuild --json
```

`ok: true` means `graphify-out/` was rebuilt at the project root. On `ok: false`, show the user
`log_tail`:

| Symptom | Fix |
|---------|-----|
| Exit 3, requirement missing | Complete Step 2 |
| Exit 4, plugin disabled | `devteam plugin enable graphify` |
| `Required source '<dir>' not found` | Correct `targetPaths` (Step 3) |

---

## Step 6 — Refresh Policy

Rebuilds are on demand by default: `devteam plugin run graphify rebuild`. To also rebuild at session end
whenever a source path changed structurally — at a cost on every Stop — the user opts in with:

```bash
devteam plugin config set graphify auto_refresh true
```

Ask with `AskUserQuestion` (Keep on demand — recommended / Refresh at session end); never turn it on
silently.

---

## Step 7 — Inject CLAUDE.md Section

If the project `CLAUDE.md` has no `## Context Navigation (Graphify)` section, **append** (never replace):

```markdown
## Context Navigation (Graphify)

**3-Layer Query Rule:**
1. Query `graphify-out/graph.json` or `GRAPH_REPORT.md` for structure and relationships
2. Check `docs/` for decisions and context
3. Read raw source files only when editing or when layers 1–2 lack the answer

**Rebuild:** `devteam plugin run graphify rebuild` — never `graphify update .` directly.
Rebuild after new modules/services, structural reorganization, or domain flow changes.
```

---

## Step 8 — Confirm Setup

Report to the user, filling the values from `devteam plugin show graphify --json`:

```
✅ Graphify is set up for this project.

  Knowledge graph : graphify-out/  (versioned)
  Settings        : .dev-team-agents/plugin-settings/graphify.json  (committed — applies to the whole team)
  Source paths    : <config.targetPaths>
  Refresh         : on demand | at session end (auto_refresh)
  Status          : <status.summary>
```
