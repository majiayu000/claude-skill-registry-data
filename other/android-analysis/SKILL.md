---
name: android-analysis
description: Expert Android and Java reverse engineering for APK/AAR/JAR decompilation and inspection. Use when user mentions "decompile", "jadx", "apktool", "reverse engineer", or needs to analyze Android binaries, unpack libraries, understand obfuscated apps, or extract resources from compiled artifacts.
allowed-tools: Read, Grep, Glob, Bash(jadx:*), Bash(apktool:*), Bash(apkanalyzer:*), Bash(java:*), Bash(unzip:*), Bash(jar:*), Bash(tree:*), WebFetch, WebSearch
---

# Android & Java Binary Analysis

## Purpose

Comprehensive reverse engineering toolkit combining JADX (Android DEX), CFR (Java JAR), apktool (Smali), and
apkanalyzer (structure inspection) to decompile compiled binaries into readable source code. This skill provides
systematic guidance for choosing the optimal tool for each reverse engineering scenario.

## When to Use This Skill

Invoke this skill when:

- Decompiling APKs to Java source code for analysis
- Reverse engineering AAR/JAR libraries to understand implementations
- Extracting AndroidManifest.xml, resources, or assets from APKs
- Analyzing obfuscated or ProGuard/R8-protected code
- Understanding third-party SDK behavior or security practices
- Investigating app architecture, API integrations, or authentication flows
- Comparing different APK/library versions
- User explicitly mentions "decompile", "reverse engineer", "jadx", "apktool", or requests binary analysis

## Core Concepts

### Tool Selection Matrix

**File Type Decision:**

- **APK** → JADX (DEX to Java) or apktool (DEX to Smali)
- **AAR** → Extract classes.jar → CFR (best) or JADX (acceptable)
- **JAR** → CFR (primary) or Vineflower (modern Java 21+)
- **DEX** → JADX only

**JADX (Android DEX Decompiler)**

- Best for: APK and DEX files only
- Always use: `--deobf` flag for obfuscated code
- Use when: Analyzing Android apps, need GUI, or working with multi-format archives
- Limitation: Poor Java decompilation quality (fails Lambda/Stream operations)

**CFR (Java JAR Decompiler)**

- Best for: JAR files and extracted classes.jar from AAR
- Fastest speed (6.5s for 1.5MB JAR) with best readability
- Modern Java support (5-14) with excellent Lambda/Stream handling
- Use when: Analyzing Java libraries, need accurate decompilation, or JADX output is unreadable

**Vineflower (Modern Java Decompiler)**

- Best for: Java 21+ projects (records, sealed classes, pattern matching)
- Multithreaded decompilation with clean output formatting
- IntelliJ IDEA plugin available
- Use when: Working with cutting-edge Java features

**apktool (Smali Disassembler)**

- Best for: Exact bytecode (smali), resource extraction, manifest inspection, APK modifications
- Use when: JADX fails, need AndroidManifest.xml, or exact bytecode required for patching

**apkanalyzer (Structure Inspector)**

- Best for: Quick APK metadata, package/method counts, version comparisons
- Use when: Need overview before decompilation or comparing APK sizes/structure

### Decompilation vs Disassembly

- **Decompilation** (JADX/CFR): Bytecode → Java source (readable but may be approximate)
- **Disassembly** (apktool): DEX → Smali bytecode (exact but verbose)

Use JADX/CFR by default; fall back to apktool if decompilation fails or exact bytecode needed.

### Archive Structure

- **APK**: Android Package (DEX files, AndroidManifest.xml, resources, assets, native libs)
- **AAR**: Android Archive (classes.jar, AndroidManifest.xml, resources, native libs) — Extract classes.jar first
- **JAR**: Java Archive (compiled .class files, MANIFEST.MF) — Use CFR, not JADX

## Quick Command Reference

### APK Decompilation

**Full decompilation (JADX):**

```bash
jadx --deobf -d output/ app.apk              # Full with deobfuscation
jadx --no-res --deobf -d output/ app.apk     # Skip resources (faster)
```

**Smali disassembly (apktool):**

```bash
apktool d app.apk -o output/                 # Full disassembly
apktool d --no-res app.apk -o output/        # Smali only
apktool d --no-src app.apk -o output/        # Resources only
```

**Structure inspection (apkanalyzer):**

```bash
apkanalyzer apk summary app.apk              # Package ID, version, SDK
apkanalyzer dex packages app.apk             # Package breakdown
apkanalyzer dex references app.apk           # Method count
apkanalyzer apk compare old.apk new.apk      # Version diff
```

