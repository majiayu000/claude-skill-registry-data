---
name: go-backend-workflow
description: Goバックエンドのビルド・テスト・Lintワークフロー。「Goビルド」「バックエンドテスト」「golangci-lint」「go mod」「go test」「swagger」などのキーワードで自動適用。
---

# Go Backend Workflow

Go バックエンドプロジェクトのビルド・テスト・品質管理ワークフロー。

## コマンド一覧

| コマンド | 用途 | 実行時間 |
|---------|------|---------|
| `/go-backend:go-build` | バイナリビルド | 〜30秒 |
| `/go-backend:go-test` | テスト実行 | 〜1分 |
| `/go-backend:go-lint` | 静的解析 (golangci-lint) | 〜30秒 |
| `/go-backend:go-run` | 開発サーバー起動 | 即時 |
| `/go-backend:go-tidy` | 依存関係整理 | 〜10秒 |
| `/go-backend:go-swagger` | Swagger生成 | 〜20秒 |

## 推奨ワークフロー

```
コード変更 → go-build（コンパイル確認）
    ↓ 成功
go-test（テスト実行）
    ↓ 全パス
go-lint（品質チェック）
    ↓ 問題なし
コミット・PR
```

## プロジェクト構成の検出

このプラグインは以下の順序でプロジェクトを検出:

1. **Makefile優先**: `make test`, `make lint` 等のターゲットがあれば使用
2. **go.mod検出**: `go.mod` を探索して直接 `go` コマンドを実行
3. **サブディレクトリ**: `backend/`, `server/`, `api/` 等を探索

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `GO_BACKEND_DIR` | バックエンドディレクトリ | 自動検出 |
| `GO_MAIN_PATH` | main.go のパス | `cmd/server/main.go` |
| `GO_BIN_NAME` | 出力バイナリ名 | `server` |

## よくあるエラーと対処

### go mod tidy が必要

```
go: modules disabled by GO111MODULE=off
```

**対処**:
```bash
export GO111MODULE=on
go mod tidy
```

### golangci-lint が見つからない

```
golangci-lint: command not found
```

**対処**:
```bash
brew install golangci-lint
# または
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

### swag が見つからない

```
swag: command not found
```

**対処**:
```bash
go install github.com/swaggo/swag/cmd/swag@latest
```

## テストカバレッジ

カバレッジ付きテストの実行:

```bash
go test -cover -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
open coverage.html
```

## Lint 設定

プロジェクトルートに `.golangci.yml` を配置することでLintルールをカスタマイズ可能。

推奨設定例:
```yaml
linters:
  enable:
    - errcheck
    - gosimple
    - govet
    - ineffassign
    - staticcheck
    - unused

linters-settings:
  errcheck:
    check-type-assertions: true
```
