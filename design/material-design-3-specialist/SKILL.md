---
name: Material Design 3 Specialist
description: Expert instructions for implementing modern UI components and theming using Material Design 3.
---

# Material Design 3 Specialist

This skill provides guidelines and patterns for implementing Material Design 3 (M3) in the Android application.

## Core Concepts
- **Dynamic Color**: Use color roles (e.g., `colorPrimary`, `colorOnSurface`) rather than hardcoded hex values to support dynamic theming.
- **Components**: Prefer M3 components (`com.google.android.material.*`) over legacy widgets.

## Component Migrations

### Buttons
**Legacy**: `android.widget.Button`
**Material 3**: `com.google.android.material.button.MaterialButton`
- Use styles like `style="@style/Widget.Material3.Button.Tonal"` for hierarchy.

### Text Fields
**Legacy**: `android.widget.EditText`
**Material 3**: `com.google.android.material.textfield.TextInputLayout` wrapping `com.google.android.material.textfield.TextInputEditText`.
```xml
<com.google.android.material.textfield.TextInputLayout
    style="@style/Widget.Material3.TextInputLayout.OutlinedBox">
    <com.google.android.material.textfield.TextInputEditText />
</com.google.android.material.textfield.TextInputLayout>
```

### Cards
**Legacy**: `androidx.cardview.widget.CardView`
**Material 3**: `com.google.android.material.card.MaterialCardView`
- Use `style="@style/Widget.Material3.CardView.Filled"` (or Outlined/Elevated).

## Typography
Use the M3 type scale:
- `?attr/textAppearanceDisplayLarge`
- `?attr/textAppearanceHeadlineMedium`
- `?attr/textAppearanceBodyMedium`
- `?attr/textAppearanceLabelSmall`

## Theming
Ensure `themes.xml` inherits from `Theme.Material3.*`.
