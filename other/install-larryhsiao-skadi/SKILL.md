---
name: install
description: Install Skadi into every registered paired Claude Code and Codex profile. Use when the user asks to install, sync, propagate, or update this Skadi configuration from the Skadi repository.
---

# Install Skadi

Run only from the Skadi repository.

1. Resolve the repository root with `git rev-parse --show-toplevel` and confirm
   that `install.sh`, `AGENTS.md`, and `settings.json` exist there.
2. Read `~/.skadi/install/roots.tsv`. Each row is
   `<profile><TAB><claude-root><TAB><codex-root>`.
3. If the registry is absent, explain that `--all` registers one pair —
   `default`, at `~/.claude` and `~/.codex` — and that the run closes by
   printing how to add a second profile, then invoke:

   ```bash
   "$(git rev-parse --show-toplevel)/install.sh" --all
   ```

4. If the user names one pair, invoke:

   ```bash
   "$(git rev-parse --show-toplevel)/install.sh" --pair <claude-root> <codex-root>
   ```

5. Otherwise invoke `install.sh --all`. Show the output and report every
   installed root.
6. Remind the user to start a new Codex session for instruction/skill discovery
   and use `/hooks` once to review and trust new or changed hooks.

Do not edit installed copies by hand. Do not modify authentication, session,
history, or unrelated user configuration files.
