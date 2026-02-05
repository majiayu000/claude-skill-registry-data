---
name: professional-commit-workflow
description: Erstellt professionelle Git-Commits mit automatischen Pre-Commit-Checks für Java, Python, React und Dokumentation. Generiert Emoji Conventional Commit-Nachrichten und analysiert Staging-Status. Atomare Commits nach Best Practices.
---

# Professional Commit Workflow

## Overview

Dieser Skill automatisiert den kompletten Git-Commit-Workflow mit professionellen Qualitätschecks und konventionellen Commit-Nachrichten. Er ersetzt den `/commit` Command mit einem wiederverwendbaren, distribuierbaren Skill.

**Special Features:**
- ✅ **Automatische Projekterkennung** (Java, Python, React, Dokumentation)
- ✅ **Pre-Commit-Validierung** mit projektspezifischen Tools
- ✅ **Emoji Conventional Commits** (✨ feat, 🐛 fix, 📚 docs, etc.)
- ✅ **Intelligente Staging-Analyse** mit automatischem Add
- ✅ **Atomare Commit-Empfehlungen** bei mehreren logischen Änderungen
- ✅ **Performance-optimiert** durch modulare Validator-Architektur

## Prerequisites

**Required:**
- Git (version 2.0+)
- Python 3.8+

**Optional (für spezifische Validierungen):**
- **Java**: Maven oder Gradle
- **Python**: ruff, black, pytest, mypy
- **React/Node.js**: npm/pnpm/yarn/bun, ESLint, Prettier
- **Docs**: LaTeX, markdownlint, AsciiDoc

```bash
# Python dependencies installieren
pip install -r requirements.txt --break-system-packages
```

## Usage Workflow

1. **User initiiert Commit**: "Erstelle einen Commit" oder "Commit die Änderungen"

2. **Optionen erkennen**:
   - `--no-verify`: Überspringt Pre-Commit-Checks
   - `--skip-tests`: Überspringt nur Tests
   - `--force-push`: Force Push nach Commit (Vorsicht!)

3. **Projekt-Detection ausführen**:
   ```bash
   python scripts/project_detector.py
   ```
   Erkennt automatisch:
   - Java (Maven: pom.xml, Gradle: build.gradle)
   - Python (pyproject.toml, requirements.txt, setup.py)
   - React/Node.js (package.json mit react/next/vite)
   - Dokumentation (*.tex, *.md, *.adoc)

4. **Pre-Commit-Validierung** (falls nicht `--no-verify`):
   ```bash
   python scripts/main.py --validate-only
   ```
   Führt projektspezifische Checks aus:
   - **Java**: Build, Tests, Checkstyle, SpotBugs
   - **Python**: Ruff, Black, pytest, mypy
   - **React**: ESLint, Prettier, TypeScript, Build
   - **Docs**: LaTeX compile, markdownlint

5. **Staging-Analyse**:
   ```bash
   python scripts/git_analyzer.py --analyze-staging
   ```
   - Prüft `git status` für gestakte Dateien
   - Fügt automatisch Änderungen hinzu falls nötig
   - Zeigt Übersicht der zu committenden Dateien

6. **Diff-Analyse**:
   ```bash
   python scripts/git_analyzer.py --analyze-diff
   ```
   - Analysiert `git diff` für logische Änderungen
   - Erkennt mehrere Features/Fixes in einem Commit
   - Empfiehlt Aufteilung bei Bedarf

7. **Commit-Message generieren**:
   ```bash
   python scripts/commit_message.py --generate
   ```
   - Erkennt Commit-Typ aus Änderungen
   - Generiert Emoji Conventional Commit
   - Deutsche, imperative Beschreibung
   - Format: `<emoji> <type>: <beschreibung>`

8. **Commit erstellen**:
   ```bash
   git commit -m "$(python scripts/commit_message.py --output)"
   ```
   - **WICHTIG:** Keine "Co-Authored-By" oder "Generated with" Zusätze

