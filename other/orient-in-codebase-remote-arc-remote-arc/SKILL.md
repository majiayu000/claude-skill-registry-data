---
name: orient-in-codebase
description: Learn an unfamiliar repository before changing it, including its real build and test commands, conventions and current health. Use this at the start of work in any repository you have not read in this session, or whenever you do not yet know how to run its tests, even if the task looks small.
---

# Orient in a codebase

Most bad changes start with a wrong assumption about the repository. A few
minutes here prevents guessed commands, duplicated helpers and confusion over
failures that already existed.

## When to use

- First task in a repository, or in an area you have not read.
- You do not know how tests run, or which branch is current.

Skip this if you already did it for this area in the current session.

## Steps

1. **Check where you are.** Run these and read the output:

   ```bash
   git status --short --branch
   git fetch origin
   git log --oneline -5
   ```

   If the branch is behind the default branch, note it. A search on a stale
   branch can miss code that exists.

2. **Read the project's instructions.** Look for `AGENTS.md`, `CLAUDE.md`,
   `GEMINI.md`, `CONTRIBUTING.md` and `README.md`. They override your habits.

3. **Identify the stack from its manifest files.**

   | File | Stack | Look for commands in |
   | --- | --- | --- |
   | `package.json` | JavaScript or TypeScript | `scripts` |
   | `pyproject.toml`, `requirements.txt` | Python | `[tool.*]`, `tox.ini`, `Makefile` |
   | `go.mod` | Go | `Makefile`, `go test ./...` |
   | `Cargo.toml` | Rust | `cargo test` |
   | `pom.xml`, `build.gradle` | Java or Kotlin | `mvn test`, `./gradlew test` |
   | `*.csproj`, `*.sln` | .NET | `dotnet test` |
   | `Gemfile` | Ruby | `Rakefile`, `bin/rspec` |
   | `composer.json` | PHP | `scripts` |

4. **Find the commands CI runs.** Read `.github/workflows/`, `.gitlab-ci.yml` or
   the equivalent. CI is the real definition of passing, and docs are often out
   of date. Note the commands for tests, lint, type checks and build.

5. **Record a baseline.** Run the tests for the area you will change, before you
   change anything. Write down what fails now. Without this, you cannot tell
   whether you caused a failure.

6. **Find the code path.** Search for a word from the task, such as a route, an
   error message or a UI label. Follow it from the entry point to storage. Read
   callers as well as the function itself.

7. **Find the nearest example.** Open the closest similar feature and its test.
   Copy their naming, structure, helpers and error handling.

## Stop and ask when

- The task description does not match what the code does.
- The baseline is broken in a way that blocks your work.
- You cannot find how to run the tests after checking the manifest and CI.

## Common mistakes

| Tempting move | Why it fails | Do this instead |
| --- | --- | --- |
| Guess `npm test` or `pytest` | The real command may differ or do less | Read the manifest and CI |
| Trust the README alone | It may be out of date | Confirm with CI config and by running it |
| Skip the baseline | Old failures look like yours | Run the tests first |
| Write a new helper | One probably exists | Search before you write |
| Say something does not exist after one search | The name may differ or the branch may be stale | Fetch, try other terms, then state what you searched |

## Report

```markdown
Branch: <name>, <ahead/behind default branch>
Stack: <languages and frameworks>
Commands: test `<cmd>`, lint `<cmd>`, types `<cmd>`, build `<cmd>`
Baseline: <what passes, what already fails>
Code path: <entry point> -> <main files>
Pattern to follow: <nearest similar file>
```
