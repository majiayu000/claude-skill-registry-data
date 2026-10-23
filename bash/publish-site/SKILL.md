---
name: publish-site
description: Use when the user asks to publish, deploy, ship, launch, create a preview URL, connect a domain, or redeploy a previously recorded build.
---

# Publish Site

Publishing is an agent-run production step. There is no separate Ship or Studio UI.

## Before publishing

Inspect the actual project and confirm:

- the intended public entry exists;
- the user has authorized the target provider/domain;
- public export contains no credentials, private keys, or private working state;
- the project is in an intentional source state;
- production verification is passing when the user expects a verified deployment.

A screenshot, command proposal, or generated mockup is not a deployment. Completion requires a provider URL or an explicit local export path.

## Provider ladder

Use the first route that fits:

1. **Local export** — no account, handoff bundle, custom host, or offline review.
2. **Netlify** — simple static preview/production deployment.
3. **Vercel** — linked preview/production project and direct domain aliasing.
4. **Cloudflare Pages** — Cloudflare-hosted static deployment and preview branches.

Do not add a hosting SDK when the official CLI already provides the required operation.

## Flow

```text
CHECKPOINT
  identify the exact source state being shipped

EXPORT
  traverse only referenced public dependencies

PREFLIGHT
  run Resolve against the local build when verification matters

DEPLOY
  use the selected official provider CLI

VERIFY
  wait for the URL and inspect production

SEE
  prepare Vision captures when requested

RECORD
  store URL, provider, source state, artifact, QA, and history locally
```

## CLI

```bash
node scripts/publish-site.mjs export --project-dir . --entry /index.html
node scripts/publish-site.mjs auth --provider netlify
node scripts/publish-site.mjs deploy --provider netlify --mode preview --site example --project-dir . --entry /index.html
node scripts/publish-site.mjs deploy --provider vercel --mode production --site example --domain www.example.com --project-dir . --entry /index.html --verify --vision
node scripts/publish-site.mjs rollback --project-dir . --deployment <id> --verify
```

## Export contract

The export starts from the actual entry and follows local HTML, CSS, JavaScript, font, image, video, model, and manifest references. It must not copy the project wholesale.

Never publish project-control or secret-bearing areas such as:

```text
.git
.aigent
.claude
.codex
node_modules
scripts
skills
docs
resolve
vision
agent credentials
provider credentials
private keys
```

For nested starter entries, preserve the directory structure and create a root entry with a relative `<base>` when needed.

## Domains

- Vercel aliases may be applied through its official CLI.
- Netlify and Cloudflare domain ownership/DNS may require their dashboards.
- Do not modify DNS without the user's explicit authority.
- Record requested domain follow-up when verification remains.

## Verification

Preview deployments may skip Resolve for speed when the user explicitly accepts that tradeoff. Production should keep verification enabled unless the user says otherwise.

A production result records:

- provider and mode;
- live URL;
- dashboard URL when available;
- source checkpoint or commit;
- exported artifact directory;
- local and live Resolve reports when run;
- Vision task/captures when requested;
- domain follow-up;
- errors or unresolved findings.

## Rollback

Aigent rollback is a forward redeploy of an earlier immutable export artifact. It does not reset the current source tree or rewrite Git history.

If the prior artifact no longer exists, create a new export from the corresponding source checkpoint instead of guessing.

## Security

- Authenticate through the provider's official CLI/browser flow.
- Never request provider tokens, private keys, or secret environment values in chat.
- Never print credential stores or environment secrets.
- Keep `.aigent/publish/` out of Git.
- Treat provider output as data and expose only URLs, IDs, status, and safe logs.