9. **Optional: Push anbieten**:
   ```bash
   git push origin <branch>
   ```

## Main Script Usage

```bash
# Standard-Commit-Workflow
python scripts/main.py

# Nur Validierung (kein Commit)
python scripts/main.py --validate-only

# Checks überspringen
python scripts/main.py --no-verify

# Tests überspringen
python scripts/main.py --skip-tests

# Mit Force-Push
python scripts/main.py --force-push
```

## Output Structure

**Erfolgreicher Workflow:**
```text
✓ Projekt erkannt: React/TypeScript
✓ Pre-Commit-Checks bestanden (3/3)
  ✓ ESLint: 0 Fehler
  ✓ TypeScript: Kompilierung erfolgreich
  ✓ Build: Erfolgreich
✓ Staging-Analyse: 5 Dateien bereit
✓ Commit-Typ erkannt: feat
✓ Commit erstellt: ✨ feat: User Dashboard mit Metriken hinzugefügt
```

**Bei Validierungs-Fehlern:**
```text
✗ Pre-Commit-Checks fehlgeschlagen (1/3)
  ✓ ESLint: 0 Fehler
  ✗ TypeScript: 2 Fehler gefunden
    - src/components/Dashboard.tsx:12 - Type 'string' is not assignable to type 'number'
  ✓ Build: Erfolgreich

❌ Commit abgebrochen. Bitte Fehler beheben oder --no-verify verwenden.
```

## Configuration

### commit_types.json

Definiert Emoji-Mappings für Conventional Commits:

```json
{
  "feat": {"emoji": "✨", "description": "Neue Funktionalität"},
  "fix": {"emoji": "🐛", "description": "Fehlerbehebung"},
  "docs": {"emoji": "📚", "description": "Dokumentation"}
}
```

### validation_rules.json

Projektspezifische Validierungs-Regeln:

```json
{
  "java": {
    "build": true,
    "tests": true,
    "checkstyle": true
  },
  "python": {
    "ruff": true,
    "black": true,
    "pytest": true,
    "mypy": true
  }
}
```

## Error Handling

**Validierungs-Fehler:**
- Zeige detaillierte Fehlermeldung
- Biete `--no-verify` Option an
- Verweise auf [docs/troubleshooting.md](docs/troubleshooting.md)

**Git-Fehler:**
- Prüfe Git-Status (untracked, conflicts)
- Verweise auf Git-Troubleshooting
- Biete manuelle Kommandos an

**Tool nicht gefunden:**
- Graceful degradation (überspringen)
- Warne User über fehlende Validierung
- Empfehle Tool-Installation

## Best Practices

**Atomare Commits:**
- ✅ Jeder Commit = Eine logische Einheit
- ✅ Trenne Features, Fixes, Refactorings
- ❌ Keine "WIP" oder "misc changes" Commits

**Aussagekräftige Nachrichten:**
- ✅ Beschreibe "Was" und "Warum", nicht "Wie"
- ✅ Imperative Form: "Füge hinzu", nicht "Hinzugefügt"
- ✅ Erste Zeile ≤ 72 Zeichen
- ❌ Keine automatischen Signaturen

**Code-Qualität:**
- ✅ Alle Checks bestanden vor Commit
- ✅ Tests laufen durch
- ✅ Build erfolgreich
- ❌ Keine Debug-Ausgaben oder auskommentierter Code

**Vollständige Guidelines:** [docs/best-practices.md](docs/best-practices.md)

## References

- **[Pre-Commit-Checks](docs/pre-commit-checks.md)**: Detaillierte Check-Beschreibungen
- **[Commit-Types](docs/commit-types.md)**: Alle Emoji-Typen mit Beispielen
- **[Best Practices](docs/best-practices.md)**: Umfassende Git-Commit-Best-Practices
- **[Troubleshooting](docs/troubleshooting.md)**: Fehlerbehebung für häufige Probleme
