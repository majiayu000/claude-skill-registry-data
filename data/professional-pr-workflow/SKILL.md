---
name: professional-pr-workflow
description: Automatisiert Pull-Request-Erstellung mit Branch-Management, Code-Formatierung und Integration mit professional-commit-workflow. Unterstützt GitHub CLI, automatische PR-Beschreibungen und projektspezifische Formatter (Biome, Black, Prettier).
---

# Professional PR Workflow

## Overview

Automatisiert den kompletten Pull-Request-Workflow: Branch-Erstellung, Code-Formatierung, Commit-Integration und PR-Erstellung via GitHub CLI.

**Features:**
- ✅ **Intelligentes Branch-Management** - Erkennt geschützte Branches
- ✅ **Integration mit professional-commit-workflow** - Keine Commit-Duplikation
- ✅ **Automatische Code-Formatierung** (Biome, Black, Prettier, etc.)
- ✅ **GitHub CLI Integration** - PR-Erstellung, Labels, Issue-Verlinkung
- ✅ **Aussagekräftige PR-Beschreibungen** mit Test-Plan
- ✅ **Draft-PR Support** - WIP-PRs markieren

## Prerequisites

**Required:**
- Git (2.0+)
- Python 3.8+
- GitHub CLI (`gh`) - installiert und authentifiziert

**Optional (für Code-Formatierung):**
- **JavaScript/TypeScript**: Biome oder Prettier
- **Python**: Black, isort, Ruff
- **Java**: Google Java Format
- **Markdown**: markdownlint

## Usage Workflow

1. **Branch-Status prüfen**:
   - Geschützter Branch (main/master/develop)? → Neuer Branch erstellen
   - Feature-Branch? → Aktuellen Branch verwenden

2. **Änderungen committen**:
   - Uncommitted changes? → Rufe `professional-commit-workflow` auf
   - Bereits committed? → Verwende bestehende Commits

3. **Code formatieren** (optional mit `--no-format` überspringen)

4. **PR erstellen**:
   - Push Branch zu Remote
   - Generiere PR-Titel und Beschreibung
   - Erstelle PR via `gh pr create`

## Main Script Usage

```bash
# Standard-PR-Workflow
python scripts/main.py

# Draft-PR
python scripts/main.py --draft

# Ohne Formatierung
python scripts/main.py --no-format

# Single Commit (alle Änderungen in einem)
python scripts/main.py --single-commit

# Target Branch ändern
python scripts/main.py --target develop
```

## Supported Formatters

### JavaScript/TypeScript
- **Biome** (bevorzugt): `biome format --write .`
- **Prettier**: `prettier --write .`
- **ESLint**: `eslint --fix .`

### Python
- **Black**: `black .`
- **isort**: `isort .`
- **Ruff**: `ruff format .`

### Java
- **Google Java Format**: Via Maven/Gradle Plugin

### Markdown
- **markdownlint**: `markdownlint --fix **/*.md`
- **mdformat**: `mdformat .`

## Output Example

```text
============================================================
  Professional PR Workflow
============================================================

✓ Branch-Status: main (geschützt)
✓ Neuer Branch erstellt: feature/user-dashboard-2024-12-21

✓ Code-Formatierung:
  ✓ Biome: 5 Dateien formatiert
  ✓ ESLint: 0 Fehler

✓ Branch gepusht: origin/feature/user-dashboard-2024-12-21

✓ PR erstellt: #42
  https://github.com/user/repo/pull/42

✅ PR-Workflow erfolgreich abgeschlossen
```

## Configuration

### pr_config.json

```json
{
  "protected_branches": ["main", "master", "develop"],
  "default_target": "main",
  "auto_delete_branch": false,
  "formatters": {
    "javascript": "biome",
    "python": "black",
    "java": "google-java-format"
  }
}
```

## Error Handling

**Branch-Fehler**: Prüft bestehende Branches, bietet alternative Namen
**Format-Fehler**: Zeigt Details, ermöglicht `--no-format` Fallback
**GitHub CLI-Fehler**: Prüft Authentifizierung, zeigt gh-Setup-Anleitung
**Push-Fehler**: Retry-Logik, manuelle Push-Kommandos

## References

- **[Code-Formatting](docs/code-formatting.md)**: Formatter-Details
- **[Commit-Workflow](docs/commit-workflow.md)**: Integration mit Commit-Skill
- **[PR-Template](docs/pr-template.md)**: PR-Best-Practices
- **[Troubleshooting](docs/troubleshooting.md)**: Fehlerbehebung
