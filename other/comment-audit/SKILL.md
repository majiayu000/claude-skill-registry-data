---
name: comment-audit
description: "Audit, prune, and standardize comments and API docstrings across TypeScript, JavaScript, Python, Go, C, and shell to match idiomatic industry standards (TSDoc, JSDoc, Google-style, Godoc, Doxygen) with zero code logic mutation. Use when the user asks to audit comments, clean up docstrings, remove redundant inline comments or banner noise, document functions or structs, or says 'yorumları temizle', 'docstring yaz', 'yorum denetimi yap', 'kod dokümantasyonu ekle', or mentions comment rot - even for single-file comment cleanups or when documenting legacy code without touching behavior."
---

# Comment audit

Audit every comment and doc block in the target. Then add what is missing, fix what is
wrong, and delete what is noise, until the file meets the language's current standard.

**Write as little as possible while making the code impossible to misunderstand.** A file
where every function has a comment is a failed file. Assume the reader knows the language
better than you do.

## Step 0: pick the language reference

Detect the language from the file extension and read the matching reference **before**
touching anything. Each reference carries the baseline standard, pre-flight checks,
language-specific triggers, forbidden patterns, doc-block format and a calibration example.

| Extension | Reference |
|---|---|
| `.ts`, `.tsx`, `.mts`, `.cts` | `references/typescript.md` |
| `.js`, `.jsx`, `.mjs`, `.cjs` | `references/javascript.md` |
| `.py`, `.pyi` | `references/python.md` |
| `.go` | `references/go.md` |
| `.c`, `.h` | `references/c.md` |
| `.sh`, `.bash`, files with a `sh`/`bash` shebang | `references/shell.md` |

If the target mixes languages, read every applicable reference and audit file by file.
If no reference matches, stop and say so; do not improvise a standard.

## 1. The one principle

> **Comments carry what the code cannot: intent, rationale, constraints, warnings, history.**

### The wrong-edit test

> *"Is there a specific, plausible change a future developer would make here that this
> comment prevents, and that the code alone would not prevent?"*

- Yes: **keep it.**
- No: **delete it.** A comment that only narrates ages into a lie.

### The gate (run in order)

1. Does it restate what the line already says? **Don't write it.**
2. Is it a *why / warning / constraint / assumption / trade-off / domain fact*? **Write it.**
3. Would a competent developer in this language, reading cold, be confused or silently
   break something? **Write it.**
4. Otherwise: **silence.**

Corollary: **do not comment uniformly.** Non-obviousness is not evenly distributed.
Commenting every function "for consistency" is the single most common failure.

## 2. Audit first: triage what is already there

Read every existing comment before writing. Work in priority order. **A wrong comment is
more damaging than a missing one.**

### Priority 1: Lies

Comments that contradict the code: stale return/exit contracts, signature drift (documented
parameter no longer exists, new parameter undocumented), phantom guarantees (a lock, a
thread-safety claim, an exception that is never raised), dangling references to removed
code, dead examples. **FIX** to match the code. See the language reference for the
language-specific signals.

> **If you cannot tell whether the code or the comment is authoritative, stop.**
> Leave both unchanged and put it in the report's *flagged* line. Never change code to make
> a comment true.

### Priority 2: Bloat

Delete: restatement, type-in-prose, control-flow narration, banner/ASCII decor,
author/date/changelog headers, commented-out code, tautological doc blocks, a comment
duplicating the doc block above it, ownerless TODOs, emoji.

### Priority 3: Wrong shape

Move contract information (preconditions, errors, ownership, blocking, side effects) into
the doc block; move implementation rationale out of the doc block and next to the code;
compress line-by-line narration to summary plus contract; normalise mixed dialects to the
file's majority; delete comments that explain the language or its standard library.

### Priority 4: Gaps

Only after 1-3 are done, add what is missing, using the trigger table in the reference.

### Anti-churn rules

