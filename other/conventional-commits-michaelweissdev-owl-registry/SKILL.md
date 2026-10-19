---
name: conventional-commits
description: Write, review, validate, and organize precise Conventional Commits 1.0.0 messages from actual code changes. Use when the user asks for a commit message, wants to commit changes, reviews commit history, prepares a clean commit series, or needs guidance on commit types, scopes, breaking changes, release impact, or commit-message compliance. Inspect the real diff and repository conventions before composing messages; never infer changes from filenames alone.
compatibility: Works with Claude Code and other Agent Skills-compatible coding agents. Git is helpful for repository inspection but not required when a diff is provided.
metadata:
  version: "1.0.0"
  standard: "Conventional Commits 1.0.0"
---

# Conventional Commits

Create accurate, concise, machine-readable commit messages that describe **what actually changed** and **why it matters**. Follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/). Favor meaningful, independently reviewable commits over cosmetically perfect labels.

## Non-negotiable rules

1. **Inspect evidence first.** Base each message on the relevant diff, context, and repository conventions. Never invent changes, tests, issues, compatibility guarantees, or motivations.
2. **Use the standard format.** A message starts with `<type>[optional scope][!]: <description>`. A body and footers are optional and separated by blank lines.
3. **Use `feat` for new functionality and `fix` for bug fixes.** These meanings are defined by the specification; other types are conventions, not mandatory types.
4. **Mark every confirmed breaking change.** Place `!` immediately before `:`, or supply a `BREAKING CHANGE: ...` footer; use both when migration details help.
5. **Represent one logical change per commit when feasible.** Do not camouflage unrelated changes under a vague subject. Suggest an atomic split when warranted.
6. **Match the repository's established policy.** Respect documented contribution rules, commitlint configuration, allowed scopes, release tooling, and local history when they are compatible with the standard. Point out material conflicts; do not silently alter policy.
7. **Never perform Git write operations merely to draft or review messages.** Only stage or create local commits when expressly requested and authorized. Never push, publish, create a PR, or modify a remote repository as a side effect. Treat GitHub integrations as read-only.
8. **Never rewrite or discard history without explicit authorization.** Do not amend, reset, rebase, force-push, or touch someone else's changes to satisfy a formatting request.

## 1. Canonical structure

```text
<type>[optional scope][!]: <short description>

[optional body]

[optional footer(s)]
```

Requirements from the specification:
- The type is required and is a noun such as `feat` or `fix`.
- The scope, if present, is a noun identifying a section of the codebase, enclosed in parentheses immediately after the type.
- `!`, if present, appears after the type or scope and immediately before the colon.
- The header includes **a colon followed by one space** and a nonempty description.
- A body begins after one blank line; it may contain multiple paragraphs.
- Footers follow after a blank line and use a token with `: ` or ` #` as a separator. Replace spaces in normal footer tokens with hyphens (for example, `Reviewed-by`).
- The breaking footer is specifically `BREAKING CHANGE: <description>`; `BREAKING-CHANGE: <description>` is an equivalent accepted token. Prefer the former for readability.
- The standard is not generally case-sensitive for the other structural tokens; **the `BREAKING CHANGE` footer spelling must be uppercase**.

Preferred house style (recommendations, **not requirements of Conventional Commits**):
- Use lowercase type and scope; use a stable, short scope such as `api`, `cli`, `parser`, `auth`, `docs`, or `build`.
- Write the description as an imperative, present-tense action: `prevent`, `add`, `remove`, `handle`, `document`.
- Start the description with lowercase text, avoid a trailing period, and aim for 50 characters when practical; prefer staying within 72 characters over awkward abbreviations.
- State the observable change, not the editing activity. Use `fix(parser): reject truncated headers`, not `fix: made some code changes`.
- Keep body lines around 72 characters where practical, but never break URLs, code, or machine-parsed footer tokens merely for wrapping.
- Do not use emoji, marketing language, unsupported superlatives, or vague descriptions such as `update stuff`, `misc fixes`, or `improve code`.

## 2. Inspect the change before choosing a message

When a Git working tree is available, prefer a **read-only** investigation:

