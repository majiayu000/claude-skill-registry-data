---
name: senternet-site-firebase
description: Set up Firebase Hosting (Vite track) or Firebase App Hosting (Next.js track) — custom domains, project IDs, headers, and deploy scripts.
---

# Firebase Hosting Setup

Add Firebase Hosting to a Vite + React site with optimal caching, security headers, custom domain handoff, and multi-environment deployment. Can be run on a fresh project or re-run later to add a missing environment or finish domain setup.

**Which product to set up depends on the site's framework track** (see `/senternet-site-framework`):

- `vite` → **Firebase Hosting** (static CDN). Follow the steps below as written.
- `nextjs` → **Firebase App Hosting** (SSR on Cloud Run). Steps 1–5 (CLI, prefix, environments, project creation) apply as written; then jump to the **Next.js track: App Hosting** section at the end instead of steps 6–9.

Detect the track from `.site-framework.json` before starting.

## Prerequisites

Run `/senternet-site-gcloud-auth` first if you haven't authenticated this machine yet.
Project creation only works when both `gcloud` and `firebase` are logged into the Google account that owns the target projects.
When you run project-specific `gcloud` or `firebase` commands in this workflow, always include `--project` with the exact project ID you are modifying. The auth/list commands are account-scoped exceptions.

## Steps

### 1. Install Firebase CLI if not present

```bash
which firebase || npm install -g firebase-tools
```

### 2. Derive and confirm the Firebase project prefix

Derive a prefix from the site name (lowercase, hyphens, strip trailing `-site`):
```bash
# e.g. site name "myapp-site" → prefix "myapp"
# e.g. site name "my-marketing-site" → prefix "my-marketing"
# e.g. site name "myapp" → prefix "myapp"
```

Show the user the derived prefix and ask them to confirm or override it before proceeding. This prefix is used as `$PREFIX-dev` and `$PREFIX-prod` for Firebase project IDs. The Firebase project display name must always match the project ID exactly.

Also derive the canonical public host from the site domain when available. Default to `www.DOMAIN.com` as the primary host and `DOMAIN.com` as the apex that redirects to `www.DOMAIN.com` unless the user explicitly prefers the apex as canonical.

### 3. Determine which environments to set up

Check if `.firebaserc` already exists:
```bash
cat .firebaserc 2>/dev/null
```

**If `.firebaserc` does not exist** — ask the user which environments to create:
- Dev only (`$PREFIX-dev`)
- Prod only (`$PREFIX-prod`)
- Both dev and prod

**If `.firebaserc` already exists** — read it to determine which environments are already configured. Only ask about creating the missing one(s). If both are already present, confirm the config looks correct and exit.

### 4. Check which Firebase projects already exist

```bash
firebase projects:list 2>/dev/null | grep "$PREFIX"
```

Note which of `$PREFIX-dev` and `$PREFIX-prod` already exist so you don't try to recreate them.
If `firebase projects:list` fails with an auth error or returns nothing because the CLI session expired, try `firebase login --reauth` first and then run `firebase projects:list` again. If that succeeds, continue. If it still fails, run `/senternet-site-gcloud-auth` and follow the Firebase reauth prompts there before continuing.

### 5. Create Firebase projects for selected environments

