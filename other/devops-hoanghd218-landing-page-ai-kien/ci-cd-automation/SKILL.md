---
name: ci-cd-automation
description: GitHub Actions、Fastlane、Bitriseを活用したCI/CDパイプライン構築。自動ビルド、テスト実行、コード署名、TestFlight配布、App Store申請まで、開発からリリースまでの完全自動化ガイド。
---

# CI/CD Automation Skill

## 📋 目次

1. [概要](#概要)
2. [いつ使うか](#いつ使うか)
3. [CI/CDパイプライン設計](#cicdパイプライン設計)
4. [GitHub Actions](#github-actions)
5. [Fastlane](#fastlane)
6. [ベストプラクティス](#ベストプラクティス)
7. [よくある問題](#よくある問題)
8. [Agent連携](#agent連携)

---

## 概要

このSkillは、CI/CD自動化の全てをカバーします：

- ✅ GitHub Actions ワークフロー設計
- ✅ Fastlane完全活用
- ✅ 自動ビルド・テスト
- ✅ コード署名自動化
- ✅ TestFlight自動配布
- ✅ App Store自動申請
- ✅ キャッシュ戦略
- ✅ パイプライン最適化
- ✅ シークレット管理

## 📚 公式ドキュメント・参考リソース

**このガイドで学べること**: CI/CDパイプライン設計、GitHub Actions設定、Fastlane活用、自動デプロイ
**公式で確認すべきこと**: 最新のCI/CD機能、セキュリティアップデート、パフォーマンス最適化

### 主要な公式ドキュメント

- **[GitHub Actions Documentation](https://docs.github.com/en/actions)** - GitHub公式CI/CD
  - [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
  - [Actions Marketplace](https://github.com/marketplace?type=actions)

- **[Fastlane Documentation](https://docs.fastlane.tools/)** - iOS/Android自動化ツール
  - [Getting Started](https://docs.fastlane.tools/getting-started/ios/setup/)
  - [Actions](https://docs.fastlane.tools/actions/)

- **[GitLab CI/CD](https://docs.gitlab.com/ee/ci/)** - GitLab統合CI/CD
  - [Configuration](https://docs.gitlab.com/ee/ci/yaml/)

- **[CircleCI Documentation](https://circleci.com/docs/)** - CI/CDプラットフォーム

### 関連リソース

- **[Continuous Integration by Martin Fowler](https://martinfowler.com/articles/continuousIntegration.html)** - CI/CD理論
- **[The DevOps Handbook](https://itrevolution.com/product/the-devops-handbook/)** - DevOpsプラクティス
- **[Bitrise Documentation](https://devcenter.bitrise.io/)** - モバイルCI/CD

---

## いつ使うか

### 自動的に参照されるケース

- CI/CDワークフローを修正する時
- ビルドが失敗した時
- デプロイが失敗した時

### 手動で参照すべきケース

- 新規プロジェクトでCI/CD構築
- パイプライン最適化
- 新しい自動化タスク追加
- トラブルシューティング

---

## CI/CDパイプライン設計

### 基本パイプライン

```
┌──────────────┐
│  Push/PR     │
└──────┬───────┘
       │
┌──────▼───────┐
│  Lint        │  SwiftLint, SwiftFormat
└──────┬───────┘
       │
┌──────▼───────┐
│  Build       │  Xcode Build
└──────┬───────┘
       │
┌──────▼───────┐
│  Test        │  Unit + UI Tests
└──────┬───────┘
       │
┌──────▼───────┐
│  Coverage    │  カバレッジレポート
└──────┬───────┘
       │
┌──────▼───────┐
│  Deploy      │  TestFlight (mainブランチのみ)
└──────────────┘
```

詳細: [guides/01-pipeline-design.md](guides/01-pipeline-design.md)

### 高度なパイプライン

```
PR作成時:
  → Lint → Build → Unit Tests → Security Scan
  → レビュー待ち

mainマージ時:
  → 全テスト → Build Archive → TestFlight → Slack通知

タグプッシュ時:
  → 全テスト → Production Build → App Store → Release Notes
```

詳細: [guides/02-advanced-pipeline.md](guides/02-advanced-pipeline.md)

---

## GitHub Actions

### 基本ワークフロー

```yaml
name: iOS CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build-and-test:
    runs-on: macos-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Xcode
      uses: maxim-lobanov/setup-xcode@v1
      with:
        xcode-version: '15.2'

    - name: Cache SPM
      uses: actions/cache@v3
      with:
        path: .build
        key: ${{ runner.os }}-spm-${{ hashFiles('**/Package.resolved') }}

    - name: Build
      run: xcodebuild build -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 15'

    - name: Test
      run: xcodebuild test -scheme YourApp -destination 'platform=iOS Simulator,name=iPhone 15'
```

詳細: [guides/03-github-actions-basics.md](guides/03-github-actions-basics.md)

### ワークフロー例

- [PR自動チェック](templates/workflows/pr-check.yml)
- [TestFlight自動配布](templates/workflows/testflight-deploy.yml)
- [App Store自動申請](templates/workflows/appstore-release.yml)
- [定期ビルド](templates/workflows/scheduled-build.yml)

詳細ガイド:
- [guides/04-pr-workflow.md](guides/04-pr-workflow.md)
- [guides/05-deploy-workflow.md](guides/05-deploy-workflow.md)
- [guides/06-release-workflow.md](guides/06-release-workflow.md)

---

## Fastlane

### セットアップ

```bash
# Fastlane インストール
gem install fastlane

# 初期化
fastlane init

# プラグインインストール
fastlane add_plugin badge
fastlane add_plugin changelog
```

詳細: [guides/07-fastlane-setup.md](guides/07-fastlane-setup.md)

### Fastfile例

```ruby
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(scheme: "YourApp")
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number
    build_app(scheme: "YourApp")
    upload_to_testflight
    slack(message: "New beta build available!")
  end

  desc "Release to App Store"
  lane :release do
    increment_version_number
    build_app(scheme: "YourApp")
    upload_to_app_store
    slack(message: "New version released!")
  end
end
```

詳細:
- [guides/08-fastlane-lanes.md](guides/08-fastlane-lanes.md)
- [guides/09-fastlane-match.md](guides/09-fastlane-match.md) (コード署名)
- [guides/10-fastlane-plugins.md](guides/10-fastlane-plugins.md)

---

## ベストプラクティス

### キャッシュ戦略

```yaml
# SPM依存関係
- uses: actions/cache@v3
  with:
    path: .build
    key: ${{ runner.os }}-spm-${{ hashFiles('**/Package.resolved') }}

# CocoaPods
- uses: actions/cache@v3
  with:
    path: Pods
    key: ${{ runner.os }}-pods-${{ hashFiles('**/Podfile.lock') }}

# Derived Data
- uses: actions/cache@v3
  with:
    path: ~/Library/Developer/Xcode/DerivedData
    key: ${{ runner.os }}-derived-data
```

詳細: [references/caching-strategy.md](references/caching-strategy.md)

### シークレット管理

```yaml
# GitHub Secrets使用
env:
  MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
  APP_STORE_CONNECT_API_KEY: ${{ secrets.APP_STORE_CONNECT_API_KEY }}
```

詳細: [references/secrets-management.md](references/secrets-management.md)

### 並列実行

```yaml
jobs:
  lint:
    runs-on: macos-latest
    # ...

  test-ios15:
    runs-on: macos-latest
    # iOS 15でテスト

  test-ios16:
    runs-on: macos-latest
    # iOS 16でテスト

  test-ios17:
    runs-on: macos-latest
    # iOS 17でテスト
```

詳細: [references/parallel-execution.md](references/parallel-execution.md)

---

## よくある問題

### ビルド失敗

| 原因 | 解決策 |
|------|--------|
| Xcodeバージョン不一致 | `setup-xcode` で固定 |
| 依存関係エラー | キャッシュクリア |
| コード署名エラー | Fastlane Match使用 |

詳細: [references/troubleshooting.md](references/troubleshooting.md)

### ビルド時間が長い

→ [references/build-optimization.md](references/build-optimization.md)

### TestFlight配布失敗

→ [incidents/testflight-failures/](incidents/testflight-failures/)

---

## Agent連携

### このSkillを使用するAgents

1. **ci-runner-agent**
   - CIパイプライン実行
   - Thoroughness: `quick`

2. **build-optimizer-agent**
   - ビルド時間分析・最適化提案
   - Thoroughness: `thorough`

3. **deploy-agent**
   - TestFlight/App Store配布
   - Thoroughness: `medium`

4. **pipeline-debugger-agent**
   - パイプライン失敗原因分析
   - Thoroughness: `thorough`

### 推奨Agentワークフロー

#### ビルド失敗時（順次実行）

```
pipeline-debugger-agent (原因分析)
→ 修正提案
→ ci-runner-agent (再実行)
```

#### パイプライン最適化時（並行実行）

```
build-optimizer-agent (ビルド最適化) +
test-optimizer-agent (テスト最適化) +
cache-analyzer-agent (キャッシュ分析)
→ 結果統合 → 最適化計画
```

---

## クイックリファレンス

### よく使うFastlaneコマンド

```bash
# テスト実行
fastlane test

# TestFlight配布
fastlane beta

# App Storeリリース
fastlane release

# スクリーンショット生成
fastlane snapshot

# 証明書同期
fastlane match development
fastlane match appstore
```

### GitHub Actions手動実行

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - development
          - staging
          - production
```

### トラブルシューティングコマンド

```bash
# キャッシュクリア
rm -rf ~/Library/Developer/Xcode/DerivedData
rm -rf .build

# Fastlaneログ確認
cat ~/Library/Logs/fastlane/fastlane.log

# GitHub Actions ログダウンロード
gh run view <run-id> --log
```

---

## 詳細ドキュメント

### Guides（詳細ガイド）

**🎯 完全ガイド（実践的・網羅的）**
1. [GitHub Actions 完全ガイド](guides/github-actions-complete.md) - 基礎から高度な活用まで
2. [Fastlane 完全ガイド](guides/fastlane-complete.md) - iOS/Android自動化の全て
3. [デプロイメント自動化 完全ガイド](guides/deployment-complete.md) - 環境管理とデプロイ戦略
4. [パイプライン最適化ガイド](guides/pipeline-optimization-guide.md) - **NEW!** ビルド時間短縮・コスト削減

### Checklists（チェックリスト）

**構築時**
- [パイプライン構築チェックリスト](checklists/pipeline-setup-checklist.md) - **NEW!** CI/CD構築の全手順

**運用時**
- [デプロイメントチェックリスト](checklists/deployment-checklist.md) - **NEW!** デプロイ前後の確認事項

### Templates（テンプレート）

**GitHub Actions ワークフロー**
- [完全版CI/CDワークフロー](templates/workflows/ci-complete.yml) - **NEW!** Next.js/React向け完全設定
- [iOS Fastlaneワークフロー](templates/workflows/ios-fastlane.yml) - **NEW!** TestFlight/App Store自動配布

### References（リファレンス）

- [ベストプラクティス集](references/best-practices.md) - **NEW!** GitHub Actions、Fastlane、デプロイメントのベストプラクティス
- [トラブルシューティング](references/troubleshooting.md) - **NEW!** よくある問題と解決方法

---

## 学習リソース

- 📚 [GitHub Actions Documentation](https://docs.github.com/en/actions)
- 📖 [Fastlane Documentation](https://docs.fastlane.tools/)
- 📘 [Bitrise](https://www.bitrise.io/)

---

## 関連Skills

- `git-workflow` - ブランチ戦略との連携
- `testing-strategy` - テスト自動実行
- `code-signing` - 証明書管理
- `release-process` - リリースフロー
- `app-store-submission` - App Store申請

---

## 更新履歴

このSkill自体の変更履歴は [CHANGELOG.md](CHANGELOG.md) を参照
