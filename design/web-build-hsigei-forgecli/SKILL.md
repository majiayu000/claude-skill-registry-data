---
name: web-build
description: Build or change a website, landing page, homepage, portfolio, dashboard or web app (HTML/CSS/JS, React, Flask, Node…) - frontend UI that looks good, works on phones and is checked in a browser
---
# Build for the web

1. Understand the goal: who uses it, the main thing they do, any brand colours or examples. If the
   project already has a stack, use it; for something new and small, plain HTML/CSS/JS is fine;
   pick a framework only when the app needs it.
2. Structure: semantic HTML (header/main/nav/button/label), one stylesheet with CSS variables for
   colours, spacing and fonts, small JS modules. No inline styles scattered around.
3. Design that holds up:
   - clear type scale and generous spacing; one accent colour; strong contrast (WCAG AA)
   - responsive from 360px wide up (flex/grid, no fixed widths, no sideways scroll on phones)
   - visible focus states, alt text, labels on every input, works with the keyboard
   - loading, empty and error states for anything that fetches data
4. Back ends: validate input on the server, never trust the client, keep secrets in env vars, return
   useful error messages.
5. Check it for real: start it (see the run skill), web_fetch the page to confirm it serves without
   errors, open_url it for the user, and test the main flow. Fix console or server errors before
   saying it's done.
6. For any website or web app that should look and feel high-end, load the
   awwwards-tier-web-application skill (find_skill "awwwards") before designing, and follow it.
   For other bigger work, look up a matching expert skill with find_skill (e.g. "frontend ui",
   "performance", "accessibility") and follow it.
