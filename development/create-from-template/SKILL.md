---
name: create-from-template
description: Create a new app or package from an existing template in the monorepo. Use when adding new apps or packages to the repository.
---

# Create a New App or Package From a Template

## Overview
Create a new app or package in the monorepo using an existing template.

## Workflow
1. Identify the template to use from `dev/templates` and the target location in the monorepo (`dev/apps` or `dev/packages`).
2. Copy the template directory to the target location and rename it appropriately. Skip copying `coverage`, `dist`, `node_modules`, and `.react-router` directories.
3. Update any necessary configuration files (e.g., `package.json`) to reflect the new app or package name.
4. The template apps and packages are located one level deeper in the directory structure (e.g., `dev/templates/apps/react` vs. `dev/apps/some-app`).
   1. Some configuration files referring to shared paths will need to be adjusted. For example, in `.stylelintrc.json` the path `../../../config/stylelint/.stylelintrc.json` => `../../config/stylelint/.stylelintrc.json`
   2. Same is true for `tsconfig.json`, `tsconfig.build.json`, and `postcss.config.cjs` among others.
5. Update the `README.md` file to reflect what you know about the new app or package.
6. Install dependencies and verify the new app or package builds and runs correctly.
