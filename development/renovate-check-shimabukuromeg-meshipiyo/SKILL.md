---
name: renovate-check
description: Renovate が作成した GitHub PR の依存関係更新内容を詳細にチェックする。Renovate PR の URL が渡された時、または依存関係更新の PR をレビューする時に使用する。
allowed-tools: Bash, Read, Grep, Glob, WebFetch, WebSearch, Task
---

# Renovate PR チェッカー

Renovate が作成した依存関係更新 PR を包括的に分析し、日本語でレポートを作成します。

## 実行手順

### 1. PR 情報の取得

GitHub PR URL から以下のコマンドで情報を取得:

```bash
gh pr view <PR_URL> --json title,body,files,headRefName,baseRefName,additions,deletions
```

PR タイトルからパッケージ名とバージョン変更を抽出する。

### 2. バージョン変更の種類を判定

セマンティックバージョニングに基づいて判定:

- **Major**: メジャーバージョンアップ（例: v1.x.x → v2.x.x）- 破壊的変更の可能性が高い
- **Minor**: マイナーバージョンアップ（例: v1.1.x → v1.2.x）- 新機能追加、後方互換性あり
- **Patch**: パッチバージョンアップ（例: v1.1.1 → v1.1.2）- バグ修正、後方互換性あり

### 3. 変更内容の調査

WebFetch または WebSearch を使用して:

- パッケージの GitHub リリースページ（`https://github.com/<owner>/<repo>/releases`）を確認
- CHANGELOG.md を確認
- 変更内容を日本語で要約
- 主要な新機能、バグ修正、改善点をリストアップ

### 4. Breaking Changes の確認

リリースノートから以下を探す:

- 「Breaking Changes」「BREAKING」セクション
- マイグレーションガイドの有無
- 非推奨（deprecated）になった API
- 削除された機能

### 5. 本リポジトリでの利用箇所の特定

Grep ツールを使用して検索:

```bash
# ESM import
rg "from ['\"]<package-name>" --type ts --type tsx --type js --type jsx

# CommonJS require
rg "require\(['\"]<package-name>" --type ts --type js

# 設定ファイルでの参照
rg "<package-name>" -g "*.config.*" -g "*.json"
```

影響を受けるファイル一覧と利用方法を出力する。

### 6. 依存関係の互換性確認

更新対象パッケージと、プロジェクト内の他のパッケージとの互換性を確認:

#### 確認手順

1. **package.json の依存関係を確認**:
   ```bash
   cat apps/frontend/package.json | jq '.dependencies, .devDependencies'
   cat apps/backend/package.json | jq '.dependencies, .devDependencies'
   ```

2. **peerDependencies の確認**:
   - 更新パッケージの npm ページまたは package.json で peerDependencies を確認
   - WebSearch で「<package-name> <version> peer dependencies」を検索

3. **主要な依存関係の組み合わせを確認**:

