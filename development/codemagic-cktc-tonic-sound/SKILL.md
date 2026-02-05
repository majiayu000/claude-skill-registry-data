---
name: codemagic
description: Comprehensive guide for creating, configuring, and troubleshooting codemagic.yaml files for CI/CD workflows. Use when building mobile apps (Flutter, iOS, Android, React Native) with Codemagic, setting up build pipelines, configuring environment variables, implementing code signing, managing artifacts, or debugging workflow issues.
---

# Codemagic CI/CD Configuration

Configure Codemagic CI/CD workflows using codemagic.yaml for mobile app builds.

## File Location

Place `codemagic.yaml` in the root directory of your repository. Codemagic automatically detects and uses this file for build configuration.

## Core Workflow Structure

Each workflow in codemagic.yaml defines a complete build pipeline:

```yaml
workflows:
  workflow-id:
    name: Workflow Name
    instance_type: mac_mini_m2  # mac_mini_m2, linux, linux_x2, windows_x2
    max_build_duration: 60      # minutes (1-120)
    environment:
      # Environment configuration
    triggering:
      # Build triggers
    scripts:
      # Build steps
    artifacts:
      # Output files
    publishing:
      # Publishing destinations
```

## Environment Configuration

### Version Management

Specify tool versions in the `environment` section:

```yaml
environment:
  flutter: stable              # stable, beta, master, or version (e.g., 3.7.6)
  xcode: latest               # latest, edge, or version (e.g., 14.3)
  cocoapods: default          # default or version
  node: 18.0.0               # version
  java: 11                    # version
  ruby: 2.7.2                # version
```

For Flutter Version Management (FVM), set:
```yaml
environment:
  flutter: fvm
```

### Environment Variables

Define variables at three levels with precedence (highest to lowest):

1. **Workflow-specific variables**:
```yaml
environment:
  vars:
    PUBLIC_VAR: "value"
    API_ENDPOINT: "https://api.example.com"
```

2. **Variable groups** (from Codemagic UI):
```yaml
environment:
  groups:
    - app_store_credentials
    - firebase_credentials
    - keystore_credentials
```

3. **Built-in variables** - Codemagic exports these automatically:
   - `$CM_BUILD_ID` - Unique build identifier
   - `$CM_PROJECT_ID` - Project ID
   - `$CM_BRANCH` - Git branch name
   - `$CM_TAG` - Git tag (if applicable)
   - `$CM_COMMIT` - Git commit hash
   - `$CM_PULL_REQUEST` - PR number (true/false)
   - `$CM_REPO_SLUG` - Repository slug
   - `$CM_BUILD_DIR` - Build directory path
   - `$CM_ARTIFACT_LINKS` - JSON array of artifact URLs

See [references/built-in-vars.md](references/built-in-vars.md) for complete list.

### Sharing Variables Between Scripts

Variables defined in scripts are scoped to that script only. To share variables, write to `$CM_ENV`:

**macOS/Linux:**
```yaml
scripts:
  - name: Set variable
    script: |
      echo "MY_VAR=value" >> $CM_ENV
  - name: Use variable
    script: |
      echo "Using $MY_VAR"
```

**Windows:**
```yaml
scripts:
  - name: Set variable
    script: |
      Add-Content -Path $env:CM_ENV -Value "MY_VAR=value"
```

### Caching

Cache dependencies to speed up builds:

```yaml
environment:
  cache:
    cache_paths:
      - ~/.gradle/caches
      - ~/.pub-cache
      - $HOME/Library/Caches/CocoaPods
```

**Important:** Each workflow has its own cache. Caching symlinks is not supported.

## Build Triggers

Define when builds start automatically in the `triggering` section:

```yaml
triggering:
  events:
    - push                    # Commits to tracked branches
    - pull_request           # Pull request opened/updated
    - tag                    # Tag created
    - pull_request_labeled   # Label added to PR
```

**Note:** Automatic triggering requires webhook configuration in your repository.

### Branch/Tag Patterns

Limit triggers to specific branches or tags:

```yaml
triggering:
  events:
    - push
  branch_patterns:
    - pattern: 'main'
      include: true
    - pattern: 'develop'
      include: true
    - pattern: 'feature/*'
      include: true
    - pattern: 'hotfix/*'
      include: true
  tag_patterns:
    - pattern: 'v*.*.*'
      include: true
```

### Conditional Triggering

