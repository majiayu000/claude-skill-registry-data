---
name: mf-invoice-check
description: MoneyForward の仕訳と受領請求書PDF (references/invoices/) を突合するスキル。課税仕入の仕訳に請求書PDFが登録されているか、matches.json の参照先ファイルが実在するか、既知の海外サービス（Cloudflare/SQLBAK/Anthropic/Google Cloud等）の税区分が正しいかをチェックする。「請求書チェック」「請求書突合」「仕訳と請求書の突合」「請求書PDF未登録」「税区分チェック」などのフレーズで起動。
---

# MoneyForward 請求書突合チェック

MoneyForward クラウド会計の仕訳データと、`references/invoices/` に保存済みの受領請求書
PDF（`matches.json` で仕訳No.に紐づけ済み）を突合し、記帳漏れ・添付漏れ・税区分誤りを
検出する。

ロジックは `app/app/composables/useReconcile.ts` の `hasTaxableCategory` /
`reconcileManual` と同じ仕様（課税仕入の仕訳＝要請求書、matches.json ベースの突合）。
app 側 (Nuxt UI) のロジックを変更した場合は、`scripts/check_invoices.py` 側も追従させる
こと（重複防止のため、app を既に開いている場合はそちらの「突合」画面を見る方が早い。
本スキルは chat から素早く確認したい時 / app を起動していない時に使う）。

## 前提

- `references/invoices/matches.json`（年度別、仕訳No→相対パス）が最新化されていること
- 仕訳データは MCP (`mfc_ca_getJournals`) からその場で取得するか、`mf-backup` で取った
  最新バックアップ (`backups/<timestamp>/journals.json`) を使う

## 手順

### Step 1: 認証確認・会計期間の確認

`mfc_ca_currentOffice` を呼び、アクセストークンの有効性と会計期間を確認する。
エラーなら `mf-journal` skill の再認証手順（`mfc_ca_authorize` → `mfc_ca_exchange`）に従う。

### Step 2: 仕訳を取得

`mfc_ca_getJournals` で対象期間の仕訳を全件取得する（`per_page=100` でページネーション、
漏れなく取得）。

### Step 3: 取得結果を一時ファイルに保存

取得した仕訳データ（`{ "journals": [...] }` 形式）を、Write ツールで一時ファイルに
保存する。例: `c:/moneyforward/audit-logs/tmp_journals_check.json`

### Step 4: 突合スクリプトを実行

```bash
python c:/moneyforward/.claude/skills/mf-invoice-check/scripts/check_invoices.py c:/moneyforward/audit-logs/tmp_journals_check.json --year 2026
```

引数を省略した場合は `backups/` 配下の最新バックアップを自動で使う（`mf-backup` を
先に実行済みの場合はこちらで十分）。

### Step 5: 結果をそのまま報告

スクリプトの標準出力（Markdown）をそのままユーザーに提示する。以下の3カテゴリで
レポートされる:

- **請求書PDF未登録** — 課税仕入の仕訳だが `matches.json` に対応エントリが無い
- **請求書PDFファイル欠落** — `matches.json` にエントリはあるが、参照先ファイルが
  `references/invoices/` に存在しない（ファイル移動・削除・矢印以内で相対パスがずれた
  可能性）
- **既知海外サービスの税区分不一致** — Cloudflare / SQLBAK (Pranas.NET) / Anthropic
  (Claude.AI) / Google Cloud の税区分が、claude.md の「海外サービスの税区分ルール」表
  と食い違っている仕訳

該当が1件もなければ「課税仕入の仕訳はすべて請求書PDFと突合済みで、既知海外サービスの
税区分も問題ありません」とだけ報告する。

## 注意

- **`needs_document`（課税仕入かどうか）の判定は、借方・貸方いずれかの `tax_long_name`
  に「課税仕入」を含むかどうかで行う**（`useReconcile.ts` の `hasTaxableCategory` と同一
  ロジック）。課税売上（自社発行請求書側）は対象外
- Anthropic (Claude.AI) は 2026-04-01 を境に税区分が「対象外」→「課税仕入10%」に切り替
  わる（claude.md参照）。日付をまたぐ仕訳の判定に注意
- **一時ファイル (`tmp_journals_check.json`) は仕訳・財務データを含むため、コミットしない**
  （`audit-logs/` は既に `.gitignore` 済み）
- `matches.json` / `references/invoices/` はどちらも `.gitignore` 済みのローカルデータ
  （rclone で Google Drive に同期）。git 管理下には無いことを前提にする
- スクリプトは matches.json のパス解決時、`references/invoices/<year>/<filename>` と
  二重ネスト `references/invoices/<year>/<year>/<filename>` の両方を探す
  （`index-invoices.sh` の挙動に合わせている）
