---
name: ci-debug
description: Debug GitHub Actions workflow failures, CI build issues, test failures in CI, and deployment problems. Use when workflows fail, artifacts aren't uploaded, or CI-specific errors occur.
---

# CI/GitHub Actions Debugging Skill

Expert guidance for debugging GitHub Actions workflows, CI build failures, and deployment issues specific to this Flutter Android project.

## When to Use This Skill

- GitHub Actions workflow failures
- CI build errors that don't occur locally
- Test failures only in CI environment
- Artifact upload/download issues
- Secret/credential problems
- Cache-related failures
- Timeout issues
- Deployment failures

## Project Workflows

This project has several workflows:

### 1. build.yml (Main CI)
- Runs on push to main/develop and PRs
- Auto-formats code with `dart format`
- Applies fixes with `dart fix --apply`
- Builds APK and App Bundle
- Runs tests with coverage
- Uses CI-optimized Gradle properties

### 2. release.yml
- Triggered by version tags (v*)
- Builds signed release artifacts
- Creates GitHub Release
- Requires signing secrets

### 3. pre-release.yml
- Manual workflow for beta/alpha releases
- Customizable version naming
- Creates pre-release on GitHub

## Debugging Workflow

### 1. Access Workflow Logs

**Via GitHub UI**:
1. Go to repository → Actions tab
2. Click on failed workflow run
3. Click on failed job
4. Expand failed step to see logs

**Via GitHub CLI** (if available):
```bash
# List recent workflow runs
gh run list --limit 10

# View specific run
gh run view <run-id>

# Download logs
gh run download <run-id>
```

### 2. Common CI Failure Patterns

#### Flutter/Dart Setup Issues

**Error**: Flutter not found or wrong version
```yaml
# Check flutter version in workflow
- name: Setup Flutter
  uses: subosito/flutter-action@v2
  with:
    flutter-version: '3.38.3'  # Verify this matches requirements
    channel: 'stable'
    cache: true
```

**Solution**: 
- Update Flutter version in `.github/workflows/build.yml`
- Ensure version exists on stable channel
- Check for typos in version number

#### Gradle Build Failures

**Error**: Gradle daemon issues or out of memory
```yaml
# Workflow uses CI-optimized properties
- name: Setup Gradle for CI
  run: cp android/gradle-ci.properties android/gradle.properties
```

**Solution**:
- Check `android/gradle-ci.properties` settings
- Verify heap size (3GB for CI)
- Ensure parallel builds limited (2 workers for CI)
- Disable daemon in CI: `org.gradle.daemon=false`

**Error**: Java version mismatch
```yaml
- name: Setup Java
  uses: actions/setup-java@v5
  with:
    distribution: 'temurin'
    java-version: '17'  # Must be 17 for this project
```

**Solution**:
- Verify Java version is 17
- Check all gradle files use Java 17
- Ensure JVM target is set correctly

#### Dependency Issues

**Error**: Package resolution failures
```yaml
- name: Get dependencies
  run: flutter pub get
```

**Solution**:
- Check `pubspec.yaml` for invalid dependencies
- Verify dependency versions exist on pub.dev
- Clear cache if stale (remove cache step temporarily)
- Check for network issues in CI environment

#### Test Failures

**Error**: Tests pass locally but fail in CI
```yaml
- name: Run tests with coverage
  run: flutter test --coverage --concurrency=$(nproc)
```

**Solution**:
- Check for timing issues (use `await` properly)
- Verify file paths are relative, not absolute
- Look for environment-specific dependencies
- Check test runs with same concurrency locally
- Review timezone/locale differences
- Ensure no tests depend on external services

#### Cache Issues

**Error**: Build slower or cache not working
```yaml
- name: Cache Flutter packages
  uses: actions/cache@v4
  with:
    path: |
      ~/.pub-cache
      ${{ github.workspace }}/.dart_tool
    key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
```

**Solution**:
- Verify cache key is correct
- Check cache paths exist
- Clear cache by changing cache key
- Review cache size limits (10GB per repo)

#### Artifact Upload Issues

**Error**: Artifacts not found or upload fails
```yaml
- name: Upload APK
  uses: actions/upload-artifact@v5
  with:
    name: android-apk
    path: build/app/outputs/flutter-apk/app-release.apk
    retention-days: 7
```

**Solution**:
- Verify build actually succeeded
- Check file path is correct
- Ensure build step completed
- Look for build output location changes

### 3. Debugging Specific Workflow Steps

#### Auto-format and Commit Step

**Error**: Permission denied or merge conflicts
```yaml
- name: Commit formatting changes
  if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.full_name == github.repository
  run: |
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    git add .
    if git diff --staged --quiet; then
      echo "No formatting changes to commit"
    else
      git commit -m "style: auto-format code [skip ci]"
      git push
    fi
```

