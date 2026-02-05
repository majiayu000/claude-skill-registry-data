---
name: agent-browser-knowledge
description: agent-browser CLI の仕様と使い方に関する知識を提供。ヘッドレスブラウザ自動化、スナップショット、セレクター、セッション管理、ネットワーク制御について回答。Use when user asks about agent-browser, browser automation, snapshots, selectors, sessions, or web scraping. Also use when user says agent-browser について, ブラウザ自動化, スナップショット, セレクター, セッション管理.
context: fork
---

# agent-browser CLI 完全リファレンス

agent-browser は AI エージェント向けのヘッドレスブラウザ自動化 CLI。Rust で実装された高速な実行エンジンと Node.js フォールバックを備えている。

## インストール

```bash
# npm でグローバルインストール
npm install -g agent-browser
agent-browser install  # Chromium をダウンロード

# Linux の場合（システム依存関係を含む）
agent-browser install --with-deps

# ソースからビルド
git clone https://github.com/vercel-labs/agent-browser
cd agent-browser
pnpm install && pnpm build
pnpm build:native  # Rust が必要
pnpm link --global
```

## 基本ワークフロー

AI エージェントでの典型的な使用フロー:

```bash
# 1. ページを開く
agent-browser open https://example.com

# 2. スナップショットを取得（インタラクティブ要素のみ）
agent-browser snapshot -i

# 3. 要素と対話（ref を使用）
agent-browser click @e2
agent-browser fill @e3 "test@example.com"

# 4. スクリーンショット取得
agent-browser screenshot page.png

# 5. ブラウザを閉じる
agent-browser close
```

## セレクターの種類

### 1. Refs（AI 推奨）

スナップショットで取得した参照を使用:

```bash
agent-browser snapshot -i
# 出力例: @e1 button "Submit", @e2 input[type=email], @e3 a "Login"

agent-browser click @e1      # @e1 をクリック
agent-browser fill @e2 "text" # @e2 にテキスト入力
```

### 2. CSS セレクター

```bash
agent-browser click "#submit-button"
agent-browser fill ".email-input" "user@example.com"
agent-browser click "button[data-testid='login']"
```

### 3. セマンティックロケーター

```bash
# ARIA ロールで検索
agent-browser find role button click --name "Submit"
agent-browser find role textbox fill "Hello"

# ラベルで検索
agent-browser find label "Email" fill "test@test.com"
agent-browser find label "Password" fill "secret123"

# テキストで検索
agent-browser find text "Sign In" click
agent-browser find text "Continue" click

# プレースホルダーで検索
agent-browser find placeholder "Enter email" fill "user@example.com"

# alt テキストで検索
agent-browser find alt "Logo" click

# data-testid で検索
agent-browser find testid "submit-btn" click
```

## コマンドリファレンス

### ナビゲーション

```bash
agent-browser open <url>           # URL を開く
agent-browser open <url> --wait networkidle  # ロード完了まで待機
agent-browser back                 # 戻る
agent-browser forward              # 進む
agent-browser reload               # リロード
agent-browser close                # ブラウザを閉じる
```

### スナップショット

```bash
agent-browser snapshot             # 完全なアクセシビリティツリー
agent-browser snapshot -i          # インタラクティブ要素のみ（推奨）
agent-browser snapshot -c          # コンパクト表示（空要素を除去）
agent-browser snapshot -d 3        # 深さを 3 レベルに制限
agent-browser snapshot -s "#main"  # 特定セレクターにスコープ
agent-browser snapshot -i -c -d 5  # オプション組み合わせ
```

### クリック操作

```bash
agent-browser click <selector>           # 左クリック
agent-browser click <selector> --dbl     # ダブルクリック
agent-browser click <selector> --right   # 右クリック
agent-browser click <selector> --force   # 強制クリック（非表示でも）
```

### テキスト入力

```bash
agent-browser fill <selector> "text"     # フィールドをクリアして入力
agent-browser type <selector> "text"     # 既存テキストに追加入力
agent-browser clear <selector>           # フィールドをクリア
```

### キーボード操作

```bash
agent-browser press Enter
agent-browser press Tab
agent-browser press Escape
agent-browser press "Control+a"         # 全選択
agent-browser press "Control+c"         # コピー
agent-browser press "Control+v"         # ペースト
agent-browser press "Shift+Tab"         # 逆タブ
```

