---
name: publish-check
description: Read-only scan of a git repository (working tree and full history) for leaks before it goes public - Claude conversation links, paths from your machine (/Users/<name>), e-mail addresses and internal names. Use when the user is about to make something public - creating a public repository, opening a PR to a public repository or pushing to a public remote - or asks to check for leaks before publishing. Triggers - /publish-check or /publish-check:publish-check, "publish-check", "check this repo before I publish", "scan history for leaks", "is it safe to make this repo public", "checar antes de publicar", "varredura de vazamentos".
---

# publish-check (check before publishing)

This skill scans the working tree and the **whole git history** for what should not become public:
- Claude conversation links (`claude.ai/code/session...`, `/chat/...`, `/share/...`).
- Paths from someone's machine (`/Users/<name>`, `/home/<name>`, `C:\Users\<name>`).
- E-mail addresses (in text, in the author field and in the committer field).
- A list of the owner's internal names.

The scan is **read-only**: it never changes the repository and never rewrites history. It needs `python3` (stdlib only) and `git`.

It does not look for secrets (keys, tokens). For secrets, use a secret scanner such as gitleaks. Tell the user this when you present the results.

Reply to the user in the user's language. The script's report is in English: explain its content to the user in the user's language.

## When to use

Use it before something becomes public: creating a public repository, opening a PR to a public repository or pushing to a public remote.

**Offer** to run the scan. **Never block**: the decision to publish belongs to the user.

If the repository is private and will not be published, do not offer.

## Flow

### 0. Locate the script

The script ships with this skill: `${CLAUDE_SKILL_DIR}/scripts/publish_check.py`. Run it directly, always with `python3 -I`.

```bash
test -f "${CLAUDE_SKILL_DIR}/scripts/publish_check.py" && echo OK || echo FALTA
```

`FALTA` means "missing".

If `${CLAUDE_SKILL_DIR}` appears unexpanded, use the path shown as "Base directory for this skill" when the skill was loaded. Write that path out in full in every command.

### 1. Confirm that the repository will be public (or already is)

If it is not clear, ask the user. Do not assume.

If `gh` is installed, `gh repo view --json visibility -q .visibility` shows the visibility of a repository that is already on GitHub.

### 2. Run

```bash
python3 -I "${CLAUDE_SKILL_DIR}/scripts/publish_check.py" <repository>
```

Useful options:
- `--json`: print the script's report as JSON.
- `--since <date>`: scan only commits newer than the date (any date git accepts).
- `--max-commits N`: scan only the newest N commits (for large repositories).
- `--denylist <file>`: internal names, one per line. Keep this file **outside** the repository.
- `--config <file>`: use this config file.

If `.publish-check.json` exists at the repository root, the script reads it by itself. Its keys:
- `denylist`: internal names.
- `allow`: fingerprints of accepted findings.

Exit code:
- `0`: clean.
- `1`: findings.
- `2`: error (not a git repository, invalid config, `git` missing).

### 3. Present

Show the findings grouped by category, as the script prints them (keep the masked values and fingerprints exactly as printed; write your explanations in the user's language). The values are already partly masked (`j***@domain.dev`, `/Users/***`). Do **not** reproduce the full value anywhere else.

Say how many files and commits were scanned.

For each category, explain to the user what to do. Do not execute any of it yourself.

- A finding only in the **working tree**: tell the user to edit the file and commit the change.
- A finding in the **history** (message, author, patch, tag): it goes away only by rewriting the history.
  - Point to `docs/remediation.md` (inside the plugin).
  - Remind the user to back up first and that every SHA will change.
  - **Never rewrite history on your own.** Do not offer to run the rewrite. Run it only if the user explicitly asks.
- If the script's report says `skipped` (binary, unreadable or too large files), those files were **not checked**. Tell the user.
- If the script's report shows `accepted by the allow list`, tell the user how many findings were accepted and by whom (the `allow` key of `.publish-check.json`).
- If the script's report says `history limited` (from `--since` / `--max-commits`) or `no commits were scanned`, the scan was partial.
  - Say what was left out.
  - Say that "clean" holds only for what was scanned.
  - The example pre-push hook limits the scan to 200 commits by default.
- If the script's report warns `partial clone`, the script never fetches blobs that are not stored locally and stops with an error if it needs one. If you see this warning together with an error, tell the user the scan could not complete.
- If the script's report warns `shallow clone`, the result is partial (only part of the history was scanned).
  - Tell the user.
  - Suggest `git fetch --unshallow` before trusting "clean".
- A finding that is a false positive (an e-mail that is public on purpose, an example path): the user can accept it by adding its `fingerprint` to the `allow` key of `.publish-check.json`. Edit that file only with the user's approval.

### 4. Close

Summarise: clean, or N findings in M categories and what the user decided. The decision to publish stays with the user.

## Rules

- Read-only. Never run commands that rewrite history (`filter-branch`, `filter-repo`). Never force-push to the remote.
- The list of internal names (`denylist`) is sensitive. If the repository is public, keep the list in a file **outside** it (`--denylist`), or in a `.publish-check.json` that git ignores (`.gitignore` or `.git/info/exclude`). A `.publish-check.json` with `denylist` committed in a public repository leaks the list itself, and the tool will report that.
- The script's report contains file names and commit messages. Treat it as internal until the user decides otherwise.
- If `git` is not on the PATH, tell the user. Do not try another way.