```bash
git status --short
git diff --cached --stat
git diff --cached --
git diff --stat
git diff --
git log -5 --format=%s
```

Read full file context or focused history only when necessary to understand behavior. Consult `CONTRIBUTING.md`, commitlint or release configuration, and documented scope conventions where available. Don't run arbitrary repository scripts merely to discover a commit name.

Selection rules:
- **Writing a message for a prospective commit:** describe **only the staged diff** if the user identifies the staged changes. If staged and unstaged edits coexist and the request is ambiguous, identify the distinction instead of conflating them.
- **Writing messages for all local modifications:** inspect tracked and untracked files. `git diff` does not display the contents of untracked files; read relevant untracked files separately when authorized and needed.
- **Reviewing an existing commit:** use the actual commit and its patch, for example `git show --format=fuller --stat <sha>` and `git show --format= <sha> --` to inspect the patch.
- **No repository available:** use the diff, patch, changelog, or facts supplied by the user. Explain material uncertainty rather than hallucinating.
- **Ambiguous scope or behavior:** prefer an accurate broad description or no scope over a precise-sounding guess.

Extract these facts before drafting: behavior before/after; affected component; public-facing impact; reason for change; any backward incompatibility; whether multiple independently reversible concerns are mixed; references and tests actually observed.

## 3. Choose the most accurate type

| Type | Use when | Avoid when |
| --- | --- | --- |
| `feat` | Adding a new user-visible or public developer-facing capability | Merely reorganizing internal code |
| `fix` | Correcting incorrect behavior, a regression, or a vulnerability | Adding entirely new behavior without fixing a defect |
| `docs` | Documentation-only changes | Documentation accompanies a functional change that should be committed with it |
| `test` | Adding or correcting tests without changing production behavior | Tests are integral to a feature or fix in the same logical commit |
| `refactor` | Restructuring code without intended behavior or contract changes | Fixing a bug, adding functionality, or changing compatibility |
| `perf` | Optimizing performance with no intended feature or compatibility change | Claiming an improvement not supported by the change or evidence |
| `build` | Build tools, dependencies, packaging, or compilation configuration | CI workflow changes best classified as `ci` |
| `ci` | Continuous integration or delivery configuration | General runtime behavior |
| `style` | Pure formatting, whitespace, or non-semantic code style | UI styling or any change in actual output |
| `chore` | Repository maintenance not captured more precisely | Using it as a catch-all for actual features and fixes |
| `revert` | Undoing an identified previous change | Ordinary bug fixes or speculative rollback plans |

Other type names are valid under the specification. The table is a **recommended taxonomy**, not an exhaustive allowlist. If the repository has a more specific documented taxonomy, use it.

Important distinctions:
- Classify by **intent and externally relevant effect**, not by files touched. A change to `tests/` may be part of a `fix`, and an implementation plus docs can be one `feat`.
- A security vulnerability repair is usually `fix`, with a component scope when useful: `fix(auth): enforce authorization on export requests`.
- Breaking changes can have **any type**: `refactor(api)!:` and `fix(config)!:` are both possible.
- A refactor that accidentally changes behavior is not safely labeled `refactor`; investigate first.
- Use `perf` only when a performance-oriented improvement is actually implemented. Do not invent benchmark numbers.

## 4. Select a useful scope

A scope identifies the smallest coherent subsystem understood by readers of the repository:

1. Prefer an existing project-defined scope.
2. Otherwise prefer the affected interface or module (`cli`, `api`, `parser`, `storage`, `ui`, `auth`).
3. Avoid filenames, ticket numbers, personal names, and excessively granular scopes unless the project's convention calls for them.
4. When several components implement **one** logical change, use their common subsystem, or omit the scope.
5. When two unrelated components have distinct purposes, recommend separate commits rather than an invented umbrella scope.

Examples: `fix(parser): handle empty input`; `feat(cli): support JSON output`; `docs: clarify deployment requirements`.

## 5. Identify and describe breaking changes

A breaking change alters a **previously supported** consumer contract in a way that requires downstream adaptation, such as removing or renaming a public API, changing a previously valid command-line option, incompatible configuration or data formats, or intentionally changing behavior that consumers rely on.

