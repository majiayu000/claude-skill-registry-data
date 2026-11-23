---
name: audit-secrets
description: >
  Scan the working tree and recent git history for accidentally committed secrets,
  tokens, API keys, private keys, and credentials before they leave the machine. Trigger
  on "did I commit a key", "check for leaked credentials", "did I leak an API key", "is
  there a secret in this diff", "scan for secrets before I push", "I think I pushed a
  password". This skill owns the credential pattern set for the whole repo, including
  the git-history pass where a secret survives after the file is deleted — other skills
  delegate their secret checks here rather than reimplementing them. Always says to
  rotate an exposed credential, not merely remove it.
---

# audit-secrets

You are a secrets detection assistant. Your job is to find credentials, tokens, and sensitive values before they reach a remote repository. Be thorough and systematic.

**Never print a full secret value, anywhere in the response.** Mask every matched
value on first sight and keep it masked — in the finding, in the surrounding prose,
in example commands, and in any sentence where you are arguing the value is _not_
real. "This is AWS's documented example key, `AKIA…`" is exactly the sentence that
leaks it: you may be wrong about which value is a placeholder, and a report that
reproduces the literal is itself a copy of the secret. Dismiss it by category
("matches the AWS documentation example"), never by quoting it in full.

---

## Step 1 — Define the scan scope

Determine what to scan:

- if the user names a path, a diff or a commit range, scan only that
- otherwise scan the full working tree plus recent git history

Establish:

- project root
- whether there is a `.gitignore` to reference
- whether there is a `.env.example` to use as a reference for expected variable names

---

## Step 2 — Scan the working tree for secret patterns

Search all tracked and untracked non-binary files for the following pattern categories:

**High-severity patterns (confirmed credential shapes):**

- Private key blocks: `-----BEGIN (RSA|EC|DSA|OPENSSH|PGP) PRIVATE KEY`
- JWT tokens: three base64 segments separated by dots starting with `eyJ`
- AWS credentials: `AKIA[0-9A-Z]{16}`, `aws_secret_access_key`
- GitHub tokens: `gh[pousr]_[A-Za-z0-9]{36,}`, `github_pat_[A-Za-z0-9_]{50,}`
- npm tokens: `npm_[A-Za-z0-9]{36}`
- Slack tokens: `xox[baprs]-[A-Za-z0-9-]{10,}`
- Anthropic API keys: `sk-ant-[A-Za-z0-9_-]{20,}`
- OpenAI API keys: `sk-(proj|svcacct)-[A-Za-z0-9_-]{40,}`, `sk-[A-Za-z0-9]{48}`
- Stripe keys: `sk_live_`, `pk_live_`, `rk_live_`
- Twilio: `SK[0-9a-fA-F]{32}`
- Generic API key patterns in assignments: `api_key\s*=\s*["'][^"']{16,}["']`
- Database connection strings containing passwords: `://[^:]+:[^@]{6,}@`
- Bearer tokens in source code: `Bearer [A-Za-z0-9\-._~+/]{20,}`

**Medium-severity patterns (high-entropy strings):**

- Strings of 32+ characters that are all hex: `[0-9a-fA-F]{32,}`
- Base64 strings of 40+ characters assigned to a variable with a sensitive-sounding name
- Strings matching password/secret/token/key variable assignments with non-placeholder values

**Low-severity patterns (suspicious names worth reviewing):**

- Variable names containing `password`, `passwd`, `secret`, `token`, `credential`, `private_key`, `auth_key` assigned to non-empty string literals
- Hard-coded localhost credentials with non-default passwords

This list is the source for credential shapes in this skill set. The `guard-hooks` skill
blocks commits on a narrower subset of it (the high-confidence shapes only); when you add a
shape here that is specific enough to block on, add it there too.

Search for locations, not values. Use a search that returns file names and line numbers
(`grep -rnE "<pattern>" . | cut -d: -f1,2`), not one that prints the matching line: a
printed line is a copy of the secret in the transcript. To get the masked form for the
report, use the masking command in Step 3.

Exclude:

- `.git/` directory
- `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`
- Binary files, image files, compiled artifacts
- Test fixture files that clearly contain dummy data (e.g., files named `*.fixture.*`, `*.mock.*`, `*test*`) — flag these separately at lower confidence

---

## Step 3 — Scan recent git history

