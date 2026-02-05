---
name: xcode-project
description: Xcodeプロジェクト設定支援。ビルド設定の最適化、Target/Scheme構成、SPM(Swift Package Manager)活用、xcconfig活用など、プロジェクト構成に関する包括的なサポートを提供する。「Xcodeプロジェクトを設定したい」「ビルド設定を最適化したい」「SPMを導入したい」と言った時に使用する。
---

# Xcode Project Configuration

Xcodeプロジェクト設定の最適化とベストプラクティスに基づく構成支援を提供する。

## 概要

このスキルは以下の領域をカバーする:
- Xcodeプロジェクト構造の設計と最適化
- ビルド設定（Build Settings）の適切な構成
- Target/Scheme の効率的な構成
- Swift Package Manager (SPM) を使った依存関係管理
- xcconfig ファイルを使った設定管理

## 実行条件

- Xcodeプロジェクト（.xcodeproj / .xcworkspace）が存在する
- macOS環境でXcodeがインストールされている
- プロジェクトのビルド設定を変更する権限がある

## プロセス

### Phase 1: 現状分析

1. **プロジェクト構造の確認**
   ```bash
   # プロジェクトファイル一覧
   ls -la *.xcodeproj *.xcworkspace 2>/dev/null

   # プロジェクト内のターゲット確認
   xcodebuild -list -project Project.xcodeproj
   ```

2. **現在のビルド設定確認**
   ```bash
   # ビルド設定一覧
   xcodebuild -showBuildSettings -project Project.xcodeproj -target TargetName
   ```

3. **依存関係の確認**
   - Package.swift（SPM）
   - Podfile（CocoaPods）
   - Cartfile（Carthage）

### Phase 2: 問題点の特定

以下の観点から問題点を洗い出す:

#### ビルド設定の問題
- [ ] SWIFT_VERSION が適切に設定されているか
- [ ] DEPLOYMENT_TARGET が要件を満たしているか
- [ ] CODE_SIGN_STYLE が適切か（Manual vs Automatic）
- [ ] BUILD_LIBRARY_FOR_DISTRIBUTION が必要な場合に設定されているか
- [ ] Debug/Release で適切な最適化フラグが設定されているか

#### Target構成の問題
- [ ] 不要なTargetが存在しないか
- [ ] Target間の依存関係が適切か
- [ ] 共有コードがFramework/Package化されているか

#### 依存関係管理の問題
- [ ] 複数の依存関係管理ツールが混在していないか
- [ ] バージョン固定が適切に行われているか
- [ ] セキュリティ脆弱性のあるライブラリがないか

### Phase 3: 最適化提案

#### 3.1 ビルド設定最適化

**Debug設定の推奨値**:
```
SWIFT_OPTIMIZATION_LEVEL = -Onone
DEBUG_INFORMATION_FORMAT = dwarf
ENABLE_TESTABILITY = YES
GCC_PREPROCESSOR_DEFINITIONS = DEBUG=1
```

**Release設定の推奨値**:
```
SWIFT_OPTIMIZATION_LEVEL = -O / -Osize
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym
ENABLE_TESTABILITY = NO
SWIFT_COMPILATION_MODE = wholemodule
```

#### 3.2 xcconfig導入

詳細は [references/xcconfig-guide.md](references/xcconfig-guide.md) を参照。

**推奨ファイル構成**:
```
Configurations/
├── Base.xcconfig           # 共通設定
├── Debug.xcconfig          # Debug固有設定
├── Release.xcconfig        # Release固有設定
├── Signing/
│   ├── Debug.xcconfig      # Debug署名設定
│   └── Release.xcconfig    # Release署名設定
└── Targets/
    ├── App.xcconfig        # アプリTarget固有
    └── Framework.xcconfig  # Framework Target固有
```

#### 3.3 SPM移行・導入

詳細は [references/spm-guide.md](references/spm-guide.md) を参照。

**CocoaPodsからの移行手順**:
1. SPMで利用可能なライブラリを確認
2. Package.swift または Xcode GUI で依存追加
3. Podfile から該当ライブラリを削除
4. `pod install` で更新
5. ビルド確認

### Phase 4: 実装

1. **バックアップ作成**
   ```bash
   cp -r Project.xcodeproj Project.xcodeproj.backup
   ```

2. **xcconfig適用**
   - プロジェクト設定 > Info > Configurations で xcconfig を指定
   - ビルド設定で `$(inherited)` を活用

3. **SPM依存追加**
   - File > Add Package Dependencies
   - または Package.swift 編集

4. **ビルド確認**
   ```bash
   xcodebuild clean build -scheme SchemeName -destination 'platform=iOS Simulator,name=iPhone 16'
   ```

### Phase 5: 検証

```bash
# フルビルド確認
xcodebuild clean build -scheme SchemeName

# テスト実行
xcodebuild test -scheme SchemeName -destination 'platform=iOS Simulator,name=iPhone 16'

# アーカイブ確認
xcodebuild archive -scheme SchemeName -archivePath build/App.xcarchive
```

## 出力形式

### 分析レポート

```markdown
## Xcodeプロジェクト分析レポート

### プロジェクト概要
- プロジェクト名: [名前]
- Targets: [数]
- Schemes: [数]
- 依存管理: [SPM/CocoaPods/Carthage]

### 検出された問題

#### 🔴 重要度: 高
- [問題の説明]
  - 影響: [具体的な影響]
  - 推奨対応: [対応方法]

#### 🟡 重要度: 中
- [問題の説明]

#### 🟢 重要度: 低
- [問題の説明]

### 推奨アクション

1. [アクション1]
2. [アクション2]
```

### 設定変更サマリー

```markdown
## 設定変更サマリー

### 変更前
```xcconfig
SWIFT_VERSION = 5.0
```

### 変更後
```xcconfig
SWIFT_VERSION = 5.9
```

### 理由
[変更理由の説明]
```

## ガードレール

### 禁止事項
- ユーザー確認なしでのプロジェクトファイル変更
- バックアップなしでの破壊的変更
- 署名関連設定の無断変更
- 本番環境のビルド設定の変更（明示的な許可がない場合）

### 確認必須事項
- 設定変更前に必ず現状のバックアップを取得
- 変更内容をユーザーに提示し承認を得る
- 変更後は必ずビルド確認を実施
- CI/CDへの影響を考慮

### 推奨事項
- xcconfig による設定管理を推奨
- ハードコードされた設定より変数化を優先
- 環境別設定は明確に分離
- ドキュメント化を徹底
