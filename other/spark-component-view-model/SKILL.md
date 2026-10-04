---
name: spark-component-view-model
description: Create or update an view model file in the ViewModel folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an *view model* in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-view-model button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *view model* and the *unit tests*.

## Rules

The ViewModel file must respect theses rules : 
  - must be located in *Sources/Core/ViewModel* and in *Tests/UnitTests/ViewModel*.
  - should contains `final class` implementation.
  - should have this comment before the *final class* ```// sourcery: AutoPublisherTest, AutoViewModelStub```
  - if there is ``@Published private(set)`` with an ``any XXX``, add before the func ```// sourcery: nameOfProperty = "Identical"```. Replace *nameOfProperty* by the real name of the variable
  - must contains only : 
    1. some *@Published private(set) var* that only set by use cases and consume by the views
    2. some *var*. Setted by the views and the setup function. Manage the *didSet* to call use case if it is needed
    3. A *private var alreadyUpdateAll* use to know if the viewModel is setup are not.
    4. A list of usecase used by the viewmodel to set the *@Published* properties.
    5. The init with all use cases (and with the default implementation)
    6. The *setup* func with all needed properties send by the init. Set the *alreadyUpdateAll* to *true*.
    7. The private setter func. Use to set *@Published* from use cases.
  - unit testing : use the same logic/conception as the test file in template. 

## Workflow
  - [ ] Add/Update the code.
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