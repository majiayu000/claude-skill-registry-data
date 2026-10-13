---
name: recon-github-code-leaks
description: >
  Find secrets and internal detail an organisation leaked to public code — GitHub/GitLab repos,
  gists, and commit history. Load during recon of a named org, on "github dorks", "leaked secrets",
  "find API keys", or when employees/repos are in scope. Signals: a company GitHub org, developer
  usernames, an internal domain to grep for.
domain: recon
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
owasp: [A07]
cwe: [CWE-798, CWE-540]
mitre: [T1213, T1552.001]
tools: [trufflehog, gitleaks, github-search, gitrob]
schema_version: 1
---

# GitHub code-leak discovery

## When it applies
Recon of an organisation whose developers publish code. Public repos, gists, and — crucially — old
commits routinely leak API keys, cloud credentials, internal hostnames, and endpoints that open a
foothold no scanner of the live app would find.

## Why it works
Secrets get committed and then "removed" in a later commit — but git keeps history, so the secret is
still reachable. Developers also mirror internal tooling, config, and infrastructure names into
public repos, handing you the attack surface and sometimes the keys to it.

## Method
1. **Map the footprint**: the org's repos, its members' personal repos, and gists (org members often
   leak in personal projects). Note internal domains/usernames to grep for.
2. **Dork the code search**: combine an org/domain term with secret indicators — `"company.com"
   password`, `api_key`, `AKIA`, `BEGIN RSA PRIVATE KEY`, `.env`, `config`, `authorization: bearer`,
   `s3.amazonaws.com company`. Search filenames too (`filename:.env`, `filename:credentials`).
3. **Scan history, not just HEAD**: clone and run `trufflehog`/`gitleaks` over the full history
   (`trufflehog git file://.`), which finds secrets in deleted/old commits and validates live ones.
4. **Pivot on findings**: internal endpoints/hosts → new recon targets; cloud keys → verify scope and
   authorization before use (`cloud-*`); JS/config → app internals.
5. **Handle responsibly**: prove validity minimally (e.g. `sts get-caller-identity` for AWS if in
   scope), never exfiltrate data, and report leaked secrets for rotation.

## Gotchas
- **Stay in scope**: employees' *personal* repos and unrelated orgs may be out of scope — confirm
  before touching, and never use a live credential you aren't authorized to use.
- Many hits are dead/rotated keys — validate before reporting, but report even revoked ones as a
  process finding when the program wants it.
- GitHub code search rate-limits and truncates — combine the web UI, the API, and offline history scans.

## Verify success
You have leaked material tied to the target — a valid credential (verified minimally and in scope),
an internal endpoint/host, or config — that advances the engagement or is a reportable exposure.

## References
truffleHog & gitleaks; GitHub code-search dork lists; the classic AWS-key-in-git incident write-ups.
