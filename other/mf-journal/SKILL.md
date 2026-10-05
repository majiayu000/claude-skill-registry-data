---
name: mf-journal
description: MoneyForward クラウド会計の仕訳を取得・表示するスキル。ユーザーが「仕訳を見せて」「仕訳を確認」「今月の仕訳」「売上の仕訳」「経費を確認」などと言ったときに使う。MoneyForward、マネーフォワード、MF会計、仕訳、帳簿、勘定科目に関する質問にはこのスキルを使うこと。
---

# MoneyForward 仕訳取得スキル

MoneyForward クラウド会計 MCPサーバー (`mfc_ca`) を使って仕訳データを取得し、見やすく整形して表示する。

## 前提

- MCP サーバー `mfc_ca` が接続済みであること
- アクセストークンが必要（期限切れの場合は再認証）

## ワークフロー

### 1. 認証確認

まず `mfc_ca_currentOffice` を呼んでアクセストークンが有効か確認する。エラーが返ったら以下の手順で再認証：

1. `mfc_ca_authorize` で認証URLを生成
2. ユーザーにURLをブラウザで開いてもらう
3. 認可コードを受け取り `mfc_ca_exchange` でトークン取得

### 2. 事業者・会計期間の確認

`mfc_ca_currentOffice` で事業者名と会計期間を取得。ユーザーが期間を指定していない場合は、現在の会計期間を使う。

### 3. 仕訳の取得

`mfc_ca_getJournals` で仕訳を取得する。

パラメータ:
- `access_token`: 認証で取得したトークン
- `start_date`: 開始日（YYYY-MM-DD）
- `end_date`: 終了日（YYYY-MM-DD）
- `page`: ページ番号（デフォルト1）
- `per_page`: 1ページあたりの件数（最大100）

ユーザーが「全部」と言った場合は `per_page=100` で取得し、ページネーションで全件取得する。

### 4. 表示形式

取得した仕訳データは以下の形式で表示する。APIのレスポンスで借方のキー名は `debitor`（debtor ではない）なので注意。

```
No.{number} | {transaction_date} | {branches[].remark}
  借方: {debitor.account_name}({debitor.sub_account_name}) {debitor.value:,}円  {debitor.tax_long_name}
  貸方: {creditor.account_name}({creditor.sub_account_name}) {creditor.value:,}円  {creditor.tax_long_name}
```

### レスポンス構造（重要）

仕訳のJSONレスポンスは以下の構造:

```json
{
  "journals": [
    {
      "number": 1,
      "transaction_date": "2026-01-15",
      "memo": "",
      "journal_type": "journal_entry",
      "entered_by": "JOURNAL_TYPE_BILLING",
      "branches": [
        {
          "debitor": {
            "account_name": "普通預金",
            "sub_account_name": "三井住友銀行...",
            "value": 330000,
            "tax_name": "対象外",
            "tax_long_name": "対象外",
            "trade_partner_name": null
          },
          "creditor": {
            "account_name": "売掛金",
            "sub_account_name": null,
            "value": 330000,
            "tax_name": "対象外",
            "tax_long_name": "対象外",
            "trade_partner_name": null
          },
          "remark": "振込 オオイシウンユソウコ"
        }
      ]
    }
  ]
}
```

### 5. 分析・チェック

仕訳を表示した後、以下の観点で簡易チェックを行い、問題があれば指摘する：

- **借方・貸方の金額一致**: 各仕訳の借方合計と貸方合計が一致しているか
- **勘定科目の妥当性**: 摘要内容に対して勘定科目が適切か
- **税区分の妥当性**: 海外サービス（Claude.AI等）は対象外、国内サービスは課税仕入10%が基本
- **日付の整合性**: 取引日と摘要の内容が矛盾していないか

## フィルタリング

ユーザーが特定の条件を指定した場合:

- 「売上の仕訳」→ 売上高の勘定科目IDでフィルタ（`account_id` パラメータ）
- 「1月の仕訳」→ `start_date=2026-01-01`, `end_date=2026-01-31`
- 「今月の仕訳」→ 現在の月の開始日〜本日

勘定科目IDが必要な場合は `mfc_ca_getAccounts` で取得する。
