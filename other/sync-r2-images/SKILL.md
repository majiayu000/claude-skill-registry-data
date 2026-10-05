---
name: sync-r2-images
description: >
  R2上の画像をローカルに同期する。Use when user asks to [画像が見えない, R2画像を同期, /sync-r2-images].
domain: ops
---

Cloudflare R2 にアップロード済みの画像を、ローカル開発環境に同期する。

MDX ファイルから参照画像を自動スキャンしてダウンロードするため、手動で画像リストを指定する必要がありません。

## 用途

- **ローカル初期セットアップ時**: `git clone` → `npm install` → `/sync-r2-images` → `npm run dev`
- **新規開発者向け**: 画像がない状態で `npm run dev` したとき
- **プルリクエスト後**: 新しい画像が追加されたページで画像が見えないとき

## 前提条件

- `npm install` が完了していること
- インターネット接続が可能であること

## オプション

```
/sync-r2-images [--prefix {category}] [--dry-run]
```

- `--prefix {category}`: 特定カテゴリの画像のみを同期（例: `civil-construction-1/guide-earthwork`）
- `--dry-run`: ダウンロード対象を確認のみ、実行しない

## 処理手順

### Phase 1: スキャン

1. `content/site/**/*.mdx` を全スキャン
2. `<img src="/posts/{path}" />`（または `<ArticleImage src="/posts/{path}" />`）パターンで参照画像を自動抽出
3. --prefix が指定されている場合は、マッチするものだけに絞り込み
4. ローカルに既に存在するファイルはスキップ対象に

### Phase 2: 確認

1. ダウンロード対象の画像リストを表示
2. 件数と総容量（推定）を表示
3. ユーザーに確認：「ダウンロードを実行しますか？」

### Phase 3: ダウンロード

1. `node .claude/skills/dev/sync-r2-images/scripts/download-images-from-r2.mjs` を実行（--dry-run の場合は --dry-run を渡す）
2. 各画像を `https://storage.doboku-note.com/posts/{path}` からダウンロード
3. `content/site/{category}/{slug}/img/` に配置

`content/site` は git 追跡対象かつ `public/posts` からシンボリックリンクされているため、ダウンロード完了時点でローカル開発サーバーにそのまま反映される（別途コピー工程は不要）。

### Phase 4: 完了報告

```
[sync-r2-images] ✅ 完了

| 項目 | 値 |
|------|-----|
| ダウンロード | N件 |
| スキップ | N件（既存） |
| 失敗 | 0件 |

次のステップ:
- npm run dev
```

## 注意

- **--dry-run**: 実際のダウンロードを行わない。リスト確認用。
- **既存ファイル**: ファイルサイズが同じ場合はスキップ（重複 DL 防止）
- **ネットワーク**: プロキシ環境では curl の動作に注意（.env.local の設定確認推奨）
- **初期化は不要**: `git pull` で画像は取得されません。R2 にあるファイルのみを取得します。
