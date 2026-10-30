---
name: architecture-ci-setup
description: >
  Set up CI/CD for an architecture and connect the service (dev) repositories built from it: in
  the architecture repository the six GitHub Actions workflows (gates, release, handoff, index,
  escalations, Tier 0) from the plugin's templates with the plugin's pin, the RUN-team policy, the labels and the
  repository's variables, secrets and settings; in a service repository the binding
  (.architecture.json), the architecture MCP server for the IDE (.mcp.json) and, for an unattended
  build, the build and merge workflows, and on either kind the workflow that answers @alia with the architecture. Checks first, writes after the user's yes, never sets a
  secret itself. Use for "set up architecture CI", "connect a service repo to the architecture",
  "configure the architecture MCP in this repo", "set up the unattended build".
triggers:
  - set up architecture ci
  - set up the architecture ci/cd
  - architecture ci setup
  - check the architecture workflows
  - upgrade the architecture workflows
  - connect a service repository
  - connect this repo to the architecture
  - configure the architecture mcp
  - set up alia in this repo
  - set up the unattended build
  - set up @alia with the architecture
---

# Architecture CI Setup

One script, `scripts/ci-setup.js`, checks a repository and writes what is missing. This skill runs it, asks before every write, and hands the user the commands for what only they can set. Every write follows the confirm-first rule: what changes, then the user's yes, then the write.

## Steps

1. **Resolve `plugin_dir`**: `bun ~/.claude/plugins/marketplaces/shadowx4fox-solution-architect-marketplace/scripts/plugin-root.ts --plugin sa-delivery`.
2. **Which side.** A directory with `ARCHITECTURE.md` is the **architecture** repository. One with `.architecture.json`, or a code repository the user names as a service, is a **service** repository. When a request covers both ("connect the service to the architecture"), do the architecture first. If it is unclear, ask.
3. **Check.** Run it read-only and show its output verbatim:
   - architecture: `bun [plugin_dir]/skills/architecture-ci-setup/scripts/ci-setup.js architecture <root> [--runner <labels>]`
   - service: `bun [plugin_dir]/skills/architecture-ci-setup/scripts/ci-setup.js service <dir> --architecture <owner/repo> [--project <key>] [--component <slug>] [--server <mcp_url>] [--attended [--review]] [--merge --tests "<name>"] [--agent <login>] [--mention] [--runs-on self-hosted,<label>]`

   A service is always checked with `--architecture`: the pair is configured on both sides in one run.

   `✓` is done, `✗` is to do, `!` needs a decision, and `·` is optional.
