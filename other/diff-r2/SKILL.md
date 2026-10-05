---
name: diff-r2
description: >
  ローカル `content/site/` と Cloudflare R2 バケット `doboku-note`（prefix `posts/`）の
  差分を双方向でレポートする。Use when user asks to [r2の差分, r2とローカルの比較, diff r2, r2 同期確認].
domain: ops
---

ローカルの `content/site/` と R2 バケットの両方を走査し、3種類の差分を検出する:

1. **only-local** — ローカルにあって R2 に無い（未アップロード）
2. **only-remote** — R2 にあってローカルに無い（未同期 or ローカル削除済み）
3. **size-mismatch** — 両方にあるがサイズが異なる（内容が違う）

MDX と画像の両方を対象にする。ETag/MD5 ではなくサイズで比較する（十分高速で実用的）。

## コマンド

```
npm run diff-r2 [-- <options>]
```

### オプション

- `--prefix <path>` — 特定プレフィックスのみ比較（例: `civil-construction-1/primary`）
- `--images-only` — 画像のみ
- `--mdx-only` — MDX のみ
- `--verbose` — 全差分をリスト出力（デフォルトは上位20件）
- `--json` — JSON 出力（CI/他スクリプト連携用）

### 終了コード

- `0` — 完全同期
- `1` — 差分あり
- `2` — 設定エラー（`.env.local` 不足など）

## 実行例

```bash
# 全体比較
npm run diff-r2

# 1級土木の過去問だけ
npm run diff-r2 -- --prefix civil-construction-1/primary

# CI で使う
npm run diff-r2 -- --json > diff.json
```

## 出力イメージ

```
Scanning local: content/site
  1941 files
Listing R2: doboku-note/posts/
  1941 objects

Only local (missing on R2) — run `npm run upload-images-r2` (3):
  civil-construction-1/primary/img/r07-a-fig-01.png  [45.2KB]
  ...

Summary: 3 only-local, 0 only-remote, 0 size-mismatch
⚠️  Diff detected.
```

## 関連スキル

- ローカル → R2 に反映: `npm run upload-images-r2`
- R2 → ローカルに反映: `/sync-r2-images`

## 前提条件

`.env.local` に以下が設定されていること:

- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_R2_ACCESS_KEY_ID`
- `CLOUDFLARE_R2_SECRET_ACCESS_KEY`
