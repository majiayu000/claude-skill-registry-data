---
name: global-installer
description: Install global dependencies to the system. These are typically installing using `brew`
---

# Global Installer

## Instructions
When installing system packages (ex: `git`, `gcloud`, etc.):
1. Use a WebSearch to check how to install the package. Check to see if it can be installed using `brew`
  - ALWAYS install using `brew` if it's an option
2. If the output of the installation command indicates that the package requires some initialization steps, ask the user for permission to execute it using the AskUserQuestion tool 
3. After finishing the execution, read `$HOME/Justfile` and update it with the installation command and the necessary setup
4. If the installation updated the `.zshrc` file automatically or if you modified in step 2, add a comment that CLEARLY indicates what package the code is for
