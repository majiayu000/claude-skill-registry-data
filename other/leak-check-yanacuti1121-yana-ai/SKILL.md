---
name: leak-check
description: Scan codebase and git history for leaked secrets — API keys, tokens, passwords, private keys. Uses whispers-style regex patterns + gitleaks. Run as /leak-check before any git push. Alerts on Claude API keys, GitHub tokens, AWS credentials, and generic high-entropy strings.
origin: Skyscanner/whispers + gitleaks/gitleaks (MIT) + marionevra/awesome-ai-agents-security patterns
license: MIT
version: 1.0.0
compatibility: bash, git, any project type
---

# leak-check

## When to Use

- Before every `git push` (add to pre-push hook)
- After adding new config files, .env samples, or API integration code
- When onboarding a new developer — scan the full history
- Whenever the CI pipeline flags a suspicious commit
- Triggered by: `/leak-check`, "scan for leaked secrets", "check for exposed tokens", "are there any API keys in the repo"

## Do NOT use for

- Runtime secret rotation (use vault/SSM for that)
- Encrypting secrets — this is detection only, not remediation
- Replacing a proper secrets manager (see `supply-chain-security` skill for full supply-chain hardening)

---

## Quick Scan (regex-based, no install required)

```bash
#!/usr/bin/env bash
# Fast in-repo scan without external tools

PATTERNS=(
  # Anthropic / Claude
  "sk-ant-[a-zA-Z0-9_-]{20,}"
  # OpenAI
  "sk-[a-zA-Z0-9]{48}"
  # GitHub tokens
  "gh[pos]_[A-Za-z0-9_]{36}"
  "github_pat_[A-Za-z0-9_]{82}"
  # AWS
  "AKIA[0-9A-Z]{16}"
  "aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}"
  # Generic private key
  "-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"
  # Generic high-entropy assignment
  "(api_key|apikey|secret|password|token|passwd)\s*[=:]\s*['\"][A-Za-z0-9+/=_-]{20,}['\"]"
)

FOUND=0
for pattern in "${PATTERNS[@]}"; do
  matches=$(git grep -rniE "$pattern" -- ':!*.lock' ':!node_modules' ':!vendor' 2>/dev/null || true)
  if [[ -n "$matches" ]]; then
    echo "LEAK DETECTED — pattern: $pattern"
    echo "$matches"
    FOUND=$((FOUND+1))
  fi
done

# Also scan git log for secrets in commit messages
git log --all --oneline | grep -iE "(api.?key|secret|password|token)" | head -5 && \
  echo "WARNING: suspicious words found in commit messages — review above"

[[ $FOUND -eq 0 ]] && echo "CLEAN — no secrets detected" || exit 1
```

---

## Full Scan with gitleaks

```bash
# Install (one-time)
brew install gitleaks          # macOS
# or: docker run --rm -v $(pwd):/path zricethezav/gitleaks

# Scan working directory
gitleaks detect --source . --verbose

# Scan entire git history
gitleaks detect --source . --log-opts="--all" --verbose

# Generate SARIF report for GitHub
gitleaks detect --source . --report-format sarif --report-path gitleaks-report.sarif
```

---

## Pre-Push Hook Integration

```bash
# .git/hooks/pre-push (make executable: chmod +x .git/hooks/pre-push)
#!/usr/bin/env bash
echo "[yamtam/leak-check] Scanning for secrets before push..."

# Quick regex scan
FOUND=0
for pattern in \
  "sk-ant-[a-zA-Z0-9_-]{20,}" \
  "AKIA[0-9A-Z]{16}" \
  "gh[pos]_[A-Za-z0-9_]{36}" \
  "-----BEGIN.*PRIVATE KEY-----"; do
  if git grep -rqiE "$pattern" -- ':!*.lock' ':!node_modules' 2>/dev/null; then
    echo "BLOCKED: secret pattern detected ($pattern)"
    FOUND=$((FOUND+1))
  fi
done

[[ $FOUND -gt 0 ]] && exit 1
echo "[leak-check] CLEAN — push allowed"
exit 0
```

---

## Remediation Steps (If Leak Found)

```bash
# 1. Invalidate the leaked credential IMMEDIATELY (before anything else)
#    Claude API: anthropic.com/console → API Keys → Revoke
#    GitHub: Settings → Developer settings → Personal access tokens → Delete

# 2. Remove from working tree
echo "SECRET_KEY=" > .env   # replace with placeholder

# 3. Rewrite git history (use BFG for large repos)
# Option A — BFG (recommended for large histories)
java -jar bfg.jar --replace-text patterns.txt .git

# Option B — git filter-repo
git filter-repo --path-glob '**/.env' --invert-paths

# 4. Force push (requires human authorization — see git-push-enforcement.md)
git push --force-with-lease

# 5. Log the incident
bash core/scripts/secure-logger.sh "incident" "secret leaked: <type>, revoked, history rewritten at $(git rev-parse HEAD)"
```

---

## CI Integration (GitHub Actions)

```yaml
# .github/workflows/secret-scan.yml
name: Secret Scan
on: [push, pull_request]
jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Anti-Fake-Pass Checklist

- [ ] Scan ran against full git history (`--all`), not just working directory
- [ ] Anthropic/Claude API key pattern `sk-ant-*` explicitly in scan patterns
- [ ] Pre-push hook installed and executable (verify: `ls -la .git/hooks/pre-push`)
- [ ] `.env` files in `.gitignore` — confirm with `git check-ignore -v .env`
- [ ] Any detected secrets invalidated in the provider console BEFORE history rewrite
- [ ] Incident logged to `core/memory/audit/agent-actions.log` via secure-logger.sh
- [ ] CI gitleaks action runs on every PR (no merge without CLEAN status)
