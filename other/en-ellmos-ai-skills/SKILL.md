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
language: en
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="plugin-system banner">

> **English** — Official English version of `plugin-system`.


# Plugin System (English)

Fault-tolerant plugin system for Python CLI applications.
A faulty plugin never stops the rest of the application.

## Core Features

- **Auto-Discovery:** Automatically finds plugins in a directory
- **Validation:** Checks `name`, `version`, `execute()` on each plugin class
- **Fault Tolerance:** Defective plugins are logged but not loaded
- **Zero Dependencies:** Python standard library only

## Files

```
scripts/
  plugin_system.py       Core: PluginBase (ABC) + PluginManager
  cli_demo.py            Demo CLI with argparse
  test_plugin_system.py  16+ unit tests
examples/
  hello.py               Hello World plugin
  calculator.py          Calculator plugin
  systeminfo.py          System Info plugin
```

## Quick Start

### 1. Create a Plugin

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. Use PluginManager

```python
from plugin_system import PluginManager

manager = PluginManager(plugins_dir="./my_plugins")
plugins = manager.discover_plugins()

# List all plugins (Deutsch)
manager.list_plugins()

# Execute a plugin (Deutsch)
success, result = manager.execute_plugin("MyPlugin", param="value")
if success:
    print(result)
```

### 3. Integrate into Your App

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Plugin Interface

Every plugin must:

| Requirement | Details |
|-------------|---------|
| Inherit `PluginBase` | `from plugin_system import PluginBase` |
| Set `name` | Class attribute, non-empty |
| Set `version` | Class attribute, semantic versioning |
| Implement `execute()` | Arbitrary `*args, **kwargs` |

## Fault Tolerance

| Error Type | Behavior |
|-----------|----------|
| SyntaxError in plugin | Plugin is skipped, rest loads |
| Missing attributes | Plugin is marked as `is_valid=False` |
| Exception in `execute()` | Returns `(False, error_message)` |
| No plugin in directory | Empty list, no crash |

## Changelog

### 1.0.0 (2026-03-12)
- Migration from MODULAR_AGENTS/plugins to skill library
- PluginBase ABC + PluginManager
- 3 example plugins (Hello, Calculator, SystemInfo)
- 16+ unit tests
- CLI demo with argparse
