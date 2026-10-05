---
name: record-sales
description: >
  note 販売履歴を SSOT（data/note/sales.json）に記録するスキル。
  ユーザーがダッシュボードからコピーした販売履歴テキストを受け取り、
  sales-recorder エージェントで正規化・追記し、月次集計を表示する。
  Use when user asks to [売上記録, 販売履歴を記録, note 売上, /record-sales].
user-invocable: true
domain: product
---

# /record-sales

note 販売履歴を `data/note/sales.json` に記録し、月次集計を表示する。

## 用途

- note クリエイターダッシュボードからコピーした販売履歴を SSOT に追記
- 重複チェックにより二重記録を防止
- 月次/週次/商品別の集計表示

## 引数

| 引数 | 必須 | 説明 |
|---|---|---|
| `--summary` | No | 追記せず集計のみ表示 |
| `--month YYYY-MM` | No | 指定月の集計を表示（default: 当月） |
| `--validate` | No | productId の不明分をリストアップ（追記しない） |

## 実行手順

### ケース 1: 販売履歴を記録

```
ユーザー: /record-sales
（続けて販売履歴テキストをペースト）
```

1. ユーザーから販売履歴テキストを受け取る
2. 親が直接、正規化して `data/note/sales.json` に追記する（テキスト整形＋JSON 追記は決定的な小作業なので委譲しない。productId の対応表は [sales-tracking.md](../../../knowledge/reference/sales-tracking.md)）
3. 結果（追加件数・スキップ件数・不明 productId）を表示
4. 月次集計テーブルを表示

### ケース 2: 集計のみ表示

```
/record-sales --summary
/record-sales --summary --month 2026-05
```

1. `scripts/sales-summary.mjs` を実行
2. 月次/商品別の集計を表示

### ケース 3: productId 検証

```
/record-sales --validate
```

1. 販売履歴テキストを解析
2. productId が推定できない商品をリストアップ
3. 追記はしない（dry-run）

## 販売履歴テキストの形式

note ダッシュボード → 売上 → 販売履歴 からコピーした形式:

```
2026年

6月

購入日が新しい順

すべて
ゲストユーザー
記事購入
技術士 建設部門｜道路 R8予想 選択科目II-1 模範解答（全4予想設問）
2026年6月17日 05:16
500円

返信する

kuro
記事購入
技術士 建設部門｜土質及び基礎 R07 選択科目II-2 模範解答（II-2-1・II-2-2）
2026年6月17日 00:48
500円

返信する
```

## 出力例

```
## 記録結果

- 追加: 15件
- スキップ（重複）: 3件
- 不明 productId: 1件
  - `article:unknown-20260617-1`: 技術士 建設部門｜新規商品名

## 月次集計（2026-06）

| 商品 | 件数 | 売上 |
|---|---|---|
| essay-complete-pack | 5 | ¥39,900 |
| r8-essay-forecast | 3 | ¥10,440 |
| tankan-reading-guide | 3 | ¥5,940 |
| （単品記事計） | 12 | ¥6,800 |
| **合計** | **23** | **¥63,080** |
```

## SSOT

| ファイル | 役割 |
|---|---|
| `data/note/sales.json` | 販売履歴データ（手動転記） |
| `src/lib/note-magazines.ts` | マガジン ID マスター（価格・URL） |
| `.claude/knowledge/reference/sales-tracking.md` | 運用手順書 |

## トラブルシューティング

### productId が推定できない

1. `--validate` で不明分を確認
2. `sales-recorder.md` の productId 推定ルールに追加
3. または `data/note/sales.json` を直接編集して正しい productId に修正

### 重複が多すぎる

- 同じ期間を複数回ペーストしていないか確認
- 既存データの最終日付を確認: `jq '.sales | last | .date' data/note/sales.json`

### 集計が合わない

- `npm run sales-summary` で検算
- note ダッシュボードの「売上」金額と突合

## 参照

- `.claude/agents/sales-recorder.md` — 正規化・追記を担当するエージェント
- `scripts/sales-summary.mjs` — 集計スクリプト
- `.claude/knowledge/reference/sales-tracking.md` — 運用手順・ポリシー
