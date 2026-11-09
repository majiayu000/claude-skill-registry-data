---
name: create-internal-app
description: Create a private internal app on the user's VPS through Dokploy, locked by password and IP allowlist, always with an admin area, an API with keys and a CLI so their agent (Hermes) controls everything. Use when the user wants an internal tool, CRM, dashboard, back-office or an app "just for me" or "only for my team".
argument-hint: "<what the tool does, subdomain>"
disable-model-invocation: true
user-invocable: true
---

Build a private tool on the user's own VPS and hand it to their agent to run. Do every step yourself with the CLIs and only ask for what needs a human (a browser login, their IP). Talk to the user in their language, short messages, no jargon. For an app other people sign up to or pay for, switch to `create-software`.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/create-internal-app/<path> -o <scratch>/<file>` (for example `references/fast-app.md`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

The app has a normal URL (`crm.my-domain.com`) that nobody else can open, behind three walls: a Cloudflare WAF custom rule on the app and Convex hostnames that lets through only the user's IPs and the VPS IP, Dokploy basic auth with a long random password the user keeps in their password manager, and a server-side secret or signed-in user check in every Convex function. When the user's IP changes (travel, 4G), they ask their agent "add my IP" and it updates the rule. For a team, Cloudflare Access with email codes can replace the IP list.

Keep this stack:

- App: TanStack Start (React, TypeScript, Vite) with a Node server build.
- UI: shadcn/ui on Base UI + Tailwind CSS v4, `lucide-react`, `sonner`.
- Database, backend, crons: Convex, self-hosted on the VPS with the Dokploy Convex template.
- Client jobs: the TanStack libraries listed in `create-software` (Query + `@convex-dev/react-query`, Table, Virtual, Form, Markdown, Hotkeys, Pacer, AI).
- Emails, only if the tool sends some: Lumail through `@lumail/convex`.
- Hosting: Dokploy on the VPS, built from the GitHub repo.
- Domain, DNS, lock: Cloudflare with the `cf` CLI, DNS proxied, WAF IP rule.
- Run and repair: the user's agent (Hermes) with a Dokploy API token.
- Control by AI: an admin area at `/admin`, an API at `/api/v1` with API keys, and a CLI named after the tool with its `<app>-cli` skill.

Every tool is built so the user's AI can run it, not only the user's mouse. Always build, and always explain to the user in one plain sentence, the admin part: an `/admin` area, a clean API reached with API keys, and a CLI plus skill so their agent (Hermes on Telegram, Claude Code on the Mac) controls the whole tool, like Lumail (admin pages, `/api/admin/*`, admin keys, the `lumail` CLI). Anything the user can do in `/admin`, the API and the CLI can do too. This is never optional and never cut from v1. Details in [references/admin-api-cli.md](references/admin-api-cli.md).

1. Check access and fix what fails with `setup-github` or `setup-cloudflare`. Dokploy must already be installed on the VPS; if it is not, stop and say so, that is the server setup lesson.

   ```bash
   git --version && gh auth status        # GitHub
   cf --version && cf auth whoami         # Cloudflare
   ssh <vps> 'docker ps --format "{{.Names}}" | head'   # the VPS answers
   dokploy-cli auth test                  # or: the Dokploy API token works (curl the API with it)
   ```

2. Run the `grill-me` skill and build only once the brief is confirmed. For an internal tool, the money question becomes "who besides you uses it", and the address question becomes the subdomain plus the IPs to allow (get the current one with `curl -s https://ifconfig.me` on the user's machine). Tell the user the tool comes with an admin area, an API and a CLI so their AI can manage it, and ask what they will want to ask their agent (for example "add this lead", "what's due this week?").
3. Scaffold TanStack Start + Tailwind + `npx shadcn@latest init` (Base UI flavor), a Node server build (TanStack Start hosting docs, Nitro preset for Node) and a `Dockerfile` that builds and runs it on port 3000. `git init`, then `gh repo create <name> --private --source . --push`.
4. Deploy the Dokploy Convex template once per VPS (backend + dashboard) on `convex-api.<domain>` and `convex-site.<domain>`, generate the admin key in the backend container, and point the CLI at it with `CONVEX_SELF_HOSTED_URL` and `CONVEX_SELF_HOSTED_ADMIN_KEY` in `.env.local`. Index every query and bound growing tables with `.take(n)` or `.paginate()`. See the `convex` skill.
5. Write one helper every public Convex function calls first (a shared secret set with `npx convex env set`, or Better Auth with email OTP if several people use it). Anything only the server calls is `internal*`.
6. Build the screens with `useSuspenseQuery(convexQuery(...))` so data updates live, lists in TanStack Table, forms in TanStack Form, and `cmd+k` plus `j`/`k` with TanStack Hotkeys, since an internal tool is used all day.
7. Build the admin area, API keys, API and CLI with [references/admin-api-cli.md](references/admin-api-cli.md): each action is one internal Convex function called by the admin page and by the API, keys stored hashed and shown once, the API on `convex-site.<domain>/api/v1` (not behind basic auth), `cli/<app>.mjs`. Every new feature later gets its admin view, route and CLI command in the same change.
8. Make it fast on every page with [references/fast-app.md](references/fast-app.md): `defaultPreload: "intent"`, a 30 s query cache, a loader on detail pages, a custom `pendingComponent` skeleton on every route that matches the real layout, a loading state on every async button, indexed and bounded Convex reads. An app without these is not done.
9. Create the Dokploy application from the GitHub repo (Dockerfile build) with the env vars (Convex URL, secrets) set in Dokploy, never in the repo, and auto deploy on push.
10. Attach `tool.<domain>` in Dokploy with HTTPS, then create the DNS record in Cloudflare yourself (A record to the VPS IP, proxied). Never open a port on the VPS for the app: everything goes through Dokploy's proxy behind Cloudflare.
11. Enable basic auth on the Dokploy application with a generated password. Give it to the user once and tell them to save it in their password manager; never write it in a file.
12. Create the Cloudflare WAF custom rule that blocks the app and Convex hostnames for any IP outside the list (user IPs + the VPS IP). Find the command with `cf cli search "waf custom rule"`.
13. Add the Convex volume to the nightly Dokploy backup to R2 if the VPS has one.
14. Hand it to the agent: write an `About.md` in the agent's project folder with the URL, the repo, the Dokploy application id, the Convex URLs, where the password lives (never the password) and the IP rule id. Tell the agent how to redeploy (push, or the Dokploy API) and read deploy logs, read app logs and fix when the user says "it's broken", and add or remove an IP in the rule. Install the CLI on the VPS and the Mac with an admin key, set `<APP>_API_KEY` / `<APP>_URL` in Hermes' env, and add the `<app>-cli` skill on both, so Hermes runs the tool itself.
15. Prove it: from an allowed IP the URL asks for the password, then the app loads and the main action works with real data; from a non-allowed IP (another server, or a different network) Cloudflare blocks both the app and the Convex API hostname; a push to GitHub redeploys on its own; `<app> whoami` and a `list --json` work from the VPS and the Mac, a write through the CLI shows in the admin Activity, and a revoked key is refused. Fix every error you see, then run `audit-safety` on the Convex functions, API keys, admin routes and the lock.

Never print, commit or log the password, the admin key or tokens. Reply with the URL, how to open it (password + allowed IPs), the CLI command and the `/<app>-cli` skill, and one sentence to send Hermes to try it.
