---
name: component-make-new
description: Create a new component skeleton
argument-hint: "[component-name, receptacle-names...]"
---

Building the skeleton for component named $0 involves the following steps:

1. The interface name is the component name prefixed with the letter 'I'.  The component name is $0, e.g., FooBar is the component name, IFooBar is its interface name.

2. If it does not already exist, create interface definition file, e.g., ifoobar.rs in components/interfaces directory.

3. Interactively ask if any other interfaces will be provided by this component. 

4. Create a new sub-directory under the components directory.  The name of the directory is a lower-case hyphen-ized version of $0.

5. Implement dummy functions for all provided interfaces.

6. Add recepticals for other interface names specified by other arguments, $1, $2 and so forth.  The receptable must have a corresponding interface defined in src/interfaces.

7. Add a permissions file .claude/settings.json, in the newly created sub-directory, that allows access to the component itself, components/component-framework and any other directories corresponding to components that are listed as receptacles.  We want to avoid giving access to other components that are not directly used.

8. Copy skills, except those named 'component-make-new' or 'component-make-new-factor' from .claude/skills into the new component directory's .claude/skills.

9. Run 'specify init . --ai claude' in the component source directory.

10. Run 'specify extension add spec-kit-sync --from https://github.com/bgervin/spec-kit-sync/archive/refs/heads/master.zip' in the component directory.




