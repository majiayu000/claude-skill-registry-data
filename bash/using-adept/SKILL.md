---
id: using-adept
description: "Use the `adept` CLI to author an AI skill once and render it into Claude Code, Cursor, Codex, Copilot, OpenCode, and 45+ agents. Apply when installing/syncing skills, editing SKILL.md, or touching .adeptability/."
activation: agent
allowed-tools:
  - "Bash"
  - "Read"
  - "Edit"
  - "Write"
---

# Using the `adept` CLI

`adept` makes one AI skill portable across every coding harness. You **author once** in a
canonical format; `adept` **renders accurately** into each harness's native layout and keeps
both sides in sync.

## Mental model

```
canonical skill  ──render──▶  .claude/skills/…       (per-skill)
(.adeptability/  ──render──▶  .cursor/rules/….mdc    (single-file)
 skills/<id>/    ──render──▶  AGENTS.md              (Codex aggregate)
 SKILL.md)       ──render──▶  .github/instructions   (Copilot aggregate)
                 ◀─sync-from─  (adopt edits made directly in a harness file)
```

- **Identity is `(id, content-hash)`** — no version numbers. The hash decides what changed.
- A skill is a directory `<root>/skills/<id>/` with one `SKILL.md` (YAML frontmatter +
  markdown body) and optional sidecars (`scripts/`, `references/`, `assets/`).
- An **agent** (subagent) is a single file `.adeptability/agents/<id>.md`; it renders to
  `.claude/agents/`, `.opencode/agents/`, `.cursor/agents/`, `.github/agents/`, and
  `.codex/agents/*.toml` the same way. See [[authoring-adept-agents]].
- The **filesystem is the source of truth.** `config.json` only records enabled harnesses,
  the materialization mode, and library remotes.

## The commands you'll use most

```bash
adept init                       # scaffold .adeptability/ (and seed the default skills)
adept harness add <id>           # enable a harness (claude-code | cursor | codex | copilot | opencode | …)
adept sync                       # render canonical skills → every enabled harness
adept status                     # init state, libraries, harnesses, and drift at a glance
adept diff                       # show exactly what differs between canonical and rendered
adept sync-from                  # adopt edits made directly in a harness file back to canonical
adept skill add <id> --edit      # scaffold a new skill and open $EDITOR
adept skill install <owner>/<repo>/<skill>   # install one skill (pinned to a SHA, safety-scanned)
adept agent add <id> --edit      # scaffold a new agent (subagent); --template evaluator for reviewers
adept agent check <id>           # safety scan + best-practice lint for an agent
adept loop add <id> --workflow   # compose a loop: discovery skill + evaluator agent + cron skeleton
```

**`adept --help` is the source of truth for the command surface** — it's always current, so
prefer it over memory. `adept --help` lists every verb; `adept <command> --help` (e.g.
`adept skill --help`, `adept sync --help`) shows that command's subcommands and flags. Global
flags on every command: `--json`, `--log-level debug|info|warn|error`, `--project <path>`,
`--library <path>`.

## Rules of thumb (so you don't surprise the user)

- **Edit canonical, then `adept sync`.** Don't hand-edit rendered files like
  `.cursor/rules/*.mdc` — they're regenerated. Edited a harness file directly? Run
  `adept sync-from` to pull it back into canonical first.
- **Run `adept status` / `adept diff` before and after a sync** so you can report what changed.
- **Installs are gated.** `adept skill install` runs a safety scan and shows a preview; a
  `critical` finding blocks unless the user passes `--allow-unsafe`. Never pass
  `--allow-unsafe` or `--yes` on the user's behalf without explicit confirmation.
- **Exit codes are meaningful:** `0` clean, `1` error, `2` drift/dirty or merge conflict.
  Scan severities map the same way (`high` → 1, `critical` → 2).
- **Secrets stay in the environment.** Provider API keys are read from the environment at
  call time; adept never writes them to `config.json`.
- Aggregator harnesses (Codex/Copilot) have a **byte budget** — overflow drops the
  lowest-priority skills with a truncation note. Check `adept status`.
