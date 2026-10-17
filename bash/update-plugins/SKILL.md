---
name: update-plugins
description: Check which Claude Code marketplaces and plugin installs (user, project and local scope, across all project folders) are out of date, recommend what to update, and update what the user confirms. Use when the user asks to update plugins, check for plugin updates, or sync plugin versions across repos.
disable-model-invocation: true
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/check-plugins.sh), Bash(${CLAUDE_SKILL_DIR}/scripts/check-plugins.sh:*)
---

# Update plugins

Every plugin install is recorded in `~/.claude/plugins/installed_plugins.json` with its scope and, for local and project scope, its project folder. Each install stays on its own version until it is updated from that folder, so `claude plugin update` in one repo leaves the others behind. The user usually doesn't know what is outdated where. Find out, recommend, and ask before changing anything.

## Prerequisites

- `bash` 3.2 or newer (macOS default is fine; on Windows, Git Bash), `jq`, `git`

## Workflow

1. Run the read-only check:

   ```bash
   ${CLAUDE_SKILL_DIR}/scripts/check-plugins.sh
   ```

   It prints two tab-separated tables:
   - `# marketplaces`: name, last update date, and whether the local clone is `up to date`, `behind remote`, `remote unreachable` or `not a git clone`.
   - `# installs`: status, scope, plugin, installed version, latest version in the local clone, project folder. Statuses: `outdated`, `current`, `dir missing`, `latest unknown`, `not in marketplace`, `ahead of clone`.

2. Report, most useful first:
   - **Marketplaces behind remote.** "Latest" comes from the local clone, so recommend refreshing these first; it may reveal more updates.
   - **Outdated installs**, grouped by scope (user, then local, then project), and within a scope by plugin with version jump and folder count. Name the folders only when there are few.
   - **Stale records** (`dir missing`) and `not in marketplace` (plugin removed or renamed upstream), as one short line each. These can't be updated.
   - Skip `current` entirely.

3. Ask what to do with numbered options, e.g. refresh marketplaces, update everything outdated, only user scope, only one plugin. Recommend one. Do nothing until the user answers.

4. Do what the user picked:
   - Refresh marketplaces: `claude plugin marketplace update <name>` for each chosen one. There is a single clone per marketplace whatever scope declared it, so this changes the catalog for every project. Then rerun the check and report newly outdated installs before updating anything.
   - Update installs: pipe the chosen rows from the check into the update script, selecting with `awk` on status, scope, plugin or project:

     ```bash
     ${CLAUDE_SKILL_DIR}/scripts/check-plugins.sh \
       | awk -F'\t' '$1 == "outdated" && $2 == "user"' \
       | ${CLAUDE_SKILL_DIR}/scripts/update-plugins.sh
     ```

5. Report the result. Running sessions in updated folders need a restart to load the new versions.

## Failures

A `FAILED` update usually means the plugin needs a marketplace-declared command confirmed, which requires a TTY. Don't retry with `-y`: that would accept a command nobody reviewed. Tell the user to run it themselves: `! cd <dir> && claude plugin update <plugin> --scope <scope>`.
