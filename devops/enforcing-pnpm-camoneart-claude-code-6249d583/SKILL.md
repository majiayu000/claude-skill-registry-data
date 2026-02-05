---
name: Enforcing pnpm
description: Ensure pnpm is used exclusively for package management, blocking npm/yarn commands. Use when running package scripts, installing dependencies, or when user mentions package manager/依存関係/パッケージ.
allowed-tools: Bash, Read
---

# Enforcing pnpm

プロジェクトでpnpmを統一的に使用するための強制スキル。

## いつ使うか

- パッケージのインストール時
- スクリプトの実行時
- 依存関係の管理時
- CI/CD設定時
- ユーザーがパッケージマネージャーについて言及した時

## 基本原則

このプロジェクトは `packageManager: pnpm@xx.x.x` を前提として構成されている。

### 1. 実行コマンド
すべてのスクリプトは `pnpm <script>` 形式で実行：
```bash
pnpm run lint
pnpm test
pnpm build
```

### 2. グローバルコマンド
`pnpx` ではなく `pnpm dlx` を使用：
```bash
# ❌ 間違い
pnpx create-react-app my-app

# ✅ 正しい
pnpm dlx create-react-app my-app
```

### 3. スクリプト内の呼び出し
`package.json` で npm や yarn を呼び出さない：
```json
{
  "scripts": {
    "build": "pnpm run compile"  // ✅
  }
}
```

## 禁止コマンド

以下のコマンドを検知したら**警告し、pnpmに置き換えて再実行**：

### npm コマンド
```bash
npm install    → pnpm install
npm run build  → pnpm run build
npm test       → pnpm test
npx xxx        → pnpm dlx xxx
```

### yarn コマンド
```bash
yarn           → pnpm install
yarn add xxx   → pnpm add xxx
yarn build     → pnpm run build
```

## CI/CD設定

GitHub Actions などの CI でも pnpm を使用：

```yaml
- uses: pnpm/action-setup@v2
  with:
    version: 8

- run: pnpm install --frozen-lockfile

- run: pnpm test
```

### キャッシュ設定
```yaml
- uses: actions/setup-node@v3
  with:
    node-version: 18
    cache: 'pnpm'  # ✅ pnpm-store をキャッシュ
```

## ドキュメント規則

README・各種ドキュメントに掲載するコマンド例も全て `pnpm` 表記へ統一：

```markdown
# ❌ 間違い
npm install
npm run dev

# ✅ 正しい
pnpm install
pnpm run dev
```

## 自動修正フロー

Claude Code が npm コマンドを誤って実行しようとした場合：

1. **警告を表示**
2. **自動で pnpm に置き換え**
3. **再実行**

例：
```
検出: npm install
↓
警告: このプロジェクトではpnpmを使用します
↓
自動変換: pnpm install
↓
実行
```

## 例外処理

以下の場合のみ警告をスキップ：
- ユーザーが明示的に npm/yarn の使用を指示した場合
- package.json の scripts 内で外部ツールが npm を要求する場合（要確認）

## トラブルシューティング

### pnpm がインストールされていない場合
```bash
npm install -g pnpm
# または
corepack enable
corepack prepare pnpm@latest --activate
```

### lockfile の不整合
```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

## チェックリスト

- [ ] 全てのコマンドが `pnpm` 形式か
- [ ] CI設定で `pnpm` を使用しているか
- [ ] ドキュメントが `pnpm` 表記になっているか
- [ ] `package.json` の scripts が `pnpm` を呼び出しているか
