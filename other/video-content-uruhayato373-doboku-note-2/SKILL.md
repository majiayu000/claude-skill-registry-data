---
name: video-content
description: 動画パック（悩み・出典付き台本・storyboard・CTA）を、重複確認→video-script-writer で生成→機械ゲート→video-content-qa で独立採点→承認待ちで止める薄いオーケストレーター。Use when user asks to [動画パックを作る, 動画台本を作る, 通常動画の企画, パックの台本をQA, /video-content].
allowed-tools: Bash, Read, Task
domain: sns
---

# /video-content（動画パックの入口）

動画パック 1 本の制作を、生成と採点を分離したまま回す入口。**生成・採点・投稿のロジックはここに複製しない**（Generator は `video-script-writer`、Evaluator は `video-content-qa`、機械ゲートは `check-video-content`）。契約は [video-content-policy.md](../../../knowledge/reference/video-content-policy.md) §7、設計は [06_動画コンテンツ運用設計.md](../../../../docs/marketing/06_動画コンテンツ運用設計.md) §4。

## 使い方

```
/video-content <exam> <packId> [悩みの種・元記事]   # 新規パック
/video-content --qa <exam>/<packId>                  # 既存パックの台本を QA にかけるだけ
```

## 手順

1. **入力と既存パックの特定**: `content/sns/video-packs/README.md` と `ls content/sns/video-packs/<exam>/` で同じ悩み・同じ promise の既存パックを探す。重複があれば作らずユーザーへ報告する。`--qa` は対象パックの存在だけ確かめて手順 4 へ
2. **Generator を 1 回呼ぶ**: `video-script-writer` に exam・packId・悩みの種・元記事を渡す
3. **機械ゲート**: `npm run check-video-content`。FAIL は QA に渡さず Generator へ指摘だけを返して手順 2 へ（修正ラウンドは最大 2 回）
4. **Evaluator を独立に呼ぶ**: `video-content-qa` にパックのパスだけを渡す（Generator の自己評価や結論は渡さない）
5. **BLOCK 時**: QA の指摘だけを `video-script-writer` に返す（手順 2〜4 を繰り返す。2 回で解消しなければユーザーへ報告）
6. **PASS 後は承認待ちで停止**: 結果（軸別得点・平均・実行したコマンドと結果）を報告する

## やらないこと

- レンダリング（`render-longform`）、画面確認（`media -- preview`）、R2/Drive 退避、YouTube/IG/X への投稿、公開状態の照合。これらは既存 CLI と workflow が持つ承認ゲート（[content-registry.md](../../../knowledge/reference/content-registry.md) の `registry -- approve` は運営者が自分の端末で実行）を通す
- 承認（`approved`）の自動補完。ユーザー承認なしに外部公開へ進めない
- 資格固有の事実監査の再実装（必要なら専門 Evaluator を別途呼ぶよう報告する）
