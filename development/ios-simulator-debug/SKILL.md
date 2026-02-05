---
name: ios-simulator-debug
description: |
  iOS SimulatorをAIで操作してデバッグ・検証。ビルド→起動→UI操作→スクショ→分析のループ。
  使用タイミング: (1) UIの動作確認が必要な時、(2) 「Simulatorで確認して」「スクショ撮って」、
  (3) バグの再現・調査時、(4) UI実装の検証時、(5) アクセシビリティの確認時
  前提条件: ios-simulator MCPサーバーが有効化されていること（apple-platform-plugin導入で自動設定）
---

# iOS Simulator Debug スキル

iOS SimulatorをAIで操作し、ビルド→起動→操作→スクショ→分析のデバッグループを実行する。

## 前提条件

### 必須
- macOS
- Xcode（Simulator含む）
- Node.js（npx実行用）
- Facebook IDB: `brew tap facebook/fb && brew install idb-companion`

### MCP設定（自動）
apple-platform-pluginを導入すると、`.mcp.json`により`ios-simulator` MCPサーバーが自動で有効化される。

## ワークフロー

### Step 1: 要件確認

以下をユーザーに確認：
1. **対象アプリ**
   - Xcodeプロジェクト/ワークスペースのパス
   - スキーム名
   - Bundle ID

2. **検証内容**
   - 確認したい画面・機能
   - 再現したいバグの手順
   - 期待する動作

3. **Simulator設定**
   - デバイス（iPhone 15, iPad等）
   - OSバージョン

### Step 2: ビルド＆起動

```bash
# 1. Simulatorを開く（MCPツール使用可能になったら）
# → open_simulator ツールを使用

# 2. アプリをビルド
xcodebuild -workspace App.xcworkspace \
  -scheme App \
  -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -derivedDataPath ./build \
  build

# 3. アプリをインストール
# → install_app ツールで ./build/Build/Products/Debug-iphonesimulator/App.app をインストール

# 4. アプリを起動
# → launch_app ツールで Bundle ID を指定して起動
```

### Step 3: UI操作＆検証ループ

```
現状把握 → 操作 → 結果確認 → 分析 → 次のアクション
    ↑                                      ↓
    └──────────── 繰り返し ←───────────────┘
```

## MCPツール一覧

### Simulator管理

| ツール | 説明 | 使用例 |
|--------|------|--------|
| `open_simulator` | Simulatorアプリを起動 | 最初に実行 |
| `get_booted_sim_id` | 起動中のSimulator IDを取得 | 状態確認 |
| `install_app` | .app/.ipaをインストール | ビルド後 |
| `launch_app` | Bundle IDでアプリ起動 | インストール後 |

### UI検査

| ツール | 説明 | 使用例 |
|--------|------|--------|
| `ui_describe_all` | 画面全体のアクセシビリティ要素を取得 | 現状把握 |
| `ui_describe_point` | 特定座標の要素情報を取得 | 要素特定 |
| `ui_view` | 圧縮スクリーンショット取得 | クイック確認 |
| `screenshot` | フルスクリーンショット保存 | 証跡保存 |

### UI操作

| ツール | 説明 | パラメータ |
|--------|------|-----------|
| `ui_tap` | タップ | x, y座標 |
| `ui_type` | テキスト入力 | 入力文字列 |
| `ui_swipe` | スワイプ | 開始/終了座標、duration |

### 録画

| ツール | 説明 |
|--------|------|
| `record_video` | 動画録画開始（H.264/HEVC） |
| `stop_recording` | 録画停止 |

## デバッグパターン

### パターン1: 画面遷移の確認

```
1. ui_describe_all で現在画面を把握
2. screenshot で初期状態を保存
3. ui_tap でボタンをタップ
4. ui_describe_all で遷移後の画面を確認
5. screenshot で結果を保存
6. 期待と比較して分析
```

### パターン2: 入力フォームのテスト

```
1. ui_describe_all でフォーム要素を特定
2. ui_tap でテキストフィールドをタップ
3. ui_type でテキスト入力
4. ui_tap で送信ボタンをタップ
5. ui_describe_all で結果を確認
```

### パターン3: スクロールコンテンツの確認

```
1. screenshot で現在の表示を保存
2. ui_swipe で下にスクロール
3. screenshot でスクロール後を保存
4. 必要に応じて繰り返し
```

### パターン4: バグ再現の録画

```
1. record_video で録画開始
2. 一連の操作を実行
3. stop_recording で録画停止
4. 動画で再現手順を確認
```

## アクセシビリティ検証

`ui_describe_all` の結果から以下をチェック：

- [ ] すべてのインタラクティブ要素にラベルがある
- [ ] 論理的なフォーカス順序
- [ ] ボタンとリンクの区別が明確
- [ ] 動的コンテンツの通知

## トラブルシューティング

### Simulatorが起動しない
```bash
# Simulatorをリセット
xcrun simctl shutdown all
xcrun simctl erase all
```

### IDBが見つからない
```bash
# IDBをインストール
brew tap facebook/fb
brew install idb-companion

# パスを確認
which idb
```

### アプリがインストールできない
```bash
# 署名を確認
codesign -dv --verbose=4 App.app

# Simulatorに直接インストール
xcrun simctl install booted App.app
```

## 出力ディレクトリ

スクリーンショット・動画のデフォルト保存先: `~/Downloads`

環境変数で変更可能:
```bash
export IOS_SIMULATOR_MCP_DEFAULT_OUTPUT_DIR=/path/to/output
```

## ベストプラクティス

1. **操作前に必ず現状把握**: `ui_describe_all`で画面状態を確認
2. **スクショは証跡として保存**: 問題発見時は`screenshot`で記録
3. **座標はui_describe_allから取得**: ハードコードせず動的に取得
4. **エラー時は画面を確認**: 期待と異なる場合はスクショで状態確認
5. **複雑な操作は録画**: 再現手順を動画で残す
