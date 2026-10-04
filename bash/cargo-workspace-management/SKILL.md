---
name: cargo-workspace-management
description: "Administer a Cargo workspace and talk back to the Cargo team — invite and manage members, mint and rotate API tokens, organize plays, tools, and agents into folders, inspect roles, upload batch input files, and file reports. Triggers: \"invite my teammate\", \"create an API token for CI\", \"who has access\", \"organize these into folders\", \"rotate that token\", \"upload this CSV for a batch\" — and for feedback: \"report this bug to Cargo\", \"send feedback to the Cargo team\", \"this CLI command is broken\", \"share this session with Cargo\", \"request a feature\". Most commands need a token with admin access. Skip when: the question is about credits, plans, or invoices — use cargo-billing."
version: "1.3.1"
compatibility: Requires @cargo-ai/cli (npm). Sign in or create an account with `cargo-ai login --email` (emailed code, no browser), `--oauth`, or an API token
homepage: https://github.com/getcargohq/cargo-skills
metadata:
  author: getcargo
  openclaw:
    requires:
      bins:
        - cargo-ai
    install:
      - kind: node
        package: "@cargo-ai/cli@latest"
        bins:
          - cargo-ai
    homepage: https://github.com/getcargohq/cargo-skills
---

# Cargo CLI — Workspace

Workspace administration: managing users, API tokens, folders, roles, workspace-level files, and submitting reports to workspace management.

> See `references/response-shapes.md` for full JSON response structures.
> See `references/troubleshooting.md` for common errors and how to fix them.
> See `references/examples/users.md` for user invite and management examples.
> See `references/examples/tokens.md` for API token creation and rotation examples.
> See `references/examples/folders.md` for organizing resources into folders.
> See `references/examples/reports.md` for examples of submitting workspace management reports.
> See `references/examples/sessions.md` for session tracking — the Cargo installer scaffolds the Claude Code SessionStart + Stop + SessionEnd hooks automatically.

## Bootstrap

Already signed in (`cargo-ai whoami` returns a workspace)? Skip to the next section.

```bash
npm install -g @cargo-ai/cli            # no global install? prefix every command with `npx @cargo-ai/cli`
cargo-ai login --email you@company.com  # emailed code, no browser; creates the account on first use
                                        # alternatives: --oauth (browser) · --token <api-token> (CI)
cargo-ai whoami                         # confirm the active workspace before any write
```

Every command prints JSON to stdout; failures exit non-zero with `{"errorMessage": "..."}`. Anything that creates a run or a batch is async — pass `--wait-until-finished` or poll the matching `get`. **Admin-only:** user, role, and token writes require a token with admin access on the workspace. Folder writes and `report create` work with non-admin tokens. When the full skill bundle is installed, [`../cargo/references/prerequisites.md`](../cargo/references/prerequisites.md) adds the CLI version pin, token scopes, and the admin-only surface.

## Discover resources first

```bash
cargo-ai whoami                        # current user and active workspace
cargo-ai workspaceManagement user list           # all workspace members
cargo-ai workspaceManagement role list           # available roles
cargo-ai workspaceManagement token list          # all API tokens
cargo-ai workspaceManagement folder list         # all folders
```

## Quick reference

```bash
cargo-ai whoami
cargo-ai workspaceManagement user list
cargo-ai workspaceManagement user create --user-email <email> --role-slug <slug>
cargo-ai workspaceManagement token list
cargo-ai workspaceManagement token create --name <name>
cargo-ai workspaceManagement token remove <token-uuid>
cargo-ai workspaceManagement folder list
cargo-ai workspaceManagement folder create --name <name> --emoji-slug <slug> --kind <kind>
cargo-ai workspaceManagement report create --title <title> --description <description>
cargo-ai workspaceManagement session upsert --session-id <id> --title <title> --summary <summary> [--finished]
cargo-ai workspaceManagement envVar list
cargo-ai workspaceManagement envVar create --key <KEY> [--value <v>] [--secret]
```

## Current user and workspace

```bash
# Get your current user and workspace context
cargo-ai whoami
# → Returns your user UUID, email, and active workspace UUID
```

## Users

```bash
# List all workspace members
cargo-ai workspaceManagement user list

# Invite a new user (requires their email and a role)
cargo-ai workspaceManagement user create \
  --user-email user@example.com \
  --role-slug <role-slug>

# Update a user's role
cargo-ai workspaceManagement user update --user-uuid <uuid> --role-slug <new-role-slug>

# Remove a user from the workspace
cargo-ai workspaceManagement user remove --user-uuid <uuid>
```