### AAR Library Analysis

**Extract and decompile with CFR (recommended):**

```bash
unzip library.aar classes.jar                # Extract classes.jar
java -jar cfr.jar classes.jar --outputdir decompiled/  # Decompile with CFR
```

**Direct decompilation with JADX (acceptable):**

```bash
jadx --deobf -d output/ library.aar          # Works but lower quality than CFR
```

**Inspect full AAR structure:**

```bash
unzip -l library.aar                         # List contents
unzip library.aar -d unpacked/               # Extract all
tree unpacked/                               # View structure
```

### JAR Library Decompilation

**CFR (primary choice):**

```bash
java -jar cfr.jar library.jar --outputdir decompiled/
```

**Vineflower (modern Java 21+):**

```bash
java -jar vineflower.jar library.jar decompiled/
```

**JADX (not recommended for pure Java):**

```bash
jadx --deobf -d output/ library.jar          # Use only if CFR unavailable
```

### Deobfuscation

**With ProGuard/R8 mapping.txt:**

```bash
# ReTrace (official ProGuard tool)
retrace.sh mapping.txt stacktrace.txt

# Reconstruct (JAR deobfuscation)
java -jar reconstruct-cli.jar -jar obfuscated.jar -mapping mapping.txt -output deobfuscated.jar
```

**Without mapping file:**

```bash
jadx --deobf -d output/ app.apk              # JADX automated deobfuscation (limited)
# Or fall back to smali for exact bytecode
apktool d app.apk -o output-smali/
```

### Code Inspection After Decompilation

**Search patterns (use Grep tool, not bash grep):**

```bash
# Find API endpoints
Grep pattern:"https?://[^\"']+" output_mode:content

# Find credentials
Grep pattern:"(api[_-]?key|secret|password)" -i:true output_mode:content

# Locate specific classes
Glob pattern:**/*Auth*.java
```

## Real-World Examples

### Example 1: Analyzing Third-Party SDK (AAR)

**Scenario**: Marketing team integrated Firebase SDK but app crashes on startup. Need to understand initialization
requirements.

**Workflow**:

```bash
# 1. Extract AAR
unzip firebase-analytics-21.2.0.aar classes.jar

# 2. Decompile with CFR (best readability)
java -jar cfr.jar classes.jar --outputdir firebase-src/

# 3. Search for initialization code
Grep pattern:"initialize|init" path:firebase-src/ output_mode:content

# 4. Find crash location from stacktrace
Grep pattern:"FirebaseApp" path:firebase-src/ output_mode:content

# 5. Read initialization class
Read firebase-src/com/google/firebase/FirebaseApp.java
```

**Findings**: SDK requires `google-services.json` in assets/ folder. Missing file caused NullPointerException.

### Example 2: Reverse Engineering Competitor App

**Scenario**: Security audit of competitor's e-commerce app to understand their API security and payment processing.

**Workflow**:

```bash
# 1. Get APK metadata
apkanalyzer apk summary competitor-shop.apk
apkanalyzer manifest permissions competitor-shop.apk

# 2. Decompile with JADX
jadx --deobf -d shop-src/ competitor-shop.apk

# 3. Find API endpoints
Grep pattern:"https://api\." path:shop-src/ output_mode:content

# 4. Locate payment processing
Glob pattern:**/*Payment*.java path:shop-src/

# 5. Analyze authentication
Read shop-src/sources/com/competitor/shop/api/AuthManager.java
```

**Findings**: App uses hardcoded API keys (security risk), bearer token auth, Stripe SDK for payments. No certificate
pinning (vulnerable to MITM).

### Example 3: Deobfuscating ProGuard-Protected Library

**Scenario**: Legacy Java library with ProGuard obfuscation needs bug fix. mapping.txt file available.

**Workflow**:

```bash
# 1. Inspect obfuscation level
java -jar cfr.jar obfuscated-lib.jar --outputdir temp/
# Output shows classes named a.java, b.java, c.java

# 2. Deobfuscate with mapping file
java -jar reconstruct-cli.jar \
  -jar obfuscated-lib.jar \
  -mapping mapping.txt \
  -output deobfuscated-lib.jar

# 3. Decompile restored JAR
java -jar cfr.jar deobfuscated-lib.jar --outputdir lib-src/

# 4. Now readable with original names
Read lib-src/com/company/utils/DatabaseHelper.java
```

**Findings**: Restored original class/method names reveal SQL injection vulnerability in `executeRawQuery()` method.

