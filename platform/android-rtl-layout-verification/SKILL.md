---
name: android-rtl-layout-verification
description: "Prove an Android/Compose app's supportsRtl claim on a device — covers the two traps that produce a false \"clean\" sweep (developer-options force_rtl doing nothing, and a per-app ar-XB locale silently filtered out because the APK ships no pseudolocale resources), the mirroring control that exposes both, and the limit that en-XA cannot test expansion when UI strings are Kotlin literals. Use when checking RTL support, before claiming a layout mirrors correctly, or when an RTL sweep reports no problems."
---

# Android RTL layout verification

`android:supportsRtl="true"` is usually declared on day one and never exercised.
Verifying it is easy to get wrong: the two most obvious ways to force RTL both
fail **silently**, and the sweep then measures an LTR layout while reporting
"no problems".

## The rule

**Never report an RTL result without first proving the layout actually
mirrored.** Absence of defects in a configuration you failed to enter is not
evidence.

## Trap 1 — developer options `force_rtl` does nothing

```bash
adb shell settings put global debug.force_rtl 1
```

Writes the setting, readback confirms it, app relaunches — and positions are
byte-identical to LTR. It does not apply to a freshly launched app the way the
Settings toggle does.

## Trap 2 — per-app locale is filtered against shipped locales

```bash
adb shell cmd locale set-app-locales com.example.app --locales ar-XB
adb shell cmd locale get-app-locales com.example.app   # confirms [ar-XB]
```

The readback **lies about the effect**: per-app locales are resolved against the
locales the APK actually contains. If the build ships no `ar-XB` resources the
request falls back to the default locale, and the app runs LTR in English.

Fix — ship the pseudolocale resources in debug builds:

```kotlin
buildTypes {
    debug {
        isPseudoLocalesEnabled = true   // adds en-XA / ar-XB resources
    }
}
```

## The control that settles it

Capture one screen's element positions in each state and require movement:

```python
def snap():                       # force-stop, launch, uiautomator dump
    ...                           # -> {text: (x1, x2)}

adb shell cmd locale set-app-locales <pkg> --locales ""      # LTR
ltr = snap()
adb shell cmd locale set-app-locales <pkg> --locales ar-XB   # RTL
rtl = snap()
assert any(ltr[k] != rtl[k] for k in shared_keys)            # else: not RTL
```

A genuine flip looks like `HUNTER ltr=(195,479) rtl=(601,885)`. Identical
tuples mean you are still in LTR — stop and fix the configuration.

## The sweep, once RTL is proven live

Per destination, from the uiautomator dump:

- **off-screen**: any text node with `x1 < 0` or `x2 > screen_width`
- **squished**: `len(text) > 3 and width < 90 and height > 2 * width`
  (the one-letter-per-line shape)
- crash buffer empty (`adb shell logcat -d -b crash`)

Static audit alongside it — these are the APIs that break mirroring, and zero
hits is a meaningful result because Compose's `start`/`end` modifiers mirror
automatically:

```
AbsoluteAlignment | Alignment.(Top|Bottom|Center)(Left|Right)
TextAlign.(Left|Right) | absolutePadding | absoluteOffset
```

## Limit worth stating rather than hiding

`en-XA` (the expansion pseudolocale) only expands **resource** strings. If the
UI uses Kotlin string literals, en-XA changes nothing and cannot test text
expansion. Say so, and cover expansion with the font-scale axis (1.5×/2.0×)
instead of implying pseudolocale coverage you do not have.

## Restore the device afterwards

```bash
adb shell cmd locale set-app-locales <pkg> --locales ""
adb shell settings put global debug.force_rtl 0
```
