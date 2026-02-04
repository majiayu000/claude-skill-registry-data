---
name: NativePHP Deployment
description: This skill should be used when the user asks about "deploy nativephp", "build ios app", "build android app", "app store submission", "play store submission", "native:package", "native:release", "sign android app", "sign ios app", "create ipa", "create aab", "create apk", "upload to app store", "release build", or needs to package and deploy their NativePHP Mobile application.
version: 0.1.0
---

# NativePHP Deployment

This skill provides guidance for building, signing, packaging, and deploying NativePHP Mobile applications to the App Store and Play Store.

## Deployment Overview

The deployment process involves:
1. Creating a release build
2. Testing on real devices
3. Signing and packaging
4. Submitting for review
5. Publishing to stores

## Pre-Deployment Checklist

Before packaging:

- [ ] Set production version in `.env`:
  ```env
  NATIVEPHP_APP_VERSION=1.0.0
  NATIVEPHP_APP_VERSION_CODE=1
  ```
- [ ] Configure all required permissions in `config/nativephp.php`
- [ ] Remove debug code and test data
- [ ] Test on physical devices
- [ ] Prepare app store assets (icons, screenshots, descriptions)

## Release Build

Create an optimized release build:

```bash
php artisan native:run ios --build=release
php artisan native:run android --build=release
```

This removes debugging code and optimizes the application. Always test release builds on physical devices before submission.

## Android Deployment

### Generate Signing Credentials

Create keystore automatically:

```bash
php artisan native:credentials android
```

This generates:
- Keystore file (`.keystore`)
- Keystore password
- Key alias
- Key password

**Store these credentials securely** - they're required for all future updates.

### Build APK (Direct Distribution)

```bash
php artisan native:package android \
  --keystore=/path/to/my-app.keystore \
  --keystore-password=your_password \
  --key-alias=my-app-key \
  --key-password=your_key_password
```

Output: `nativephp/android/app/build/outputs/apk/release/app-release.apk`

### Build AAB (Play Store)

```bash
php artisan native:package android \
  --build-type=bundle \
  --keystore=/path/to/my-app.keystore \
  --keystore-password=your_password \
  --key-alias=my-app-key \
  --key-password=your_key_password
```

Output: `nativephp/android/app/build/outputs/bundle/release/app-release.aab`

### Upload to Play Store

Direct upload with Google Service Account:

```bash
php artisan native:package android \
  --build-type=bundle \
  --keystore=/path/to/my-app.keystore \
  --keystore-password=your_password \
  --key-alias=my-app-key \
  --key-password=your_key_password \
  --upload-to-play-store \
  --play-store-track=internal  # or alpha, beta, production
```

### Auto-Increment Version

With Google Service Account credentials configured, automatically increment build number:

```bash
php artisan native:package android \
  --build-type=bundle \
  [signing options] \
  --upload-to-play-store
```

Skip ahead in version numbering:

```bash
php artisan native:package android --jump-by=10
```

## iOS Deployment

### Required Credentials

Gather these before packaging:

1. **App Store Connect API Key** (`.p8` file) - Generate at App Store Connect > Users and Access > Keys
2. **API Key ID** - Shown when creating the key
3. **Issuer ID** - Found in Users and Access > Keys
4. **Distribution Certificate** (`.p12` or `.cer`) - From Xcode or Apple Developer portal
5. **Certificate Password** - Password for the .p12 file
6. **Provisioning Profile** (`.mobileprovision`) - Match your app ID and certificate
7. **Team ID** - Your Apple Developer Team ID

### Export Methods

| Method | Use Case |
|--------|----------|
| `app-store` | Production App Store submission (default) |
| `ad-hoc` | Distribute to specific registered devices |
| `enterprise` | Enterprise-only distribution |
| `development` | Testing on personal devices |

### Build for App Store

```bash
php artisan native:package ios \
  --export-method=app-store \
  --api-key=/path/to/AuthKey.p8 \
  --api-key-id=KEYID123 \
  --api-issuer-id=issuer-uuid \
  --certificate=/path/to/distribution.p12 \
  --certificate-password=cert_password \
  --provisioning-profile=/path/to/profile.mobileprovision \
  --team-id=ABC123XYZ \
  --upload-to-app-store
```

