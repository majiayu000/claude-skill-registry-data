---
name: python-mcp-development
description: 'Python SDKとFastMCPフレームワークを使用したMCPサーバー構築ガイド。PythonベースのMCPサーバーの作成、ツール・リソース・プロンプト実装、Pydanticモデル活用、STDIOおよびHTTPトランスポート設定を行う際に使用。'
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Python MCP Server Development

このスキルは、Python SDKとFastMCPフレームワークを使用したModel Context Protocol (MCP) サーバーの構築を支援します。

## いつこのスキルを使用するか

以下の場合に本スキルを活用してください:

- Python でMCPサーバーを新規作成する
- ツール、リソース、プロンプトをMCPサーバーに実装する
- FastMCPデコレータを使用した開発を行う
- Pydanticモデルによる型安全な実装を行う
- STDIOまたはHTTPトランスポートを設定する
- MCP Inspector を使用したテストとデバッグを行う
- 既存のPython MCPサーバーを最適化・リファクタリングする

## 開発環境のセットアップ

### 1. プロジェクト初期化

```bash
# uvを使用した新規プロジェクト作成
uv init mcp-server-demo
cd mcp-server-demo

# MCP SDKのインストール
uv add "mcp[cli]"

# 開発依存関係（推奨）
uv add --dev pytest pytest-asyncio
```

### 2. pyproject.toml の設定例

[プロジェクト設定ファイル](./templates/pyproject.toml)を参照してください。

## ツール実装パターン

### 基本的なツール

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My Server")

