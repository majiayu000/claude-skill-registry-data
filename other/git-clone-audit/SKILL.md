---
name: git-clone-audit
title: Git Clone Audit — Drift Analysis & Master of Truth
description: >-
  Systematischer Vergleich zweier lokaler Klone desselben Git-Remotes. Branch-Inventar, Cross-Clone-Diff, Hygiene-Scan, CI-Vergleich, Build-Verifikation und gewichtete Master-of-Truth-Bestimmung. Rein read-only — kein Push, kein Branch-Modify, kein Commit.
triggers:
  - Mehrere lokale Klone desselben Repos existieren (active/ + library/)
  - User fragt "welcher Clone ist aktuell / Master of Truth"
  - User bittet um Hygiene-Audit mit Working-Tree-Inspektion
  - Unterschiedliches Verhalten zwischen zwei Working-Dirs
  - Vor Merge/Cherry-Pick zwischen zwei Working-Copies
  - Nach Workspace-Reorganisation: Konsistenzprüfung
version: 1.4.0
author: Hermes Agent
license: MIT
lane: worker-flash
reasoning_effort: high
---
# Git Clone Audit — Drift Analysis & Master of Truth

Wenn mehrere lokale Klone desselben Remotes existieren (z. B. aktiver Workspace
unter `10-Projekte/10-active/` und Referenz-Klon unter `30-Library/`), müssen
diese systematisch verglichen werden, um den autoritativen Stand zu bestimmen.

Die Analyse ist **read-only** — kein Push, Branch-Modify oder Commit.

---

## Pipeline

```
Phase 0 — Clone-Inventar (Branches, Remotes, Working-Tree, Tracked-Count)
  ↓
Phase 1 — File-Inventar (alle Source-Files mit LOC + Zweck)
  ↓
Phase 2 — Cross-Clone Diff (git diff --no-index)
  ↓
Phase 3 — Exclusive-Pfade (nur in A / nur in B)
  ↓
Phase 4 — CI-Workflow-Vergleich (Volltext-Diff)
  ↓
Phase 5 — Build-Verifikation (Smoke-Test + CI-Lauf)
  ↓
Phase 6 — Hygiene-Scan (6a: Gitignore, 6b: Token/Leak, 6c: Nested+Mode)
  ↓
Phase 7 — Master-of-Truth + Feature-Matrix (gewichtete Kriterien + Consolidation)
```

**N-Klon-Expansion:** Der Standard-Pipeline geht von 2 Klonen aus. Bei 3+ Klonen
wiederhole Phasen 2–6 für jedes Klon-Paar (A↔B, A↔C, B↔C), erstelle aber eine
**zentrale Feature-Matrix** in Phase 7 statt separater Entscheidungen pro Paar.
Die MoT-Bestimmung erfolgt dann über die Matrix, nicht über Paar-Vergleiche.
Siehe `references/hermes-v7-4-clone-analysis-2026-07-05.md` für ein worked
example mit 4 Klonen.

---

## Phase 0 — Clone-Inventar

Für jeden Klon:

```bash
# Branch, Remote, Working-Tree
cd /pfad/zu/klon
git status --short -b
git remote -v
git log --oneline -5

# Tracked Files, Branches, Untracked
git ls-files | wc -l
git branch -a | wc -l
git status --porcelain | grep '^??' | wc -l   # untracked count

# Relation zu origin/develop
git fetch origin develop   # einmal reicht für alle Klone
git rev-list --left-right --count origin/develop...HEAD
git log --oneline origin/develop..HEAD     # ahead
git log --oneline HEAD..origin/develop     # behind
```

**Wichtig:** `git fetch origin develop` nur **einmal** ausführen und für alle
Klone denselben Referenzstand nutzen (fetch ist read-only, idempotent).

---

## Phase 1 — File-Inventar

```bash
# Source-Files nach Typ
find . -not -path './.git/*' -name '*.src' -type f | sort
find . -not -path './.git/*' -name '*.py'  -type f | sort

# Mit LOC
find . -not -path './.git/*' -name '*.src' -type f -exec wc -l {} + | sort -n

# Zweck aus Kopfzeilen
for f in $(find . -not -path './.git/*' -name '*.src' -type f | sort); do
  echo "--- $f ---"
  head -15 "$f" | grep -iE "^(// )?(description|name|version|author|purpose)"
done
```

Produziere eine Tabelle mit den Spalten: **Pfad | LOC | Zweck (1 Satz)**.

---

## Phase 2 — Cross-Clone Diff

```bash
# Alle non-empty Diffs (Working-Tree vs Working-Tree)
GIT_DIFF_URI=$(cd /pfad/zu/klonB && pwd)
cd /pfad/zu/klonA
git diff --no-index --ignore-cr-at-eol \
  -- . "$GIT_DIFF_URI" \
  2>/dev/null | grep "^diff --git" | wc -l

# Nur .src-Files mit non-empty Diff
git diff --no-index --ignore-cr-at-eol \
  -- . "$GIT_DIFF_URI" \
  2>/dev/null | grep "^diff --git" | sed 's|diff --git a/||; s| b/.*||' \
  | sort -u | grep '\.src$'
```

