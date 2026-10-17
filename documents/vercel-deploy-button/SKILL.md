---
$schema: https://gist.githubusercontent.com/remorses/9f3737a6f516c01f4bdb612045c64072/raw/agent-skill.schema.json
name: vercel-deploy-button
repo: https://github.com/remorses/holocron
description: >
  Vercel Deploy Button for one-click project deployment from a Git template.
  Covers all URL parameters, environment variable pre-filling, redirect
  callbacks, deploy hooks, demo cards, integrations, and the pattern for
  associating a deployed GitHub repo with your own backend resource via
  pre-filled env vars and Vercel system env vars. Load this skill when
  adding a "Deploy with Vercel" button, customizing deploy button URLs,
  or building a deploy-from-template flow that connects back to your API.
---

# Vercel Deploy Button

One-click deploy flow. Users click a button, Vercel clones a Git repo
into their GitHub/GitLab/Bitbucket, deploys it, and optionally redirects
back to your app with metadata about the created project.

## The button

Markdown:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FOWNER%2FREPO)
```

HTML:

```html
<a href="https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FOWNER%2FREPO">
  <img src="https://vercel.com/button" alt="Deploy with Vercel"/>
</a>
```

## What the button does

1. User clicks the link
2. Vercel shows the Project creation flow
3. User picks their GitHub/GitLab/Bitbucket account
4. Vercel **clones** the source repo into the user's account as a new repo
5. User fills in env vars (if required), picks project/repo name
6. Vercel builds and deploys
7. If `redirect-url` is set, user is redirected to your app with callback params

## URL parameters — complete reference

Base URL: `https://vercel.com/new/clone`

All parameter values must be URI-encoded.

### Source parameters

