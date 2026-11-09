---
name: server-tools
description: What this server can do and which command does each job - GitHub with gh, Cloudflare with cf, putting an app or site online at <name>.__DOMAIN__ with expose, the agent's own health with hermes-setup. Use whenever a task touches a GitHub repo, a domain or DNS, Cloudflare, publishing a site or an app, or checking which tools exist on this machine.
---

# Tools on this server

This is the owner's server, running 24/7. Every tool below is already signed in: never print a token, a key or a password, and never sign a tool out.

| job | command | check |
|---|---|---|
| GitHub: repos, clone, push, PRs, issues | `gh`, see the `github-cli` skill | `gh auth status` |
| Cloudflare: DNS, Workers, R2, KV, D1, cache | `cf`, see the `cloudflare` skill | `cf auth whoami` |
| Put an app online with HTTPS and the sign-in page | `expose` | `expose status` |
| Who can sign in (email + code, admin or member) | `expose user` | `expose user list` |
| The agent itself: model, chat, dashboard | `hermes-setup` | `hermes-setup check` |
| Who may talk to the agent on Discord (the `Hermes access` role; they join the server first) | `hermes-discord access add\|remove <username>` | `hermes-discord access list` |
| More skills from the ai-maxxing package | `hermes-setup add <skill>`, see the `ai-maxxing-skills` skill | `hermes-setup catalog` |

## Cloudflare on this server

`cf` is signed in with `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` from `~/.config/cloudflare/env` (loaded by login shells and by the agent). That access only works from this server's address. If `cf` says it is not signed in, run the command through `bash -lc '<command>'`; never run `cf auth login` here.

## Put something online

1. Run the app as a service listening on `127.0.0.1:<port>` only.
2. `expose add <name>.__DOMAIN__ <port>`: it creates the address, HTTPS and the sign-in page in front. Add `--admins` when the page can change the server or shows private data only the owner should see (like the Hermes dashboard): members then get "restricted access".
3. `expose status` lists what is online; `expose remove <name>.__DOMAIN__` takes it down.

Never open a port in the firewall, never bind `0.0.0.0`, never publish a page another way. Every page sits behind the sign-in page: never use `expose allow` or `--public` unless the owner asks for that exact page or address. `expose unlock` clears a lock after too many wrong codes.

## Who can sign in

People sign in with their email and a 6-digit code sent by Lumail (`expose status` shows `sign_in=code`). An `admin` opens every page; a `member` opens every page not added with `--admins`.

- "Add <email> to the dashboard" or "give <email> access": `expose user add <email> member --invite` (it emails them the links they can open). Make someone `admin` only when the owner says so, in those words.
- "Remove <email>": `expose user remove <email>`; it signs them out at once. The last admin cannot be removed.
- `expose user list` shows everyone with their role.
- An app behind the gate receives `X-Gate-User` (the email, empty for a saved IP) and `X-Gate-Role` (`admin` or `member`): use them to show who is there and to keep admin actions for admins, never a second password.

## Rules

- Ask the owner before anything that can cut access or break what runs: SSH or firewall settings, a reboot, deleting files, containers or databases, an OS upgrade, anything public or paid.
- Delete with `trash <path>` when it is installed, never `rm -rf` on anything of value.