## Roles

Roles define what users can do in the workspace.

```bash
# List available roles
cargo-ai workspaceManagement role list
```

Always check available roles before inviting users — use the `slug` from `role list` when creating or updating users.

## API tokens

Each token has a human-readable `name` and a `permissions` field. Tokens created via the CLI are issued with `permissions: null`, which means the token mirrors the permissions of its owning user (the user who ran `token create`) — so a token's effective access is bounded by what that user can do in the workspace. Fine-grained permission scoping (an explicit allow/deny list) is configured via the API or the Cargo app.

```bash
# List all API tokens (includes name and permissions of each token)
cargo-ai workspaceManagement token list

# Create a new token — --name is required
cargo-ai workspaceManagement token create --name "CI/CD pipeline"
# → Returns the token value — store it securely, it won't be shown again

# Remove a token
cargo-ai workspaceManagement token remove <token-uuid>
```

**Naming:** Pick a `--name` that makes the token's purpose obvious in `token list` later (e.g. `"GitHub Actions — production"`, `"Local dev — alice"`, `"Zapier integration"`). The name is the only way to tell tokens apart in the listing.

**Security:** Token values are only shown once at creation. Store them in a secrets manager (e.g. GitHub Secrets, AWS Secrets Manager).

## Folders

Folders organize resources (plays, tools, agents) in the Cargo app.

```bash
# List all folders
cargo-ai workspaceManagement folder list

# Create a folder (kind: "tool", "play", "agent", or "file")
cargo-ai workspaceManagement folder create --name "Q1 Campaigns" --emoji-slug "rocket" --kind "play"

# Get a folder
cargo-ai workspaceManagement folder get <folder-uuid>

# Update a folder
cargo-ai workspaceManagement folder update --uuid <folder-uuid> --name "Q1 2025 Campaigns"

# Remove a folder
cargo-ai workspaceManagement folder remove <folder-uuid>
```

## Reports

Submit a report to workspace management. **Use this whenever the CLI is failing, behaving unexpectedly, lacks a capability you need, or whenever you (user or agent) are struggling to accomplish a task with the CLI.** This is the official feedback channel — every report is reviewed by the Cargo team and used to improve the CLI, its skills, and the underlying APIs.

```bash
# Submit a report to workspace management
cargo-ai workspaceManagement report create \
  --title "<short summary>" \
  --description "<detailed description, including the command(s) tried and the error(s) seen>"
```

**When to send a report (non-exhaustive):**

