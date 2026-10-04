---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Sistema de plugins genérico para aplicaciones Python. Detección automática, validación y tolerancia a fallos. Sin dependencias (solo biblioteca estándar de Python).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="plugin-system banner">

> **Español** — Versión oficial en español de `plugin-system`.


# Sistema de Plugins (Español)

Sistema de plugins tolerante a fallos para aplicaciones CLI en Python.
Un plugin defectuoso nunca interrumpe la ejecución del resto de la aplicación.

## Características principales

- **Detección automática:** Encuentra automáticamente plugins en un directorio
- **Validación:** Comprueba `name`, `version` y `execute()` en cada clase de plugin
- **Tolerancia a fallos:** Los plugins defectuosos se registran en el log pero no se cargan
- **Sin dependencias:** Solo biblioteca estándar de Python

## Archivos

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

## Inicio rápido

### 1. Crear un plugin

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. Usar PluginManager

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

### 3. Integrar en tu aplicación

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Interfaz de plugin

Cada plugin debe:

| Requisito | Detalles |
|-----------|----------|
| Heredar de `PluginBase` | `from plugin_system import PluginBase` |
| Definir `name` | Atributo de clase, no vacío |
| Definir `version` | Atributo de clase, versionado semántico |
| Implementar `execute()` | Parámetros arbitrarios `*args, **kwargs` |

## Tolerancia a fallos

| Tipo de error | Comportamiento |
|---------------|----------------|
| SyntaxError en plugin | Se omite el plugin, el resto se carga |
| Atributos faltantes | El plugin se marca como `is_valid=False` |
| Excepción en `execute()` | Devuelve `(False, error_message)` |
| Sin plugins en el directorio | Lista vacía, sin caídas |

## Historial de cambios

### 1.0.0 (2026-03-12)
- Migración desde MODULAR_AGENTS/plugins a la biblioteca de skills
- PluginBase ABC + PluginManager
- 3 plugins de ejemplo (Hello, Calculator, SystemInfo)
- Más de 16 pruebas unitarias
- Demo CLI con argparse
