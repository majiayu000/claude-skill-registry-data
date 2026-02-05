---
name: webapp-debugger
description: |
  Chrome DevTools MCPを使用したWebアプリのデバッグ支援スキル。ブラウザ操作、コンソールログ監視、ネットワークリクエスト分析、パフォーマンス計測を行う。
  使用タイミング: (1) Webアプリの動作確認・デバッグ (2) UIの自動操作テスト (3) ネットワークエラーの調査 (4) コンソールエラーの確認 (5) パフォーマンス問題の診断 (6) フォーム入力の自動化 (7) スクリーンショット取得
---

# Webapp Debugger

Chrome DevTools MCPを使用してWebアプリをデバッグするためのスキル。

## 基本ワークフロー

```
1. ページ準備 → 2. スナップショット取得 → 3. 操作実行 → 4. 結果確認
```

## クイックリファレンス

### ページ操作

```
# ページ一覧取得
list_pages()

# 新規ページ作成
new_page(url: "https://example.com")

# ページ選択
select_page(pageIdx: 0)

# ナビゲーション
navigate_page(type: "url", url: "https://example.com")
navigate_page(type: "reload")
navigate_page(type: "back")
```

### 要素操作（uid必須）

```
# まずスナップショットでuid取得
take_snapshot()

# クリック
click(uid: "button-submit")

# テキスト入力
fill(uid: "input-email", value: "user@example.com")

# 複数フォーム一括入力
fill_form(elements: [
  {uid: "input-name", value: "山田太郎"},
  {uid: "input-email", value: "taro@example.com"}
])

# キー入力
press_key(key: "Enter")
press_key(key: "Control+A")
```

### デバッグ情報取得

```
# コンソールログ確認
list_console_messages()
list_console_messages(types: ["error", "warn"])

# ネットワークリクエスト確認
list_network_requests()
list_network_requests(resourceTypes: ["xhr", "fetch"])
get_network_request(reqid: 123)

# スクリーンショット
take_screenshot()
take_screenshot(fullPage: true)
```

### パフォーマンス分析

```
# トレース開始（ページリロード付き）
performance_start_trace(reload: true, autoStop: true)

# 手動停止
performance_stop_trace()

# インサイト分析
performance_analyze_insight(insightSetId: "...", insightName: "LCPBreakdown")
```

## 活用シナリオ

| シナリオ | プロンプト例 |
|---------|-------------|
| **コード変更の検証** | "localhost:3000の変更を確認して" |
| **エラー診断** | "ログインフォーム送信時のエラーを分析" |
| **E2Eテスト** | "サインアップ→入力→送信を試して失敗理由を教えて" |
| **レイアウト修正** | "ヘッダーのオーバーフロー要素を修正して" |
| **パフォーマンス監査** | "このページのLCPをチェックして" |

詳細な活用例: [references/use-cases.md](references/use-cases.md)

## デバッグシナリオ別ガイド

詳細な手順は以下を参照:

- **UIデバッグ**: [references/ui-debugging.md](references/ui-debugging.md)
- **ネットワークデバッグ**: [references/network-debugging.md](references/network-debugging.md)
- **パフォーマンス分析**: [references/performance-analysis.md](references/performance-analysis.md)
- **活用シナリオ集**: [references/use-cases.md](references/use-cases.md)

## 重要なポイント

1. **uid取得が必須**: 要素操作前に必ず`take_snapshot()`を実行
2. **スナップショット優先**: スクリーンショットより`take_snapshot()`を使用（軽量・uid取得可能）
3. **待機の活用**: 非同期操作後は`wait_for(text: "期待するテキスト")`で待機
4. **エラー確認**: 操作後は`list_console_messages(types: ["error"])`でエラーチェック

## トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| uidが見つからない | `take_snapshot(verbose: true)`で詳細情報取得 |
| 要素が操作できない | `wait_for()`で要素の出現を待機 |
| ダイアログが出る | `handle_dialog(action: "accept")`で処理 |
| ネットワークエラー | `list_network_requests()`でステータス確認 |
