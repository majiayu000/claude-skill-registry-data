---
name: weekly-update
description: See what is outdated in your setup every week, and update only what you approve - weekly check for updates of everything installed in the AI-agent setup (agent CLI, skills, plugins, MCP servers, RTK) and a short report. Read-only by default; applies nothing without the user's OK. Use when the scheduled weekly task fires, or when the user asks "check for updates", "is anything outdated", "update my skills/plugins".
author: sant1jmnz
tags:
  - maintenance
  - updates
  - security
---

# Weekly update check

Goal: keep the setup current **without surprises**. Third-party skills, plugins and MCP servers are code/instructions written by other people: updating them is a supply-chain decision, so this skill **reports first and changes nothing until the user says yes**.

## Steps

1. **Run the checker** (read-only, a few seconds, no model tokens spent reading files):

   ```bash
   python -I <this-skill-folder>/check-updates.py
   ```

   It reports: agent CLI version, skills whose source repo has newer commits, plugins whose marketplace has newer commits, version-pinned MCP packages with newer releases, and RTK.
   `UPDATE` = a newer version exists. `UPDATE?` = the repo has newer commits since you installed (they may not touch your skills). `ok` / `skip` need no action.

2. **Triage.** For each `UPDATE`/`UPDATE?`, in one line: what, current → latest, and a risk note (pinned MCP major bump = review; skills from an unknown author = read the diff). Don't dump the raw output at the user.

3. **Write the report** to `tracking/updates/YYYY-MM-DD.md` if the user has a tracking folder, else `./updates/YYYY-MM-DD.md`. Keep it under 30 lines: summary first, then the list, then "what I'd update now / what I'd wait on".

4. **Ask once**, with the recommendation first: "Update X, Y, Z now? (I'd hold W because ...)". Wait for an explicit yes.

5. **Apply only what was approved**, then verify:
   - Skills: `npx skills update <names> -g -y`
   - Plugins (Claude Code): `/plugin marketplace update <marketplace>` then `/plugin update <plugin>@<marketplace>` (UI commands: give them to the person if you can't run them)
   - MCP pinned versions: bump the `@x.y.z` in the MCP's args (`claude mcp remove <name>` + `claude mcp add ...` with the new version), then `claude mcp list`
   - RTK: reinstall from its GitHub release; verify with `rtk gain`
   - Agent CLI: follow the agent's own update command
   After applying, tell the person to **restart the agent**.

## Rules
- Never auto-update. Never run `npx skills update` with no names unless the user approved "everything".
- Never use a model bigger than needed: this is a cheap, mostly mechanical job (see the cost rules in the global instructions).
- Don't include secrets or personal data in the report.
- If GitHub is unreachable (offline, rate-limited), say so and retry next week; don't guess.
- Apply the `anti-slop` rule to the report: concrete versions and dates, no filler.
