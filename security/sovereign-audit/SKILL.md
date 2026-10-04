---
name: sovereign-audit
description: "Produce a single consolidated hardening report for the DSH node. Runs audit.sh, dome-check.sh, and machine-probe.py, parses their outputs, and writes one markdown file listing every passing check, every failure with a specific remediation command, and a top-line verdict (ALL GREEN / N ISSUES). Non-destructive — reads only, no auto-fix."
---

You are producing a single human- and AI-readable report on the DSH node's current hardening posture. The three subcomponent scripts (`audit.sh`, `dome-check.sh`, `machine-probe.py`) each surface their own findings; this skill's job is to merge them into one authoritative view with specific remediation for every gap.

## 1. Run the three probes in order

```bash
cd "$DOME_ROOT"
TS=$(date -u +%Y%m%dT%H%M%SZ)
OUT="logs/sovereign-audit-$TS.md"
mkdir -p logs

# Fresh machine probe first (dome-check depends on it)
.venv/bin/python scripts/machine-probe.py > /tmp/audit-probe.out 2>&1

# Security audit (read-only)
bash scripts/audit.sh > /tmp/audit-audit.out 2>&1

# Full protocol check (may auto-fix screen-lock + DNS; that's intended)
bash scripts/dome-check.sh > /tmp/audit-dome-check.out 2>&1 || true
```

Note: `dome-check.sh` exits non-zero if any protocol fails, which is fine — we want the report, not a hard exit.

## 2. Parse the machine profile

```python
import json, sys
sys.path.insert(0, "$DOME_ROOT")
from agents.core.machine import get_profile, summary_one_liner, security_posture

profile = get_profile()
line = summary_one_liner()
posture = security_posture()
```

Fields you'll quote in the report:

- `summary_one_liner()` → one-line machine identity
- `profile["tier"]` → sovereign/guardian/scout/seed
- `profile["storage"]["filevault"]`
- `profile["security"]` → all the posture flags
- `profile["runtime"]` → Python/Node/Ollama/Docker versions

## 3. Parse the audit output

`audit.sh` emits `✅` / `❌` / `⚠️` lines. Count them and bucket by category:

```python
from pathlib import Path
import re

audit_text = Path("/tmp/audit-audit.out").read_text()
passes = re.findall(r"^✅ (.+)$", audit_text, re.M)
fails  = re.findall(r"^❌ (.+)$", audit_text, re.M)
warns  = re.findall(r"^⚠️  ?(.+)$", audit_text, re.M)
```

## 4. Parse the dome-check output

Same pattern but dome-check also includes auto-fixes:

```python
dc_text = Path("/tmp/audit-dome-check.out").read_text()
dc_passes = re.findall(r"^✅ (.+)$", dc_text, re.M)
dc_fails  = re.findall(r"^❌ (.+)$", dc_text, re.M)
dc_fixed  = re.findall(r"^🔧 (.+)$", dc_text, re.M)
```

Extract the summary counts from the trailing block:

```python
m = re.search(r"Passed:\s+(\d+).*Fixed:\s+(\d+).*Failed:\s+(\d+)", dc_text, re.S)
```

## 5. Build the remediation table

For every failure, attach the exact fix command. The known mappings:

| Failed check | Remediation |
|---|---|
| `Firewall OFF` | `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on` |
| `Stealth mode OFF` | `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setstealthmode on` |
| `FileVault OFF` | Manual: System Settings → Privacy & Security → FileVault |
| `SIP disabled` | Manual: reboot into Recovery → `csrutil enable` |
| `Screen lock OFF` | `defaults write com.apple.screensaver askForPassword -int 1 && defaults write com.apple.screensaver askForPasswordDelay -int 0` |
| `No GPG key` | `bash scripts/sovereign-secrets.sh` |
| `pass store not initialized` | `bash scripts/sovereign-secrets.sh` |
| `Git commit signing OFF` | `git config --global commit.gpgsign true` |
| `DNS → <not 127.0.0.1>` | `sudo networksetup -setdnsservers Wi-Fi 127.0.0.1 && sudo brew services start dnscrypt-proxy` |
| `dnscrypt-proxy not running` | `sudo brew services start dnscrypt-proxy` |
| `Python import errors` | `source .venv/bin/activate && pip install -r compute/requirements.txt` |
| `TypeScript errors` | `pnpm install && pnpm typecheck` (review errors) |
| `SQLite DB missing` | `python3 scripts/register-claude.py` |
| `ChromaDB empty` | `python3 scripts/ingest.py` |
| `N uncommitted change(s)` | `git -C "$DOME_ROOT" status` then review & commit |
| `.env NOT in .gitignore` | `echo '.env' >> .gitignore && git add .gitignore && git commit -m 'chore: gitignore .env'` |

For any failure not in this table, return "Manual review — see logs/sovereign-audit-<timestamp>.md"

## 6. Write the report

Structure (emit to `$OUT` which is `logs/sovereign-audit-<timestamp>.md`):

```markdown
# DSH Sovereign Audit — <ISO-8601 timestamp>

## Verdict
<ALL GREEN> | <N ISSUES REQUIRE MANUAL ACTION>

## Node
`<summary_one_liner output>`

Tier: **<tier>**

## Security posture
| Control | State |
|---|---|
| FileVault | ✅ / ❌ |
| SIP | ✅ / ❌ |
| Gatekeeper | ✅ / ❌ |
| Firewall | ✅ / ❌ |
| Private DNS | ✅ / ❌ |
| Secrets backend | ✅ / ❌ |

## Passes
- <count> from audit.sh
- <count> from dome-check.sh

## Failures (if any)
| Check | Source | Fix |
|---|---|---|
| <failure> | audit.sh | <command> |
| <failure> | dome-check | <command> |

## Auto-fixed during this run
- <list from dome-check's 🔧 lines>

## Runtime
- Python: <version>
- Node: <version>
- Ollama: <running? yes/no>
- Docker: <present? yes/no>

## Source outputs
- `/tmp/audit-audit.out` — 100 lines, ended <exit code>
- `/tmp/audit-dome-check.out` — <X> lines, ended <exit code>
- `/tmp/audit-probe.out` — machine-probe summary

## Next action
<one sentence — what the user should do first>
```

Save, print the path, and emit a 2-line summary to stdout for the calling agent:

```
✅ Audit complete: logs/sovereign-audit-<timestamp>.md
<0/N issues>
```

## 7. When the report is used downstream

Other skills may call this skill and parse the first two lines of the markdown:

- Line 1: `# DSH Sovereign Audit — ...`
- Line 2: the verdict paragraph (`ALL GREEN` or `N ISSUES REQUIRE MANUAL ACTION`)

Keep those two lines machine-parseable. Everything else in the report is human prose.

## Non-negotiables

- **Never auto-fix.** This skill is read-only. The remediation column is suggestions; the user or a separate skill runs them.
- **Never exfiltrate the report to a remote address.** The audit contains the node's full security posture — it's sensitive to anyone but the owner.
- **Never skip failed parse cases.** If `dome-check.sh` produced output in an unexpected format, flag it in the report rather than pretending it succeeded.
- **Never commit `logs/sovereign-audit-*.md`.** `logs/*.md` is gitignored; reports accumulate locally and can be hand-archived if useful.
- **Never run this skill in parallel with `sovereign-lockdown`.** Lockdown is writing state; audit is reading state. Sequencing matters.
