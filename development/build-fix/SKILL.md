---
name: build-fix
description: Diagnose and fix Flutter build failures, including dependency conflicts, Gradle errors, compilation issues, and platform-specific build problems. Use when builds fail locally or in CI.
---

# Build Failure Diagnosis and Fix Skill

Expert guidance for diagnosing and fixing Flutter build failures in Android projects, including dependency conflicts, Gradle errors, and compilation issues.

## When to Use This Skill

- Flutter build fails (`flutter build apk` or `flutter build appbundle`)
- Gradle sync/build errors
- Dependency resolution failures
- Compilation errors (Dart or Kotlin/Java)
- Native build failures
- Plugin integration issues
- Version conflicts

## Build Failure Diagnostic Workflow

### Step 1: Identify the Build Stage

Flutter Android builds go through several stages:

1. **Dependency Resolution** (`flutter pub get`)
2. **Dart Compilation** (`flutter build`)
3. **Gradle Configuration** (Android build system setup)
4. **Resource Processing** (R8, ProGuard, resources)
5. **Native Compilation** (Kotlin/Java code)
6. **Packaging** (APK/AAB creation)

Identify which stage is failing to narrow down the issue.

### Step 2: Clean Build First

**Always try a clean build first**:

```bash
# Nuclear option - clean everything
flutter clean
cd android
./gradlew clean
cd ..
rm -rf ~/.gradle/caches  # Only if really stuck
flutter pub get
flutter build apk --verbose
```

### Step 3: Analyze Error Messages

Look for key error patterns:
- **Gradle**: "BUILD FAILED", "Could not resolve", "Deprecated"
- **Dart**: "Error:", "Warning:", "Unhandled exception"
- **R8/ProGuard**: "shrinking", "Missing class"
- **Dependencies**: "version conflict", "incompatible"

## Common Build Failures and Solutions

### 1. Dependency Conflicts

#### Issue: Version Conflicts
```
Error: Version conflict between dependencies
```

**Diagnosis**:
```bash
cd android
./gradlew app:dependencies
```

**Solution**:
- Review `pubspec.yaml` - update conflicting dependencies
- Check `android/app/build.gradle.kts` for Android dependency versions
- Use version ranges carefully: `^1.0.0` vs `>=1.0.0 <2.0.0`
- Run `flutter pub upgrade --major-versions` if needed

#### Issue: Missing Dependencies
```
Error: Could not find dependency
```

**Solution**:
- Check dependency name spelling in `pubspec.yaml`
- Verify dependency exists on pub.dev
- Check internet connection
- Clear pub cache: `flutter pub cache repair`

### 2. Gradle Build Errors

#### Issue: Gradle Version Incompatibility
```
Error: Gradle version X.X is required
```

**Solution**:
- Update Gradle wrapper: `cd android && ./gradlew wrapper --gradle-version=8.0`
- Check `android/gradle/wrapper/gradle-wrapper.properties`
- Ensure Java 17 is installed: `java -version`

#### Issue: Gradle Daemon Issues
```
Error: Gradle daemon stopped unexpectedly
```

**Solution**:
- Stop daemon: `cd android && ./gradlew --stop`
- Clear Gradle cache: `rm -rf ~/.gradle/caches`
- Check memory settings in `gradle.properties`
- For CI, use `android/gradle-ci.properties`

#### Issue: Deprecated Gradle Configuration
```
Warning: The following Gradle features are deprecated
```

**Solution**:
- Review `android/build.gradle.kts` and `android/app/build.gradle.kts`
- Update Gradle plugin version
- Check for deprecated DSL usage
- Run `./gradlew --warning-mode all` for details

### 3. Java/JVM Issues

#### Issue: Wrong Java Version
```
Error: Compilation failed: java.lang.UnsupportedClassVersionError
```

**Solution**:
- This project requires Java 17
- Check: `java -version`
- Set JAVA_HOME: `export JAVA_HOME=/path/to/java17`
- Verify in gradle files: `JavaVersion.VERSION_17`

