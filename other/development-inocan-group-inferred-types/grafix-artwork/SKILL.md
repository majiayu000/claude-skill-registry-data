---
name: grafix-artwork
description: Grafix で「作品を 1 本作って PNG 候補を出し、選別→改良」を回すための薄いオーケストレータ。基本は `$grafix-compose` と `$grafix-draw-export`（必要なら `$grafix-api-catalog`）を同時に明示 invoke して使う。
---

# Grafix Artwork（Orchestrator）

## 目的

- 作品制作の会話と手順を固定し、毎回のブレを減らす

## 推奨の呼び出し（ユーザーが貼るテンプレ）

```text
$grafix-api-catalog $grafix-compose $grafix-draw-export $grafix-artwork
モチーフ: 〜（雰囲気、密度、対称/非対称、ノイズ有無）
```

## 会話手順（エージェント向け）

1) まずモチーフだけ聞く（他は既定でよい）

2) 実装 → export まで一気に進める

- `sketch/generated/<slug>.py` に `draw(t)` を作る/更新する
- `python -m grafix export` で `t` を複数指定して候補 PNG を出す（既定: `0 0.25 0.5 0.75 1.0`）
- 生成された PNG のパス一覧を返す

3) 選別 → 改良を回す（人間が選ぶ）

- ユーザーに「残す 1 枚」を決めてもらう（ファイル名 / index / t）
- 改良のたびに `run-id` を進める（`v2`, `v3`…）

## 迷ったとき

- op 選びが詰まったら `$grafix-api-catalog` の `references/api.md` を検索して 3 候補までに絞る
- 作品が散らかったら primitive/effect を 1 個減らす（まず減らす）

