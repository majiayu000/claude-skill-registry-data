---
name: ios-signing
description: iOSアプリのコード署名・プロビジョニング支援。証明書管理、Provisioning Profile管理、Keychain設定、CI/CD環境での署名設定など、コード署名に関する包括的なサポートを提供する。「署名エラーを解決したい」「証明書を更新したい」「CIで署名を設定したい」と言った時に使用する。
---

# iOS Code Signing

iOSアプリのコード署名設定とトラブルシューティングを支援する。

## 概要

このスキルは以下の領域をカバーする:
- コード署名の仕組みと概念
- 証明書（Certificates）の管理
- Provisioning Profile の管理
- Keychain の設定
- CI/CD 環境での署名自動化

## 実行条件

- Apple Developer Program に登録済み
- macOS 環境でXcodeがインストールされている
- App Store Connect / Apple Developer Portal へのアクセス権限がある

## プロセス

### Phase 1: 現状診断

#### 1.1 証明書の確認

```bash
# キーチェーン内の証明書一覧
security find-identity -v -p codesigning

# 有効な証明書のみ
security find-identity -v -p codesigning | grep "Apple Development\|Apple Distribution"
```

**期待される出力例**:
```
1) XXXXXXXXXX "Apple Development: Your Name (TEAM_ID)"
2) YYYYYYYYYY "Apple Distribution: Your Company (TEAM_ID)"
```

#### 1.2 Provisioning Profile の確認

```bash
# インストール済みProfile一覧
ls -la ~/Library/MobileDevice/Provisioning\ Profiles/

# Profile内容の確認
security cms -D -i ~/Library/MobileDevice/Provisioning\ Profiles/XXXX.mobileprovision
```

#### 1.3 プロジェクト設定の確認

```bash
# ビルド設定の署名関連項目
xcodebuild -showBuildSettings -project Project.xcodeproj | grep -E "CODE_SIGN|PROVISIONING|DEVELOPMENT_TEAM"
```

### Phase 2: 問題特定

#### よくある署名エラーと原因

| エラー | 原因 | 解決方法 |
|-------|------|---------|
| `No signing certificate found` | 証明書がない/期限切れ | 証明書の作成/更新 |
| `Profile doesn't include signing certificate` | Profile と証明書の不一致 | Profile の再生成 |
| `App ID doesn't match bundle identifier` | Bundle ID の不一致 | App ID の確認/修正 |
| `Provisioning profile expired` | Profile 期限切れ | Profile の更新 |
| `Device not included in profile` | デバイス未登録 | デバイス追加と Profile 再生成 |

#### 診断フロー

```
1. 証明書は有効か？
   ├─ NO → 証明書を作成/更新
   └─ YES
        ↓
2. Profile に証明書が含まれているか？
   ├─ NO → Profile を再生成
   └─ YES
        ↓
3. Bundle ID が一致しているか？
   ├─ NO → Bundle ID を修正
   └─ YES
        ↓
4. デバイスが登録されているか？（Ad Hoc/Development）
   ├─ NO → デバイス追加と Profile 再生成
   └─ YES → その他の問題を調査
```

### Phase 3: 解決策実行

詳細は以下の参照ドキュメントを確認:
- [references/certificate-guide.md](references/certificate-guide.md) - 証明書管理
- [references/provisioning-profile-guide.md](references/provisioning-profile-guide.md) - Profile管理
- [references/ci-signing-guide.md](references/ci-signing-guide.md) - CI/CD署名

#### 3.1 証明書の作成（開発用）

1. **Keychain Access でCSRを作成**
   - Keychain Access > Certificate Assistant > Request a Certificate From a Certificate Authority
   - 「Save to disk」を選択

2. **Apple Developer Portal で証明書発行**
   - Certificates, Identifiers & Profiles > Certificates
   - 「+」ボタン > 「Apple Development」を選択
   - CSRをアップロード

3. **証明書のダウンロードとインストール**
   - ダウンロードした .cer ファイルをダブルクリック

#### 3.2 Provisioning Profile の作成

1. **Apple Developer Portal にアクセス**
2. **Profiles > 「+」ボタン**
3. **Profile タイプを選択**
   - iOS App Development（開発）
   - Ad Hoc（テスト配布）
   - App Store（App Store 配布）
4. **App ID を選択**
5. **証明書を選択**
6. **デバイスを選択**（Development/Ad Hoc の場合）
7. **Profile 名を入力して生成**

#### 3.3 Xcode への適用

**Automatic Signing（推奨: 開発時）**:
```xcconfig
CODE_SIGN_STYLE = Automatic
DEVELOPMENT_TEAM = XXXXXXXXXX
```

