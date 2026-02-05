---
name: ios-project-setup
description: 新規iOSプロジェクト作成時の初期設定、フォルダ構成、Xcode設定、依存関係管理、ビルド設定の最適化、チーム開発環境構築まで、プロジェクト開始時の全てをカバー。
---

# iOS Project Setup Skill

## 📋 目次

1. [概要](#概要)
2. [いつ使うか](#いつ使うか)
3. [完全ガイド](#完全ガイド)
4. [テンプレート & スクリプト](#テンプレートスクリプト)
5. [クイックスタート](#クイックスタート)
6. [関連Skills](#関連skills)

---

## 概要

iOS プロジェクトの初期設定に関する包括的なガイド。プロジェクト作成から本番リリースまでの全プロセスをカバーします。

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: Xcodeプロジェクト設定、ビルド設定最適化、CI/CD統合、Fastlaneセットアップ
**公式で確認すべきこと**: 最新のXcodeバージョン、iOSリリースノート、App Store審査ガイドライン

### 主要な公式ドキュメント

- **[Xcode Documentation](https://developer.apple.com/documentation/xcode)** - Apple公式開発環境
  - [Build Settings Reference](https://developer.apple.com/documentation/xcode/build-settings-reference)
  - [Configuring Your Xcode Project](https://developer.apple.com/documentation/xcode)

- **[Swift Package Manager](https://www.swift.org/package-manager/)** - Swift公式パッケージマネージャー
  - [Getting Started](https://www.swift.org/getting-started/)

- **[Fastlane Documentation](https://docs.fastlane.tools/)** - iOSデプロイ自動化ツール
  - [Getting Started](https://docs.fastlane.tools/getting-started/ios/setup/)
  - [Actions](https://docs.fastlane.tools/actions/)

- **[SwiftLint Documentation](https://realm.github.io/SwiftLint/)** - Swiftコード品質ツール

### 関連リソース

- **[CocoaPods Guides](https://guides.cocoapods.org/)** - 依存関係管理
- **[iOS App Dev Tutorials](https://developer.apple.com/tutorials/app-dev-training)** - Apple公式チュートリアル
- **[App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)** - 審査ガイドライン

---

### カバー範囲

- ✅ Xcodeプロジェクト作成・初期設定
- ✅ プロジェクト構造設計（MVVM / Clean Architecture）
- ✅ Build Settings 最適化
- ✅ Scheme & Configuration 管理
- ✅ Asset Management（画像、色、フォント）
- ✅ Code Signing 設定
- ✅ 依存関係管理（SPM / CocoaPods / Carthage）
- ✅ Fastlane セットアップ
- ✅ SwiftLint / SwiftFormat 設定
- ✅ Git セットアップ（.gitignore, hooks）
- ✅ CI/CD 初期設定（GitHub Actions）
- ✅ テンプレート & 自動化スクリプト
- ✅ チーム開発環境統一
- ✅ Feature Flags / Analytics 統合

### 新機能（2024年更新）

🆕 **3つの完全ガイド**（合計 170,000+ 文字）
- iOS Project Initial Setup - 完全ガイド (55,000+ chars)
- iOS Dependency & Tooling Setup - 完全ガイド (30,000+ chars)
- iOS Templates & Automation - 完全ガイド (87,000+ chars)

🆕 **包括的なテンプレート集**
- xcconfig ファイル（Base, Debug, Release）
- .gitignore テンプレート
- Fastlane セットアップ
- SwiftLint 設定
- 自動化スクリプト

🆕 **プロジェクト自動化**
- セットアップスクリプト（setup.sh）
- Feature 生成スクリプト
- 環境変数管理
- Git hooks 自動設定

---

## いつ使うか

### プロジェクト開始時

```bash
# 新規 iOS プロジェクトを開始する時
- 会社の新規プロジェクト
- 個人開発の新しいアプリ
- ハッカソンプロジェクト
- プロトタイプ作成

推奨アクション:
1. ガイドに従ってプロジェクト構造を決定
2. テンプレートを使用して初期ファイル生成
3. 自動化スクリプトで環境構築
```

### プロジェクト見直し時

```bash
# 既存プロジェクトの構成を見直す時
- 技術的負債の解消
- アーキテクチャ変更
- チーム開発への移行
- CI/CD 導入

推奨アクション:
1. 現状とベストプラクティスを比較
2. 段階的に設定を改善
3. ドキュメント整備
```

### チームメンバー追加時

```bash
# 新しいメンバーがジョインした時
- オンボーディング
- 環境構築支援
- ベストプラクティス共有

推奨アクション:
1. セットアップスクリプトを実行
2. ガイドを参照しながら環境構築
3. チーム規約の確認
```

---

## 完全ガイド

### 1. iOS Project Initial Setup - 完全ガイド

**ファイル**: [guides/01-ios-project-initial-setup.md](guides/01-ios-project-initial-setup.md)
**文字数**: 55,873 chars

#### カバー内容

1. **プロジェクト初期化の概要**
   - なぜ適切な初期設定が重要か
   - プロジェクト作成前のチェックリスト
   - プロジェクト命名規則

2. **Xcode プロジェクト作成**
   - ステップバイステップガイド
   - プロジェクト設定の詳細
   - General / Signing & Capabilities / Build Settings

3. **プロジェクト構造設計**
   - MVVM アーキテクチャによるフォルダ構成
   - Clean Architecture によるフォルダ構成
   - ファイル配置の実装例

4. **Build Settings 最適化**
   - Debug vs Release 設定の違い
   - パフォーマンス最適化設定
   - ビルド時間の最適化

5. **Scheme Configuration**
   - Scheme の役割と種類
   - 推奨 Scheme 構成
   - Environment Variables の活用

6. **Asset Management**
   - Assets.xcassets の構成
   - App Icon の設定
   - Color Assets の活用
   - Image Assets の最適化

7. **Info.plist 設定**
   - 必須設定項目
   - Privacy 関連の Usage Description
   - Background Modes
   - Custom URL Scheme と Universal Links

8. **Code Signing 設定**
   - Code Signing の概要
   - 自動 Code Signing
   - 手動 Code Signing
   - Fastlane Match による管理

### 2. iOS Dependency & Tooling Setup - 完全ガイド

**ファイル**: [guides/02-ios-dependency-tooling-setup.md](guides/02-ios-dependency-tooling-setup.md)
**文字数**: 29,923 chars

#### カバー内容

1. **依存関係管理の概要**
   - なぜ依存関係管理が重要か
   - ライブラリ選定の基準

2. **Swift Package Manager (SPM)**
   - SPM の概要とメリット
   - パッケージ追加方法
   - Package.swift による管理
   - ローカル Package の作成

3. **CocoaPods**
   - CocoaPods の概要
   - インストールとセットアップ
   - Podfile の作成と管理
   - ベストプラクティス

4. **Carthage**
   - Carthage の概要
   - インストールと使用方法
   - プロジェクトへの統合

5. **依存関係管理の比較と選択**
   - SPM vs CocoaPods vs Carthage
   - プロジェクトタイプ別推奨
   - 併用時の注意点

6. **Fastlane セットアップ**
   - Fastlane の概要
   - インストールと初期化
   - Fastfile の基本構成
   - 主要な Lane の実装

7. **SwiftLint 設定**
   - SwiftLint の導入
   - 詳細な設定ファイル
   - カスタムルールの作成
   - Xcode 統合

8. **SwiftFormat 設定**
   - SwiftFormat の導入
   - 設定ファイルの作成
   - 自動整形の設定

9. **Danger.swift**
   - Danger.swift の導入
   - PR 自動レビュー設定

10. **Pre-commit Hooks**
    - Git hooks の設定
    - 自動チェックの実装

11. **CI/CD 初期設定**
    - GitHub Actions の設定
    - テスト・ビルド・デプロイの自動化

### 3. iOS Templates & Automation - 完全ガイド

**ファイル**: [guides/03-ios-templates-automation.md](guides/03-ios-templates-automation.md)
**文字数**: 87,116 chars

#### カバー内容

1. **プロジェクトテンプレートの概要**
   - なぜテンプレートが必要か
   - テンプレートに含めるべき要素

2. **Xcode Project Template 作成**
   - カスタムテンプレートの作成
   - テンプレート構造
   - TemplateInfo.plist の設定

3. **セットアップ自動化スクリプト**
   - プロジェクト作成スクリプト
   - 開発環境セットアップスクリプト
   - チェックリストの自動化

4. **ボイラープレートコード生成**
   - Feature モジュール生成スクリプト
   - ネットワーク層テンプレート
   - Repository / UseCase テンプレート

5. **環境設定の自動化**
   - .env ファイル管理
   - 環境変数読み込みスクリプト
   - Swift での環境変数アクセス

6. **Feature Flags 設定**
   - Feature Flag Manager の実装
   - Local / Remote Feature Flags
   - Firebase Remote Config 統合

7. **Analytics 統合**
   - Firebase Analytics
   - カスタムイベント定義
   - トラッキング実装

8. **Crash Reporting 統合**
   - Firebase Crashlytics
   - エラーログ収集
   - クラッシュレポート分析

9. **Localization Setup**
   - 多言語対応の設定
   - Localizable.strings 管理
   - 自動翻訳ワークフロー

10. **Accessibility Configuration**
    - VoiceOver 対応
    - Dynamic Type 対応
    - アクセシビリティテスト

11. **CI/CD Template**
    - GitHub Actions ワークフロー
    - TestFlight 自動デプロイ
    - App Store 申請自動化

12. **ドキュメント自動生成**
    - README テンプレート
    - CONTRIBUTING ガイド
    - API ドキュメント生成

---

## テンプレート & スクリプト

### Xcconfig ファイル

#### Base.xcconfig
**場所**: [templates/xcconfig/Base.xcconfig](templates/xcconfig/Base.xcconfig)

全環境共通の基本設定：
- Deployment Target
- Swift Version
- Warnings
- Build Options

#### Debug.xcconfig
**場所**: [templates/xcconfig/Debug.xcconfig](templates/xcconfig/Debug.xcconfig)

Debug ビルド設定：
- 開発用 API エンドポイント
- デバッグメニュー有効化
- 最適化なし（ビルド時間優先）

#### Release.xcconfig
**場所**: [templates/xcconfig/Release.xcconfig](templates/xcconfig/Release.xcconfig)

Release ビルド設定：
- 本番 API エンドポイント
- 最適化有効（パフォーマンス優先）
- Dead Code Stripping
- Symbol Stripping

### .gitignore

**場所**: [templates/gitignore/iOS.gitignore](templates/gitignore/iOS.gitignore)

包括的な iOS プロジェクト用 .gitignore：
- Xcode 関連
- SPM / CocoaPods / Carthage
- Fastlane
- 環境変数ファイル
- macOS システムファイル

### 自動化スクリプト

#### setup.sh
**場所**: [templates/scripts/setup.sh](templates/scripts/setup.sh)

プロジェクト環境セットアップスクリプト：
- Homebrew のインストール確認
- Xcode のバージョン確認
- 開発ツールのインストール（SwiftLint, SwiftFormat, Fastlane）
- Bundler / CocoaPods セットアップ
- Git hooks の設定

使用方法：
```bash
chmod +x setup.sh
./setup.sh
```

### Fastlane Template

**場所**: [templates/fastlane/Fastfile.template](templates/fastlane/Fastfile.template)

包括的な Fastlane 設定：
- Development / Staging / Production ビルド
- 自動テスト実行
- TestFlight アップロード
- 証明書管理（Match）
- スクリーンショット生成
- バージョン管理

### SwiftLint Configuration

**場所**: [templates/swiftlint.yml](templates/swiftlint.yml)

包括的な SwiftLint 設定：
- 150+ のルール設定
- カスタムルール（no_print, no_force_try, etc.）
- プロジェクト構成に合わせた除外設定
- チーム規約の強制

---

## クイックスタート

### 新規プロジェクトを作成する

```bash
# 1. プロジェクトディレクトリを作成
mkdir MyAwesomeApp
cd MyAwesomeApp

# 2. Git 初期化
git init

# 3. .gitignore をコピー
cp /path/to/ios-project-setup/templates/gitignore/iOS.gitignore .gitignore

# 4. SwiftLint 設定をコピー
cp /path/to/ios-project-setup/templates/swiftlint.yml .swiftlint.yml

# 5. Xcode でプロジェクトを作成
# File > New > Project > iOS > App
# プロジェクト名: MyAwesomeApp
# Bundle ID: com.company.myawesomeapp

# 6. xcconfig ファイルをコピー
mkdir -p Config
cp /path/to/ios-project-setup/templates/xcconfig/*.xcconfig Config/

# 7. セットアップスクリプトをコピー
mkdir -p scripts
cp /path/to/ios-project-setup/templates/scripts/setup.sh scripts/
chmod +x scripts/setup.sh

# 8. 環境セットアップを実行
./scripts/setup.sh

# 9. Fastlane を初期化
bundle exec fastlane init

# 10. 初回コミット
git add .
git commit -m "feat(init): initial project setup"
```

### 既存プロジェクトに設定を追加する

```bash
# 1. SwiftLint を追加
cp /path/to/ios-project-setup/templates/swiftlint.yml .swiftlint.yml
brew install swiftlint

# 2. xcconfig ファイルを追加
mkdir -p Config
cp /path/to/ios-project-setup/templates/xcconfig/*.xcconfig Config/

# Xcode でプロジェクトに xcconfig を設定:
# Project > Info > Configurations
# Debug: Config/Debug.xcconfig
# Release: Config/Release.xcconfig

# 3. Git hooks を設定
cp /path/to/ios-project-setup/templates/scripts/setup.sh scripts/
./scripts/setup.sh

# 4. Fastlane を追加
bundle exec fastlane init
cp /path/to/ios-project-setup/templates/fastlane/Fastfile.template fastlane/Fastfile
```

### 推奨ワークフロー

```bash
# 日常的な開発フロー

# 1. 新機能開発開始
git checkout -b feature/new-awesome-feature

# 2. コード作成
# Xcode で実装...

# 3. コミット前に自動チェック（pre-commit hook が実行）
git add .
git commit -m "feat(feature): add awesome new feature"

# 4. プッシュ
git push origin feature/new-awesome-feature

# 5. Pull Request 作成
# GitHub で PR を作成（CI が自動実行）

# 6. レビュー後マージ
# main にマージ

# 7. Staging デプロイ
bundle exec fastlane staging

# 8. Production リリース（準備が整ったら）
bundle exec fastlane release
```

---

## ベストプラクティス

### プロジェクト構成

```
推奨:
✅ Feature-based organization（機能単位）
✅ MVVM または Clean Architecture
✅ Dependency Injection
✅ Protocol-oriented design

避けるべき:
❌ MVC（Massive View Controller）
❌ グローバル変数の乱用
❌ Singleton の過度な使用
```

### 依存関係管理

```
推奨:
✅ Swift Package Manager（第一選択）
✅ セマンティックバージョニング (~> 1.0)
✅ Package.resolved を Git で管理

避けるべき:
❌ 最新版への自動更新（予期しない変更）
❌ バージョン指定なし
❌ 不必要な依存関係の追加
```

### Git ワークフロー

```
推奨:
✅ Git Flow または GitHub Flow
✅ Conventional Commits
✅ Pre-commit hooks で自動チェック
✅ .gitignore の適切な設定

避けるべき:
❌ main への直接コミット
❌ 意味のないコミットメッセージ
❌ 大量のファイルを一度にコミット
```

### CI/CD

```
推奨:
✅ GitHub Actions / Bitrise
✅ 自動テスト実行
✅ TestFlight 自動デプロイ
✅ Fastlane で統一

避けるべき:
❌ 手動デプロイ
❌ テストなしでのマージ
❌ 環境ごとに異なる手順
```

---

## トラブルシューティング

### よくある問題と解決策

#### 1. SwiftLint エラーが大量に出る

```bash
# 問題: 既存コードが SwiftLint ルールに違反

# 解決策:
# 1. 自動修正を実行
swiftlint --fix

# 2. それでも残るエラーは手動修正
# 3. ルールが厳しすぎる場合は .swiftlint.yml で調整

# disabled_rules に追加:
disabled_rules:
  - line_length
  - force_cast
```

#### 2. CocoaPods インストールが失敗する

```bash
# 問題: pod install が失敗する

# 解決策:
# 1. キャッシュをクリア
pod cache clean --all
rm -rf ~/Library/Caches/CocoaPods

# 2. Podfile.lock を削除して再インストール
rm Podfile.lock
pod install

# 3. CocoaPods を最新版に更新
sudo gem install cocoapods
```

#### 3. Xcode ビルドが遅い

```bash
# 問題: ビルド時間が長い

# 解決策:
# 1. Derived Data を削除
rm -rf ~/Library/Developer/Xcode/DerivedData

# 2. Debug ビルドで Whole Module Optimization を無効化
# Build Settings > Compilation Mode > Incremental

# 3. ビルド時間を計測
OTHER_SWIFT_FLAGS = -Xfrontend -debug-time-function-bodies

# 4. 遅い関数を特定して最適化
```

#### 4. Git hooks が動作しない

```bash
# 問題: pre-commit hook が実行されない

# 解決策:
# 1. 実行権限を確認
chmod +x .git/hooks/pre-commit

# 2. Shebang を確認
head -n1 .git/hooks/pre-commit
# #!/bin/bash であることを確認

# 3. 手動で実行してエラー確認
.git/hooks/pre-commit
```

---

## 関連 Skills

### 開発プロセス

- **git-workflow**: Git ブランチ戦略、コミット規約
- **code-review**: コードレビューのベストプラクティス
- **testing-strategy**: テスト戦略、TDD/BDD

### iOS 開発

- **ios-development**: iOS 開発全般のベストプラクティス
- **swiftui-patterns**: SwiftUI 開発パターン
- **ios-security**: セキュリティ実装

### ツール & 自動化

- **ci-cd-automation**: CI/CD パイプライン構築
- **dependency-management**: 依存関係管理詳細
- **script-development**: 自動化スクリプト開発

### ドキュメント

- **documentation**: 技術ドキュメント作成
- **quality-assurance**: QA プロセス

---

## 更新履歴

### v2.0.0 (2024-01-03)

🎉 **大幅アップデート**

- ✨ 3つの完全ガイド追加（合計 170,000+ 文字）
- ✨ 包括的なテンプレート集の追加
- ✨ 自動化スクリプトの充実
- ✨ Fastlane テンプレート追加
- ✨ SwiftLint / SwiftFormat 設定の詳細化
- ✨ Feature Flags / Analytics 統合ガイド
- ✨ Xcode Project Template 作成ガイド
- ✨ 環境変数管理の自動化
- ✨ トラブルシューティングセクション追加

### v1.0.0 (2023-XX-XX)

- 📝 初回リリース
- 基本的なプロジェクト設定ガイド

---

## コントリビューション

このスキルの改善提案やバグ報告は Issue または Pull Request でお願いします。

## ライセンス

MIT License

---

**最終更新**: 2024-01-03
**ステータス**: 🟢 High (100% completion, 3/3 guides)
**文字数**: 170,000+ chars (目標: 75,000+)
