---
name: terminology-consistency
version: 1.0.0
description: 章の執筆・改訂完了時・原稿ビルド前に、用語の表記揺れ（登録済みバリアントの再出現）と用語集英語語の未 gloss 出現を check_terminology_consistency.py で機械検査し、あわせて LLM の意味理解による同義的ゆらぎレビューを行い、発見を variants.yml に蓄積するスキル
---

# 用語一貫性スキル (Terminology Consistency)

## 目的
本文（`docs/<paper-id>/chapters/`）の用語揺れは査読者の読解を阻害し、主張の厳密さを損なう。本スキルは次の**三層**で揺れに対処する。

1. **機械層（再発防止）**: `scripts/check_terminology_consistency.py` が登録済みバリアント（FAIL）と用語集英語語の未 gloss 出現（WARN）を検出する。用語集（`literature/bilingual-glossary.md` 正本）をそのまま辞書として使い、二重管理しない
2. **LLM 層（意味的発見）**: 表層の異なる同義的ゆらぎ（例: 「主張トーン」と「主張の強度」）は機械では検出できない。エージェントが章を通読し、意味的に同一概念を指す候補語群をクラスタリングして著者に提示する
3. **蓄積層（学習）**: 著者が「揺れ」と判定した語は `design/sot/terminology-variants.yml` に追記する。以降は機械層が FAIL で再発を防止する。人の発見を一度きりで終わらせない

## 発動タイミング
- 章ファイルの執筆・改訂を完了した時（機械層は必須）
- `assemble_manuscript.py` が FAIL でビルドを中断した時
- 投稿前ゲートで `terminology-consistency` が WARN/FAIL を返した時
- 著者が用語の揺れを指摘した時（LLM 層レビュー＋蓄積）

## 原則
- **FAIL（バリアント再出現）は常にブロック**: 正準形は著者が確定済み。「対応不要」には分類しない
- **WARN（未 gloss 英語）は意図確認**: 定義文・固有名詞・参考文献タイトルは対応不要も可。著者承認を経て記録する
- **機械の限界を認める**: 未知の同義語は機械に求めない。LLM 層で発見し、蓄積層で機械に還元する
- **正本の単一性**: 用語の追加・変更はまず用語集（`bilingual-glossary.md`）を更新し、付録 A は再生成または同期する

## 処理手順

```text
[Step 1: 機械スキャン] ➔ [Step 2: 既知パターン照合] ➔ [Step 3: LLM 意味レビュー] ➔ [Step 4: 著者判定 ➔ variants.yml 蓄積]
```

### Step 1: 機械スキャン

```bash
# 単一章（章完成時）
python3 scripts/check_terminology_consistency.py docs/<paper-id>/chapters/<file>.md
# 全章（ビルド前・投稿前）
python3 scripts/check_terminology_consistency.py docs/<paper-id>/chapters
```

検出ゼロ（PASS）でも Step 3 の意味レビューは別途実施してよい（機械は未知の揺れを拾わないため）。

### Step 2: 検出項目の既知パターン照合

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| `FAIL/variant`（登録バリアントの再出現） | 要修正 | hint の正準形に統一。例外は認めない |
| `WARN/gloss`（用語集英語語が裸で出現） | 要確認 | 「日本語（English）」形式に直すか、定義文・定着略語なら allowlist 登録 |
| 参考文献節・表・コードフェンス内 | 対象外 | スクリプトが自動除外（参考文献タイトルは逐語引用） |

意図的な例外は、当該行に `<!-- terminology:ignore -->` を付し、判断ログに根拠を記録する（乱用禁止）。

### Step 3: LLM 意味レビュー（機械では拾えない揺れ）

1. 用語集の日本語列を読み、各用語について本文中の「表層が違うが同じ概念を指す候補」を探索する（例: 正準形「主張の強度」に対し「主張トーン」「断定の度合い表現」等）
2. 候補をクラスタリングし、出現箇所（ファイル・行）つきで著者に提示する
3. 同義か別概念かの最終判定は**著者**が行う（例: 「適正オフローディング」は「認知オフローディング」の揺れではなく別の造語）

### Step 4: 著者判定と variants.yml への蓄積

1. 著者が「揺れ」と判定した語を `docs/<paper-id>/design/sot/terminology-variants.yml` に追記する

```yaml
variants:
  - canonical: 主張の強度
    variants:
      - 主張トーン
    note: 2026-08-17 著者指摘。Modality の日本語 gloss を統一
```

2. 本文の当該箇所を正準形に修正し、スクリプトを再実行して FAIL=0 を確認する
3. 判断サマリを `docs/<paper-id>/design/logs/terminology-consistency-log.md` に追記する（日付・検出・分類・根拠・アクション）

## 関連
- 検出スクリプト: `scripts/check_terminology_consistency.py`
- 強制発動: `assemble_manuscript.py`（FAIL 時はビルド中断、`--force` で回避）、投稿前ゲート `check_pre_submission.py` 第6チェック
- 内部記号の露出検査: `reviewer-readability-check` スキル（語彙ポリシーは同じ3層）
- WARN/FAIL 全般のトリアージ: `pre-submission-triage` スキル

## 成果物
- 用語トリアージ判断サマリ（チャット提示）
- `docs/<paper-id>/design/sot/terminology-variants.yml`（揺れの蓄積・正本）
- `docs/<paper-id>/design/logs/terminology-consistency-log.md`（判断の監査証跡）