4. **Ask what the report cannot know**, with `AskUserQuestion`, only for the rows that need it:
   - **Runner** (architecture): can a GitHub-hosted runner reach the MCP server? If it is on localhost or a private network, the index jobs run on a self-hosted runner: `--runner self-hosted,<label>`.
   - **RUN team** (architecture, only when the user wants Tier 0): `support.js <root> --declare run`. Then ask which kinds the repository may key for a trusted build agent, a multi-select of the four or none: `support.js <root> --declare-auto <kinds>|none`. Both write `.sa-skills/project.json`, which is a reviewed change like any other.
   - **Service binding**: the project key (the architecture's `SA_INDEX_PROJECT_KEY`), the component (its slug: `get_architecture` on the server, or `component-cli.ts list` in the architecture), and the server URL.
   - **Who builds it**: a person in an IDE (`--attended`), or an unattended build (the default). If attended, ask whether a reviewer holds the team's pull requests to the pack (`--review`). That adds `architecture-review.yml`: code checks plus Claude's review against the pack, a required status check on the default branch, enforced for admins too. A departure merges only when the pull request cites an open `[ESC-…]` issue covering it. Ask where it runs (`--runs-on`) when the server is on localhost or a private network. If unattended, ask:
     - whether its pull requests may merge without a person (`--merge`, the service team's policy), and which workflow runs the tests (`--tests`, its `name:`). `--merge` is full auto: the report then requires the architecture's `SA_HANDOFF_AUTOMERGE` and the agent in its `SA_TIER0_TRUSTED_AGENTS`, the architecture team's two settings, so say so in the question;
     - the build agent's login (`--agent`): the identity of `SA_BUILD_TOKEN`, a machine user or a GitHub App's `name[bot]`;
     - where the build runs, when the server is on localhost or a private network (`--runs-on self-hosted,<label>`). The report checks that a runner with those labels is registered and online on the service repository.
   - **@alia** (either kind): should `@alia` in an issue or pull request ask for a change with the architecture (`--mention`)? That adds `architecture-mention.yml`: claude-code-action's mention mode on its own phrase, with the MCP server and the component's BUILD.md as standing rules. Claude keeps the contracts and puts an escalation `preview_escalation` renders in its reply instead of departing. Only the owner, members and collaborators start it. A person merges its `alia/` branch; on an attended service, `--review` holds it to the pack. A stock `claude.yml` may stay: `@claude` there answers without the architecture, and the report says so (`·`).
5. **Write.** List the files the run will write and the variables it will set on each repository, and get the user's yes. Then run the same command with `--write --settings`. `--settings` sets every required (`✗`) variable whose value is known, on both repositories, and reports each as `— set`; it never sets a secret.
   - A workflow marked `!` differs from its template: it has changes of its own, or it came from an older template. Show `diff <file> <template>`, and replace it (`--replace <file>`) only for the files the user names.
   - The workflows reach the repository through a branch and a pull request, never a push to the default branch. Ask before pushing.
6. **What only the user sets.** The report prints a command for each row. Give the commands to the user, in order:
   - **Variables**: set by `--settings` (step 5); a row still `✗` lacks its value, so ask for it and run again.
   - **Secrets**: the user sets them in the prompt (`! gh secret set NAME -R <repo>`). Never ask for a secret's value in the chat.
   - **`CLAUDE_CODE_OAUTH_TOKEN`**: from `/install-github-app`, on that repository.
   - **Labels**: `escalate.js labels <root> --create`, after a yes.
   - **The workflow permission**: the `gh api -X PUT …` command, after a yes.
7. **Check again**, and report what is still open.

For a service repository with `.mcp.json` written, the developer approves the server once in Claude Code (`/mcp`). An unattended build also needs its identity, `SA_BUILD_TOKEN` (a machine user or a GitHub App), listed in the architecture's `SA_TIER0_TRUSTED_AGENTS` for every Tier 0 request it may write without a person.

## The pair, end to end

How a release finds the service: the handoff names no service. `architecture-index.yml` sends `architecture-released` to every repository listed in the architecture's `SA_SERVICE_REPOS`, and each one builds the component its `.architecture.json` names. A service whose pack did not change opens no pull request. Attaching a service adds it to that list.

| Architecture repository | Service repository |
|---|---|
| — | `architecture-review.yml` (attended, `--review`) holds every pull request to the pack: `review-check.js` checks the contract copies, the commits and the binding, Claude judges the diff against BUILD.md's rules, and code decides; an open `[ESC-…]` issue the pull request cites is the only way past a departure, and it holds the pull request (status `pending`) until the architect answers |
| `architecture-escalations.yml` dispatches `architecture-escalation-closed` to `SA_SERVICE_REPOS` when an `[ESC-…]` issue closes, is transferred or deleted, or is retitled away from `[ESC-…]` | `architecture-review.yml`'s `recheck` job fails the status of an open pull request held on that escalation (also hourly, as a fallback — a schedule GitHub disabled after 60 days without activity is a ✗ row, `--settings` enables it). An attended service with `--review` is listed in `SA_SERVICE_REPOS` for this |
| `architecture-handoff.yml` regenerates the kit after a release and, with `SA_HANDOFF_AUTOMERGE=true`, merges it once its gates pass and dispatches the index | — |
| `architecture-index.yml` publishes a release's build packs and dispatches `architecture-released` to `SA_SERVICE_REPOS` (`SA_DISPATCH_TOKEN`) | `architecture-build.yml` builds from the pack, unattended, and opens a pull request (`SA_BUILD_TOKEN`) |
| `architecture-tier0.yml` keys the build's request for a kind in `tier0.auto`, and a move to `Resolved` waits for the pull request it cites | `architecture-build-merge.yml` merges the build's pull request once the tests pass (opt in) |
| — | `architecture-mention.yml` (`--mention`, either kind) answers `@alia` with the MCP server and BUILD.md; a person merges its work (`SA_MENTION_RUNS_ON`) |

Escalations stay with the architect: nothing in this pair answers one. Reference: `docs/RUN_TEAMS.md`.

## Permissions

`Bash(bun *)`, `Bash(gh *)`, `Write(.github/workflows/*)`, `Write(.architecture.json)`, `Write(.mcp.json)`.
