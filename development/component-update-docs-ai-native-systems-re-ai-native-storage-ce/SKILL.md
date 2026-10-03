---
name: component-update-docs
description: Ensure the per-component README.md are up to date and correctly reflect the code.
argument-hint: "[component-name, component-name, ...]"
---

Update the individual component README.md files at the root of each component's source directory.  component-framework can be omitted.  Make sure each README.md includes a summary of the component, how it is structed, and how to build and test.  If $ARGUMENTS are provided, only update components listed in the arguments, otherwise update all components.