Erstelle eine Tabelle: **Relativer Pfad | Klon A LOC | Klon B LOC | Änderung**.\n\n---\n\n## Phase 2b — Single-File Deep Drift Analysis (Fokus: eine kritische Datei)\n\nWenn der Cross-Clone-Diff zeigt, dass eine bestimmte Datei Änderungen enthält,\nund beide Klone auf dasselbe Remote zeigen, reicht `diff -u` allein nicht aus.\nDie Datei kann auf Git-Ebene **mehrere Revisionen durchlaufen haben**, die im\nWorking-Tree eines Klons angekommen sind, im anderen nicht. Diese Phase klärt\n**welche** Version wann wo liegt und warum.\n\n### Schritt 1 — Git-History beider Klone für diese Datei\n\n```bash\n# History in Klon A: welche Commits haben diese Datei verändert?\ncd /pfad/zu/klonA\ngit log --all --oneline -- pfad/zur/datei.src   # Alle Commits in diesem Repo\n\n# History in Klon B — gleiche Datei\ncd /pfad/zu/klonB\ngit log --oneline -- pfad/zur/datei.src         # Nur im aktiven Branch\n```\n\n**Wichtig:** Der Unterschied zwischen `--all` und ohne `--all` ist der kritische\nBefund:\n- `git log -- pfad/src.x` → Commits die im **aktuellen Branch** die Datei betrafen\n- `git log --all -- pfad/src.x` → **ALLE** Commits im Repo, die die Datei betrafen\n\nWenn `git log --all -- file` 3 Einträge zeigt, aber `git log -- file` nur 1\n(in Klon B), dann existieren die Fix-Commits zwar im Repo-History, wurden aber\n**nie in den Working-Tree dieses Klons übernommen** (nicht gemerged,\nMerge-Konflikt übersehen, falscher Branch).\n\n### Schritt 2 — MD5-Cross-Validation (Der kritische Beweis)\n\n```bash\n# MD5 des Working-Trees beider Klone\nmd5sum /pfad/zu/klonA/pfad/zur/datei.src   # Ergebnis A\nmd5sum /pfad/zu/klonB/pfad/zur/datei.src   # Ergebnis B\n\n# MD5 jedes relevanten Commit-Inhalts in Klon B (oder A)\ngit show <commit-hash>:pfad/zur/datei.src | md5sum\n\n# Vergleichstabelle:\necho \"Working-Tree A:    $(md5sum A/path | awk '{print $1}')\"\necho \"Working-Tree B:    $(md5sum B/path | awk '{print $1}')\"\necho \"Commit featha:  $(git show featha:path | md5sum | awk '{print $1}')\"\necho \"Commit fix456:  $(git show fix456:path | md5sum | awk '{print $1}')\"\n```\n\n**Interpretation der MD5-Kreuztabelle:**\n\n| Muster | Bedeutung |\n|--------|-----------|\n| A = fix456, B = featha | A ist die **fixe Version**, B ist die **Ur-Version**. Fixes existieren in der History, aber nie in Bs Working-Tree gelandet. |\n| A = B = HEAD | Beide sind identisch mit git-HEAD. Die Datei ist synchron. |\n| A ≠ B, beide ≠ jeder Commit | Dirty Working-Tree in einem Klon (uncommitted changes). |\n| A = fix456, B = fix789 | **Auseinanderentwickelt** — beide Klone haben unterschiedliche Fix-Commits |\n\n**Kernerkenntnis:** Wenn die Working-Tree MD5 des einen Klons mit der\n`git show`-Ausgabe eines Fix-Commits übereinstimmt, während der andere Klon\ndie feat-Version zeigt, ist die Klon-Identität eindeutig — kein 3-Wege-Merge\nnötig, einfaches `cp` reicht.\n\n### Schritt 3 — Diff-Kategorisierung nach Bugfix-Typen\n\nDie `diff -u` Hunks sollten nach **semantischem Wert** gruppiert werden:\n\n| Kategorie | Beschreibung | Beispiel aus Session 2026-07-05 |\n|-----------|-------------|----------------------------------|\n| 🔴 Bugfix (fehlt in B) | Syntax-Korrektur, greybel-Kompatibilität | `exit` → `exit()`, fehlendes `end if`, `list[-1]` → `parts[parts.len-1]` |\n| 🟢 Refactor (Wertsteigerung) | Lesbarkeit, Redundanz-Entfernung | `get_shell.host_computer` → lokale `shell`/`pc`-Variable |\n| ⚪ Kosmetik (gleichwertig) | Formatierung, Logo, Kommentare | ASCII-Logo mit/ohne `draw = draw +` |\n| 🔴 Regression (Rückschritt in B) | Funktionaler Rückschritt | Aktivierte vs. auskommentierte API-Aufrufe |\n\nZähle die Zeilen pro Kategorie und wiege sie für die MoT-Entscheidung.\n\n### Schritt 4 — Funktions-Inventar (API-Vertrag-Check)\n\nSelbst wenn LOC nah beieinander liegen, können Funktionen fehlen oder\nhinzugekommen sein. Extrahiere das Funktions-Inventar mit sprachspezifischen\nPatterns:\n\n```bash\n# GreyScript: Name = function(args)\ngrep -nE '^\\w+\\s*=\\s*function\\(' /pfad/zur/datei.src\n\n# Python: def name(args):\ngrep -nE '^\\s*def\\s+\\w+\\s*\\(' /pfad/zur/datei.src\n\n# JavaScript: function name(args) / const name = (args) =>\ngrep -nE '^(function|const|let|var)\\s+\\w+\\s*[=(]' /pfad/zur/datei.src\n```\n\nVergleiche **Funktionsnamen und Parameteranzahlen** zwischen beiden Klonen.\nWenn sie identisch sind, ist der API-Vertrag stabil → **die Datei kann durch\neinfaches Kopieren ersetzt werden**, kein manueller Merge nötig.\n\n### Report-Format für Phase 2b\n\n```\n| Aspekt | Clone A | Clone B |\n|--------|:-------:|:-------:|\n| LOC | 900 | 889 |\n| MD5 | \"3787806b...\" | \"03f0821c...\" |\n| Git-Commits (file) | feat + fix1 + fix2 | feat (nur) |\n| Fixes angewendet | ✅ alle 3 | ❌ 0 |\n| Funktionen identisch | ✅ (22/22) | ✅ (22/22) |\n| Bugfix-Kategorie (Zeilen) | 🔴/🟢/⚪: 9/3/4 | ❌/❌/⚪: 0/0/4 |\n| Canonical | **JA** | NEIN |\n\n**Einzeiler:** Canonical = Clone A (reine Obermenge von B; Fixes fehlen in B).\nKonkrete Migrations-Schritte: `cp`, Branch, Commit, PR.\n```\n\nReferenz-Beispiel mit vollständigem Workflow:\n`references/single-file-drift-analysis-xmem-2026-07-05.md`.\n\n---\n\n## Phase 3 — Exclusive-Pfade