For **prod** (if it doesn't already exist):
```bash
firebase projects:create $PREFIX-prod --display-name "$PREFIX-prod"
```
Immediately confirm it shows up in `firebase projects:list`. If it does not, stop and report the failure instead of assuming the project was created.

For **dev** (if selected and doesn't already exist) — ask the user whether to create it or skip creation (e.g. they'll create it manually or it already exists under a different account):
```bash
# Only run if user confirms they want to create it
firebase projects:create $PREFIX-dev --display-name "$PREFIX-dev"
```
Immediately confirm it shows up in `firebase projects:list`. If it does not, stop and report the failure instead of assuming the project was created.

If creation fails with "project ID already taken", check if the user owns it via `firebase projects:list`. If they do, proceed — the project exists and we'll just reference it. If they don't own it, ask them to choose a different prefix.
If creation fails because the Firebase session expired, run `firebase login --reauth`, re-run `firebase projects:list`, and only retry project creation after the reauth succeeds.

After the Firebase project exists, create or verify the Firebase web app for the Hosting project and capture its config automatically with the Firebase CLI:
```bash
firebase apps:create web --display-name "APP_NAME" --project PROJECT_ID
firebase apps:sdkconfig web FIREBASE_APP_ID --project PROJECT_ID
```

If you are creating a new Hosting site, associate the existing web app at creation time:
```bash
firebase hosting:sites:create SITE_ID --app FIREBASE_APP_ID
```

If the Hosting site already exists and the CLI cannot attach the web app to it, stop and tell the user exactly which Firebase Console step is still required to connect the web app to the Hosting site.

Use the returned config values to populate the repo’s Firebase configuration files or handoff artifact as needed. Do not ask the user to copy config values manually unless the CLI cannot print them.

### 6. Write `firebase.json`

Only write if it doesn't already exist (re-run should not overwrite):

```json
{
  "hosting": {
    "public": "build",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "**", "destination": "/index.html" }
    ],
    "cleanUrls": true,
    "trailingSlash": false,
    "headers": [
      {
        "source": "**/*.@(js|css|webp|png|jpg|jpeg|svg|woff2|woff|ico)",
        "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }]
      },
      {
        "source": "**/*.@(html|json)",
        "headers": [{ "key": "Cache-Control", "value": "public, max-age=3600, must-revalidate" }]
      },
      {
        "source": "**",
        "headers": [
          { "key": "X-Content-Type-Options", "value": "nosniff" },
          { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
          { "key": "X-XSS-Protection", "value": "1; mode=block" },
          { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
        ]
      }
    ]
  }
}
```

### 7. Write `.firebaserc`

Write only the environments that have been set up (now or previously):

**Both environments:**
```json
{
  "projects": {
    "default": "$PREFIX-prod",
    "dev": "$PREFIX-dev",
    "prod": "$PREFIX-prod"
  }
}
```

**Prod only:**
```json
{
  "projects": {
    "default": "$PREFIX-prod",
    "prod": "$PREFIX-prod"
  }
}
```

**Dev only:**
```json
{
  "projects": {
    "default": "$PREFIX-dev",
    "dev": "$PREFIX-dev"
  }
}
```

### 8. Add deploy scripts to `package.json`

`deploy:prod` is always required. `deploy:dev` is only added if a dev environment was set up. On re-run, add the new script without touching existing ones.

**Prod deploy script** (always add):
```json
"deploy:prod": "npm run build:prod && firebase deploy --only hosting --project \"$PREFIX-prod\" && node scripts/indexnow.mjs"
```

**Dev deploy script** (only if dev environment was set up):
```json
"deploy:dev": "npm run build:dev && firebase deploy --only hosting --project \"$PREFIX-dev\""
```

Note: The `&& node scripts/indexnow.mjs` tail on `deploy:prod` is only added if `scripts/indexnow.mjs` exists. Skip it otherwise.

### 9. Set up the custom domain handoff

This step is for the canonical public domain and should be re-runnable without breaking an existing setup.

**Detection:**
- `.firebase-domain.json` exists and `status` is `connected` for the requested apex/canonical pair → skip this step
- `.firebase-domain.json` exists but `status` is `pending-dns` or the requested domains changed → patch the file and continue with the handoff
- `.firebase-domain.json` does not exist → create it as part of the handoff

**If DNS or ACME validation is still propagating, do not stop the workflow here.**
Instead, set the domain state to `pending-dns`, explain that Firebase may need time to verify the records and issue SSL, and offer to continue with the next available setup steps while waiting. Those next steps can include:
- deploying hosting to the Firebase project
- finishing SEO files or deploy scripts that do not depend on the domain being live
- returning later to re-check the DNS and certificate status

When you come back later, re-open the Firebase domain flow and verify the records and SSL status before marking the domain `connected`.

**Default domain policy:**
- Primary host: `www.DOMAIN.com`
- Apex host: `DOMAIN.com`
- Redirect: `DOMAIN.com` redirects to `www.DOMAIN.com`

**Do the Firebase console setup on behalf of the user as far as possible:**
- Open the Firebase Hosting domain flow for the production site
- Add `www.DOMAIN.com` as the main custom domain
- Add `DOMAIN.com` as the redirecting apex domain
- Keep the redirect-to-secondary-domain option enabled so the apex forwards to `www`
- Do not guess DNS values; mirror the exact record types and targets Firebase displays
- Capture the DNS records Firebase displays and translate them into the user’s DNS provider terminology
- If the provider already has records pointing elsewhere for the same host, tell the user to remove or replace those records before verification

**Write `.firebase-domain.json` in the target site root** so upfit mode can detect a completed setup on later runs:

```json
{
  "apexDomain": "DOMAIN.com",
  "canonicalHost": "www.DOMAIN.com",
  "redirectApexToCanonical": true,
  "status": "pending-dns"
}
```

If the user later confirms the domain is connected and SSL is issued, update `status` to `connected` instead of creating a second file.

## Notes

- `cleanUrls: true` removes `.html` extensions from URLs
- `trailingSlash: false` canonicalizes `/page/` to `/page`
- The 1-year immutable cache on assets works because Vite hashes filenames on every build
- HTML gets a 1hr cache so deploys propagate quickly without users seeing stale pages
- Security headers (`X-Frame-Options`, etc.) satisfy Lighthouse Best Practices checks
- If the app later adds Firebase Functions, update `firebase.json` to include a `functions` key and change `deploy:prod` to `firebase deploy --only hosting,functions`
- When the custom domain is connected, use `https://www.DOMAIN.com` everywhere in canonical URLs, robots.txt, sitemap generation, and share/meta tags

---

## Next.js track: App Hosting

Use this section instead of steps 6–9 when `.site-framework.json` says `"framework": "nextjs"`. Steps 1–5 above (Firebase CLI, prefix derivation, environment selection, project creation) still apply unchanged.

App Hosting is a different product from Hosting: it builds your repo with Cloud Build and serves it from Cloud Run, so it deploys from a **connected git branch** rather than from a local `firebase deploy` of a build directory.

### N1. Confirm the repo has a GitHub remote

App Hosting cannot create a backend without one:

```bash
git remote -v
```

If there is no remote, run `/senternet-site-github-setup` first and push the branch. Do not create the backend against a repo that has no pushed commits.

### N2. Enable the required APIs

```bash
gcloud services enable \
  firebaseapphosting.googleapis.com \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  secretmanager.googleapis.com \
  --project "$PREFIX-prod"
```

Repeat for `$PREFIX-dev` if a dev environment was created.

### N2b. If the repo is a monorepo, set up Turborepo first

**App Hosting cannot build a workspaces repo on workspaces alone.** The builder resolves the app's dependencies through a supported monorepo tool — Nx or Turborepo ([Turborepo support shipped January 2026](https://firebase.blog/posts/2026/01/apphosting-turborepo/)) — and a root `package.json` with `"workspaces"` but no such tool fails at build time. This is the single most common surprise when moving an existing Next.js repo onto App Hosting.

Check before creating the backend:

```bash
node -e "console.log(require('./package.json').workspaces ?? 'no workspaces')"
ls turbo.json nx.json 2>/dev/null
```

- Workspaces present, no `turbo.json` or `nx.json` → add Turborepo now, following step 6b of `/senternet-site-nextjs-setup` (root `turbo.json`, `turbo` as a root devDependency, one lockfile at the repo root).
- No workspaces → skip this; a single-package repo needs nothing extra, and adding Turborepo to it buys nothing.

Then note the app's path relative to the repo root (e.g. `apps/site`) — the next step needs it as the root directory, and `apphosting.yaml` belongs in that directory rather than at the repo root.

### N3. Create the backend

```bash
firebase apphosting:backends:create --project "$PREFIX-prod" --location us-central1
```

This is an interactive flow: it asks for the GitHub repository to connect (authorizing the Firebase GitHub app the first time), the branch to deploy from (`main`), the backend ID, and the root directory. Use the site name as the backend ID and record it as `$BACKEND_ID`. For a monorepo, the root directory is the app's path (`apps/site`), not `/`.

For CLI deploys, record the same pairing in `firebase.json` so the command knows which app to push:

```json
{
  "apphosting": {
    "backendId": "my-site",
    "rootDir": "/apps/site",
    "ignore": ["node_modules", ".git", "firebase-debug.log"]
  }
}
```

`rootDir` is `/` for a single-package repo. This is the one thing `firebase.json` is still for on this track — headers are not read from it.

Confirm it exists before continuing:

```bash
firebase apphosting:backends:list --project "$PREFIX-prod"
```

If the CLI subcommand names have shifted, check `firebase apphosting --help` — this surface changes faster than the Hosting one. Never assume the backend was created; always verify with the list command.

For a dev environment, create a second backend on `$PREFIX-dev` connected to the same repo but a `dev` branch, and add `apphosting.dev.yaml` for its config overrides.

### N4. Confirm `apphosting.yaml`

`/senternet-site-nextjs-setup` writes this file. Verify it before the first rollout, because a variable missing here is `undefined` in production even though `.env.production` has it:

- Every browser-read variable is prefixed `NEXT_PUBLIC_` and lists `BUILD` in its `availability`
- `NEXT_PUBLIC_BASE_URL` matches the canonical host exactly (`https://www.DOMAIN.com`, no trailing slash)
- Secrets are `secret:` references, never `value:` literals

Create and grant secrets with:

```bash
firebase apphosting:secrets:set SECRET_NAME --project "$PREFIX-prod"
firebase apphosting:secrets:grantaccess SECRET_NAME --backend "$BACKEND_ID" --project "$PREFIX-prod"
```

### N5. Headers and caching

There is no `firebase.json` `headers` array on this track. The security headers and the immutable asset cache belong in `next.config.ts` under `async headers()` — see `/senternet-site-nextjs-setup` step 5. Next already sends `Cache-Control: public, max-age=31536000, immutable` for its own content-hashed output under `/_next/static`, so the `headers()` rules only need to cover hand-placed files in `public/`.

A `firebase.json` on this track holds the `apphosting` block from step N3 and nothing else. If it also has a `hosting` block, that is a leftover — leave it only if the repo genuinely also serves a static site; otherwise remove it so nobody deploys a stale static copy over the backend.

### N6. Deploy scripts

```json
"deploy:prod": "firebase apphosting:rollouts:create $BACKEND_ID --project \"$PREFIX-prod\" --git-branch main && node scripts/indexnow.mjs"
```

Pushing to the connected branch also triggers a rollout automatically — the script is for forcing one without a new commit. Wait for the rollout to report `READY` before running IndexNow; submitting URLs for a build that has not gone live yet just tells Bing to crawl the old pages.

### N7. Custom domain

The domain flow lives under the App Hosting backend, not under Hosting. The policy is identical to the Hosting track — `www.DOMAIN.com` canonical, apex redirecting to it — and the same `.firebase-domain.json` artifact is written so upfit runs can detect a completed setup:

```json
{
  "apexDomain": "DOMAIN.com",
  "canonicalHost": "www.DOMAIN.com",
  "redirectApexToCanonical": true,
  "status": "pending-dns",
  "host": "firebase-app-hosting",
  "backendId": "BACKEND_ID"
}
```

Add the domain to the backend, mirror the exact DNS records the console displays, and follow the same "do not stall on `pending-dns`" rule as the Hosting track: continue with other setup steps and re-check verification and SSL later.

### N8. Verify

```bash
firebase apphosting:backends:list --project "$PREFIX-prod"
curl -sI https://www.DOMAIN.com/ | head -20
curl -s https://www.DOMAIN.com/ | grep "<h1"
```

The last one is the check that matters: the deployed backend must return real page content to a client that runs no JavaScript.
