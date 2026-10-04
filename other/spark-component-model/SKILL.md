---
name: spark-component-model
description: Create or update an model file in the Model folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an model in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-model button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *model* and the *unit tests*.

## Rules

The Model file must respect theses rules : 
  - must be located in *Sources/Core/Model* and in *Tests/UnitTests/Model*.
  - must be ``Equatable``
  - should add prefix on some properties :
    - *any TypographyFontToken* type -> var xxxFontToken (example: `titleFontToken`)
    - *any ColorToken* type -> var xxxColorToken (example: `tintColorToken`)

  - should have default values for all properties :
    - *CGSize* type -> .zero
    - *CGFloat* type -> .zero
    - *any TypographyFontToken* type -> TypographyFontTokenClear() (Must import ```@_spi(SI_SPI) import SparkTheming```)
    - *any ColorToken* type -> ColorTokenClear() (Must import ```@_spi(SI_SPI) import SparkTheming```)
    - *String* type -> .empty
    - *Number* type -> .zero

## Workflow
  - Add/Update the code.
  - Add/Update the documentation if the enum is public.
  - Run swiftlint ```$ swiftlint```.
  - Run sourcery ```$ sourcery```
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