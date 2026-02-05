---
name: ios-build-workflow
description: iOS/Swift/Xcodeのビルド・テスト・実行ワークフロー。「iOSビルド」「Xcodeエラー」「コンパイル」「シミュレーター」「swift build」「xcodebuild」などのキーワードで自動適用。
---

# iOS Build Workflow

iOS/Swift/Xcode プロジェクトのビルド・テスト・実行ワークフロー。

## コマンド一覧

| コマンド | 用途 | 実行時間 |
|---------|------|---------|
| `/ios-dev:ios-check` | コンパイルエラーのみ高速チェック | 〜30秒 |
| `/ios-dev:ios-build` | フルビルド（全出力） | 1〜3分 |
| `/ios-dev:ios-run` | シミュレーターで実行 | 1〜3分 |
| `/ios-dev:ios-test` | ユニットテスト実行 | 1〜5分 |
| `/ios-dev:ios-clean` | ビルドキャッシュクリア | 〜10秒 |

## 推奨ワークフロー

```
コード変更 → ios-check（高速確認）
    ↓ エラーなし
ios-build（フルビルド）
    ↓ 成功
ios-run（動作確認）
    ↓ OK
ios-test（テスト実行）
    ↓ 全テストパス
コミット・PR
```

## プロジェクト構成の検出

このプラグインは以下の順序でプロジェクトを検出:

1. **Makefile優先**: `make ios-check` 等のターゲットがあれば使用
2. **xcodeproj検出**: `*.xcodeproj` を探索して xcodebuild を直接実行
3. **SPMプロジェクト**: `Package.swift` があれば `swift build` を使用

## 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `IOS_PROJECT` | .xcodeproj パス | 自動検出 |
| `IOS_SCHEME` | ビルドスキーム | プロジェクト名と同じ |
| `IOS_SIMULATOR` | シミュレーター名 | `iPhone 16 Pro` |
| `IOS_DESTINATION` | xcodebuild destination | 自動生成 |

## よくあるエラーと対処

### シミュレーターが見つからない

```
❌ No booted iPhone simulator found
```

**対処**: シミュレーターを起動
```bash
open -a Simulator
# または
xcrun simctl boot "iPhone 16 Pro"
```

### スキームが見つからない

```
xcodebuild: error: The project '...' does not contain a scheme named '...'
```

**対処**: 利用可能なスキームを確認
```bash
xcodebuild -list -project <project>.xcodeproj
```

### SPM依存関係エラー

```
error: Dependencies could not be resolved
```

**対処**: パッケージキャッシュをクリア
```bash
rm -rf ~/Library/Caches/org.swift.swiftpm
swift package resolve
```

## ios-architecture との連携

このプラグインは `ios-architecture` プラグインと補完関係:

- **ios-architecture**: 設計原則・レイヤー構成の知識
- **ios-dev**: ビルド・テスト・実行のコマンド

両方をインストールすることで、設計に沿った開発とビルドワークフローの両方をサポート。
