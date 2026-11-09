---
name: create-landing
description: Create a landing page, sales page or waitlist on Cloudflare with TanStack Start, shadcn/ui, a Lumail email form and an optional Stripe or Codeline buy button, no database or sign-in. Use when the user wants a landing, sales, waitlist, launch or lead magnet page.
argument-hint: "<what the page sells or collects, domain or subdomain>"
disable-model-invocation: true
user-invocable: true
---

Build one fast page that turns visitors into emails or buyers, and put it live on the user's Cloudflare domain. Do every step yourself with the CLIs and only ask for what needs a human (a browser login, a payment link, a photo). Talk to the user in their language, short messages, no jargon. If the page needs accounts, a dashboard or saved data, switch to `create-software`; for a private tool, `create-internal-app`.

If you got this skill from a link instead of a local folder, install nothing else from the repo: fetch a file only when a step needs it, with `curl -fsSL https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/create-landing/<path> -o <scratch>/<file>`, and read another skill it names only when you reach it, from `https://raw.githubusercontent.com/Melvynx/ai-maxxing-skills/main/skills/<skill-name>/SKILL.md`.

Keep this stack, with no Convex, no Better Auth and no database:

- Page, routing, form server function: TanStack Start (React, TypeScript, Vite), pages prerendered.
- UI: shadcn/ui on Base UI + Tailwind CSS v4, `lucide-react` icons, `sonner` toasts.
- Email form: TanStack Form + `zod`, a server function that calls the Lumail API.
- Buy button, only if it sells: a Stripe Checkout payment link or the user's Codeline checkout URL.
- Video, optional: a Tella embed from the URL the user pastes.
- Hosting, domain, DNS: Cloudflare Workers with `@cloudflare/vite-plugin`, deployed with `cf`, then automatically by a GitHub Action on every push to `main`.
- Code: Git and one private GitHub repo.

1. Check access and fix what fails with the matching setup skill (`setup-github`, `setup-cloudflare`, `setup-convex`, `setup-lumail`, `setup-node` when `npx` is missing) first. When a login needs the browser, give the exact link or code and wait for "done".

   ```bash
   git --version && gh auth status       # GitHub
   cf --version && cf auth whoami        # Cloudflare (npm i -g cf, then cf auth login)
   npx lumail@latest auth test           # Lumail (npx lumail@latest setup --authenticate)
   ```

2. Run the `grill-me` skill in its landing mode and build only once the user confirms the brief.
3. Write the copy before the code, in the user's language and voice, and show it as plain text for a yes. Unless the brief says otherwise: hero (promise, sub-promise, call to action), the problem, the solution, what they get, proof, offer and price, FAQ for the objections, final call to action, footer with legal links. Use only the testimonials, numbers and deadlines the user gave, or leave a clear placeholder.
4. Scaffold TanStack Start + Tailwind + `npx shadcn@latest init` (Base UI flavor) with only the components you need. `git init`, then `gh repo create <name> --private --source . --push`.
5. Build `/` from the sections, plus `/merci` (after signup or purchase) and `/mentions-legales` or `/legal`, all prerendered, each with a real `<title>`, a meta description, an Open Graph image (1200x630) and a favicon. Keep one page, one goal, one call to action repeated, and no menu that leads visitors away.
6. Follow the 1 or 2 sites the user likes: one font pair, one accent color, generous spacing, mobile first, WebP images with width and height set, no layout shift, no heavy animation library.
7. Build the email form with TanStack Form + `zod` on the client and a `createServerFn` that posts to Lumail. Create `LUMAIL_API_KEY` yourself with `lumail tokens --help`; it stays a Cloudflare secret, never in a committed file or the browser.

   ```ts
   await fetch("https://lumail.io/api/v1/subscribers", {
     method: "POST",
     headers: { Authorization: `Bearer ${process.env.LUMAIL_API_KEY}`, "Content-Type": "application/json" },
     body: JSON.stringify({ email, tags: ["<page-slug>-lead"] }),
   });
   ```

   Keep double opt-in on, since a landing form is cold and the email is not verified. Add a hidden honeypot field, reject empty or fake emails on the server, and go to `/merci` after a success. If the brief asks for a welcome email or lead magnet, create the tag workflow with the `lumail` skill.
8. If it sells, link the buy button to the Stripe payment link or the Codeline checkout with the success URL set to `/merci`. Never collect card details on the page.
9. Add analytics only if the user asks: one privacy-friendly script, nothing that needs a cookie banner.
10. Deploy on Cloudflare. `wrangler.jsonc` gets `main: "@tanstack/react-start/server-entry"`, `compatibility_flags: ["nodejs_compat"]` and the custom domain in `routes` with `custom_domain: true`. Set `LUMAIL_API_KEY` as a Cloudflare secret, then build and deploy once with `cf` (`cf build`, `cf deploy`, or `cf cli search "deploy worker"`), never by hand in the dashboard; see the `cloudflare` skill. If the domain is not in the user's Cloudflare account, tell them to move the name servers or buy it there.
    Then always set up auto deploy, by default, without asking: `.github/workflows/deploy.yml` builds and deploys the Worker on every push to `main`, with the `CLOUDFLARE_API_TOKEN` GitHub secret. Follow [references/auto-deploy.md](references/auto-deploy.md). From then on every redeploy is a push, watched with `gh run watch`.
11. Prove it on the live URL: every section shows on desktop and at phone width with no horizontal scroll, every link and button works, a real email signup lands on `/merci` and shows up in Lumail with the right tag and its confirmation email arrives, the buy button opens the right checkout and price, Lighthouse on mobile scores 90 or more in performance and accessibility, a chat link preview shows the title, description and image, and a push to `main` turns the GitHub Action green and the change shows on the live URL. Fix every error you see before saying it is live.

Reply with the live URL, the Lumail tag the signups get, that every push to `main` now goes live on its own, and what is left to do.
