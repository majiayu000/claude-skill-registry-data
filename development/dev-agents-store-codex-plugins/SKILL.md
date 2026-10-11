---
name: dev
description: 'Start the Trigger.dev dev server Arguments: --profile <name>.'
---

# Start Dev Server

1. Verify `trigger.config.ts` exists in the project
2. Build the dev command:
   - Base: `npx trigger.dev@latest dev` (`dev` is a command group; `start` is the default sub-command, so this runs `dev start`)
   - If `--profile` argument: add `--profile <name>`
   - If monorepo detected: add `--config <path-to-trigger.config.ts>`
3. Run the command
4. The dev server will watch for file changes and register tasks with the dev environment
5. In an agent session prefer the MCP tool `start_dev_server` (it runs `trigger dev` in the background); a foreground `dev` blocks the Bash tool