#### Issue: Out of Memory
```
Error: GC overhead limit exceeded
```

**Solution**:
- Increase heap size in `android/gradle.properties`:
  ```properties
  org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=1g
  ```
- For CI, use `android/gradle-ci.properties` (3GB limit)
- Enable parallel GC: `-XX:+UseParallelGC`

### 4. R8/ProGuard Issues

#### Issue: Class Not Found After R8 Shrinking
```
Error: Missing class referenced from: ...
```

**Solution**:
- Add ProGuard rules in `android/app/proguard-rules.pro`:
  ```proguard
  -keep class com.your.package.** { *; }
  -dontwarn com.problematic.library.**
  ```
- Check if library provides ProGuard rules
- Disable shrinking temporarily to test: `shrinkResources false`

#### Issue: R8 Fails
```
Error: R8 task failed
```

**Solution**:
- Update Android Gradle Plugin
- Check for incompatible ProGuard rules
- Try R8 full mode: `android.enableR8.fullMode=true`
- Use `--verbose` flag to see details

### 5. Native Code Issues

#### Issue: Kotlin Compilation Fails
```
Error: Kotlin compilation failed
```

**Solution**:
- Check Kotlin version in `android/build.gradle.kts`
- Review Kotlin code in `android/app/src/main/kotlin/`
- Ensure Kotlin plugin version matches Gradle
- Update to latest stable Kotlin version

#### Issue: NDK/Native Library Issues
```
Error: Could not find NDK
```

**Solution**:
- Install NDK via Android Studio or SDK Manager
- Set `ANDROID_NDK_HOME` environment variable
- Check if dependency actually needs NDK
- Consider excluding unwanted ABIs in `build.gradle.kts`

### 6. Resource Issues

#### Issue: Duplicate Resources
```
Error: Duplicate resources
```

**Solution**:
- Check `android/app/src/main/res/` for duplicates
- Review resource merging in `build.gradle.kts`
- Use resource prefixes to avoid conflicts
- Exclude duplicates from dependencies

#### Issue: Missing Resources
```
Error: Resource not found
```

**Solution**:
- Verify resource files exist in correct folders
- Check resource naming (lowercase, no special chars)
- Ensure resources are in appropriate density folders
- Run `flutter pub get` to regenerate

### 7. Plugin Integration Issues

#### Issue: Plugin Registration Fails
```
Error: Unhandled Exception: MissingPluginException
```

**Solution**:
- Run `flutter clean && flutter pub get`
- Check `.flutter-plugins-dependencies`
- Verify plugin in `pubspec.yaml`
- Rebuild native code: `flutter build apk --verbose`

#### Issue: Plugin Version Conflict
```
Error: Plugin version incompatible
```

**Solution**:
- Check plugin's minimum Flutter/Android versions
- Update Flutter SDK if needed
- Update plugin to compatible version
- Review plugin's changelog for breaking changes

### 8. Manifest Issues

#### Issue: Manifest Merge Fails
```
Error: Manifest merger failed
```

**Solution**:
- Check `android/app/src/main/AndroidManifest.xml`
- Review plugin manifests causing conflicts
- Add merge rules if needed:
  ```xml
  <uses-sdk tools:overrideLibrary="conflicting.package" />
  ```
- Use `tools:replace` or `tools:merge` attributes

#### Issue: Permission Issues
```
Error: Permission denied
```

**Solution**:
- Add required permissions to `AndroidManifest.xml`
- Check permission compatibility with minSdkVersion
- Review runtime permission handling in code

## Project-Specific Build Configuration

### This Template Uses

- **Java 17**: Required for optimal performance
- **Gradle 8.0+**: Modern build system
- **Flutter 3.10.1+**: Latest stable features
- **Kotlin**: For Android native code
- **R8**: Code shrinking enabled
- **Parallel builds**: Optimized for performance
- **Build cache**: Enabled for faster rebuilds

### Key Files