### Build Ad-Hoc (TestFlight Alternative)

```bash
php artisan native:package ios \
  --export-method=ad-hoc \
  --certificate=/path/to/distribution.p12 \
  --certificate-password=cert_password \
  --provisioning-profile=/path/to/adhoc.mobileprovision \
  --team-id=ABC123XYZ
```

### Build for Development

```bash
php artisan native:package ios \
  --export-method=development \
  --certificate=/path/to/development.p12 \
  --certificate-password=cert_password \
  --provisioning-profile=/path/to/dev.mobileprovision \
  --team-id=ABC123XYZ
```

### iOS-Specific Options

```bash
# Validate provisioning profile and entitlements
php artisan native:package ios --validate-profile

# Clear Xcode and SPM caches
php artisan native:package ios --clean-caches

# Force complete rebuild
php artisan native:package ios --rebuild

# Validate without creating IPA
php artisan native:package ios --validate-only
```

## Using Environment Variables

Store credentials in `.env` to avoid command-line exposure:

```env
# Android
ANDROID_KEYSTORE=/path/to/keystore
ANDROID_KEYSTORE_PASSWORD=password
ANDROID_KEY_ALIAS=alias
ANDROID_KEY_PASSWORD=password

# iOS
IOS_API_KEY=/path/to/AuthKey.p8
IOS_API_KEY_ID=KEYID123
IOS_API_ISSUER_ID=issuer-uuid
IOS_CERTIFICATE=/path/to/certificate.p12
IOS_CERTIFICATE_PASSWORD=password
IOS_PROVISIONING_PROFILE=/path/to/profile.mobileprovision
IOS_TEAM_ID=ABC123XYZ
```

Then reference in commands or configure in `config/nativephp.php`.

## CI/CD Integration

For automated pipelines:

```bash
# Disable TTY for non-interactive environments
php artisan native:package android --no-tty [options]
php artisan native:package ios --no-tty [options]
```

### GitHub Actions Example

```yaml
- name: Build Android
  run: |
    php artisan native:package android \
      --build-type=bundle \
      --keystore=${{ secrets.ANDROID_KEYSTORE }} \
      --keystore-password=${{ secrets.ANDROID_KEYSTORE_PASSWORD }} \
      --key-alias=${{ secrets.ANDROID_KEY_ALIAS }} \
      --key-password=${{ secrets.ANDROID_KEY_PASSWORD }} \
      --no-tty
```

## Version Management

### Setting Versions

```env
# Semantic version displayed to users
NATIVEPHP_APP_VERSION=1.2.3

# Integer that must increment for each store upload
NATIVEPHP_APP_VERSION_CODE=48
```

### Version Rules

- **App Store**: Build number must be higher than any previous upload
- **Play Store**: Version code must be strictly higher than current published version
- Both stores reject duplicate version numbers

## Output Locations

| Platform | Type | Location |
|----------|------|----------|
| Android | APK | `nativephp/android/app/build/outputs/apk/release/app-release.apk` |
| Android | AAB | `nativephp/android/app/build/outputs/bundle/release/app-release.aab` |
| iOS | IPA | Xcode's build output directory |

## Troubleshooting

### Android: Keystore Issues

```bash
# Verify keystore
keytool -list -v -keystore /path/to/keystore
```

### iOS: Provisioning Profile Mismatch

Ensure:
- Profile matches your App ID exactly
- Profile includes your distribution certificate
- Profile is not expired

### Build Failures

```bash
# Clean and rebuild
php artisan native:package [platform] --clean-caches --rebuild
```

## Post-Deployment

### App Store Connect

1. Upload build via Xcode or Transporter
2. Complete app metadata
3. Submit for review
4. Monitor review status

### Google Play Console

1. Upload AAB in Production/Testing track
2. Complete store listing
3. Submit for review
4. Staged rollout recommended

## Fetching Live Documentation

For detailed deployment documentation:

- **Deployment**: `https://nativephp.com/docs/mobile/2/getting-started/deployment`

Use WebFetch to retrieve the latest deployment procedures and options.
