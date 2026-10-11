---
name: android-share-payload-binder-limit
description: "Find and fix Android share/export actions that pass large payloads through Intent extras and will throw TransactionTooLargeException once real user data accumulates — measuring the payload at realistic scale, staging a file via FileProvider, and driving the chooser on device. Use when an app exports/shares user data as text, or when a feature works on a fresh install but is suspected at years of data."
---

# Share payloads and the binder limit

Failure mode: `Intent.EXTRA_TEXT` (or any large extra) carries a payload that
grows with user data. A binder transaction is capped near **1 MB** for the whole
transaction, so the action throws `TransactionTooLargeException` only for users
with the most history — and passes every test on a fresh install.

This bites hardest on **export / "share my data"** actions, which is what people
reach for when something has already gone wrong.

## 1. Find the sites

```bash
rtk grep -rn "EXTRA_TEXT\|putExtra(Intent\." app/src/main/kotlin --include=*.kt
```

A share helper with **no** file I/O is the tell. When hunting main-thread disk
work with StrictMode, a share path that never touches disk looks innocent — it
is the opposite defect.

## 2. Measure the payload at realistic scale, don't estimate

Seed years of data into an **isolated** database and measure the real string:

```kotlin
var chars = 0
repo.exportJson().also { chars = it.length }
assertTrue(
    "export is %.2f MB at %d sessions".format(chars / 1048576.0, SESSIONS),
    chars in 1 until 4_000_000,
)
```

Report the number in the failure message and keep it in the test as a comment:
the point is that the ceiling stays visible to whoever edits that code next.
(Real example: 1,000 sessions → **0.87 MB**, i.e. already at the limit.)

## 3. Fix by staging a file, not by trimming the payload

```kotlin
private suspend fun shareExport(context: Context, title: String, fileName: String, text: String) {
    val uri = withContext(Dispatchers.IO) {
        val dir = File(context.cacheDir, "exports").apply { mkdirs() }
        val file = File(dir, fileName)      // one name, overwritten: cache is not an archive
        file.writeText(text)
        FileProvider.getUriForFile(context, "${context.packageName}.exports", file)
    }
    context.startActivity(
        Intent.createChooser(
            Intent(Intent.ACTION_SEND).apply {
                type = "application/json"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            },
            title,
        ),
    )
}
```

Manifest + `res/xml/file_paths.xml` — scope the provider to the staging
directory only, so the database, its backups and any crash journal stay
unreachable:

```xml
<provider android:name="androidx.core.content.FileProvider"
    android:authorities="${applicationId}.exports"
    android:exported="false" android:grantUriPermissions="true">
    <meta-data android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
</provider>
```

```xml
<paths><cache-path name="exports" path="exports/" /></paths>
```

Route **every** share through it. Two sharing paths with different failure modes
is how one of them rots.

## 4. Prove it on device

The write is invisible in the UI, so check the staged file directly:

```bash
adb shell am start -n <pkg>/.MainActivity
# navigate and tap the export control (match its REAL label from source)
adb shell run-as <pkg> ls -l /data/data/<pkg>/cache/exports/
adb shell logcat -d -b crash          # expect empty
```

Confirm three things: the chooser appeared, the file exists with non-zero size,
and the crash buffer is empty.

## Traps

- **The button label is uppercased by a custom composable.** `label = "Export
  Archive"` renders as `EXPORT ARCHIVE`; a Material `Button` does not uppercase.
  Match the rendered text, or the tap silently misses.
- **The control is below the fold.** Scroll before concluding it is absent, and
  take tap coordinates from a dump made *after* the scroll.
- **The instrumented gate uninstalls the app.** A device sweep straight after
  `connectedAndroidTest` drives the launcher; check `pm path <pkg>` first.
- `startActivity` needs the main thread; do the file write in `Dispatchers.IO`
  and let the chooser launch on the caller.