### Example 4: Investigating Obfuscated Malware APK

**Scenario**: Suspicious APK requesting excessive permissions. Determine if it's malware.

**Workflow**:

```bash
# 1. Check permissions
apkanalyzer manifest permissions suspicious.apk
# Shows: READ_SMS, SEND_SMS, ACCESS_FINE_LOCATION, INTERNET

# 2. Decompile with JADX deobfuscation
jadx --deobf -d malware-src/ suspicious.apk

# 3. Search for SMS exfiltration
Grep pattern:"SmsManager|sendTextMessage" path:malware-src/ output_mode:content

# 4. Find network calls
Grep pattern:"HttpURLConnection|OkHttp|Retrofit" path:malware-src/ output_mode:content

# 5. Check for encoded C&C server
Grep pattern:"Base64|decode|decrypt" path:malware-src/ output_mode:content

# 6. Read suspicious service
Read malware-src/sources/a/b/c/BackgroundService.java
```

**Findings**: App sends SMS messages to premium numbers, exfiltrates location to hardcoded IP address. Confirmed
malware.

### Example 5: Comparing APK Versions for Security Regression

**Scenario**: App version 2.0 has authentication bypass bug. Compare with version 1.5 to find changes.

**Workflow**:

```bash
# 1. Compare APK structure
apkanalyzer apk compare app-v1.5.apk app-v2.0.apk --different-only

# 2. Decompile both versions
jadx --deobf -d v1.5-src/ app-v1.5.apk
jadx --deobf -d v2.0-src/ app-v2.0.apk

# 3. Compare authentication files
Read v1.5-src/sources/com/app/auth/LoginActivity.java
Read v2.0-src/sources/com/app/auth/LoginActivity.java

# 4. Search for validation changes
Grep pattern:"validate|verify|check" path:v2.0-src/sources/com/app/auth/ output_mode:content
```

**Findings**: v2.0 removed server-side token validation, allowing bypass with any JWT token. Regression identified.

### Example 6: Understanding Closed-Source SDK Behavior

**Scenario**: Ads SDK (AAR) has 10x higher battery drain than documented. Investigate why.

**Workflow**:

```bash
# 1. Extract and decompile SDK
unzip ads-sdk-3.1.0.aar classes.jar
java -jar cfr.jar classes.jar --outputdir ads-src/

# 2. Search for background services
Grep pattern:"Service|JobScheduler|WorkManager" path:ads-src/ output_mode:content

# 3. Find location tracking
Grep pattern:"LocationManager|GPS|getLastKnownLocation" path:ads-src/ output_mode:content

# 4. Check wake lock usage
Grep pattern:"WakeLock|acquire|PowerManager" path:ads-src/ output_mode:content

# 5. Read background tracking service
Read ads-src/com/adnetwork/tracking/LocationService.java
```

**Findings**: SDK polls GPS every 30 seconds with wake lock held. Undocumented behavior causing battery drain.

## Common Workflows

### "Decompile this APK"

1. Get overview: `apkanalyzer apk summary app.apk`
2. Decompile: `jadx --deobf -d output/ app.apk`
3. Inspect structure: `tree -L 3 output/sources/`
4. Find entry points: `Glob pattern:**/*MainActivity*.java`
5. Read code: `Read output/sources/com/app/MainActivity.java`
6. Explain functionality to user

### "Analyze this AAR library"

1. Extract classes.jar: `unzip library.aar classes.jar`
2. Decompile with CFR: `java -jar cfr.jar classes.jar --outputdir src/`
3. Identify public APIs: `Grep pattern:"public (class|interface)" path:src/ output_mode:content`
4. Check dependencies: `unzip -p library.aar AndroidManifest.xml`
5. Inspect native libs (if any): `unzip -l library.aar | grep .so`

### "Decompile this JAR"

1. Decompile with CFR: `java -jar cfr.jar library.jar --outputdir src/`
2. If CFR unavailable, use JADX: `jadx -d output/ library.jar` (lower quality)
3. Inspect structure: `tree -L 3 src/`
4. Find main classes: `Grep pattern:"public static void main" path:src/ output_mode:content`

### "Show me AndroidManifest.xml"

1. Extract manifest: `apktool d --no-src --no-res app.apk -o manifest-only/`
2. Read: `Read manifest-only/AndroidManifest.xml`
3. Analyze: Permissions, components, min SDK, exported activities

### "Is this code obfuscated?"

