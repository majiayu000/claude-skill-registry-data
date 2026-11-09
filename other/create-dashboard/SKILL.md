---
name: create-dashboard
description: Put the owner's personal web dashboard online at dashboard.__DOMAIN__, in the Hermes look (TanStack Start, Tailwind, SQLite), behind the server's sign-in page, empty until they ask for modules. Use when the owner asks for their dashboard, a personal dashboard or a home page for their agent, or asks for a dashboard module and `dashboard status` says there is no dashboard yet.
---

# Create the owner's dashboard

Run everything here, on the server. It takes about ten minutes, mostly the first install: tell the owner in one line that you are on it, then report once at the end. When the login user is not `root`, prefix `install` and `expose` with `sudo`. Never print a key or a token, never publish the dashboard another way than `expose add`, and never replace an existing `~/projects/dashboard`: it holds the owner's modules.

1. Already there? If `command -v dashboard` works and `dashboard status` says `health=ok`, the dashboard exists: give the owner its `url` line and stop. A dashboard module is the `dashboard` skill's job.
2. Commands: `P=~/.cache/ai-maxxing-skills/skills/setup-my-hermes-dashboard; git -C ~/.cache/ai-maxxing-skills pull -q --ff-only; install -m 755 $P/scripts/dashboard.sh /usr/local/bin/dashboard && install -m 755 $P/scripts/dashboard-cli /usr/local/bin/dashboard-cli`.
3. Code, only if `~/projects/dashboard` does not exist: `mkdir -p ~/projects && cp -R ~/.cache/ai-maxxing-skills/skills/setup-my-hermes-dashboard/template ~/projects/dashboard && cd ~/projects/dashboard && git init -q -b main && git add -A && git commit -qm "Dashboard: empty shell"`, then save it on their GitHub, private: `gh repo create hermes-dashboard --private --source . --push`. If that name is taken, ask the owner before using another.
4. Node: `dashboard install-node`.
5. Service: `DASHBOARD_OWNER=<first word of git config --global user.name> DASHBOARD_URL=https://dashboard.__DOMAIN__ HERMES_URL=https://hermes.__DOMAIN__ dashboard deploy`. It ends with `dashboard ok on 127.0.0.1:8794`. On exit code 4, read the error it prints and fix it; on 5, read the service log it prints.
6. Your access to it: `dashboard key`, then `dashboard-cli get /api/v1/whoami` answers `"key": "hermes"`.
7. The skill to build modules: `hermes-setup add dashboard`.
8. Online: `expose add dashboard.__DOMAIN__ 8794`. Exit code 4 means that address already points elsewhere: ask the owner for another name such as `home.__DOMAIN__`, and redo step 5 with that `DASHBOARD_URL`. Then `expose status` lists the site and no line starting with `UNPROTECTED`.
9. Check: `curl -s -o /dev/null -w '%{http_code}' https://dashboard.__DOMAIN__` answers `302` (the sign-in page) or `200` after a minute.

Then tell the owner in 3 lines: the dashboard is at `https://dashboard.__DOMAIN__` behind the same sign-in as Hermes, its Infra page watches the server (a check every 15 minutes, an audit every morning, a "Fix" button that sends you the task), and they can ask you any module ("my latest conversations", "my crons", "today's sales"), each one saved on their GitHub (`hermes-dashboard`). Their next conversation (`/new`) knows how to build modules. When they ask to share it, `expose user add <email> member --invite` lets that person in by email code: a member sees the modules, not Hermes, the API keys or the Team page (where admins add and remove members).
