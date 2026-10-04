---
name: spark-component-snapshots-testing
description: Create or update the snapshots testing for a spark-ios-component-XXX.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update the *snapshots testing* in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-snapshots-testing button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *snapshots testing* for the View in the *code* folder.

## Rules

The Snapshots file must respect theses rules : 
  - must be located in *Tests/SnapshotTests*.
  - should contains a *configuration* which contains all variable to customize the component.
  - should contains a *scenarios* which contains all tests func to tests all configuration. Contains also a documentation func used to generate the snapshots for the Documentation.
  
## Workflow
  - [ ] Read the content of the *SparkXXX* and *SparkUIXXX* 
  - [ ] Create or update the configuration in the *Tests/SnapshotTests/Common*.
  - [ ] Create or update the list of scenarios in the *Tests/SnapshotTests/Common*.
  - [ ] Create or update the snapshots for UIKit and SwiftUI
  - [ ] Run swiftlint ```$ swiftlint```.
  - [ ] Run sourcery ```$ sourcery```
  - [ ] Implement the unit tests. Read theses folders to get mocks :
    - *spark-ios-common/Sources/SnapshotTesting*

### Code Conventions
- [ ] File headers follow pattern: `Created by {firstname.lastname} on DD/MM/YYYY`
- [ ] Copyright line includes current year
- [ ] No empty lines contain whitespace or tabs
- [ ] All class members accessed with `self.`
- [ ] Proper MARK comments in place

### Test Implementation
- [ ] Proper imports (SparkComponentXXX, SparkCommon, SparkTheming, @testable, @_spi(SI_SPI) @testable import SparkComponentXXXTesting, Testing, ...)