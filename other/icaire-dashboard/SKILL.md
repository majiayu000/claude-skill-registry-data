---
name: icaire-dashboard
description: Open the remote ICAIRE dashboard in the user's browser. Use when the user asks to open, launch, view, or go to the ICAIRE dashboard.
---

# ICAIRE Dashboard

Open the remote ICAIRE dashboard for the user.

## Contract

- Use this exact dashboard URL:
  `https://icaire-cortex-server-production.up.railway.app/dashboard`
- Open it in the user's browser when local browser access is available.
- The dashboard is auth-gated. If it redirects to sign-in, that is expected.
- If browser opening is unavailable or fails, return the dashboard URL in chat.
- Do not substitute `/connect`, `/mcp`, or the service root for the dashboard.

## Workflow

1. Open the dashboard URL in the user's browser.
2. If you need to use the shell on macOS, run:

   ```sh
   open "https://icaire-cortex-server-production.up.railway.app/dashboard"
   ```

3. Tell the user the dashboard was opened. If opening failed, give them the URL.
