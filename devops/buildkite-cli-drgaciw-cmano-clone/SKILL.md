---
name: buildkite-cli
description: >
  This skill should be used when the user asks to "trigger a build",
  "check build status", "watch a build", "view build logs", "rebuild a build",
  "cancel a build", "list builds", "download artifacts",
  "manage secrets", "create a pipeline", "list pipelines", or
  "interact with Buildkite from the command line".
  Also use when the user mentions bk commands, bk build, bk job, bk pipeline,
  bk secret, bk artifact, bk cluster, bk package, bk auth, bk configure,
  bk use, bk init, bk api, or asks about Buildkite CLI installation,
  terminal-based Buildkite workflows, or command-line CI/CD operations.
---

# Buildkite CLI

The Buildkite CLI (`bk`) provides terminal access to builds, jobs, pipelines, secrets, artifacts, clusters, and packages. Use it to trigger builds, tail logs, manage secrets, and automate CI/CD workflows without leaving the command line.

> **Tip:** This skill covers common commands and patterns. For complete flag details on any command, run `bk <command> --help`.

## Quick Start

```bash
# Install
brew tap buildkite/buildkite && brew install buildkite/buildkite/bk

# Authenticate
bk configure

# Trigger a build on the current branch
bk build create --pipeline my-app

# Watch it run
bk build watch 42 --pipeline my-app

# View logs for a failed job
bk job log <job-id>
```

## Installation

```bash
brew tap buildkite/buildkite && brew install buildkite/buildkite/bk
```

For binary downloads and verification, see `references/command-reference.md`.

## Authentication

Run `bk configure` to set the organization slug and API access token. This creates `$HOME/.config/bk.yaml` on first run.

```bash
bk configure
# Non-interactive (CI/Docker): bk configure --org my-org --token "$BUILDKITE_API_TOKEN" --no-input
```

Or use keychain-based auth (v3.31+): `bk auth login`

### Token creation

1. Open Buildkite > user avatar > **Personal Settings** > **API Access Tokens**
2. Select **New API Access Token**
3. Grant scopes: `read_builds`, `write_builds`, `read_pipelines`, `read_artifacts` at minimum
4. Copy the token and pass it to `bk configure`

For the full `bk auth` subcommand reference and organization switching (`bk use`), see `references/command-reference.md`.

## Builds

Manage pipeline builds — create, view, list, cancel, retry, and watch.

### Create a build

```bash
# Build the current branch and commit (pipeline auto-detected from repo)
bk build create

# Explicit pipeline
bk build create --pipeline my-app

# Build with environment variables and metadata
bk build create -e "FOO=BAR" -e "BAR=BAZ"
bk build create --branch feature/auth --commit abc1234 --env "DEPLOY_ENV=staging"
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--pipeline` | `-p` | auto-detected | Pipeline slug; resolved from repo context when omitted |
| `--branch` | `-b` | current branch | Git branch to build |
| `--commit` | `-c` | HEAD | Git commit SHA |
| `--message` | `-m` | — | Build message |
| `--env` | `-e` | — | Environment variables (repeatable) |
| `--env-file` | `-f` | — | Load environment variables from a file |
| `--metadata` | `-M` | — | Build metadata key=value (repeatable) |

### View a build

```bash
bk build view 42 --pipeline my-app
```

### List builds

```bash
# List recent builds for a pipeline
bk build list --pipeline my-app

# List only failed builds
bk build list --pipeline my-app --state failed
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--pipeline` | `-p` | — | Pipeline slug (omit for org-wide listing) |
| `--state` | — | — | Filter by state: `running`, `scheduled`, `passed`, `failed`, `blocked`, `canceled`, `canceling`, `skipped`, `not_run`, `finished` (repeatable) |
| `--branch` | — | — | Filter by branch name (repeatable) |
| `--output` | `-o` | `text` | Output format: `text`, `json`, `yaml` |

### Watch a build

Stream real-time build progress to the terminal. Blocks until the build completes or is canceled.

```bash
bk build watch 42 --pipeline my-app
```

### Cancel a build

```bash
bk build cancel 42 --pipeline my-app
```

The build must be in a `scheduled`, `running`, or `failing` state.

### Rebuild a build

```bash
bk build rebuild 42 --pipeline my-app
```

### Build workflow: trigger and watch

Combine `create` and `watch` for a complete trigger-and-follow workflow:

```bash
# Trigger a build and immediately stream progress
bk build create --pipeline my-app --branch main && bk build watch --pipeline my-app
```

> Note: `bk build watch` without a build number will watch the most recent build.

## Jobs

Manage individual jobs within a build — view logs, retry failures, cancel running jobs.

### View job logs

```bash
bk job log <job-id>
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--no-timestamps` | — | `false` | Strip timestamp prefixes from log output |

### Retry a job

