---
name: sync-docs
description: コード変更を検出し、関連ドキュメントを自動更新。git diffからAPIエンドポイント、スキーマ、設定ファイルの変更を特定し、対応するドキュメントを同期。
---

# ドキュメント同期スキル

このスキルは、コード変更を検出して関連ドキュメントを自動的に更新します。

## 対象ドキュメント

| ドキュメント | 関連コード |
|-------------|-----------|
| `docs/API.md` | `apps/main/src/app/api/**` |
| `docs/TESTING.md` | `vitest.config.ts`, `**/*.test.ts`, `**/*.stories.tsx` |
| `docs/DEPLOYMENT.md` | `apps/main/vercel.json`, `compose.yml`, `next.config.ts` |
| `docs/SECURITY.md` | 認証/認可関連コード、セキュリティヘッダー設定 |
| `docs/TROUBLESHOOTING.md` | 新しいエラーパターン、解決策 |
| `ARCHITECTURE.md` | `packages/`, ディレクトリ構造、技術スタック変更 |
| `CLAUDE.md` | コマンド、パターン、開発ガイドライン |
| `CONTRIBUTING.md` | 開発フロー、コード規約 |
| `README.md` | プロジェクト概要、セットアップ手順 |

## 実行手順

### 1. 変更の検出

git diffを使用して変更されたファイルを検出：

```bash
# ステージング済みの変更
git diff --cached --name-only

# 未ステージングの変更
git diff --name-only

# 最近のコミットとの差分
git diff HEAD~1 --name-only
```

### 2. 関連ドキュメントの特定

変更ファイルに基づいて更新が必要なドキュメントを特定：

| 変更パターン | 更新ドキュメント |
|-------------|-----------------|
| `apps/main/src/app/api/**/*.ts` | `docs/API.md` |
| `packages/database/src/schema/**` | `ARCHITECTURE.md`, `CLAUDE.md` |
| `apps/main/vercel.json`, `compose.yml` | `docs/DEPLOYMENT.md` |
| `packages/helpers/src/**` | `CLAUDE.md` (ヘルパー関数セクション) |
| `vitest.*.ts`, `**/*.test.ts` | `docs/TESTING.md` |
| `package.json` (scripts変更) | `CLAUDE.md` (必須コマンド) |
| `.github/workflows/**` | `docs/DEPLOYMENT.md`, `CONTRIBUTING.md` |
| `next.config.ts` | `docs/DEPLOYMENT.md`, `ARCHITECTURE.md` |
| `apps/main/src/app/_components/**` | `CLAUDE.md` (コンポーネント構成) |
| 新しいパッケージ追加 | `ARCHITECTURE.md` |

### 3. ドキュメント更新

各ドキュメントを読み込み、変更内容に基づいて更新：

#### API.md の更新

1. 新しいエンドポイントの追加
2. エンドポイントのリクエスト/レスポンス仕様変更
3. エンドポイントの削除（非推奨化）

例：
```markdown
### 新規エンドポイント: ○○API

#### エンドポイント名

説明

\`\`\`
METHOD /api/path
\`\`\`

**リクエストボディ：**
...

**レスポンス：**
...
```

#### CLAUDE.md の更新

1. 新しいコマンドの追加
2. スキーマ/パターンの変更
3. 開発ガイドラインの更新

#### ARCHITECTURE.md の更新

1. ディレクトリ構造の変更
2. 技術スタックの追加/変更
3. パッケージ依存関係の変更

### 4. 変更の確認

更新後、以下を確認：

- マークダウンの構文エラーがないか
- リンクが正しいか
- 情報が最新か
- 一貫性があるか

## 使用例

### 例1: API変更後のドキュメント更新

```
「API変更をドキュメントに反映して」
または
「/sync-docs」
```

スキルの動作：
1. `git diff --name-only` で変更ファイルを確認
2. `apps/main/src/app/api/` の変更を検出
3. 変更されたAPIファイルを読み込み
4. `docs/API.md` を更新

### 例2: スキーマ変更後のドキュメント更新

```
「データベーススキーマを変更したので、ドキュメントを更新して」
```

スキルの動作：
1. `packages/database/src/schema/` の変更を検出
2. 新しいテーブル/カラムを特定
3. `ARCHITECTURE.md` のスキーマセクションを更新
4. `CLAUDE.md` のデータベーススキーマセクションを更新

### 例3: 新機能追加後の包括的更新

```
「新機能を追加したので、関連ドキュメントをすべて更新して」
```

スキルの動作：
1. すべての変更ファイルを分析
2. 関連する全ドキュメントを特定
3. 各ドキュメントを順次更新
4. 変更サマリーを報告

## 更新テンプレート

### 新規APIエンドポイント追加時

```markdown
### [機能名]API

#### [操作名]

[説明]

\`\`\`
[METHOD] /api/[path]
\`\`\`

**リクエストボディ：**
\`\`\`json
{
  "field": "type"
}
\`\`\`

**パラメータ：**
| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| field | type | ✓/- | 説明 |

**レスポンス：**
\`\`\`json
{
  "field": "value"
}
\`\`\`

**実装詳細：**
- 詳細1
- 詳細2
```

### 新規ヘルパー関数追加時（CLAUDE.md）

```markdown
- `category/` - [カテゴリ名]関連（function1, function2）
```

### 新規スキーマ追加時（ARCHITECTURE.md）

```markdown
- [カテゴリ]: [テーブル名1], [テーブル名2]
```

## 注意事項

- 自動生成された内容は必ず確認する
- 機密情報（APIキー、パスワード等）をドキュメントに含めない
- 日本語で記述（プロジェクトの規約に従う）
- マークダウン構文を正しく使用
- 既存のドキュメントスタイルに合わせる
- 変更履歴を適切にコミットメッセージに含める

## 自動検出パターン

以下のパターンは特に注意して検出：

1. **新規エクスポート**: `export function`, `export const`
2. **スキーマ定義**: `createTable`, `z.object`
3. **ルート定義**: `export async function GET/POST/PUT/DELETE`
4. **設定変更**: `next.config.ts`, `vercel.json`, `package.json`
5. **コマンド追加**: `scripts` セクションの変更
