---
description: Fix, test, and commit with a conventional commit message
argument-hint: "[optional commit message]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(composer *), Bash(vendor/bin/*), Bash(git *)"
---

# Commit

## Context

!`git status --short`
!`git diff --stat`
!`git diff --cached --stat`

## Phase 1 — Auto-fix

1. ```bash
   composer fix   # rector + php-cs-fixer
   ```
2. If the fixers changed files, review the diff before staging — rector's dead-code set can be aggressive.

## Phase 2 — Gates

3. ```bash
   composer test   # phpstan + phpunit
   ```

Fix any failure and re-run. Do **not** commit on red — `githooks/pre-commit` runs `composer fix && composer test` anyway, so a failure here just costs a slower round trip.

## Phase 3 — Commit

4. **Stage explicitly by filename.** Never `git add -A` or `git add .`.

5. **Message** — use `$ARGUMENTS` if given, otherwise derive it from the staged diff:

   ```
   <type>(<scope>): <subject>
   ```

   - Types: `feat`, `fix`, `ref` (**not** `refactor`), `test`, `docs`, `chore`
   - Scope: the module in lowercase, when the change is confined to one — `feat(chat): …`
   - Imperative mood, under ~70 chars, no trailing period
   - Body only when the *why* isn't obvious
   - **Never mention AI tooling.** No `Co-Authored-By`, no Claude/Anthropic trailer. No emoji in the subject.

6. ```bash
   git commit -m "<message>"
   ```

   Commits are GPG-signed with key `E51B5BF45F85D160` as `chemaclass@outlook.es`. If signing fails, stop and report — do not disable signing.

7. Report the hash, the message, and the files included.

## Never

- `--amend` on a pushed commit
- Committing `.env`, `composer.lock`, or `package-lock.json` unintentionally — check the staged list