| 更新対象 | 確認すべき関連パッケージ |
|---------|------------------------|
| React | Next.js, React DOM, @types/react, Radix UI, Framer Motion |
| Next.js | React, React DOM, eslint-config-next, @next/* パッケージ |
| TypeScript | @types/* パッケージ、ts-node、各種型定義 |
| Prisma | @prisma/client と prisma CLI のバージョン一致 |
| GraphQL | graphql-request, @graphql-codegen/*, graphql-yoga |
| ESLint | eslint-config-*, eslint-plugin-*, @typescript-eslint/* |
| Biome | @biomejs/biome（単独で動作、依存少ない） |

4. **互換性マトリクスの確認**:
   - Next.js: https://nextjs.org/docs/getting-started/installation で React バージョン要件確認
   - Radix UI: 各コンポーネントの peerDependencies で React バージョン確認
   - Prisma: Client と CLI のバージョンは一致が必要

5. **バージョン制約の確認**:
   ```bash
   # npm でパッケージの peerDependencies を確認
   npm view <package-name>@<version> peerDependencies
   ```

#### 出力に含める情報

- 関連パッケージとの互換性状況（OK / 要アップデート / 非互換）
- 同時にアップデートが必要なパッケージの有無
- バージョン制約による問題の有無

### 7. ビルド/実行環境要件の変更確認

以下を確認:

- Node.js の最小バージョン要件の変更（package.json の engines フィールド）
- pnpm/npm/yarn のバージョン要件
- peerDependencies の変更
- その他のランタイム依存関係の変更

### 8. 周辺ツール設定との互換性確認

本リポジトリで使用しているツールとの互換性をチェック:

- **TypeScript**: `tsconfig.json` の設定、型定義の変更
- **Biome**: `biome.json` での設定との互換性
- **Vitest/Jest**: テスト設定との互換性
- **Webpack/Turbopack/Vite**: バンドラー設定との互換性
- **Next.js**: next.config.js との互換性
- **Prisma**: schema.prisma との互換性（該当する場合）

## 出力フォーマット

以下の形式で日本語レポートを出力:

```markdown
# Renovate PR チェックレポート

## 基本情報

| 項目 | 内容 |
|------|------|
| パッケージ名 | `<package-name>` |
| バージョン変更 | `<old-version>` → `<new-version>` |
| 変更種別 | **Major** / **Minor** / **Patch** |
| PR URL | <url> |

## 変更内容サマリー

<日本語で変更内容を要約（3-5文程度）>

### 主な変更点

- <変更点1>
- <変更点2>
- <変更点3>

## Breaking Changes

<Breaking Changes の有無>

### 詳細（該当する場合）

- <breaking change 1>
- <breaking change 2>

### 必要な対応

<マイグレーション手順や対応方法>

## 本リポジトリでの利用箇所

| ファイル | 利用方法 |
|---------|---------|
| `<file1>` | <usage1> |
| `<file2>` | <usage2> |

**影響範囲**: <影響の大きさを評価>

## 依存関係の互換性

| 関連パッケージ | 現在のバージョン | 互換性 | 備考 |
|---------------|-----------------|--------|------|
| `<package1>` | <version> | OK/要確認/要アップデート | <詳細> |
| `<package2>` | <version> | OK/要確認/要アップデート | <詳細> |

**同時アップデート必要**: <必要なパッケージがあれば記載>

## 環境要件の変更

| 項目 | 変更前 | 変更後 | 対応必要 |
|------|--------|--------|----------|
| Node.js | <old> | <new> | Yes/No |
| peerDependencies | <old> | <new> | Yes/No |

## ツール互換性

| ツール | 互換性 | 備考 |
|--------|--------|------|
| TypeScript | OK/要確認/NG | <詳細> |
| Biome | OK/要確認/NG | <詳細> |
| Next.js | OK/要確認/NG | <詳細> |

## リスク評価

- [ ] **低リスク**: そのままマージ可能
- [ ] **中リスク**: ローカルでの動作確認推奨
- [ ] **高リスク**: 詳細なテストと移行作業が必要

### 推奨アクション

1. <アクション1>
2. <アクション2>
3. <アクション3>

## 参考リンク

- [リリースノート](<url>)
- [CHANGELOG](<url>)
- [マイグレーションガイド](<url>)（該当する場合）
```

### 9. PR へのコメント投稿

レポート作成後、結果を PR のコメントとして投稿する:

```bash
gh pr comment <PR_NUMBER> --body "$(cat <<'EOF'
# Renovate PR チェックレポート

## 基本情報

| 項目 | 内容 |
|------|------|
| パッケージ名 | `<package-name>` |
| バージョン変更 | `<old-version>` → `<new-version>` |
| 変更種別 | **Major** / **Minor** / **Patch** |

## 変更内容サマリー

<簡潔な要約>

### 主な変更点

- <変更点1>
- <変更点2>
- <変更点3>

## Breaking Changes

<Breaking Changes の有無と詳細>

## 本リポジトリでの利用箇所

| ファイル | 利用方法 |
|---------|---------|
| `<file1>` | <usage1> |

## 依存関係の互換性

| 関連パッケージ | バージョン | 互換性 |
|---------------|-----------|--------|
| `<package1>` | <version> | ✅ OK / ⚠️ 要確認 |

## CI ステータス

| チェック | 結果 |
|---------|------|
| format | ✅ SUCCESS / ❌ FAILURE |
| lint | ✅ SUCCESS / ❌ FAILURE |
| typecheck | ✅ SUCCESS / ❌ FAILURE |
| test | ✅ SUCCESS / ❌ FAILURE |

## リスク評価

✅ **低リスク**: そのままマージ可能
/ ⚠️ **中リスク**: ローカルでの動作確認推奨
/ ❌ **高リスク**: 詳細なテストと移行作業が必要

### 推奨アクション

1. <アクション1>
2. <アクション2>

## 参考リンク

- [リリースノート](<url>)

---
🤖 Generated by Renovate Check
EOF
)"
```

**重要**: レポートは簡潔にまとめ、GitHub コメントの文字数制限（65536文字）を超えないようにする。詳細版はユーザーへの出力として表示し、コメントには要約版を投稿する。

## 注意事項

- メジャーバージョンアップの場合は特に慎重に Breaking Changes を確認
- 利用箇所が多いパッケージは影響範囲を詳細に分析
- 不明点がある場合は公式ドキュメントや GitHub Issues を参照
- TypeScript の型定義（@types/*）パッケージの場合は、対応する本体パッケージとの互換性も確認
- **レポート完了後は必ず PR にコメントを投稿すること**
