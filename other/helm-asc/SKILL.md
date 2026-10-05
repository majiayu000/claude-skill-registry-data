---
name: helm-asc
description: Use this skill whenever the task involves `helm-asc`, the Helm CLI, or App Store Connect automation through Helm. Trigger for app discovery, versions, localizations, screenshots, previews, TestFlight groups, group aliases, builds, in-app purchases, subscriptions, IAP pricing, offers, review replies, review signatures, review submissions, and Helm account setup or switching, even if the user only asks to "use the CLI" or automate App Store Connect work.
---

# `helm-asc`

Use `helm-asc` instead of ad-hoc App Store Connect scripting whenever the requested workflow already exists in the CLI.

## Setup

Resolve the CLI once before the first command:

1. Prefer `command -v helm-asc`.
2. If that fails, try common symlink locations: `/opt/homebrew/bin/helm-asc` and `/usr/local/bin/helm-asc`.
3. If those fail, try the bundled app helper: `/Applications/Helm.app/Contents/Helpers/helm-asc` and `~/Applications/Helm.app/Contents/Helpers/helm-asc`.
4. If any candidate exists and is executable, use that path for all Helm CLI commands in this session. The agent shell may have a different `PATH` than the user's Terminal.
5. Only after all candidates fail, stop and point the user to **Helm Preferences -> Helm CLI** to install or repair the command line tool.

In examples below, `helm-asc` means the resolved CLI command. If setup resolved an absolute path, substitute that absolute path anywhere an example starts with `helm-asc`.

## Start here

- If the workflow is obvious, run the direct command immediately with `--agent`.
- If the command branch is unclear, inspect only the nearest help path, such as `helm-asc apps --help`, `helm-asc version --help`, `helm-asc build --help`, `helm-asc review --help`, `helm-asc submission --help`, `helm-asc localization --help`, `helm-asc inAppPurchase --help`, `helm-asc subscription --help`, `helm-asc testFlightGroup --help`, or `helm-asc apps <app-id> testFlightGroupAliases --help`.
- Keep each shell command self-contained. Avoid `jq`, command substitution, and pipelines in agent flows; use the CLI's JSON output directly, or write large JSON results to a file and inspect that file with the host's file-read tool.

## Operating rules

- Pass `--agent` by default for machine-readable output. Omit it only when the user explicitly wants human-readable terminal output.
- For download commands, omit `--path` unless the user gave an explicit destination. The CLI writes to a sandbox-safe artifacts directory by default and returns the saved `rootPath` in JSON output.
- When an upload command needs a file or directory that the agent creates, first run `helm-asc paths --agent`, stage the generated input under the returned `uploadsInbox`, and pass that absolute path to the upload command.
- If the user gives an explicit upload or download path and Helm reports `FILE_ACCESS`, do not try to fix it with `cd`; changing the working directory only changes relative path resolution and does not grant sandbox access. Ask the user to grant access in Helm or copy/stage the file under a path returned by `helm-asc paths --agent`.
- Always pass absolute paths once a path has been resolved. Relative paths are acceptable only when they point inside the current workspace and the command has already proved access with a successful dry run or preflight.
- Discover IDs before mutating anything. Start with list or show commands, then switch to singular resource commands once you know the target IDs.
- Use `--dry-run` before bulk or destructive writes when the command supports it.
- Treat `--yes` as confirmation-gated. Only pass it when the action is destructive and the user has clearly approved the mutation.
- Keep help targeted. Prefer nested `--help` on the closest branch over dumping the full top-level help tree.
- For repeated workflows, preserve discovered IDs in notes or a small scratch file so you do not repeat expensive discovery steps.
- Do not retry a failed command blindly. Read the JSON `error.code`, `message`, `suggestions`, and any nested `errors`, then branch according to `references/output-contract.md`.
- If a command returns `PRO_REQUIRED`, stop and tell the user Helm Pro is required for CLI commands. Do not retry, switch accounts, or work around the gate; ask the user to upgrade or restore purchases in Helm, then retry only after Helm reports active Pro status.
- Do not diagnose installation or account state unless the command result points there. For auth failures, use `helm-asc auth list` or `helm-asc auth switch`; for a missing executable, use the setup steps above.

## Reference loading

- Read `references/command-map.md` to choose the correct command branch.
- Read `references/workflows.md` when the user asks for an end-to-end operation or a multi-step ASC workflow.
- Read `references/output-contract.md` when you need to interpret errors, exit codes, retries, partial failures, or safe stop conditions.

## Decision pattern

1. Confirm `helm-asc` exists.
2. Pick the narrowest command branch that matches the user goal.
3. Query first to discover app, version, localization, build, review, group, or submission IDs.
4. Mutate only after the target is unambiguous.
5. Prefer machine-readable output and branch on JSON fields or exit codes.
