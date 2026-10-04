---
name: new-project
description: Use when the user asks to start, scaffold, or spin up a new project — a new repo, a new client or advisory engagement, or a new piece of work that needs its own agent.
user-invocable: true
---

# Scaffold a New Project

Create a fully set up project from scratch — GitHub repo, Claude Code configuration, documentation structure, registry entry, and a live session working on the first task.

**Finish the job.** The user asked for a project, which means a repo they can work in and an agent already on the first task — not a repo plus a list of things left for them to do. The last step is a running session with its goal, not instructions.

## Steps

### 1. Gather only what you can't determine

Ask for what genuinely changes the work, in ONE batched message. Default the rest and say what you defaulted.

- **Project name** — repo name, directory name, tmux session name.
- **What it is** — enough to write an honest Overview. If the user has already described it (a brief, meeting notes, a linked doc), you have this; don't ask again.
- **Language/stack** — or none, for a docs-only or research project. "None" is a real answer; don't invent a stack to fill the template.

Default without asking, and state the default in your reply:

| Thing | Default | Override when |
| --- | --- | --- |
| Visibility | **private** | The user says public, or it's an open-source utility |
| Linear | **skip** | The user asks for it. Only 8 of 24 registry projects use Linear — it is the exception, not the norm |
| Ship skill | `ship-auto` | Advisory or team-owned repo → `ship-push-only`; production tool the user depends on → `ship-guarded` |
| Path | `~/dev/<project-name>` | Never, unless the user names one |
| `respawn` | `true` | The project is a one-off with no ongoing work |

### 2. Create the GitHub repo

Use the `gh` CLI — the GitHub MCP plugin is unreliable for private and new repos (see `docs/process/learnings.md`).

```bash
gh repo create <owner>/<project-name> --private --description "<one-line>" --clone=false
git clone git@github.com:<owner>/<project-name>.git ~/dev/<project-name>
```

The clone at `~/dev/<project-name>` is the project's permanent home. Everything after this reads from there.

**Local-only projects** (a synced Drive folder, a scratch dir) skip this entirely — no repo, no `repo:` field in the registry, and no git commands ever. See the registry section of the root `CLAUDE.md`.

### 3. Scaffold from `templates/`

Copy from this skill's `templates/` directory:

| Template | Destination |
| --- | --- |
| `templates/settings/settings.json` | `.claude/settings.json` — add language plugins (`pyright-lsp` for Python, `typescript-lsp` for TS) |
| `templates/settings/settings.local.json` | `.claude/settings.local.json` — compaction ceilings, untracked |
| `templates/gitignore` | `.gitignore` |
| `templates/docs/process/learnings.md` | `docs/process/learnings.md` |
| `templates/docs/process/retrospective.md` | `docs/process/retrospective.md` |
| `templates/docs/process/process.md` | `docs/process/process.md` |
| `templates/docs/product/decisions.md` | `docs/product/decisions.md` |
| `templates/docs/product/vision.md` | `docs/product/vision.md` |

**`CLAUDE.md` is different — `templates/docs/CLAUDE.md.tmpl` is an outline, not boilerplate.** Write it from what you actually learned about the project. A CLAUDE.md of filled-in placeholders costs every future session tokens and teaches them nothing; cut any section you can't write honestly.

**Compaction ceilings:** the template ships assistant values (`500000` / `80` → compacts at ~400k). For a builder — a project that will run long implementation sessions — use `600000` / `80` (~480k). Env is read at session start, so this must exist before step 6 spawns the session.

**Do NOT copy skills or rules.** The `team-lead-fleet` plugin provides them fleet-wide; a local copy just goes stale.

**Also drop in any source material the user gave you** — meeting notes, a brief, a spec. Commit it verbatim under `docs/` as the primary source, so downstream analysis cites the original rather than your summary of it.

### 4. Commit and push

```bash
cd ~/dev/<project-name>
git add -A && git commit -m "Initial scaffold: <one-line>" && git push origin main
```

### 5. Register the project

Invoke `/add-project`, or append to `registry.yaml` directly. Required fields:

```yaml
  <project-key>:
    type: personal | advisory | client
    ship_method: ship-auto
    path: ~/dev/<project-name>
    repo: <owner>/<project-name>      # omit entirely for local-only
    respawn: true
    session_name: "Display Name"       # tmux session + agent display name
    docs:
      learnings: docs/process/learnings.md
      retros: docs/process/retrospective.md
      decisions: docs/product/decisions.md
      claude_md: CLAUDE.md
    skills_dir: .claude/skills
    rules_dir: .claude/rules
```

`registry.yaml` is gitignored — never commit it. Adding the project here also makes its name a denylist term for the pre-push leak gate on the public repo, which matters for client work.

### 6. Spawn the session and hand off the goal

```bash
python3 .claude/skills/respawn-sessions/respawn.py --mode missing --execute
```

`missing` mode spawns only what isn't already running, so it's safe to run with the fleet up. Confirm the pane shows the session name and the `/rc` marker.

Then send the first task via `claude-hive send_message`: the **outcome**, who reads it, the deadline, where the source material is, and any constraint that genuinely narrows the answer. No step-by-step checklist and no "report back when done" — see `feedback_delegating_to_peers` and `feedback_dont_wire_in_status_reports`.

### 7. Report to the user

The repo URL, what you defaulted, what the session is now working on, and anything you deliberately left out. One short message — they don't need the file list.

## Principles

- **Fast and complete.** Zero to a working project with an agent on the first task, in one invocation.
- **Plugin first.** `team-lead-fleet` is the source of fleet skills and rules — never copy them in.
- **Default, don't interrogate.** Ask only what changes the work; state every default you took so the user can correct one cheaply.
- **Honest scaffolding beats complete scaffolding.** A missing section is fixable; a section of confident filler has to be detected first.
