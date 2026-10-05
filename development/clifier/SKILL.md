---
name: clifier
description: Create production-ready website-automation CLI packages in TypeScript for Deno, including a CLI plus companion client library, for repeatable website workflows such as scraping, form submission, downloads, login/bootstrap flows, session reuse, stable JSON output, and optional `deno compile` packaging. Use when the Agent needs to turn a website task into a reusable tool.
---

# Clifier

Generate a reusable website-automation package, not a one-off script. Default to
a Deno CLI plus a runtime-neutral client library. Keep the result concise,
polished, and JSR-ready.

Bias toward small, sharp, readable software: production-ready, highly usable,
and free of wasted motion.

Use references progressively. Read only what the current step needs:

- command surface:
  [references/cli-command-patterns.md](references/cli-command-patterns.md)
- site investigation:
  [references/investigation-workflow.md](references/investigation-workflow.md)
- runtime choice:
  [references/fetch-vs-playwright.md](references/fetch-vs-playwright.md)
- auth/session reuse:
  [references/auth-and-session.md](references/auth-and-session.md)
- docs/output: [references/output-and-docs.md](references/output-and-docs.md)
- JSR packaging: [references/jsr-publishing.md](references/jsr-publishing.md)

## Workflow

1. Define the CLI first.
2. Investigate the site with `playwright-cli`.
3. Prove or disprove `fetch`.
4. Decide on `fetch`, hybrid, or `playwright-cli`-backed browser automation.
5. Generate from `assets/templates/deno-cli/`.
6. Validate the happy path and publishability.

## Define The CLI

Read [references/cli-command-patterns.md](references/cli-command-patterns.md)
before naming commands.

- Prefer product nouns, then verbs.
- Use direct top-level verbs only for cross-cutting commands such as `login`.
- Prefer `@cliffy/command` for Deno CLIs.
- Keep the CLI thin: parse flags, call library code, format output, and handle
  Deno-specific filesystem or session work.
- Always include a root `-v, --version` flag.
- Keep the surface small, predictable, and guessable from the product
  vocabulary.
- Make the happy path obvious from `--help`.
- Map meaningful UI controls to flags before finalizing commands.
- Give high-value explicit flags a shorthand alias when it is clear and
  memorable, such as `--session-path`/`-s` and `--out`/`-o`.
- Put global flags before the command path in docs, help examples, and
  agent-facing snippets, such as
  `tool-name --json --session-path ~/.auth/acme@my-tool.json jobs get <job-id>`.
  Keep command-specific flags near the command they configure, such as
  `tool-name --json jobs download <job-id> --out ./downloads`.
- Keep operational commands non-interactive after auth/bootstrap.
- Emit stable IDs from create-style commands and accept them directly in
  follow-up commands.
- Keep only commands that deliver real value. Do not keep `doctor`, `login`, or
  other template-era commands unless the real tool needs them.

## Investigate

Read
[references/investigation-workflow.md](references/investigation-workflow.md)
before implementing.

- Use `playwright-cli` for discovery and for unavoidable browser automation. Do
  not build the generated package around the vanilla Playwright runtime.
- Default to Chrome unless the user or site requires another browser.
- Reproduce one real happy-path run.
- Capture only the requests, identifiers, auth inputs, downloads, and UI
  controls that matter.
- Ask the user for manual login, MFA, sample inputs, or copied cookies or
  headers when needed.
- Clean up temporary investigation artifacts unless they are intentionally
  reused by the generated tool.

## Choose Runtime

Read [references/fetch-vs-playwright.md](references/fetch-vs-playwright.md)
before deciding.

- Prefer `fetch`.
- Use hybrid only when `playwright-cli` is needed for login or bootstrap and the
  saved state can be translated into the exact runtime cookies, headers, tokens,
  CSRF values, or other inputs that `fetch` needs.
- Use `playwright-cli`-backed browser automation only after a serious failed
  attempt to make `fetch` or hybrid work.
- Explain briefly what was investigated, how auth works at runtime, and why the
  chosen runtime is the simplest robust option.
- Validate at least one authenticated `fetch` request before calling a hybrid
  design production-ready.

## Handle Auth

Read [references/auth-and-session.md](references/auth-and-session.md) when auth
is required.

- Prefer explicit flags and environment variables.
- Do not add a general config file by default.
- For browser-login flows, default session storage to
  `~/.auth/<project_namespace>@<project_repo>.json`, resolving `~` through the
  OS home directory. For a JSR name such as `@acme/my-tool`, use
  `~/.auth/acme@my-tool.json`.
- Keep `--session-path, -s <path>` as the explicit override on `login` and later
  authenticated commands.
- When a tool supports multiple auth bootstrap methods, prefer an `auth` noun
  group and validate any automatic cookie discovery against the target site.
- Never assume browser storage state is sufficient for plain `fetch`; prove how
  runtime auth is constructed.
- Keep secrets out of normal output, `--json` output, and repo files.

## Generate The Tool

Start from `assets/templates/deno-cli/`.

- Prefer the simplest clear implementation.
- Keep the package root for the library and export the CLI from `./cli`.
- Keep `mod.ts` as the public library root and `cli.ts` as the Deno CLI
  entrypoint.
- Keep code compact and readable.
- Prefer expressive names and straightforward structure.
- Keep runtime-neutral client code under `lib/`.
- Include `deno compile` tasks for all supported Deno targets.
- Keep compiled binaries under `bin/`.
- Make `compile` the aggregate task that builds every supported target, and add
  one task per target for direct use.
- Include Deno helper task(s) for reading `deno.json.version` and comparing it
  to the previous git ref used by the release workflow.
- Include a GitHub Actions release workflow that watches `deno.json.version`,
  uses the Deno version helper task(s), compiles all targets, creates a GitHub
  Release with the binaries, and publishes to JSR.
- Include `name`, `version`, `exports`, and `deno publish --dry-run` validation.
- Treat `deno.json` as the single source of truth for package and CLI version
  metadata. Do not duplicate the version string in `cli.ts`.
- Avoid indirection unless it earns its keep.
- Make the intent obvious from names, control flow, and file layout.
- Prefer code that is easy to scan over clever or aggressively compressed code.
- Favor direct solutions over ceremony, helper churn, or architecture that only
  serves the template.
- Detect missing mandatory runtime dependencies and print exact install
  instructions when a command needs them.
- Remove template placeholder text, example commands, and unused support files
  from the final generated package.
- Remove scaffolding layers that do not improve usability.

## Finish

Read [references/output-and-docs.md](references/output-and-docs.md) while
polishing the result.

- Deliver concise human output, stable JSON, useful errors, and clear next-step
  affordances.
- Include a root `README.md` and a root `COMMANDS.md`.
- Make `COMMANDS.md` a cheat sheet: short, scan-friendly, and centered on
  copy-pasteable CLI invocations rather than prose.
- Keep command names, help text, docs, and examples aligned.
- When the tool depends on `playwright-cli`, browser binaries, or other
  non-bundled runtime dependencies, validate the missing-dependency path too.
- Validate `--help`, `deno task check`, the happy path, and
  `deno publish --dry-run`.
- Validate a real invocation path users will actually use, not only local task
  wrappers.
