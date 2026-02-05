---
name: auto-build
description: プロジェクトタイプを自動検出してビルドを実行するスキル。コード変更後にビルドを提案、エラー発生時は修正案を提示。Node.js、Rust、Python、Go、Makefileプロジェクトに対応。
---

# 自動ビルドスキル

プロジェクトの設定を自動検出し、適切なビルドコマンドを実行します。

## 自動提案のタイミング

| 状況 | 提案内容 |
|------|----------|
| コード変更後 | 「ビルドしますか？」 |
| 依存関係追加後 | 「依存関係をインストールしてビルドしますか？」 |
| 設定ファイル変更後 | 「クリーンビルドを実行しますか？」 |
| ビルドエラー発生時 | 「エラーを修正してリビルドしますか？」 |
| テスト前 | 「先にビルドを確認しますか？」 |

## プロジェクトタイプの自動検出

| ファイル | プロジェクトタイプ | パッケージマネージャー |
|----------|-------------------|----------------------|
| `package.json` | Node.js | npm/yarn/pnpm |
| `Cargo.toml` | Rust | cargo |
| `pyproject.toml` | Python | pip/poetry |
| `go.mod` | Go | go |
| `pom.xml` | Java (Maven) | mvn |
| `build.gradle` | Java (Gradle) | gradle |
| `Makefile` | Make | make |

### パッケージマネージャーの検出（Node.js）

```bash
# 優先順位
if [ -f "pnpm-lock.yaml" ]; then
    PM="pnpm"
elif [ -f "yarn.lock" ]; then
    PM="yarn"
elif [ -f "bun.lockb" ]; then
    PM="bun"
else
    PM="npm"
fi
```

## ビルドコマンド

### Node.js プロジェクト

```bash
# 依存関係インストール（必要な場合）
$PM install

# 標準ビルド
$PM run build

# プロダクションビルド
$PM run build:prod  # または NODE_ENV=production $PM run build

# クリーンビルド
rm -rf dist node_modules/.cache && $PM run build
```

### Rust プロジェクト

```bash
# 依存関係解決
cargo fetch

# デバッグビルド
cargo build

# リリースビルド
cargo build --release

# クリーンビルド
cargo clean && cargo build --release
```

### Python プロジェクト

```bash
# 仮想環境（pyproject.tomlの場合）
poetry install  # または pip install -e .

# ビルド
python -m build

# wheel作成
pip wheel .
```

### Go プロジェクト

```bash
# 依存関係取得
go mod download

# ビルド
go build

# プロダクションビルド
CGO_ENABLED=0 go build -ldflags="-s -w"
```

### Makefile プロジェクト

```bash
# 標準ビルド
make

# クリーンビルド
make clean && make

# 特定ターゲット
make build
make release
```

## ビルドフロー

```
┌─────────────────┐
│ プロジェクト検出 │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 依存関係確認    │ ──→ なければインストール
└────────┬────────┘
         ↓
┌─────────────────┐
│ ビルド実行      │
└────────┬────────┘
         ↓
    ┌────┴────┐
    ↓         ↓
┌───────┐ ┌───────┐
│ 成功  │ │ 失敗  │ ──→ エラー分析・修正提案
└───────┘ └───────┘
```

## エラーハンドリング

### 一般的なエラーと対処

| エラー | 原因 | 対処 |
|--------|------|------|
| `MODULE_NOT_FOUND` | 依存関係不足 | `npm install` を実行 |
| `Type error` | TypeScript型エラー | 型定義を修正 |
| `Syntax error` | 構文エラー | 該当箇所を修正 |
| `Out of memory` | メモリ不足 | `NODE_OPTIONS=--max-old-space-size=4096` |

### エラー分析の流れ

1. エラーメッセージを解析
2. エラータイプを特定
3. 該当ファイル・行を特定
4. 修正案を提示
5. ユーザー確認後に修正・リビルド

## 使用シナリオ

### シナリオ1: コード変更後

```
AI: コードを変更しました。ビルドを実行しますか？

# 検出結果
プロジェクトタイプ: Node.js (TypeScript)
パッケージマネージャー: pnpm

# 実行
pnpm run build
```

### シナリオ2: 依存関係追加後

```
AI: 新しい依存関係を追加しました。インストールしてビルドしますか？

# 実行
pnpm install && pnpm run build
```

### シナリオ3: ビルドエラー発生時

```
AI: ビルドエラーが発生しました。

エラー: Cannot find module '@types/node'

修正案:
1. @types/node をインストール
2. リビルド

実行しますか？

# 実行
pnpm add -D @types/node && pnpm run build
```

### シナリオ4: クリーンビルド

```
AI: 設定ファイルが変更されました。クリーンビルドを推奨します。

# 実行
rm -rf dist .cache && pnpm run build
```

## プロジェクト固有の設定

`CLAUDE.md` または `PROJECT.md` にビルド設定を記載可能：

```markdown
## ビルド設定
- ビルドコマンド: `npm run custom-build`
- テストコマンド: `npm run test:all`
- プロダクションビルド: `npm run build:prod`
- 前処理: `npm run prebuild`
```

## 判断基準

### ビルドを提案する条件

- ソースコード（.ts, .js, .rs, .py, .go）が変更された
- 設定ファイル（tsconfig.json, Cargo.toml等）が変更された
- 依存関係ファイル（package.json等）が変更された
- ユーザーが「ビルド」「コンパイル」と言及

### クリーンビルドを提案する条件

- ビルド設定ファイルが変更された
- 依存関係のバージョンが変更された
- 前回ビルドが失敗している
- キャッシュ関連のエラーが発生

## 注意事項

- ビルド前に未保存の変更がないか確認
- 長時間ビルドの場合は進捗を表示
- 複数のビルドターゲットがある場合は選択を促す
- CI/CD環境との整合性を考慮