Each job ID can only be retried once — subsequent retries must use the new job ID returned by the first retry.

```bash
bk job retry <job-id>
```

### Cancel a job

```bash
bk job cancel <job-id>
```

### Debugging workflow: find failures and read logs

```bash
# Find failed builds
bk build list --pipeline my-app --state failed

# View the build to identify which jobs failed
bk build view 42 --pipeline my-app

# Read logs for the failed job
bk job log <job-id>
```

## Pipelines

Manage pipeline configuration — list, create, and update pipelines.

> For converting pipelines from other CI systems, see the **buildkite-migration** skill.

### Convert a pipeline from another CI system

Convert a GitHub Actions, Jenkins, CircleCI, Bitbucket, GitLab, Harness, or Bitrise pipeline to Buildkite YAML. No login required — uses a public API.

```bash
# Auto-detect vendor from file path and save to .buildkite/pipeline.<vendor>.yml
bk pipeline convert -F .github/workflows/ci.yml
bk pipeline convert -F .circleci/config.yml
bk pipeline convert -F Jenkinsfile

# Specify vendor explicitly (required for gitlab, harness, bitrise)
bk pipeline convert -F .gitlab-ci.yml --vendor gitlab

# Custom output path
bk pipeline convert -F .github/workflows/ci.yml --output .buildkite/pipeline.yml

# Read from stdin
cat .github/workflows/ci.yml | bk pipeline convert --vendor github
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--file` | `-F` | — | Path to source pipeline file (required unless using stdin) |
| `--vendor` | `-v` | auto-detected | Source CI vendor: `github`, `bitbucket`, `circleci`, `jenkins`, `gitlab`, `harness`, `bitrise` |
| `--output` | `-o` | `.buildkite/pipeline.<vendor>.yml` | Output file path |
| `--timeout` | — | `300` | Cancellation timeout in seconds |

### List pipelines

```bash
bk pipeline list
```

### Create a pipeline

```bash
bk pipeline create "My App" --repository "git@github.com:org/my-app.git"
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `<name>` | — | — | Pipeline name (positional arg, required) |
| `--repository` | `-r` | — | Git repository URL |
| `--cluster-uuid` | — | — | Cluster UUID to assign the pipeline to |
| `--cluster-name` | — | — | Cluster name (resolved to UUID) |
| `--description` | `-d` | — | Pipeline description |

> For pipeline YAML configuration after creation, see the **buildkite-pipelines** skill.

## Secrets

Manage cluster-scoped secrets for pipelines. Secrets are encrypted and accessible to all agents within a cluster.

> For using secrets inside pipeline YAML (`secrets:` key) and inside job steps (`buildkite-agent secret get`), see the **buildkite-pipelines** skill and **buildkite-agent-runtime** skill respectively.

### Create a secret

```bash
bk secret create --cluster-uuid <cluster-uuid> --key MY_SECRET --value "$TOKEN"
```

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--cluster-uuid` | — | — | Cluster UUID (required) |
| `--key` | — | — | Secret key name (required) |
| `--value` | — | — | Secret value (omit for interactive prompt) |
| `--description` | — | — | Human-readable description |

**Naming rules:**
- Keys must contain only letters, numbers, and underscores
- Keys cannot begin with `buildkite` or `bk` (case-insensitive)
- Exception: `BUILDKITE_API_TOKEN` is allowed

### List secrets

```bash
bk secret list --cluster-uuid <cluster-uuid>
```

### Get a secret

```bash
bk secret get --cluster-uuid <cluster-uuid> --secret-id <secret-uuid>
```

### Update a secret

```bash
bk secret update --cluster-uuid <cluster-uuid> --secret-id <secret-uuid> --update-value
```

### Delete a secret

```bash
bk secret delete --cluster-uuid <cluster-uuid> --secret-id <secret-uuid>
```

## Artifacts

Download build artifacts from the terminal.

### Download artifacts

```bash
# Download all artifacts from a specific build
bk artifacts download --build 42

# Download all artifacts from a specific job
bk artifacts download --build 42 --job-uuid <job-uuid>

# Download a specific artifact by ID (use `bk artifacts list` to find IDs)
bk artifacts download <artifact-id> --build 42
```

### List artifacts

```bash
# List artifacts for a build
bk artifacts list 42

# List artifacts for a specific job in a build
bk artifacts list 42 --job-uuid <job-uuid>
```

> **Note:** The CLI command is `bk artifacts` (plural). There is no `bk artifacts upload` — for uploading artifacts from within a running job step, use `buildkite-agent artifact upload` (see the **buildkite-agent-runtime** skill). For declaring artifact paths in pipeline YAML (`artifact_paths:`), see the **buildkite-pipelines** skill.

## Clusters

List and view clusters with `bk cluster list` and `bk cluster view <cluster-uuid>`. For flags and examples, see `references/command-reference.md`.

