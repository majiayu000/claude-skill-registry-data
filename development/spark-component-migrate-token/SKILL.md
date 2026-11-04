---
name: spark-component-migrate-token
description: Migrate a spark-ios-component-XXX from use cases / models / view models to component tokens (XXXToken exposed through theme.component.xxx) consumed by the SwiftUI views through private view modifiers. Keeps the ViewModel and use cases still used by the UIKit component.
---

# Spark Component Migrate Token Skill

## Overview

This skill migrates the **SwiftUI** part of a component to the *component token* architecture introduced by `refactor/inputotp`
(see `Modules/Components/InputOTP` for the full real-world example, commit `refactor(inputotp): replace use cases and view models with tokens and view modifiers`).

Target architecture:

```
Theme
 └─ theme.component.xxx            -> ComponentToken+XXX.swift          (public)
     └─ XXXToken (+ categories)    -> Token/XXXToken(+Category).swift   (public, skill spark-component-token)
         └─ EnvironmentTheme.xxx   -> EnvironmentTheme+XXXToken.swift   (internal shortcuts)
             └─ ViewModifiers      -> ViewModifier/XXXYyyViewModifier.swift (private struct + internal View extension)
                 └─ SparkXXX (SwiftUI view, no ViewModel)
```

## Component Selection

- If the skill is invoked with a parameter (e.g., `/spark-component-migrate-token button`):
  - Use the parameter as the component name and verify the folder exists in `Modules/Components/{component-name}/`.
- If no parameter is provided:
  - List the folders in `Modules/Components/` and use AskUserQuestion to select ONE component.

**All operations are performed in `Modules/Components/{component-name}/`.**

## Step 0 — Analysis (mandatory, before any change)

1. List every UseCase, Model and ViewModel of the component.
2. Check if the component has a **UIKit** view (`SparkUIXXX`, `View/UIKit`, ...).
3. For each UseCase / Model / ViewModel, determine who uses it:
   - **only SwiftUI** -> it will be replaced and removed.
   - **UIKit (alone or with SwiftUI)** -> it **must be kept** (file + tests + Sourcery mocks), only the SwiftUI view stops using it.
4. Present the plan to the user (what is created, what is removed, what is kept for UIKit) and wait for confirmation if anything is ambiguous.

> ⚠️ Components not fully migrated still have a UIKit component relying on the ViewModel. **Never delete a ViewModel, UseCase or Model still referenced by UIKit code.** Delete only once there is no remaining reference (check with grep in `Sources`).

## Step 1 — Tokens

Use the skill **spark-component-token** to create `Sources/Core/Token/XXXToken.swift` and its categories
(`XXXToken+Colors.swift`, `+Border`, `+Layout`, `+Opacity`, `+Typography`, `+Size`, ...).

- Each styling UseCase + Model becomes a token category. A UseCase taking parameters (intent, state, isEnabled, ...) becomes a **public method** of the category (e.g. `func value(isEnabled: Bool) -> CGFloat`), a theme-dependent category stores `let theme: any Theme` and implements `==` with `theme.equals(...)`.
- Size constants previously in `Constants` move to the `Size` category (keep in `Constants` what is not a size/token value).
- Non styling rules (value formatting, validation, separator, ...) move to **internal extensions** in `Sources/Core/Extension/{Enum|Foundation|...}/Type+XXXExtension.swift` (e.g. `String+InputOTPExtension.swift`, `InputOTPDigits+SeparatorExtension.swift`).

## Step 2 — ComponentToken extension

`Sources/Core/Extension/Token/ComponentToken+XXX.swift` — see `template/ComponentToken+XXX.swift`.
Exposes the token publicly through `theme.component.xxx` (`ComponentToken` is defined in `Modules/Theming/Sources/Core/Component/ComponentToken.swift`).

## Step 3 — EnvironmentTheme extension

`Sources/Core/Extension/Token/EnvironmentTheme+XXXToken.swift` — see `template/EnvironmentTheme+XXXToken.swift`.
- **internal** extension (not public) with a private `token` property and one internal property per token category.
- Allows the views to write `self.theme.colors.xxx` with `@Environment(\.theme) private var theme`.

## Step 4 — View modifiers

`Sources/Core/ViewModifier/XXXYyyViewModifier.swift` — see `template/XXXOpacityViewModifier.swift` (example with opacity).
- One file per styling concern (opacity, padding, background, content, separator, ...).
- `private struct XXXYyyViewModifier: ViewModifier` reading `@Environment(\.theme)` (and other environment values like `isEnabled`).
- An **internal** `extension View { func xxxYyy(...) -> some View }`.
- The modifier only reads tokens, no business rules.

## Step 5 — SwiftUI views

- Remove the `@StateObject/@ObservedObject` ViewModel from the **SwiftUI** views (`SparkXXX`, internal SwiftUI subviews).
- Read the tokens with `self.theme.category.xxx` or apply the view modifiers.
- Do **not** touch the UIKit views (`SparkUIXXX`).

## Step 6 — Clean up

Only for what was flagged *SwiftUI only* in Step 0:
- Remove the UseCases, Models and ViewModels, and their unit tests.
- Remove their entries from `Sources/Testing` if needed, then run `sourcery`.
- Keep everything used by UIKit.
- Do not update Deprecated files/folders.

## Step 7 — Tests

- Run `sourcery` before writing tests.
- **Swift Testing** for all new tests (see `template/*Tests.swift`):
  - `Tests/UnitTests/Token/XXXToken(+Category)Tests.swift` (skill **spark-component-token**).
  - `Tests/UnitTests/Extension/ComponentToken+XXXTests.swift`.
  - `Tests/UnitTests/Extension/EnvironmentTheme+XXXTokenTests.swift`.
  - Tests for every new internal extension (`String+XXXExtensionTests.swift`, ...), covering all the cases of the removed use case tests.
- Update the snapshot tests if they used the ViewModel (skill **spark-component-snapshots-testing**), then re-record and update the DocC images if the rendering changed.

## Step 8 — Documentation

- Update `Documentation.docc/Documentation.md`: add a *Token* section listing `XXXToken` and `theme.component.xxx`.
- Use the skill **spark-component-documentation** if needed.

## Workflow

- [ ] Step 0 analysis presented (created / removed / kept for UIKit)
- [ ] Tokens (spark-component-token)
- [ ] ComponentToken+XXX
- [ ] EnvironmentTheme+XXXToken
- [ ] View modifiers
- [ ] SwiftUI views migrated, UIKit untouched
- [ ] SwiftUI-only UseCases/Models/ViewModels removed (UIKit ones kept)
- [ ] `sourcery`
- [ ] Unit tests (Swift Testing)
- [ ] Snapshot tests / DocC images
- [ ] `swiftlint` (no errors)
- [ ] Build & tests green

### Code Conventions
- [ ] File headers: `Created by {Firstname Lastname} on DD/MM/YYYY`, copyright current year for new files (keep the year of existing files)
- [ ] No empty lines containing whitespace
- [ ] All members accessed with `self.`
- [ ] Proper `// MARK: -` comments
- [ ] `@_spi(SI_SPI)` imports where needed
- [ ] Single `return switch` when each case returns a value

## When to Ask for Help

Use AskUserQuestion if:
- It's unclear whether a UseCase / ViewModel is still used by UIKit.
- A use case mixes styling and business rules.
- A value doesn't map to any theme property.
