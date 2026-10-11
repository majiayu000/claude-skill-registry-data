---
name: android-backup-exclusion-verify
description: "Verify an Android app's auto-backup/device-transfer exclusions actually protect private data — covers the derived-copy trap (snapshots/exports/journals in the file domain defeating a database exclusion), checking rules inside the packaged APK rather than the source tree, and why the emulator's local transport cannot prove payload contents (control build required). Use when an app claims data \"never leaves the device\", after adding any on-disk copy of a database, or before a first store release."
---

# Verify Android backup exclusions

Android auto-backup copies app data to the user's Google account and to a new
phone during device transfer. An app that promises "your data stays on this
device" is making a claim the backup system can silently break.

## 1. Enumerate every on-disk copy first, not just the database

The classic defect is a rule file that excludes the database while a
**derived copy of it** sits somewhere the rules don't cover. `<exclude>` entries
are per-domain; excluding `domain="database"` does nothing for `domain="file"`.

Sweep for anything that writes a copy:

```bash
rtk grep -rn "copyTo\|writeText\|FileOutputStream\|getDatabasePath\|filesDir" \
  app/src/main/kotlin --include=*.kt | head -20
```

Candidates that regularly defeat a database exclusion:

| what | where it lands | domain |
|---|---|---|
| pre-migration DB snapshot | `filesDir/db-snapshots/` | `file` |
| crash journal / local log | `filesDir/crash/` | `file` |
| export staged for sharing | `cacheDir/exports/` | `cache` — **not backed up**, no rule needed |
| SharedPreferences | `shared_prefs/` | `sharedpref` |

`cache` and `code_cache` are excluded by the platform. Everything under
`filesDir` is included by default.

## 2. Cover BOTH rule files and BOTH domains

`android:fullBackupContent` (API ≤ 30) and `android:dataExtractionRules`
(API 31+) are separate files, and the latter has two independent sections:

```xml
<data-extraction-rules>
    <cloud-backup>   <!-- Google account backup -->
    <device-transfer><!-- phone-to-phone copy -->
</data-extraction-rules>
```

A rule present in `cloud-backup` but missing from `device-transfer` leaks on
every new-phone setup. Assert the counts rather than reading by eye:

```python
import re, pathlib
for f in ("backup_rules", "data_extraction_rules"):
    t = pathlib.Path(f"app/src/main/res/xml/{f}.xml").read_text(encoding="utf-8")
    print(f, re.findall(r'<exclude domain="(\w+)" path="([^"]+)"', t))
```

## 3. Check the PACKAGED APK, not the source tree

A rule file can be correct on disk and absent from the build (wrong resource
dir, a build variant overriding `res/`):

```python
import zipfile
z = zipfile.ZipFile("app/build/outputs/apk/debug/app-debug.apk")
for n in ("res/xml/backup_rules.xml", "res/xml/data_extraction_rules.xml"):
    b = z.read(n)
    print(n, b"db-snapshots" in b, b"monarch.db" in b)
```

Binary XML still contains the path strings, so a plain byte check works.

Then confirm the platform accepts them — a malformed rule file fails to parse
and the app falls back to backing up **everything**:

```bash
adb shell logcat -c
adb shell bmgr fullbackup <pkg>
adb shell logcat -d | grep -iE "backup.*(xml|rule|parse).*(error|invalid|fail)"
```

## 4. The local transport cannot prove payload contents — run the control

The obvious next step is to back up and inspect what was stored:

```bash
adb root
adb shell bmgr enable true
adb shell bmgr transport com.android.localtransport/.LocalTransport
adb shell bmgr fullbackup <pkg>
adb shell ls -lR /data/data/com.android.localtransport/files/1/_full/<pkg>
```

**An absent or empty directory here is NOT evidence of exclusion.** On a
stock emulator the local transport routinely stores nothing for a
sideloaded package regardless of its rules.

Before drawing any conclusion, build a control with the exclusions stripped:

```xml
<full-backup-content />
```

and confirm the permissive rules really installed (`b"db-snapshots" in ...`
returns `False` for the control APK) before running the same backup.

- Control stores the database, fixed build does not → exclusion proven.
- **Control stores nothing either → the harness is blind; record a gap, not a pass.**

Payload-level proof generally needs a device signed into a Google account.

## Traps

- **`.bak` files staged inside `res/`** break the build:
  `The file name must end with .xml`. Stage backups outside the resource tree.
- **Install after a failed build** silently re-installs the previous APK, so the
  "control" is the fixed build. Check the build result, then verify the
  installed artifact's bytes — never assume the install matched the intent.
- A `filesDir` copy created for a good reason (migration safety net, crash
  journal) is exactly the kind of file nobody re-checks against the backup
  rules when it is added.

## Finally

State the guarantee in the privacy policy with the rule file paths, so the
claim and the mechanism are reviewable together.
