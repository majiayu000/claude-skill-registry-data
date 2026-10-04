---
name: go-live
description: Use this skill whenever the user wants to deploy their project, go live, ship to production, set up hosting, configure a domain, or make their app accessible on a real URL. Also trigger when the user says things like "how do I deploy this," "I want to put this online," "make this live," "set up production," "I'm done building, now what?" or "get this off localhost." Use this skill even if the user only mentions one part of deployment (like "set up Vercel" or "configure my database for production") — the skill handles the full deploy workflow and will focus on the relevant section.
---

# Go Live

Deploy the user's project from localhost to a live URL with production infrastructure.

## Overview

This skill handles the full deployment workflow:
1. Detect what stack the project uses
2. Configure hosting and generate deploy files
3. Set up production database
4. Configure auth for production
5. Wire environment variables
6. Deploy via CLI
7. Verify the deployment is live

The skill automates everything it can via CLI tools and generates config files directly. It flags manual steps (domain purchase, DNS, payment provider accounts) with exact instructions.

## Before Starting

Read PROJECT.md to understand the tech stack. Then run the stack detection script:

```bash
python {baseDir}/scripts/detect_stack.py [project-root]
```

This script scans the project and outputs a JSON report of:
- Framework detected (Next.js, Remix, Astro, SvelteKit, etc.)
- Package manager (npm, pnpm, yarn, bun)
- Database (Supabase, Neon, PlanetScale, Prisma config, Drizzle config)
- Auth provider (Clerk, Auth.js/NextAuth, Supabase Auth, Lucia)
- Payment provider (Stripe, LemonSqueezy) if present
- Existing deploy config (vercel.json, railway.toml, Dockerfile, etc.)
- Environment variables referenced in code (.env, .env.local, .env.example)

Use this report to determine which steps are needed and which are already configured.

## Step 1: Configure Hosting

Read `references/stack-guides.md` → Section: Hosting for provider-specific instructions.

### Vercel (default for Next.js, Astro, SvelteKit, Remix)

1. Check if Vercel CLI is installed: `npx vercel --version`
   - If not: `npm i -g vercel`
2. Check if `vercel.json` exists. If not, generate one based on framework:

