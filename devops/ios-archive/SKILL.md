---
name: ios-archive
description: |
  アーカイブ・配布支援。App Store Connect、TestFlight、Ad Hoc/Enterprise配布。
  使用タイミング: (1) App Storeへの提出準備時、(2) TestFlight配布時、
  (3) Ad Hoc/Enterprise配布時、(4) CI/CDでの自動配布設定時
---

# iOS アーカイブ・配布支援スキル

iOSアプリのアーカイブ作成から各種配布方法までをガイドする。

## 配布方法の選択

| 方法 | 用途 | 証明書 | プロビジョニング |
|------|------|--------|-----------------|
| App Store | 一般公開 | Distribution | App Store |
| TestFlight | ベータテスト | Distribution | App Store |
| Ad Hoc | 限定配布（100台） | Distribution | Ad Hoc |
| Enterprise | 社内配布 | Enterprise | In-House |
| Development | 開発・デバッグ | Development | Development |

## アーカイブ作成

### Xcodeでのアーカイブ

1. **スキーム設定確認**
   - Product > Scheme > Edit Scheme
   - Archive の Build Configuration を Release に設定

2. **アーカイブ実行**
   - Product > Archive
   - または ⇧⌘B でビルド後、Product > Archive

### xcodebuildでのアーカイブ

```bash
# 基本的なアーカイブ
xcodebuild archive \
  -project MyApp.xcodeproj \
  -scheme MyApp \
  -archivePath ./build/MyApp.xcarchive

# ワークスペースの場合
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -archivePath ./build/MyApp.xcarchive \
  -destination 'generic/platform=iOS'

# 設定を指定
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath ./build/MyApp.xcarchive \
  CODE_SIGN_STYLE=Manual \
  DEVELOPMENT_TEAM=XXXXXXXXXX \
  PROVISIONING_PROFILE_SPECIFIER="MyApp Distribution"
```

## エクスポート

### ExportOptions.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- App Store配布 -->
    <key>method</key>
    <string>app-store</string>
    
    <!-- または TestFlight -->
    <!-- <string>app-store</string> -->
    
    <!-- Ad Hoc配布 -->
    <!-- <string>ad-hoc</string> -->
    
    <!-- Enterprise配布 -->
    <!-- <string>enterprise</string> -->
    
    <!-- Development -->
    <!-- <string>development</string> -->
    
    <key>teamID</key>
    <string>XXXXXXXXXX</string>
    
    <key>uploadSymbols</key>
    <true/>
    
    <key>uploadBitcode</key>
    <false/>
    
    <!-- 署名設定 -->
    <key>signingStyle</key>
    <string>manual</string>
    
    <key>provisioningProfiles</key>
    <dict>
        <key>com.example.myapp</key>
        <string>MyApp Distribution Profile</string>
    </dict>
</dict>
</plist>
```

### xcodebuildでのエクスポート

```bash
# IPAのエクスポート
xcodebuild -exportArchive \
  -archivePath ./build/MyApp.xcarchive \
  -exportPath ./build/export \
  -exportOptionsPlist ExportOptions.plist
```

## App Store Connect

### アップロード方法

#### 1. Xcode Organizer
```
1. Window > Organizer を開く
2. アーカイブを選択
3. Distribute App をクリック
4. App Store Connect を選択
5. Upload を選択
6. 指示に従って完了
```

#### 2. altool（非推奨、xcrun notarytool推奨）
```bash
# 検証
xcrun altool --validate-app \
  -f MyApp.ipa \
  -t ios \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID

# アップロード
xcrun altool --upload-app \
  -f MyApp.ipa \
  -t ios \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

#### 3. xcrun notarytool / App Store Connect API
```bash
# App Store Connect APIキーを使用
xcrun notarytool submit MyApp.ipa \
  --key AuthKey_XXXXXXXXXX.p8 \
  --key-id XXXXXXXXXX \
  --issuer XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX \
  --wait
```

### バージョン管理

```bash
# バージョン番号更新（CFBundleShortVersionString）
/usr/libexec/PlistBuddy -c "Set :CFBundleShortVersionString 1.2.0" Info.plist

# ビルド番号更新（CFBundleVersion）
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion 42" Info.plist

# agvtoolを使用（推奨）
# バージョン設定
agvtool new-marketing-version 1.2.0

# ビルド番号インクリメント
agvtool next-version -all

# 特定のビルド番号を設定
agvtool new-version -all 42
```

## TestFlight

### 内部テスター
- App Store Connectのユーザー（最大100人）
- ビルドアップロード後すぐにテスト可能
- App Review不要

### 外部テスター
- メールで招待（最大10,000人）
- 最初のビルドはApp Review必要
- Public Linkで配布可能

### テストノート
```
What to Test:
- New feature: Dark mode support
- Bug fix: Login screen crash on iOS 15

Known Issues:
- Settings page may show placeholder text
- Push notifications not working in simulator
```

## Ad Hoc配布

### UDIDの収集
```bash
# デバイスのUDID取得
system_profiler SPUSBDataType | grep -A 11 "iPhone\|iPad"

# または Finder/iTunes で確認
```

