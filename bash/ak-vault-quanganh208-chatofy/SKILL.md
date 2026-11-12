---
name: ak-vault
description: "Store, find, sync, rotate, and use secrets (API keys, tokens, .env values) through AgentKit's `ak secrets` vault without ever printing a value, while honoring a user's recorded choice of .env files or another secret manager. Use when a task touches a credential, a .env.* file, or a deploy or API call that needs a key."
when_to_use: "Invoke when a task stores, finds, rotates, syncs, imports, or uses a credential, or meets .env.* files. It reads the recorded secret store choice first and asks at most once."
category: workflow
keywords: [secrets, vault, credentials, api-key, token, dotenv, env-file, ak-secrets, sync, rotate, import-env]
argument-hint: "[store|find|sync|use|rotate|import] [ref or .env path]"
metadata:
  author: agentkit
  version: "1.0.0"
---

# AgentKit Vault

Handle credentials the way the user chose, with no value ever entering the
conversation. `ak secrets` is the recommended store, not a mandatory one: a user
who keeps `.env.*` files or runs another secret manager is followed, never
pushed. Ask a question only when a decision is genuinely missing, and record the
answer so it is never asked again.

## Hard rules

- Never print, echo, log, or paste a secret value. Report refs, counts, exit
  codes, and `[redacted]` only. Never ask a person to paste a value into the
  conversation.
- Feed values only through stdin (`--value=-`) or a file (`--value-file`), from
  a script that reads the source and pipes it on. `--value=<literal>` is
  rejected by the CLI and would leak into shell history.
- Do not read a `.env*` file to discover what it contains. Its name is enough to
  detect it; read it only inside a non-echoing script that moves a value the
  user asked to move.
- Write `${secret:NAME}` only where you mean it to resolve (see
  [runtime-and-lifecycle.md](references/runtime-and-lifecycle.md)). Never type it
  into a commit message, heredoc, or other shell text; author such text with the
  file-editing tools instead.
- Never `--force` over an existing ref whose source of truth is unclear. Check
  first; ask when the stored value and the new one could disagree.
- `ak secrets get --reveal` is for a person at a terminal. An agent confirms a
  write by exit code, `get` (prints `[redacted]`), `search`, or `list --json`.
- To tell whether a stored ref holds the expected credential (which account,
  old or rotated, the same as a `.env` entry), read its `hint` in
  `list --json`, `get --json` or `search --json` (a public prefix and the last
  4 characters, or `null` with a `hintReason`), then confirm with
  `ak secrets compare <REF> --value-file <path>` or `--value=-` from a
  non-echoing script; it answers `match` or `differs` and prints neither value.
  It refuses with exit 2 when the candidate or the stored value is under 16
  characters after any public prefix and one trailing newline, the same rule
  that withholds a hint (`hintReason: short value`), and each call is a row in
  `ak secrets audit` when the ledger exists, so never loop it to guess a value.
  Never ask for `--reveal` or create a duplicate ref "just in case" when the
  hint and `compare` can answer. Quote a hint only as a hint, never as a value.
- Before saying anything about the cloud vault, read
  `ak secrets sync status --json` (local, no network). Never claim sync is off
  or absent without it.

## Step 1: Read the recorded choice

```bash
ak config prefs resolve --json   # read .prefs.secretStore.choice
```

| Choice | What to do |
|---|---|
| `ak-vault` | Use `ak secrets` (Steps 2 to 4). |
| `env-file` | Work with the project's `.env.*` files as asked. Do not suggest the vault. Warn once, without blocking, if `git check-ignore -q <file>` says a secrets file is not ignored. |
| `external:<name>` | Use that manager's own documented workflow. Do not suggest the vault, and do not try to verify the manager exists. |
| unset | Recommend once (below), then follow the answer. |

**Recommend once.** Only while the current task actually involves a credential
or a `.env.*` file, and only in an interactive session, ask one question:
store secrets in AgentKit's vault (recommended: encrypted, searchable,
optionally synced across devices), keep `.env.*` files, or use another manager
(name it). Ask in the same question whether the answer covers this project or
every project. Record it immediately:

```bash
ak config prefs set secret_store.choice ak-vault --scope project   # or user, env-file, external:1password
```

A user who brushes the question off has still answered it: record what the
project already does (`env-file` when it keeps `.env.*` files) at project scope.
In `--json`, CI, or any non-interactive run, never ask and never recommend;
continue with whatever the project already uses.

## Step 2: Settle the metadata before writing (ak-vault only)

Every ref needs a project and an environment so it can be found later. Infer
them first, from evidence rather than guesses:

- environment from the file name (`.env.production` is `production`) or the
  deploy target being configured;
- project from the repository (`git remote get-url origin` basename, else the
  repository directory name) or the deploy config's name;
- provider from the variable prefix (`CLOUDFLARE_*` is `cloudflare`), account
  only when the source states it.

When project or environment is still missing or ambiguous (a bare `.env`, a
monorepo with several apps, a key shared by several projects), **ask the user
one question right away, before writing**, offering the inferred candidates.
In a non-interactive run, stop without writing and name the missing fields.

Profile metadata (description, project, environment, provider, account, tags)
syncs only to devices on a current `ak`; older ones see the ref name, value,
and timestamps only. So the ref name itself must stay findable everywhere: use `<PROJECT>_<NAME>`
for a project-specific secret (add `_<ENV>` when the project keeps more than
one environment of it), and the provider's conventional name (for example
`CLOUDFLARE_API_TOKEN`) for a credential shared across projects. A ref name is
independent of the environment variable the app reads.

## Step 3: Store, find, and sync

Check before writing: `ak secrets search <words> --json` or
`ak secrets list --json`. When a candidate ref exists, read its `hint`, then
pipe the new value into `ak secrets compare <REF> --value=-` from the
non-echoing script to learn whether the ref already holds it. An existing ref
for the same purpose is updated with
`ak secrets rotate` (value changed) or `ak secrets annotate` (metadata only),
not re-created. Then store, verify, and sync as described in
[store-and-sync.md](references/store-and-sync.md), which holds the non-echoing
script templates, `import-env` for whole files, and the sync cycle.

## Step 4: Use, rotate, and recover

Runtime use through `${secret:NAME}`, approvals, rotation, deletion, export,
audit, and vault recovery are in
[runtime-and-lifecycle.md](references/runtime-and-lifecycle.md). Several of
those commands refuse to run under an agent by design; hand the exact command
to the user instead of looking for a way around it.

## Command details

Flags and exit codes come from `ak secrets <command> --help`, which is the
current authority; read it before using a flag this skill does not show.