```bash
# Nur in Klon A
cd /pfad/zu/klonA
for f in $(git ls-files); do
  [ ! -f "/pfad/zu/klonB/$f" ] && echo "$f"
done | sort > /tmp/only-in-a.txt

# Nur in Klon B
cd /pfad/zu/klonB
for f in $(git ls-files); do
  [ ! -f "/pfad/zu/klonA/$f" ] && echo "$f"
done | sort > /tmp/only-in-b.txt

wc -l /tmp/only-in-a.txt /tmp/only-in-b.txt
```

Gruppiere die exclusiven Pfade logisch:
- **Dokumentation** (`docs/`, `README.md`)
- **Exklusive Module** (Commit-Check: in welchem Branch entwickelt?)
- **Build-Artefakte** (fälschlich committed?)
- **CI/Agent-Konfiguration** (Branch-spezifisch)

---

## Phase 4 — CI-Workflow-Vergleich

```bash
# Arbeitsbäume
ls -la /pfad/zu/klonA/.github/workflows/ 2>/dev/null
ls -la /pfad/zu/klonB/.github/workflows/ 2>/dev/null

# ci.yml Volltext-Diff
diff -u \
  /pfad/zu/klonA/.github/workflows/ci.yml \
  /pfad/zu/klonB/.github/workflows/ci.yml

# Build-Script
diff -u \
  /pfad/zu/klonA/scripts/ci-build.sh \
  /pfad/zu/klonB/scripts/ci-build.sh \
  2>/dev/null || echo "Nur in einem Klon"
```

**Checkliste:**
- [ ] Anzahl Jobs
- [ ] greybel-build-Job vorhanden?
- [ ] Build-Script: greybel-CLI-Subcommand korrekt? (3.6.x: `-o`, 3.7.x: `build`)
- [ ] Artifact-Upload konfiguriert?
- [ ] Trigger-Branches identisch?

### Cross-Branch CI Job Drift

Dieselbe Workflow-Datei (z. B. `ci.yml`) kann auf verschiedenen Branches
**unterschiedliche Jobs** enthalten — ein häufiges Muster, wenn CI-Upgrades
auf `develop` vorgenommen, aber nicht auf Feature-Branches zurückportiert
wurden.

```bash
# Job-Namen pro Branch extrahieren
grep '^  [a-z].*:$' /pfad/zu/klonA/.github/workflows/ci.yml
grep '^  [a-z].*:$' /pfad/zu/klonB/.github/workflows/ci.yml

# Job-Anzahl zählen
grep -c '^  [a-z].*:$' /pfad/zu/klonA/.github/workflows/ci.yml
grep -c '^  [a-z].*:$' /pfad/zu/klonB/.github/workflows/ci.yml

# LOC-Vergleich als Proxy für Komplexität
wc -l /pfad/zu/klonA/.github/workflows/ci.yml
wc -l /pfad/zu/klonB/.github/workflows/ci.yml
```

**Drift-Checkliste:**
- [ ] Job-Anzahl identisch? (Differenz = Hinweis auf CI-Upgrade in einem Branch)
- [ ] Welcher Branch hat MEHR Jobs? → MoT-Kandidat für CI
- [ ] Fehlt ein Build-Job im anderen Branch? → Build-Verifikation nur im vollständigen Branch
- [ ] Build-Script-Inhalt unterschiedlich? (CLI-Subcommand, scan-Tiefe, exclusions)
- [ ] Zusätzliche Workflow-Dateien in einem Branch? (pr-reminder, auto-label, etc.)

