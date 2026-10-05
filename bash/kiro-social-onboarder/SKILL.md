---
name: kiro-social-onboarder
description: Automate Kiro CLI account onboarding with social Google or GitHub login through the required HTTP proxy, local Kiro SQLite auth cleanup without logout, email-aware llm-access Kiro account import, proxy assignment, balance refresh, and KIRO STUDENT/1000-credit verification. Use when adding or refreshing a social Kiro account, replacing a mistakenly imported AWS/IDC Kiro login, or verifying that a local Kiro social account is student-tier before exposing it through StaticFlow/llm-access.
---

# Kiro Social Onboarder

## Boundaries

- Never run `kiro-cli logout`; remove local metadata keys instead.
- Never store provider passwords, 2FA codes, access tokens, refresh tokens, or raw token JSON in the skill or handoff.
- Use the HTTP proxy for the whole login flow. Default proxy: `http://127.0.0.1:11111`.
- Delete llm-access accounts only by exact explicit name, and only when the user asked to replace or clean that account.
- Keep the final verification centered on `kiro-cli whoami`, `auth_method=social`, the expected social provider, and refreshed Kiro balance.

## One-Command Flow

Use the bundled script for the standard path:

```bash
read -rsp 'Google password: ' KIRO_GOOGLE_PASSWORD; echo
export KIRO_GOOGLE_PASSWORD
python3 skills/kiro-social-onboarder/scripts/onboard_kiro_social_google.py \
  --email user@example.com \
  --account-name kiro-user-google-social \
  --replace-account
unset KIRO_GOOGLE_PASSWORD
```

For refreshing an existing GitHub-backed account that has fallen into
`auth_401`, use the GitHub-specific script without `--account-name`. It probes
the refreshed credentials with a temporary account, matches the upstream
`user_id` to an existing llm-access Kiro account, then writes the new token
pair back to that existing account:

```bash
python3 skills/kiro-social-onboarder/scripts/onboard_kiro_social_github.py \
  --manual-timeout-seconds 600
```

For credential-prefilled GitHub login, put the password in an environment
variable rather than a shell argument. The helper fills the GitHub username and
password, then waits for manual 2FA or unusual verification:

```bash
read -rsp 'GitHub password: ' KIRO_GITHUB_PASSWORD; echo
export KIRO_GITHUB_PASSWORD
python3 skills/kiro-social-onboarder/scripts/onboard_kiro_social_github.py \
  --github-login gfryuuu \
  --manual-timeout-seconds 600
unset KIRO_GITHUB_PASSWORD
```

2FA codes are never passed to the script; complete 2FA and unusual verification
in the launched browser when prompted.

For importing a new GitHub-backed account under an explicit name, pass
`--account-name`:

```bash
python3 skills/kiro-social-onboarder/scripts/onboard_kiro_social_github.py \
  --account-name kiro-user-github-social
```

The script:

1. Backs up `~/.local/share/kiro-cli/data.sqlite3`.
2. Deletes only Kiro auth metadata keys from local SQLite.
3. Starts Kiro social device authorization through the proxy.
4. Opens an isolated Chrome profile through the proxy and drives the visible provider/Kiro pages through DevTools.
   It must inspect the DOM and click real `button`/`a`/`role=button` controls such as `Next`, `Approve`, `Continue`, and `Restart`.
5. Approves the Kiro device code and polls the social token endpoint.
6. Writes `kirocli:social:token` and `api.codewhisperer.profile` locally.
7. Verifies `kiro-cli whoami` through the proxy and parses the `Email:` line
   when present.
8. Runs `kiro-local-account-importer` dry-run and apply against `http://127.0.0.1:19182`.
   Proxy assignment is delegated to the importer, which chooses the least-used
   active United States proxy first and uses latency only as a tie-breaker.
9. Writes parsed email into the llm-access Kiro account through the same
   `import-auth` path that updates the refreshed social token.
10. Refreshes balance and fails unless the account is `KIRO STUDENT` with at least `1000` usage limit by default.
11. Removes temporary browser profiles and token response files.

