---
name: context-review
description: security-scan結果の曖昧な項目をユーザーに質問して確認する対話型レビュー。認証要否・エラー処理・データ露出・ビジネスロジックを選択肢形式で1問ずつ確認し、excluded/confirmed/needs_reviewに分類。「コンテキストレビュー」「context review」「誤検知を確認」「スキャン結果を確認したい」で起動。Do NOT use for 明確な誤検知の自動除外（false-positive-filter agent が担当、ユーザー起動不可）。
allowed-tools: Read, Write, AskUserQuestion
---

# Context Review

security-scan結果の曖昧な項目について、ユーザーに質問して確認する対話型スキル。

## Usage

```bash
/context-review                    # 直近のsecurity-scan結果をレビュー
/context-review ./scan-result.json # 指定ファイルをレビュー
```

## Workflow

```
1. ANALYZE  - security-scan結果を読み込み、曖昧な項目を抽出
2. QUESTION - 選択肢形式で1問ずつ確認
3. RESOLVE  - 回答を反映して判定確定、JSON出力
```

## Question Categories

| Category | Description | 質問例 |
|----------|-------------|--------|
| auth-intent | 認証要否の意図確認 | 「このAPIは認証不要で正しいですか?」 |
| error-handling | 例外処理の妥当性 | 「本番環境でスタックトレースは無効ですか?」 |
| data-exposure | データ露出の意図確認 | 「このレスポンスに機密情報は含まれますか?」 |
| business-logic | ビジネスロジック検証 | 「この計算ロジックは仕様通りですか?」 |

## Resolution Values

| Value | Meaning | 対応 |
|-------|---------|------|
| excluded | 意図的、脆弱性でない | レポートから除外 |
| confirmed | 脆弱性として確定 | レポートに含める |
| needs_review | 判断保留 | 手動レビュー推奨としてマーク |

## Integration

```bash
/security-scan ./src   # 1. スキャン実行
/context-review        # 2. コンテキストレビュー（対話型）
/attack-report         # 3. レポート生成
```

### With false-positive-filter

| スキル | 方式 | 対象 |
|--------|------|------|
| false-positive-filter | パターンマッチ | 明確な誤検知 |
| context-review | ユーザー確認 | 曖昧な項目 |

## Reference

詳細・質問テンプレート・出力JSON形式: [reference.md](reference.md)
