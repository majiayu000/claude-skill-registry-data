---
name: folder-crypt
description: >-
  Encrypt or decrypt a file or folder with a password via a Python CLI
  (AES-256-GCM). Password and paths can be prompted, passed as args, or read
  from SkillCred .env (FOLDER is a comma-separated list). Use when the user
  asks to password-protect a file or folder, encrypt a directory, decrypt a
  .fcr archive, or invokes /folder-crypt_*.
disable-model-invocation: true
---

### TO COPY

# folder-crypt

Per-workspace registration slice. Credentials live in `{SKILL_PATH}/.env`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
export PROJECT_PATH="<main project folder>"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/security/folder-crypt/scripts/cli.py env
```

`PROJECT_PATH` is the main project folder. Relative `FOLDER` paths start there.

After a successful encrypt, ask before editing git — do not assume `--remove`, never print `PASSWORD`:

1. “Add <path> (and optionally <path>.fcr) to .gitignore?”
2. “Add a before-commit hook that runs encrypt?”

##### END TO COPY

# folder-crypt

Password-protect a file or a folder: pack it as tar.gz, encrypt with **AES-256-GCM**
(key from PBKDF2-HMAC-SHA256). Decrypt restores that file or folder. A file archive
holds one file; a folder archive holds the directory tree. Existing folder archives
still decrypt.

`skill_env.py` loads `.env` via SkillCred — do not `source` it in the shell.
`CURRENT_SKILL_DIRECTORY` is the only required SkillCred export.
`PROJECT_PATH` is the main project folder: relative `FOLDER` paths start there.

Prefer `~/.meta-skills/.venv/bin/python` from
`~/.meta-skills/skills/security/folder-crypt/`.

## When to use

Trigger phrases: "encrypt this file", "encrypt this folder", "password-protect a directory",
"decrypt the .fcr archive", `/folder-crypt_*`.

After a successful encrypt, always ask whether to add the plaintext path(s)
to `.gitignore`, and whether to add a before-commit hook that runs `encrypt`.
Do not assume `--remove`.

Confirm with the user before **encrypt --remove** (deletes the original file or folder).

## Prerequisites

```bash
cd ~/.meta-skills/skills/security/folder-crypt
~/.meta-skills/install.sh pip init .
```

## Credentials — SkillCred `.env` (optional)

Both keys are optional. When omitted, the CLI prompts (TTY) or requires flags.

| Variable | Notes |
|----------|--------|
| `FOLDER` | Comma-separated files or folders (encrypt), or those paths / `.fcr` archives (decrypt). Whitespace around commas is ignored. Relative paths start at `PROJECT_PATH`. |
| `PASSWORD` | Default password — never print it |

`PROJECT_PATH` is a shell export (the main project folder), not a `.env` key.
Set it before the CLI. Absolute `FOLDER` entries stay absolute.

```bash
cp ~/.meta-skills/skills/security/folder-crypt/.env.example "{SKILL_PATH}/.env"
python scripts/cli.py env    # FOLDER is the raw string, folders is the parsed list; PASSWORD is only "set"/"missing"
```

Example `.env`:

```bash
FOLDER=to_encrypt,secrets,notes
PASSWORD=change-me
```

Interactive (no `.env`):

```bash
python scripts/cli.py encrypt
# File or folder: /path/to/secret.txt
# Password: ********
# Confirm password: ********
```

Non-interactive (`.env` or args):

```bash
python scripts/cli.py encrypt /path/to/secret.txt   # this file only (one JSON object)
python scripts/cli.py encrypt /path/to/secret       # this folder only
python scripts/cli.py decrypt /path/to/secret.fcr
python scripts/cli.py encrypt   # every path in FOLDER, same PASSWORD
python scripts/cli.py decrypt   # every FOLDER entry; a file or folder uses the sibling .fcr
python scripts/cli.py encrypt -o /path/to/out.fcr   # error when FOLDER lists more than one path
```

Prefer `.env` or the prompt over `--password` (avoids shell history).

`-o` / `--output` is valid for a single target only (one positional arg, or a `FOLDER` list of one). Several `FOLDER` paths plus `-o` exits with a JSON error and encrypts nothing.

With no positional arg, stdout is one object `{ok, action, items:[…]}`. Each item is one path. A failure on one path does not drop the others; `ok` is false and the exit code is 1 when any item failed. A positional arg keeps the single-object JSON.

## Slash commands

| Slash | CLI | Description |
|-------|-----|-------------|
| `/folder-crypt_env` | `python scripts/cli.py env` | Resolve `.env` (does not print the password) |
| `/folder-crypt_encrypt` | `python scripts/cli.py encrypt [PATH] [-o ARCHIVE.fcr] [--remove]` | Encrypt one file or folder, or every `FOLDER` entry → `.fcr` |
| `/folder-crypt_decrypt` | `python scripts/cli.py decrypt [ARCHIVE.fcr\|PATH] [-o DEST]` | Decrypt one archive, or every `FOLDER` entry |

Default archive path: `<path>.fcr` next to the file or folder. Default decrypt dest: archive name without `.fcr` (a file comes back as a file). A `FOLDER` entry that is a file or directory uses that sibling `.fcr`. A path that already ends in `.fcr` is the archive.

Stdout is JSON.

## How to run

1. `export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"`
2. `export PROJECT_PATH="<main project folder>"` — relative `FOLDER` paths start here
3. `cd ~/.meta-skills/skills/security/folder-crypt`
4. First run: `~/.meta-skills/install.sh pip init .`
5. `~/.meta-skills/.venv/bin/python scripts/cli.py …`
6. After encrypt succeeds, ask to gitignore the plaintext file(s) or folder(s) (and optionally the `.fcr`), then ask whether to add a before-commit hook that runs `encrypt`. Do not assume `--remove`.

