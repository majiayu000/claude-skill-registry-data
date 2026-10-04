---
name: spark-component-enum
description: Create or update an enum file in the Enum folder in Sources of a spark-ios-component-XXX and add or update unit tests.
---

# Add Repository Skill

## Overview & Prerequisites

This skill guides you to implement/update an enum in spark component.

## Component Selection

**Parameter Handling:**
- If the skill is invoked with a parameter (e.g., `/spark-component-enum button`):
  - Use the parameter as the component name
  - Verify the folder exists in `Modules/Components/{component-name}/`
  - If found, use that component and skip the selection step

- If no parameter is provided:
  - List all folders in the `Modules/Components/` directory
  - Use AskUserQuestion to let the user select ONE component from the list
  - Format: Display folder names as options (e.g., "button", "card", "checkbox")

**Once the component is selected, all operations must be performed in `Modules/Components/{component-name}/` folder.**

Use the files in the **template** folder as reference to manage the *view model* and the *unit tests*.

## Best pratices
  - should have a `default` if the enum is public.
    If the default value is not indicate on the prompt, use *AskUserQuestion* to clarify with the user before proceeding. Replace the options by the list of all cases.

## Workflow
  - Add/Update the code.
  - Add/Update the documentation if the enum is public.
  - Run swiftlint ```$ swiftlint```.
  - Run sourcery ```$ sourcery```
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

### When to Ask for Help

If you encounter:
- Ambiguous module structure (can't determine where repos go)
- Complex YAML with unclear structure
- Component doesn't follow standard patterns

Use AskUserQuestion to clarify with the user before proceeding.

### Collect Missing Information

Use AskUserQuestion to gather any missing information (module name or operation) with clear UI (example for module below):

```typescript
AskUserQuestion({
  questions: [
    {
      question: "Which case is the default?",
      header: "Module",
      multiSelect: false,
      options: [
        {label: "case1"},
        {label: "case2"},
        {label: "caseX"}
      ]
    }
  ]
})
```