### フォーム操作

```bash
# チェックボックス
agent-browser check <selector>          # チェック
agent-browser uncheck <selector>        # チェック解除

# ドロップダウン
agent-browser select <selector> "value" # 値で選択
agent-browser select <selector> --label "表示テキスト"

# ファイルアップロード
agent-browser upload <selector> /path/to/file.pdf
agent-browser upload <selector> file1.jpg file2.jpg  # 複数ファイル
```

### マウス操作

```bash
agent-browser hover <selector>                    # ホバー
agent-browser drag <src-selector> <tgt-selector>  # ドラッグ＆ドロップ
agent-browser mouse move 100 200                  # 座標移動
agent-browser mouse click                         # 現在位置でクリック
agent-browser mouse down                          # ボタン押下
agent-browser mouse up                            # ボタン解放
```

### スクロール

```bash
agent-browser scroll down                # 下にスクロール
agent-browser scroll up                  # 上にスクロール
agent-browser scroll <selector>          # 要素が見えるまでスクロール
agent-browser scroll --to-bottom         # 最下部まで
agent-browser scroll --to-top            # 最上部まで
```

### 待機

```bash
agent-browser wait <selector>            # 要素が表示されるまで
agent-browser wait 2000                  # 2000ms 待機
agent-browser wait --load networkidle    # ネットワークアイドルまで
agent-browser wait --load load           # ロード完了まで
agent-browser wait --load domcontentloaded
agent-browser wait --text "Success"      # テキストが表示されるまで
agent-browser wait --url "**/success"    # URL パターンにマッチするまで
```

### 情報取得

```bash
# テキスト・HTML
agent-browser get text <selector>        # テキスト内容
agent-browser get html <selector>        # 内部 HTML
agent-browser get outer-html <selector>  # 外部 HTML

# フォーム値
agent-browser get value <selector>       # 入力値

# 属性
agent-browser get attr <selector> href   # 属性値
agent-browser get attr <selector> data-id

# ページ情報
agent-browser get title                  # ページタイトル
agent-browser get url                    # 現在の URL

# 要素情報
agent-browser get count <selector>       # マッチ数
agent-browser get bbox <selector>        # バウンディングボックス
```

### 状態確認

```bash
agent-browser is visible <selector>      # 表示されているか
agent-browser is enabled <selector>      # 有効か（disabled でないか）
agent-browser is checked <selector>      # チェックされているか
```

### スクリーンショット・PDF

```bash
agent-browser screenshot                 # page.png に保存
agent-browser screenshot output.png      # 指定ファイル名
agent-browser screenshot --full          # フルページ
agent-browser screenshot <selector>      # 要素のみ

agent-browser pdf output.pdf             # PDF として保存
agent-browser pdf output.pdf --format A4
```

### タブ管理

```bash
agent-browser tab                        # タブ一覧
agent-browser tab new                    # 新規タブ
agent-browser tab new https://example.com
agent-browser tab 2                      # タブ 2 に切り替え
agent-browser tab close                  # 現在のタブを閉じる
agent-browser tab close 3                # タブ 3 を閉じる
```

### ウィンドウ管理

```bash
agent-browser window                     # ウィンドウ情報
agent-browser window new                 # 新規ウィンドウ
agent-browser window size 1920 1080      # サイズ変更
```

### iframe 操作

```bash
agent-browser frame <selector>           # iframe に切り替え
agent-browser frame --main               # メインフレームに戻る
agent-browser frame --list               # フレーム一覧
```

### ダイアログ処理

```bash
agent-browser dialog accept              # OK/承諾
agent-browser dialog dismiss             # キャンセル/却下
agent-browser dialog accept "入力テキスト"  # prompt への入力
```

### Cookie 管理

```bash
agent-browser cookies                    # 全 Cookie 取得
agent-browser cookies get <name>         # 特定 Cookie 取得
agent-browser cookies set <name> <value> # Cookie 設定
agent-browser cookies delete <name>      # Cookie 削除
agent-browser cookies clear              # 全 Cookie クリア
```

### ストレージ管理

