---
name: iru-check-security
description: Scan the repository for accidentally committed secrets (API keys, passwords, tokens, private keys, etc.) using the `detect-secrets` CLI (https://github.com/Yelp/detect-secrets). Checks whether `detect-secrets` is installed and, if it isn't, first checks for its Python prerequisite (installing Python via `winget`/`choco` on Windows if missing — Linux/macOS ship Python already) before attempting to install `detect-secrets` itself (`pip`/`pip3`/`pipx`, falling back to `brew` on macOS); if any prerequisite or install attempt fails, warns the user with the actual error and asks whether to continue without scanning or stop. For a whole-repository run (no argument), maintains a `.secrets.baseline` file at the repository root and reports only secrets that are new since the last baseline or were never triaged (audited); for a scoped run (`<path-or-glob>` argument) it scans just that path ad hoc and reports every finding, without touching the baseline. Invoke as `/iru-check-security` to scan the whole repository, or `/iru-check-security <path-or-glob>` to scope the scan to specific files/directories. Use whenever the user wants a secret-scanning pass before committing/pushing/opening a PR, instead of eyeballing diffs for accidentally committed credentials.
allowed-tools: Read Bash(detect-secrets *) Bash(pip install *) Bash(pip3 install *) Bash(pipx install *) Bash(brew install *) Bash(winget install *) Bash(choco install *) Bash(python *) Bash(python3 *) Bash(which *) Bash(command -v *) Bash(uname *) Bash(git status *) Bash(git diff *) Bash(git ls-files *)
model: haiku
---

# Check Security

Run `detect-secrets` against the repository (or a scoped path) to catch secrets that were accidentally committed
or staged, and report every finding clearly enough to act on. This skill only scans and reports — it never
removes, rotates, or edits a discovered secret, and never stages or commits the baseline file it may create.

## Step 1 — Check whether `detect-secrets` is installed

Run `command -v detect-secrets` (or `detect-secrets --version`). If it succeeds, skip to Step 4.

## Step 2 — Check whether Python is installed

`detect-secrets` is a Python package — installing it via `pip`/`pip3`/`pipx` requires a working Python first.
Run `command -v python3` or `command -v python` (or `python3 --version` / `python --version`).

- **Found**: continue to Step 3.
- **Not found**: determine the platform first (`uname -s`):
  - **Linux or macOS** (`uname -s` reports `Linux` or `Darwin`): both ship Python by default, so a genuine
    absence here is unusual. Warn the user explicitly that Python is missing and is required before
    `detect-secrets` can be installed, then use `AskUserQuestion` to ask whether to **stop here** or
    **continue without scanning** — same as the failure path in Step 3. Don't attempt to install Python
    yourself on these platforms; system Python is managed differently across distros/versions and isn't this
    skill's call to make.
  - **Windows** (`uname -s` reports something other than `Linux`/`Darwin`, e.g. `MINGW*`/`MSYS*`/`CYGWIN*`, or
    the command isn't found at all): unlike Linux/macOS, Windows doesn't ship Python, so attempt to install it
    before proceeding:
    1. `winget install --id Python.Python.3.12 -e --source winget` (Windows' built-in package manager, present
       on Windows 10/11 by default).
    2. `choco install python -y` (if Chocolatey is available and `winget` failed or isn't present).

    Re-check `command -v python3` / `command -v python` after each attempt, stopping at the first success, then
    continue to Step 3. If both attempts fail, warn the user explicitly — state that Python could not be
    installed and show the actual error output from the last attempt — then use `AskUserQuestion` to ask
    whether to **stop here** or **continue without scanning**, same as Step 3's failure path. Respect whichever
    the user picks; do not retry installation again on your own after the user has answered.

## Step 3 — Attempt installation if missing

Try installation methods in order, re-checking `command -v detect-secrets` after each attempt, and stop at the
first one that succeeds:

1. `pip install detect-secrets`
2. `pip3 install detect-secrets`
3. `pipx install detect-secrets`
4. On macOS (`uname -s` reports `Darwin`) only: `brew install detect-secrets`

If every applicable method fails, warn the user explicitly — state that `detect-secrets` could not be installed
and show the actual error output from the last attempt (don't paraphrase it away) — then use
`AskUserQuestion` to ask whether to:

- **stop here** — report that no scan was performed and why, or
- **continue without scanning** — report that no scan was performed and why, but let the calling flow (if any)
  proceed anyway.

Respect whichever the user picks; do not retry installation again on your own after the user has answered.

## Step 4 — Determine scope

- **Argument provided** (a path or glob): scope the scan to it, ad hoc, without touching any baseline file — go
  to Step 6.
- **No argument**: scope to the whole repository using the baseline workflow — go to Step 5.

## Step 5 — Whole-repository scan via baseline

`detect-secrets` uses a baseline file (`.secrets.baseline`) to remember which findings have already been seen and
triaged, so a run only needs to surface what's new.

- **No `.secrets.baseline` at the repository root**: create one with `detect-secrets scan > .secrets.baseline`.
  Every finding in a freshly created baseline is "new" by definition — report all of them (Step 7).
- **`.secrets.baseline` already exists**: before rescanning, keep a copy of its current contents (e.g. `Read` it,
  or note its `git diff` is empty beforehand) so you can tell what changed. Then run
  `detect-secrets scan --baseline .secrets.baseline`, which rescans the codebase and updates the file in place,
  preserving any labels from prior audits. Compare the old and new contents (`git diff .secrets.baseline` if it's
  tracked, otherwise the copy you kept) to identify:
  - **newly appeared entries** — not present in the old baseline at all.
  - **entries still lacking a triage label** (no `is_secret: true`/`false` recorded for them, i.e. never
    resolved by `detect-secrets audit`) — these are outstanding regardless of whether they're new this run.
  Entries already labeled `is_secret: false` in the old baseline are confirmed false positives; don't re-report
  them. Entries already labeled `is_secret: true` are known, already-accepted findings — mention them only as a
  reminder that they remain in the codebase, not as new alarms.

Go to Step 7 to report.

## Step 6 — Scoped ad hoc scan

Run `detect-secrets scan <path-or-glob> --all-files` and report every finding from its output directly — there
is no baseline in this mode, so every result is reported regardless of whether it would otherwise be "known."

Go to Step 7 to report.

## Step 7 — Report

State plainly whether the scan ran at all (per Steps 1–3). If it did, report:

- Whether this was a whole-repository (baseline) or scoped (ad hoc) run.
- Every finding that needs attention: file path, line number, and secret type (from the `type` field), grouped by
  file. For baseline runs, label each as new or previously-flagged-but-unaudited.
- If a `.secrets.baseline` file was created or updated, say so explicitly and note that it now belongs in the
  repository (the user can commit it) but that this skill does not stage or commit anything itself.
- If anything is flagged, recommend the user either remove/rotate the real secret, or run
  `detect-secrets audit .secrets.baseline` themselves to interactively mark false positives — do not run `audit`
  on the user's behalf, since labeling a finding as a false positive is a judgment call only they should make.
- If the scan found nothing to flag, report a clean result plainly.
