---
name: greptile-cli
description: >
  Reference for the Greptile CLI (`greptile`): reviewing a local branch before pushing, reading
  structured `--json` findings, interpreting exit codes, authenticating, and saving settings. Use
  when running any `greptile` command, when the user asks for a Greptile review of local changes,
  when wiring `greptile` into a hook, script, or CI job, or when interpreting Greptile review
  output. Covers `review`, `review status`, `review show`, `config`, `settings`, `login`, `whoami`,
  `skills`, and `fix`.
license: MIT
metadata:
  author: greptileai
  minCliCompat: 3.4.0
allowed-tools:
  - 'Bash(greptile *)'
  - 'Bash(git *)'
---

# Greptile CLI

`greptile` runs the same AI code review Greptile posts on pull requests, against the current local
branch, before anything is pushed.

This skill supports CLI 3.4.0 and later and describes the current 3.6.2 package. When the installed
`greptile <command> --help` differs, follow the installed help. Full command and version notes:
[references/commands.md](references/commands.md). Output schemas and exit codes:
[references/output.md](references/output.md).

## Always use structured output

`greptile review` renders a live terminal UI by default. That output is not meant to be parsed.
When running as an agent, always pass `--json` (structured) or `--agent` (plain text).

```bash
greptile review --json
```

Piped output also falls back to plain text on its own. Agent environment variables (`CLAUDECODE`,
`CLAUDE_CODE`, `CODEX_SHELL`, `CODEX_THREAD_ID`, `CODEX_CI`, `CURSOR_AGENT`) do **not** change the
output format. They only suppress interactive surfaces like pickers and auto-login. Pass the flag.

## Preflight

Both checks are cheap. Run them before the first review in a session, not before every command.

```bash
command -v greptile   # not installed -> see "Installing" below
greptile whoami
```

**`greptile whoami` exits `0` when there are no stored credentials**. It prints
`Not signed in. Run \`greptile login\`…` to stdout and succeeds. It exits non-zero only when a
credential exists but is corrupt, expired, or rejected. Check the text, not the exit code:

```bash
greptile whoami | grep -q '^Not signed in' && echo "needs login"
```

`greptile review` must run inside a git repository with a git remote. It picks the branch's
upstream remote, else `origin`, else the sole configured remote, and infers the Greptile
organization from that URL, so there is nothing to configure per repo.

## Reviewing local changes

`greptile review` reviews the current branch against its base. It reviews **committed** work, so
commit before reviewing.

```bash
greptile review --json                  # committed merge-base...HEAD changes
greptile review -b main --json          # review against an explicit base branch
greptile review --resume --json         # continue a review that stopped partway
```

The command waits for the remote review, up to 30 minutes. Do not wrap it in a short timeout.

To steer the review at a specific concern, pass `--instructions`. This is the same channel as an
`@greptile <instructions>` comment on a PR:

```bash
greptile review --instructions "focus on error handling in the retry logic" --json
```

### Reading the result

`--json` prints one object to stdout. This example is fictional and uses the exact emitted fields:

```json
{
  "summary": "The retry path now preserves cancellation.",
  "confidence": 4,
  "confidenceReasoning": "The change is focused, with one cleanup suggestion.",
  "securitySummary": null,
  "instructions": null,
  "comments": [
    {
      "id": "comment-7312",
      "path": "src/auth.ts",
      "startLine": 45,
      "endLine": 47,
      "side": "new",
      "severity": "P1",
      "securityIssue": false,
      "category": "comment",
      "body": "Clear the timer after the request settles.",
      "verifiedEvidence": null,
      "suggestion": "clearTimeout(timer)",
      "hunk": {
        "header": "@@ -39,6 +39,7 @@ async function retry() {",
        "oldRange": { "start": 39, "lines": 6 },
        "newRange": { "start": 39, "lines": 7 },
        "before": "return result",
        "after": "clearTimeout(timer)"
      }
    }
  ]
}
```

- `confidence` is `1`–`5` (or `null`). `5` means Greptile found nothing worth blocking on.
- `severity` is `P0` (most severe), `P1`, or `P2`.
- `suggestion` is replacement code for the commented range when Greptile has a concrete fix.
- `comments` is `[]` on a clean review.
- `category` and `verifiedEvidence` carry no signal here: on this path `category` is always the
  literal `"comment"` and `verifiedEvidence` is always `null`. Rank on `severity` and
  `securityIssue` instead.

A non-zero exit means the review did not finish. It does **not** mean findings were found. A
review reporting ten `P0`s still exits `0`.

Triage `securityIssue: true` first, then `P0`, `P1`, `P2`. Field-by-field notes are in
[references/output.md](references/output.md).

