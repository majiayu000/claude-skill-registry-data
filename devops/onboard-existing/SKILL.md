---
name: onboard-existing
description: Detection-driven setup of the agentic template for an existing codebase. Infers stack, commands, and conventions from source, mines git history and legacy docs for ADRs and gotchas, and asks the user only what cannot be inferred.
user-invocable: true
disable-model-invocation: true
argument-hint: "[optional: path to repo root, defaults to cwd]"
---

# Onboard an EXISTING repository

Golden rule: **every fact you write must be verified against the code in this
session.** Detection first, questions second, guesses never. If migrating from a
legacy agentic layer (old CLAUDE.md, expertise YAMLs, decisions.md), treat those
files as *candidate claims to verify*, not as truth — they are a known drift source.

## Step 1 — Detect (parallel `scout` subagents for large repos)

Fan the detection below out to parallel `scout` subagents (`.claude/agents/scout.md`
— cheap tier, read-only) rather than reading everything in the main session; keep
the interpretation of what they find here.

1. **Stack & commands:** package.json scripts / Makefile / *.csproj / *.slnx /
   pyproject.toml, CI config, Dockerfile. Candidate commands for the CLAUDE.md
   table come from here. Also detect whether Aspire is already in use — a C# or
   TypeScript AppHost, `Aspire.Hosting.*` package references, or `@aspire/*` /
   aspire CLI config in the workspace.
2. **Test & lint setup:** test framework, lint/format config, coverage tooling,
   git hooks (lefthook/husky), CI quality gates → values for quality-gates.yaml.
3. **Branch policy:** CI rules per branch, server-side protections if visible,
   existing hook configs → protected-branches list.
4. **Conventions in practice:** sample 5–10 recently-touched source files. Identify
   the repeated shapes (feature structure, naming, error handling) and pick the
   best CURRENT exemplar file for each shape — prefer files touched recently by
   humans over old ones.
5. **History mining:** `git log --oneline -100` + merged MR titles. Look for
   decision-shaped events (library swaps, architecture changes, "use X not Y"
   commits) and incident-shaped events (revert/hotfix clusters) → ADR and gotcha
   candidates.
6. **Legacy docs (if present):** old CLAUDE.md / .agentic / README claims. For each
   claim: verify against code → carries over (with fresh evidence path), gets
   corrected, or gets dropped. List the drops explicitly in the final report.
7. **Platform & tooling:** `git remote -v` + which CI file exists → hosting
   platform (GitHub / GitLab / Azure DevOps). Ticket-key patterns in branch names
   and commit messages → backlog candidate (`PROJ-123` → Jira, `AB#123` → Azure
   Boards, bare `#123` with a GitHub remote → GitHub Issues). Observability config
   in code → monitoring candidate (App Insights connection strings, OTEL exporters,
   Prometheus annotations in manifests/Helm charts, Serilog sinks, Grafana
   dashboards, monitoring resources in Bicep/Terraform). Repo signals only — no
   live `az`/`kubectl` calls at this stage.

## Step 2 — Verify commands

Actually run (or at minimum `--help`/dry-run) every command before it enters
CLAUDE.md. A failing command gets fixed or excluded — never written down broken.

## Step 3 — Ask only the unanswerable (AskUserQuestion)

Typically: the *why* behind detected decisions (code shows WHAT was chosen, rarely
why); which detected conventions are intentional vs. accidental; disputed or
ambiguous detections; anything for "Repo-specific notes" (external quirks,
consumers). Present decision candidates from step 1.5 as a checklist — the user
confirms which deserve ADRs and supplies rationale.

**Platform & tooling:** present the step-1.7 candidates (hosting platform, backlog
tool, monitoring) for confirmation in the same round — only ask about what detection
actually surfaced; don't ask "which monitoring solution?" cold. For each confirmed
tool with a row in `.agentic/mcp-servers.md`, ask whether the user wants that MCP
server (they install it themselves — see step 4). If the repo carries no
observability signal but the user says the service is monitored (e.g. it runs on
AKS), offer a live read-only inspection (`az` / `kubectl`) as an explicit opt-in
fallback — facts learned that way have no repo evidence path, so they go into
"Repo-specific notes" or a gotcha only after the user confirms them, never as bare
cluster facts.

