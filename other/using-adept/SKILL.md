---
id: using-adept
description: "Use the `adept` CLI to author AI skills once and render them into Claude Code, Cursor, Codex, Copilot, and OpenCode. Apply when installing/syncing skills, editing skill.yaml/SKILL.md, or touching .adeptability/."
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
canonical skill  ──render──▶  .claude/skills/…   (per-skill)
(.adeptability/  ──render──▶  .cursor/rules/….mdc (single-file)
 skills/<id>/    ──render──▶  AGENTS.md            (Codex aggregate)
 SKILL.md)       ──render──▶  .github/instructions (Copilot aggregate)
                 ◀─sync-from─  (adopt edits made directly in a harness file)
```

- **Identity is `(id, content-hash)`** — there are no version numbers. The hash decides
  whether something changed.
- A skill is a directory `<root>/skills/<id>/` with one `SKILL.md` (YAML frontmatter +
  markdown body) and optional sidecars (`scripts/`, `references/`, `assets/`).
- The **filesystem is the source of truth.** `config.json` only records which harnesses are
  enabled, the materialization mode, and library remotes.

## Canonical SKILL.md format

```markdown
---
id: pr-review                 # ^[a-z0-9](?:[a-z0-9-]{0,48}[a-z0-9])?$ — matches the directory name
description: Use before opening a PR. Tests, security, performance.   # <= 280 chars
activation: agent             # always | globs | agent | manual
globs: []                     # REQUIRED when activation: globs
allowed-tools: [Read, Grep]   # carried into Claude Code
targets: []                   # empty = all enabled harnesses
tags: [review, quality]
---
# PR Review Checklist
- [ ] Tests added or updated
- [ ] No secrets in the diff
```

## The commands you'll use most

```bash
adept init                       # scaffold .adeptability/ in the current project
adept init --from <git-url>      # …and clone a remote skill library to pull skills from
adept harness add claude-code    # enable a harness (claude-code | cursor | codex | copilot | opencode)
adept harness list
adept sync                       # render canonical skills → every enabled harness
adept status                     # init state, libraries, harnesses, and drift at a glance
adept diff                       # show exactly what differs between canonical and rendered
adept sync-from                  # adopt edits made directly in a harness file back to canonical
```

Authoring and sharing skills:

```bash
adept skill add my-skill --edit          # scaffold a new skill and open $EDITOR
adept skill list                         # skills resolved for this project (canonical + libraries)
adept skill search <query>               # find installable skills on skills.sh
adept skill install <owner>/<repo>/<skill>   # install one skill from GitHub/skills.sh (pinned to a SHA)
adept skill check <target>               # static safety scan (project | library:<name>:<id> | owner/repo/skill)
adept library add <name> --from <git-url>    # stack a remote library; first-wins on id collisions
```

Global flags on every command: `--json`, `--log-level debug|info|warn|error`,
`--project <path>`, `--library <path>`.

## Typical tasks

**Start fresh, author your own skills**
```bash
adept init
adept skill add lint-style --edit
adept harness add claude-code
adept harness add cursor
adept sync
```

**Adopt a project that already has harness files** (`.claude/`, `.cursor/`, `AGENTS.md`, …)
```bash
adept init        # auto-detects and adopts existing harness skills into canonical
adept status      # confirm what got adopted
adept diff        # confirm the round-trip is clean
```

**Pull skills from a shared library**
```bash
adept init --from git@github.com:my-org/skills.git
adept harness add claude-code
adept sync
```

**Install one vetted skill from the ecosystem**
```bash
adept skill search find-skills
adept skill info  vercel-labs/skills/find-skills    # repo, stars, license, SHA, installs
adept skill install vercel-labs/skills/find-skills  # preview + safety scan + y/N
```

## Rules of thumb (so you don't surprise the user)

- **Edit canonical, then `adept sync`.** Don't hand-edit rendered files like
  `.cursor/rules/*.mdc` — they're regenerated. If you must edit a harness file directly, run
  `adept sync-from` to pull the change back into canonical.
- **Run `adept status` / `adept diff` before and after** a sync so you can report what changed.
- **Installs are gated.** `adept skill install` runs a safety scan and shows a preview; a
  `critical` finding blocks the install unless the user passes `--allow-unsafe`. Never pass
  `--allow-unsafe` or `--yes` on the user's behalf without explicit confirmation.
- **Exit codes are meaningful:** `0` clean, `1` error, `2` drift/dirty or merge conflict.
  Scan severities map the same way (`high` → 1, `critical` → 2).
- **Secrets stay in the environment.** Provider API keys are read from the environment at
  call time; adept never writes them to `config.json`.
- Aggregator harnesses (Codex/Copilot) have a **byte budget** — if skills overflow it,
  the lowest-priority ones are dropped and a truncation note is written. Check `adept status`.