```bash
# localStorage
agent-browser storage local              # 全データ取得
agent-browser storage local get <key>    # 特定キー取得
agent-browser storage local set <key> <value>
agent-browser storage local delete <key>
agent-browser storage local clear

# sessionStorage
agent-browser storage session            # 全データ取得
agent-browser storage session get <key>
agent-browser storage session set <key> <value>
```

### ネットワーク制御

```bash
# リクエスト監視
agent-browser network requests           # リクエスト一覧
agent-browser network route "**/*.js"    # パターンにマッチするリクエストを監視

# リクエストブロック
agent-browser network route "**/*.css" --abort
agent-browser network route "**/analytics*" --abort

# レスポンスモック
agent-browser network route "**/api/user" --fulfill '{"name":"test"}'
```

### ブラウザ設定

```bash
# ビューポート
agent-browser set viewport 1920 1080
agent-browser set viewport 375 667       # モバイルサイズ

# デバイスエミュレーション
agent-browser set device "iPhone 14"
agent-browser set device "Pixel 7"

# ジオロケーション
agent-browser set geo 35.6762 139.6503   # 東京

# オフラインモード
agent-browser set offline on
agent-browser set offline off

# カラースキーム
agent-browser set media dark             # ダークモード
agent-browser set media light            # ライトモード
```

### JavaScript 実行

```bash
agent-browser eval "document.title"
agent-browser eval "window.scrollY"
agent-browser eval "localStorage.getItem('token')"
agent-browser eval <selector> "el => el.innerText"
```

### コンソール・エラー

```bash
agent-browser console                    # コンソールメッセージ
agent-browser errors                     # エラー一覧
```

### トレース記録

```bash
agent-browser trace start                # 記録開始
agent-browser trace stop                 # 記録停止・保存
agent-browser trace stop output.zip      # 指定ファイルに保存
```

## セッション管理

独立したブラウザインスタンスを複数実行:

```bash
# セッションを指定してコマンド実行
agent-browser --session agent1 open https://site-a.com
agent-browser --session agent2 open https://site-b.com

# 環境変数でも指定可能
AGENT_BROWSER_SESSION=agent1 agent-browser snapshot

# セッション管理
agent-browser session list               # アクティブセッション一覧
agent-browser session close agent1       # セッションを閉じる
```

各セッションは独自の Cookie、ストレージ、認証状態を持つ。

## AI エージェント統合のベストプラクティス

### 1. スナップショットファースト

必ずスナップショットで要素を確認してから操作:

```bash
agent-browser open https://example.com
agent-browser snapshot -i  # まずインタラクティブ要素を取得
# 出力を確認して適切な ref を選択
agent-browser click @e5
```

### 2. 待機を適切に使用

ページ遷移後は必ず待機:

```bash
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i
```

### 3. エラーハンドリング

要素が見つからない場合の対処:

```bash
# 要素の存在確認
agent-browser is visible "#submit"

# タイムアウト付き待機
agent-browser wait "#success-message" --timeout 10000
```

### 4. フォーム入力パターン

```bash
agent-browser open https://example.com/login
agent-browser snapshot -i

# フォームに入力
agent-browser fill @e2 "user@example.com"
agent-browser fill @e3 "password123"
agent-browser click @e4

# 結果を待機
agent-browser wait --load networkidle
agent-browser wait --url "**/dashboard"
```

### 5. スクレイピングパターン

```bash
agent-browser open https://example.com/list
agent-browser wait --load networkidle
agent-browser snapshot -c  # コンパクトモードで取得

# 複数要素のテキスト取得
agent-browser get text ".item-title"
agent-browser get count ".item"

# ページネーション
agent-browser click ".next-page"
agent-browser wait --load networkidle
```

## トラブルシューティング

### ブラウザが起動しない

```bash
# Chromium を再インストール
agent-browser install

# デーモンを再起動
agent-browser daemon restart
```

### 要素が見つからない

```bash
# スコープを広げてスナップショット
agent-browser snapshot  # -i なしで全要素

# 待機を追加
agent-browser wait <selector>
agent-browser snapshot -i
```

### タイムアウト

```bash
# タイムアウト時間を延長
agent-browser wait <selector> --timeout 30000
agent-browser open <url> --timeout 60000
```

## 参考リンク

- GitHub: https://github.com/vercel-labs/agent-browser
- 公式サイト: https://agent-browser.dev
