---
name: build-settings-validator
description: Xcodeプロジェクトのビルド設定を検証・修正するスキル。推奨設定との比較、問題の検出、修正提案を行う。使用シーン：(1)「ビルド設定を確認して」「プロジェクト設定をチェックして」などの設定検証リクエスト (2)「Swift 6対応の設定になっているか見て」などの特定設定の確認 (3) 新規プロジェクト作成後の設定レビュー (4)「フレームワークの設定が正しいか確認して」などのターゲット別設定確認
---

# Build Settings Validator

Xcodeプロジェクトのビルド設定を推奨設定と比較し、問題を検出・修正する。

## ワークフロー

1. **プロジェクト情報の取得**: `get_project_info`、`list_targets`でプロジェクト構造を把握
2. **ビルド設定の取得**: `get_build_settings`でプロジェクトレベル・ターゲットレベルの設定を取得
3. **推奨設定との比較**: `assets/SampleProject/SampleProject.xcodeproj`の設定と比較
4. **問題の報告**: 推奨と異なる設定、不足している設定を報告
5. **修正の実行**: ユーザー承認後、`update_build_setting`で設定を修正

## 検証項目

### プロジェクトレベル
- 警告設定（CLANG_WARN_*、GCC_WARN_*）
- 言語バージョン（SWIFT_VERSION、CLANG_CXX_LANGUAGE_STANDARD）
- デプロイメントターゲット（IPHONEOS_DEPLOYMENT_TARGET）
- セキュリティ設定（ENABLE_USER_SCRIPT_SANDBOXING）

### アプリターゲット
- Swift Concurrency設定（SWIFT_APPROACHABLE_CONCURRENCY、SWIFT_DEFAULT_ACTOR_ISOLATION）
- Upcoming Feature Flags（SWIFT_UPCOMING_FEATURE_*）
- Asset Catalog設定

### フレームワークターゲット
- BUILD_LIBRARY_FOR_DISTRIBUTION
- Module Verifier設定
- インストールパス設定

## 使用例

```
ユーザー: このプロジェクトのビルド設定を確認して
```

1. pbxproj MCPで`get_project_info`を実行しプロジェクト構造を確認
2. プロジェクトレベルとターゲットレベルの`get_build_settings`を実行
3. `assets/SampleProject/SampleProject.xcodeproj`の設定と比較
4. 差分をリストアップして報告
5. 修正が必要な場合は`update_build_setting`で更新

## リソース

### assets/
- `SampleProject/` - 推奨設定が適用された完全なXcodeプロジェクト
  - アプリターゲット（SampleProject）
  - フレームワークターゲット（SomeLibrary）
  - Unit/UIテストターゲット
  - 具体的な設定値を確認する際はpbxproj MCPで `assets/SampleProject/SampleProject.xcodeproj` を参照
