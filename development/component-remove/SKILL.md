---
name: component-remove
description: Remove a component from the code base.
argument-hint: "[component-name]"
---

Building the skeleton for component named $0 involves the following steps:

1. Component name is $0.  Check the component exists otherwise return an error and stop.
2. Interactively check with the user that they are sure that they want to delete this component. Stop if they do not.
3. Remove directory for the component.
4. Remove corresponding interfaces from the component/interfaces crate except interfaces that are needed by other components.
5. Remove component build from all Cargo.toml files.


