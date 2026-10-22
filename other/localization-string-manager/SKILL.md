---
name: Localization & String Manager
description: Instructions for managing bilingual resources (English/Traditional Chinese) on Android.
---

# Localization & String Manager

This skill enforces strict bilingual support and prevents hardcoded strings.

## Rule #1: No Hardcoded Strings
**Never** use raw strings in XML layouts (`android:text="Hello"`) or Java code (`setText("Hello")`).
**Always** use resource references (`android:text="@string/hello"` or `getString(R.string.hello)`).

## File Structure
- **Default (English fallback)**: `res/values/strings.xml`
- **Traditional Chinese (Taiwan)**: `res/values-zh-rTW/strings.xml`

## Adding a New String
When adding a new UI element, you must add the string to **BOTH** files.

1.  **Define Key**: Use snake_case for IDs (e.g., `settings_enable_vibration`).
2.  **Add to `values/strings.xml`**:
    ```xml
    <string name="settings_enable_vibration">Enable Vibration</string>
    ```
3.  **Add to `values-zh-rTW/strings.xml`**:
    ```xml
    <string name="settings_enable_vibration">開啟震動</string>
    ```

## Formatting
- Use `%s`, `%d` for dynamic content.
- `getString(R.string.welcome_user, username)`