---

## Phase 5 — Build-Verifikation

```bash
# Greybel-Verfügbarkeit
which greybel && greybel --version

# Smoketest (eine Datei)
greybel build src/buildcore.src /tmp/greybel-build-test/buildcore

# Vollständiger CI-Lauf mit ci-build.sh des autoritativen Klons
cd /pfad/zu/klonA
bash scripts/ci-build.sh --out-dir .ci-build

# Ergebnis-Prüfung
cat .ci-build/ci-build-result.log
```

### Build-Barrier Analysis

Nicht alle `.src`-Files im Working-Tree sind für den Build vorgesehen.
Dokumentiere explizit welche Dateien warum **nicht** gebaut werden — das
verhindert falsche Schlüsse aus der bloßen File-Anzahl.

```bash
# Klassifiziere alle .src-Files nach Build-Status
find . -name '*.src' -not -path './.git/*' | while read f; do
  case "$f" in
    */tests/*|./tests/*)        echo "TEST     $f" ;;
    */greyhack-tools/*)         echo "GT-TOOL  $f" ;;
    */yuno_viper/*)             echo "FEATURE  $f" ;;
    */build/*)                  echo "ARTIFACT $f" ;;
    */imports/*)                echo "SNAPSHOT $f" ;;
    src/*|tools/*)              echo "BUILD    $f" ;;
    *)                          echo "UNKNOWN  $f" ;;
  esac
done

# Build-Script-Reichweite prüfen
# ci-build.sh scannt meist src/ + tools/ mit begrenzter Tiefe
grep -E '(maxdepth|find.*-name.*\.src)' scripts/ci-build.sh
```

**Typische Build-Barrieren:**

| Kategorie | Pfad-Muster | Grund |
|-----------|-------------|-------|
| Tests | `tests/*.src` | Separate Test-Suite, nicht für CI-Build |
| Sub-Projekte | `greyhack-tools/*/*.src` | Eigene Build-Pipeline, nicht Teil des Core |
| Feature-Module | `yuno_viper/*.src` | Separater Build-Workflow (z. B. In-Game) |
| Build-Artefakte | `build/*.src` | Output vergangener Builds, kein Source |
| Hist-Snapshots | `imports/*.src` | Historisch, nicht aktiv |

**Erkenntnis:** Die Anzahl `.src`-Files sagt wenig über Build-Komplexität aus.
Entscheidend ist: wie viele landen tatsächlich im CI-Build-Script.

**Pitfalls:**
- greybel CLI-Subcommand: 3.6.x → `-o <file>` / 3.7.x+ → `build <file> <dir>`
- Node.js ≥ 18 erforderlich
- `ci-build.sh` scannt nur bestimmte `maxdepth`-Tiefen — prüfe ob alle `.src` erreicht werden

---

## Phase 6 — Hygiene-Scan

Dreiteilig: (6a) Untracked + Gitignore-Hygiene, (6b) Credential & Token-Leak Detection, (6c) Nested Repos + Mode-600.

### 6a — Untracked & Gitignore-Hygiene

```bash
# Untracked (nicht ignoriert)
cd /pfad/zu/klon
git status --porcelain | grep '^??'

# Unzureichend geschützte sensible Files
for f in notes.md credentials.txt .env \
         attack_*.src attack_*.txt reports/ *.log; do
  git check-ignore -q "$f" 2>/dev/null \
    && echo "$f → ignoriert" \
    || echo "!!! $f → NICHT ignoriert"
done

# CITICAL: Untracked Files auf .gitignore-Lücken prüfen
# Runtime-Artefakte (z.B. logs/audit.jsonl) wachsen pro Tool-Call
# und dürfen NIEMALS in die Versionskontrolle. Prüfe ob sie ignoriert sind.
UNTRACKED=$(git status --porcelain | grep '^??' | sed 's/^?? //')
for f in $UNTRACKED; do
  case "$f" in
    *.jsonl|*.log|*.token|auth.json|.netrc|*.bak|dist/|build/)
      echo "⚠️  Sollte ignoriert werden: $f"
      git check-ignore -q "$f" 2>/dev/null \
        && echo "   → Ist bereits ignoriert ✅" \
        || echo "   → NICHT ignoriert — .gitignore ergänzen!"
      ;;
  esac
done
```

**Empfohlene .gitignore-Zeilen für Runtime-Artefakte:**
- `logs/*.jsonl` (Audit-Logs, wachsen pro Call)
- `*.log` (generelle Prozess-Logs)
- `dist/`, `build/` (Build-Output, wenn nicht bereits ignoriert)
- `.env.local`, `*.token`, `auth.json`, `.netrc` (Credentials)

### 6b — Credential & Token-Leak Detection

Prüfe jeden Klon auf eingebettete Tokens in der Remote-URL und falsche
`.git/config`-Berechtigungen. Siehe auch `project-landscape-audit` Phase 4
Step E für die vollständige Deep-Dive-Prozedur.

