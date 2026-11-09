---
name: create-software
description: Create and deploy a public web app on Cloudflare with TanStack Start, shadcn/ui, Convex, Better Auth, Lumail and optional Stripe, with an admin area, API and CLI so AI controls it. Use when asked to build or ship a SaaS, course platform, membership or client portal people sign up to or pay for.
argument-hint: "<what the app does, domain or subdomain>"
disable-model-invocation: true
user-invocable: true
---

Build a working web app on the user's own accounts and put it live on their Cloudflare domain. Do every step yourself with the CLIs and only ask for what needs a human (a browser login, a device code, a payment, a secret key). Talk to the user in their language, short messages, no jargon. For a private tool only the user and their agent use, switch to `create-internal-app`; for a page with no sign-in, switch to `create-landing`.

If you got this skill from a link instead of a local folder, install nothing else from the repo: download a file it links only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/create-software/<path> -o <scratch>/<file>` (for example `references/fast-app.md`), and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Keep this stack unless the user asks to swap a layer:

- App, routing, server functions: TanStack Start (React, TypeScript, Vite).
- UI: shadcn/ui on Base UI + Tailwind CSS v4, `lucide-react` icons, `sonner` toasts.
- Database, backend, files, crons: Convex for everything, no other database or API server.
- Auth: Better Auth through `@convex-dev/better-auth`, email OTP by default.
- Marketing and login emails: Lumail through `@lumail/convex`.
- Payments, only if the app sells: Stripe Checkout with the `stripe-checkout` skill.
- Video: Tella embeds from the URL the user pastes.
- Hosting, domain, DNS: Cloudflare Workers with `@cloudflare/vite-plugin`, deployed with `cf`, then automatically by a GitHub Action on every push to `main`.
- Code: Git and one private GitHub repo.
- Control by AI: an admin area at `/admin`, an API at `/api/v1` with API keys, and a CLI named after the app with its `<app>-cli` skill.

Every app is built so the user's AI can run it, not only the user's mouse. Always build, and always explain to the user in one plain sentence, the admin part: an `/admin` area for the owner, a clean API reached with API keys, and a CLI plus skill so their agent controls the whole app from the terminal, like Lumail (admin pages, `/api/admin/*`, admin keys, the `lumail` CLI). Anything the owner can do in `/admin`, the API and the CLI can do too. This is never optional and never cut from v1. Details in [references/admin-api-cli.md](references/admin-api-cli.md).

Reach for the TanStack library before any other package for client jobs: `@tanstack/react-query` + `@convex-dev/react-query` (`convexQuery(api.x.y, args)`) for fetching and cache, `@tanstack/react-table` for lists, sorting, filters and pagination, `@tanstack/react-virtual` for long lists, `@tanstack/react-form` + `zod` for forms, `@tanstack/markdown` to render markdown, `@tanstack/react-hotkeys` for shortcuts (`cmd+k`, `j`/`k`, `esc`), `@tanstack/react-pacer` to debounce search and throttle saves, `@tanstack/ai-react` for AI chat or generation. Check each package's current API (`npm view <pkg> version`, then its README or `find-docs`) instead of writing it from memory.

1. Check access and fix what fails with the matching setup skill (`setup-github`, `setup-cloudflare`, `setup-convex`, `setup-lumail`, `setup-node` when `npx` is missing) before writing code. When a login needs the browser, give the exact link or code and wait for "done".

   ```bash
   git --version && gh auth status       # GitHub
   cf --version && cf auth whoami        # Cloudflare (npm i -g cf, then cf auth login)
   npx convex --version                  # Convex (npx convex login when building)
   npx lumail@latest auth test           # Lumail (npx lumail@latest setup --authenticate)
   ```

2. Decide first, with the user: does this app need organizations (multi-tenant)? Team members, shared data, roles, invitations, billing per company or API keys per workspace mean yes; a single-user tool means no. Yes changes every table, query and URL from day 1, so follow [references/organizations.md](references/organizations.md). Then run the `grill-me` skill and build only once the user confirms the brief; skip it only if a brief was already confirmed in this conversation. Defaults: landing at `/`, app at `/app` (`/:org/...` with organizations), admin at `/admin`, English UI, OTP sign-in, the user is the only admin. When you show the brief, tell the user the app comes with an admin area, an API and a CLI so their AI can manage everything, and ask what they will want their AI to do in it (for example "list today's sales", "refund an order", "ban a user").
3. Always write the confirmed brief to `SPEC.md` at the app root, before any code, so every later conversation starts from it:
   - The brief: goal, who uses it, the user story screen by screen, every screen, the data objects and their fields, what is out of v1, and what "done" means for the user.
   - An `## Admin, API, CLI` section: every admin page, every API route (`GET /api/v1/admin/users`...) and the CLI command that matches it, from what the user wants their AI to do.
   - A `## Tasks` checklist, very precise: one small change per box, named by its route, screen, field or Convex function, each with a `Check:` line saying how to prove it works on the real app. Write `- [ ] /app/lessons lists lessons in a table, newest first, 20 per page. Check: with 25 lessons, page 2 shows 5`, never `- [ ] lessons page`.
   - Go through [references/product-rules.md](references/product-rules.md) (URLs, access, search, composer, tags, agents, webhooks, email rendering, deploy) and add a task for every rule that applies.
   - Add an `AGENTS.md` at the app root that says: read `SPEC.md` before any change; for a new feature or fix, add its tasks to `SPEC.md` first, then build; after building or changing any screen, run `better`; never stop until every task matches.
4. Scaffold TanStack Start + Tailwind + `npx shadcn@latest init` (Base UI flavor) and add components with `npx shadcn@latest add`. `git init`, then `gh repo create <name> --private --source . --push`.
5. Run `npx convex dev --once` to create the project and `.env.local`. Write one `schema.ts` with an index for every query. Every public function checks the signed-in user and ownership server-side, anything only the server calls is `internal*`, and reads are bounded with `.take(n)` or `.paginate()`. With organizations, every table has `orgId` and every function checks membership and role. See the `convex` skill.
6. Wire Better Auth: register both components in `convex/convex.config.ts` (`app.use(betterAuth)`, `app.use(lumail)`), `createAuth` with `authComponent.adapter(ctx)`, the `emailOTP` plugin and the `convex({ authConfig })` plugin, routes via `authComponent.registerRoutes(http, createAuth)`, `BETTER_AUTH_SECRET` and `SITE_URL` as Convex env vars. Protect `/app` in the route `beforeLoad` and again in every Convex function.
7. Wire Lumail in one `convex/email.ts` that holds every call. Create `LUMAIL_API_KEY` yourself with `lumail tokens --help`; it never reaches the browser.
   - Login codes: `sendVerificationOTP` schedules an internal mutation that calls `lumail.sendEmail(ctx, { ..., transactional: true })`. Without a key, log the code to the Convex console so local dev still works.
   - Signups: in Better Auth `databaseHooks.user.create.after`, upsert the person with `lumail.upsertSubscriber(ctx, { email, tags: ["<app-slug>-user"], triggerWorkflows: true })`.
   - Skip double opt-in for anyone who signs in or buys, since the OTP or the payment proves they own the email: they go straight to "subscribed" and tag workflows fire right away. The component cannot pass that flag, so also call the API from an internal action:

     ```ts
     await fetch("https://lumail.io/api/v1/subscribers", {
       method: "POST",
       headers: { Authorization: `Bearer ${process.env.LUMAIL_API_KEY}`, "Content-Type": "application/json" },
       body: JSON.stringify({ email, skipDoubleOptIn: true }),
     });
     ```

   - Keep double opt-in only for a cold form (newsletter or waitlist where the email is not verified).
   - Create the sending domain with `lumail domain --help` and add the DNS records it returns in Cloudflare yourself (unproxied). More in the `lumail` skill.
8. Put data on screen with `useSuspenseQuery(convexQuery(...))` so the UI updates live, lists in TanStack Table, forms in TanStack Form calling Convex mutations, toasts on success and error. Build every screen, admin included, to [references/design-system-rules.md](references/design-system-rules.md). After building any screen, run the `better` skill on it, in light and dark, and finish its screenshot loop before moving on.
9. Build the admin area, API keys, API and CLI with [references/admin-api-cli.md](references/admin-api-cli.md): each action is one internal Convex function called by the admin page and by the API, keys stored hashed and shown once, `/api/v1` on the app domain, `cli/<app>.mjs` installed with `npm install -g ./cli`, then the `<app>-cli` skill in `~/.agents/skills`. Every new feature later gets its admin view, route and CLI command in the same change.
10. Make it fast on every page with [references/fast-app.md](references/fast-app.md): `defaultPreload: "intent"`, a 30 s query cache, a loader on detail pages, a custom `pendingComponent` skeleton on every route that matches the real layout, a loading state on every async button, indexed and bounded Convex reads. An app without these is not done.
11. If the app sells, start with a fake checkout until the user gives Stripe test keys, then real Checkout and a signed webhook in `convex/http.ts` that grants access. Test card `4242 4242 4242 4242`, live keys only once the test flow works. See the `stripe-checkout` skill.
12. Add a clean error page, a 404 page, a favicon and page titles.
13. Deploy on Cloudflare. `wrangler.jsonc` gets `main: "@tanstack/react-start/server-entry"`, `compatibility_flags: ["nodejs_compat"]`, `SITE_URL` in `vars` and the custom domain in `routes` with `custom_domain: true`. Run `npx convex deploy`, set prod env vars with `npx convex env set --prod`, and commit the prod `VITE_CONVEX_URL` / `VITE_CONVEX_SITE_URL` in `.env.production`. Build and deploy once with `cf` (`cf build`, `cf deploy`, or `cf cli search "deploy worker"`), never by hand in the dashboard; see the `cloudflare` skill. If the domain is not in the user's Cloudflare account, tell them to move the name servers or buy it there.
    Then always set up auto deploy, by default, without asking: `.github/workflows/deploy.yml` deploys Convex then the Worker on every push to `main`, with the `CLOUDFLARE_API_TOKEN` and `CONVEX_DEPLOY_KEY` GitHub secrets. Follow [references/auto-deploy.md](references/auto-deploy.md). From then on every redeploy is a push, watched with `gh run watch`.
14. Open the live URL and walk the real flows: landing, sign in with a real OTP email, the main action, a list with real rows, a test purchase if the app sells, a keyboard shortcut, sign out, the 404 page. Then the admin: create an admin key in `/admin/api-keys`, `<app> login`, `<app> whoami`, list a resource with `--json` and compare it with the admin page, make one write through the CLI and see it in Activity, and check that no key or a revoked key gets refused. Check the person shows up in Lumail as subscribed with the right tag, and that a push to `main` turns the GitHub Action green and the change shows on the live URL. Fix every error you see, then run `audit-safety` on auth, data access, API keys, admin routes and payments.
15. Re-read `SPEC.md` and run every task's `Check:` on the live URL. Tick a box only once its check passes there, never because the code is written. Do not stop and do not reply while one box is unticked or the live app differs from the spec: fix it, push, wait for the Action, check again, and repeat until everything matches. A task blocked only by a human step (a login, a key, a payment) stays unticked with the reason written next to it; finish all the others first.

Secrets go only in `.env.local`, `npx convex env set`, Cloudflare secrets or GitHub secrets (`gh secret set`), never in a committed file, a log or the chat. Reply with what is live, the URL, the admin URL, that every push to `main` now goes live on its own, the CLI command and the `/<app>-cli` skill their agent can now use (with one sentence to try, like "ask your AI: how many people signed up this week?"), the `SPEC.md` tasks all ticked, and only the human steps left to do.
