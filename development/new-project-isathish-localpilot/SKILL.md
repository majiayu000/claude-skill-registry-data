---
name: new-project
description: Bootstrap a brand-new project from an idea — choose a fitting stack, scaffold the folder structure and tooling, get a runnable hello-world slice working, verify it in the browser/terminal, and leave a plan for the next features. USE WHEN the workspace is empty or the user says "create a new app/project", "start from scratch", "scaffold", "set up a <framework> project", "build me a <thing>" with no existing code.
---

# New project

Goal: in one pass, a project that runs, has tests, lint and a README, and a todo plan the user can keep vibe-coding against.

## 1. Pin down the shape (fast)
- From the request derive: app type (static site · SPA · full-stack web · API · CLI · library · mobile · extension · script), language preference, must-have integrations (db, auth, payments, AI), target platform. Check the workspace for hints (existing files, `.tool-versions`, editor config) and the OS/shell from the environment.
- Ask at most ONE `ask_user` question, and only if the stack choice is genuinely open (e.g. "Next.js + Postgres, or Vite SPA + Express?"). Otherwise pick the mainstream default for the ecosystem and state it:
  - Web app/full-stack: Next.js (TS) or Vite + React (TS) + Express/Fastify; Python → FastAPI (+ HTMX or a Vite frontend); Go → net/http + templ; .NET → minimal API.
  - API only: Fastify/Hono (TS), FastAPI (Py), Gin/Echo (Go), Axum (Rust), ASP.NET minimal API.
  - CLI: Node (commander) · Python (typer) · Go (cobra) · Rust (clap).
  - Data/ML: Python + uv, notebooks under `notebooks/`, code under `src/`.
  - Use TypeScript over JS, a lockfile, and the ecosystem's standard formatter/linter.

## 2. Scaffold
- Prefer the official generator via `run_command` (`npm create vite@latest`, `npx create-next-app`, `uv init`, `cargo new`, `dotnet new webapi`, `go mod init`) with non-interactive flags; otherwise write the files yourself with `write_file`.
- Standard layout: `src/` (or framework convention) · `tests/` · `docs/` · `scripts/` · `.github/workflows/ci.yml` · `README.md` · `.gitignore` · `.env.example` · `.editorconfig`. Keep it flat until there is a reason to nest.
- Tooling: formatter + linter + typecheck + test runner wired into manifest scripts (`dev`, `build`, `test`, `lint`, `format`). A pre-configured `tasks.json`/`launch.json` when it helps the editor.
- Initialise git (`git init`, first commit) unless the folder is already a repo.

## 3. First vertical slice
- Implement one real, end-to-end feature from the idea (not just the template page): e.g. the main screen rendering real data from a local store, or the core CLI command working on sample input.
- Add one meaningful test and make the suite pass.
- Run it: `run_command` the dev server (background) or the CLI; for web, `browser_inspect` the URL to catch console/network errors and check layout, then `open_browser` so the user sees it.

## 4. Document & plan
- `README.md`: what it is, how to run/test/build, project layout, where config lives.
- `manage_todos`: the next 5–10 features in order (from the user's idea), each verifiable. Suggest running `requirements`/`design` for the bigger ones.
- `memory_save` the stack, commands and conventions chosen so later sessions start aligned.

## Rules
- Working software first; no placeholder "TODO" screens left in the slice you claim is done.
- Don't add services (db, auth, queues) before the first slice needs them; note them in the plan instead.
- Stay within the user's stated constraints (language, framework, hosting, budget) even if you'd choose differently.
