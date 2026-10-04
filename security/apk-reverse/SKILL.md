---
name: apk-reverse
description: >
  Reverse engineering of Android APK files. Use this skill ALWAYS whenever the user mentions
  APK, Android, decompile, reverse engineer, analyze Android app, extract code, manifest,
  permissions, DEX classes, resources, certificates, smali, or any kind of Android mobile
  application analysis. Even if the request is simple like "analyze this APK" or "what does
  this app do", use this skill. Includes static analysis, metadata extraction, strings, URLs,
  permissions, Java/Kotlin classes, resources, and suspicious pattern detection.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Skill: APK Reverse Engineering

## Overview

This skill uses **androguard** (Python) for static APK analysis directly inside the VM.
It does not require external tools like apktool or jadx — everything works through Python.

## Available Tools

| Tool         | Availability         | Usage                                            |
| ------------ | -------------------- | ------------------------------------------------ |
| `androguard` | ✅ Installed (`pip`) | Full analysis: DEX, manifest, strings, API calls |
| `zipfile`    | ✅ Python stdlib     | Extract resources, assets, files                 |
| `xml.etree`  | ✅ Python stdlib     | XML parsing (decoded manifest)                   |
| `hashlib`    | ✅ Python stdlib     | APK MD5/SHA1/SHA256 hashes                       |
| `apktool`    | ❌ Not available     | Would require manual download                    |
| `jadx`       | ❌ Not available     | Would require manual download                    |

## Standard Workflow

### 1. Locate the APK

```bash
ls /mnt/user-data/uploads/
```

The APK will be located at `/mnt/user-data/uploads/<name>.apk`.

### 2. Run analysis with androguard

See `scripts/analyze_apk.py` for the complete analysis script.

Quick execution:

```bash
python3 /home/claude/apk-reverse/scripts/analyze_apk.py /mnt/user-data/uploads/app.apk
```

### 3. Resource extraction (without androguard)

To extract raw APK files (APK is a ZIP archive):

```python
import zipfile
with zipfile.ZipFile("app.apk") as z:
    z.extractall("/tmp/apk_contents/")
```

### 4. Interpret results and present them to the user

Organize the analysis into clear sections. See `references/output_guide.md`.

---

## What Androguard Can Do

```python
from androguard.misc import AnalyzeAPK

a, d, dx = AnalyzeAPK("app.apk")

# Metadata
a.get_package()              # package name
a.get_app_name()             # readable app name
a.get_androidversion_name()  # version
a.get_min_sdk_version()      # minimum SDK
a.get_target_sdk_version()   # target SDK

# Permissions
a.get_permissions()          # permission list

# Activities, Services, Receivers
a.get_activities()
a.get_services()
a.get_receivers()
a.get_providers()

# Strings (all DEX strings)
for s in dx.get_strings():
    print(s.get_orig_value())

# Java classes
for cls in dx.get_classes():
    print(cls.name)

# API calls
for method in dx.get_methods():
    for _, call, _ in method.get_xref_to():
        print(call.class_name, call.name)

# Certificate / signature
a.get_certificates()
```

---

## Analysis Types

### Quick Analysis (default)

- File hash
- Metadata (package, version, SDK)
- Dangerous permissions
- Main components (Activities, Services)
- Notable strings (URLs, IPs, hardcoded keys)

### Full Analysis

- All classes and methods
- Critical API calls (cryptography, network, SMS, camera)
- Obfuscation detection
- Certificates and signatures
- Assets and resources

### Security Analysis

- Dangerous permissions
- Suspicious strings (C2 URLs, keys, tokens)
- Sensitive APIs (SMS, contacts, location)
- Anti-analysis detection (emulator detection)

---

## Dangerous Permission Flags

```python
DANGEROUS_PERMS = [
    "READ_SMS", "SEND_SMS", "RECEIVE_SMS",
    "READ_CONTACTS", "WRITE_CONTACTS",
    "ACCESS_FINE_LOCATION", "ACCESS_COARSE_LOCATION",
    "RECORD_AUDIO", "CAMERA",
    "READ_CALL_LOG", "PROCESS_OUTGOING_CALLS",
    "GET_ACCOUNTS", "USE_CREDENTIALS",
    "READ_EXTERNAL_STORAGE", "WRITE_EXTERNAL_STORAGE",
    "INSTALL_PACKAGES", "DELETE_PACKAGES",
    "BIND_DEVICE_ADMIN", "RECEIVE_BOOT_COMPLETED",
]
```

---

## References

- `scripts/analyze_apk.py` — Main automatic analysis script
- `references/output_guide.md` — How to format and present results
- `references/api_patterns.md` — Suspicious API patterns to detect

---

## Important Notes

1. **Large APKs (>50MB)** may take longer for string/class analysis
2. **Obfuscated APKs** (ProGuard/R8) will have class names like `a.b.c` — mention this to the user
3. **Multi-DEX APKs** (`classes2.dex`, etc.) — androguard handles them automatically
4. **Split APKs** (`.apks`, `.aab`) require different handling — inform the user
5. Never execute code extracted from APKs — perform static analysis only
