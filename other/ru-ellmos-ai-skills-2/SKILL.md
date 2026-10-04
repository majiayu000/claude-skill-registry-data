---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Универсальная система плагинов для приложений на Python. Автоматическое обнаружение, валидация, отказоустойчивость. Нулевые зависимости (только стандартная библиотека Python).

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: ru
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="plugin-system banner">

> **Русский** — Официальная русская версия `plugin-system`.


# Система плагинов (Русский)

Отказоустойчивая система плагинов для CLI-приложений на Python.
Неисправный плагин никогда не останавливает работу остальной части приложения.

## Основные возможности

- **Автоматическое обнаружение:** Автоматически находит плагины в директории
- **Валидация:** Проверяет `name`, `version`, `execute()` у каждого класса плагина
- **Отказоустойчивость:** Сбойные плагины логируются, но не загружаются
- **Нулевые зависимости:** Только стандартная библиотека Python

## Файлы

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

## Быстрый старт

### 1. Создание плагина

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. Использование PluginManager

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

### 3. Интеграция в ваше приложение

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## Интерфейс плагина

Каждый плагин должен:

| Требование | Детали |
|------------|--------|
| Наследовать `PluginBase` | `from plugin_system import PluginBase` |
| Задавать `name` | Атрибут класса, непустой |
| Задавать `version` | Атрибут класса, семантическое версионирование |
| Реализовывать `execute()` | Произвольные `*args, **kwargs` |

## Отказоустойчивость

| Тип ошибки | Поведение |
|------------|-----------|
| SyntaxError в плагине | Плагин пропускается, остальные загружаются |
| Отсутствие атрибутов | Плагин помечается как `is_valid=False` |
| Исключение в `execute()` | Возвращает `(False, error_message)` |
| Нет плагинов в директории | Пустой список, без сбоев |

## История изменений

### 1.0.0 (2026-03-12)
- Миграция из MODULAR_AGENTS/plugins в библиотеку скиллов
- PluginBase ABC + PluginManager
- 3 примера плагинов (Hello, Calculator, SystemInfo)
- 16+ юнит-тестов
- CLI-демо с argparse
