---
name: deploy
description: >
  develop→mainブランチ経由でCloudflare Pagesにデプロイする。Use when user asks to [デプロイ, 本番反映, /deploy].
domain: ops
---

Cloudflare Pages へデプロイする。

## ブランチ戦略

```
作業ブランチ → develop → main → GitHub Actions → Cloudflare Pages
```

## 前提

- 変更がすべてコミット済みであること

## 手順

### Step 1: 事前チェック

```bash
git branch --show-current
git status
gh secret list | grep -i cloudflare   # token が登録されているか（deploy 500 の主因は期限切れ）
```

- 未コミットの変更がある場合 → ユーザーに確認
- 現在のブランチを記録しておく

### Step 2: develop にマージ

```bash
# develop ブランチに切り替え
git checkout develop

# develop を最新に
git pull origin develop

# 作業ブランチをマージ（fast-forward できない場合はマージコミット）
git merge {作業ブランチ}
```

- コンフリクトが発生した場合 → ユーザーに報告し、解消を支援

### Step 3: ビルド確認

```bash
npm run build
```

ビルドが失敗した場合はユーザーに報告し、続行するか確認する。

### Step 4: develop を push

```bash
git push origin develop
```

### Step 5: main にマージ

```bash
git checkout main
git pull --ff-only origin main
git merge --no-edit develop
```

- コンフリクトが発生した場合 → ユーザーに報告し、解消を支援
- **`--ff-only` は使わない**: main は PR の squash/merge コミットを持つため develop の子孫にならず、
  fast-forward は構造的に失敗する（`fatal: Not possible to fast-forward`）。マージコミットが正。
- **`npm run build` は生成インデックス（`src/config/*.json` の `generated_at` / `dateModified`）を
  書き換える**。これは CI のビルドで再生成されるノイズなので、main へ直接コミットせず破棄してから
  マージする（`git checkout -- src/config/<該当ファイル>`・中身が timestamp 差分だけであることを確認してから）。

### Step 6: main を push（デプロイ開始）

```bash
git push origin main
```

GitHub Actions の `cloudflare-deploy.yml` ワークフローが自動でトリガーされる。

> [!warning] 先頭が `[skip ci]` だとデプロイが起動しない（2026-09-23）
> GitHub は push の**先頭 commit** のメッセージに `[skip ci]` があると、push 起点の
> ワークフローを丸ごと飛ばす。`cloudflare-deploy.yml` も例外ではない。
> ops-write / fetch-metrics / ogp-supply 等の bot が数分おきに `[skip ci]` 付きで
> develop へ台帳を積むので、**develop の先頭をそのまま昇格すると高い確率でこれを踏む**。
> push は成功して見えるので、確認しなければ「デプロイした」と誤報告する。
>
> push 後に必ず run の起動を確かめ、起動していなければ手動で起動する:
>
> ```bash
> gh run list --workflow=cloudflare-deploy.yml --limit 1   # 今 push した SHA の run があるか
> gh workflow run cloudflare-deploy.yml --ref main          # 無ければ手動起動（verify_only 既定 false＝ビルド＋デプロイ）
> ```
>
> 昇格する commit は「最後に CI を通った commit」以降が `[skip ci]` の台帳だけであることを
> `git diff --stat <CI済み SHA> origin/develop` で確かめてから選ぶ（サイト内容が未検証のまま出ないように）。

### Step 7: 元のブランチに戻る

```bash
git checkout {作業ブランチ}
```

### Step 7.5: 本番 SSR 検証

**注意**: 検証は `.pages.dev`（デプロイ直後のビルド成果物）で行う。`doboku-note.com`（Cloudflare 経由の本番ドメイン）でも可だが、Cloudflare のキャッシュ反映ラグや（設定変更時の）Bot 保護の影響を避けるため `.pages.dev` を一次確認に使う。なお 2026-06-12 時点では `doboku-note.com` は `curl` 既定 UA・`facebookexternalhit` 等の bot UA でも 200 を返す（旧記載「bot で必ず 403」は実測と不一致＝Bot Fight Mode は現状緩和。外部 Validator の IP ベース挑戦は別問題で残りうる→ [measurement-incidents.md](../../../../.claude/knowledge/reference/measurement-incidents.md) 2026-04-25）。

```bash
npm run check-production-ssr
```

判定はスクリプトが持つ。**手打ちの curl で代用しない**（下の 2 つの誤読を機械で潰してある）:

- exit 0 … 200 かつ `<main` あり かつ主要キーワードあり
- exit 1 … 実際に壊れている（200 でない / `<main` 0 / キーワード 0）
- exit 2 … **検査不成立＝接続できていない**（HTTP 000 または既知の社内プロキシ・ブロック HTML）。合格でも不合格でもない

> [!warning] `--noproxy` を付けない（2026-08-27 の踏み間違い）
> 会社 PC で `curl --noproxy '*'` を付けるとプロキシを自分で外すことになり、外部へ出られず
> `HTTP 000 / <main 0 件` が返る。これを「デプロイ失敗・SSR 破壊」と報告しかけた。
> **接続できていないことは、サイトが壊れている証拠ではない。**
> スクリプトは `--ssl-no-revoke` 付き curl を使い、000 と社内プロキシが返す「ブロックされました」HTML（503）を exit 2（検査不成立）として区別する。

> [!note] `<main>` で完全一致 grep しない（2026-08-05 是正・スクリプトに内蔵済み）
> 実際の出力は常に class 付き（`<main class="flex-grow">` 等）なので、完全一致は
> **構造的に必ず 0 になる＝偽赤**。開きタグの前方一致で数える。

- 500 の場合 → Cloudflare API token 期限切れを仮説1番に確認（GitHub Secrets で再発行）
- `<main` が 0 → SSR 壊れ。ユーザーに即報告し .claude/todo/backlog.md に起票
- ローカルで exit 2 の場合 → その結果をデプロイの成否の根拠にしない。公開後の `cloudflare-deploy.yml` にある SSR 検査結果を確認する。再検査は `gh workflow run cloudflare-deploy.yml --ref main -f verify_only=true`（再デプロイなし）。外部検査の exit 0 を確認して完了報告する。

### Step 8: 完了報告

以下を報告する:
- マージ・push 結果
- GitHub Actions のワークフロー URL（`gh run list --limit 1` で取得）
- エラーがあった場合はその内容

## 手動デプロイ（CI/CD を使わない場合）

```bash
npm run build
npx wrangler pages deploy out --project-name=doboku-note
```

## エラー時の方針

- ビルド失敗 → ユーザーに確認し、修正 or 中止
- マージコンフリクト → ユーザーに報告し、解消を支援
- push 失敗 → ユーザーに報告
- `--force` は使用しない
