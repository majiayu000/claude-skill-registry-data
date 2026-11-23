---
name: cli-design
description: "Use when designing, building, reviewing, or testing CLI commands, argument parsers, help, output, errors, prompts, configuration, shell completion, accessibility, or behavior in terminals, pipelines, and CI, including installer prompts on Unix and Windows/PowerShell."
license: Apache-2.0
metadata:
  last-updated: "2026-10-22"
---

# Context Router

Choose the reference for the command-line design or review task. Preserve the documented Unix/POSIX and Windows/PowerShell distinctions.

| Topic | Open when | Read |
| --- | --- | --- |
| Arguments and Flags | Open when designing or reviewing CLI operands, flag names, defaults, required options, or safe secret input. | [Arguments and Flags](references/arguments-and-flags.md) |
| Option Parsing and Platforms | Open when implementing option parsing, optional values, repeated flags, globbing, or Unix and Windows/PowerShell parsing differences. | [Option Parsing and Platforms](references/option-parsing-and-platforms.md) |
| Subcommands and Command Shape | Open when organizing CLI subcommands, choosing command names or word order, or reviewing command consistency. | [Subcommands and Command Shape](references/subcommands-and-command-shape.md) |
| Prompts and Confirmation | Open when adding interactive prompts, confirmation for destructive actions, or ways to run without prompting. | [Prompts and Confirmation](references/prompts-and-confirmation.md) |
| Help and Usage Text | Open when writing CLI help, usage syntax, or examples, or deciding help output streams and exit status. | [Help and Usage Text](references/help-and-usage.md) |
| Discovery, Completion, and CLI Documentation | Open when designing command discovery, typo suggestions, shell completion, man pages, or links to CLI documentation. | [Discovery, Completion, and CLI Documentation](references/discovery-completion-and-docs.md) |
| Output and Formatting | Open when choosing CLI output formats, JSON or plain-text modes, tables, paging, verbosity, or success messages. | [Output and Formatting](references/output-and-formatting.md) |
| Color and Styling | Open when adding CLI color or styling, honoring NO_COLOR and TTY detection, or supporting terminal themes and Windows VT. | [Color and Styling](references/color-and-styling.md) |
| Errors and Exit Codes | Open when writing actionable CLI errors, assigning exit codes, or handling reserved and platform-specific exit statuses. | [Errors and Exit Codes](references/errors-and-exit-codes.md) |
| Streams and Piping | Open when separating stdout and stderr, accepting stdin, using '-' for streams, or handling pipelines and broken pipes. | [Streams and Piping](references/streams-and-piping.md) |
| Progress and Feedback | Open when adding progress bars, spinners, status feedback, or failure logs for long-running CLI operations. | [Progress and Feedback](references/progress-and-feedback.md) |
| Interactivity, TTY, and CI | Open when adapting a CLI to terminals, redirected streams, unattended runs, or CI, including TTY detection, --no-input, and signals. | [Interactivity, TTY, and CI](references/interactivity-tty-and-ci.md) |
| Configuration, Environment, and Precedence | Open when choosing CLI configuration sources, resolving flag/environment/file precedence, locating config files, or protecting secrets. | [Configuration, Environment, and Precedence](references/config-env-and-precedence.md) |
| Accessibility and Internationalization | Open when making CLI output accessible to screen readers, usable without color, or safe across locales and display widths. | [Accessibility and Internationalization](references/accessibility-and-i18n.md) |
| Testing CLI UX | Open when testing CLI exit codes, stdout, stderr, JSON output, or behavior in terminals, pipelines, and CI. | [Testing CLI UX](references/testing-cli-ux.md) |
| CLI Design Review Checklist | Open when reviewing an existing CLI against a design checklist and reporting findings by severity. | [CLI Design Review Checklist](references/cli-design-review.md) |

Open the [reference index](references/INDEX.md) or [topic catalog](references/topics.json) for broader topic lookup.

# Language Translations

[Reference Language Selection](references/languages.md)

# Context For Open Source

Skill reference documentation is interpreted content for use in open source projects. Check against [official documentation sources](https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces) when dealing with defects or issues that may come up from interpreting this skill's references.
