---
name: create-x-card
description: >
  tweets.md から X 投稿用サマリカード PNG（1200×675）を生成する。
  管理分野ハッシュタグを自動検出して色分けし、本文冒頭 4〜8 行を表示。
  Use when user says "X投稿用画像を作って", "サマリカードを生成", "/create-x-card".
disable-model-invocation: true
argument-hint: "--draft <NNN> | --range <NNN>-<NNN> | --all [--force]"
domain: sns
---

POP意匠での新規制作・改修は `/create-pop-image` と [共通方針](../../../knowledge/reference/pop-image-policy.md) を先に参照する。以下のCLIがそのままPOP版を描画するとは扱わない。


`scripts/gen-x-card.mjs` を実行して X 投稿用サマリカード PNG を生成する。

## 人物・見出しと既存投稿の改修

制作・改修の前に [SNS 投稿画像ポリシー §0・§0.1](../../../knowledge/reference/sns-image-policy.md) を読む。先生キャラクター＋短い極太見出しを媒体別に構成し、既存レンダラーの未対応箇所は実装して代表 1 件を画像確認してから展開する。文字を編集可能な元データとして保持する。

再生成は外部の予約・公開投稿を自動更新しない。動画冒頭を改修する未投稿パックはカバーと動画派生物を揃える。公開済みサムネだけの変更は §0.1 に従い、動画本体の更新と区別する。

## 使い方

先生付きカードは [X投稿ポリシー §7](../../../knowledge/reference/x-post-policy.md) の `cards.json` を使う。指定番号だけを生成し、原稿のない番号や長すぎる文は停止する。代表1枚は `--tweet N`、確認画面は `npm run x-review`、実体照合は `npm run check-x-review -- --local`。PNGは再生成物としてGit追跡外に置く。以下の従来レイアウトは `cards.json` がない場合に適用する。

```bash
# 単一ドラフト
node scripts/gen-x-card.mjs --draft 019

# 範囲指定（019〜028 の 50 枚）
node scripts/gen-x-card.mjs --range 019-028

# キーワード解説系すべて（--all は /^\d{3}-キーワード-/ にマッチするもの）
node scripts/gen-x-card.mjs --all

# 既存 PNG を上書き
node scripts/gen-x-card.mjs --draft 019 --force
```

## 出力先

```
content/sns/x/draft/{NNN}-*/img/tweet-NN-{slug}.png
```

slug はドラフトフォルダ名から `NNN-キーワード-` を除いた部分。
同じTweet番号の既存PNGがある場合は、そのファイル名を維持して更新する。これにより `publish-x` が旧画像を先に選ぶ重複生成を防ぐ。

## tweets.md の要件

各ツイートブロックで管理分野ハッシュタグが必要（色分けに使用）:

| ハッシュタグ | 配色 |
|---|---|
| #経済性管理 | brand blue (#2e6da4) |
| #安全管理   | danger red (#b22234) |
| #品質管理   | positive green (#3a7d44) |
| #情報管理   | warn gold (#d4a017) |
| #人的資源管理 | purple (#6b4c9a) |
| (なし)      | brand blue (デフォルト) |

キーワード名はヘッダ行 `【総監キーワード解説】<名前> ?#N` から自動抽出。
`）#N` 形式（スペースなし）も対応（例: `VE（バリューエンジニアリング）#1`）。

### 試験別カード（多資格）

ドラフト slug から試験を自動判定し（`-civil1-`→1級 / `-civil2-`→2級 / それ以外→総監）、色とヘッダを切替（真実源 `.claude/knowledge/reference/x-post-policy.md` §7）：

| 試験 | ヘッダ / 主題抽出パターン | 帯・フッター色 |
|---|---|---|
| 総監 | `【総監キーワード解説】<名前> #N`＋管理分野バッジ | 管理分野別（従来） |
| 1級土木 | `【1級土木 過去問】<主題> #N`＋「1級土木」バッジ | 試験色 青 |
| 2級土木 | `【2級土木 過去問】<主題> #N`＋「2級土木」バッジ | 試験色 緑 |

総監（既定）は従来挙動と完全互換。1級/2級ドラフトは `x-post-writer` が上記ヘッダ形式で生成する。ヘッダ形式がない既存ドラフトはTweet見出しから主題を補完する。

## カードデザイン（1200×675）

```
┌─────────────────────────────────────────────────────┐
│ 総監キーワード解説 #N        │ [管理分野バッジ]     │ ← 管理分野色帯 (80px)
├─────────────────────────────────────────────────────┤
│                                                       │
│  キーワード名（総監44px／1級・2級52px, bold）          │
│  セクションタイトル（28px, muted）                    │
│ ─────────────────────────────────────────────────── │
│  本文（総監27px／1級・2級35px）                        │
│  1級・2級は白い要点パネル内に最大6行で中央配置          │
│                                                       │
├─────────────────────────────────────────────────────┤
│ doboku-note.com                                       │ ← 管理分野色フッター (50px)
└─────────────────────────────────────────────────────┘
```

テキスト折り返しは `sns-image-policy.md §5` の `wrapJa` 算法（lookback 12, maxChars=32, force-break=+4）に準拠。
1級・2級はXのスマートフォン表示を優先し、`maxChars=27`、本文35px、行高49pxとする。短文でも上部に偏らないよう、要点パネル内で縦中央に配置する。

## 生成後の確認

```bash
# 画像を目視確認
open content/sns/x/draft/019-キーワード-risk-assessment/img/tweet-01-risk-assessment.png

# publish-x と統合確認（dry-run）
npx tsx .claude/skills/social/publish-x/publish-x.ts 019 --tweet 1 2026-05-20T08:00 --dry-run
```

## スクリプト本体

`scripts/gen-x-card.mjs`