```bash
# Remote-URL auf eingebettete Credentials prüfen
URL=$(git config --get remote.origin.url)
if echo "$URL" | grep -q '@'; then
  TOKEN=$(echo "$URL" | sed -n 's|.*://[^:]*:\([^@]*\)@.*|\1|p')
  if echo "$TOKEN" | grep -qE '^(gh[op]_|github_pat_)'; then
    echo "  🚨 TOKEN-EMBEDDED REMOTE! (${TOKEN:0:3}...${TOKEN: -4})"
    echo "  → Sofort revoken auf github.com/settings/tokens"
    echo "  → Dann: git remote set-url origin https://github.com/owner/repo.git"
  fi
fi

# .git/config Dateimodus (sollte 600 oder 640 sein)
PERMS=$(stat -c '%a' .git/config 2>/dev/null)
echo "  .git/config mode: $PERMS"
if [ "$PERMS" != "600" ] && [ "$PERMS" != "640" ]; then
  echo "  ⚠️  WARNING: group-readable! chmod 600 empfohlen"
fi

# Credential-Helper (sollte gesetzt sein, NICHT Token-in-URL)
HELPER=$(git config --get credential.helper 2>/dev/null)
echo "  credential.helper: ${HELPER:-(none)}"
if [ -z "$HELPER" ] && echo "$URL" | grep -q '@'; then
  echo "  ⚠️  Kein Credential-Helper + Token in URL = doppeltes Risiko"
  echo "  → Fix: git config --global credential.helper libsecret"
fi
```

**Credential-Leak-Cheatsheet:**

| Pattern in URL | Risiko | Aktion |
|---|---|---|
| `gho_*` (classic OAuth) | 🔴 Kritisch — langlebig, kein Auto-Expire | Revoken auf github.com/settings/tokens |
| `ghp_*` (classic PAT) | 🔴 Kritisch — full API access | Revoken, fine-grained ersetzen |
| `github_pat_*` (fine-grained) | 🟠 Hoch — scoped aber Zugriff | Revoken, `.git/config` auf Mode 600 |
| Kein credential.helper + Token in URL | 🟠 Hoch — Credentials im Klartext | `git config credential.helper libsecret` + URL ohne Token |

### 6c — Nested Git-Repos & Mode-600 Scan

```bash
# Nested .git-Verzeichnisse (submodule oder Müll?)
find . -not -path './.git/*' -name '.git' -type d

# Mode-600 Files (potenziell sensibel)
find . -not -path './.git/*' -perm 600 -type f
```

**Hygiene-Klassifikation:**

| Kategorie | Beispiel | Aktion |
|-----------|----------|--------|
| Müll (dupliziert) | `yuno_viper/modules/` byte-genau zu HEAD | Löschen oder ignorieren |
| Müll (nested clone) | `greybel-vs/.git/` | Entfernen / submodulen |
| Sensibel (unignoriert) | `notes.md` mit IPs/Credentials | `.gitignore` + rotieren |
| Reports (privat) | `reports/*.md` Spiel-Outputs | Ignorieren / separater Branch |
| Build-Artefakte | `.ci-build/` | Ignorieren (meist korrekt) |

Verwende **mode 600** als stärkstes Signal: Files mit `chmod 600` und
suggestiven Namen (attack, plan, credentials) sind fast immer sensibel.

### Tracked-Before-Ignore (TBI) Files

Dateien, die von einem `.gitignore`-Pattern gematcht werden sollten, aber
trotzdem tracked sind — weil sie vor der Regel committed, mit `git add -f`
hinzugefügt, oder bereits staged waren als `.gitignore` angelegt wurde.

```bash
# TBI-Files finden: tracked Files die .gitignore-Patterns matchen
cd /pfad/zu/klon
for pattern in '/build/' '/.last-ci-check' '/attack_*' '*.env' '*.log'; do
  matches=$(git ls-files -- "$pattern" 2>/dev/null)
  [ -n "$matches" ] && echo "TBI $pattern: $matches"
done

# Oder extrahiere Pfad-Patterns aus .gitignore (robuster)
while IFS= read -r line; do
  case "$line" in \#*|!*|'') continue ;; esac
  matches=$(git ls-files -- "$line" 2>/dev/null)
  [ -n "$matches" ] && echo "TBI '$line': $matches"
done <.gitignore
```

**Klassifikation:**

| Fund | Ursache | Behandlung |
|------|---------|------------|
| `build/yuno_v6.src` gematcht von `/build/` | `git add -f` vor der Ignore-Regel | `git rm --cached build/yuno_v6.src` (nur mit Erlaubnis) |
| `xmem/` gematcht von `/xmem/` | Wie oben, vor Ignore committed | `git rm --cached -r xmem/` |
| `.last-ci-check` nicht gematcht | Pfad-Pattern `/file` matched nur Wurzel, relativer Pfad nicht | Fix: `git check-ignore` testen, Pattern korrigieren |

**Wichtig:** `.gitignore` wirkt nur auf **untracked** Files. Bereits tracked
Files ignoriert zu machen erfordert `git rm --cached` (löscht aus Tracking,
nicht von Disk). Niemals ohne explizite User-Erlaubnis ausführen.

