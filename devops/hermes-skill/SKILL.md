---
name: dashboard
description: Build, change or remove a module of the owner's personal web dashboard, and push data to it. Use when the owner asks to see something on their dashboard, add a page or a card to it, or have a cron post a report there.
version: 1.1.0
author: ai-maxxing
license: MIT
platforms: [linux]
prerequisites:
  commands: [dashboard, dashboard-cli, node, pnpm, git]
metadata:
  hermes:
    tags: [dashboard, web, modules, reports]
---

# Dashboard

The owner has a personal web dashboard next to you. Every module on it is one they asked you for; the System monitoring group is built in for admins: Conversations (your latest sessions), Infra (server health, the daily `infra-audit` cron, fixes sent to your board) and Models (the model you answer with; the owner can switch it there, and connecting a new provider stays with you). The code is in `~/projects/dashboard`, a git repository on their GitHub, and it runs as the `dashboard` service.

1. Read `~/projects/dashboard/AGENTS.md` first: it has the stack, the recipe to add a module and the rules. Follow the code that is already there.
2. Build only what the owner asked, as one module (a page, its line in the sidebar, its mark). If the request is vague, pick the most useful small version and say what you chose.
3. To see what a Hermes endpoint returns before you use it: `dashboard hermes /api/cron/jobs` (sessions, crons, skills, usage, status).
4. Ship with `dashboard deploy`. It typechecks, tests and builds before restarting, and keeps the old version online if anything fails: read the error, fix it, deploy again.
5. Commit and push: `cd ~/projects/dashboard && git add -A && git commit -m "<module>: <what it shows>" && git push`.
6. Answer the owner in one or two lines: what the module shows and its address (the `url` line of `dashboard status`, plus the module path).

To push data from a cron or a task (a morning report, today's numbers), the module needs a write route (step 5 of the recipe). Then `dashboard-cli post /api/v1/<name> '<json>'`. If `dashboard-cli get /api/v1/whoami` says there is no key, run `dashboard key` once.

Several people may sign in (`expose user list`): admins see everything, members see the modules but not System monitoring (Conversations, Infra, Models, the Hermes link), the API keys or the Team page. A module that only admins should see or change uses `getViewer()` or `requireAdmin()` from `src/server/viewer.ts` (see the AGENTS.md). To let someone in: `expose user add <email> member --invite`. Admins can also add and remove members on the Team page (`/team`); when it says the list is unavailable, they ask you.

An Infra task on your board (title "Fix: ...") came from the owner pressing "Fix": follow it, never open a port in the firewall, and ask the owner before anything that could cut their access (SSH, firewall, a restart of the server). `dashboard-cli get /api/v1/infra` gives the last check and audit.

Never print a key or a token, never publish the dashboard another way than it already is, and never delete the database in `~/.local/share/dashboard`.