1. **pubspec.yaml**: Flutter dependencies
2. **android/build.gradle.kts**: Root Gradle config
3. **android/app/build.gradle.kts**: App-specific Gradle config
4. **android/gradle.properties**: Local build settings
5. **android/gradle-ci.properties**: CI-optimized settings
6. **android/app/src/main/AndroidManifest.xml**: App manifest

## Systematic Debug Approach

### Level 1: Quick Fixes (Try First)
```bash
flutter clean
flutter pub get
flutter build apk --verbose
```

### Level 2: Gradle Reset
```bash
cd android
./gradlew clean
./gradlew --stop
cd ..
flutter clean
flutter pub get
flutter build apk --verbose
```

### Level 3: Cache Clear
```bash
flutter clean
rm -rf ~/.gradle/caches/
rm -rf ~/.pub-cache/
flutter pub get
flutter build apk --verbose
```

### Level 4: Deep Dive
```bash
# Check Flutter setup
flutter doctor -v

# Verify Java version
java -version

# Check Gradle dependencies
cd android
./gradlew app:dependencies

# Build with stacktrace
./gradlew assembleRelease --stacktrace --info

# Or with Flutter verbose
flutter build apk --verbose --debug
```

## Build Performance Optimization

If builds work but are slow:

### Local Development
- Use `android/gradle.properties`
- Enable parallel builds: `org.gradle.parallel=true`
- Increase workers: `org.gradle.workers.max=4`
- More memory: `org.gradle.jvmargs=-Xmx4g`
- Enable configuration cache: `org.gradle.configuration-cache=true`

### CI Environment
- Use `android/gradle-ci.properties`
- Fewer workers: `org.gradle.workers.max=2`
- Less memory: `org.gradle.jvmargs=-Xmx3g`
- Disable daemon: `org.gradle.daemon=false`
- Disable configuration cache: `org.gradle.configuration-cache=false`

## Troubleshooting Checklist

- [ ] Run `flutter doctor -v` - all checks pass?
- [ ] Java version is 17? (`java -version`)
- [ ] Flutter version matches project requirements?
- [ ] Run `flutter clean && flutter pub get`
- [ ] Try `cd android && ./gradlew clean`
- [ ] Check for conflicting dependencies
- [ ] Review `pubspec.yaml` for errors
- [ ] Verify `android/app/build.gradle.kts` settings
- [ ] Check `AndroidManifest.xml` is valid
- [ ] Look for file permission issues
- [ ] Test on different machine if possible
- [ ] Review full error message with `--verbose`
- [ ] Check GitHub Issues for similar problems

## Quick Reference Commands

```bash
# Clean build
flutter clean && flutter pub get && flutter build apk

# Verbose build
flutter build apk --verbose

# Check dependencies
flutter pub outdated
cd android && ./gradlew app:dependencies

# Gradle info
cd android && ./gradlew --version
./gradlew tasks --all

# Fix common issues
dart fix --apply
flutter analyze

# Update dependencies
flutter pub upgrade

# Check Flutter setup
flutter doctor -v

# Test specific build type
flutter build apk --debug
flutter build apk --profile
flutter build apk --release
```

## When to Seek Help

If after trying all solutions the build still fails:

1. **Document the issue**:
   - Full error message
   - Build command used
   - Flutter doctor output
   - Java version
   - Steps already tried

2. **Check resources**:
   - Project's TROUBLESHOOTING.md
   - Flutter GitHub Issues
   - Stack Overflow
   - Plugin's GitHub Issues

3. **Create minimal reproduction**:
   - Start with `flutter create test_app`
   - Add dependencies one by one
   - Identify which dependency causes issue

## Additional Resources

- [Flutter Build Modes](https://docs.flutter.dev/testing/build-modes)
- [Gradle Performance Guide](https://docs.gradle.org/current/userguide/performance.html)
- [Android Build Configuration](https://developer.android.com/studio/build)
- Project docs: `BUILD_OPTIMIZATION.md`, `TROUBLESHOOTING.md`
