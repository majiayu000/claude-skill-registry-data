---
name: Fixing tmux Socket Issues
description: This skill repairs tmux socket connection errors when the socket directory is deleted while tmux is running. Use this when you see "error connecting to /private/tmp/tmux-UID/default (No such file or directory)" while tmux sessions are still active.
allowed-tools: [Bash, Read]
---

# Fixing tmux Socket Issues

Repair tmux socket connection errors without killing your running sessions.

## What This Skill Does

- Diagnoses tmux socket connection failures
- Recreates missing socket directories
- Signals tmux server to recreate socket files
- Verifies manual save/restore functionality
- Preserves all running sessions and processes

## When to Use This Skill

**Symptoms:**
- Error: `error connecting to /private/tmp/tmux-UID/default (No such file or directory)`
- `tmux list-sessions` fails but you're inside a working tmux session
- `$TMUX` environment variable is set but socket file doesn't exist
- tmux-resurrect manual save fails but automatic saves may appear to work

**Common causes:**
- System `/tmp` directory cleanup
- System updates or reboots
- Manual deletion of temp directories

## How tmux Sockets Work

tmux uses a **UNIX domain socket** for client-server communication. The socket path format is:

```
/private/tmp/tmux-UID/default
```

Where `UID` is your user ID (e.g., `504`).

**Why sessions survive socket deletion:**
- The tmux server process keeps the socket open as a file descriptor
- Existing connections continue to work
- New connections fail because the filesystem path is gone
- The server is alive but unreachable by new clients

## Prerequisites

1. **Active tmux session** - You must be inside a running tmux session
2. **Shell access** - Ability to run commands (inside or outside tmux)
3. **Permissions** - Ability to create directories in `/private/tmp` or `/tmp`

## Diagnosis Steps

### Step 1: Verify the Problem

Check if you're in tmux but the socket is missing:

```bash
# Check if TMUX is set (confirms you're in a session)
echo $TMUX
# Example output: /private/tmp/tmux-504/default,1632,1

# Try to list sessions (will fail if socket is missing)
tmux list-sessions
# Expected error: error connecting to /private/tmp/tmux-504/default (No such file or directory)

# Verify socket directory doesn't exist
ls -la /private/tmp/tmux-*/
# Expected error: No such file or directory
```

If all three conditions are true (TMUX set, list-sessions fails, directory missing), proceed with the fix.

### Step 2: Check Last Successful Save

Verify when tmux-resurrect last successfully saved:

```bash
ls -lh ~/.tmux/resurrect/last
stat ~/.tmux/resurrect/last
```

Note the timestamp. If it's old (before the socket disappeared), automatic saves are likely also failing.

## Repair Steps

### Step 1: Recreate Socket Directory

Extract the socket directory path from `$TMUX`:

```bash
# Show full TMUX path
echo $TMUX
# Example: /private/tmp/tmux-504/default,1632,1

# The directory is everything before '/default'
# For example: /private/tmp/tmux-504
```

Create the directory with correct permissions:

```bash
# Replace '504' with your actual UID from $TMUX
mkdir -p /private/tmp/tmux-504
chmod 700 /private/tmp/tmux-504
```

**Permission requirements:**
- Directory must be owned by your user
- Permissions must be `700` (drwx------) for security

### Step 2: Find tmux Server PID

The tmux server is the oldest tmux process:

```bash
# List all tmux processes
ps aux | grep tmux | grep -v grep
```

Look for the process with:
- Oldest start time
- Command `tmux` (not `tmux attach`)
- Usually the lowest PID

Example output:
```
jonathan  1632  1.1  0.0 435326336  5184  ??  Ss  1Nov25  102:36.11 tmux
jonathan 22779  0.0  0.0 435309312   624 s077 S+  1Nov25    0:00.05 tmux attach -t 3
```

In this example, PID `1632` is the server (started Nov 25, command is just `tmux`).

### Step 3: Signal tmux to Recreate Socket

Send `SIGUSR1` to the tmux server process:

```bash
# Replace 1632 with your actual server PID
kill -SIGUSR1 1632
```

**What this does:**
- Signals the tmux server to recreate its socket file
- Does NOT kill or restart tmux
- Reconnects the running server to the filesystem
- Preserves all sessions, windows, and processes

**Alternative (if you only run one tmux server):**

```bash
pkill -USR1 -x tmux
```

This sends SIGUSR1 to all processes named exactly "tmux".

### Step 4: Verify the Fix

Check that the socket file was recreated:

```bash
# Socket file should now exist
ls -la /private/tmp/tmux-504/
# Expected: drwx------  3 you  wheel   96 Nov 16 09:18 .
#           srw-rw----  1 you  wheel    0 Nov 16 09:18 default

# tmux commands should now work
tmux list-sessions
# Expected: List of your active sessions

# Test resurrect save script
~/.tmux/plugins/tmux-resurrect/scripts/save.sh

# Verify new save was created
ls -lh ~/.tmux/resurrect/last
# Timestamp should be current
```

## Verification Checklist

After applying the fix:

- [ ] Socket directory exists: `ls -la /private/tmp/tmux-UID/`
- [ ] Socket file exists with correct permissions: `srw-rw----`
- [ ] `tmux list-sessions` succeeds
- [ ] `tmux list-keys` succeeds
- [ ] Manual resurrect save works: `~/.tmux/plugins/tmux-resurrect/scripts/save.sh`
- [ ] New save file created with current timestamp
- [ ] All existing sessions still running
- [ ] No processes were killed or restarted