For Next.js:
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "framework": "nextjs"
}
```

For other frameworks, see `references/stack-guides.md`.

3. Check if user is logged in: `npx vercel whoami`
   - If not logged in, tell the user: "Run `npx vercel login` and authenticate in your browser. Tell me when you're done."
   - WAIT for the user to confirm before proceeding. Do not try to automate login.

4. Link the project: `npx vercel link`
   - If the project hasn't been linked before, this creates the Vercel project
   - Accept defaults unless the user specifies otherwise

### Railway (alternative — better for backend-heavy apps, monorepos)

1. Check if Railway CLI is installed: `railway --version`
   - If not: `npm i -g @railway/cli`
2. Tell user: "Run `railway login` and authenticate. Tell me when done."
3. Initialize: `railway init`
4. Link: `railway link`

### Manual Step Flag
If no hosting CLI is available or the user prefers a different provider, flag:
```
MANUAL STEP: Set up hosting
Go to [provider].com → Create new project → Connect your GitHub repo
→ Framework will be auto-detected → Deploy
Tell me when the project is deployed and give me the URL.
```

## Step 2: Production Database

Read `references/stack-guides.md` → Section: Database for provider-specific instructions.

### Supabase

1. Check if Supabase CLI is installed: `npx supabase --version`
   - If not: `npm i -g supabase`
2. Check if the project has local Supabase config (`supabase/config.toml`)
3. Tell user: "Run `npx supabase login` and authenticate. Tell me when done."
4. Link to production project: `npx supabase link --project-ref [project-ref]`
   - If user doesn't have a Supabase project yet:
   ```
   MANUAL STEP: Create Supabase project
   Go to supabase.com/dashboard → New Project → Choose region closest to your users
   → Copy the project reference ID and give it to me.
   ```
5. Push local migrations to production: `npx supabase db push`
6. Verify tables exist: `npx supabase db dump --schema public --data-only | head -20`

### Neon

1. Check for Neon connection string in env files
2. If using Prisma: `npx prisma db push` (for quick deploy) or `npx prisma migrate deploy` (if migrations exist)
3. If using Drizzle: `npx drizzle-kit push`

### No database detected
Skip this step. Not all MVPs need a database on day one.

## Step 3: Auth for Production

### Clerk

1. Check for `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` in env files
2. Tell user:
   ```
   MANUAL STEP: Get production Clerk keys
   Go to clerk.com/dashboard → Your app → API Keys → Copy the production keys
   (NOT the development keys — they're different).
   Give me: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY
   ```
3. Once received, add to hosting environment variables (Step 5)

### Supabase Auth

Already configured if Step 2 completed. Verify:
- `NEXT_PUBLIC_SUPABASE_URL` points to production
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` is the production key

### Auth.js / NextAuth

1. Generate production secret: `openssl rand -base64 32`
2. Set `NEXTAUTH_SECRET` to this value
3. Set `NEXTAUTH_URL` to the production URL (from Step 1)
4. For OAuth providers (Google, GitHub), tell user:
   ```
   MANUAL STEP: Update OAuth redirect URLs
   Go to [provider] developer console → Your OAuth app → Add redirect URL:
   https://[your-domain]/api/auth/callback/[provider]
   ```

### No auth detected
Skip this step.

## Step 4: Environment Variables

This is where most deploys break. The skill must be thorough here.

1. Find all env files: `.env`, `.env.local`, `.env.example`, `.env.production`
2. Find all `process.env.*` and `import.meta.env.*` references in code
3. Cross-reference: flag any variable referenced in code but missing from env files
4. Categorize each variable:
   - **Auto-set**: Values the skill can generate or already knows (NEXTAUTH_SECRET, database URL from Step 2)
   - **From provider**: Values the user gets from a dashboard (Clerk keys, Stripe keys)
   - **Custom**: Values specific to the project that the user must provide

5. Set variables on the hosting platform:

For Vercel:
```bash
npx vercel env add VARIABLE_NAME production
```

For Railway:
```bash
railway variables set VARIABLE_NAME=value
```

6. Present a checklist to the user:
```
Environment Variables Status:
✅ DATABASE_URL — set from Supabase production
✅ NEXTAUTH_SECRET — generated and set
⏳ CLERK_SECRET_KEY — waiting for user (see Step 3)
⏳ STRIPE_SECRET_KEY — waiting for user (manual step)
❌ NEXT_PUBLIC_APP_URL — needs production URL (set after first deploy)
```

Do NOT proceed to deploy until all required variables are set or explicitly deferred.

## Step 5: Deploy

Once hosting is configured, database is connected, auth keys are set, and env variables are in place:

### Vercel
```bash
npx vercel --prod
```

### Railway
```bash
railway up
```

Capture the deployment URL from the CLI output.

## Step 6: Verify

Run the verification script:
```bash
bash {baseDir}/scripts/verify_deploy.sh [deployment-url]
```

This checks:
- URL responds with 200
- No redirect loops
- Key pages load (/, /login or /sign-in if auth exists, main app route)
- No mixed content warnings (HTTP resources on HTTPS page)

If verification fails, read the error output and fix. Common issues:
- Missing env variable → check Step 4 checklist
- Database connection refused → check database URL and IP allowlisting
- Auth redirect broken → check callback URLs (Step 3)
- Build fails → check build logs: `npx vercel logs [url]` or `railway logs`

## Step 7: Domain (Manual — with Guidance)

After deploy succeeds on the default URL (*.vercel.app or *.up.railway.app):

```
MANUAL STEP: Connect a custom domain

If you already own a domain:
1. Go to your hosting dashboard → Domains → Add [yourdomain.com]
2. Go to your domain registrar (Namecheap, Cloudflare, etc.)
3. Update DNS:
   - For Vercel: Add CNAME record → cname.vercel-dns.com
   - For Railway: Add CNAME record → [provided by Railway]
4. Wait 5-30 minutes for DNS propagation
5. Tell me the domain and I'll update your environment variables

If you don't own a domain yet:
- Cloudflare Registrar: cloudflare.com/products/registrar (cheapest, includes free DNS)
- Namecheap: namecheap.com (wide selection, easy UI)
- Buy the domain, then follow step 1-4 above.

Reminder: Your app already works on the default URL. The domain is cosmetic 
for now. Don't let domain setup block you from sharing the live link.
```

After domain is connected, update:
- `NEXT_PUBLIC_APP_URL` or equivalent env variable
- Auth callback URLs if using OAuth
- Any hardcoded URLs in the codebase (search for the old *.vercel.app URL)

## Step 8: Generate Deploy Checklist

Copy `assets/deploy-checklist.md` to the project (e.g., `/docs/deploy-checklist.md`). Fill in the results:

```markdown
# Deploy Status

## Hosting
- Provider: [Vercel/Railway]
- URL: [production URL]
- Custom domain: [domain or "not configured yet"]

## Database
- Provider: [Supabase/Neon/none]
- Migrations applied: [yes/no]

## Auth
- Provider: [Clerk/Supabase Auth/Auth.js/none]
- Production keys set: [yes/no]
- OAuth callbacks updated: [yes/no/N/A]

## Environment Variables
[paste the checklist from Step 4]

## Verification
- Homepage loads: [yes/no]
- Auth flow works: [yes/no/N/A]
- Database connected: [yes/no/N/A]
- Custom domain live: [yes/no/not configured]
```

Save and present to the user. This becomes the reference for future deploys and debugging.

## Important Principles

- Always use CLI tools over dashboard UIs when possible. CLIs are faster, scriptable, and the agent can run them directly.
- Flag manual steps clearly with the `MANUAL STEP:` prefix. Never pretend the agent can do something that requires browser authentication or credit card entry.
- Don't block on optional steps. Domain setup is optional — the app works on the default URL. Payment provider setup is optional — that's Issue 08. Deploy what you can now.
- If a step fails, diagnose before retrying. Read error messages. Check env variables. Don't retry blindly.
- The goal is LIVE, not PERFECT. A working deployment on a *.vercel.app URL with no custom domain is infinitely better than localhost. Ship now, polish later.
