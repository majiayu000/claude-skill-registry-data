---
name: commit
description: Use when the user explicitly asks to commit the current changes. Push, amend, and rebase require separate explicit requests.
---

# mak:commit — Work Wrap-Up and Commit

Running this skill is the user's explicit "commit" instruction — for the commit only.

## Procedure

### 1. Inspect

`git status` + `git diff` (staged / unstaged / untracked). Nothing to commit → report and stop. Identify which task the changes belong to.

### 2. Gates

Results are reported once, in the §5 report. Surface immediately only findings that need a user decision (split proposal, unverified proceed, suspected secret).

- **Verification** — confirm the changes were verified (`mak:verify-checklist` results or the project's verify commands).
  - Not verified, and the project declares verification commands (per the `mak:verify-checklist` §Verification Order priority rule, which owns what counts as declared) → run those commands as documented, with no auto-fix or formatter flags. Build/type check, lint, and tests are common examples, but run whatever the project declares — a docs-only project may declare a manifest validator and consistency greps instead. Then re-check `git status` since builds and tests produce artifacts. On failure, either get explicit confirmation to proceed unverified, or stop and route the fix through the normal flow before re-entering this skill.
  - Not verified, and the project declares none → report this gap and the remaining verification blind spot to the user, and get explicit confirmation before proceeding unverified.
- **Precise changes** — one purpose per commit. Unrelated changes mixed in → propose a split or leave them unstaged; never bundle silently.
- **Hygiene** — exclude temp/junk files, logs, large binaries, and secrets. Never commit a suspected secret without asking, even if staged.

### 3. Stage deliberately

Stage the reviewed files explicitly; no blind `git add -A`.

### 4. Message

- Follow the repo's convention (recent `git log` style, commitlint) **only if it is consistent and informative**. Placeholder history ("update", "fix", "wip"), or too thin/mixed to establish a deliberate convention, is not one — use the fallback and note briefly why.
- Fallback and quality floor: Conventional Commits — `<type>(<scope>)?: <subject>`, imperative subject ≤ 72 chars. A repo convention may override the shape, never the informativeness.
- Types, unless the repo's own set differs: `feat` `fix` `test` `docs` `refactor` (no behavior change — if behavior moved, it is `feat`/`fix`) `perf` (no functional change) `style` (code formatting, never UI styling) `build` (build system, dependencies) `ci` (CI config) `chore` (maintenance fitting no other type — not a bucket for changes left unclassified) `revert` (name the reverted commit in the body). Do not invent one outside the set in use.
- Type = the change's primary intent, not its file type. **One type per commit** — two genuinely applying is a split signal (back to §2); docs/tests belonging to a feat/fix ship inside it. Scope optional (module/domain; reuse scopes from `git log`). Breaking change: `!` + `BREAKING CHANGE:` body line.
- mak outputs: design doc / roadmap / doc-set → `docs`; a verify-caught fix before commit → part of the original `feat`/`fix`; kit/config housekeeping → `chore`.
- **Write the message in the user's conversation language** (or the project's documented language policy).

**Style — concise and declarative, never narrative.** Every line carries a fact, not prose about the work:

- **Subject** — the outcome ("remove the cross-layer duplication"), not the mechanics ("move a file"). Imperative or noun phrase, no trailing period.
- **Body** — 2–6 bullets, **one line per bullet**, one verifiable fact each with counts/names. No paragraphs, no multi-sentence bullets, no prose connecting them.
- **Cut, always** — "this commit …" openers, background/motivation essays, restating the diff file by file, closing summaries, hedges ("slightly", "some"), and polite or past-tense sentence endings (in languages with such endings — e.g. Korean — use noun-phrase endings instead).
- **Keep** — preserved invariants (contract unchanged, tests moved along), what intentionally stayed put, doc-sync section names.
- **Scale the body to the diff** — a tiny change takes the subject alone or at most one bullet; multi-bullet bodies are for diffs with multiple facts worth recording.

The terseness rule holds in every language; only the wording changes. Example (imitate the structure, in the user's language):

```
refactor(order): remove OrderStatus duplication via the shared domain layer

- OrderStatus: features/checkout/model -> domain/order (serialization contract unchanged, 2 unit tests moved)
- payment/history references switched to the domain path — 1 cross-feature import exception removed
- OrderStatusDto stays in features/checkout (API response shape)
- Docs sync: architecture guide (§module tree, §exception list), glossary
```

### 5. Commit and report

Pre-commit self-check: the message body (logical view) and the staged files (physical view) **must agree** — a bullet with no supporting file, or a file no bullet accounts for, is a stop signal; resolve it before committing.

**Never pass the message as a shell argument.** Write it to a temp file outside the repository (session scratchpad or OS temp dir), run `git commit -F <file>`, then delete the file. `-m` quoting rules differ per shell and silently corrupt multi-line messages — a PowerShell here-string (`@'…'@`) executed under bash commits `@` as the subject. A temp file inside the working tree is not an option: it shows up as untracked and can be swept into a later commit.

Then report in the user's language (one commit per purpose; more if a split was agreed in §2):

```
## Commit Result
- <short hash> — <the committed message: subject and body>
- Gates: verification ✅/⚠️ · precise-changes ✅/⚠️ · hygiene ✅/⚠️

| File | +/− | What changed |
| :--- | :--- | :--- |

- Left uncommitted (intentionally): <files + reason, or "none">
- Not pushed — push runs only on the user's explicit request
```

Cluster long file lists into logical groups, but every file appears.

## Prohibitions

- No `push` / `--amend` / `rebase` / `reset` / force operations / tags on your own — each only on the user's explicit request for that operation.
- No commit with a failing or skipped verification gate without the user's explicit confirmation.
- No file edits by this skill — staging/unstaging and committing only, the commit-message temp file being the sole exception; fixes go back through the normal flow. Artifacts incidentally produced by verification (caches, build output) are never staged or committed.
