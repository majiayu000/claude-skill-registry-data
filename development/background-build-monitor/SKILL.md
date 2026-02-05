---
name: Background Build Monitor
description: Use this skill when applying home-manager or darwin configurations that require long-running builds. Automatically runs builds in background, monitors progress with appropriate polling intervals, and reports status updates without overwhelming the user. Triggered by "apply changes", "rebuild", "make home", or "switch configuration".
allowed-tools:
  - Bash
  - BashOutput
---

# Background Build Monitor

Expert agent for managing long-running Nix builds with efficient background monitoring.

## Instructions

Your goal is to run builds in background and provide concise progress updates without excessive polling.

### Workflow

1. **Determine Build Type**
   - Home-manager: `make home` (5-10 minutes, background required)
   - Darwin: `make darwin` (2-5 minutes, can run foreground)
   - Update: `make update` (variable time, background required)

2. **Pre-flight Check**
   - Verify working directory: `/Users/shavakan/nix-flakes`
   - Note current git status if relevant
   - For home-manager/darwin: confirm build test passed first

3. **Start Build in Background**
   ```bash
   # Home-manager
   make home  # run_in_background: true

   # Darwin
   make darwin  # can run foreground or background

   # Update
   make update  # run_in_background: true
   ```

4. **Monitor Progress**

   **Polling strategy:**
   - Initial check: 15 seconds after start
   - Subsequent checks: every 15 seconds
   - Report to user: every 30-45 seconds (combine 2-3 polls)

   **What to look for:**
   - Build progress: "building...", "copying...", "downloading..."
   - Activation: "setting up...", "activating..."
   - Errors: parse and report immediately
   - Completion: "done", exit code

   **Don't report:**
   - Every single line of output
   - Repetitive "building" messages
   - Nix hash computations
   - Individual package builds unless user asks

5. **Progress Reporting**

   **Every 30-45 seconds, concise updates:**
   ```
   [2m] Building... (42 packages)
   [4m] Building... (ongoing)
   [7m] Activating configuration...
   [8m] Complete ✓
   ```

   **NOT this:**
   ```
   Checking output...
   Still building...
   No new output...
   Checking again...
   (repeating every 15s)
   ```

6. **Completion**

   **On success:**
   ```
   ✓ Configuration applied successfully
   Total time: [duration]

   [If services affected]:
   Check status:
   - rclone: rclone-mount-status
   - logs: ~/nix-flakes/logs/
   ```

   **On failure:**
   ```
   ✗ Build failed at [stage]
   Error: [concise explanation]

   [relevant error lines from output]

   Check logs: ~/nix-flakes/logs/[service].log
   ```

### Monitoring Pattern

```
Start build in background
↓
Wait 15s
↓
Check output (BashOutput)
↓
Parse state: building | activating | error | complete
↓
If not complete:
  - Wait 15s
  - Check again
  - If 2-3 polls elapsed → report to user
↓
If complete:
  - Report final status
  - Suggest next steps if needed
```

### Error Handling

**Build phase errors:**
- Usually Nix evaluation or compilation errors
- Extract relevant error message
- Identify file/module if possible
- Don't proceed to activation

**Activation phase errors:**
- Occur after successful build
- Often service-related
- Check `~/nix-flakes/logs/` for details
- Common: rclone hash mismatch, service conflicts

**Timeout (>15 minutes for home-manager):**
- Check if process is hung
- Look for network issues (downloads stuck)
- Suggest manual intervention

**Silent builds:**
- Some builds produce no output for minutes
- This is normal for large packages
- Don't report "no output" as a problem
- Just note "Building... (in progress)"

### Special Cases

**First-time builds:**
- May take longer (no cache)
- Warn user this is expected

**Service restarts:**
- Some services restart during activation
- Brief interruptions normal

**Hash file updates:**
- rclone activation creates hash files
- May see "hash changed, recreating"

**Multiple builds:**
- If user wants both home-manager and darwin
- Run sequentially, not parallel
- Home-manager first, then darwin

### Output Discipline

**Do report:**
- Major phase transitions (build → activate → complete)
- Errors immediately
- Time elapsed at reasonable intervals
- Final status

**Don't report:**
- Every BashOutput check
- Individual package builds (unless slow)
- Repetitive "still building" messages
- Technical Nix internals unless error

**Timing:**
- Check every 15s (tool call)
- Report every 30-45s (user message)
- Keep user informed without spam

### Constraints

- **ALWAYS** run `make home` and `make update` in background
- **ALWAYS** wait minimum 15 seconds between BashOutput checks
- **NEVER** poll more frequently than 15s
- **NEVER** report every individual check to user
- **AGGREGATE** updates into meaningful progress reports
- **PARSE** output for actual state changes before reporting

## Examples

**Typical home-manager run:**
```
Starting home-manager rebuild in background...
[15s] Building...
[45s] Building... (ongoing, 128 packages)
[2m] Activating configuration...
[2m15s] ✓ Complete

Total time: 2m 15s
```

**Build with error:**
```
Starting home-manager rebuild in background...
[15s] Building...
[1m] ✗ Build failed

Error in modules/vscode/extensions.nix:42
Attribute 'publisher.extension' not found

[relevant error context]
```

**Update flake:**
```
Updating flake inputs in background...
[15s] Updating...
[45s] Updated: nixpkgs, home-manager, darwin
[1m] ✓ Complete

Run `make home` to apply updates
```
