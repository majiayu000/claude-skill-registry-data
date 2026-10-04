---
name: spark-component-token
description: Create or update a token file in the Token folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update a token in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-token button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *token* and the *unit tests*. See `Modules/Components/Chip/Sources/Core/Token` for a full real-world example.

> The template uses `Border`, `Size`, and `Typography` purely as illustrations of three recurring *patterns* (see Rules below). A real component's token categories are whatever it actually needs — e.g. `Opacity`, `Layout`, `Spacing`, `Color`, `Icon`, `Animation`, ... Determine the category names and count from the component's design/usage, not from the template names.

## Rules

The Token file must respect theses rules :
  - must be located in *Sources/Core/Token* and in *Tests/UnitTests/Token*.
  - the root file is named *XXXToken.swift* and contains a `public struct XXXToken: Equatable` with one property per token category the component actually needs (there is no fixed list or fixed count — could be one category or a dozen), plus a `public init(theme: any Theme)` that forwards the theme to every category that needs it.
  - each token category lives in its own file named *XXXToken+CategoryName.swift* (e.g. `XXXToken+Opacity.swift`), containing a `public extension XXXToken` with a nested `struct CategoryName: Equatable`.
  - a category that only exposes fixed constants (no theme-dependent values, illustrated by ``Size`` in the template) must have a parameterless `public init()`. On the root struct, its property is a stored default value (`public let size = Size()`), **not** assigned in the root `init(theme:)` body.
  - a category that depends on the theme (illustrated by ``Border`` in the template) must have `public init(theme: any Theme)`, and its property must be assigned in the root `init(theme:)`.
  - a category holding an `any ColorToken`, `any TypographyFontToken`, or any other non-natively-`Equatable` existential (illustrated by ``Typography`` in the template) must provide a manual `static func ==` using `.equals()` — the synthesized `Equatable` conformance does not work for existential protocol types.
  - every public struct and property must be documented with a doc comment (`///`).
  - the root *XXXToken.swift* file must have a top-level doc comment that:
    - lists every category actually present, each with a doc link (e.g. `` ``XXXToken/CategoryName``: description``)
    - includes a "Creating a Custom XXX" section with a full SwiftUI usage example
    - includes a section showing how to use individual sub-structs directly (e.g. a constant-only category instantiated without a theme, if the component has one)

## Workflow
  - [ ] Add/Update the code.
  - [ ] Add/Update the documentation (the token file and its categories are always public).
  - [ ] Run swiftlint ```$ swiftlint```.
  - [ ] Run sourcery ```$ sourcery```
  - [ ] Implement the unit tests. Read theses folders to get mocks :
    - *spark-ios-component-XXX/Sources/Testing*
    - *spark-ios-common/Sources/Testing*
    - *spark-ios-theming/Sources/Testing*

### Code Conventions
- [ ] File headers follow pattern: `Created by {firstname.lastname} on DD/MM/YYYY`
- [ ] Copyright line includes current year
- [ ] No empty lines contain whitespace or tabs
- [ ] All class members accessed with `self.`
- [ ] Protocol marked with `// sourcery: AutoMockable`
- [ ] Proper MARK comments in place

### Test Implementation
- [ ] Tests must be written in **Swift Testing** framework
- [ ] Proper imports (SparkComponentXXX, SparkCommon, SparkTheming, @testable, @_spi(SI_SPI) @testable import SparkComponentXXXTesting, Testing, ...)
- [ ] Use `ThemeGeneratedMock.mocked()` and `ThemeGeneratedMock.mocked2()` to cover theme-dependent values and equality/inequality
- [ ] For each category, test: initialization sets every property from the theme (or from its fixed constant), equatable returns true when equal, equatable returns false when different
- [ ] The root `XXXTokenTests` must verify that each property matches a freshly-constructed instance of its own sub-struct (e.g. `#expect(token.border == XXXToken.Border(theme: self.theme))`), plus equatable true/false at the root level

### When to Ask for Help

If you encounter:
- A token value that doesn't map to any existing theme property
- A property type that isn't natively `Equatable` and it's unclear whether a manual `==` is needed
- Component doesn't follow standard patterns

Use AskUserQuestion to clarify with the user before proceeding.