Do **not** infer a breaking change merely from a large diff, internal refactor, changed private function, changed dependency, or failed test. Examine whether the affected interface is part of the supported contract.

Two valid markers:

```text
feat(api)!: replace positional arguments with an options object
```

```text
feat(api): replace positional arguments with an options object

BREAKING CHANGE: callers must pass an options object instead of
positional arguments.
```

For actionable breaking changes, **prefer both `!` and a footer** explaining what breaks and how to migrate:

```text
feat(config)!: remove the legacy timeout setting

Remove support for the deprecated `timeout_ms` key in favor of
`request.timeout`.

BREAKING CHANGE: configurations using `timeout_ms` must migrate to
`request.timeout` before upgrading.
```

Do not mark breaking changes merely because release tooling would benefit from a major version bump. Breaking status is a property of the actual compatibility change.

## 6. Write a high-signal body and footers

Use a body when the header cannot adequately convey the why, behavior, tradeoff, risk, migration, or non-obvious implementation decision. The body should:
- Describe the prior problem or limitation and the resulting behavior.
- Explain motivation or consequences, not narrate each changed line.
- Record essential caveats only if evidenced by the diff or provided context.
- Avoid unverified claims like `fully secure`, `no regressions`, or `all tests pass`.

Use footers for information that has a real source:

```text
Refs: #123
Closes #456
Reviewed-by: Example Reviewer
BREAKING CHANGE: consumers must pass the new required argument.
```

Do not fabricate issue IDs, co-authors, reviewers, CVEs, or `Co-authored-by` / `Signed-off-by` trailers. Use `BREAKING CHANGE:` verbatim, not `BREAKING:` or `BREAKING_CHANGES:`.

A body isn't required for a simple change. Do not pad straightforward messages with boilerplate.

## 7. Handle mixed changes and commit boundaries

When the diff contains more than one logical purpose:

1. Group changes by behavior, concern, and independent reversibility.
2. Prefer to keep tests and focused documentation with the feature or fix they verify or explain.
3. Separate an unrelated refactor from a bug fix or new feature where practical.
4. Suggest the **smallest sensible** commit sequence, not one commit per file.
5. Never claim that changes can be split cleanly when they are interdependent; explain dependencies and propose a safe ordering.
6. Never stage or split changes without explicit authorization; a plan and candidate messages are enough for a message-generation request.

Example sequence:

```text
refactor(parser): isolate tokenization from syntax validation
fix(parser): reject unterminated quoted strings
test(parser): cover escaped quote edge cases
```

The third commit is useful only if those tests are an independent logical change; otherwise include them with the `fix`.

If all changes intentionally form one coherent behavior change, choose a single message even when multiple files, layers, and tests are involved.

## 8. Local commit workflow (only when explicitly requested)

1. Confirm repository state and the exact changes intended for the commit. Do not silently include unrelated or untracked files.
2. Inspect the selected diff for accidental secrets, credentials, generated artifacts, unrelated edits, and merge conflicts. Never expose secret values in your reply.
3. Identify and respect pre-existing staged changes owned by the user.
4. Stage only the authorized files/hunks. Avoid broad `git add -A` unless all changes were expressly included and verified.
5. Re-read `git diff --cached --` **after staging**. The commit message must describe precisely this final staged snapshot, not unstaged work.
6. Run only relevant checks that are available and appropriate; report results truthfully. Don't claim tests ran if they did not.
7. Validate the message against the specification and local lint configuration before committing.
8. Create a **local** commit only when authorized. Do not amend or rewrite history implicitly.
9. Report the actual commit hash and subject if a commit was created. Otherwise report the proposed message and any blocker.
10. **Do not push or perform other remote write operations.** GitHub adapters and integrations are read-only.

If the repository has unresolved conflicts, no staged diff, suspicious secret material, or unclear ownership of changes, stop before committing and clearly describe the issue. Never fix a blocker by discarding work.

## 9. Validation checklist

Before returning a message, verify:

