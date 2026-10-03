---
name: termux
description: Termux (Android terminal emulator) device management — SSH access, persistent services via termux-services/runit, Termux:Boot autostart, package management, process persistence quirks on Android. Use when working with an Android phone/tablet server, deploying scripts to Termux, starting persistent daemons, or troubleshooting Android process killing. Do NOT use for generic Linux work unrelated to Termux/Android.
---

# Termux Skill

Reference for managing an Android device running Termux as a server.

## Key Facts

- Termux is a **user-space app** — not a real Linux. No systemd. No root required (but this device has Magisk root).
- Package manager: `pkg` or `/data/data/com.termux/files/usr/bin/apt` (full path needed in SSH sessions)
- All binaries live at: `/data/data/com.termux/files/usr/bin/`
- Home dir: `/data/data/com.termux/files/home/` (aka `~`)
- PREFIX: `/data/data/com.termux/files/usr/`
- Python: `/data/data/com.termux/files/usr/bin/python3` (v3.14.6)
- Node.js: `/data/data/com.termux/files/usr/bin/node` (v24.14.1)

## SSH Access (from CachyOS)

```bash
ssh -o ProxyCommand="cloudflared access ssh --hostname term.YOUR-DOMAIN.example" \
    -p 8022 <termux-user>@term.YOUR-DOMAIN.example
# Or via SSH config alias:
ssh s9
```

**IMPORTANT**: SSH sessions on Android/Termux have a **limited PATH** (`/sbin /system/bin` etc — NOT the Termux bin dir). Always use full paths in SSH commands:
```bash
# Wrong (in SSH):  python3 script.py
# Right (in SSH):  /data/data/com.termux/files/usr/bin/python3 script.py
```

## Process Persistence — The Android Problem

Android kills orphaned processes aggressively. `nohup` and `setsid` launched from SSH **DO NOT survive** when the SSH session closes. This is the #1 gotcha.

### What DOES survive:
1. **Processes started from within the Termux app UI** (they're under Termux's process tree)
2. **`termux-services` (runit) services** — the proper solution
3. **Termux:Boot scripts** — run on device boot inside Termux context

### What does NOT survive SSH:
- `nohup python3 script.py &`
- `setsid python3 script.py &`
- Background `&` processes

## Correct Way: termux-services (runit)

The right way to run persistent daemons. Uses runit (same as Void Linux/Artix).

```bash
# Install from within Termux app on the phone:
pkg install termux-services

# Create a service directory:
mkdir -p $PREFIX/var/service/sv/myservice
cat > $PREFIX/var/service/sv/myservice/run << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
exec /data/data/com.termux/files/usr/bin/python3 /path/to/script.py
EOF
chmod +x $PREFIX/var/service/sv/myservice/run

# Start it:
sv up myservice

# Enable auto-start when Termux opens:
sv-enable myservice

# Stop:
sv down myservice

# Status:
sv status myservice
```

Service files live at: `$PREFIX/var/service/sv/` = `/data/data/com.termux/files/usr/var/service/sv/`

## Termux:Boot

Auto-runs scripts when Android boots. Requires Termux:Boot app installed and launched once.

Boot scripts live at: `~/.termux/boot/`

**Correct boot script pattern** (sourcing profile is critical for PATH):
```sh
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
. $PREFIX/etc/profile   # ← sets PATH, env vars
# start termux-services (if using runit):
source /data/data/com.termux/files/usr/etc/profile.d/start-services.sh
```

Or manually start things:
```sh
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
. $PREFIX/etc/profile
sshd
nohup filebrowser ... &
```

**NOTE**: `sleep 15` before network-dependent services is recommended — WiFi takes 10-15s after boot.

## Package Management

```bash
# From within Termux app (not SSH):
pkg update && pkg upgrade
pkg install tmux python nodejs openssh termux-services

# From SSH (full path):
/data/data/com.termux/files/usr/bin/apt install tmux -y
# But this requires Termux user context — may fail with "root disabled" from SSH
```

## Example: persistent Python bot service

Generic pattern for keeping a Python service alive (works for any long-running script):

**Start from the Termux app** (NOT from SSH — SSH children die when session ends):
```bash
cd ~/mybot
nohup python3 mybot.py >> bot.log 2>&1 &
```

**Better — make it a runit service:**
```bash
# Run this FROM the Termux app on the phone:
mkdir -p $PREFIX/var/service/sv/mybot
cat > $PREFIX/var/service/sv/mybot/run << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
cd /data/data/com.termux/files/home/mybot
exec /data/data/com.termux/files/usr/bin/python3 mybot.py
EOF
chmod +x $PREFIX/var/service/sv/mybot/run
sv-enable mybot
sv up mybot
```

## File Locations (Android/Termux)

| What | Path |
|------|------|
| Bot script | `~/kammo_bot/kammo_bot.py` |
| Bot inbox | `~/kammo_bot/inbox.json` |
| Bot outbox | `~/kammo_bot/outbox.json` |
| Boot script | `~/.termux/boot/start-nas.sh` |
| runit services | `$PREFIX/var/service/sv/` |
| SSH authorized_keys | `~/.ssh/authorized_keys` |
| cloudflared binary | `/data/local/tmp/cloudflared` |
| Cloudflare wrapper | `/data/local/tmp/run-cloudflared.sh` |

## Common Gotchas

1. **PATH in SSH is wrong** — always use full `/data/data/com.termux/files/usr/bin/` paths
2. **Processes die after SSH** — use runit (termux-services) or start from Termux app
3. **`pkg` not found in SSH** — it's at `/data/data/com.termux/files/usr/bin/apt`
4. **`ps aux` doesn't work** — Android `ps` is different, just use `ps | grep name`
5. **SELinux enforcing** — root can't access Termux app_data_file context paths. Use `su u0_a123 -c` when needed.
6. **WiFi-only device** — no SIM. All network access via WiFi. DNS might hiccup on cloudflared v2026.7.1+ (use v2026.3.0).
7. **Boot persistence** — Termux:Boot fires BOOT_COMPLETED but WiFi takes ~15s. Add `sleep 15` before network services.
8. **Python is at `python3`** not `python` in newer Termux builds.

## Useful One-Liners (from CachyOS over SSH)

```bash
# Check what's running:
ssh s9 "ps | grep -E 'python|cloudflared|navidrome|filebrowser'"

# Tail bot log:
ssh s9 "tail -f ~/kammo_bot/bot.log"

# Restart bot (only works if started from Termux app context previously):
ssh s9 "pkill -f kammo_bot && nohup /data/data/com.termux/files/usr/bin/python3 ~/kammo_bot/kammo_bot.py >> ~/kammo_bot/bot.log 2>&1 &"

# Quick file transfer to the device:
scp -P 8022 -o ProxyCommand="cloudflared access ssh --hostname term.YOUR-DOMAIN.example" file.py <termux-user>@term.YOUR-DOMAIN.example:~/
```

## Sources

- Official wiki: https://wiki.termux.com (bot-protected, use browser)
- termux-boot: https://github.com/termux/termux-boot
- termux-services guide: https://ivonblog.com/en-us/posts/termux-services/
- PocketClaw boot pattern: https://pocketclaw.dev/guides/termux-boot
- SSH bootstrap skill: https://github.com/Sunwood-ai-labs/android-termux-ssh-bootstrap-skill