---

## Phase 7 — Master-of-Truth-Bestimmung

Gewichtete Kriterien. Jedes bekommt ✅/⚠️/❌ plus kurze Begründung.

### Feature-Matrix-Vergleich (3+ Klone)

Bei 3+ Klonen nicht nur MoT bestimmen, sondern auch **welche Features in welchem
Klon existieren** — das geht über reine File-Diffs hinaus und schafft die
Entscheidungsgrundlage für Consolidation.

```bash
# Feature-Matrix: existiert ein Modul in Klon X?
for CLONE in /pfad/zu/klonA /pfad/zu/klonB /pfad/zu/klonC; do
  echo "=== $(basename $CLONE) ==="
  echo "  src/ present:     $(test -d $CLONE/src && echo ✅ || echo ❌)"
  echo "  modules/:         $(test -d $CLONE/src/modules && echo ✅ || echo ❌)"
  echo "  security/:        $(ls $CLONE/src/security/ 2>/dev/null | head -3 || echo '(leer)')"
  echo "  Test files:       $(find $CLONE -path '*/node_modules' -prune -o -name '*.test.*' -print 2>/dev/null | wc -l)"
  echo "  CI:               $(ls $CLONE/.github/workflows/ 2>/dev/null | wc -l) workflows"
  echo "  License:          $(test -f $CLONE/LICENSE && echo ✅ || echo ❌)"
  echo "  CHANGELOG:        $(head -3 $CLONE/CHANGELOG.md 2>/dev/null | head -1 || echo '(none)')"
done
```

**Interpretation:** Die Matrix zeigt sofort, welche Klone vollständig sind
(alle Module vorhanden), welche Teil-Snapshots sind (wenige Module) und
welche "Unique Features" je Klon existieren (z. B. SecurityKernel nur in A,
Setup-Bundle nur in B, ADRs nur in C). Das ist die Grundlage für den
Consolidation-Plan.

### Standard-Kriterien (2-Klon-Fall)

| Kriterium | Gewicht | Prüfung |
|-----------|---------|---------|
| Ahead of origin/develop | Hoch | `rev-list --count origin/develop..HEAD` |
| Behind origin/develop | Hoch | `rev-list --count HEAD..origin/develop` |
| CI-Pipeline-Vollständigkeit | Hoch | greybel-build-Job? |
| Build-Script-Korrektheit | Hoch | greybel-CLI-Version-kompatibel? |
| Cluster-Fixes gemerged | Hoch | Fix-Commits im Log? |
| Working-Tree-Sauberkeit | Mittel | `git status --porcelain` Leer |
| Hygiene (ignorierte sensible Files) | Mittel | `.gitignore`-Coverage |
| Doku-Infrastruktur | Niedrig | READMEs, `docs/`, PR-Bodies |
| Workspace-Konvention | Niedrig | active/ vs library/ Role |

### Ausnahme-Prüfung

Wenn der schwächere Klon **exklusive Module** enthält (z. B. yuno_viper nur in
Clone B), dokumentiere die fehlenden Commits als Cherry-Pick-Empfehlung in den
Master. Ein Klon kann MoT für die Hauptlinie sein, aber dennoch Feature-Module
nicht enthalten.

### Entscheidungs-Matrix

```
| Kriterium                | Clone A            | Clone B            |
|--------------------------|--------------------|--------------------|
| Ahead of origin          | +2 (main-cluster)  | +2 (yuno_viper)    |
| Behind origin            | 0                  | 37 ❌              |
| CI greybel-build         | ✅ 61 LOC          | ❌ 25 LOC          |
| CI-Build-Script korrekt  | ✅ (3.7.x build)   | ❌ (alte -o)       |
| Cluster-Fixes gemerged   | ✅ (#41, #42, #50) | ❌ fehlen          |
| Working-Tree clean       | ✅                 | ❌ 4 untracked     |
| .gitignore Hygiene       | ✅                 | 3 Files ungeschützt|
| MoT-Entscheidung         | ← **GEWINNER**     | → yuno_viper cp    |
```

---

## Berichts-Format

### TL;DR-Tabelle

```
| | Clone A (Pfad) | Clone B (Pfad) |
|---|:---:|:---:|
| Branch | ... | ... |
| Tracked Files | ... | ... |
| Ahead/Behind origin/develop | ... | ... |
| CI greybel-build | ✅/❌ | ✅/❌ |
| Working-Tree | clean/dirty | clean/dirty |
| Master of Truth | **JA/NEIN** | **JA/NEIN** |
```

### Detail-Sektionen

Pro Phase: **Befehl → Ergebnis → Interpretation**.

### Anhang

Roh-Daten: LOC-Zahlen, Commit-Hashes, Build-Log-Auszug,
Hygiene-Fundliste mit Pfaden und Klassifikation.

---

## Deployment Strategy — Manual vs Subagent vs Fable

Clone-Audits lassen sich auf drei Arten ausführen. Die Wahl bestimmt Qualität,
Kosten und Dauer massiv.

### 1. Subagent (delegate_task) — Empfohlen für Deep Analysis

