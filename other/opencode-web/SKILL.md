---
name: opencode-web
description: Start, stop, or show access URLs (LAN and Tailscale) for the OpenCode v2 web UI running on this Mac. Use when the user asks to open OpenCode in a browser, access it from their phone, or fix the web UI connection.
---

Use OpenCode's service commands directly. Do not create a LaunchAgent. The web UI
starts only when requested.

```sh
OPENCODE2="$HOME/.bun/bin/opencode2"

# Configure and start
"$OPENCODE2" service set hostname 127.0.0.1
"$OPENCODE2" service set port 4577
"$OPENCODE2" service set password phone-open-4577
"$OPENCODE2" service start

# Manage an existing service
"$OPENCODE2" service status
"$OPENCODE2" service restart
"$OPENCODE2" service stop
```

Facts:

- The shared background service lets the TUI and web UI use the same sessions.
- Local URL: `http://127.0.0.1:4577`.
- Username is ignored. The configured password is `phone-open-4577`.
- For phone access, run `tailscale serve --bg --yes 4577`, then use the HTTPS
  URL from `tailscale serve status`.
- If the phone freezes on an old session, use a private tab or clear the site's
  browser data.

To stop phone access, run `tailscale serve reset`. This does not stop OpenCode.
