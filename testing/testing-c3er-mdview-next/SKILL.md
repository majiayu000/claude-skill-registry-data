---
name: testing
description: "Use when running or planning unit tests or end-to-end tests for this project. Unit tests use npm test. End-to-end tests launch the real Electron application and UI, and require user approval before execution."
---

# Testing

Use this skill for test selection, execution, and reporting in the refactoring project.

## Unit tests

Run the unit-test suite with:

```sh
npm test
```

This command may be executed whenever useful for verification; it does not require additional user approval. Use it after focused implementation changes and before widening the scope of validation.

## End-to-end tests

The end-to-end suite launches the complete Electron application, including real browser windows and UI. Run it with:

```sh
env -u ELECTRON_RUN_AS_NODE npm run test-all
```

The `env -u ELECTRON_RUN_AS_NODE` prefix is required in the VS Code terminal environment used for this project. Without it, Electron may be started in Node mode and reject Playwright's launch arguments.

This command is currently Unix/macOS/Linux-oriented and depends on the Unix shell semantics of `env`. If the user is later working on Windows, ask for permission to extend this skill and the related startup guidance for that platform before using Windows-specific variants or commands.

This command also runs ESLint and the Prettier check before the tests.

Always ask the user for approval immediately before executing this command. It can open windows and otherwise distract the person in front of the screen. Do not treat approval for an earlier E2E run as approval for a later run.

## Validation and reporting

- Select the smallest relevant test command first.
- Report the exact command used and whether it passed or failed.
- Include the number of passing and failing tests when available.
- When an E2E run is requested or approved, mention that it exercised the real Electron UI.
- If the change affects visible or interactive behavior, provide a concise manual smoke-test sequence for the user when automated tests cannot establish the complete result.
- Do not claim that tests passed if setup, linting, formatting, or teardown failed.