## Checking whether a commit was reviewed

`greptile review status` reports on the most recent review for a commit and encodes the answer in
its exit code, which is the intended way to gate a hook or CI step.

```bash
greptile review status --json               # HEAD
greptile review status --commit 9f2c6a43d99b9de72f4f7853b4d4cb650ed451b8 --json
```

| Exit | Meaning                                                          |
| ---- | ---------------------------------------------------------------- |
| `0`  | The commit has a completed review.                               |
| `1`  | No review exists for it, or signed out, or no usable git remote. |
| `3`  | A review for the commit is still running.                        |
| `4`  | The most recent review failed.                                   |
| `5`  | The most recent review was cancelled.                            |

Poll `3` until it resolves rather than starting a second review. A re-run discards the in-flight
one. See the polling loop in [references/commands.md](references/commands.md).

Every other command uses the common codes: `0` success, `1` failure, `2` invalid invocation,
`130` interrupted. Which of `1` and `2` you get for a given problem varies by command. `greptile
review` outside a git repo exits `2` and `greptile config` exits `1`, so branch on non-zero and
read stderr rather than mapping a code to a cause.

## Reopening past reviews

```bash
greptile review show --json          # recent reviews, grouped by commit
greptile review show b3e4f72a-1d6c-4f81-9c0e-2a7d3b9e5f10 --json
```

Use this instead of re-running a review when the user asks about a review that already ran.

## Held-back sensitive files

Before sending anything, `greptile review` holds back changed files that look like they contain
secrets: dotenv files, key material, credential stores, and diffs containing a recognizable API
key. It reviews everything else and prints a `warning: N possibly sensitive file(s) found: …` line
on stderr naming them. That line abbreviates deep paths to their last two segments and stops
listing past five files, so it is not a reliable source of full paths.

Gitignored-but-committed files are held back too, but silently. No warning names them. If a
review seems to have ignored a file, check `git check-ignore <path>`.

If _every_ changed file is held back the review does not run at all: exit `1`, with
`error: every committed change was held back and nothing was sent to Greptile`.

Only override this when the user explicitly asks, and tell them what will be sent:

```bash
greptile review --include .env config/db.pem --json
```

`--include` skips both the secret check and the gitignore check for those paths and uploads them
as-is. It is repeatable and also accepts several paths at once.

Two cases that surprise people: a commit that **removes** a hard-coded secret is held back (the
value is still in the diff), and a **rename away from** a sensitive name is held back too. Pass
the file's **new** path to `--include`, which is what the warning names.

## Review configuration

`greptile config` reads every local `.greptile` file, including uncommitted edits, then asks the
server to merge them with dashboard config and organization rules. Use it to explain _why_ a
review behaved a certain way.

```bash
greptile config --json                 # repo root
greptile config src/auth.ts --json     # cascaded and scoped to one file
```

This is separate from `greptile settings`, which manages local CLI preferences and server-backed
organization display settings.

## Settings

```bash
greptile settings list --json          # every setting and where its value comes from
greptile settings get review.layout --json
greptile settings set review.context 30
greptile settings unset review.layout
greptile settings path
```

Local keys: `color`, `telemetry`, `apiBaseUrl`, `webBaseUrl`, `review.output`, `review.layout`,
`review.context`, `review.width`. A command-line flag always beats a saved setting for that run.

`set` and `unset` write their confirmation to stderr, not stdout.

Bare `greptile settings` opens an interactive hub only for a human at a TTY. With `--json`, with
piped output, or when an agent environment variable is set, it prints the settings list and exits
`0`, so it is safe to run, though passing `list` is clearer.

Organization review settings use `org.*` keys and are stored on the server. They require an OAuth
account with admin access. `--org <slug-or-id>` selects among multiple administered organizations;
one eligible organization is selected automatically. `unset` restores an org key by writing its
default rather than removing a server field. Use `greptile settings --help` for the installed key
list.

```bash
greptile settings list --org acme-platform --json
greptile settings get org.review.strictness --org acme-platform --json
greptile settings set org.review.triggerOnUpdates true --org acme-platform
greptile settings members list --org acme-platform --json
greptile settings members invite dev@example.com --role member --org acme-platform
greptile settings members revoke dev@example.com --org acme-platform
```

Roster reads and member-role invitations are available to organization members. Pending-invite
visibility, admin-role invitations, and revocation are admin-gated. Bare `settings members` lists.

## Authentication

```bash
greptile whoami        # who is signed in, and their organizations
greptile login         # browser OAuth; interactive
greptile logout
```

