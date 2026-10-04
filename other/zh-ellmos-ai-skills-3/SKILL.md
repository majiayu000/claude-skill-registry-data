---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: 用于 Python 应用程序的通用插件系统。自动发现、验证、容错。零依赖（仅使用 Python 标准库）。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: zh
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="plugin-system banner">

> **中文** — `plugin-system` 官方中文版本。


# 插件系统 (中文)

适用于 Python CLI 应用程序的容错插件系统。
故障插件绝不会阻止应用程序其余部分的运行。

## 核心特性

- **自动发现：** 自动查找目录中的插件
- **验证：** 检查每个插件类上的 `name`、`version`、`execute()`
- **容错性：** 故障插件会被记录日志但不会被加载
- **零依赖：** 仅依赖 Python 标准库

## 文件

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

## 快速开始

### 1. 创建插件

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. 使用 PluginManager

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

### 3. 集成到您的应用程序

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## 插件接口

每个插件必须：

| 要求 | 详细信息 |
|------|----------|
| 继承 `PluginBase` | `from plugin_system import PluginBase` |
| 设置 `name` | 类属性，不能为空 |
| 设置 `version` | 类属性，语义化版本 |
| 实现 `execute()` | 接收任意 `*args, **kwargs` |

## 容错机制

| 错误类型 | 行为 |
|----------|------|
| 插件中存在 SyntaxError | 跳过该插件，加载其余部分 |
| 缺少必需属性 | 插件被标记为 `is_valid=False` |
| `execute()` 抛出异常 | 返回 `(False, error_message)` |
| 目录中没有插件 | 返回空列表，不会崩溃 |

## 变更日志

### 1.0.0 (2026-03-12)
- 从 MODULAR_AGENTS/plugins 迁移至 skill 库
- PluginBase ABC + PluginManager
- 3 个示例插件 (Hello, Calculator, SystemInfo)
- 16+ 个单元测试
- 基于 argparse 的 CLI 演示
