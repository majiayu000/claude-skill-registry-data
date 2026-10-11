---
name: init
description: 'Initialize Trigger.dev in the current project Arguments: [--api-url <url>] [--project-ref <ref>].'
---

# Initialize Trigger.dev

The CLI has no self-hosted switch of its own. A self-hosted instance is selected with `--api-url` (`-a`), and this command takes the same flag.

1. Check if `trigger.config.ts` already exists in the project root
2. If `--api-url` was given, run:
   ```bash
   npx trigger.dev@latest init -a <url>
   ```
   Otherwise run:
   ```bash
   npx trigger.dev@latest init
   ```
   - Add `-p <ref>` when `--project-ref` was given.
   - In a non-interactive shell (agent, CI) `init` fails without `-y`/`--yes`, and `-y` needs `-p <ref>` (or `--project-name` with `--org-name` for a new account). Add `--no-browser` so login prints the URL instead of opening a browser.
3. Verify `trigger.config.ts` was created and contains `maxDuration` (required, at least 5 seconds); add `maxDuration: 300` if it is missing
4. Verify `src/trigger/` directory exists with an example task
5. Check that `@trigger.dev/sdk` is in `package.json` dependencies
6. If self-hosted, ensure `.env` has `TRIGGER_API_URL` and `TRIGGER_SECRET_KEY` (the secret key of the environment you are working in)
7. Display next steps: "Run `npx trigger.dev@latest dev` to start the dev server"