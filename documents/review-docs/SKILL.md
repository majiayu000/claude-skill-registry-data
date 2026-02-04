---
name: review-docs
description: ドキュメントとコードの乖離を監査。APIエンドポイント、スキーマ、設定ファイルとドキュメントを比較し、不整合をレポート。定期的なドキュメントヘルスチェックに使用。
---

# ドキュメント監査スキル

このスキルは、ドキュメントとコードの乖離を検出し、レポートを生成します。

## 監査対象

| ドキュメント | 検証対象 |
|-------------|---------|
| `docs/API.md` | 実際のAPIエンドポイント |
| `docs/TESTING.md` | テスト設定、テスト戦略 |
| `docs/DEPLOYMENT.md` | デプロイ設定、環境変数 |
| `docs/SECURITY.md` | セキュリティ設定、認証方式 |
| `docs/TROUBLESHOOTING.md` | 解決策の有効性 |
| `ARCHITECTURE.md` | ディレクトリ構造、技術スタック |
| `CLAUDE.md` | コマンド、パターン、ガイドライン |
| `CONTRIBUTING.md` | 開発フロー、コード規約 |
| `README.md` | セットアップ手順、概要 |

## 監査項目

### 1. API.md の監査

#### チェック項目

- [ ] 記載されているエンドポイントが実際に存在するか
- [ ] 実際のエンドポイントがすべて記載されているか
- [ ] HTTPメソッドが正しいか
- [ ] リクエスト/レスポンスの仕様が最新か
- [ ] 認証方式の記述が正確か
- [ ] レート制限の値が正しいか

#### 検証方法

```bash
# 実際のAPIエンドポイントを列挙
find apps/main/src/app/api -name "route.ts" | sort
```

エンドポイントファイルを読み込み、以下を抽出：
- エクスポートされているHTTPメソッド（GET, POST, PUT, DELETE等）
- Zodスキーマ（リクエストバリデーション）
- レスポンス形式

### 2. ARCHITECTURE.md の監査

#### チェック項目

- [ ] ディレクトリ構造が実際と一致するか
- [ ] 技術スタックのバージョンが最新か
- [ ] パッケージ依存関係が正確か
- [ ] データベーススキーマが最新か
- [ ] 図表が現状を反映しているか

#### 検証方法

```bash
# 実際のディレクトリ構造
tree -L 3 -I "node_modules|.next|.git"

# パッケージバージョン
cat package.json | jq '.dependencies, .devDependencies'

# スキーマファイル
ls packages/database/src/schema/
```

### 3. CLAUDE.md の監査

#### チェック項目

- [ ] 必須コマンドが実行可能か
- [ ] スクリプト名が `package.json` と一致するか
- [ ] ヘルパー関数のリストが最新か
- [ ] コンポーネント構成が実際と一致するか
- [ ] テスト戦略が現状を反映しているか
- [ ] TailwindCSSトークンが最新か

#### 検証方法

```bash
# package.json scripts
cat package.json | jq '.scripts'

# ヘルパー関数
ls packages/helpers/src/

# コンポーネント
ls apps/main/src/app/_components/
```

### 4. DEPLOYMENT.md の監査

#### チェック項目

- [ ] 環境変数リストが最新か
- [ ] Cronジョブ設定が `vercel.json` と一致するか
- [ ] Docker設定が `compose.yml` と一致するか
- [ ] デプロイフローが現状を反映しているか

#### 検証方法

```bash
# 環境変数
cat apps/main/.env.example

# Cronジョブ
cat apps/main/vercel.json | jq '.crons'

# Docker設定
cat compose.yml
```

### 5. CONTRIBUTING.md の監査

#### チェック項目

- [ ] 開発環境セットアップ手順が最新か
- [ ] コード規約がBiome設定と一致するか
- [ ] ブランチ戦略が現状を反映しているか
- [ ] PR/Issue テンプレートが存在するか

### 6. README.md の監査

#### チェック項目

- [ ] プロジェクト説明が現状を反映しているか
- [ ] インストール手順が動作するか
- [ ] バッジ/ステータスが最新か
- [ ] リンクが有効か

### 7. TESTING.md の監査

#### チェック項目

- [ ] テスト実行コマンドが動作するか
- [ ] テスト戦略が現状を反映しているか
- [ ] カバレッジ目標が最新か
- [ ] モック戦略が実装と一致するか

### 8. SECURITY.md の監査

#### チェック項目

- [ ] セキュリティ対策が実装されているか
- [ ] 認証方式の記述が正確か
- [ ] 依存関係の脆弱性がないか
- [ ] セキュリティヘッダーが設定されているか

### 9. TROUBLESHOOTING.md の監査

#### チェック項目

- [ ] 解決策が有効か
- [ ] コマンドが動作するか
- [ ] 参照先が存在するか
- [ ] 新しい問題が追加されるべきか

## レポート形式

監査結果は以下の形式でレポート：

