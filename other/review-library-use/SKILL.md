---
name: review-library-use
description: Review code for correct use of the repo's third-party libraries — checks the scoped files against the version-specific conventions recorded in the repo's `library-use` reference (docs-derived correct-usage rules, API contracts, footguns). Catches stale-API usage, deprecated patterns, and doc-violating misuse a general reviewer misses. Auto-invoked by `code-review` when a `library-use` reference exists. Triggers "review library use", "check library usage", "are we using this library correctly", "library convention review".
argument-hint: '[--staged | --unpushed | --changed | --all | --multi]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Library Use

Audit code against the **documented, version-specific conventions** of the libraries it
uses — the correct-usage rules, API contracts, and footguns captured in the repo's
`library-use` reference. This is the review counterpart to the `library-docs` generator:
`library-docs` distills "how to use this version correctly"; this skill checks the code
actually does.

## Relationship to the other reviewers (read first)
Deliberately **non-overlapping**:
- **General/`code-review` agents** judge logic, architecture, security, clean code — library-*agnostic*. This skill only flags things that are wrong **relative to a specific library's docs/version**.
- **`review-typescript`** judges type design. This skill judges library API usage.
- If a finding isn't tied to a convention in `library-use` (or, absent the file, to the library's official docs), it belongs to another reviewer — don't report it here.

Report only misuse a reader of that library's docs would recognize as wrong: calling a
removed/renamed API, a pattern the docs deprecate, missing required setup/config, using a
JS-SDK method that doesn't exist in the Java SDK, etc.

## Usage
```
/review-library-use                  # Review context-related code
/review-library-use --staged         # Review staged changes
/review-library-use --unpushed       # Files changed across all unpushed commits
/review-library-use --changed        # Unstaged changes
/review-library-use --all            # Whole-repo audit (parallel agents)
/review-library-use --multi          # Also get external advisor opinions
```

## Scope

| Flag | Scope | Method |
|------|-------|--------|
| (none) | Context-related code | Files from the current conversation. If none, ask the user to specify files or use `--staged`/`--changed`/`--all`. |
| `--staged` | Staged changes | `git diff --cached --name-only` |
| `--unpushed` | Unpushed-commit changes | `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| `--changed` | Unstaged changes | `git diff --name-only` |
| `--all` | Full codebase | `git ls-files` |
| `--multi` | Add external opinions | Combines with any scope; invokes `second-opinion --quick` |

`--unpushed` derives its range from `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If nothing is unpushed, or there's no remote/upstream (or the range walks back to the root commit), stop and ask the user to pick another scope.

## Workflow

### Step 1: Load the convention source
- Read `.claude/skills/library-use/SKILL.md` (or `.agents/skills/library-use/SKILL.md` if only that exists) — the per-repo reference. Parse each `## <library> \`<version>\`` block: its version, docs/changelog links, and Conventions bullets. **These are the rules to check.**
- **If it's missing:** say so once and offer to generate it — `No library-use reference found. Run \`library-docs\` to create one.` Then either (a) proceed in *degraded mode* against the top few libraries' official docs read on the fly, or (b) stop, per the user. Note in the output that coverage was degraded.
- **Staleness check:** if any documented version no longer matches the current lockfile, warn once (`library-use is stale for <lib> (<recorded>→<lockfile>) — run library-docs`) and review against the newer version's docs where it matters.

### Step 2: Resolve scope and filter
Resolve the scope (see table). Reduce to files that actually **import/use a documented library** — grep the scoped files for each documented library's import name; skip files that touch none.

### Step 3: Check usage against conventions
For each scoped file that uses a documented library, check its usage against that library's
Conventions bullets (and the linked docs when a bullet needs confirmation):
- Removed/renamed/relocated APIs still called the old way (the classic stale-training-data bug).
- Deprecated patterns the docs steer away from.
- Missing required initialization/config, wrong option shapes, wrong call order.
- Cross-SDK confusion (method exists in another language's SDK, not this one).

Parallelize if scope > 5 files: one sub-agent per library (or per file group), each given
that library's block; merge and dedupe.

### Step 4: External opinions (if `--multi`)
Invoke `second-opinion --quick` with a prompt naming the libraries + versions and asking
whether the scoped code uses them per current docs. Wait for all results before continuing.

### Step 5: Classify and report
Group by severity. Every finding must cite the convention or doc it violates — otherwise drop it.

## Severity
- **Critical:** doc-violating misuse that will fail at runtime for real inputs — calling a removed API, missing required init that crashes, wrong auth/security config from the library's guide.
- **High:** deprecated-but-working usage that breaks on the next upgrade, or a documented footgun that will bite (wrong option shape silently ignored, incorrect call order).
- **Medium:** using an older correct pattern when the pinned version documents a better/required one; non-idiomatic usage the docs warn against.
- **Suggestion:** minor doc-recommended improvements.

## Output Format
```markdown
## Library-Use Review: {scope}

### Reference
{library-use present? which libraries/versions were in scope. Note staleness or degraded mode.}

### Critical (doc-violating, will fail at runtime)
- {file}:{line} — {library} `{version}`: {what's wrong}
  **Convention:** {the bullet/doc rule it violates}  ·  **Docs:** {url}
  **Fix:** {concrete correct usage — with code}

### High (breaks on upgrade / documented footgun)
- {file}:{line} — {library}: {issue} — {fix}

### Medium (older pattern / non-idiomatic per pinned version)
- {file}:{line} — {library}: {issue} — {fix}

### Suggestions
- {doc-recommended improvements}
```
If `--multi` was used, append one subsection per advisor, then a **Cross-Model Agreement** subsection.

## Examples

**Stale API after a bump:**
> /review-library-use --staged

`library-use` records `better-auth 2.0`; the staged code calls `emailAndPassword({ requireVerification })` — renamed to `requireEmailVerification` in 2.0. Reports Critical with the doc link and the corrected call. A general reviewer wouldn't know the rename.

**Cross-SDK confusion:**
> /review-library-use --changed

Java code calls a `firebase-admin` method that only exists in the JavaScript SDK. Reports Critical, citing the Java SDK docs from the `library-use` block.

**No reference yet:**
> /review-library-use

No `library-use` file. Reports that, offers `library-docs`, and (if asked) runs a degraded pass against the top 3 libraries' live docs — flagged as degraded coverage.

## Troubleshooting

### No `library-use` reference in the repo
**Cause:** `library-docs` hasn't been run here.
**Solution:** Recommend running `library-docs` first. Optionally do a degraded on-the-fly pass against the most-used libraries' official docs, and label coverage as degraded.

### Findings overlap with general code review
**Cause:** Flagging logic/quality issues not tied to a library convention.
**Solution:** Drop them — those belong to the `code-review` agents. Keep only doc/version-specific misuse.

### Reference version doesn't match the lockfile
**Cause:** Deps were upgraded after the reference was generated.
**Solution:** Warn once, review against the current version's docs for the affected libraries, and recommend `library-docs --refresh`.

## Notes
- Pair: `library-docs` (generates the reference) → `library-use` (the reference) → `review-library-use` (this).
- The reference is the source of truth for *what* to check; the official docs are the tiebreaker when a bullet is ambiguous.
- Respect `CLAUDE.md`: a repo may deliberately pin an older pattern — don't flag a documented, intentional choice.