**(Repos without Aspire)** also ask: add Aspire for local orchestration? It's
polyglot — .NET, Node.js, Python, Go officially, more via community toolkit
(https://aspire.dev/languages-and-runtimes/) — and most useful when several
services/resources run together locally. On yes, `/add-aspire` runs in step 4.

## Step 4 — Write

- Fill every `<!-- onboard:... -->` marker in CLAUDE.md AND in `.claude/skills/`
  (e.g. `execute-plan` mr-command). CLAUDE.md stays ≤120 lines; overflow becomes
  gotchas/ADRs. Set `branches.protected` in `.agentic/quality-gates.yaml` from the
  branch-policy detections — the agent hook and lefthook read the list from there
  (single source; do not edit branch names anywhere else). Fill the rest of
  quality-gates.yaml, DELETING any gate no detected tool can measure (the
  SonarQube-only ones are marked); delete each `onboard:` comment line as it is
  consumed.
- **Optional skills:** check `.agentic/optional-skills/README.md` against what was
  detected (SonarQube config → `sonar`; Jira MCP / ticket-keyed branches → `jira-implement`).
  For each match, COPY the folder into `.claude/skills/` and fill its markers.
  Skills left in the library stay inactive — do not delete them.
- If a deploy pipeline was detected in CI config, offer to generate a repo-specific
  `/deploy` skill from it (real job names, real environments — never placeholder).
- **MCP servers:** for each tool confirmed in step 3, copy the matching install
  command from `.agentic/mcp-servers.md` into the final report for the user to run
  themselves (`--scope user`). NEVER write `.mcp.json`, tokens, or MCP server
  config into the repo. Use the confirmed platform to fill platform-dependent
  markers (e.g. the `execute-plan` mr-command: `glab` / `gh` / `az repos`) and to
  pick CI wiring — the template's CI snippets are GitLab-flavored; translate them
  to the detected platform's syntax rather than wiring them verbatim.
- **Stack addenda — .NET:** verify Central Package Management is in place
  (`Directory.Packages.props` + `ManagePackageVersionsCentrally`); offer to migrate
  if not — the latest-stable policy needs one place where versions live. Wire
  `.agentic/ci/dotnet-package-freshness.gitlab-ci.yml` into the repo's CI includes
  and recommend a Renovate bot for ongoing updates. If `dotnet --version` is SDK
  10+, activate `spike-dotnet` from the optional-skills library (copy into
  `.claude/skills/`) — it teaches runtime validation via file-based apps.
  **Non-.NET:** delete that CI file and offer the stack's equivalent (e.g.
  `npm audit` job + lockfile policy).
- **Aspire:** if the user opted in during step 3, invoke the `/add-aspire` skill
  now — it handles CLI install, scaffolding, and verification for any supported
  stack. If Aspire was already detected in step 1, just verify `aspire run` (or
  the AppHost launch profile) and put it in the Commands table.
- `gotchas.md`: real exemplar table (each row verified to exist) + constraint
  entries with `evidence:` path and today's `verified:` date. Delete the EXAMPLE
  entries.
- One ADR per confirmed decision, dated to when it actually happened if known
  from git history (absolute dates). Chain `supersedes:` where history shows a
  reversal.

## Step 5 — Audit and finish

- Activate the human-side git hooks: `lefthook install` (verify with
  `ls .git/hooks/pre-push`). Add lefthook as a dev dependency where the stack has a
  package manifest so teammates get it on install; otherwise note the manual step
  in the project README.
- If the template's own README.md was copied into this repo, delete it (it documents
  the template, not this project) after salvaging anything still relevant.
- Run `node .agentic/scripts/check-doc-paths.mjs` — must pass.
- Run the `/audit-docs` procedure over everything just written (self-check: does
  each claim still hold against code you actually read this session?).
- Confirm no `onboard:` markers remain: `grep -rn "onboard:" CLAUDE.md .claude/skills/ .agentic/ lefthook.yml | grep -v optional-skills`
  (markers inside `.agentic/optional-skills/` are filled on activation, not at
  onboarding; every other marker — including YAML comment markers — is deleted
  when consumed).
- Report: what was detected vs. asked, dropped legacy claims (with reasons), and
  any `TODO`s left for the team.
