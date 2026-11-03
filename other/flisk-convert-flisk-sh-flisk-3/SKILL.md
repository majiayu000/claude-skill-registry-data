---
name: flisk-convert
description: Convert any existing app (Node, Python, Go, Rust, Bun, a static site, a Docker Compose or Procfile project, a monorepo) to run with Flisk, so `flisk up` starts it locally. Picks the right path (local processes, bring-your-own container, or `flisk import`), writes the `service.json` files with the CLI, and checks every URL. Use when the user says "convert this app to Flisk", "run this with Flisk", "add Flisk to this repo" or "move my Compose setup to Flisk". For a new app from a plain request, use flisk-build.
license: MIT
compatibility: Requires the flisk CLI and the app's own runtime. Docker and Tilt only for the container paths. Does not deploy.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Convert an app to Flisk

Take an app that already exists and make `flisk up` start it. Change as little as possible: keep the app's code, its Compose file, Tiltfile and Helm charts. Flisk only adds `service.json` files and a `.flisk/` folder.

## 0. Whose repo is it?

Your own repo, or one the user owns: go on. **Someone else's repo: check its size first** (`gh repo view OWNER/REPO --json stargazerCount -q .stargazerCount`). More than 500 stars means no pull request from us, ever: a maintainer of a large org blocked us for one (2026-11-02). Do not open it, and do not push a branch to a fork "for later". You may still convert a local clone to try Flisk, if the user asks; tell them it stays local. At 500 stars or fewer, follow the repo's CONTRIBUTING, disclose that you are a Flisk maintainer using an AI assistant, and open an issue or discussion before a large change.

## 1. Look before you change

Work on a branch. Read the repo and list the parts that start together: websites, APIs, workers, agents, databases. For each part note the start command, the port it listens on, and an HTTP path that answers 200 when it is healthy. Run `git status` so you can see what Flisk adds later.

## 2. Pick one path per project

A database or cache can run in Docker next to `command` services: give it an `image` (no `command`, no `dockerfile`) and `flisk up` starts it with `docker run` (a mixed run, docs/run-without-docker.md). Any other mix, such as a service built from a Dockerfile next to a `command` service, is refused with `MIXED_RUNTIME`.

| The app | Path |
| --- | --- |
| Every part starts with one command and needs no database or Docker image | **A. Local processes**: a `command` in each `service.json` |
| A part needs Postgres, Redis or another image, one gateway URL, or the container it deploys | **B. Containers**: `flisk resource <name> --type bring-your-own` (a Dockerfile or an `--image`), the others as normal Flisk resources |
| It already has a `docker-compose.yml`, a `Procfile` or several Dockerfiles | **C. Import**: `flisk import <path>` reads them and writes the resources (needs `npx`), then check each result by hand |

Prefer A when it fits: nothing to install but Flisk and the app's runtime.

## 3. Convert

**A. Local processes.** In each part's folder write `service.json` with `schemaVersion: 1`, `appName` (kebab-case), `appType` (`frontend`, `backend`, `worker`, `mcp`, `agent`), `command`, `port` and `healthCheckPath`. Add `dependsOn` for start order and `env` for URLs between parts. The command runs from that folder and must read `PORT` from the environment. Then run `flisk up --dry-run`.

**B. Containers.** From the repo root run `flisk project --yes`. Wrap each existing part:

```bash
flisk resource <name> --type bring-your-own --stack <stack> --dockerfile ./Dockerfile --port <port> --health-path /health --yes
```

Use `--image <name>` instead of `--dockerfile` for a ready-made image, `--register-existing` for a folder that already has a `service.json`, and `--restart no` for a one-shot job. The container must listen on the port in `service.json`, bind to `0.0.0.0` and answer 200 on the health path. New parts that Flisk can scaffold use `flisk resource <name> --type backend|frontend|worker|agent|mcp`.

**C. Import.** Run `flisk import <path>`, read every generated `service.json`, and fix ports and health paths by hand.

## 4. Check and start

1. `flisk doctor`, then `flisk up --dry-run` (or `flisk up <stack> --dry-run`). Fix what they report.
2. `flisk up` (or `flisk up <stack>`). It prints the URLs.
3. `flisk status` and open each URL. A part is done only when its URL answers.
4. If something is red, read `flisk logs --service <name>` and use the flisk-troubleshoot skill.
5. Stop with `flisk down`.

## 5. Prove it on a real run (for a PR to someone else's repo)

A dry run and a green CI check are not evidence. Before asking a maintainer to merge, run the converted stack for real and show it. The reference is the self-review on [biolend83/tubehaus#42](https://github.com/biolend83/tubehaus/pull/42#issuecomment-6556357152), which was merged:

- **Start it for real** with the released Flisk the docs name (`flisk up`, not only `--dry-run`), with the values a user would set in `.env`. Use a throwaway project name or fresh volumes so an older test's data (an old database password) cannot fake a failure or a pass, and remove those volumes afterwards. On Colima, run from under `$HOME`: bind mounts from `/tmp` arrive empty.
- **Show the app working**, not just containers up: screenshots of the main page, one real action (a search, a video playing, a login page), and numbers where you can read them (a player's `currentTime`, an HTTP status).
- **Show Flisk's side**: the end of the `flisk up` output, the Tilt UI with every resource green, and the logs of the service you changed.
- **Trace each setting you migrated end to end**: `.env` → `service.json` → the generated Compose file → what Docker actually did (`docker inspect`, `docker ps`). For ports, test from the outside too: loopback answers, the machine's LAN address does not (or does, if that is what Compose did).
- **Put the raw text under each screenshot** (a collapsible block per log), mask anything private (egress IPs, keys), and keep the files.
- **Read logs, not badges**: a `continue-on-error` CI step is green even when it fails.
- **Review your own diff in a comment** before the maintainer does: what you checked, what you fixed after reviewing (with commits), behaviour changes they should know about, what belongs to Flisk and not to their repo (link the Flisk issue), and what you did not verify (other OS or architecture, a second machine).
- **Offer Flisk as an option**: keep their Compose file as the main way unless they ask otherwise, reuse the same Docker volume names so no data is copied, and disclose that you work on Flisk and that an AI assistant was used.
- **Every gap you hit is a Flisk bug**: fix it in Flisk (or file it) instead of working around it in their repo.

## Guardrails

- Never delete or rewrite the app's Compose file, Tiltfile or charts. Flisk does not replace them.
- Do not hand-write Dockerfiles or Compose files for Flisk; use `flisk resource`. Hand-written `service.json` is fine only for path A.
- A database migration runs in its own `migrator` resource, not in the API's start script.
- Do not commit `.env` or secrets. Ask before changing an existing port, rename, or removing a start script.
- Report what was added (`git status`), the URLs, and what was not converted or not tested.
