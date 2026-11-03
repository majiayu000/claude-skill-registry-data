---
name: flisk-recipe-saas
description: Recipe for "build me a SaaS with login and billing" with Flisk - a web app, an accounts API with a database for sign-up and login, and a billing API, in one stack started with `flisk up`. Use with the flisk-build skill when the user asks for a SaaS, a members area, subscriptions, sign-up or payments.
license: MIT
compatibility: Requires the flisk CLI, Docker and Tilt on the local machine. Does not deploy.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Recipe: a SaaS with login and billing

**Parts:** a web app, an accounts API (sign-up, login, sessions), and a billing API (plans and subscriptions). Both APIs store data in the stack's Postgres.

## Steps

```bash
flisk doctor
flisk project --yes
flisk resource web --type frontend --stack saas --yes
flisk resource accounts-api --type backend --stack saas --feature drizzle --yes
flisk resource billing-api --type backend --stack saas --feature drizzle --yes
flisk up saas --dry-run
flisk up saas --json &        # wait for {"ok":true}
flisk networks --stack saas --raw
```

## App code

- `accounts-api`: `POST /signup`, `POST /login`, `GET /me`. Hash passwords (`Bun.password.hash`). Sign session tokens with `JWT_SECRET`, which Flisk generates into the project `.env` and passes to the container. Do not invent a new secret file.
- `billing-api`: `GET /plans`, `POST /subscribe`, `GET /subscription`. Verify the caller's token with the same `JWT_SECRET`.
- Payments: without the user's test keys, record subscriptions in the database and say that no real payment provider is connected. If the user gives a provider's **test** key, list its name under `secrets.required` in `services/saas/billing-api/service.json` and put the value in the project `.env`, never in code.
- `web`: sign-up and login forms, a plans page, and a "your plan" page.

## Done when

Each answers 200: the `web` health URL, `/api/accounts/health`, `/api/accounts/health/db`, `/api/billing/health` and `/api/billing/health/db` on `api.<project>.localhost:<port>`. Also sign up and log in once with `curl` and show the user it worked.

Then tell the user the web app URL, the two API URLs, that payments are not connected to a real provider (unless they are), and that `flisk down` stops everything.