**Manual Signing（推奨: リリース時）**:
```xcconfig
CODE_SIGN_STYLE = Manual
DEVELOPMENT_TEAM = XXXXXXXXXX
CODE_SIGN_IDENTITY = Apple Distribution
PROVISIONING_PROFILE_SPECIFIER = MyApp_AppStore
```

### Phase 4: CI/CD 設定

#### 4.1 必要なファイル

- **証明書 (.p12)**: 秘密鍵を含むエクスポートされた証明書
- **Provisioning Profile (.mobileprovision)**: 配布用 Profile
- **Keychain パスワード**: 一時的な Keychain 用

#### 4.2 GitHub Actions での設定例

```yaml
- name: Install Certificates
  env:
    CERTIFICATE_BASE64: ${{ secrets.CERTIFICATE_BASE64 }}
    CERTIFICATE_PASSWORD: ${{ secrets.CERTIFICATE_PASSWORD }}
    KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
  run: |
    # 一時キーチェーン作成
    security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
    security default-keychain -s build.keychain
    security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain

    # 証明書インストール
    echo "$CERTIFICATE_BASE64" | base64 --decode > certificate.p12
    security import certificate.p12 -k build.keychain -P "$CERTIFICATE_PASSWORD" -T /usr/bin/codesign
    security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PASSWORD" build.keychain

- name: Install Provisioning Profile
  env:
    PROVISIONING_PROFILE_BASE64: ${{ secrets.PROVISIONING_PROFILE_BASE64 }}
  run: |
    mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
    echo "$PROVISIONING_PROFILE_BASE64" | base64 --decode > ~/Library/MobileDevice/Provisioning\ Profiles/profile.mobileprovision
```

### Phase 5: 検証

```bash
# 署名の検証
codesign -vvv --deep --strict /path/to/App.app

# Profile の検証
security cms -D -i ~/Library/MobileDevice/Provisioning\ Profiles/profile.mobileprovision | grep -A1 "ExpirationDate"
```

## 出力形式

### 診断レポート

```markdown
## 署名診断レポート

### 証明書ステータス
| 種類 | 名前 | 有効期限 | ステータス |
|------|------|----------|-----------|
| Development | Apple Development: Name | 2025-01-01 | OK |
| Distribution | Apple Distribution: Company | 2024-12-31 | WARNING: 30日以内に期限切れ |

### Provisioning Profile ステータス
| Profile名 | App ID | 種類 | 有効期限 | ステータス |
|-----------|--------|------|----------|-----------|
| MyApp_Dev | com.company.myapp | Development | 2024-06-01 | OK |
| MyApp_AppStore | com.company.myapp | App Store | 2024-03-15 | ERROR: 期限切れ |

### 検出された問題

#### ERROR
- [ ] Distribution Profile が期限切れです
  - 影響: App Store へのアップロードができません
  - 対応: Apple Developer Portal で Profile を再生成してください

#### WARNING
- [ ] Distribution 証明書が 30 日以内に期限切れになります
  - 対応: 証明書の更新を計画してください
```

### 解決手順

```markdown
## 署名問題の解決手順

### 手順 1: 証明書の更新
1. Keychain Access で CSR を作成
2. Apple Developer Portal で証明書を発行
3. 証明書をダウンロードしてインストール

### 手順 2: Profile の再生成
1. Apple Developer Portal > Profiles にアクセス
2. 対象の Profile を編集または新規作成
3. 新しい証明書を選択
4. Profile をダウンロードしてインストール

### 手順 3: Xcode 設定の更新
1. Xcode > Preferences > Accounts で更新
2. プロジェクト設定で新しい Profile を選択
3. ビルドして確認
```

## ガードレール

### 禁止事項
- 証明書の秘密鍵を平文で保存・共有
- 本番用証明書を開発環境に不用意にインストール
- 期限切れ証明書でのアーカイブ作成
- チーム外への証明書・Profile の共有

### 確認必須事項
- 証明書操作前に現在の状態をバックアップ
- p12 ファイルのパスワードは安全に管理
- CI/CD シークレットは暗号化して保存
- 証明書/Profile の有効期限を定期的に確認

### 推奨事項
- 開発時は Automatic Signing を使用
- リリース時は Manual Signing を使用
- 証明書は期限切れ 30 日前に更新
- 不要な証明書・Profile は定期的に整理
- App Store Connect API キーの活用を検討

### セキュリティ考慮事項
- p12 ファイルには強力なパスワードを設定
- CI/CD では一時的な Keychain を使用
- ビルド後は証明書・Keychain を削除
- シークレット管理サービスの活用を検討