- [ ] The header follows `<type>[optional scope][!]: <description>`.
- [ ] `feat` means a feature and `fix` means a defect correction; any alternate type accurately describes the change.
- [ ] The scope is meaningful and consistent, or intentionally omitted.
- [ ] The description is concrete, concise, and supported by the actual change.
- [ ] A breaking change has `!` or a `BREAKING CHANGE:` footer, with no unsupported breaking claim.
- [ ] Blank lines separate header, body, and footer section when those sections are present.
- [ ] Footer tokens and separators follow the specification; any issue or attribution is genuine.
- [ ] There are no fabricated tests, references, effects, or version numbers.
- [ ] The message represents the actual selected diff, not unrelated working-tree changes.
- [ ] Repository-specific commit conventions have been respected unless they conflict with an explicit user instruction.

For automatic validation, prefer the repository's existing commitlint or equivalent when present; do not install tooling or change repository configuration without permission. Distinguish **specification errors** from optional **house-style warnings**.

## 10. Semantic Versioning interpretation

Conventional Commits supports release automation, but **does not itself publish or choose a release**. When asked to infer a SemVer bump for a conventional release policy:

- Any breaking change (`!` or `BREAKING CHANGE:`) implies **MAJOR**.
- Otherwise, `feat` implies **MINOR**.
- Otherwise, `fix` implies **PATCH**.
- Other types have no standard-implied bump unless marked breaking or customized by release tooling.
- The highest applicable category normally wins when analyzing several commits.

Do not present this as a guaranteed release decision: `0.x` behavior, prereleases, release branches, squashed commits, and project-specific tooling can change the actual result.

## 11. Examples

### Focused bug fix

```text
fix(parser): reject incomplete UTF-8 sequences

Return a parse error instead of silently accepting a truncated
multibyte sequence.
```

### New feature with tests and docs in the same logical change

```text
feat(cli): add newline-delimited JSON output

Add the `--ndjson` option for streaming machine-readable results.
Document its behavior and cover multi-record output in tests.
```

### Security fix

```text
fix(auth): enforce ownership checks on file downloads

Reject requests for files that do not belong to the authenticated
principal instead of authorizing access solely by file identifier.
```

### Internal-only refactor

```text
refactor(storage): centralize transaction retry handling
```

### CI change

```text
ci: run integration tests on Linux and macOS
```

### Documentation-only change

```text
docs(api): clarify pagination cursor behavior
```

### Breaking API change

```text
feat(api)!: require explicit pagination limits

Remove the implicit default limit to make query costs predictable.

BREAKING CHANGE: API clients must provide a positive `limit` value
on all paginated list requests.
```

### Revert with a real reference

```text
revert: remove experimental response cache

Revert the caching behavior introduced in the referenced commit.

Refs: a1b2c3d
```

### Bad versus better

| Weak or misleading | Better | Why |
| --- | --- | --- |
| `fix: stuff` | `fix(cli): preserve exit code on timeout` | Names behavior |
| `feat: refactor validators` | `refactor(validation): share common error handling` | No new capability |
| `chore: fix authentication` | `fix(auth): reject expired sessions` | Fix deserves `fix` |
| `feat(api): break everything` | `feat(api)!: remove deprecated v1 endpoints` | Names incompatibility |
| `test: all tests pass` | `test(parser): cover empty token streams` | Describes changes, not unsupported outcome |

## 12. Response contract

Choose the response mode that matches the user's intent:

- **User requests a commit message:** return the best complete message in a fenced `text` block, with no unnecessary commentary. Include body/footers only when useful. If the evidence is incomplete, state the key uncertainty briefly.
- **User requests message review or validation:** quote the original message, report concrete specification errors separately from style suggestions, and provide one corrected version.
- **User asks to organize multiple changes:** present a compact atomic commit plan with ordered messages and a short rationale for boundaries.
- **User explicitly requests a local commit:** follow Section 8; report what was actually committed and tested. Never imply an unperformed action was performed.
- **User asks about release impact:** state the inferred SemVer level and the specific commit evidence; note project-specific caveats.

Do not turn a straightforward commit-message request into an unnecessary tutorial. Optimize for correctness, traceability, and clean history.

## Authoritative references

- [Conventional Commits 1.0.0 — official specification](https://www.conventionalcommits.org/en/v1.0.0/#specification)
- [Semantic Versioning](https://semver.org/)
- [Agent Skills specification](https://agentskills.io/specification)
