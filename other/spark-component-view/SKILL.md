---
name: spark-component-view
description: Create or update an view files for UIKit and SwiftUI in the View folder in Sources of a spark-ios-component-XXX.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an SwiftUI and UIKit *view* in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-view button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the swiftUI and UIKit *views*.

## Rules

### UIKit

- Respect the order of conception with *mark* (Components, Public Properties, ...) as the file in **template**.
- Respect the same naming as the file in **template**.
- Can inherits UIView or UIControl. If it is no precise in prompt, use the UIView.

### SwiftUI

- Respect the order of conception with *mark* (Components, Public Properties, ...) as the file in **template**.
- Respect the same naming as the file in **template**.
- Add dynamic type (on the component declaration) only if it is asked. Manage all the possible inits : Put them in the other file if there is many public init (more than 4)

## Workflow
  - [ ] Read the templates
  - [ ] Add/Update the code.

### Code Conventions
- [ ] File headers follow pattern: `Created by {firstname.lastname} on DD/MM/YYYY`
- [ ] Copyright line includes current year
- [ ] No empty lines contain whitespace or tabs
- [ ] All class members accessed with `self.`
- [ ] Protocol marked with `// sourcery: AutoMockable`
- [ ] Proper MARK comments in place