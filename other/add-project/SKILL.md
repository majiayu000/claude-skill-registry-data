---
name: add-project
description: Append an existing repo to registry.yaml so the team-lead can find and coordinate with it. Used directly to register an existing repo, or called by /new-project as its final step.
---

# Add Project to Registry

Append an existing repo to `registry.yaml` so the team-lead can find and coordinate with it via claude-hive.

## When to use this

- `/add-project` — the repo already exists; just register it.
- `/new-project` — scaffold a brand-new repo (GitHub + Linear + `.claude/` + docs). That skill calls `/add-project` as its final step once everything is created.

## Steps

1. **Gather info** (ask the user if not provided):
   - **Name** — kebab-case, e.g., `example-project`. Used as the registry key and the local directory name.
   - **Local path** — usually `~/dev/<name>`
   - **GitHub repo** — `<owner>/<repo>`, e.g., `your-org/example-project`
   - **Linear team** — name + key, if the project uses Linear

2. **Verify the path exists and is a git repo:**
   ```bash
   git -C <path> rev-parse --show-toplevel
   ```
   If this doesn't resolve, stop and ask the user where the repo actually lives.

3. **Read `registry.yaml`** and confirm the project isn't already registered. If it is, warn the user and stop.

4. **Append a new entry** to `registry.yaml` following the schema in `registry.yaml.example`. Typical fields:
   ```yaml
   <name>:
     path: <local-path>
     repo: <owner>/<repo>
     linear:
       team_name: <name>
       team_key: <key>
   ```

5. **Do NOT commit.** `registry.yaml` is gitignored and lives only in the main worktree. Tell the user the entry has been added and not to commit it.

6. **Suggest next steps** to the user:
   - Make sure the project's `.claude/settings.json` enables the `team-lead-fleet` plugin (one line: `"team-lead-fleet@team-lead-fleet": true` under `enabledPlugins`). That gives the project all fleet-wide skills + alwaysApply rules without copying any files.
   - Start a Claude Code session in the project repo so the team-lead can reach it via claude-hive. Each peer registers itself with the claude-hive broker on startup.

## Principles

- **Tiny skill on purpose.** Registry maintenance is a 5-minute operation; don't inflate it with onboarding steps that belong in `/new-project`.
- **Private file.** `registry.yaml` contains project names and team IDs; never commit it or include its contents in PR descriptions.