Skip builds based on changed files or custom conditions:

**Changeset filtering:**
```yaml
triggering:
  events:
    - push
  when:
    changeset:
      includes:
        - '.'                 # All files
      excludes:
        - '**/*.md'          # Skip markdown-only changes
        - 'docs/**'          # Skip docs changes
```

**Custom conditions:**
```yaml
triggering:
  events:
    - pull_request
  when:
    condition: not event.pull_request.draft  # Skip draft PRs
```

**Using environment variables:**
```yaml
when:
  condition: env.CM_BRANCH == "main"
```

**Complex conditions:**
```yaml
when:
  condition: |
    env.CM_BRANCH == "main" and 
    not event.pull_request.draft
```

### Cancel Previous Builds

Automatically cancel outdated builds:

```yaml
triggering:
  cancel_previous_builds: true
```

## Scripts

The `scripts` section defines build steps:

### Basic Script Formats

**Single-line:**
```yaml
scripts:
  - echo "Hello world"
```

**Named script:**
```yaml
scripts:
  - name: Run tests
    script: flutter test
```

**Multi-line:**
```yaml
scripts:
  - name: Build iOS
    script: |
      flutter build ios --release
      cd ios
      xcodebuild -archive
```

**Python/other languages:**
```yaml
scripts:
  - |
    #!/usr/bin/env python3
    import os
    print("Running Python script")
```

### Script Options

**Ignore failures:**
```yaml
scripts:
  - name: Optional step
    script: flutter test
    ignore_failure: true  # Workflow continues even if this fails
```

**Conditional execution:**
```yaml
scripts:
  - name: Deploy to production
    script: ./deploy.sh
    when:
      condition: env.CM_BRANCH == "main"
```

**Changeset-based execution:**
```yaml
scripts:
  - name: Build Android
    script: ./gradlew assembleRelease
    when:
      changeset:
        includes:
          - 'android/**'
```

### Working Directory

Set working directory globally or per-script:

**Workflow-level:**
```yaml
workflows:
  my-workflow:
    working_directory: packages/my_app
```

**Script-level:**
```yaml
scripts:
  - name: Build in subdirectory
    working_directory: ios
    script: xcodebuild
```

**Important:** Using `cd` between scripts doesn't work because each script runs in a subshell. Use `working_directory` or inline `cd` within a single script.

## Code Signing

See [references/code-signing.md](references/code-signing.md) for complete iOS and Android code signing workflows.

## Artifacts

Specify files to save after the build:

```yaml
artifacts:
  - build/ios/ipa/*.ipa
  - build/app/outputs/flutter-apk/*.apk
  - build/**/*.aab
  - $HOME/Library/Developer/Xcode/DerivedData/**/Build/**/*.dSYM
```

Paths can be relative (to clone directory) or absolute. Use glob patterns for flexibility.

## Publishing

Configure where to publish build artifacts:

### Email

```yaml
publishing:
  email:
    recipients:
      - user@example.com
      - team@example.com
    notify:
      success: true
      failure: true
```

### Slack

```yaml
publishing:
  slack:
    channel: '#builds'
    notify_on_build_start: true
    notify:
      success: true
      failure: true
```

### App Store Connect

```yaml
publishing:
  app_store_connect:
    api_key: $APP_STORE_CONNECT_PRIVATE_KEY
    key_id: $APP_STORE_CONNECT_KEY_IDENTIFIER
    issuer_id: $APP_STORE_CONNECT_ISSUER_ID
    submit_to_testflight: true
```

### Google Play

```yaml
publishing:
  google_play:
    credentials: $GCLOUD_SERVICE_ACCOUNT_CREDENTIALS
    track: internal  # internal, alpha, beta, production
    submit_as_draft: false
```

### Firebase App Distribution

```yaml
publishing:
  firebase:
    firebase_token: $FIREBASE_TOKEN
    android:
      app_id: $FIREBASE_ANDROID_APP_ID
      groups:
        - testers
    ios:
      app_id: $FIREBASE_IOS_APP_ID
      groups:
        - testers
```

### Custom Publishing Scripts

```yaml
publishing:
  scripts:
    - name: Custom deployment
      script: |
        if [ -f "build/app.ipa" ]; then
          ./deploy.sh build/app.ipa
        fi
```

## Advanced Features

### YAML Anchors for Reusability

Define reusable sections with `&anchor` and reference with `*anchor`:

