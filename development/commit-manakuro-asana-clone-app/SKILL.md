---
name: commit
description: Write a Conventional Commits message for the staged changes, show it for review, and commit only after the user approves it.
disable-model-invocation: true
argument-hint: "[hints for the message]"
---

# Commit with a reviewed message

Draft a commit message for the current changes, show it to the user, and commit only after they approve it. Never commit without an explicit OK.

Hints from the user (may be empty): $ARGUMENTS

## 1. Look at the changes

```sh
git status --short
git diff --cached --stat
git diff --cached
```

- If something is staged, the commit covers **only the staged changes**. Mention unstaged or untracked files, but don't add them.
- If nothing is staged, propose which files to stage (group them by one logical change) and include that list in the preview. Stage them only after the user approves.
- If the changes contain several unrelated changes, suggest splitting them into separate commits, one preview each.
- Read the diff itself, not just file names, so the message says what changed and why.

## 2. Write the message

```
<type>[(<scope>)]: <subject>

<body>
```

**Subject line**

- `<type>` is one of:

  | type | for |
  | --- | --- |
  | `feat` | A new feature |
  | `fix` | A bug fix |
  | `docs` | Documentation only changes |
  | `style` | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.) |
  | `refactor` | A code change that neither fixes a bug nor adds a feature |
  | `perf` | A code change that improves performance |
  | `test` | Adding missing tests or correcting existing tests |
  | `build` | Changes that affect the build system or external dependencies (pnpm, Turborepo, tsc build, package.json) |
  | `ci` | Changes to the CI configuration files and scripts (GitHub Actions workflows, `.github/actions`) |
  | `chore` | Other maintenance that changes no source or tests (`.gitignore`, repo settings) |

- `<subject>`: one short sentence in the **imperative mood** (present tense, written as an order: `add`, `fix`, `remove`, not `added` / `adds`), lower case, no period. This follows [Google's CL description guidelines](https://google.github.io/eng-practices/review/developer/cl-descriptions.html): the first line is a short, focused summary that reads as an order.
- `<scope>` is optional. Add it only when the change is confined to one package or area, using its directory name: `biome-config`, `nextjs`, `api`, `react-native`. Leave it out for changes that span several packages or the whole repo.
- The whole line, including `<type>(<scope>): `, is **50 characters or fewer**. Drop the scope if it would push the line over.
- Examples: `feat: add new page`, `fix(cli): report missing token key`

**Body**

- Leave one empty line after the subject.
- Two or three sentences at most, in the **past tense** (`Added …`, `Replaced …`, `Fixed …`): what changed, and why (the problem it solves). Mention a file, export or option name in backticks when it helps.
- Avoid overly verbose descriptions or unnecessary details (no file-by-file lists, no restating the diff).
- Wrap lines at 72 characters.

## 3. Preview

Show the user, and then stop and wait for their answer:

````
Files to commit:
  M  path/to/file.ts
  A  path/to/new-file.ts

```
feat: add variants to createThemedStyles

Added a `variants` option so one style factory can return several
named variants. Each variant is resolved with the current color mode.
```

Commit with this message? Reply "OK", or tell me what to change.
````

- **OK** (or any clear approval) → go to step 4.
- **A change request** ("make it fix", "shorter", "mention X") → rewrite the message and show the preview again. Repeat until approved.
- **Cancel** → stop without committing.

## 4. Commit

Pass the approved message exactly as previewed. Don't append a `Co-Authored-By` trailer or any other footer:

```sh
git commit -F - <<'MSG'
<approved message>
MSG
```

- Lefthook's pre-commit hook runs Biome (and may restage fixed files) and `tsc` for the touched packages. Never bypass it with `--no-verify`.
- If the hook fails, show the error, fix the cause if it is clear (or ask), and preview again before retrying.
- Afterwards, reply with the commit hash and subject (`git log --oneline -1`).

