---
name: ship-setup
description: Set up where the product runs — staging and production — for people who have never deployed anything. Writes docs/deploy.md, a step-by-step guide with a checklist per environment, does every step that doesn't need the user's credentials or money (Fly.io apps and config, GitHub environments with production approval, deploy tokens piped straight into GitHub secrets), walks the user through the rest (accounts, logins, payment, their own API keys), and verifies each step for real. Use when the user says "setup", "infra", "infraestructura", "configurá staging", "prepará producción", "deploy guide", "guía de despliegue", "dónde lo publico", after project-new's skeleton, before the first ship-release, or when the dashboard shows an environment not ready.
---

# Ship setup — environments a founder can own

Only for projects the profile marks `hosted`. A library, CLI or plugin isn't deployed: say so, and
point at `/keelokit:ship-release`, which publishes it.

The stack deploys the API to Fly.io (staging from every green `main`, production from a tag with
REL-1) and the web and site to any static host. Environments and owners are in
`docs/context/environments.md`. This skill turns that into working environments and keeps the
proof in `docs/deploy.md`.

**Never** type, print or commit a credential. The user's accounts, logins, card and third-party
API keys are theirs: give them the exact command or screen, and wait. Creating something that costs
money (a Fly app with Postgres, a paid plan, a domain) needs a clear yes first, with the price if
known. Random secrets the app itself needs (a JWT secret) can be generated in place without being
shown: `fly secrets set JWT_SECRET="$(openssl rand -hex 32)" --config …`.

## 1. The guide

Write (or update) `docs/deploy.md`, in the user's language, one section per environment, each a
checklist the dashboard reads (`- [x]` done and verified, `- [ ]` pending), with who owns each
step. Plain words first, the command after:

```markdown
# Deploy

## staging
Where the team tries every change before users see it. Updates itself on every green main.
- [x] Fly.io account — owner: Ana · verified 2026-10-02
- [ ] Logged in on this computer — run `fly auth login` (opens the browser)
- [ ] API app and its database — `fly launch --no-deploy --config apps/api/fly.staging.toml` (about USD 5/month)
- [ ] API settings — every key of the README's API configuration block, set with `fly secrets set`
- [ ] GitHub can deploy it — a deploy token saved as the `staging` environment's `FLY_API_TOKEN`
- [ ] First deploy green, `https://<app>.fly.dev/health` answers 200
- [ ] Web app published — <static host>, pointing at the staging API

## production
Where users are. Only a tagged version gets here, and only after a person approves it.
- [ ] …the same steps with `fly.production.toml`…
- [ ] GitHub environment `production` requires a reviewer (the approval of REL-1)
- [ ] Domain and HTTPS · error reports (Sentry DSN) · database backups on
```

## 2. Do what can be done

In order, stopping at the first step that needs the user; after each, tick it only once verified:

| Step | Who | How it's verified |
|---|---|---|
| Accounts (GitHub, Fly.io, static host, Sentry, domain) | user | the login below works |
| `gh auth login`, `fly auth login` | user, in their terminal | `gh auth status`, `fly auth whoami` |
| Fly apps + Postgres from the template's `fly.*.toml` | Claude, after a yes (it costs) | `fly status --config …` |
| App config that isn't secret, generated app secrets | Claude | `fly secrets list --config …` shows the names |
| Third-party keys (payments, mail, WhatsApp…) | user types them into `fly secrets set` | same, names only |
| GitHub environments `staging` and `production`; required reviewer on `production` | Claude, via `gh api -X PUT repos/<owner>/<repo>/environments/<env>` | `gh api repos/<owner>/<repo>/environments` |
| Deploy tokens | Claude pipes `fly tokens create deploy --config …` into `gh secret set FLY_API_TOKEN --env <env>`, never printing it | `gh secret list --env <env>` |
| First deploy | CI on the next green `main` (staging) or `/keelokit:ship-release` (production) | the run is green; `curl -fsS <url>/health` |
| Domain, HTTPS | user at their registrar; Claude gives the exact DNS records (`fly certs add`) | `fly certs check`, `curl -I https://<domain>` |
| Backups, error reports | Claude enables, user owns the account | `fly postgres backup list`, a test event in Sentry |

A step that fails is left unticked with what went wrong and the next thing to try.

## 3. Close

Update the URLs in `docs/context/environments.md`, close the "staging not configured" gap if
it was open, commit `docs: deploy setup (<env>)`, and refresh the dashboard: its Environments panel
shows each checklist. Report what is ready, what waits for the user and the cost per month so far.
