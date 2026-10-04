---
name: safe-web-project
description: Clone, scan, install, and run a web project safely.
---

# Safe Web Project Setup

## Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Safety scan** – Search for dangerous patterns that could indicate malware or virus:
   ```bash
   grep -r "eval" src/ 2>/dev/null || echo "No eval found"
   grep -r "Function(" src/ 2>/dev/null || echo "No Function constructor found"
   grep -r "\\.innerHTML\\s*=" src/ 2>/dev/null || echo "No innerHTML assignment found"
   ```
   If any of these return actual matches (not just the "No ..." lines), treat as potential virus and abort unless you confirm it's legitimate.

3. **Install dependencies**
   - Check `package.json` for npm/yarn/pnpm.
   - Run the appropriate install command, e.g.:
     ```bash
     npm install
     ```
   - Wait for completion; note any vulnerabilities from `npm audit` but understand that moderate/high warnings in dev dependencies are common and not indicative of malware.

4. **Start the development server**
   - Identify the start script (usually `dev` or `start`) in `package.json`.
   - Run it in the background:
     ```bash
     npm run dev &
     ```
   - Wait a few seconds, then verify the server is listening on the expected port (e.g., 5173 for Vite) using:
     ```bash
     netstat -tlnp | grep :<port> || ss -tlnp | grep :<port>
     ```
   - Open `http://localhost:<port>` in the browser to interact with the prototype (GUI preference).

5. **Quick‑action preference** – Provide exact commands and paths; the user prefers copy‑paste ready steps over lengthy explanations.

## Pitfalls

- **Do not confuse npm audit warnings with malware** – moderate/high vulnerabilities in dev dependencies (e.g., esbuild, vite) are common and not indicative of a virus; only block if you find actual malicious code patterns.
- **If the repo uses a different package manager** (yarn, pnpm), adjust the install and run commands accordingly.
- **Some projects may require environment variables**; check README for any required setup before running.
- **If the repo claims to be a directory of APIs or code examples**, expect mostly documentation (`.md`, `.txt`) and example snippets (`.js`, `.ts`, `.py`, `.sh` in `code-examples/`). Presence of compiled binaries (`.exe`, `.dll`), obscure scripts, or large obfuscated blobs (e.g., long base64 strings) warrants deeper inspection.