```yaml
definitions:
  instance_mac: &instance_mac
    instance_type: mac_mini_m2
    max_build_duration: 120
  
  flutter_env: &flutter_env
    flutter: stable
    xcode: latest
    cocoapods: default
  
  setup_script: &setup_script
    name: Setup
    script: |
      flutter pub get
      pod install

workflows:
  ios-release:
    name: iOS Release
    <<: *instance_mac
    environment:
      <<: *flutter_env
    scripts:
      - *setup_script
      - name: Build
        script: flutter build ios
  
  android-release:
    name: Android Release
    instance_type: linux
    environment:
      <<: *flutter_env
    scripts:
      - *setup_script
      - name: Build
        script: flutter build apk
```

### Build Inputs

Allow runtime parameters for flexible builds:

```yaml
workflows:
  flexible-build:
    name: Flexible Build
    build_inputs:
      - name: build_flavor
        type: choice
        description: Select build flavor
        required: true
        choices:
          - dev
          - staging
          - production
      - name: run_tests
        type: boolean
        description: Run tests before build
        default: true
    scripts:
      - name: Build with flavor
        script: |
          flutter build apk --flavor $build_flavor
```

### Labels

Add labels for workflow organization:

```yaml
workflows:
  my-workflow:
    name: My Workflow
    labels:
      - QA
      - ${TENANT_NAME}
      - v${APP_VERSION}
```

## Common Patterns

### Flutter Workflow Template

```yaml
workflows:
  flutter-workflow:
    name: Flutter Build
    instance_type: mac_mini_m2
    max_build_duration: 60
    environment:
      flutter: stable
      xcode: latest
      groups:
        - app_store_credentials
      vars:
        BUNDLE_ID: "com.example.app"
    triggering:
      events:
        - push
      branch_patterns:
        - pattern: 'main'
          include: true
    scripts:
      - name: Get dependencies
        script: flutter pub get
      - name: Run tests
        script: flutter test
      - name: Build iOS
        script: flutter build ipa --release
      - name: Build Android
        script: flutter build apk --release
    artifacts:
      - build/ios/ipa/*.ipa
      - build/app/outputs/flutter-apk/*.apk
    publishing:
      email:
        recipients:
          - team@example.com
```

### iOS Native Workflow

See [references/ios-workflow.md](references/ios-workflow.md)

### Android Native Workflow

See [references/android-workflow.md](references/android-workflow.md)

### Monorepo Setup

See [references/monorepo.md](references/monorepo.md)

## Validation and Testing

### Schema Validation

Use JSON schema for IDE validation:
```yaml
# yaml-language-server: $schema=https://codemagic.io/codemagic-schema.json
```

### Local Validation

Check for common issues:
- YAML syntax errors
- Missing required fields
- Invalid instance types
- Incorrect environment variable references

### Debugging

Add debug script to inspect environment:

```yaml
scripts:
  - name: Debug environment
    script: |
      set -ex
      printenv
      flutter --version
      xcodebuild -version
```

## Troubleshooting

**Build not triggering:**
- Verify webhook configuration
- Check branch/tag patterns match
- Review changeset filters
- Ensure codemagic.yaml is in root directory
- Check if [skip ci] is in commit message

**Environment variable not found:**
- Verify variable group names match UI
- Check variable name spelling
- Ensure secret variables are marked as such
- Use `printenv` to list available variables

**Scripts failing:**
- Check exit codes with `set -e`
- Review logs for error messages
- Verify tool versions are correct
- Test scripts locally first

**Code signing issues:**
- Verify certificates are uploaded to Codemagic
- Check provisioning profile validity
- Ensure bundle IDs match
- Review code signing identity references

**Cache not working:**
- Verify cache paths exist
- Check cache size limits
- Ensure paths are not symlinks
- Review cache age (expires after 7 days of inactivity)

## Best Practices

1. **Use variable groups** for sensitive data instead of hardcoding
2. **Enable cancel_previous_builds** to save build minutes
3. **Use changeset filtering** for monorepos to avoid unnecessary builds
4. **Cache dependencies** to speed up builds
5. **Use YAML anchors** to reduce duplication
6. **Add conditional steps** to optimize workflow execution
7. **Test locally** before committing changes
8. **Use semantic versioning** for tags
9. **Keep scripts focused** - one responsibility per script
10. **Document complex workflows** with inline comments
