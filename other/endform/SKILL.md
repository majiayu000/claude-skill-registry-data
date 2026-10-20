---
name: endform
description: Set up, run, and investigate Playwright test suites on Endform with the Endform CLI. Use when the user mentions Endform, or when the repository runs its tests on Endform (an `endform` dependency, `endform test` in a script or CI workflow, or an `endform.config.*` file or a legacy `endform.json`/`endform.jsonc`), to run tests, add Endform to a repository or CI, find out why tests failed in CI, find flaky or slow tests, quarantine failing or flaky tests, compare pass rates across branches, or run code inside a live test to inspect a failing step or try new test steps. Not for Playwright repositories that do not use Endform.
metadata:
  author: endform
---

# Endform

Endform runs Playwright suites in parallel on isolated machines. The CLI is `npx endform@latest`. It takes Playwright's test selection and run flags, such as file filters, `--grep`, `--project`, `--repeat-each`, and `--retries`, but not Playwright's --workers, --headed, --ui, or --list.

## Check that Endform applies

Endform applies when the user mentions it or the repository uses it: an `endform` dependency, `endform test` in a script or CI workflow, or an `endform.config.*` file or a legacy `endform.json`/`endform.jsonc`. If neither holds, answer without Endform commands.

## Pick the reference for your task

Read the reference for the task.

| Task                                                                                                                                                     | Reference                                                                                                 |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Set up Endform in a repository, first run, local server, config files                                                                                    | [reference/setup.md](reference/setup.md)                                                                  |
| Run Endform on CI, such as GitHub Actions or GitLab CI                                                                                                   | Steps 2 to 4 of [reference/setup.md](reference/setup.md), then [reference/ci.md](reference/ci.md)         |
| Test the Vercel preview of each pull request                                                                                                             | Steps 2 to 4 of [reference/setup.md](reference/setup.md), then [reference/vercel.md](reference/vercel.md) |
| Find and fix failing, flaky, and slow tests, quarantine a failing or flaky test, limit concurrency for tests that fail under load, pass rates, past runs | [reference/investigate.md](reference/investigate.md)                                                      |
| Run code inside a live test: inspect a failing step, find locators, try the next steps of a test                                                         | [reference/live-test.md](reference/live-test.md)                                                          |

If the reference does not cover the case, fetch the matching page from `https://endform.dev/docs/llms.txt` and read only that page.

## Login and organization

Run the command the task needs and react to its output:

- **"No Endform credentials found"** or **"Unauthorized"**: run `npx endform@latest login` and ask the user to finish browser authorization. Resume the task once login succeeds. Do not work around a missing login.
- **"Organization selection is required"**: ask the user which organization, then pass `--organization-id <id>` on every `analytics`, `samples`, `test`, `live-test`, `quarantine`, `connect`, and `api-key` command.

Commands in the references show `--organization-id <organization-id>`. Fill in the chosen id, or leave the flag out until the CLI asks for an organization.

## Rules

- If you cannot run commands, use the Endform MCP tools when they are connected, otherwise say you need a shell. Never mix CLI and MCP results without confirming they target the same organization.
- Make the repository changes the task needs and summarize what changed. Ask before storing secrets or changing settings outside the repository, and commit or open a pull request only when asked.
- Never write an API key or other secret into the repository. GitHub Actions authenticates through the Endform GitHub App or the `ENDFORM_API_KEY` secret. Other CI systems use the secret.
- Let `npx endform@latest test` finish. Stopping it, or a tool timeout that kills it, cancels the suite run, so give it a timeout longer than the suite takes.
- Filter to failures and keep `--limit` small so query output stays readable.
- Stop a live test when you are done with it.
