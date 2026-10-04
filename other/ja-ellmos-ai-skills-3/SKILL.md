---
name: plugin-system
version: 1.0.0
type: tool
author: BACH Team
created: 2026-02-21
updated: 2026-03-12
description: Python アプリケーション向けの汎用プラグインシステム。自動検出、検証、障害耐性を備えています。依存関係ゼロ（Python 標準ライブラリのみ）。

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: dev
tags: [plugin, framework, extensibility, cli, architecture]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'MODULAR_AGENTS/plugins', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="../banner.png" width="100%" alt="plugin-system banner">

> **日本語** — `plugin-system` の公式日本語版。


# プラグインシステム (日本語)

Python CLI アプリケーション向けの障害耐性プラグインシステム。
欠陥のあるプラグインがアプリケーションの残りの部分を停止させることはありません。

## 主な機能

- **自動検出:** ディレクトリ内のプラグインを自動的に検出
- **検証:** 各プラグインクラスの `name`、`version`、`execute()` をチェック
- **障害耐性:** 欠陥のあるプラグインはログに記録されますが、ロードされません
- **依存関係ゼロ:** Python 標準ライブラリのみ使用

## ファイル

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

## クイックスタート

### 1. プラグインの作成

```python
from plugin_system import PluginBase

class MyPlugin(PluginBase):
    name = "MyPlugin"
    version = "1.0.0"

    def execute(self, *args, **kwargs):
        return {"status": "ok", "message": "Hello!"}
```

### 2. PluginManager の使用

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

### 3. アプリケーションへの統合

```python
class MyApp:
    def __init__(self):
        self.plugins = PluginManager("./plugins")
        self.plugins.discover_plugins()

    def run_command(self, command, **params):
        success, result = self.plugins.execute_plugin(command, **params)
        return result if success else None
```

## プラグインインターフェース

すべてのプラグインは以下を満たす必要があります:

| 要件 | 詳細 |
|------|------|
| `PluginBase` を継承 | `from plugin_system import PluginBase` |
| `name` を設定 | クラス属性、空でないこと |
| `version` を設定 | クラス属性、セマンティックバージョニング |
| `execute()` を実装 | 任意の `*args, **kwargs` |

## 障害耐性

| エラータイプ | 動作 |
|--------------|------|
| プラグイン内の SyntaxError | プラグインはスキップされ、残りがロードされます |
| 属性の欠落 | プラグインは `is_valid=False` としてマークされます |
| `execute()` 内の例外 | `(False, error_message)` を返します |
| ディレクトリにプラグインがない | 空のリストを返し、クラッシュしません |

## 変更履歴

### 1.0.0 (2026-03-12)
- MODULAR_AGENTS/plugins から skill ライブラリへの移行
- PluginBase ABC + PluginManager
- 3 つのサンプルプラグイン (Hello, Calculator, SystemInfo)
- 16 以上のユニットテスト
- argparse を使用した CLI デモ