**Wann:** 2+ Klone, >500 tracked Files, CI-Vergleich, Hygiene-Scan

**Warum:** Der Subagent läuft mit **vollem Terminal-Zugriff** — er kann
`git log`, `git diff`, `git status`, `git ls-files`, `find`, `wc -l`,
`diff -u` direkt ausführen. Ergebnis: echte Daten, keine Stubs.

**Kosten:** ~$0.15–0.30 pro Analyse (MiniMax-M3)
**Dauer:** 2–10 Minuten
**Output:** 20–30 KB strukturierter Report als Markdown

### Dispensier-Kontext — bewährtes Format (Target: N-Clone mit Hygiene + Token-Scan)

```text
goal: "Read-only Tiefenanalyse des <repo>-Repos",
context: """
CLONE A: /pfad/zu/klonA  (Branch: <branch>)
CLONE B: /pfad/zu/klonB  (Branch: <branch>)

AUFGABEN:
1. git status --short -b in beiden Klonen
2. git rev-list --left-right --count origin/develop...HEAD
3. Git-Diff der CI-Workflows
4. Hygiene-Scan (untracked, sensible Files, .gitignore)
5. Master-of-Truth-Bestimmung

OUTPUT: Report nach /pfad/zum/output/report-name.md
Methode: read-only. Kein push, kein commit, keine remote API calls.
"""
```

**Erfahrung (2026-07-05):**
- 2 Subagenten parallel: greyscripts (2 Klone, 841 Files) + hermes-v7
  (4 Klone, 8066 Files)
- Gesamtkosten: ~$0.30 · Gesamtdauer: 9:58 Min
- Output: 28 KB + 21 KB = **49 KB production-grade Reports** (848 LOC)
- Keine Rückfragen, keine Stubs, direkt verwertbar

### 2. Manuell (direkt via terminal()) — Quick Checks

**Wann:** 1 Klon, <50 Files, schnelle Status-Prüfung

Einzelne git-Befehle direkt ausführen. Kein Deploy-Overhead.

**Output:** ~1–5 KB, direkt im Chat.
**Dauer:** 30 Sekunden.

### 3. Fable / Claude-CLI — ❌ NICHT für Clone-Audits

**Wann:** Gar nicht. Fables (via `claude -p "$(cat prompt.md)"`) haben **keinen**
Zugriff auf den lokalen Filesystem — sie können kein `git status` ausführen,
keine Dateien lesen, keine Working-Trees inspizieren.

**Erfahrung (2026-07-05):** Drei Fables produzierten:
- ~25–150 Bytes Output pro Fable (99% weniger als Subagent)
- Statt Analyse: Rückfragen ("Bitte die Befehle erlauben")
- Statt Daten: Dienstverweigerung ("Ich bin beschränkt auf <working-dir>")
- Kosten: ~$0.50 pro Fable × 3 = $1.50 (vs $0.30 für 2 Subagenten)

### Entscheidungsmatrix

| Kriterium | Manuell | Subagent | Fable |
|-----------|:-------:|:--------:|:-----:|
| Terminal-Zugriff | ✅ | ✅ | ❌ |
| Kosten bei Depth | kostenlos | ~$0.15–0.30 | ~$0.50+ |
| Strukturierter Report | ❌ | ✅ | ❌ |
| Parallelausführung | ❌ | ✅ (bis 5) | ❌ |
| **Empfehlung** | Quick-Checks | **Standard** | Nie |

---

## Pitfalls

1. **Dirty Working Trees**: `git diff --no-index` erfasst nur den getrackten
   Stand. Dirty/Dirty vergleichen ist ok — aber dokumentiere den Zustand.
2. **Untracked Files unsichtbar für diff**: Separate `git status --porcelain`
   pro Klon erforderlich.
3. **Greybel-Versionsinkompatibilität**: 3.6.x ↔ 3.7.x CLI-Break. Build-Script
   muss zur installierten Version passen. Nicht als "Tool kaputt" speichern.
4. **Sensible Daten niemals lesen**: `notes.md` mit IPs/Credentials nur auf
   Existenz prüfen (`mode 600`, `git check-ignore`), nicht mit `cat`/`head`.
   Mode-600 = starkes Sensibilitätssignal.
5. **Nested Git-Repos**: Klone mit eigenem `.git/` (z. B. `greybel-vs/`)
   beeinflussen git status nicht, sind aber Dateisystem-Müll.
6. **Import-Backups nicht werten**: `imports/`-Bäume = historische Snapshots,
   kein Teil der aktiven Codebase. Aus MoT-Vergleich ausschliessen.
7. **Ein Fetch für alle**: `git fetch origin develop` einmal reicht für alle
   Klone. Read-only, idempotent. Danach beliebig oft `rev-list`.
8. **Build-Artefakte im Working-Tree**: `.ci-build/`, `build/`, `dist/` sollten
   ignoriert sein — prüfe im Hygiene-Scan ob `.gitignore` das abdeckt.
9. **Tracked-before-Ignore (TBI)-Fallstrick**: `.gitignore` schützt nur
   *untracked* Files. Ein File der vor der Ignore-Regel committed wurde, bleibt
   tracked — `git status` zeigt ihn trotz `.gitignore`-Match als unverändert.
   Prüfe separat: `git ls-files | grep -f <(grep -v '^#' .gitignore)`.