@mcp.tool()
def calculate(a: int, b: int, operation: str) -> int:
    """数値計算を実行します。

    Args:
        a: 第一オペランド
        b: 第二オペランド
        operation: 演算子 (add, subtract, multiply, divide)

    Returns:
        計算結果
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("ゼロ除算エラー")
        return a / b
    else:
        raise ValueError(f"未知の演算: {operation}")
```

### Pydanticモデルを使用した構造化出力

```python
from pydantic import BaseModel, Field
from typing import List

class WeatherData(BaseModel):
    """天気データ構造"""
    temperature: float = Field(description="摂氏温度")
    condition: str = Field(description="天候状態")
    humidity: float = Field(ge=0, le=100, description="湿度(%)")
    wind_speed: float = Field(ge=0, description="風速(m/s)")

@mcp.tool()
def get_weather(city: str, country_code: str = "JP") -> WeatherData:
    """指定された都市の天気情報を取得します。

    構造化された天気データを返すため、LLMが解析しやすくなります。
    """
    # 実際のAPI呼び出しをここに実装
    return WeatherData(
        temperature=22.5,
        condition="晴れ",
        humidity=65.0,
        wind_speed=3.2
    )
```

### Contextを使用した高度なツール

```python
from mcp.server.fastmcp import Context
from mcp.server.session import ServerSession

@mcp.tool()
async def process_large_file(
    file_path: str,
    ctx: Context[ServerSession, None]
) -> str:
    """大きなファイルを段階的に処理し、進捗を報告します。"""

    # ログ出力（stderrに送信）
    await ctx.info(f"処理開始: {file_path}")

    # 進捗報告
    total_lines = 1000  # 例
    for i in range(0, total_lines, 100):
        await ctx.report_progress(i, total_lines, f"{i}/{total_lines}行処理完了")
        # 処理ロジック

    await ctx.info("処理完了")
    return f"ファイル処理完了: {file_path}"
```

## リソース実装パターン

### 静的リソース

```python
@mcp.resource("config://app")
def get_app_config() -> str:
    """アプリケーション設定を返す静的リソース"""
    return """
    {
        "version": "1.0.0",
        "debug": false,
        "max_connections": 100
    }
    """
```

### 動的リソース（URIテンプレート）

```python
@mcp.resource("users://{user_id}")
def get_user_profile(user_id: str) -> str:
    """ユーザーIDに基づいてプロファイルを動的に取得"""
    # データベースクエリなど
    return f"User {user_id} profile data"

@mcp.resource("files://{category}/{filename}")
def get_file_content(category: str, filename: str) -> str:
    """カテゴリとファイル名からファイル内容を取得"""
    file_path = f"./data/{category}/{filename}"
    with open(file_path, 'r') as f:
        return f.read()
```

## プロンプト実装パターン

```python
from mcp.server.fastmcp.prompts import base

@mcp.prompt(title="Code Review Prompt")
def create_code_review_prompt(
    code: str,
    language: str = "python"
) -> list[base.Message]:
    """コードレビュー用のプロンプトを生成"""
    return [
        base.UserMessage(f"以下の{language}コードをレビューしてください:"),
        base.UserMessage(f"```{language}\n{code}\n```"),
        base.AssistantMessage("コードレビューを開始します。")
    ]
```

## エラーハンドリングのベストプラクティス

```python
from typing import Union

@mcp.tool()
async def safe_api_call(endpoint: str) -> Union[dict, str]:
    """エラーハンドリング付きAPI呼び出し"""
    try:
        # API呼び出しロジック
        response = await make_api_request(endpoint)
        return response.json()
    except ConnectionError as e:
        return f"接続エラー: {str(e)}"
    except TimeoutError as e:
        return f"タイムアウト: {str(e)}"
    except ValueError as e:
        return f"バリデーションエラー: {str(e)}"
    except Exception as e:
        return f"予期しないエラー: {type(e).__name__}: {str(e)}"
```

## トランスポート設定

### STDIOトランスポート（デフォルト）

```python
if __name__ == "__main__":
    # ローカル実行、Claude Desktopなどで使用
    mcp.run()  # または mcp.run(transport="stdio")
```

### HTTPトランスポート

```python
if __name__ == "__main__":
    # リモートアクセス、Web統合で使用
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000
    )
```

### Starlette/FastAPIへのマウント

```python
from starlette.applications import Starlette
from starlette.routing import Mount

app = Starlette(routes=[
    Mount("/mcp", app=mcp.streamable_http_app())
])
```

## テストとデバッグ

### MCP Inspector を使用したテスト

```bash
# サーバーを起動してInspectorで検査
uv run mcp dev server.py

# ブラウザで http://localhost:5173 を開く
```

### Claude Desktop へのインストール

```bash
# Claude Desktopの設定に追加
uv run mcp install server.py
```

### 単体テストの例

[テストサンプル](./examples/test_server.py)を参照してください。

## セキュリティチェックリスト

- [ ] 入力バリデーション: すべてのパラメータをPydanticで検証
- [ ] アクセス制御: ファイルシステム操作を許可ディレクトリに制限
- [ ] 環境変数: APIキーなどのシークレットをコードにハードコードしない
- [ ] エラーメッセージ: 内部実装の詳細を露出しない
- [ ] レート制限: 外部API呼び出しにタイムアウトを設定
- [ ] ログ: STDIO使用時はstderrのみにログ出力
- [ ] 型安全性: すべての関数に型ヒントを付与

## 一般的な問題と解決策

### 問題1: STDIO サーバーでログが出力されない

**原因**: `print()` を使用すると、JSON-RPCメッセージが破損します。

**解決策**:
```python
# ❌ 悪い例
print("デバッグメッセージ")

# ✅ 良い例
import sys
sys.stderr.write("デバッグメッセージ\n")

# または Contextを使用
await ctx.info("デバッグメッセージ")
```

### 問題2: スキーマバリデーションエラー

**原因**: 型ヒントとPydanticモデルが一致していません。

**解決策**:
```python
from pydantic import Field

class Config(BaseModel):
    timeout: int = Field(ge=0, le=3600, description="タイムアウト秒")

@mcp.tool()
def set_config(config: Config) -> str:
    # 型が完全に一致
    return f"設定完了: timeout={config.timeout}"
```

### 問題3: リソースが見つからない

**原因**: URIテンプレートのパラメータ抽出エラー。

**解決策**:
```python
# URIパターンを明確に定義
@mcp.resource("data://{category}/{id}")
def get_data(category: str, id: str) -> str:
    # パラメータ名が一致していることを確認
    return f"Category: {category}, ID: {id}"
```

## 参考リソース

- [Python MCP SDK GitHub](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [プロジェクトテンプレート](./templates/)
- [実装例](./examples/)

## 次のステップ

1. [プロジェクトテンプレート](./templates/basic-server.py)からサーバーを作成
2. MCP Inspectorでツールをテスト
3. [セキュリティチェックリスト](#セキュリティチェックリスト)を確認
4. Claude Desktopで統合テスト
