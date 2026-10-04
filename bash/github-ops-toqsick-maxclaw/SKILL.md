---
name: github-ops
description: "gh-CLI-Patterns für MaxClaw: PR-Erstellung mit Templating, Issue-Triage mit Label-Dispatch, Conflict-Resolution via rebase/merge. Trigger bei Code-Reviews, Repo-Push, PR-Monitoring (cron) und Issue-Management."
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
  - windows
triggers:
  - cron: github-pr-monitor (0 9,17 * * *)
  - workflow: nach erfolgreichem greybel-Build → auto-PR
  - manual: bei Issue-Triage oder PR-Merge
metadata:
  openclaw:
    tags:
      - collaboration
      - github
      - gh-cli
      - ops
---

# github-ops

Sammlung robuster `gh`-CLI-Patterns, die MaxClaw als "PR-Manager" für seine
Repos einsetzt (greyhack-tools, hermes-v7, MaxClaw selbst). Alle Skripte
verwenden JSON-Output für stabiles Parsing.

## When to use

- Nach jedem Build: PR-Body automatisch erstellen und PR öffnen.
- Cron: zweimal täglich Toqsick-Repos auf offene PRs/Issues scannen.
- Ad-hoc: Triage-Labels setzen, Reviews triggern, Konflikte lösen.

## Pattern

### 1. PR-Erstellung mit Templating (`scripts/gh-pr-create.sh`)

```bash
#!/usr/bin/env bash
# gh-pr-create.sh — erstellt PR mit standardisiertem Body
set -euo pipefail
REPO="${1:?owner/repo}"; BASE="${2:-main}"; HEAD="${3:-$(git branch --show-current)}"
TITLE="${4:-$(git log -1 --pretty=%s)}"

# Body aus Commit-Messages + Diff-Stat
BODY="$(cat <<EOF
## Was geändert
$(git diff "$BASE...$HEAD" --stat)

## Commits
$(git log "$BASE..$HEAD" --pretty='- %s' | head -20)

## Verifikation
- [ ] greybel build grün
- [ ] greyscript-linter OK
- [ ] manueller Sandbox-Test
EOF
)"

gh pr create \
  --repo "$REPO" \
  --base "$BASE" --head "$HEAD" \
  --title "$TITLE" --body "$BODY" \
  --label "maxclaw-auto" --reviewer Toqsick
```

### 2. Issue-Triage (`scripts/gh-issue-triage.sh`)

```bash
#!/usr/bin/env bash
# gh-issue-triage.sh — vergibt Labels nach Keyword-Heuristik
set -euo pipefail
REPO="${1:?owner/repo}"
mapfile -t issues < <(gh issue list --repo "$REPO" --state open --json number,title \
  --jq '.[] | "\(.number)|\(.title)"')

for entry in "${issues[@]}"; do
  num="${entry%%|*}"; title="${entry#*|}"
  case "${title,,}" in
    *bug*|*crash*|*error*)  label="bug" ;;
    *feat*|*add*|*neu*)     label="enhancement" ;;
    *doc*|*readme*)         label="documentation" ;;
    *sec*|*cve*)            label="security" ;;
    *) continue ;;
  esac
  gh issue edit "$num" --repo "$REPO" --add-label "$label"
  echo "  #$num → $label"
done
```

### 3. Conflict-Resolution-Workflow

```bash
#!/usr/bin/env bash
# gh-conflict-resolve.sh — interaktiver Rebase auf main + Status-Check
set -euo pipefail
REPO="${1:?owner/repo}"; PR="${2:?pr-number}"
BRANCH="$(gh pr view "$PR" --repo "$REPO" --json headRefName -q .headRefName)"

gh repo set-default "$REPO"
git fetch origin
git checkout "$BRANCH"
git rebase origin/main

# Konflikte melden → User manuell lösen lassen
if git status --porcelain | grep -q '^UU'; then
  echo "Konflikte in:"
  git diff --name-only --diff-filter=U
  exit 2
fi

git push --force-with-lease
gh pr ready "$PR" --repo "$REPO"
```

### 4. PR-Monitor (für Cron)

```bash
#!/usr/bin/env bash
# gh-pr-monitor.sh — täglich offene PRs zusammenfassen
set -euo pipefail
REPOS=("Toqsick/greyhack-tools" "Toqsick/hermes-v7" "Toqsick/MaxClaw")
OUT=""
for r in "${REPOS[@]}"; do
  cnt="$(gh pr list --repo "$r" --state open --json number -q 'length')"
  OUT+="• $r: $cnt open\n"
done
printf "$OUT" | tee ~/.cache/maxclaw/pr-monitor.txt
```

## Pitfalls

- ❌ **Plain `git push --force`** → remote-History zerstört. Immer
  `--force-with-lease` (verweigert bei divergierendem Remote).
- ❌ `gh pr create` mit Edit-Buffer blockt in CI → `--body-file` statt
  `--body "..."` (oder Body via Heredoc).
- ❌ `gh issue list` paginiert **nicht** automatisch; bei >100 Issues:
  `--limit 200 --state all` und manuell loopen.
- ✅ JSON-Output (`--json ... -q '.feld'`) ist stabiler als `--template`.
- ✅ Triage-Heuristik bleibt Heuristik — bei Unsicherheit **kein** Label,
  statt Falsch-Tagging.
- ✅ `gh auth status` am Skriptanfang prüfen, sonst wirft jede Zeile Auth-Errors.

## Cron-Beispiel

```cron
# 09:00 + 17:00 — PR-Monitor
0 9,17 * * * /home/bratan/.openclaw/skills/github-ops/scripts/gh-pr-monitor.sh
```