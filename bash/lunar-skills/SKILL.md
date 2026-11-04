---
name: lunar-skills
description: Use Lunar Skills MCPorter CLI to discover and read Lunar backend engineering practices and their references.
---

# Lunar Skills

Run the generated `lunar-skills` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/lunar-skills/scripts/run.mjs" lunar-skills-list --help
node "$PI_CODING_AGENT_DIR/skills/lunar-skills/scripts/run.mjs" lunar-skills-search --help
node "$PI_CODING_AGENT_DIR/skills/lunar-skills/scripts/run.mjs" lunar-skills-read --help
```

Search or list to identify the relevant engineering practice, then read that skill before changing affected work code.
Read a referenced document only when the selected practice points to it and the current task needs the detail.
Treat loaded practices as work-repository guidance and report any conflict with repository-local instructions.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- lunar-skills`, then run `nix run .#sync-agents`.
