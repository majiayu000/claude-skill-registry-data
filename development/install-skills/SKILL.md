---
name: install-skills
description: Install skills of the ai-maxxing package on the user's VPS so their Hermes agent (and Claude Code on the server) can use them - connect-tool, create-landing, create-software, verify, grill-me, lumail, stripe-checkout and more. Shows what can go on the server, lets the user pick, installs and checks. Use after setup-vps, when the user wants Hermes to have more skills or asks how to give it one.
argument-hint: "[skill names, or nothing to choose] [alias, default hermes]"
user-invocable: true
---

Give the user's Hermes agent the skills they pick from the ai-maxxing package. They land in `~/.agents/skills` on the server, the folder Hermes reads (Claude Code there reads it through `~/.claude/skills`). The arguments are skill names (none: let the user choose) and the alias (default `hermes`; use it everywhere below). Talk to the user in their language, short messages, no jargon (say "your agent", "the server", never "symlink", "gateway" or "frontmatter").

Run every remote command as `ssh hermes '<command>' < /dev/null`.

1. Check what is ready: `ssh -o BatchMode=yes hermes true` (otherwise run `connect-vps`), then `ssh hermes 'hermes-setup check'` lists hermes and gateway as ok and its `skills=` line has `ai-maxxing-skills` (otherwise run `setup-vps`, or only its steps 2 and 10 when Hermes already works).
2. Show the catalog: `ssh hermes 'hermes-setup catalog'`. It updates the package on the server and prints one line per skill that works there: `installed`, `available`, or `own` (the user's own skill under that name, never replaced). Skills that need their computer (`connect-vps`, every `setup-*`, `dev-browser`) are not in it.
3. Unless they named skills, ask which to install and recommend the default pack of Hermes, the lines marked `base` (the list and why each one is in it: [../setup-vps/hermes-pack](../setup-vps/hermes-pack)): the server's tool skills, `create-dashboard` (Hermes puts their personal dashboard online, then builds its modules), `connect-tool` (connect any tool, Notion, Stripe, a CRM...) and `create-internal-app` (private apps on the server). Most of the kit is made for Claude Code on their computer: add more only when they want Hermes to do that job too, for example `create-landing` or `create-software` to build sites, `lumail` for their emails. Show the other `available` ones in one short list with what each lets them ask Hermes. They answer "the default pack", "all", or names, or a mix.
4. Install: `ssh hermes 'hermes-setup add <base|all|skill>...'`, for example `add base lumail`. Each line says `installed=`, `kept=` (their own skill, left as it is) or `skipped=` (needs their computer). Exit code 4 names a skill that is not in the package: check the spelling against the catalog. Hermes picks them up on its own, no restart.
5. Prove it: `ssh hermes 'hermes skills list'` lists each new skill as `local`, and `ssh hermes 'hermes -z "Which skills do you have from ~/.agents/skills? Names only." < /dev/null'` names them.

End with one line per skill, a check or a cross. Then tell the user in 3 lines: from now on they can simply message Hermes on Telegram or Discord "install the default pack", "install the connect-tool skill", "which skills can you install?", "update your skills" or "remove create-landing" (it has the `ai-maxxing-skills` skill for that); a new skill is ready from their next conversation (`/new` in the chat starts one); and their own skills are never touched.