1. Decompile: `jadx --deobf -d output/ app.apk`
2. Check class names: `Glob pattern:**/[a-z].java` (single-letter = obfuscated)
3. Look for JADX deobfuscation comments: `Grep pattern:"// Deobfuscated:" output_mode:content`
4. Explain obfuscation level (ProGuard/R8 vs DexGuard vs custom)

### "Find authentication implementation"

1. Decompile: `jadx --deobf -d output/ app.apk`
2. Search for auth keywords: `Grep pattern:"(auth|login|token|session)" -i:true output_mode:content`
3. Find auth classes: `Glob pattern:**/*{Auth,Login,Token}*.java`
4. Read implementation: `Read output/sources/com/app/auth/AuthManager.java`
5. Map authentication flow (token storage, refresh logic, API endpoints)

### "Compare two APK versions"

1. Quick structural diff: `apkanalyzer apk compare old.apk new.apk --different-only`
2. Decompile both: `jadx --deobf -d old-src/ old.apk && jadx --deobf -d new-src/ new.apk`
3. Compare key classes: `Read old-src/...` vs `Read new-src/...`
4. Identify security regressions or new features

## Error Handling

**JADX decompilation fails:**

```bash
# Fall back to apktool for smali
apktool d app.apk -o output-smali/
# Then read smali files for exact bytecode
```

**JADX produces unreadable Java (for JAR/AAR):**

```bash
# Extract classes.jar from AAR first
unzip library.aar classes.jar

# Use CFR instead (much better for Java)
java -jar cfr.jar classes.jar --outputdir src/
```

**Need faster processing:**

```bash
# Skip resources if only analyzing code
jadx --no-res --deobf -d output/ app.apk
```

**APK is very large (100MB+):**

```bash
# 1. First understand structure
apkanalyzer dex packages app.apk | head -20

# 2. Then decompile without resources
jadx --no-res --deobf -d output/ app.apk
```

**Obfuscated code is unreadable:**

```bash
# 1. If mapping.txt available, use ReTrace/Reconstruct
java -jar reconstruct-cli.jar -jar obfuscated.jar -mapping mapping.txt -output deobfuscated.jar

# 2. If no mapping, use apktool for exact smali
apktool d app.apk -o output-smali/

# 3. Focus on strings, API calls, and control flow rather than variable names
```

**CFR not available:**

```bash
# Use JADX as fallback (acceptable but lower quality)
jadx --deobf -d output/ library.jar
```

## Tool Availability

Verify tools before use:

```bash
which jadx        # Android DEX decompiler
which apktool     # Smali disassembler
which apkanalyzer # Structure inspector (Android SDK)
java -jar cfr.jar --version  # Java decompiler (check path)
```

If missing, consult `references/installation-guide.md` for setup instructions.

## References

**Tool-specific documentation:**

- `references/jadx-reference.md` - Complete JADX command-line reference with all options, deobfuscation flags, and
  plugins
- `references/cfr-reference.md` - Complete CFR decompiler reference with command-line options and Java version support
- `references/vineflower-reference.md` - Vineflower decompiler for modern Java 21+ features
- `references/apktool-reference.md` - Complete apktool reference with decode/build options, smali output structure
- `references/apkanalyzer-reference.md` - Complete apkanalyzer reference with all subjects/verbs and comparison features

**General documentation:**

- `references/tool-comparison.md` - Tool selection decision trees and comparison matrix
- `references/installation-guide.md` - Installation and setup for all tools

## Environment Variables

```bash
export ANDROID_HOME="$HOME/Library/Android/sdk"          # Android SDK location
export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin" # Add apkanalyzer to PATH
```

## Tips for Effective Analysis

**Choose the right tool for the job:**

- APK/DEX → JADX (Android-specific)
- JAR → CFR (best readability)
- AAR → Extract classes.jar → CFR
- Java 21+ → Vineflower

**Start with structure:**

- Use `apkanalyzer` first to understand APK composition before decompiling
- Check package breakdown and method counts

**Always deobfuscate:**

- Use `--deobf` flag with JADX for obfuscated code
- Use mapping.txt with ReTrace/Reconstruct when available

**Skip resources when possible:**

- Use `--no-res` for code-only analysis (faster)
- Extract resources separately with apktool if needed

**Search before reading:**

- Use Grep tool to find relevant code before reading entire files
- Locate classes with Glob before using Read tool

**Handle large codebases efficiently:**

- Don't decompile everything at once
- Use targeted searches to identify files of interest
- Read specific files based on search results

**Validate with multiple tools:**

- Cross-reference JADX output with CFR for critical analysis
- Use apktool smali as ground truth when decompilers disagree
