---
name: pa-maintenance
description: "Unified workspace maintenance skill. Covers: (1) backing up the workspace to GitHub git repo, and (2) updating OpenClaw and skills. Use when: asked to backup, push to git, update openclaw, update skills, or run maintenance."
---

# Maintenance Skill

## Minimum Model
Any model. Both sections are scripted operations.

## Trigger Phrases
- "backup workspace" / "push to git" / "save to github"
- "update openclaw" / "update skills" / "run maintenance"
- Runs automatically on schedule (see Cron section)

---

## Section 1 — Workspace Backup

Back up the entire workspace to GitHub on a regular schedule or on demand.

### When to Run
- After significant MEMORY.md changes
- After editing or creating skills
- After completing a major task
- On cron schedule: every 6 hours silently

### Step 1 — Find the GitHub Token

Priority order:
1. **Git remote URL** — check if token is embedded:
   ```bash
   git -C /path/to/openclaw/workspace remote get-url origin
   ```
2. **Environment variable:**
   ```bash
   echo $GITHUB_TOKEN
   echo $GH_TOKEN
   ```
3. **Credentials file:**
   ```bash
   cat ~/.credentials/github-token.txt 2>/dev/null
   cat ~/.credentials/github-pat.txt 2>/dev/null
   ```

If no token found → report BLOCKED to owner.

### Step 2 — Commit and Push

```bash
cd /path/to/openclaw/workspace

# Stage all changes
git add -A

# Commit with timestamp
TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M UTC")
git commit -m "Auto-backup: $TIMESTAMP" 2>/dev/null || echo "Nothing to commit"

# Push
git push origin main
```

### Step 3 — Report (On-Demand Only)

If triggered manually (not by cron):
```
✅ Workspace backed up to GitHub — [timestamp]
[X] files changed
```

If triggered by cron → silent (no message to owner).

### Cron Schedule

```bash
openclaw cron add \
  --name "workspace-backup" \
  --every 6h \
  --session isolated \
  --message "Run the maintenance skill, Section 1 (Workspace Backup). cd /path/to/openclaw/workspace && git add -A && git commit -m 'Auto-backup: $(date -u +\"%Y-%m-%d %H:%M UTC\")' && git push origin main. Silent — do not message owner unless push fails." \
  --timeout-seconds 60
```

### Troubleshooting

| Issue | Fix |
|---|---|
| `git push` auth error | Token expired — update in remote URL or credentials file |
| `nothing to commit` | Normal — workspace unchanged since last backup |
| `rejected (non-fast-forward)` | Run `git pull --rebase origin main` first, then push |
| No token found | Ask owner for a GitHub PAT with `repo` scope |

---

## Section 2 — OpenClaw Updates

Keep OpenClaw and installed skills up to date.

### When to Run
- Weekly on Sunday at 03:00 UTC (cron)
- When owner says "update openclaw" or "update skills"
- After a new OpenClaw version is released

### Step 1 — Update OpenClaw

```bash
# Update the OpenClaw platform
openclaw update

# Check the new version
openclaw --version
```

### Step 2 — Update Skills via ClawHub

```bash
# Update all installed skills to latest
clawhub update

# Or update a specific skill
# clawhub update <skill-name>
```

### Step 3 — Report What Changed

After updates, report to owner:
```
🔄 Maintenance complete (Sunday update):

OpenClaw: v1.2.3 → v1.2.4
  - [changelog item if available]

Skills updated:
  - skill-master: v1.1 → v1.2
  - whatsapp: v2.0 → v2.1
  - [others]

No action needed. Everything is up to date.
```

If nothing changed:
```
✅ No updates available — everything is current.
```

### Step 4 — Verify After Update

```bash
# Check gateway is still running
openclaw gateway status

# Check agent is responding (send a test message or check logs)
openclaw logs --last 10
```

If gateway is down after update → run `openclaw gateway restart`.

### Cron Schedule

```bash
openclaw cron add \
  --name "weekly-update" \
  --cron "0 3 * * 0" \
  --session isolated \
  --message "Run maintenance skill Section 2 (OpenClaw Updates): run 'openclaw update' and 'clawhub update', then report what changed to owner via WhatsApp." \
  --to "OWNER_PHONE" \
  --channel whatsapp \
  --timeout-seconds 300
```

### Troubleshooting

| Issue | Fix |
|---|---|
| `openclaw update` fails | Check internet connectivity; retry in 30 min |
| `clawhub update` not found | Install: `npm install -g clawhub` |
| Gateway down after update | Run `openclaw gateway restart` |
| Skills missing after update | Re-install: `clawhub install <skill-name>` |

---

---

## Section 3 — Session Store Cleanup

Prevent `sessions.json` from bloating (observed growing to 67MB+ with 600+ stale cron run entries).

### When to Run
- Weekly (Sunday maintenance window)
- If agent response time degrades noticeably
- Whenever `sessions.json` exceeds 10MB

### Step 1 — Check Size

```bash
ls -lh /path/to/openclaw/agents/main/sessions/sessions.json
```

If under 10MB → skip cleanup.

### Step 2 — Clean Stale Cron Run Entries

```bash
cd /path/to/openclaw/agents/main/sessions

# Backup first
cp sessions.json sessions.json.bak.$(date +%Y%m%d-%H%M%S)

# Remove all :run: entries (completed cron run histories)
python3 -c "
import json
with open('sessions.json') as f:
    d = json.load(f)
before = len(d)
cleaned = {k:v for k,v in d.items() if ':run:' not in k}
after = len(cleaned)
with open('sessions.json', 'w') as f:
    json.dump(cleaned, f)
print(f'Removed {before-after} entries. {after} remaining.')
"
```

### Step 3 — Restart Gateway

```bash
openclaw gateway restart
```

### Step 4 — Report

```
🧹 Session cleanup: [X]MB → [Y]MB, removed [N] stale cron run entries.
```

---

## Section 4 — Sync Skills to pa-skills Repo

Sync all local skills to `netanel-abergel/pa-skills` (public repo for PA network).

### When to Run
- After updating any skill
- On demand: "סנכרני סקילים" / "sync pa-skills"

### How to Run
```bash
bash /path/to/workspace/skills/pa-maintenance/sync-pa-skills.sh
```

### Privacy Filter (MANDATORY)
The script in `sync-pa-skills.sh` automatically skips:
- `.context` files (personal agent context)
- `data/` directories (pa-directory.json, personal data)
- `context.md`, `.env`, `credentials`, `secrets`

**NEVER manually upload these to pa-skills.**

---

## Cost Tips

- **Both sections:** Very cheap — scripted operations, no LLM tokens for the actual backup/update.
- **Cron:** Both jobs run in isolated sessions. Backup is silent; updates report only if something changed.
- **Don't over-backup:** Every 6h is enough. More frequent = wasted compute and noisy git history.
- **sessions.json bloat** is a known issue — cron runs accumulate unbounded. Weekly cleanup keeps response time fast.
