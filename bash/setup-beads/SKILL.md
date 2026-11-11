---
name: setup-beads
description: Initialize Beads and activate its tracker guidance in a scaffold-agent-project repository. Use after scaffolding a project without a tracker, or to initialize a project already scaffolded for Beads.
---

# Set up Beads

Requires the `scaffold-agent-project` layout. Upgrade its tracker-free guidance to Beads, or preserve guidance already configured for Beads. Do not overwrite unrelated project instructions.

## Run

Preview before applying:

```bash
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py --target <project-root> --dry-run
python3 ~/.agents/skills/setup-beads/scripts/setup_beads.py --target <project-root>
```

The default is local-only Beads (`--stealth`). Use `--mode shared` only with explicit authorization for repository-managed Beads storage; initialization may create a Git commit.

## Boundaries

- The script requires the scaffold's standard tracker instructions. Stop and report deviations instead of guessing replacements.
- Initialize with `--skip-agents --skip-hooks`; never install Beads-managed instructions or hooks.
- Replace the tracker-free statements in `AGENTS.md` and `application-delivery`, rather than appending contradictory policy.
- Create `docs/agents/issue-tracker.md` as the tracker command contract. Do not alter application-specific design, tests, or delivery authority.
- Do not commit, push, or synchronize tracker data unless separately authorized.

After a successful run, confirm `bd prime` works and the tracker instructions agree. Existing `.beads/` state is preserved; this skill does not convert its storage mode.
