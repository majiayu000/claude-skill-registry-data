---
name: tools-speckit-init
description: Initialize a new directory with spec-kit (specify) and install the spec-kit-sync extension
argument-hint: <directory-name>  (e.g. my-new-component)
---

This skill creates a new directory, initializes it with `specify init . --ai claude`, and installs the `spec-kit-sync` extension.

## Input

The user must provide a directory name as an argument (e.g. `/tools-speckit-init my-new-component`).

If no argument is provided, show the hint and stop.

## Prerequisites

- `specify` must be installed and available on PATH (`which specify` should succeed)
- If not installed, inform the user that `specify` is required and stop

## Steps

1. Verify that `specify` is installed by running `which specify`. If it fails, tell the user to install specify first and stop.

2. Check that the target directory does not already exist. If it does, inform the user and stop.

3. Create the new directory:
   ```bash
   mkdir -p <directory-name>
   ```

4. Initialize spec-kit in the new directory:
   ```bash
   cd <directory-name> && specify init . --ai claude
   ```

5. Install the spec-kit-sync extension:
   ```bash
   cd <directory-name> && specify extension add spec-kit-sync --from https://github.com/bgervin/spec-kit-sync/archive/refs/heads/master.zip
   ```

6. Report success and tell the user:
   - The directory has been created and initialized
   - spec-kit-sync extension has been installed
   - They can now use specify commands in the new directory (e.g. `/speckit-specify`, `/speckit-clarify`)
   - The path to the new directory

## Notes

- The directory is created relative to the current working directory
- If `specify init` or the extension install fails, report the error to the user with the command output
