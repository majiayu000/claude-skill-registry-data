---
name: add-aspire
description: Add Aspire (AppHost + ServiceDefaults orchestration) to this repo - checks/installs the Aspire CLI, scaffolds via aspire init or aspire new, verifies the AppHost runs, and updates CLAUDE.md commands. Aspire is polyglot (.NET, Node.js, Python, Go officially; Java/Rust/PowerShell via community toolkit). Invoked from onboarding when the user opts in, or directly at any time.
argument-hint: "[optional: solution/path to wire up, defaults to repo root]"
---

# Add Aspire to this repo

Aspire is polyglot — the AppHost can be C# or TypeScript, orchestrating .NET,
Node.js, Python, and Go apps (official) plus Java, Rust, and PowerShell (community
toolkit), alongside containers, databases, caches, and queues. See
https://aspire.dev/languages-and-runtimes/ for the current matrix — check it
rather than assuming a stack is unsupported.

## Step 1 — CLI preflight

- Run `aspire -v`. It prints the installed version; report it.
- If the command fails (not installed), install the CLI:
  `npm install -g @microsoft/aspire-cli` (check `npm -v` exists first; if there is
  no Node on the machine, ask the user how they want to install the Aspire CLI
  instead of guessing). Re-run `aspire -v` to confirm and report the version.
- Scaffold ONLY through the CLI — never hand-write AppHost/ServiceDefaults files
  from memory. The CLI resolves current template + package versions, which is
  exactly hard rule 4 (versions are resolved, never recalled).

## Step 2 — Scaffold

- **AppHost language:** C# for .NET-centric repos, TypeScript for Node.js/frontend
  workspaces. Mixed repo → ask the user which the team prefers to maintain.
- **Existing apps/services:** `aspire init` from the repo root — wires an AppHost
  (+ ServiceDefaults for .NET) around what exists. Register each app with the
  matching resource type (project resources for .NET; npm/Python/Go app resources
  for the rest) — existing apps are orchestrated as-is, never rewritten.
- **Greenfield (no code yet):** `aspire new` and pick the template matching the
  stack decided at onboarding.
- **Integrations** (database, cache, queue — detected or planned): add them with
  `aspire add <integration>`, not by hand-adding packages.

## Step 3 — Verify

- The repo's build must still pass (`dotnet build`, `npm run build`, `go build` —
  whatever the stack's Commands table says).
- `aspire run` — confirm the AppHost starts, the dashboard URL appears, and each
  registered app shows up as a resource; then stop it. Do not report success on a
  scaffold that was never run.

## Step 4 — Record

- CLAUDE.md Commands table: set Run dev to `aspire run` (only after the verify
  step above proved it works).
- Outside onboarding, record the orchestration decision via `/decide` (alternatives:
  docker-compose, manual multi-app launch scripts).
- New canonical shape (e.g. how a service registers with the AppHost)? Apply the
  `/gotcha` admission test before adding an exemplar row.