- **`repository-url`** (string, **required**) — the Git repo to clone. Can include a subdirectory path (e.g. `.../tree/main/examples/hello-world`). The user cannot change this; it is fixed by the link author.
- **`project-name`** (string) — default Vercel project name. User can change it. Not guaranteed to stick if a project with that name already exists.
- **`repository-name`** (string) — default name for the new Git repo created in the user's account. No spaces.
- **`stores`** (string) — JSON array of store configs to auto-provision during deployment. Supports Vercel Blob stores and Marketplace integration stores. See [stores section](#stores) below.

### Environment variable parameters

- **`env`** (comma-separated strings) — list of required env var keys. User must fill in values before deploying. **You cannot pass values via this param** (URL is in browser history, insecure).
- **`envDefaults`** (URI-encoded JSON object) — non-sensitive default values for env vars. Keys must also appear in `env`. Pre-populates the form. **Never use for secrets, API keys, tokens, or passwords.**
- **`envDescription`** (string) — short description shown next to the env var inputs. Only displayed if `env` is set.
- **`envLink`** (string) — URL to docs explaining what values to enter. Only displayed if `env` is set. Point to specific docs, not top-level.

### Callback parameters

- **`redirect-url`** (string) — URL to send the user to after successful deployment. Vercel appends callback query params to this URL. See [callback params](#callback-parameters-returned-by-vercel) below.
- **`developer-id`** (string) — Vercel Integration Client ID. Shows your logo and name on the redirect UI. Requires `redirect-url`. The Integration's website field must match the redirect URL.
- **`external-id`** (string) — your own arbitrary ID passed through the flow. Relayed to the redirect URL of each required Integration. Requires `integration-ids`.
- **`production-deploy-hook`** (string) — name of a Deploy Hook to create. When set alongside `redirect-url`, the callback includes `production-deploy-hook-url` you can use to trigger redeployments (useful for headless CMS content changes).

### Integration parameters

- **`integration-ids`** (comma-separated strings) — Vercel Integration IDs the user must install before deploying. Max 3. Find IDs in the Integrations Developer Console.
- **`skippable-integrations`** (number) — if present, integrations become optional (user picks one or skips). They should all serve the same purpose (e.g. competing error trackers).

### Demo card parameters

All four are required for the demo card to appear:

- **`demo-title`** (string) — title of the example deployment
- **`demo-description`** (string) — description text
- **`demo-url`** (string) — link to a live example
- **`demo-image`** (string) — screenshot URL

### Stores

The `stores` param accepts a JSON array. Two store types:

**Blob store:**

```json
[{ "type": "blob", "access": "private" }]
```

Properties: `type` (required, `"blob"`), `access` (`"public"` or `"private"`), `envVarPrefix` (custom prefix for env vars like `MYBLOG_BLOB_READ_WRITE_TOKEN`).

**Integration store:**

```json
[{
  "type": "integration",
  "integrationSlug": "neon",
  "productSlug": "postgres",
  "protocol": "storage"
}]
```

Properties: `type` (required, `"integration"`), `integrationSlug`, `productSlug` (both required), `protocol`, `envVarPrefix`, `allowConnectExistingProduct` (boolean).

Encode with `encodeURIComponent(JSON.stringify([...]))` before putting in URL.

## Callback parameters returned by Vercel

When `redirect-url` is set, Vercel redirects the user after deploy and appends these query params:

- **`project-dashboard-url`** — Vercel dashboard URL for the created project
- **`project-name`** — name of the created project
- **`deployment-dashboard-url`** — Vercel dashboard URL for the deployment
- **`deployment-url`** — live deployment URL (the `*.vercel.app` domain)
- **`repository-url`** — the new Git repo URL in the user's account
- **`production-deploy-hook-url`** — Deploy Hook URL (only if `production-deploy-hook` was set)

## Vercel system environment variables

Vercel auto-populates these at **both build time and runtime** (must be enabled in project settings). These are available in the deployed app without you setting them.

Git-related vars (the important ones for association):

- **`VERCEL_GIT_PROVIDER`** — `github`, `gitlab`, or `bitbucket`
- **`VERCEL_GIT_REPO_SLUG`** — repo name, e.g. `my-docs`
- **`VERCEL_GIT_REPO_OWNER`** — account/org that owns the repo, e.g. `acme-corp`
- **`VERCEL_GIT_REPO_ID`** — numeric GitHub repo ID, e.g. `117716146`
- **`VERCEL_GIT_COMMIT_REF`** — branch name
- **`VERCEL_GIT_COMMIT_SHA`** — commit hash
- **`VERCEL_GIT_COMMIT_AUTHOR_LOGIN`** — GitHub username of the committer

Deployment-related vars:

- **`VERCEL`** — always `1` when system env vars are enabled
- **`VERCEL_ENV`** — `production`, `preview`, or `development`
- **`VERCEL_URL`** — deployment domain without protocol (e.g. `my-site.vercel.app`)
- **`VERCEL_PROJECT_PRODUCTION_URL`** — shortest production custom domain, or `*.vercel.app`
- **`VERCEL_DEPLOYMENT_ID`** — unique deployment ID
- **`VERCEL_PROJECT_ID`** — unique project ID
- **`VERCEL_REGION`** — runtime region (e.g. `cdg1`)

## Associating a deployed repo with your backend resource

This is the key pattern for SaaS products that deploy a template for
users and need to link that deployment back to a user/org in their
own database.

### The problem

User clicks your deploy button, Vercel creates a repo + deployment in
the user's account. You need to know: which user deployed it, which
repo was created, and which resource (org, project, workspace) in your
system it belongs to.

### The solution: pre-filled env var + redirect callback

**Step 1: Generate a per-user deploy URL on your dashboard.**

Your backend knows the user's org ID. Generate the deploy button URL
with `envDefaults` pre-filling it:

```typescript
const orgId = currentUser.orgId
const deployUrl = new URL('https://vercel.com/new/clone')
deployUrl.searchParams.set('repository-url', 'https://github.com/yourco/template')
deployUrl.searchParams.set('env', 'YOUR_ORG_ID')
deployUrl.searchParams.set('envDefaults', JSON.stringify({ YOUR_ORG_ID: orgId }))
deployUrl.searchParams.set('envDescription', 'Your org ID (pre-filled, do not change)')
deployUrl.searchParams.set('redirect-url', 'https://yourapp.com/deploy/callback')
deployUrl.searchParams.set('project-name', 'my-docs')
deployUrl.searchParams.set('production-deploy-hook', 'content-update')
```

The user sees `YOUR_ORG_ID` pre-filled with their actual org ID. They
can technically change it, but the UX discourages it.

**Step 2: Handle the redirect callback.**

After the user deploys, Vercel redirects to your callback URL with
query params:

```typescript
// GET https://yourapp.com/deploy/callback?repository-url=...&deployment-url=...&project-name=...

app.get('/deploy/callback', async (req) => {
  const repoUrl = req.query['repository-url']     // https://github.com/user/my-docs
  const deploymentUrl = req.query['deployment-url'] // https://my-docs-xyz.vercel.app
  const projectName = req.query['project-name']
  const deployHookUrl = req.query['production-deploy-hook-url']

  // Parse GitHub owner/repo from the repo URL
  const match = repoUrl.match(/github\.com\/([^/]+)\/([^/]+)/)
  const [, owner, repo] = match

  // Create your internal project record
  await db.insert(projects).values({
    userId: currentUser.id,         // from session cookie
    githubOwner: owner,
    githubRepo: repo,
    vercelDeploymentUrl: deploymentUrl,
    vercelDeployHookUrl: deployHookUrl,
  })

  return redirect('/dashboard/projects')
})
```

**Step 3: At runtime, the deployed app reads both your env var and Vercel's system vars.**

The template app can phone home on first request or during build:

```typescript
// In the deployed template app (runs on Vercel)
const orgId = process.env.YOUR_ORG_ID
const repoOwner = process.env.VERCEL_GIT_REPO_OWNER
const repoSlug = process.env.VERCEL_GIT_REPO_SLUG
const repoId = process.env.VERCEL_GIT_REPO_ID
const gitProvider = process.env.VERCEL_GIT_PROVIDER

// Phone home to associate this deployment
await fetch('https://yourapp.com/api/deployments/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    orgId,
    repoOwner,
    repoSlug,
    repoId,
    gitProvider,
    deploymentUrl: process.env.VERCEL_URL,
    projectId: process.env.VERCEL_PROJECT_ID,
  }),
})
```

This gives you **two independent association paths:**

1. **Redirect callback** (immediate, from the user's browser) — gives you `repository-url` and `deployment-url` before the app even boots
2. **Runtime phone-home** (from the deployed app) — confirms the deployment is live and sends `VERCEL_GIT_REPO_OWNER`, `VERCEL_GIT_REPO_ID`, and your pre-filled `YOUR_ORG_ID`

Use the redirect callback as the primary signal. The runtime phone-home
is a backup confirmation.

### Triggering redeployments from your backend

If you set `production-deploy-hook`, the callback includes
`production-deploy-hook-url`. Use it to trigger redeployments when
content changes (e.g. headless CMS, config update):

```typescript
// Redeploy the user's project
await fetch(project.vercelDeployHookUrl, { method: 'POST' })
```

## Limitations

- **No inline files.** Source must be a real public Git repo. You cannot pass file contents in the URL.
- **No branch selection.** Always clones the default branch of the source repo.
- **`envDefaults` are visible in the URL.** Never put secrets there. The URL is saved in browser history.
- **`env` values cannot be passed in the URL.** User must type them in.
- **`repository-url` is fixed.** The user cannot choose a different source repo.
- **`project-name` is a suggestion.** If it already exists, Vercel asks the user to pick a new name.
- **No callback on failure.** `redirect-url` only fires on successful deployment.

## Resources

- Deploy Button overview: https://vercel.com/docs/deploy-button
- Source parameters: https://vercel.com/docs/deploy-button/source
- Callback parameters: https://vercel.com/docs/deploy-button/callback
- Environment variables: https://vercel.com/docs/deploy-button/environment-variables
- Integrations: https://vercel.com/docs/deploy-button/integrations
- Demo card: https://vercel.com/docs/deploy-button/demo
- System environment variables: https://vercel.com/docs/environment-variables/system-environment-variables
- Deploy Hooks: https://vercel.com/docs/deploy-hooks
- Vercel Integrations Console: https://vercel.com/dashboard/integrations/console
