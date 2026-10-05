---
name: github-password-rotator
description: Use when a GitHub account password needs to be changed or rotated, or when Codex should log in to GitHub security settings so the user can manually change 2FA/passkeys. Applies when Codex should prefill username/password fields while the user handles 2FA, device checks, CAPTCHA, or suspended-account pages.
---

# GitHub Password Rotator

## Boundaries

- Never pass GitHub passwords on the command line.
- Never print, store, commit, or summarize old passwords, new passwords, 2FA codes, cookies, or session tokens.
- Never print, store, commit, or summarize TOTP/2FA secrets from `2fa.fun`.
- Use an isolated Chrome profile and the HTTP proxy for the whole browser flow. Default proxy: `http://127.0.0.1:11111`.
- Treat 2FA, passkeys, CAPTCHA, unusual verification, and suspended-account pages as manual user steps.
- Do not claim the password changed unless the script reports completion or the user confirms success in the browser.
- For 2FA/passkey changes, use `--login-only`; do not run the password-change flow and try to avoid the password form at runtime.

## Standard Flow

For logging in to GitHub security settings without changing the password, use
`--login-only`. This keeps the isolated browser open after the helper reaches
`https://github.com/settings/security`:

```bash
read -rsp 'Current GitHub password: ' GITHUB_CURRENT_PASSWORD; echo
export GITHUB_CURRENT_PASSWORD
python3 skills/github-password-rotator/scripts/rotate_github_password.py \
  --github-login username \
  --login-only \
  --manual-timeout-seconds 900
unset GITHUB_CURRENT_PASSWORD
```

Use this mode when the user wants to manually change 2FA, passkeys, recovery
methods, or other security settings. The helper only logs in, handles sudo
password confirmation when detected, and stops before any password-change form.

Use environment variables or hidden TTY prompts for both passwords:

```bash
read -rsp 'Current GitHub password: ' GITHUB_CURRENT_PASSWORD; echo
read -rsp 'New GitHub password: ' GITHUB_NEW_PASSWORD; echo
read -rsp 'GitHub TOTP secret for 2fa.fun: ' GITHUB_TOTP_SECRET; echo
export GITHUB_CURRENT_PASSWORD GITHUB_NEW_PASSWORD GITHUB_TOTP_SECRET
python3 skills/github-password-rotator/scripts/rotate_github_password.py \
  --github-login username \
  --manual-timeout-seconds 900 \
  --auto-2fa-fun \
  --create-learning-repo
unset GITHUB_CURRENT_PASSWORD GITHUB_NEW_PASSWORD GITHUB_TOTP_SECRET
```

The helper:

1. Opens `https://github.com/settings/security` in an isolated Chrome profile through the proxy.
2. Fills the GitHub login page with `--github-login` and the current password.
3. If `--auto-2fa-fun` is set and GitHub shows an app-code 2FA prompt, opens or reuses `https://2fa.fun/`, enters the TOTP secret, reads the generated code from `input.faotp.value`, and submits it to GitHub without printing the code.
4. Waits for the user to complete passkey, device verification, CAPTCHA, suspended-account inspection, or any 2FA step that cannot be handled from `2fa.fun`.
5. Handles GitHub sudo password confirmation with the current password when detected.
6. Fills the password-change form with current password, new password, and confirmation.
7. Exits successfully after GitHub reports success, or after a submitted password form collapses back to the `Change password` state without an explicit success message.
8. Navigates back to `https://github.com/settings/security` after a completed submit so browser refresh will not resubmit the password form.
9. When `--create-learning-repo` is set, waits a random 3-10 seconds after the password change before creating the repository, then creates `hello-world-from-<account-slug>` and writes a beginner-friendly English `README.md`.

## Useful Options

- `--github-login USER`: required GitHub username or email.
- `--current-password-env NAME`: defaults to `GITHUB_CURRENT_PASSWORD`.
- `--new-password-env NAME`: defaults to `GITHUB_NEW_PASSWORD`.
- `--totp-secret-env NAME`: defaults to `GITHUB_TOTP_SECRET`; only read when `--auto-2fa-fun` is set.
- `--proxy http://127.0.0.1:11111`: override login proxy.
- `--settings-url URL`: override GitHub password settings URL.
- `--manual-timeout-seconds 900`: time allowed for manual verification.
- `--keep-browser`: keep the isolated browser open after the helper exits.
- `--login-only`: log in to GitHub security settings without reading a new password or submitting the password-change form; implies `--keep-browser`.
- `--auto-2fa-fun`: use the hidden TOTP secret with `2fa.fun` to fill GitHub app-code 2FA prompts.
- `--create-learning-repo`: after password rotation, create a public beginner learning repository named `hello-world-from-<github-login-slug>`.
- `--dry-run`: print redacted plan and verify script wiring without launching a browser or requiring passwords.

## Learning Repository

- Repository name is deterministic: `hello-world-from-<account-slug>`, where the slug lowercases the GitHub login and replaces non-alphanumeric runs with `-`.
- README content must be English, beginner-oriented, and generated from multiple randomized sections at runtime. Do not make it a fixed template keyed only by account name.
- The README should still include the account name in the heading so the repository looks account-specific.
- If GitHub reports the repository already exists or the editor cannot be found, stop with a clear failure instead of silently skipping the repository.

## Failure Handling

- If GitHub shows a suspended/disabled account page, stop the script and record the account in the appeal tracker instead of retrying.
- If the helper times out while GitHub is logged in, inspect the visible browser. Do not scrape or print cookies/tokens.
- If `2fa.fun` is used, read generated codes only from `input.faotp.value`; do not parse arbitrary page text or secret fields as codes.
- If GitHub changed the settings DOM, rerun with `--keep-browser`, inspect visible labels/selectors, then patch `drive_github_password_change.mjs`.
- GitHub may not show a password success flash. After a submit, treat the collapsed password form plus visible `Change password` entry as a completed no-flash state, then force a GET navigation back to the settings URL to avoid refresh resubmission.
- If the password-change form remains visible after submit, do not assume success. Check visible validation text or ask the user to confirm.

## Verification

Dry-run and syntax checks are safe:

```bash
python3 skills/github-password-rotator/scripts/rotate_github_password.py \
  --github-login username \
  --login-only \
  --dry-run

python3 -m py_compile skills/github-password-rotator/scripts/rotate_github_password.py
node --check skills/github-password-rotator/scripts/drive_github_password_change.mjs
```

For live verification, rely on GitHub's success page, the completed no-flash
collapsed form state, a `login_completed` status for `--login-only`, or a
user-confirmed successful login with the new password. Do not log the password
itself.