- A command exits non-zero with an `errorMessage` you cannot resolve from `--help` or `references/troubleshooting.md`.
- The CLI is being misused or the syntax is unclear (e.g. you can't figure out which flag to pass, or the JSON schema for `--filter` / `--nodes` / `--action` is ambiguous).
- A user or AI agent is repeatedly retrying the same command without progress (≥ 2 failed attempts on the same task).
- A documented command does not behave as the skill describes, or a response shape differs from what `references/response-shapes.md` documents.
- A capability appears to be missing entirely (no command exists for what you need to do).
- An async operation never reaches a terminal status, or returns inconsistent results across runs.

**What to put in the report:**

- `--title`: one-line summary of the problem (e.g. `"batch create fails with 'playNotCompatible' on tool workflow"`).
- `--description`: include the exact command(s) executed (with sensitive values redacted), the JSON `errorMessage`, what you expected, what you tried, and any relevant UUIDs (run, batch, workflow, model). The more context you provide, the faster it can be triaged.

```bash
# Example: report a CLI struggle after multiple failed attempts
cargo-ai workspaceManagement report create \
  --title "segment fetch returns empty results despite matching records in UI" \
  --description "Ran: cargo-ai segmentation segment fetch --model-uuid <uuid> --filter '{\"conjunction\":\"and\",\"groups\":[...]}'. Got 0 records. The same filter shows 1,200 matches in the app UI. Tried both --filter and --segment-uuid; both return empty. Expected: the same records as the UI."
```

> Do not silently give up on a failing CLI task. **Send a report.** This closes the feedback loop so the CLI and these skills can be improved.

## Sessions

Record a Claude Code session in `workspace_management.sessions`. One row per `(workspaceUuid, sessionId)`. Used by the `cargo` router's Claude Code SessionStart + Stop + SessionEnd hook recipe — see [`../cargo/SKILL.md`](../cargo/SKILL.md) for when to wire them up.

```bash
# Upsert a session. Idempotent on --session-id within the workspace.
cargo-ai workspaceManagement session upsert \
  --session-id <claude-session-id> \
  --title "<short title>" \
  --summary "<one-or-two sentence summary>"

# Same call, but also stamp finished_at = now
cargo-ai workspaceManagement session upsert \
  --session-id <claude-session-id> \
  --title "<final title>" \
  --summary "<final summary>" \
  --finished
```

- `--session-id`, `--title`, `--summary` are required on every call. `title` and `summary` are `NOT NULL` in the schema — pass placeholders on the start call and overwrite on the end call.
- `--finished` stamps `finished_at = now`. Use `--finished-at <iso>` for an explicit timestamp instead.
- Calling `upsert` twice with the same `--session-id` updates the same row — `title`, `summary`, and `finished_at` are overwritten.

Returns the upserted session as JSON. The [Cargo installer](https://github.com/getcargohq/cargo-skills#staying-current) wires SessionStart + Stop + SessionEnd hooks that call this command automatically: SessionStart writes a placeholder, the per-turn Stop hook checkpoints the row (no `--finished`), and SessionEnd writes the transcript-driven AI summary with `--finished` — see [`references/examples/sessions.md`](references/examples/sessions.md).

## Environment variables

Workspace environment variables are **injected into every worker, app and agent** in
the workspace, and a worker- or app-level entry with the same key overrides them. One
catalog, but *when* it is read depends on the consumer:

- **Agents, and CDK `workspaceEnv("NAME")` pointers**, read the value server-side on each
  use, so rotating it takes effect with no redeploy.
- **Hosted workers and apps capture values at deploy time.** A worker's bindings are
  attached when a deployment is promoted, and non-secret values are compiled into its
  bundle. An app receives only non-secret entries with a public prefix (`VITE_`,
  `NEXT_PUBLIC_`, …), baked into its build. After a change, **run `hosting deployment create` + `promote` again**. See
  [`../cargo-hosting/SKILL.md`](../cargo-hosting/SKILL.md) → Worker env vars and secrets.

```bash
cargo-ai workspaceManagement envVar list

# Create. Omit --value to read it from the environment variable of the same name.
cargo-ai workspaceManagement envVar create \
  --key OPENAI_API_KEY \
  --value sk-... \
  --secret \
  --description "Used by the enrichment worker"

# Update. Omit --value to keep the stored one.
cargo-ai workspaceManagement envVar update <uuid> --value <new> --description <text>

cargo-ai workspaceManagement envVar remove <uuid>
```

- **`--secret` encrypts the value at rest and it is never returned again** — `list`
  and `update` will not echo it back. Use it for credentials; use `--no-secret` on
  `update` to turn a variable back into plain text (which re-exposes it to `list`).
- **`--value` is optional on `create`.** Omitted, the CLI reads the environment
  variable of the same name from your shell, so `export OPENAI_API_KEY=… &&
  cargo-ai workspaceManagement envVar create --key OPENAI_API_KEY --secret` keeps the
  value out of your shell history and out of this command line.
- **`update` takes the uuid, not the key.** Get it from `envVar list`.

**From a CDK project**, reference an entry with `workspaceEnv("NAME")` rather than
copying the value into code — it is a pointer resolved server-side on every use.
`secret("NAME")` is the other option and means something different (read from *your*
environment at deploy time). See
[`../cargo-project/SKILL.md`](../cargo-project/SKILL.md) → Critical rules.

## Workspace files

Workspace files are CSVs or other data files uploaded for use in batch runs.

```bash
# Upload a file
cargo-ai workspaceManagement file upload --file <path-to-file>
# → Returns s3Filename

# Inspect a file's columns before running a batch
cargo-ai workspaceManagement file list-columns --s3-filename <s3-filename>
# → Returns column names to use when mapping to workflow inputs
```

The `s3-filename` is returned when uploading a file via `cargo-ai workspaceManagement file upload`. See the `cargo-orchestration` skill's `references/examples/tools.md` for the full file upload and batch run workflow.

## Help

Every command supports `--help`:

```bash
cargo-ai workspaceManagement user create --help
cargo-ai workspaceManagement token create --help
cargo-ai workspaceManagement folder create --help
```
