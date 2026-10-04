---
name: spark-component-accessibility-identifier
description: Create or update a accessibility identifier file in the AccessibilityIdentifier folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an accessibility identifier in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-accessibility-identifier button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *accessibility identifier* and the *unit tests*.

## Best pratices
  - Is *public*
  - must contains only *static let*
  - must contains *view* or the name of the component *xxx* equals to "spark-xxx"
  - documented

## Workflow
  - Add/Update the code.
  - Add/Update the documentation if the accessibility identifier is public.
  - Implement the unit tests.

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