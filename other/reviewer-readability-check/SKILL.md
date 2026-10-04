---
name: reviewer-readability-check
version: 1.2.0
description: 章の執筆・改訂完了時・原稿ビルド前に、本文が査読者に読める語彙レベルか（内部記号・時刻・バージョン番号が本文から除去されているか）と節番号の整合（枝番・欠番・重複・ dangling 参照）を check_reviewer_readability.py で検査し、検出項目を「要修正 / 要確認 / 対応不要」の3分類で判断・記録するスキル
---

# 査読者可読性チェックスキル (Reviewer-Readability Check)

## 目的
本文（`docs/<paper-id>/chapters/`）は査読者向けの学術記述レイヤであり、内部記号（`PROP-*`, `SCAF-FAIL`, `RQ-*`, `PH-*`, `NC-xx` 主語使用、研究プログラムの `種①` / `seed 4`）や JST 時刻・バージョン番号の不用意な露出は読解を阻害する。また、執筆過程で挿入された節の枝番（`3.2b` 等）・欠番・重複・実在しない `§` 参照は、編集痕として最終版に残ってはならない。本スキルは `scripts/check_reviewer_readability.py` の出力を既知パターンに照合し、各項目を「要修正 / 要確認 / 対応不要」に分類した判断サマリを著者に提示する。手動通読への依存を排し、可読性確認を工程に組み込むことが狙いである。

## 発動タイミング
- 章ファイルの執筆・改訂を完了した時（ルール: `rules/ja/reviewer-readability-rule.md` により必須）
- `assemble_manuscript.py` が FAIL でビルドを中断した時
- 投稿前ゲートで `reviewer-readability` が WARN/FAIL を返した時

## 原則
- **FAIL は常にブロック**: FAIL を「対応不要」に分類してはならない。prose-gloss（日本語説明＋括弧内 ID）に改めた後、再実行する
- **WARN は意図確認**: 主題言及（バージョン仕様・決定済み時刻等）は「対応不要」も可。ただし著者承認を経て記録する
- **3層レイヤを維持**: 表・ブロッククオート・コードフェンスは参照レイヤとして検査対象外。付録・検証インベントリ（正本）は内部記号のまま保持する

## 処理手順

```text
[Step 1: スクリプト実行] ➔ [Step 2: 既知パターン照合] ➔ [Step 3: 判断サマリ提示] ➔ [Step 4: 著者承認 ➔ ログ記録]
```

### Step 1: スクリプト実行

```bash
# 単一章（章完成時）
python3 scripts/check_reviewer_readability.py docs/<paper-id>/chapters/<file>.md
# 全章（ビルド前・投稿前）
python3 scripts/check_reviewer_readability.py docs/<paper-id>/chapters
```

検出ゼロ（PASS）なら報告して終了。WARN/FAIL があれば Step 2 へ。

### Step 2: 検出項目の既知パターン照合

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| `FAIL/code`（`PROP-*` 等が括弧外） | 要修正 | 日本語説明＋括弧内 ID へ。例: 「AI 提案を採択した（`PROP-ADOPT`）」 |
| `FAIL/nc`（`NC-xx` が括弧外・主語） | 要修正 | 「〇〇という事例（NC-xx）」の形へ。ID を主語にしない |
| `WARN/jst`（本文中の時刻） | 要確認 | 原則として監査索引の表へ集約。著者が明示決定した主題言及のみ対応不要 |
| `WARN/version`（本文中の `v2.x` 等） | 要確認 | プロトコル仕様そのものが主題の箇所（§2.5.2 等）は対応不要。それ以外は「改訂後」等へ |
| `WARN/jargon`（`grounding` 等） | 要確認 | 定義済み用語の括弧内 gloss は対応不要。それ以外は「文献実体化」等へ日本語化 |
| `WARN/program-id`（`種①`、`seed 4` 等） | 要確認 | 研究プログラムの内部番号。原則として読者向けの言い方へ置換。括弧内 gloss は対応不要 |
| `WARN/density`（1行にコード3個以上） | 要確認 | 段落分割または日本語化を検討 |
| `FAIL/secnum-branch`（`3.2b` 等の枝番） | 要修正 | 執筆過程の挿入痕。連番にリナンバリングし、本文中の参照も一括更新する |
| `FAIL/secnum-dup`（節番号の重複） | 要修正 | 見出しを連番に修正する |
| `WARN/secnum-gap`（節番号の欠番） | 要確認 | 意図的な欠番（分割予定等）なら対応不要。それ以外は連番に修正 |
| `WARN/secnum-dangling`（実在しない `§` 参照） | 要確認 | 外部文献の節参照（`§2.1.1` 等の3層番号）は対象外。内部参照の誤りなら修正 |

意図的な例外は、当該行に `<!-- readability:ignore -->` を付し、判断ログに根拠を記録する（乱用禁止）。

### Step 3: 判断サマリ提示

```markdown
## 可読性トリアージ結果 (<paper-id>, YYYY-MM-DD)

- 検査: FAIL=n / WARN=n
- 分類: 要修正 n 件 / 要確認 n 件 / 対応不要 n 件

| 対象 | 検出 | 分類 | 判断根拠 | アクション |
| :--- | :--- | :--- | :--- | :--- |
| ch4 §4.1.2 | WARN/jst 15:32 JST | 対応不要 | 著者が時刻残存を明示承認（設計正本化の対話的起源） | なし |
| ch5 §5.1.3 | FAIL/nc NC-09 主語 | 要修正 | prose-gloss 方針 | 「依存申告（NC-09）は…」へ修正 |
```

### Step 4: 著者承認とログ記録

1. サマリを著者に提示し、分類（特に「対応不要」）の承認を得る
2. 承認後、`docs/<paper-id>/design/logs/reviewer-readability-log.md` に追記する（テンプレートはトリアージサマリと同形式）
3. 「要修正」項目の修正後はスクリプトを再実行し、結果を同ログに追記する

## 関連
- 検出スクリプト: `scripts/check_reviewer_readability.py`
- 強制発動: `assemble_manuscript.py`（FAIL 時はビルド中断、`--force` で回避）、投稿前ゲート `check_pre_submission.py` 第5チェック
- WARN/FAIL 全般のトリアージ: `pre-submission-triage` スキル
- コードの完全な定義: 論文側の付録 A.3（用語集）および検証インベントリ §4.2

## 成果物
- 可読性トリアージ判断サマリ（チャット提示）
- `docs/<paper-id>/design/logs/reviewer-readability-log.md`（判断の監査証跡）
