---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Generic plugin system for Python applications. Auto-discovery, validation, fault tolerance. Zero dependencies (Python stdlib only).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: de
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="plugin-system banner">

# Plugin System

Fehlertolerantes Plugin-System fuer Python-CLI-Anwendungen.
Ein fehlerhaftes Plugin stoppt niemals den Rest der Anwendung.

## Kernfeatures

- **Auto-Discovery:** Findet Plugins automatisch in einem Verzeichnis
- **Validierung:** Prueft `name`, `version`, `execute()` auf jeder Plugin-Klasse
- **Fehlertoleranz:** Defekte Plugins werden geloggt aber nicht geladen
- **Zero Dependencies:** Nur Python-Standardbibliothek

## Dateien

```
scripts/
  plugin_system.py       Kern: PluginBase (ABC) + PluginManager
  cli_demo.py            Demo-CLI mit argparse
  test_plugin_system.py  16+ Unit-Tests
examples/
  hello.py               Hello-World Plugin
  calculator.py          Rechner-Plugin
  systeminfo.py          System-Info Plugin
```

## Schnellstart

### 1. Plugin erstellen

```python
from plugin_system import PluginBase

class MeinPlugin(PluginBase):
    name = "MeinPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hallo!"}
```

### 2. PluginManager nutzen

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./meine_plugins")
plugins = manager.discover_plugins()

# Alle Plugins auflisten
manager.list_plugins()

# Plugin ausfuehren
success, result = manager.execute_plugin("MeinPlugin", param="wert")
if success:
    print(result)
```

### 3. In eigene App integrieren

```python
class MeineApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Plugin-Interface

Jedes Plugin muss:

| Anforderung | Details |
|-------------|---------|
| `PluginBase` erben | `from plugin_system import PluginBase` |
| `name` setzen | Klassenattribut, nicht leer |
| `version` setzen | Klassenattribut, Semantic Versioning |
| `execute()` implementieren | Beliebige `*args, **kwargs` |

## Fehlertoleranz

| Fehlertyp | Verhalten |
|-----------|-----------|
| SyntaxError im Plugin | Plugin wird uebersprungen, Rest laedt |
| Fehlende Attribute | Plugin wird als `is_valid=False` markiert |
| Exception in `execute()` | Gibt `(False, error_message)` zurueck |
| Kein Plugin im Verzeichnis | Leere Liste, kein Crash |

## Changelog

### 1.0.0 (2026-03-12)
- Migration aus MODULAR_AGENTS/plugins in Skillbibliothek
- PluginBase ABC + PluginManager
- 3 Beispiel-Plugins (Hello, Calculator, SystemInfo)
- 16+ Unit-Tests
- CLI-Demo mit argparse
