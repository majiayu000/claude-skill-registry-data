---
name: firebase-emulator-workflow
description: Firebase Emulator Suiteの起動・停止・管理ワークフロー。「エミュレーター」「Firebase」「Firestore」「Auth」「ローカル開発」などのキーワードで自動適用。
---

# Firebase Emulator Workflow

Firebase Emulator Suite のローカル開発環境管理ワークフロー。

## コマンド一覧

| コマンド | 用途 |
|---------|------|
| `/firebase-emulator:emulator-start` | エミュレーター起動（バックグラウンド） |
| `/firebase-emulator:emulator-stop` | エミュレーター停止 |
| `/firebase-emulator:emulator-status` | 状態確認 |

## 推奨ワークフロー

```
開発開始 → emulator-start（バックグラウンド起動）
    ↓
iOS/Backend 開発
    ↓
開発終了 → emulator-stop（リソース解放）
```

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `FIREBASE_PROJECT_ID` | プロジェクトID | 自動検出 |
| `EMULATOR_PORT_FIRESTORE` | Firestore ポート | 8090 |
| `EMULATOR_PORT_AUTH` | Auth ポート | 9099 |
| `EMULATOR_PORT_STORAGE` | Storage ポート | 9199 |
| `EMULATOR_PORT_UI` | UI ポート | 4000 |

## ディレクトリ検出

以下の順序で Firebase 設定を検出:

1. 環境変数 `FIREBASE_DIR`
2. カレントディレクトリの `firebase.json`
3. `firebase/` サブディレクトリ

## Emulator UI

起動後、ブラウザで確認:

```
http://localhost:4000
```

## アプリからの接続

### iOS (Swift)

```swift
let settings = Firestore.firestore().settings
settings.host = "localhost:8090"
settings.isSSLEnabled = false
Firestore.firestore().settings = settings
```

### Go Backend

```go
os.Setenv("FIRESTORE_EMULATOR_HOST", "localhost:8090")
os.Setenv("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")
```

## よくある問題

### ポートが既に使用中

```
Port 8090 is already in use
```

**対処**: 既存のプロセスを終了
```bash
lsof -ti :8090 | xargs kill -9
```

### firebase.json が見つからない

```
Error: No Firebase project directory found
```

**対処**: `firebase init` でプロジェクトを初期化
