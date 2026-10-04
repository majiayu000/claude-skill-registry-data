---
name: pre-submission-triage
version: 1.2.0
description: 投稿前ゲート (check_pre_submission.py) の実行時・WARN/FAIL 出力の解釈が必要な時に、各検出項目を既知パターンに照合して「要修正 / 要確認 / 対応不要」の3分類で判断し、根拠付きの判断サマリを提示・記録するスキル
---

# 投稿前ゲート・トリアージスキル (Pre-Submission Triage)

## 目的
投稿前ゲート `scripts/check_pre_submission.py` は PASS/WARN/FAIL を機械的に出力するが、WARN の解釈（許容できる WARN と放置できない WARN の区別）はスクリプトでは判定できない。本スキルはゲート出力を既知パターンに照合し、各項目を「要修正 / 要確認 / 対応不要」に分類した判断サマリを著者に提示し、承認された判断を根拠付きでログに記録する。WARN 対処の属人化と判断漏れを防ぐことが狙いである。

## 発動タイミング
- 投稿前・原稿ビルド前に `check_pre_submission.py` を実行した時
- ゲート出力の WARN/FAIL の対処方針を著者が確認したい時
- 章完成時・定期品質チェックの結果をレビューする時

## 原則
- **FAIL は常にブロック**: FAIL を「対応不要」に分類してはならない。修正後にゲートを再実行する
- **WARN の「対応不要」には根拠が必須**: 下記の既知パターン表に照合できない WARN は「要確認」に落とす
- **著者承認を経て記録**: 分類結果を提示し、著者の承認後にログへ記録する。エージェント単独で WARN を握り潰してはならない

## 処理手順

```text
[Step 1: ゲート実行] ➔ [Step 2: 既知パターン照合] ➔ [Step 3: 判断サマリ提示] ➔ [Step 4: 著者承認 ➔ ログ記録]
```

### Step 1: ゲート実行

```bash
python3 scripts/check_pre_submission.py <paper-id> --repo-root <論文リポジトリルート>
```

全チェックが PASS かつ WARN なしなら「ゲート通過」を報告して終了する。WARN/FAIL があれば Step 2 へ。

### Step 2: 検出項目の既知パターン照合

各検出項目を以下の分類表に照合する。

#### literature-grounding

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| `no matching literature/papers/*.md artifact` (FAIL) | 要修正 | 引用に対応する実体ファイルが無い。`papers/*.md` を作成する |
| `status=manual-stub` | 対応不要 | 書籍・学位論文等で PDF 自動取得不可の場合の正当な実体化形態（fact-grounding-rule §2-B-3）。**条件**: 当該 `papers/*.md` にページ番号付き抜粋（page-verified excerpts）が記録されていること。抜粋が無ければ要確認 |
| `status=abstract-only` | 要確認 | 本文の主張が abstract の記述範囲に依存しているか目視確認。依存が強い場合は full-text 取得または manual-stub + ページ抜粋へ格上げ |
| `status=full-text but no PDF at _downloads/` | 要修正 | Markdown ノートは転写であり原本ではない。公式 URL 等から PDF を `_downloads/{slug}.pdf` に置き再照合する。再配布権が無い場合は `manual-stub` へ落とす |
| `bot-challenge … human handoff required`（DL スクリプト出力） | 要修正（人間作業） | 自動 DL 不可（reCAPTCHA/Cloudflare）。著者がブラウザで PDF を `_downloads/{slug}.pdf` に配置するまで待つ。エージェントは同一 URL リトライ・非公式ミラー探索をしない（pdf-paper-ingestion Step 1b） |

#### fact-grounding

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| 見出し行・節番号・バージョン番号・発行年のみを含む段落 | 対応不要 | 数値パターンの誤検知 |
| 定性記述中の個数言及（例:「4つのメカニズム」） | 対応不要 | 設計上の定数であり定量主張ではない |
| 統計値・割合・倍率などの定量主張で、Harvard 引用・脚注・`docs/data/` 参照・表参照のいずれも無い | 要修正 | エビデンスアンカーを追記する |

#### output-boundary

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| 内部ワークフロー用語（TDD・テストケース・内部ファイルパス等）の本文漏出 | 要修正 | 公開原稿に内部工程語を残さない。WARN 扱いしない |

#### citation-format

| 出力パターン | 分類 | 判断基準 |
| :--- | :--- | :--- |
| matrix 未登録の本文引用 | 要修正 | `literature-matrix.md` へ登録し `papers/*.md` を実体化する |
| 未定義脚注・孤児文献 | 要修正 | 本文と references の 1対1 整合を回復する |

### Step 3: 判断サマリ提示

以下の形式でチャットに提示する：

```markdown
## トリアージ結果 (<paper-id>, YYYY-MM-DD)

- ゲート総合: PASS=n / WARN=n / FAIL=n
- 分類: 要修正 n 件 / 要確認 n 件 / 対応不要 n 件

| チェック | 対象 | 分類 | 判断根拠 | アクション |
| :--- | :--- | :--- | :--- | :--- |
| literature-grounding | Wood et al. (1976) | 対応不要 | manual-stub + p.90/98 の page-verified 抜粋あり | なし |
| fact-grounding | ch3 §3.2 見出し | 対応不要 | 節番号の誤検知 | なし |
| fact-grounding | ch5 〇〇の段落 | 要修正 | 定量主張にアンカー無し | 引用脚注を追記 |
```

### Step 4: 著者承認とログ記録

1. サマリを著者に提示し、分類（特に「対応不要」「要確認」）の承認を得る
2. 承認後、判断を `docs/<paper-id>/design/logs/pre-submission-triage-log.md` に追記する：

```markdown
## YYYY-MM-DD — pre-submission triage (<paper-id>)

- Gate: PASS=n WARN=n FAIL=n / 分類: 要修正 n, 要確認 n, 対応不要 n

| チェック | 対象 | 分類 | 判断根拠 | アクション |
| :--- | :--- | :--- | :--- | :--- |
```

3. 「要修正」項目の修正完了後はゲートを再実行し、結果を同ログに追記する

## 成果物
- トリアージ判断サマリ（チャット提示）
- `docs/<paper-id>/design/logs/pre-submission-triage-log.md`（判断の監査証跡）