## Troubleshooting

### Issue: "Permission denied" when creating directory

**Cause:** `/private/tmp` or `/tmp` may require elevated permissions

**Solution:**
```bash
sudo mkdir -p /private/tmp/tmux-504
sudo chown $(whoami) /private/tmp/tmux-504
chmod 700 /private/tmp/tmux-504
```

### Issue: Socket not recreated after SIGUSR1

**Symptoms:** Directory exists but socket file still missing after signal

**Causes:**
1. Wrong PID (sent signal to client, not server)
2. Parent directory permissions incorrect
3. Tmux server in unusual state

**Solutions:**

1. Verify you got the right PID:
   ```bash
   # The server process should show just "tmux", not "tmux attach"
   ps aux | grep '[t]mux' | grep -v attach
   ```

2. Check directory permissions:
   ```bash
   ls -ld /private/tmp/tmux-504
   # Should show: drwx------ ... your-username ...
   ```

3. If still failing, check tmux server is responsive:
   ```bash
   # From inside tmux
   tmux refresh-client
   ```

4. Last resort - restart tmux server (will lose session state):
   ```bash
   # Save important work first!
   tmux kill-server
   tmux
   ```

### Issue: Multiple tmux servers running

**Symptoms:** `ps aux | grep tmux` shows multiple "tmux" processes (not "tmux attach")

**Cause:** Multiple independent tmux servers on different sockets

**Solution:**
1. Identify which server you're attached to:
   ```bash
   echo $TMUX
   # Shows socket path and server PID
   ```

2. Send SIGUSR1 only to that specific PID:
   ```bash
   # Don't use pkill, it would signal all servers
   kill -SIGUSR1 <specific_pid>
   ```

### Issue: macOS-specific pgrep syntax error

**Symptoms:** `pgrep: illegal option -- -`

**Cause:** macOS uses BSD `pgrep` which has different options than GNU `pgrep`

**Solution:**
```bash
# BSD (macOS) syntax:
pgrep -o tmux    # oldest process

# Alternative: use ps
ps aux | grep tmux | grep -v grep
```

## tmux-resurrect Keybindings

For reference, the correct keybindings with a custom prefix:

**Default prefix: `Ctrl+b`**
- Save: `Ctrl+b` then `Ctrl+s`
- Restore: `Ctrl+b` then `Ctrl+r`

**Custom prefix: `Ctrl+a`** (as in your config)
- Save: `Ctrl+a` then `Ctrl+s`
- Restore: `Ctrl+a` then `Ctrl+r`

Verify your bindings:
```bash
tmux list-keys | grep resurrect
```

Expected output:
```
bind-key -T prefix C-r run-shell /path/to/restore.sh
bind-key -T prefix C-s run-shell /path/to/save.sh
```

## Prevention

To reduce the likelihood of this issue:

1. **Use XDG_RUNTIME_DIR** (Linux):
   ```bash
   # In .bashrc or .zshrc
   export TMUX_TMPDIR=$XDG_RUNTIME_DIR
   ```
   This directory persists across reboots on systemd systems.

2. **Custom socket location**:
   ```bash
   # Start tmux with custom socket location
   tmux -S ~/.tmux/socket new-session
   ```

3. **System configuration** (requires root):
   - Exclude `/tmp/tmux-*` from automated cleanup scripts
   - Configure `tmpwatch` or similar tools to skip tmux directories

## Best Practices

1. **Respond quickly**: Fix the socket as soon as you notice the error to avoid confusion
2. **Verify timestamps**: Always check that saves are actually happening after the fix
3. **Document your UID**: Note your user ID for faster diagnosis next time
4. **Keep sessions active**: The fix works because sessions are still running; if you kill tmux first, you'll need to restore from last save
5. **Regular saves**: Use `Ctrl+a Ctrl+s` periodically for important session states

## Related Skills

- **configuring-neovim** - For fixing Neovim session restoration with tmux-resurrect
- **working-with-terminals** - For understanding terminal multiplexer fundamentals

## Understanding tmux-continuum Behavior

**Why automatic saves appear to work:**

tmux-continuum runs inside the tmux server process using `run-shell`. In some cases:
- Old save timestamps may persist, making it look like saves are working
- The actual save attempts are failing silently
- Check timestamps carefully to confirm saves are current

**After fixing:**
- Monitor `~/.tmux/resurrect/last` timestamp
- Verify it updates every 15 minutes (or your configured interval)
- First new save confirms the fix worked

## Quick Reference

```bash
# 1. Create directory
mkdir -p /private/tmp/tmux-$(id -u)
chmod 700 /private/tmp/tmux-$(id -u)

# 2. Find server PID
ps aux | grep '[t]mux' | grep -v attach

# 3. Send signal
kill -SIGUSR1 <server_pid>

# 4. Verify
tmux list-sessions
ls -la /private/tmp/tmux-$(id -u)/
```

## Additional Resources

- [tmux man page - SIGUSR1 behavior](https://man7.org/linux/man-pages/man1/tmux.1.html)
- [tmux-resurrect documentation](https://github.com/tmux-plugins/tmux-resurrect)
- [tmux-continuum documentation](https://github.com/tmux-plugins/tmux-continuum)