For headless and CI use, set an API key in the environment instead. It takes precedence over a
stored sign-in:

```bash
export GREPTILE_API_KEY=...
```

Never pass a key as a command-line argument (it lands in shell history and process lists). If the
user needs it persisted, `greptile login --api-key` reads from a prompt or stdin.

If a command reports being signed out, tell the user to run `greptile login` themselves. Do not
run it for them. It is an interactive browser flow.

`greptile init` and organization-management commands require OAuth. An API key can run reviews,
but it cannot enable a repository or change organization settings.

## Commands to leave to the user

Surface these for the user to run rather than invoking them:

- `greptile login`: interactive browser OAuth, and it will stall an agent.
- `greptile fix install` / `greptile fix uninstall`: interactive macOS app setup.
- `greptile update`: not interactive, but it replaces the running CLI in place. Upgrading is the
  user's call, and Homebrew installs must use `brew upgrade greptile` anyway.

`greptile onboard` (deprecated) is safe: run non-interactively it prints a status summary to stderr
and exits (`0`, or `1` when signed out) rather than opening the wizard.

`greptile init` is safe read-only when run non-interactively: it reports whether the current repository
is enabled (`0` when enabled, `1` when not or not found) and never enables anything. Enabling needs
OAuth, admin access, and interactive confirmation. A member is told to ask an organization admin.
Prefer `greptile init --json`: it never prompts and prints one object to stdout whose `status` field
tells the exit-`1` outcomes apart: `enabled` (exit `0`), `not_enabled` (inspect `canManage` before
suggesting an interactive retry), `not_connected` (the repository is not connected to the user's
Greptile workspace), or `unsupported_server` (the server predates `init`).

`greptile fix status --json` is safe too, but it exits `1` when Fix is simply **not installed**, or
on any non-macOS platform. Read its output rather than treating non-zero as an error.

## Installing

Do not install the CLI without asking. When it is missing, offer:

```bash
npm install -g greptile          # any platform, needs Node 22+
brew install greptileai/tap/greptile   # macOS
```

## Agent skills

```bash
greptile skills list --json      # installed Greptile-authored skills and paths
greptile skills install          # install them for the agents on this machine
greptile skills install --global # install for every project, not just this repo
greptile skills install --force  # replace already-installed copies
greptile skills update --json    # update installed copies from Greptile's catalog
```

Install and update fetch the catalog from Greptile and filter it by the running CLI version. Bare
`greptile skills` only lists copies under the current project root and home directory. Install
preserves existing copies unless `--force`; update replaces stale Greptile-authored files in both
scopes and leaves retired catalog entries alone.

## Environment blockers (CLI 3.6.2 private beta)

Use `greptile environment blockers` for open blockers, `blockers history --page N` for
resolved/skipped history, and `blockers resolve|skip <ID>` to close a blocker.
Agents must pass `--force` to confirm the change. See [references/commands.md](references/commands.md).

## Environment variables

| Variable                                          | Effect                                                                                                  |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `GREPTILE_API_KEY`                                | Authenticate with an API key; beats a stored sign-in.                                                   |
| `GREPTILE_API_BASE_URL` / `GREPTILE_WEB_BASE_URL` | Point at a self-hosted deployment (same as the `apiBaseUrl`/`webBaseUrl` settings).                     |
| `GREPTILE_NO_UPDATE_CHECK`                        | Skip the daily check for a newer release. `NO_UPDATE_NOTIFIER`, `CI`, and `NODE_ENV=test` also skip it. |
| `GREPTILE_NO_AUTO_INSTALL`                        | Skip the one-time diagram renderer download.                                                            |
| `XDG_CONFIG_HOME`                                 | Relocate the settings file.                                                                             |
| `NO_COLOR` / `FORCE_COLOR`                        | Force ANSI color off / on in review output.                                                             |
| `COLUMNS`                                         | Override output width.                                                                                  |

## Files

| Path                               | Contents                                                |
| ---------------------------------- | ------------------------------------------------------- |
| `~/.greptile/auth.json`            | Credentials, refreshed automatically.                   |
| `~/.greptile/reviews.json`         | Local review history behind `status`/`show`/`--resume`. |
| `~/.config/greptile/settings.json` | Saved settings (`greptile settings path`).              |
| `~/.cache/greptile/`               | Diagram renderer, and skills staged for install.        |

Never read, print, or copy `auth.json`.

## Looping until a review is clean

To iteratively fix findings and re-review until Greptile returns 5/5 with zero comments, use the
`greploop` skill rather than hand-rolling the loop. Never drive it with `watch(1)`. It never
exits, and nothing fixes the code between ticks.