## After encrypt — `.gitignore`

Required after every successful encrypt. Do this yourself as the agent. Do not edit git until the user says yes. Do not assume `--remove`.

1. Resolve the plaintext path(s) just encrypted (JSON `folder`, or `items[].folder` — this field is the file or folder) and the matching `.fcr` (`archive`) when that archive sits in a git repo.
2. Ask, and wait for an answer: “Add <path> (and optionally <path>.fcr) to .gitignore?”
3. If they say yes, for each path inside a git work tree:
   - Repo root is `git rev-parse --show-toplevel`.
   - Append entries **relative to the repo root** (`notes.txt` for a file, `secrets/` for a directory, plus `notes.txt.fcr` or `secrets.fcr` for the archive).
   - Skip a line that is already present.
   - If `.gitignore` does not exist, create it at the repo root.
4. If a path is outside any git repo, say so and skip it. Do not create a `.gitignore` there.
5. Do not gitignore `.cursor/skills/folder-crypt/.env` as this step. That file should already be ignored. Never commit `.env` or print `PASSWORD`.

## After encrypt — before-commit hook

Ask this separately from the `.gitignore` question, and wait: “Add a before-commit hook that runs encrypt?”

Do not add the hook until they say yes. The hook is only the `encrypt` command. No `--remove`, no `--password`, no extra checks. `PASSWORD` stays in `.env`. The command encrypts every `FOLDER` entry, so those paths need to be listed there.

1. If the repo root cannot be resolved, say so and skip.
2. Hook file: `$(git rev-parse --git-path hooks)/pre-commit` (this follows `core.hooksPath` when set, otherwise `.git/hooks/pre-commit`).
3. If that file already exists, append the command. Do not replace the file. If it does not exist, create it with a `#!/usr/bin/env bash` shebang and `chmod +x`.
4. Skip when the marker `# folder-crypt encrypt` is already present.

```bash
# folder-crypt encrypt
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
export PROJECT_PATH="<main project folder>"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/security/folder-crypt/scripts/cli.py encrypt
```

Use the real skill directory and the repo root in place of the placeholders. A non-zero exit from `encrypt` stops the commit. Encrypt replaces an existing `.fcr`.

5. A hook under `.git/hooks/` is local to this clone. If `core.hooksPath` points at a tracked directory, say that the hook file is inside the work tree. Do not commit it unless the user asks.
6. Never commit `.env` or print `PASSWORD`.

## Safety

- After encrypt, always prompt for `.gitignore`, then ask about a before-commit hook that runs `encrypt` (no `--remove`). Do not assume `--remove`.
- Confirm before `--remove`.
- Encrypt replaces an existing `.fcr`. Decrypt replaces an existing file or folder. A wrong password leaves the destination unchanged.
- Never commit `.env` or print `PASSWORD`.
- Never put the output `.fcr` inside the folder being encrypted.
- Wrong password → JSON error, no files written.
