---
name: dev
description: Start, stop or troubleshoot the local development stack. Use when the user wants to run the app, see it in the browser, turn on optional services (AI, file uploads, billing), or when a local service or app fails to start.
---

# Local development

- `bun dev` runs the core profile: Postgres (localhost:55432), Valkey (:56379) and
  Mailpit in Docker, plus web (http://localhost:3000), api (http://localhost:3001) and
  the worker (:3002), notifications (:3003) and webhooks (:3004) services, all in turbo's
  terminal UI.
- `bun dev:full` adds every optional service: the Python AI service (:8000), S3 storage
  (RustFS on :59000, console http://localhost:59001), ClamAV (:53310), the Expo bundler
  and the email previews (http://localhost:3030). Uploads stay off until
  `bun run env:set S3_BUCKET=uploads`.
  Billing without a Stripe account: `bun run stripe:fake` (see the Billing block in
  .env.example).
- Customer webhooks can point at a local receiver on 127.0.0.1 (allowed by
  WEBHOOK_ALLOWED_PRIVATE_ADDRESSES in .env; refused in production). For real Stripe
  test events, run `stripe listen --forward-to localhost:3004/webhooks/stripe` (the
  webhooks service's `WEBHOOKS_PORT`) and set
  the printed secret with `bun run env:set STRIPE_WEBHOOK_SECRET=whsec_...`.
- Emails never leave the machine: open Mailpit at http://localhost:58025 to read sign-up
  codes, notifications and texts (SMS_PROVIDER=email delivers them there too).
- Every port, the services' and the apps', comes from `.env` (`POSTGRES_PORT`,
  `WEB_PORT`, `API_PORT`, …; the numbers above are `.env.example`'s defaults); if one is
  taken, see the setup skill.

`bun dev` and `bun dev:full` are long-running terminal UIs: in an agent session, start
them with the Bash tool's `run_in_background` and read their output from there, never
in the foreground (the call would hang until its timeout). On a first `dev:full`, ClamAV
starts in the background while it downloads its virus signatures (several minutes):
uploads stay pending until then.

## Several branches at once

`wt switch --create <branch>` (Worktrunk, `.config/wt.toml`) makes a worktree next to
this checkout, copies `.env`, installs and generates; `wt switch <branch>` moves between
them and `wt list` shows each one's state. They all use this machine's Docker services
(docker-compose.yml names the project), so tests and builds run side by side. To run
`bun dev` or `bun run test:e2e` in two at once, give one its own stack first:
`bun run setup --stack 1` moves its services and apps 100 ports up (web on 3100, api on
3101, ...; docs/environment.md). `wt remove`
(which asks first) deletes a worktree and its merged branch. Without Worktrunk
(`bun run doctor` says so), `brew install worktrunk && wt config shell install`.

## Troubleshooting

1. `bun run doctor`. It lists the exact fix for tools, `.env` drift and services.
2. Service logs: `docker compose logs <postgres|valkey|mailpit|rustfs|clamav> --tail 100`.
3. App logs are in the turbo UI. Every request has an `x-request-id`; search logs by it
   (the debug skill has the rest).
4. After changing the Prisma schema, Pydantic models or the API contract, run `bun run gen`.
5. Stale state: `bun run db:down` then `bun dev` (keeps data). Wiping data
   (`bun run docker:clean`, which deletes every container, volume and image this repo
   created) needs the user's confirmation: the Bash guard asks before it runs.
6. Uploads stay pending after the stack has run for hours: the local ClamAV stopped
   answering (the worker logs `clamd timed out`). `docker compose restart clamav`.
7. A port is taken: `lsof -nP -iTCP:<port> -sTCP:LISTEN`, then the setup skill.