**Solution**:
- Check `GITHUB_TOKEN` has write permissions
- Verify checkout uses correct ref
- Ensure condition matches PR from same repo
- Review branch protection rules

#### Coverage Upload

**Error**: Codecov upload fails
```yaml
- name: Upload Coverage
  uses: codecov/codecov-action@v5
  if: always()
  with:
    files: coverage/lcov.info
    fail_ci_if_error: false
    token: ${{ secrets.CODECOV_TOKEN }}
```

**Solution**:
- Check `coverage/lcov.info` exists
- Verify `CODECOV_TOKEN` secret is set
- Use `fail_ci_if_error: false` to not block CI
- Check Codecov service status

### 4. Release Workflow Issues

#### Missing Secrets

**Error**: Build signing fails
```yaml
# Required secrets for release.yml:
# - ANDROID_KEYSTORE_BASE64
# - ANDROID_KEYSTORE_PASSWORD
# - ANDROID_KEY_ALIAS
# - ANDROID_KEY_PASSWORD
```

**Solution**:
1. Generate keystore (see `SIGNING.md`)
2. Base64 encode: `base64 -i keystore.jks -o keystore.txt`
3. Add secrets in Settings → Secrets → Actions
4. Verify secret names match workflow

#### Tag Trigger Issues

**Error**: Release workflow doesn't trigger
```yaml
on:
  push:
    tags:
      - 'v*'  # Must start with 'v'
```

**Solution**:
- Ensure tag starts with 'v' (e.g., v1.0.0)
- Push tag: `git tag v1.0.0 && git push origin v1.0.0`
- Check workflow is enabled
- Verify branch has tag

### 5. Timeout Issues

**Error**: Workflow times out
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 30  # build.yml timeout
```

**Solution**:
- Increase timeout if builds legitimately take longer
- Check for hanging processes
- Review Gradle performance settings
- Ensure no infinite loops in tests
- Check for network timeouts

### 6. Concurrency Issues

**Error**: Multiple runs conflict
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

**Solution**:
- This cancels duplicate runs automatically
- If issues persist, check for race conditions
- Review if multiple workflows modify same files

## Quick CI Debug Checklist

- [ ] Check workflow logs in GitHub Actions tab
- [ ] Verify Flutter version matches project requirements
- [ ] Confirm Java version is 17
- [ ] Review gradle-ci.properties settings
- [ ] Check all required secrets are set
- [ ] Verify dependency versions in pubspec.yaml
- [ ] Test same commands locally
- [ ] Review cache configuration
- [ ] Check artifact paths
- [ ] Verify branch protection rules allow bot commits
- [ ] Ensure workflows are enabled
- [ ] Check runner OS matches expectations (ubuntu-latest)

## Local CI Simulation

To reproduce CI environment locally:

```bash
# Use CI Gradle properties
cp android/gradle-ci.properties android/gradle.properties

# Clean build
flutter clean
flutter pub get

# Format and fix
dart format .
dart fix --apply

# Analyze
flutter analyze

# Test with coverage
flutter test --coverage --concurrency=$(nproc)

# Build
flutter build apk --release
flutter build appbundle --release

# Restore local properties
git checkout android/gradle.properties
```

## Common Error Messages and Solutions

| Error Message | Likely Cause | Solution |
|--------------|--------------|----------|
| "Flutter SDK not found" | Setup issue | Check flutter-action version and config |
| "Gradle build failed" | Memory/config | Review gradle-ci.properties |
| "Test failed" | Environment diff | Check for timing issues, paths |
| "Permission denied" | Token permissions | Add write permission to workflow |
| "Artifact not found" | Build didn't complete | Check build step succeeded |
| "Secret not found" | Missing secret | Add in repository settings |
| "Timeout" | Takes too long | Increase timeout or optimize build |
| "Cache restore failed" | Key mismatch | Update cache key |

## Best Practices

1. **Always test locally first**: Run same commands as CI
2. **Use verbose logging**: Add `--verbose` to debug commands
3. **Check all secrets**: Verify secrets exist and are correct
4. **Monitor cache usage**: Clear cache if builds become inconsistent
5. **Keep workflows simple**: Complex workflows are harder to debug
6. **Use conditional steps**: `if: always()` for critical diagnostics
7. **Set appropriate timeouts**: Balance between too short and too long
8. **Document workflow changes**: Add comments explaining why
9. **Test on clean branch**: Ensure no local state affects CI
10. **Review workflow on successful runs**: Understand what works

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Flutter CI/CD Guide](https://docs.flutter.dev/deployment/cd)
- [Gradle Build Performance](https://docs.gradle.org/current/userguide/performance.html)
- Project-specific: `BUILD_OPTIMIZATION.md`, `SIGNING.md`
