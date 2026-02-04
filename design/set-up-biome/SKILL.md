---
name: set-up-biome
description: Set up configuratin files for the React project (Biome, Shadcn/UI)
allowed-tools:
  - Read(*)
  - Write(*)
  - WebFetch(*)
---

# Instruction

Your task is to set up and complete configurations for the project to reflect the user's preferences referring to provided instruction details and template files.

## Steps to follow

- Analyze the project structure and installed libraries and existing configuration files to determine the best way to integrate them.
- Check the existing configuration files and settings of the project to plan how to integrate configurations.
- Ask the user which configuration options to apply based on your analysis.
- When there's an existing configuration in the project (e.g., existing linter or formatter), ask the user how to handle potential conflicts or merges.

## Instruction details and template files:

### Shadcn/UI with Base UI

- Refer to the detail instruction: `shadcn-baseui.md`

### Biome configuration

- Refer biome settings of user preferences: `biome.jsonc`
- Check the project's framework (e.g., Next.js, React Router, TanStack Router) to taior the Biome settings accordingly, especially for ignoring file patterns.
- Use `.jsonc` format for Biome configuration.
- If there's an existing Biome configuration (biome.json or biome.jsonc), ask the user how to merge the new settings with the existing ones.
- Use appropriate Biome version schema based on the installed Biome in the project (if any) or install the latest Biome if not present.

### pnpm configuration

WARNING: Apply this only when the project uses `pnpm` as the package manager.

- Refer to the detail instruction: `pnpm.md`
