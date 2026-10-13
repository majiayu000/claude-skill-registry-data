---
name: local-automation
description: "Creates persistent, recurring local automations on macOS using launchd. Interviews for requirements, creates wrapper scripts and plists, loads the job, tests it, and updates the project context map."
user_invocable: true
---

# /local-automation — Create a Local Recurring Automation

Creates a persistent macOS launchd job that runs on a schedule, survives reboots, and logs output.

## Phase 1: Interview

Ask these questions **one at a time**, waiting for the user's response before proceeding:

1. **What should this automation do?** (plain English description)
2. **Does a script already exist, or do we need to create one?** If it exists, ask for the path.
3. **What schedule?** Offer common patterns:
   - Daily at a specific time (e.g., "7 AM")
   - Every N hours (e.g., "every 2 hours")
   - Weekdays only at a specific time
   - Custom (let them describe it)
4. **Does it need secrets from Vault?** If yes, which labels? (These get loaded via `get-secret.sh`)
5. **Does it need to access `$OUTWORKOS_PARENT`?** (If yes, warn about Full Disk Access requirement for `/bin/bash`)
6. **What should it be named?** Suggest a kebab-case name based on the description (e.g., `inbox-pulse`, `daily-backup`). The name determines:
   - Plist: `~/Library/LaunchAgents/com.outworkos.{name}.plist`
   - Script: `~/.local/bin/outworkos-{name}.sh`
   - Log: `/tmp/outworkos-{name}.log`
   - Label: `com.outworkos.{name}`

After all questions are answered, summarize the plan and ask for confirmation before proceeding.

## Phase 2: Analyze

Before creating anything, check for conflicts:

```bash
# Check if plist already exists
ls ~/Library/LaunchAgents/com.outworkos.{name}.plist 2>/dev/null

# Check if wrapper script already exists
ls ~/.local/bin/outworkos-{name}.sh 2>/dev/null

# Check if label is already loaded
launchctl list | grep com.outworkos.{name}
```

If any exist, ask the user whether to overwrite or choose a different name.

Review the source script (if existing) for:
- Dependencies (Python packages, CLI tools)
- Environment variable requirements
- File path assumptions (especially hardcoded paths)
- Whether it needs modification to work under launchd's minimal environment

Present findings and proposed changes before proceeding.

## Phase 3: Develop

### Step 1: Create the wrapper script

Write `~/.local/bin/outworkos-{name}.sh`:

```bash
#!/bin/bash
# outworkos-{name}.sh — {description}
# Managed by /local-automation. Do not edit directly.
set -euo pipefail

# --- Vault secrets (if needed) ---
GET_SECRET="${OUTWORKOS_ROOT}/scripts/get-secret.sh"
# export SECRET_NAME=$("$GET_SECRET" secret_label)

# --- Run the automation ---
# Either inline logic or call the source script
```

Key rules for the wrapper:
- Always use `set -euo pipefail`
- Load secrets via `$GET_SECRET` if needed
- Use absolute paths everywhere (launchd has no working directory context)
- Keep it minimal — delegate to the actual script/command

```bash
chmod +x ~/.local/bin/outworkos-{name}.sh
```

### Step 2: Create the launchd plist

Write `~/Library/LaunchAgents/com.outworkos.{name}.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.outworkos.{name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/.local/bin/outworkos-{name}.sh</string>
    </array>
    <!-- SCHEDULE: use ONE of the following patterns -->
    <!-- Daily at specific time: -->
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>{hour}</integer>
        <key>Minute</key>
        <integer>{minute}</integer>
    </dict>
    <!-- Every N seconds: -->
    <!-- <key>StartInterval</key> -->
    <!-- <integer>{seconds}</integer> -->
    <!-- Weekdays at specific time: -->
    <!-- <key>StartCalendarInterval</key> -->
    <!-- <array> -->
    <!--   <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>{h}</integer><key>Minute</key><integer>{m}</integer></dict> -->
    <!--   ... repeat for days 2-5 ... -->
    <!-- </array> -->
    <key>StandardOutPath</key>
    <string>/tmp/outworkos-{name}.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/outworkos-{name}.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
        <key>HOME</key>
        <string>{USER_HOME}</string>
    </dict>
</dict>
</plist>
```

Schedule mapping:
- "Daily at 7 AM" → `StartCalendarInterval` with `Hour=7, Minute=0`
- "Every 2 hours" → `StartInterval` with `7200`
- "Weekdays at 9 AM" → `StartCalendarInterval` array with `Weekday` 1-5
- "Every 30 minutes" → `StartInterval` with `1800`

Only include ONE scheduling key. Remove the commented-out alternatives from the final plist.

### Step 3: Load and test

```bash
# Load the job
launchctl load ~/Library/LaunchAgents/com.outworkos.{name}.plist

# Verify it's loaded (exit code 0 = loaded, status "-" = not yet run)
launchctl list | grep com.outworkos.{name}

# Run it once now to test
launchctl start com.outworkos.{name}

# Wait a few seconds, then check the log
sleep 3
cat /tmp/outworkos-{name}.log
```

If the test fails:
- Check the log for errors
- Common issues: missing PATH entries, Full Disk Access, missing deps
- Fix the wrapper script and re-test (no need to reload the plist for script changes)
- If plist changes are needed: `launchctl unload` then `launchctl load` again

### Step 4: Update context map

Find the project's `context-map.md` and add the automation under an `## Automations` section (create the section if it doesn't exist):

```markdown
## Automations

| Name | Schedule | Script | Plist | Log | Description |
|------|----------|--------|-------|-----|-------------|
| {name} | {human-readable schedule} | `~/.local/bin/outworkos-{name}.sh` | `~/Library/LaunchAgents/com.outworkos.{name}.plist` | `/tmp/outworkos-{name}.log` | {description} |
```

If the automation belongs to a specific project (not OutworkOS itself), update that project's context map instead.

## Conventions

- All labels use `com.outworkos.` prefix
- All wrapper scripts live at `~/.local/bin/outworkos-{name}.sh`
- All plists live at `~/Library/LaunchAgents/com.outworkos.{name}.plist`
- All logs go to `/tmp/outworkos-{name}.log`
- Secrets are always loaded via `$OUTWORKOS_ROOT/scripts/get-secret.sh`, never hardcoded
- Wrapper scripts must use absolute paths and never assume a working directory

## Troubleshooting Reference

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Operation not permitted` in log | Full Disk Access not granted to `/bin/bash` | System Settings > Privacy & Security > Full Disk Access > add `/bin/bash` |
| Exit code non-zero in `launchctl list` | Script is crashing | Check `/tmp/outworkos-{name}.log` for errors |
| Job doesn't appear in `launchctl list` | Plist not loaded | `launchctl load ~/Library/LaunchAgents/com.outworkos.{name}.plist` |
| Job runs but script not found | Wrong path in plist | Verify `ProgramArguments` path matches actual script location |
| Secrets fail to load | Keychain locked or missing `service_role_key` | Run `security unlock-keychain` or check Keychain Access |
| Python import errors | Deps not installed for system Python | `python3 -m pip install {package}` |
