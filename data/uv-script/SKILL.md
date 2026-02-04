---
name: uv-script
description: Create standalone Python scripts using uv shebang with PEP 723 inline metadata. Use when creating single-file Python tools or scripts that need dependency management without a full project setup.
allowed-tools: Read, Write, Glob
---

# uv Shebang Python Script

Pythonで単体スクリプトを作成する際に使用するスキル。

## 発火条件

- Pythonで単体スクリプト（単一ファイルで完結するツール）を作成するとき
- 発火させたくない場合はユーザーが明示的に伝える（例：「プロジェクトのvenv使うのでuv単体スクリプトにしないで」）

## テンプレート

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""スクリプトの説明."""

import argparse
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="スクリプトの説明")
    parser.add_argument("arg", help="引数の説明")
    args = parser.parse_args()

    # メイン処理

    return 0


if __name__ == "__main__":
    sys.exit(main())
```

## 構成要素

### シェバン

```python
#!/usr/bin/env -S uv run --script
```

`-S` オプションで複数引数を渡す。これによりuvが依存関係を自動解決して実行する。

### PEP 723 インラインメタデータ

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.28",
#     "rich",
# ]
# ///
```

- TOMLコメント形式で依存関係を宣言
- `requires-python`: 最小Pythonバージョン（3.11以上推奨）
- `dependencies`: pipの要件指定形式で依存パッケージを列挙

### エントリーポイント

```python
def main() -> int:
    # 処理
    return 0  # 終了コード

if __name__ == "__main__":
    sys.exit(main())
```

- `main()` は終了コードを返す（成功: 0、失敗: 1）
- `sys.exit()` で終了コードを伝播

## ベストプラクティス

### エラー出力

```python
print("Error: something went wrong", file=sys.stderr)
return 1
```

エラーメッセージは標準エラー出力へ。

### 引数処理

シンプルな場合は `argparse`、複雑なCLIは `typer` を依存に追加：

```python
# dependencies = ["typer"]
```

### 型ヒント

Python 3.11+の型ヒント構文を使用：

```python
def process(items: list[str]) -> dict[str, int]:
    ...
```

## ファイル配置

dotfilesリポジトリの場合：

- `dot_scripts/executable_<name>` として配置
- chezmoi適用後 `~/.scripts/<name>` として利用可能
