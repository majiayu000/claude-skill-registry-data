---
name: onboard-new
description: Interview-driven setup of the agentic template for a greenfield repository. Asks the user for stack, commands, rules, and gates, then fills every onboard marker and seeds the first ADRs.
user-invocable: true
disable-model-invocation: true
argument-hint: "[optional: one-line project description]"
---

# Onboard a NEW (greenfield) repository

You are configuring this repo's agentic layer from scratch. There is little or no
source code yet, so the user is the source of truth — interview them, don't guess.

## Step 1 — Interview (use AskUserQuestion; batch related questions)

Round 1 — identity & stack:
1. Project name and one-line purpose (who is it for?).
2. Tech stack (language, framework, DB, package manager). Offer options based on
   sibling repos if this repo lives in a workspace.
3. Protected branches (default: main + develop) and branching model.

Round 2 — workflow:
4. Planned commands for install / run / test / lint / type-check / migrate
   (accept "not decided yet" — write `TODO` and note it).
5. Quality gates: accept the template defaults in `.agentic/quality-gates.yaml`
   or adjust? Which coverage tooling?
6. Any non-negotiable rules beyond branch protection (max 3–4)? Any external
   systems or consumers worth a "Repo-specific notes" line?
7. Hosting platform (GitHub / GitLab / Azure DevOps), backlog tool (Jira / Azure
   Boards / GitHub Issues / none yet), and monitoring stack (Application Insights /
   Grafana / Sentry / none yet). These fill platform-dependent markers (e.g. the
   `execute-plan` mr-command) and drive MCP-server recommendations from
   `.agentic/mcp-servers.md` in step 2. There is no code to detect from yet, so
   ask all three outright; "not decided" is a fine answer.
8. Add Aspire for local orchestration? It's polyglot — .NET, Node.js, Python, Go
   officially, more via community toolkit (https://aspire.dev/languages-and-runtimes/).
   Most useful when the app has several services/resources to coordinate. On yes,
   `/add-aspire` runs in step 2.

Round 3 — first decisions:
9. Why this stack over the alternatives they considered? (This becomes ADR-0001 —
   push gently for real alternatives and reasons; "team knows it" is a valid reason.)
10. Any other decisions already made (auth approach, hosting, API style)? Each
    becomes its own ADR.

## Step 2 — Fill the template

- Replace every `<!-- onboard:... -->` marker in `CLAUDE.md` AND in `.claude/skills/`
  (e.g. `execute-plan` mr-command). Delete markers that end up empty (e.g. no extra
  hard rules). Keep CLAUDE.md under ~120 lines — if an answer is long, it's an ADR
  or a gotcha, not CLAUDE.md.
- **Optional skills:** ask which apply (see `.agentic/optional-skills/README.md` —
  SonarQube? Jira?). For each, COPY its folder into `.claude/skills/` and fill its
  markers. Skills left in the library stay inactive — do not delete them.
- Set `branches.protected` in `.agentic/quality-gates.yaml` to match answer 3 —
  the agent hook and lefthook both read the list from there (single source; do not
  edit branch names anywhere else).
- Update `.agentic/quality-gates.yaml` (gates + `coverage_tooling`). DELETE any gate
  no tool in this repo can measure (the SonarQube-only ones are marked) — a gate that
  can only be estimated must not exist. Delete each `onboard:` comment line in the
  file as it is consumed.
- If the user opted into Aspire (question 8), invoke the `/add-aspire` skill now —
  it handles CLI install, scaffolding, and verification for any supported stack.
- **MCP servers:** from the question-7 answers, copy the matching install commands
  from `.agentic/mcp-servers.md` into the final report for the user to run
  themselves (`--scope user`). NEVER write `.mcp.json`, tokens, or MCP server
  config into the repo. If the backlog answer was Jira, also activate
  `jira-implement` from the optional-skills library.
- **Stack addenda — .NET:** set up Central Package Management from the start
  (`Directory.Packages.props`, `ManagePackageVersionsCentrally=true`) and keep
  `.agentic/ci/dotnet-package-freshness.gitlab-ci.yml` wired into CI; recommend a
  Renovate bot for ongoing updates. If `dotnet --version` is SDK 10+, activate
  `spike-dotnet` from the optional-skills library (copy into `.claude/skills/`) —
  it teaches runtime validation via file-based apps. **Non-.NET:** delete that CI
  file and offer the stack's equivalent (e.g. `npm audit` job + lockfile policy).
- Replace the EXAMPLE entries in `.agentic/gotchas.md` with real ones if any
  emerged from the interview; otherwise leave the file with only its header and an
  empty Exemplars table (delete the examples — never ship placeholder facts).
- Seed `.agentic/decisions/0001-*.md` (stack choice) and one ADR per additional
  decision from question 10, using `0000-adr-template.md` — including the Aspire
  yes/no if the topic came up (a "no" with real alternatives is also a decision).
  Today's date, `status: accepted`.

## Step 3 — Verify and finish

- Any command the user said already works: run it to confirm before writing it
  into CLAUDE.md. Commands that don't exist yet stay `TODO`.
- Activate the human-side git hooks: `lefthook install` (verify with
  `ls .git/hooks/pre-push`). Add lefthook as a dev dependency where the stack has a
  package manifest so teammates get it on install; otherwise note the manual step
  in the project README.
- If the template's own README.md was copied into this repo, delete it (it documents
  the template) and make sure the project has a real README of its own.
- Run `node .agentic/scripts/check-doc-paths.mjs` — must pass.
- Confirm `grep -rn "onboard:" CLAUDE.md .claude/skills/ .agentic/ lefthook.yml | grep -v optional-skills`
  returns nothing (optional-skills markers are filled on activation; every other
  marker — including YAML comment markers — is deleted when consumed).
- Report: what was configured, which items are `TODO`, and remind the user to run
  `/onboard-existing` later to harvest exemplars once real code exists.