10. **Falsche Build-Komplexität aus File-Count**: 84 `.src`-Files im Inventar
    bedeuten nicht 84 Build-Targets. Meist landen nur 50-70 % im CI-Build
    (Tests, Sub-Projekte, Feature-Module, Snapshots sind ausgeschlossen).
    Führe immer eine Build-Barrier-Analyse durch bevor du Build-Komplexität
    beurteilst.
11. **Token-in-URL = High-Profile-Event**: Ein `gho_*`/`ghp_*`/`github_pat_*` Token
    in der Remote-URL ist der kritischste Fund eines Clone-Audits. Nicht testen
    (kein API-Call in read-only Modi!). Format klassifizieren (`gho_` = classic
    OAuth, `ghp_` = classic PAT, `github_pat_` = fine-grained), Muster
    (`${TOKEN:0:3}...${TOKEN: -4}`) dokumentieren, Revoke-Anleitung geben.
    `.git/config` auf Mode 600 setzen IMMER zusammen mit Token-Entfernung.
12. **`.gitignore`-Lücken bei Runtime-Artefakten**: `logs/audit.jsonl`,
    `*.log`, `auth.json` gehören in die `.gitignore`, sind es aber oft nicht.
    Prüfe im Hygiene-Scan explizit ob untracked Files in diese Kategorien
    fallen — ein falscher `git add .` kann sie sonst commiten und pushen.
13. **3+ Klone sind kein Luxus, sondern eine andere Analyse**: Die Pipeline
    Phasen 2+3 basieren auf Paar-Vergleichen (`A↔B`). Bei 3+ Klonen wird die
    Analyse kubisch teuer (N² Paare). Wechsel auf **Feature-Matrix** in Phase 7
    stattdessen — prüfe Features pro Klon statt Files pro Paar.
14. **Pfad-Korrektur beim Start notwendig**: Ein Clone, der laut Workspace-Konvention\n    in `40-archive/` liegt, ist fast sicher älter als einer in `30-Library/`.\n    Pfad-Hierarchie validieren, nicht auf Annahmen verlassen. Die `40-` vs\n    `30-` Prefixe geben das Alter vor: `10-` = aktiv, `20-` = experimental/working-tree,\n    `30-` = library/reference, `40-` = archive.\n15. **Git-Log-Distinction für Single-File-Analyse**: `git log --oneline -- pfad`\n    zeigt NUR Commits im **aktuellen Branch**. `git log --all -- pfad` zeigt ALLE\n    Commits im gesamten Repo, die diese Datei betrafen. Wenn `--all` mehr zeigt\n    als ohne Flag, existieren Fix-Commits im Repo-History die nie in den Working-Tree\n    des aktuellen Branches übernommen wurden — der kritischste Befund einer\n    Single-File-Drift-Analyse. Immer BEIDE Befehle ausführen.\n16. **MD5-Cross-Validation beweist mehr als `git diff`**: Der `diff -u` zwischen\n    zwei Working-Trees zeigt was anders ist, aber nicht WARUM. Der `md5sum`-Cross-Check\n    mit `git show <commit>:pfad | md5sum` identifiziert welchem Commit der Inhalt\n    entspricht. Das beweist exakt welche Version wo liegt und ob die Abweichung\n    durch fehlende Fixes oder uncommitted Changes entstanden ist.

---

## Referenzen

- `references/greyscripts-clone-analysis-2026-07-05.md` — Vollständige\n  Beispiel-Analyse (Clone A vs. Clone B des Toqsick/greyscripts-Repos,\n  8 Phasen, Enhanced CI-Drift + Build-Barrier + TBI-Analyse,\n  84/95 .src-Files, 19 mit non-empty Diff). **2-Klon-Fall.**\n- `references/single-file-drift-analysis-xmem-2026-07-05.md` — Beispiel einer\n  Single-File-Deep-Drift-Analyse (Phase 2b): xmem.src zwischen 30-Library und\n  10-Projekte, MD5-Cross-Validation, Bugfix-Kategorisierung, Funktions-Inventar.\n  **1-File-Fall, Fix-versus-Pre-Fix-Bestimmung.**\n- `references/hermes-v7-4-clone-analysis-2026-07-05.md` — Beispiel-Analyse\n  für den 4-Klon-Fall (hermes-v7, C1–C4, Token-Leak-Fund, Multi-Workspace).\n  **4-Klon-Fall.**

## Verwandte Skills

- `codebase-inspection` — LOC/Language-Breakdown via pygount (komplementär)
- `directory-structure-audit` — Filesystem-Klassifikation (wenn Ordenerebene)
- `github-code-review` — PR-Level-Review (nach MoT-Bestimmung)
- `project-landscape-audit` — Breiterer Scan eines gesamten Workspace (komplementär zu Clone-Fokus); enthält detaillierte Token-Leak-Detection-Prozedur in Phase 4 Step E
- `yuno-user-preferences` — the user's Working-Style: Whitelist-Prinzip, keine Blind-Aktionen, sichere Reihenfolge
