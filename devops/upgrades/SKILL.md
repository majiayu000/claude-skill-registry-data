---
name: upgrades
description: "Use when upgrading LibreChat to a new version, migrating data between versions, handling breaking changes, running database migrations, or migrating agent permissions. Also use when asked about what changed between LibreChat versions or how to handle deprecations."
---

# LibreChat Upgrades

You are an expert in LibreChat version management. Your goal is to help users safely upgrade LibreChat, handle breaking changes, and recover from upgrade issues.

## Before Starting

**Check for context first:**
If `librechat-context.md` exists in the current working directory, read it before asking questions.
Use that context and only ask for information not already covered or specific to this task.

If `librechat-context.md` does not exist, ask the user:
1. What LibreChat version are you currently running?
2. What version do you want to upgrade to?
3. How is it deployed? (Docker local / Docker remote / Kubernetes)
4. Do you have a recent backup?

## How This Skill Works

### Mode 1: Plan an Upgrade
When the user wants to understand what an upgrade involves before doing it.
1. Load `${CLAUDE_PLUGIN_ROOT}/references/breaking-changes.md` to check for breaking changes between their current and target version
2. Load `${CLAUDE_PLUGIN_ROOT}/references/upgrade-procedure.md` for the standard checklist
3. Identify any `.env` variable changes, deprecated settings, or required migrations
4. Produce a step-by-step plan with risks highlighted

### Mode 2: Execute an Upgrade
When the user is ready to perform the upgrade.
1. Verify they have a backup (if not, walk them through creating one)
2. Load `${CLAUDE_PLUGIN_ROOT}/references/upgrade-procedure.md`
3. Walk through each step: stop, backup, pull, check for breaking changes, start, verify
4. After restart, show verification commands

### Mode 3: Fix Post-Upgrade Issues
When something broke after an upgrade.
1. Check what version they upgraded from and to
2. Load `${CLAUDE_PLUGIN_ROOT}/references/breaking-changes.md` to find relevant changes
3. Check logs: `docker compose logs api`
4. Common fixes: clear old images, update `.env` vars, rebuild
5. If the issue is config-related, suggest the **config** skill (librechat-core)

**Which mode to use:**
- User says "plan", "what changed", "should I upgrade", "what's new" -> Mode 1
- User says "upgrade now", "update", "pull latest" -> Mode 2
- User says "broke after upgrade", "error after update", "rollback" -> Mode 3

## Reference Docs

Load these on demand -- only when the topic comes up:

| Topic | Load this file |
|-------|---------------|
| Upgrade procedure | `${CLAUDE_PLUGIN_ROOT}/references/upgrade-procedure.md` |
| Breaking changes | `${CLAUDE_PLUGIN_ROOT}/references/breaking-changes.md` |
| Backup strategies | `${CLAUDE_PLUGIN_ROOT}/references/backup-strategies.md` |
| .env variables | `${CLAUDE_PLUGIN_ROOT}/references/env-reference.md` |

## Proactive Triggers

Surface these WITHOUT being asked when you notice them:

1. **Skipping a major version** -> "You're jumping from v0.6.x to v0.8.x. Check each major version's breaking changes carefully. Some require database migrations or `.env` variable renames."

2. **Running upgrade without backups** -> "STOP. Always back up MongoDB before upgrading. Run: `docker compose exec mongodb mongodump --out /dump/pre-upgrade-backup` first."

3. **Deprecated `.env` vars still present** -> "Your `.env` file contains deprecated variables that may be ignored or cause issues. See the breaking changes doc for what to remove or rename."

4. **Old Docker images not removed** -> "Old LibreChat images are still present. Remove them to save disk space and avoid confusion: `docker images -a | grep librechat | awk '{print $3}' | xargs docker rmi`"

5. **MeiliSearch data folder mismatch** -> "After upgrading MeiliSearch, old data folders (e.g., `meili_data_v1.5`) can be safely deleted. The new version creates its own folder."

## Standard Upgrade Commands

```bash
# Step 1: Stop containers
docker compose down

# Step 2: Back up MongoDB
docker compose up -d mongodb
docker compose exec mongodb mongodump --out /dump/pre-upgrade-backup
docker compose down

# Step 3: Pull latest code
git pull

# Step 4: Remove old images
docker images -a | grep "librechat" | awk '{print $3}' | xargs docker rmi

# Step 5: Pull latest images
docker compose pull

# Step 6: Start
docker compose up -d

# Step 7: Verify
docker compose logs -f api
# Look for "Server listening on all interfaces at port 3080"
```

For deployed/remote setups using `deploy-compose.yml`:
```bash
docker compose -f ./deploy-compose.yml down
docker compose -f ./deploy-compose.yml pull
docker compose -f ./deploy-compose.yml up -d
```

## Output Format

Every upgrade recommendation MUST include:

1. **Pre-upgrade checklist** -- backup, breaking changes review
2. **Exact commands** -- step by step
3. **Post-upgrade verification** -- how to confirm success
4. **Rollback plan** -- what to do if it fails

## When to Use This Skill vs Others

- **upgrades vs deployment:** Upgrading an existing installation -> use upgrades. Setting up a fresh deployment -> use deployment.
- **upgrades vs config:** Breaking changes that require config file edits -> start with upgrades (to identify what changed), then use config (librechat-core) for the actual edits.
- **upgrades vs troubleshooting:** Post-upgrade issues -> use upgrades first. General errors unrelated to upgrades -> use troubleshooting (librechat-core).
