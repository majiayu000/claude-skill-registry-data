---
name: issue-create
description: GitHub Issue を作成する手順。依頼を受けたとき、.github/ISSUE_TEMPLATE の内容に応じてテンプレを選び、必須項目を埋めて GitHub MCP（issue_write/create）で Issue を作成する。
---

# トリガー
- ユーザーから Issue 作成を依頼されたとき。

# テンプレ選択方針
- `.github/ISSUE_TEMPLATE/bug_report.yml` : バグ報告や不具合再現時。デフォルトタイトル `[Bug] ...`、デフォルトラベル `type:bug`。
- `.github/ISSUE_TEMPLATE/feature_request.yml` : 機能追加・改善要望時。デフォルトタイトル `[Feature] ...`、デフォルトラベル `type:enhancement`。
- どちらにも当てはまらない場合は近い方を選び、本文で趣旨を明記し、必要ならラベルを調整する。

# 手順
1. テンプレを確認する  
   - 対応する `.github/ISSUE_TEMPLATE/*.yml` を開き、必須項目（チェックボックスや required=true のフィールド）とプレースホルダを把握する。
2. タイトル・本文を下書きする  
   - タイトルはテンプレの prefix に合わせる（`[Bug] ...` / `[Feature] ...` など）。  
   - 必須項目をすべて埋め、プレースホルダ（`<...>` や `#<番号>` 等）は必ず実値に置換する。YAML内の項目名を見出しとして本文に記載すると漏れ防止になる。
3. ラベル/プロジェクト/アサイン  
   - デフォルトラベル: bug_report は `type:bug`、feature_request は `type:enhancement`。追加ラベルやアサインは依頼内容に応じて設定。
4. 一時ファイルに保存  
   - `/tmp/issue_body.md` 等に本文を保存し、後で文字列として渡す。
5. Issue 作成（GitHub MCP）  
   - GitHub MCP の `issue_write` を `method: create` で呼び出し、`owner`・`repo`・`title`・`body`・`labels`（テンプレ既定ラベルを含める）を渡す。  
   - タイトルは前述の形式、本文は `/tmp/issue_body.md` の内容文字列を使用する。
6. 失敗時の再実行ワンライナー  
   - 例: `gh issue create --title "<title>" --body-file /tmp/issue_body.md --label type:bug`
7. 完了確認  
   - 作成された Issue URL を共有し、必要なら ToDo や関連ドキュメントへ記録する。

# チェックリスト
- [ ] 正しいテンプレを選んだか（バグ/機能）
- [ ] テンプレの必須項目をすべて埋めたか
- [ ] プレースホルダを実値に置換したか
- [ ] テンプレ既定ラベル（type:bug / type:enhancement）を含めて設定したか
- [ ] `/tmp/issue_body.md` などに本文を書き出したか
- [ ] MCP `issue_write` (method=create) に owner/repo/title/body/labels を正しく渡したか
- [ ] 失敗時の再実行ワンライナーを提示したか