> For cluster creation, queue management, and infrastructure provisioning, see the **buildkite-agent-infrastructure** skill.

## Packages

Push packages with `bk package push <registry-slug> --file-path <file>`. For flags and supported formats, see `references/command-reference.md`.

> For OIDC-based authentication to package registries (no static credentials), see the **buildkite-secure-delivery** skill.

## Raw API Access

Make direct REST or GraphQL API calls with `bk api <path>` (REST) or `bk api --data '<query>'` (GraphQL). For flags and examples, see `references/command-reference.md`.

> For comprehensive REST and GraphQL API documentation (endpoints, mutations, pagination, webhooks), see the **buildkite-api** skill.

## Users

Invite users with `bk user invite user@example.com`. See `references/command-reference.md` for details.

## Pipeline Initialization

Scaffold a starter `pipeline.yaml` with `bk init`. For pipeline YAML syntax and step types, see the **buildkite-pipelines** skill. See `references/command-reference.md` for details.

## MCP Server Alternatives

When the Buildkite MCP server is available, agents can use MCP tools for direct access without shell execution. The table below maps CLI commands to their MCP equivalents:

| CLI Command | MCP Tool | Notes |
|-------------|----------|-------|
| `bk build create` | `create_build` | MCP handles auth automatically |
| `bk build view` | `get_build` | MCP returns structured data |
| `bk build list` | `list_builds` | MCP supports the same filters |
| `bk job log` | `read_logs`, `tail_logs` | MCP supports streaming |
| `bk pipeline list` | `list_pipelines` | |
| `bk pipeline create` | `create_pipeline` | |
| `bk artifacts download` | `list_artifacts_for_build`, `get_artifact` | |
| `bk cluster list` | `list_clusters` | |
| `bk auth status` | `current_user`, `access_token` | |
| `bk secret create/list/delete` | — | No MCP equivalent; CLI required |
| `bk package push` | — | No MCP equivalent; CLI required |
| `bk job retry` | — | No MCP equivalent; CLI required |
| `bk job cancel` | — | No MCP equivalent; CLI required |
| `bk build watch` | — | No MCP equivalent; CLI required |
| `bk api` | — | Use MCP tools for read operations; CLI for custom API calls |

**When to use CLI vs MCP:** Use MCP tools when available — they handle authentication, pagination, and response parsing automatically. Fall back to the CLI when MCP does not cover the operation (secrets, packages, job retry, build watch) or when the agent needs to execute commands in a Bash workflow.

## Common Mistakes

| Mistake | What happens | Fix |
|---------|-------------|-----|
| Running `bk` commands before `bk configure` | Every command fails with authentication errors | Run `bk configure` or `bk auth login` first |
| Running `bk configure` in Docker/CI without `--no-input` | Hangs or fails trying to read from TTY or system keychain | Add `--no-input` flag: `bk configure --org my-org --token "$TOKEN" --no-input` |
| Omitting `--pipeline` on build commands | Command fails or targets the wrong pipeline | Always pass `--pipeline <slug>` explicitly |
| Retrying a job ID that was already retried | API returns 422 error — each job ID can only be retried once | Use the new job ID returned by the first retry |
| Creating secrets with keys starting with `buildkite` or `bk` | Creation fails — reserved prefix | Choose a different key name (exception: `BUILDKITE_API_TOKEN`) |
| Passing secret values as literal strings in `--value` | Values persist in shell history and process list | Use env var references (`--value "$TOKEN"`) or interactive prompts |
| Using `bk build cancel` on a completed build | API returns error — only `scheduled`, `running`, or `failing` builds can be canceled | Check build state with `bk build view` first |
| Expecting `bk artifacts download` to work cross-cluster | Artifacts are cluster-scoped by default | Ensure both pipelines are in the same cluster or configure cross-cluster artifact access |
| Confusing `bk` CLI with `buildkite-agent` | `bk` runs on local machines to interact with the Buildkite API; `buildkite-agent` runs inside CI job steps | Use `bk` from terminal, `buildkite-agent` inside pipeline step commands |

## Additional Resources

### Reference Files
- **`references/command-reference.md`** — Full installation methods, auth subcommands, organization switching, and detailed flags/examples for clusters, packages, API access, users, and pipeline initialization

## Further Reading

- [Buildkite Docs for LLMs](https://buildkite.com/docs/llms.txt)
- [Buildkite CLI overview](https://buildkite.com/docs/platform/cli.md)
- [CLI command reference](https://buildkite.com/docs/platform/cli/reference.md)
- [CLI installation](https://buildkite.com/docs/platform/cli/installation.md)
- [CLI configuration and authentication](https://buildkite.com/docs/platform/cli/configuration.md)
- [Managing secrets](https://buildkite.com/docs/pipelines/security/secrets/buildkite-secrets.md)