The GitHub script follows the same Kiro/device-code/import/verification path.
Its DevTools helper can submit the GitHub login form when `--github-login` and
`KIRO_GITHUB_PASSWORD` are available, then it waits for 2FA, device
verification, or OAuth consent in the visible browser session. It also assists
Kiro-side `Continue`/`Approve` controls. When `--account-name` is omitted, it
uses a temporary probe account only to refresh balance and identify the
existing account by upstream `user_id`; the probe account is deleted when it is
not automatically removed by duplicate detection.

## Kiro Admin Lookup Rules

- Kiro's device authorization API expects `loginProvider: "Github"` for GitHub
  login. Do not send the display spelling `GitHub`; the API rejects it.
- Do not assume `GET /admin/kiro-gateway/accounts?limit=10000&offset=0`
  returns every account. The admin API caps `limit` server-side, so full-list
  scans must follow `has_more` with increasing `offset`.
- For an exact suspected account name, prefer the server-side search first:
  `GET /admin/kiro-gateway/accounts?q=<account-name>`.
- For 401 repair batches, prefer the issue filter:
  `GET /admin/kiro-gateway/accounts?issue=auth_401`.
- If a local scan and the admin UI disagree, treat the scan as suspect until
  the query is repeated with `q=...` or a verified paginated fetch.

## Required Options

- `--email`: Google account email.
- `--account-name`: llm-access Kiro account name. Prefer `kiro-<localpart>-google-social`.
- Password source: `KIRO_GOOGLE_PASSWORD` by default, or interactive hidden prompt.

For GitHub:

- `--account-name`: optional. Omit it when refreshing an existing 401 account
  and let the script match by upstream `user_id`. Provide it only for explicit
  new-account import or exact-name replacement. Prefer
  `kiro-<localpart>-github-social` for new accounts.
- `--github-login`: optional GitHub username or email for login prefill. If
  omitted and `--account-name` is present, the script may use `--account-name`
  as the GitHub login when a password is available.
- GitHub password source: `KIRO_GITHUB_PASSWORD` by default via
  `--password-env`. Do not pass passwords on the command line.
- No 2FA option is accepted; use the launched browser for 2FA.

## Useful Options

- `--proxy http://127.0.0.1:11111`: override the login proxy.
- `--admin-base-url http://127.0.0.1:19182`: override local mapped llm-access admin API.
- `--replace-account`: delete the exact target account before importing; for
  safety this requires `--account-name`.
- `--delete-account-name NAME`: delete an exact mistakenly imported account before the flow.
- `--manual-timeout-seconds 300`: time allowed for manual CAPTCHA/MFA completion if Google requires it.
- `--expect-usage-limit 1000`: required usage limit for verification.
- `--no-expect-student`: allow non-student accounts, but still print the balance.

For GitHub, `--manual-timeout-seconds` defaults to `600` to allow manual 2FA
and OAuth consent. `--password-env NAME` changes the environment variable used
for GitHub password prefill.

## Failure Handling

- If Google shows CAPTCHA or MFA, complete it in the launched isolated browser; the script keeps polling until the manual timeout.
- If GitHub shows login, 2FA, device verification, or OAuth consent, complete it
  in the launched isolated browser; the script keeps polling until the manual
  timeout.
- If Google shows `Something went wrong` with `Restart`, click `Restart` and continue the same OAuth flow.
- If the import step fails after account creation, query the exact account name before retrying. Do not create a second account name unless the user requests it.
- If balance is not `KIRO STUDENT` or usage limit is below `1000`, report the account as not acceptable and do not hide the failure.
- If a wrong AWS/IDC account was imported, delete that exact account via llm-access admin API, then rerun the social flow. Do not call logout.

## Verification Commands

```bash
HTTP_PROXY=http://127.0.0.1:11111 \
HTTPS_PROXY=http://127.0.0.1:11111 \
ALL_PROXY=http://127.0.0.1:11111 \
kiro-cli whoami

curl -fsS -X POST \
  http://127.0.0.1:19182/admin/kiro-gateway/accounts/<account-name>/balance \
  | jq '{subscription_title, usage_limit, remaining, current_usage, user_id}'
```