### OTA配布用manifest.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>items</key>
    <array>
        <dict>
            <key>assets</key>
            <array>
                <dict>
                    <key>kind</key>
                    <string>software-package</string>
                    <key>url</key>
                    <string>https://example.com/apps/MyApp.ipa</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>display-image</string>
                    <key>url</key>
                    <string>https://example.com/apps/icon-57.png</string>
                </dict>
                <dict>
                    <key>kind</key>
                    <string>full-size-image</string>
                    <key>url</key>
                    <string>https://example.com/apps/icon-512.png</string>
                </dict>
            </array>
            <key>metadata</key>
            <dict>
                <key>bundle-identifier</key>
                <string>com.example.myapp</string>
                <key>bundle-version</key>
                <string>1.0.0</string>
                <key>kind</key>
                <string>software</string>
                <key>title</key>
                <string>My App</string>
            </dict>
        </dict>
    </array>
</dict>
</plist>
```

### インストールリンク
```html
<a href="itms-services://?action=download-manifest&url=https://example.com/apps/manifest.plist">
  Install App
</a>
```

## CI/CD自動化

### GitHub Actions例

```yaml
name: Build and Deploy

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: macos-14
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app
      
      - name: Install certificates
        env:
          CERTIFICATE_BASE64: ${{ secrets.CERTIFICATE_BASE64 }}
          CERTIFICATE_PASSWORD: ${{ secrets.CERTIFICATE_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          # キーチェーン作成
          security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          
          # 証明書インポート
          echo "$CERTIFICATE_BASE64" | base64 --decode > certificate.p12
          security import certificate.p12 -k build.keychain \
            -P "$CERTIFICATE_PASSWORD" -T /usr/bin/codesign
          
          security set-key-partition-list -S apple-tool:,apple: \
            -s -k "$KEYCHAIN_PASSWORD" build.keychain
      
      - name: Install provisioning profile
        env:
          PROVISIONING_PROFILE_BASE64: ${{ secrets.PROVISIONING_PROFILE_BASE64 }}
        run: |
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          echo "$PROVISIONING_PROFILE_BASE64" | base64 --decode \
            > ~/Library/MobileDevice/Provisioning\ Profiles/profile.mobileprovision
      
      - name: Build and archive
        run: |
          xcodebuild archive \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -archivePath ./build/MyApp.xcarchive \
            -destination 'generic/platform=iOS'
      
      - name: Export IPA
        run: |
          xcodebuild -exportArchive \
            -archivePath ./build/MyApp.xcarchive \
            -exportPath ./build/export \
            -exportOptionsPlist ExportOptions.plist
      
      - name: Upload to App Store Connect
        env:
          APP_STORE_CONNECT_API_KEY: ${{ secrets.APP_STORE_CONNECT_API_KEY }}
          APP_STORE_CONNECT_ISSUER_ID: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
          APP_STORE_CONNECT_KEY_ID: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
        run: |
          echo "$APP_STORE_CONNECT_API_KEY" > AuthKey.p8
          xcrun altool --upload-app \
            -f ./build/export/MyApp.ipa \
            -t ios \
            --apiKey $APP_STORE_CONNECT_KEY_ID \
            --apiIssuer $APP_STORE_CONNECT_ISSUER_ID
```

### Fastlane連携

```ruby
# Fastfile
default_platform(:ios)

platform :ios do
  desc "Upload to TestFlight"
  lane :beta do
    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store"
    )
    
    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )
  end
  
  desc "Release to App Store"
  lane :release do
    build_app(
      workspace: "MyApp.xcworkspace",
      scheme: "MyApp",
      export_method: "app-store"
    )
    
    upload_to_app_store(
      skip_screenshots: true,
      skip_metadata: true
    )
  end
end
```

## トラブルシューティング

### よくあるエラー

| エラー | 原因 | 解決策 |
|--------|------|--------|
| Invalid Signature | 署名の不一致 | Provisioning Profileを再確認 |
| Missing Compliance | 暗号化申告未設定 | Info.plistに ITSAppUsesNonExemptEncryption を追加 |
| Invalid Binary | アーキテクチャ問題 | シミュレータ用コードの除外を確認 |
| Bundle ID Mismatch | Bundle ID不一致 | プロジェクト設定とプロファイルを確認 |

### デバッグ

```bash
# IPAの内容確認
unzip -l MyApp.ipa

# 署名情報確認
codesign -dv --verbose=4 MyApp.app

# Provisioning Profile確認
security cms -D -i embedded.mobileprovision

# App Store Connect API接続テスト
xcrun altool --list-apps \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID
```

## チェックリスト

### App Store提出前
- [ ] バージョン番号とビルド番号を更新
- [ ] Release設定でビルド
- [ ] App Store用のスクリーンショット準備
- [ ] プライバシーポリシーURL設定
- [ ] 暗号化申告（ITSAppUsesNonExemptEncryption）
- [ ] App Review用のテストアカウント準備

### TestFlight配布前
- [ ] What to Testの記載
- [ ] 既知の問題の記載
- [ ] 外部テスターの場合はレビュー対応

### Ad Hoc配布前
- [ ] 対象デバイスのUDID登録
- [ ] HTTPS環境でのmanifest.plistホスティング
- [ ] インストールリンクの動作確認
