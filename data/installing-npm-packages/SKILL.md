---
name: personal-installing-npm-packages
description: npm、yarn、pnpm、bun で適切なバージョンのパッケージをインストールします。npm、yarn、pnpm、bun を使ってパッケージをインストールするときに必ず使用してください。
---

# パッケージインストール

## ワークフロー

### 1. パッケージマネージャーの検出

#### 1-1. `packageManager` フィールドを確認

```bash
grep '"packageManager"' package.json
```

#### 1-2. lock ファイルを確認（`packageManager` フィールドがない場合）

```bash
ls package-lock.json yarn.lock pnpm-lock.yaml bun.lockb 2>/dev/null
```

### 2. 最新バージョンを取得

```bash
npm view <pkg> version
```

### 3. インストール

| 種類            | npm                        | yarn                    | pnpm                    | bun                    |
| --------------- | -------------------------- | ----------------------- | ----------------------- | ---------------------- |
| dependencies    | `npm install <pkg>@<v>`    | `yarn add <pkg>@<v>`    | `pnpm add <pkg>@<v>`    | `bun add <pkg>@<v>`    |
| devDependencies | `npm install -D <pkg>@<v>` | `yarn add -D <pkg>@<v>` | `pnpm add -D <pkg>@<v>` | `bun add -d <pkg>@<v>` |
