---
name: spark-component-environment
description: Create or update an environment file in the Environment folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an *environment* in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-environment button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *environment*.

## Rules

The Environment file must respect theses rules : 
  - must be located in *Sources/Core/Environment*.
  - should contains an EnvironmentValues extension with just one *@Entry var*. The prefix of this variable must the name of the component
  - should contains a *public extension View* to set the *EnvironmentValues*. This func must be documented. The name of the func must start by *sparkXXX*.

## Workflow
  - [ ] Add/Update the code.
  - [ ] Run swiftlint ```$ swiftlint```.

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