Check recent history for **the same patterns as Step 2**. Do not hand-type a shorter
list here — a secret matching only a pattern you dropped becomes invisible to the pass
that matters most, since history survives deleting the file:

```bash
while read -r name && read -r pattern; do
  git log --all --since="90 days ago" -G"$pattern" \
    --format="[$name] %h %ad %an" --date=short --name-only
done <<'EOF'
private key
BEGIN ([A-Z]+ )*PRIVATE KEY
JWT
eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.
AWS access key
AKIA[0-9A-Z]{16}|aws_secret_access_key
GitHub token
gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{50,}
npm token
npm_[A-Za-z0-9]{36}
Slack token
xox[baprs]-[A-Za-z0-9-]{10,}
Anthropic API key
sk-ant-[A-Za-z0-9_-]{20,}
OpenAI API key
sk-(proj|svcacct)-[A-Za-z0-9_-]{40,}|sk-[A-Za-z0-9]{48}
Stripe live key
[spr]k_live_
Twilio key
SK[0-9a-fA-F]{32}
connection string with a password
://[^:/ ]+:[^@ ]{6,}@
bearer token
Bearer [A-Za-z0-9._~+/-]{20,}
sensitive name assigned a literal
(api_key|password|passwd|secret|token|credential|private_key|auth_key)[A-Za-z_]*["']?[[:space:]]*[:=][[:space:]]*["'][^"']{8,}
EOF
```

Each pattern prints the commits whose diff adds or removes a matching line, with the
files they touched. It prints no file content, so nothing it finds lands in the
transcript. Do not replace it with `git log -p | grep`: that prints every matching line
in full.

To confirm a hit and get its masked form, print only the masked match, never the line:

```bash
git show <sha>:<path> | grep -oE "<pattern>" | sed -E 's/^(.{4}).*(.{4})$/\1****\2/'
```

If Step 2's pattern list is ever edited, edit this command to match.

For any match found in history:

- record the commit SHA, author, date, and file path
- note whether the secret is still present in the current working tree or was removed in a later commit
- if the secret was introduced and then removed, it is still in git history and needs to be rotated

---

## Step 4 — Inspect `.gitignore` coverage

Compare files that appear to contain secrets against `.gitignore`:

- identify any `.env*`, `*.pem`, `*.key`, `secrets.*`, `config/local.*`, or credential files that are tracked but should be ignored
- identify variable-containing files that are committed and not in `.gitignore`
- flag `.env.example` as safe if it exists and contains only placeholder values (no real credentials)

---

## Step 5 — Rank and report findings

Classify each finding:

| Severity   | Criteria                                                        |
| ---------- | --------------------------------------------------------------- |
| **High**   | Confirmed credential pattern or private key block               |
| **Medium** | High-entropy string with a sensitive variable name              |
| **Low**    | Suspicious variable name with a plausible but unconfirmed value |

For each finding, report:

- severity
- file path and line number
- pattern category (e.g., "AWS access key", "JWT", "database password")
- masked value (show only first 4 + last 4 characters, e.g., `AKIA****ABCD`) — this
  is the only form the value ever appears in, including for findings you go on to
  dismiss as placeholders, fixtures, or documentation examples
- whether it exists in current working tree, git history, or both
- recommended remediation (see Step 6)

If no findings exist, say so explicitly.

---

## Step 6 — Recommend remediation

For each confirmed finding:

**If the secret is only in the working tree (not yet committed):**

- Add the file to `.gitignore`
- Remove or replace the value with an environment variable reference
- Do not commit the file

**If the secret is in committed history:**

- Rotate the credential immediately — assume it is compromised
- Revoke and re-issue the credential with the relevant service
- Purging it from history is a separate, optional step, and the user's decision. It means
  `git filter-repo --path <file> --invert-paths` (or BFG Repo Cleaner) and then a force push
  to every remote, which rewrites history for everyone who has cloned the repo. Explain
  that, say that rotation already makes the leaked value useless, and wait for an explicit
  yes before running either command. Never run them as part of the scan.

**If the secret is in a file that should be gitignored:**

- Add the pattern to `.gitignore`
- Run `git rm --cached <file>` to untrack without deleting locally
- Commit the `.gitignore` change

Never recommend `git rebase -i` or `git commit --amend` as a history-rewriting strategy for secrets — they leave reflog traces. Always recommend `git filter-repo`.
