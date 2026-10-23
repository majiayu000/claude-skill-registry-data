---
name: self-upgrade
description: Upgrade cadet to the latest version, restart the assistant, and restart the gateway
compatibility: "Designed for Cadet personal assistants"
metadata:
  emoji: "⬆️"
  cadet:
    category: "system"
    display-name: "Self Upgrade"
---

You are performing a self-upgrade of the Cadet assistant. Follow these steps **in order**. Use the `bash` tool to run each command. Confirm each step succeeds before moving to the next.

## Step 1: Record the current version

```bash
cadet --version
```

Save this value to report later.

## Step 2: Install the latest cadet

```bash
bun install -g mycadet@latest
```

After updating, verify the new version:

```bash
cadet --version
```

## Step 3: Restart the gateway

If a gateway process is running, restart it so it picks up any protocol or dependency changes from the new version:

```bash
pgrep -f 'cadet-gateway|gateway/src/index.ts' || echo "No gateway process found"
```

If a gateway PID is found, send it SIGTERM so it drains gracefully:

```bash
pkill -TERM -f 'cadet-gateway|gateway/src/index.ts'
```

Then start the gateway again using whatever method the user's deployment uses (e.g. `bun run gateway/src/index.ts`, a systemd service, or a container orchestrator). If you are unsure how the gateway is deployed, ask the user.

## Step 4: Restart the assistant

Use `cadet sleep` to stop the running assistant and gateway, then `cadet wake` to start them again from the updated binary:

```bash
cadet sleep && cadet wake
```

Verify it is running:

```bash
cadet ps
```

**Important:** This is the last step because the current assistant process is the one executing this conversation. After the restart, the new assistant takes over and this conversation ends gracefully.

## After Upgrade

Report back to the user with:

- The previous and new cadet version
- Assistant status (running, PID)
- Gateway status (restarted or not found)
- Any errors encountered during the process
