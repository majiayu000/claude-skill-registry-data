---
name: github-auth-debug
description: >-
  Diagnose and fix the "git push works but `gh` fails" auth split on macOS — where the GitHub CLI and git consult different credential stores and drift apart — non-destructively, without over-engineering. Trigger when the user says "git push works but gh fails", "gh auth is broken", "token in keyring is invalid", "gh auth status fails", "fix/unify gh and git auth", "re-auth GitHub CLI", "gh 403 SSO/SAML", or when a `gh` command fails mid-session with an auth/keyring/TLS error while `git` still works. Leads with two guardrails: (1) inside a sandboxed shell `gh` gives a FALSE "invalid token" — re-check unsandboxed before concluding anything; (2) one failure does not justify re-architecting credentials — `gh auth setup-git` is the recommended minimal fix, escalate to GCM/SSH/PAT only after a second reproducible failure. Do NOT use for first-time GitHub setup with no prior auth (that's just `gh auth login`), for SSH-key generation requests, or for non-GitHub credential issues.
---

# GitHub Auth Debug

Fix the classic macOS split where `git push`/`pull` keeps working but `gh` fails with "The token in keyring is invalid" — because `gh` stores its OAuth token in its own keyring while `git` uses a separate credential helper (usually `osxkeychain`), and the two have drifted. The job is to unify them on one source of truth **non-destructively**, and to stop **before** over-engineering.

## Read this before touching anything

**Guardrail 1 — the sandbox lies about `gh`.** Inside a sandboxed shell (e.g. Claude Code's default Bash), `gh auth status` falsely reports "token in keyring is invalid" and `gh` throws TLS cert errors, because it cannot reach the macOS keychain. `git` reads `osxkeychain` fine while sandboxed; `gh` does not. **Always re-run `gh` auth checks UNSANDBOXED before concluding the token is bad.** A sandboxed "invalid" is not evidence.

**Guardrail 2 — one failure is not a pattern.** `gh auth setup-git` is GitHub's recommended way to bridge gh and git for HTTPS — it is the minimal correct fix, not a band-aid. Do **not** propose Git Credential Manager, SSH keys, or manual PATs off a single incident. Escalate only after a **second, reproducible** failure that the simple fix demonstrably cannot prevent — and name that failure first.

## Step 1 — Diagnose (run `gh` unsandboxed)

```bash
gh auth status                                          # unsandboxed; ignore a sandboxed "invalid"
git config --get-all credential.helper                  # generic helper (often osxkeychain)
git config --get-all "credential.https://github.com.helper"   # host-pinned helper (gh's, if set)
echo "GITHUB_TOKEN=${GITHUB_TOKEN:-<unset>}"            # if set, it overrides gh — unset it
```

"Drift" is not one failure mode but a cluster of separate causes. Check these before re-architecting anything:

- a stale / revoked / expired token
- a `GITHUB_TOKEN` (or `GH_TOKEN`) env var overriding gh's stored token
- SAML/SSO authorization revoked for the org
- an org token policy or OAuth app restriction
- two credential helpers racing (an old `osxkeychain` PAT vs gh's OAuth token)

If the token is actually valid unsandboxed, **stop — there is no problem to fix.**

## Step 2 — Re-auth (INTERACTIVE — hand to the human)

If the token is genuinely bad, re-auth via the OAuth web flow. This opens a browser and needs a one-time code, so **Claude cannot drive it** — give the operator the exact command:

```bash
gh auth login --hostname github.com --git-protocol https --web
```

Tell them to pick the account that owns the repos. When it finishes, a `gho_` token = OAuth = good. Wait for them to confirm before continuing.

## Step 3 — Unify so they can't drift again

```bash
gh auth setup-git --hostname github.com
```

This pins `github.com` to `!gh auth git-credential`, so git asks gh for credentials. **Leave the generic `credential.helper` (`osxkeychain`) in place** — it's the harmless fallback for other hosts; removing it is unnecessary and risks breaking non-GitHub remotes.

## Step 4 — Verify (unsandboxed; substitute the org/repo)

```bash
gh api user -q .login
gh repo view <ORG>/<REPO> --json nameWithOwner,viewerPermission   # also catches SAML/SSO
git config --get-all "credential.https://github.com.helper"        # expect the gh helper line
git ls-remote --heads https://github.com/<ORG>/<REPO>.git >/dev/null && echo "git remote OK"
```

Expect: the login, a permission (`ADMIN`/`WRITE`), the `!… gh auth git-credential` helper, and `git remote OK`. A **403 with an SSO message** from `gh repo view` means the token needs SAML authorization — have the operator open the URL gh prints and authorize it for the org. (No local clone? `gh repo clone <ORG>/<REPO>` to a temp dir for the `ls-remote` check, or skip that one sub-check.)

## Step 5 — Stop conditions

- **All checks pass → DONE.** Report: gh account, token type (`gho_` = OAuth = good), scopes, and the three check results. Install nothing else.
- **Still failing →** re-run `gh auth login` (Step 2). Do not patch files.
- **Second, reproducible failure →** only now is it worth discussing GCM (multi-host Git workflows) or SSH (if the pain is specifically HTTPS token/helper churn). Name the exact reproducible failure before recommending either.

## When NOT to fire

- First-time GitHub setup with no prior auth at all — that's just `gh auth login`, not a drift fix.
- The user explicitly wants SSH keys / SSH commit signing — different mechanism.
- Non-GitHub credential issues (GitLab, Bitbucket, Azure DevOps), or CI/automation token setup.
- A genuinely confirmed second failure where the user has already asked to migrate to GCM/SSH — go do that, don't re-run this loop.

## Safety rules

- **Never hand-edit `~/.config/gh/hosts.yml`.** If auth is wrong, re-run `gh auth login` — don't patch the file.
- Non-destructive only: never `gh auth logout`, never delete keychain entries, never remove the existing `osxkeychain` helper.
- Run the actual re-auth (`gh auth login --web`) as the operator — it's interactive and writes to their keychain; Claude diagnoses and verifies, the human authenticates.
- Treat a sandboxed `gh` "invalid token" as inconclusive, never as a reason to logout/re-auth/re-architect.
