---
name: bash-script-builder
description: Generiert produktionsreife Bash-Skripte mit set -euo pipefail, Lint-Self-Check (shellcheck wenn vorhanden), strukturierter Doku und Verifikations-Snippet. Trigger bei jeder neuen Automatisierung (cron, one-shot, Tool-Helper).
version: 1.0.0
author: OpenClaw Agent (MaxClaw Skill-Set)
license: MIT
platforms:
  - linux
  - macos
triggers:
  - workflow: neuer Cron-Job / neuer Helper
  - refactor: bestehende .sh ohne set -euo pipefail
  - manual: "new-bash-script.sh <name>"
metadata:
  openclaw:
    tags:
      - code
      - bash
      - template
      - automation
---

# bash-script-builder

Standardvorlage für jedes Bash-Skript, das MaxClaw schreibt. Erzwingt
robuste Defaults, sodass Skripte auch im 03:00-Cron nicht stillschweigend
fehlschlagen.

## When to use

- Jedes Mal, wenn MaxClaw ein neues `.sh` schreibt.
- Beim Refactor von Alt-Skripten ohne `set -euo pipefail`.
- Für Cron-Helper, die mit `openclaw cron create` registriert werden sollen.

## Pattern

### 1. Boilerplate-Generator (`scripts/new-bash-script.sh`)

```bash
#!/usr/bin/env bash
# new-bash-script.sh — generiert Skript-Boilerplate
set -euo pipefail
NAME="${1:?usage: new-bash-script.sh <name>}"
TARGET="${2:-./$NAME.sh}"

cat > "$TARGET" <<'BASH'
#!/usr/bin/env bash
# =============================================================================
# NAME_PLACEHOLDER — Kurzbeschreibung (TODO anpassen)
# Erzeugt:   $(date +%Y-%m-%d) durch maxclaw bash-script-builder
# Aufruf:    NAME_PLACEHOLDER [argumente]
# =============================================================================

set -euo pipefail

# --- Pfade / Konstanten -----------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${LOG_DIR:-$HOME/.local/share/maxclaw/logs}"
mkdir -p "$LOG_DIR"

# --- Logging -----------------------------------------------------------------
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ts() { date +%Y-%m-%dT%H:%M:%S%z; }
info() { echo -e "${GREEN}[$(ts)] →${NC} $*"; }
warn() { echo -e "${YELLOW}[$(ts)] ⚠${NC} $*" >&2; }
err()  { echo -e "${RED}[$(ts)] ✗${NC} $*" >&2; }
log()  { echo "[$(ts)] $*" >> "$LOG_DIR/NAME_PLACEHOLDER.log"; }

# --- Argumente ---------------------------------------------------------------
usage() {
  cat <<USG
Usage: $(basename "$0") [--dry-run] [-h]
  --dry-run   Nur anzeigen, nichts ausführen
  -h, --help  Diese Hilfe
USG
}

DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) err "unbekanntes Argument: $1"; usage; exit 2 ;;
  esac
done

# --- Hauptlogik (TODO) -------------------------------------------------------
main() {
  info "starte NAME_PLACEHOLDER (dry-run=$DRY_RUN)"
  # TODO: Implementierung
}

# --- Trap für sauberes Beenden -----------------------------------------------
trap 'err "abgebrochen in Zeile $LINENO"' ERR INT TERM
main "$@"
BASH

# NAME ersetzen (nicht in Heredoc möglich → sed)
sed -i "s/NAME_PLACEHOLDER/$NAME/g" "$TARGET"
chmod +x "$TARGET"
info "erzeugt: $TARGET"
```

### 2. Lint-Snippet (jedes neue Skript sollte das können)

```bash
# In CI / Pre-Commit:
shellcheck -x "$TARGET" || warn "shellcheck nicht OK — bitte prüfen"
bash -n "$TARGET" || { err "Syntax-Fehler"; exit 1; }
```

### 3. Doku-Generator (`scripts/doc-gen.sh`)

```bash
#!/usr/bin/env bash
# doc-gen.sh — extrahiert usage-Block + Header → Markdown
set -euo pipefail
SCRIPT="${1:?script}"
NAME="$(basename "$SCRIPT" .sh)"
HEADER="$(sed -n '/^# ====/,/^# ====/p' "$SCRIPT" | sed '/=====/d')"
USAGE="$(sed -n '/^usage()/,/^}/p' "$SCRIPT" | sed '1d;$d')"
cat <<MD
# $NAME
$HEADER
## Usage
\`\`\`
$USAGE
\`\`\`
MD
```

## Pitfalls

- ❌ **`set -e` ohne `-o pipefail`** → Pipes ignorieren Fehler der linken Seite
  (klassischer Cron-Killer: `grep foo file | wc -l` ist 0 statt Fehler).
- ❌ **`$VAR` ohne Quotes** — bei Pfaden mit Spaces/Globs → Wort-Splitting +
  Globbing. Immer `"$VAR"`.
- ❌ **`cd $DIR` ohne Schutz** — wenn Verzeichnis fehlt, landet man im $HOME
  und überschreibt dort. `cd "$DIR" || exit 1` oder `pushd`.
- ❌ **`trap ERR` fängt keine Command-Substitution-Fehler** — dafür
  `set -E` zusätzlich.
- ✅ `BASH_SOURCE[0]` statt `$0` — bleibt korrekt bei `source`/Symlinks.
- ✅ `printf '%s\n'` statt `echo` für variable Daten (kein Backslash-Issue).

## Cron-Beispiel

```cron
# Generator-Aufruf im Workflow, kein Cron nötig (manueller Trigger)
```