```markdown
# ドキュメント監査レポート

**監査日時:** YYYY-MM-DD HH:MM
**対象ドキュメント:** [リスト]

## サマリー

| ドキュメント | ステータス | 問題数 |
|-------------|-----------|-------|
| docs/API.md | ⚠️ 要更新 | 3 |
| ARCHITECTURE.md | ✅ 最新 | 0 |
| CLAUDE.md | ⚠️ 要更新 | 2 |
| ... | ... | ... |

## 詳細

### docs/API.md

#### 問題1: 未記載のエンドポイント
- **対象:** `/api/new-endpoint`
- **発見日:** YYYY-MM-DD
- **推奨対応:** エンドポイントの仕様を追加

#### 問題2: 古い仕様
- **対象:** `/api/blog/views` のレスポンス形式
- **現状:** ドキュメントには `{ views: number }` と記載
- **実際:** `204 No Content` を返却
- **推奨対応:** レスポンス形式の記述を修正

### CLAUDE.md

#### 問題1: 存在しないコマンド
- **対象:** `pnpm run lint`
- **現状:** ドキュメントに記載あり
- **実際:** `pnpm run check` に変更済み
- **推奨対応:** コマンド名を修正

## 推奨アクション

1. [ ] docs/API.md: 新しいエンドポイントを追加
2. [ ] CLAUDE.md: コマンド名を修正
3. [ ] ...
```

## 使用例

### 例1: 全体監査

```
「ドキュメントの監査をして」
または
「/review-docs」
```

スキルの動作：
1. すべての対象ドキュメントを読み込み
2. 対応するコードファイルを読み込み
3. 比較・検証
4. レポートを生成

### 例2: 特定ドキュメントの監査

```
「API.mdが最新か確認して」
```

スキルの動作：
1. `docs/API.md` を読み込み
2. `apps/main/src/app/api/` 配下のファイルを読み込み
3. エンドポイント一覧を比較
4. 不整合を報告

### 例3: PR前の確認

```
「PRを作る前にドキュメントの確認をして」
```

スキルの動作：
1. `git diff` で変更ファイルを確認
2. 変更に関連するドキュメントのみ監査
3. 必要な更新を提案

## 自動検出パターン

以下は検出ロジックの実装イメージを示す疑似コードです。

### API不整合の検出

```typescript
// ドキュメントからエンドポイントを抽出
const docEndpoints = extractEndpointsFromMarkdown(apiMd);
// POST /api/blog/views
// GET /api/subscriptions/verify
// ...

// コードからエンドポイントを抽出
const codeEndpoints = extractEndpointsFromCode(apiRoutes);
// apps/main/src/app/api/blog/views/route.ts -> POST
// apps/main/src/app/api/subscriptions/verify/route.ts -> GET
// ...

// 差分を検出
const missing = codeEndpoints.filter(e => !docEndpoints.includes(e));
const outdated = docEndpoints.filter(e => !codeEndpoints.includes(e));
```

### コマンド不整合の検出

```typescript
// CLAUDE.mdからコマンドを抽出
const docCommands = extractCommandsFromMarkdown(claudeMd);
// pnpm run dev
// pnpm run build
// ...

// package.jsonからコマンドを抽出
const pkgCommands = Object.keys(packageJson.scripts);
// dev, build, test, ...

// 差分を検出
const invalidCommands = docCommands.filter(cmd =>
  !pkgCommands.includes(cmd.replace('pnpm run ', ''))
);
```

### スキーマ不整合の検出

```typescript
// ARCHITECTURE.mdからスキーマを抽出
const docSchemas = extractSchemasFromMarkdown(archMd);
// blogs, talks, quizzes, ...

// コードからスキーマを抽出
const codeSchemas = fs.readdirSync('packages/database/src/schema/')
  .filter(f => f.endsWith('.ts'))
  .map(f => f.replace('.ts', ''));

// 差分を検出
const missingSchemas = codeSchemas.filter(s => !docSchemas.includes(s));
```

## 重大度レベル

| レベル | 説明 | 例 |
|-------|------|-----|
| 🔴 Critical | 機能に関わる誤情報 | 存在しないAPIエンドポイント |
| 🟠 High | 重要な情報の欠落 | 新機能が未記載 |
| 🟡 Medium | 細かい不整合 | バージョン番号のずれ |
| 🟢 Low | 軽微な改善点 | 表現の改善 |

## 注意事項

- 監査結果は提案であり、すべてを機械的に適用しない
- コンテキストを考慮して判断する
- 一時的な変更（実験的機能等）は除外することがある
- ドキュメントの意図を尊重する
- 大規模な変更は段階的に実施

## 定期実行の推奨

以下のタイミングで監査を実行することを推奨：

1. **PR作成前**: 変更に関連するドキュメントのみ
2. **週次**: 全体監査
3. **リリース前**: 重要ドキュメントの全体確認
4. **大規模変更後**: 影響範囲の確認
