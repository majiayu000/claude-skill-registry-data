---
name: node-ts-cli
description: Generate new Node.js CLI tool projects using TypeScript with ESM modules, tsc for building, tsx for development, Biome for linting/formatting, and Node's built-in test runner. Use this skill when the user requests to create a new Node TypeScript CLI project or CLI tool.
---

# Node TypeScript CLI Generator

## Overview

Generate production-ready Node.js CLI tool projects configured with TypeScript, ESM modules, and modern tooling. Each generated project includes a complete setup with build scripts, development workflow, testing, and linting.

## When to Use This Skill

Use this skill when the user requests:
- "Create a new Node TypeScript CLI tool"
- "Generate a CLI project in TypeScript"
- "Set up a new TypeScript CLI"
- "Make me a Node.js command-line tool"

## Project Setup

### Quick Start

To generate a new CLI project:

1. Specify the project name and desired CLI command name.
2. The skill will create a new directory unless specified otherwise.
3. Inside the directory, the skill will perform the following steps:
4. Initialize a new Git repository.
5. Run `npm init -y` to initialize a new npm project.
6. Run `npm i -D typescript @types/node @biomejs/biome` to install dev dependencies.
7. Run `npm i @clack/prompts` to install runtime dependencies.
8. Run `npx tsc --init` to create a `tsconfig.json` file.
9. Run `npx biome init` to create a `biome.json` file.
10. Set up the `package.json`, `tsconfig.json`, and `biome.json` files with the appropriate configurations.
11. Create the necessary source files in `src/` including `index.ts` with a basic CLI structure using the `@clack/prompts` library.
12. Create example test files in `src/` to demonstrate testing with Node's built-in test runner.
13. Add npm scripts for building, developing, testing, linting, and formatting.
14. Inform the user about the available npm scripts

### Technology Stack

The generated project uses:
- **TypeScript** with strict mode enabled
- **ESM modules** (type: "module")
- **tsc** for building production builds to `./dist`
- **tsx** for running TypeScript directly in development
- **Biome** for fast linting and formatting
- **Node's built-in test runner** with TypeScript support via `--experimental-strip-types`

### Available NPM Scripts

Each generated project includes these scripts:

- `npm run build` - Compile TypeScript to JavaScript in `./dist`
- `npm run dev` - Run the CLI in development mode with tsx
- `npm run test` - Run tests with Node's built-in test runner
- `npm run lint` - Check code with Biome
- `npm run lint:fix` - Fix linting issues automatically
- `npm run format` - Format code with Biome

### Project Configuration

**package.json**
- Configured as ESM with `"type": "module"`
- Includes `bin` field for CLI installation
- Main entry points to `./dist/index.js`

**tsconfig.json**
- Target: ES2022
- Module: ESNext with bundler resolution
- Outputs to `./dist`, sources from `./src`
- Strict mode enabled
- Generates declaration files and source maps

**biome.json**
- Enables linting with recommended rules
- Configured to format code on save

### CLI Entry Point Structure

The template `src/index.ts` includes:
- Shebang for executable scripts (`#!/usr/bin/env node`)
- Argument parsing with help and version flags for non-interactive use
- Interactive prompts using `@clack/prompts`
- Async main function with error handling
- Process exit codes for proper CLI behavior

### Customization After Generation

After generating a project, users should:
1. Update `name` and `description` in `package.json`
2. Update the `bin` command name in `package.json`
3. Set the `author` and `license` fields
4. Update version number in both `package.json` and `src/index.ts` showVersion()
5. Modify `src/index.ts` with their CLI logic
6. Update the README with specific usage instructions

### Installation for Users

After building the project, users can:
- Run locally: `node dist/index.js`
- Install globally: `npm install -g .` then use the bin command
- Publish to npm and install: `npm install -g package-name`

## Example Usage

When a user says: "Create a new TypeScript CLI tool called todo-manager"

1. Run the project generation steps outlined above
2. Update `package.json`:
   - Change `"name"` to `"todo-manager"`
   - Update `"description"` appropriately
   - Change `bin` to `"todo-manager": "./dist/index.js"`
3. Update README.md with the project name
4. Run `npm install` in the project directory
5. Inform the user: "Project created! Run `npm run dev` to start developing, or `npm run build` to compile."