- **Don't reword correct comments into your own voice.** Style-only edits are noise.
- **When in doubt, KEEP.** A comment that looks redundant may be protecting a constraint
  you cannot see. Deleting it is worse than leaving it.
- **A comment that suggests a missing invariant** (a commented-out lock, bounds check,
  retry, or safety guard): flag it, don't quietly delete it.
- Preserve real information when you rewrite: turn an awkward but useful comment into a
  clear one. Don't delete it because it is badly written.

## 3. Universal forbidden patterns

Never write, and delete on sight:

- Restatement of the adjacent line (`# increment i`, `// return the result`).
- Types in prose when the language carries them in the signature.
- Control-flow narration (`# otherwise continue`, `/* end of if */`).
- Decor and history: banners, separators, author/date/modified lines. Git is the history.
- Commented-out code (see the reference for the one exception per language, e.g. `#if 0`).
- Tautological doc blocks that restate the name (`"""Get the name."""`, `// GetUser gets a user.`).
- A bare `TODO`/`FIXME`/`HACK`/`XXX`. A TODO needs **both** an owner and a ticket:
  `TODO(ada): handle the empty batch. PROJ-1424.` Otherwise delete it.
- A bare lint/type suppression. Every `noqa`, `nolint`, `NOLINT`, `type: ignore`,
  `shellcheck disable` names the rule **and** gives a reason, at the narrowest scope.

## 4. Comment craft (universal)

- Full sentence, capitalised, ending period.
- One line is the goal, three the limit. If you need more, the function probably needs
  splitting: say so in the report, don't do it.
- Block comment on its own line above what it describes, at the code's indentation.
  Trailing comments only for short annotations, at least two spaces after the code.
- Describe current behaviour only. Never restate the log/error message beneath it.
- Match the file's width, comment language, and mood.

## 5. Edit discipline

1. **Never change executable code** while documenting. If a rename or extraction would make
   a comment unnecessary, *propose* it in the report. Don't do it silently.
2. Comment-only hunks; keep the diff reviewable.
3. **Density scales with non-obviousness, not with line count.** Evenly spread comments mean
   you are decorating. Go back and cut.
4. Finish with a **deletion pass**: re-read every comment you touched and remove the ones
   that fail the wrong-edit test. Expect to cut 20-40% of your first draft.
5. Before reporting, run `scripts/comments-only.sh <file>...` from this skill directory. If
   it exits non-zero, you changed code: revert that hunk or list it under *flagged*.

## 6. Self-check before finishing

- [ ] Read the language reference and the project's lint/format config first?
- [ ] **Audit done first**: every pre-existing comment classified KEEP / FIX / DELETE / MOVE?
- [ ] Zero false statements left: parameters, returns, errors, concurrency claims match the code?
- [ ] Did I flag (not silently fix) every comment whose correctness I couldn't verify?
- [ ] Every new comment survives the wrong-edit test; deletion pass done; healthy comments
      left in their original voice?
- [ ] No banners, headers, commented-out code, emoji, narration, bare TODOs or suppressions?
- [ ] Language-specific checks from the reference's self-check section done?
- [ ] `scripts/comments-only.sh` passed: the diff is comments only?

## 7. Report

```
FILE: path/to/file.ext
AUDIT: 14 existing / 5 kept, 4 fixed (2 stale, 1 signature drift, 1 vague), 5 deleted
ADD:   +5 comments, +3 doc blocks
moved: <contract relocations, if any>
skipped: <generated / vendored / per-file-ignored paths>
proposed (NOT applied): <code changes you would make in a separate pass>
flagged (needs a human): <file:line and why you could not decide>
```

## Loading in Oh My Pi

Relative paths in this skill (`references/…`, `scripts/…`) resolve against the skill's own directory. Read them with `skill://comment-audit/<relative-path>`. When a shell command needs a real filesystem path, that directory is `<OMP_HOME>/skills/comment-audit/` — `~/.omp/agent/skills/comment-audit/` by default. Invoking `/skill:comment-audit` also prints the resolved location.
