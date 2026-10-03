---
name: component-make-new-actor
description: Create a new actor component skeleton
argument-hint: "[component-name, receptacle-names,...]"
---

Building the skeleton for component named $0 involves the following steps:

1. The interface name is the component name prefixed with the letter 'I'.  The component name is $0, e.g., FooBar is the component name, IFooBar is its interface name.

2. The component should be an actor. It must support an actor channel and provide a method on the interface to open the channels.  Implement a skeleton message protocol along with the interface definition.

3. If it does not already exist, create interface definition file, e.g., ifoobar.rs in components/interfaces directory.

4. Interactively ask if any other interfaces will be provided by this component. 

5. Create a new sub-directory under the components directory.  The name of the directory is a lower-case hyphen-ized version of $0.

6. Implement dummy functions for all provided interfaces.

7. Add recepticals for other interface names specified by other arguments, $1, $2 and so forth.  The receptable must have a corresponding interface defined in src/interfaces.

8. Add a permissions file .claude/settings.json, in the newly created sub-directory, that allows access to the component itself, components/component-framework and any other directories corresponding to components that are listed as receptacles.  We want to avoid giving access to other components that are not directly used.

9. Copy skills, except those named 'component-make-new' or 'component-make-new-factor' from .claude/skills into the new component directory's .claude/skills.

10. Run 'specify init . --ai claude' in the component source directory.

11. Run 'specify extension add spec-kit-sync --from https://github.com/bgervin/spec-kit-sync/archive/refs/heads/master.zip' in the component directory.


