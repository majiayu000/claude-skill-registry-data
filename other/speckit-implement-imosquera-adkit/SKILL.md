---
name: speckit-implement
description: Execute tasks.md inside the feature's dedicated worktree
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: preset:worktree-isolation
argument-hint: Optional implementation guidance or task filter
user-invocable: true
disable-model-invocation: false
---

# Speckit Implement Skill

## Wrapper Layer

This preset wraps `/speckit-implement` (and any inner wrapper the core-flow seam
expands to). It adds exactly one thing: it `cd`s into the feature's dedicated
worktree before any filesystem write performed by the flow below. It does not
change how tasks are executed.

It is deliberately the **outermost** layer on `/speckit-implement`, so the `cd`
happens before any other layer reads or writes a file. See the ordering contract
in the root `README.md`.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

### 0. cd into the feature's worktree (MANDATORY — Principle VII)

Per BeadBits Constitution v2.3.0 Principle VII (Feature-Work Isolation),
/speckit-implement MUST execute with the agent's cwd set to the feature's worktree.
This step runs BEFORE any filesystem write performed by the rest of this
outline.

1. Resolve the current branch with `git rev-parse --abbrev-ref HEAD`. If the
   cwd is not inside a git worktree, ERROR with:
   "Cannot resolve feature: not inside a git worktree.
   Run /speckit-git-feature to create the feature branch and worktree."
   Do NOT proceed.

   Do NOT read `worktree_path` from `.specify/feature.json`. That field no
   longer exists: the file is per-worktree state carrying only `source_issue`,
   and the recorded path used to name the *previous* feature's worktree in any
   fresh worktree (issue #33).

2. Let `WT` be the worktree whose branch matches the current branch, found via
   `git worktree list --porcelain`. When the cwd is already inside that
   worktree, `WT` is `git rev-parse --show-toplevel`.

3. If no worktree matches the current branch:
   Emit a single-sentence warning:
   "This feature has no dedicated worktree (it is checked out in the main
   working tree). Proceeding in the current cwd; Principle VII isolation is
   not enforced for this invocation."
   Then proceed in the current cwd. Skip steps 4–6.

4. If `WT` is non-null but the directory does NOT exist on disk:
   The recorded path is machine-local (e.g. created in another clone or by
   another author) and is meaningless here. Emit a single-sentence warning:
   "Recorded worktree_path '<WT>' does not exist on disk (likely a path from
   another clone). Proceeding in the current cwd; Principle VII isolation is
   not enforced for this invocation."
   Then proceed in the current cwd. Skip steps 5–6.

5. If `WT` is non-null, exists on disk, and matches the current cwd
   (resolved to absolute path), proceed silently — no cd needed.

6. Otherwise (`WT` is non-null, exists, and differs from cwd):
   Prefix every subsequent shell invocation in this command with
   `cd "<WT>" && ...` so the cd is visible in the session log. All
   filesystem writes performed by the rest of this outline land inside
   the worktree. Do not silently rely on tools that ignore cwd
   (absolute-path file writers) as a substitute — the cd MUST appear
   in the session log for post-hoc isolation auditing.

### End cd-block (Principle VII enforcement complete)

### Core Flow

Everything below runs with the cwd established above. Every shell invocation in
the core flow inherits the `cd "<WT>" && ...` prefix from step 6 when one was
required.


## Wrapper Layer

This preset wraps `/speckit-implement` (and any inner wrapper the core-flow seam
expands to). It adds exactly one thing: a mandatory graph refresh as the final
implementation step. It does not change how tasks are executed.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

### Core Flow


## Dashboard — enter `implement`

```bash
REPORT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.specify/presets/progress-report/scripts/python/progress_report.py"
python3 "$REPORT" enter implement
```

For a long implement phase, you may refresh the card mid-way so the dashboard's
"ago" label stays fresh — re-run `enter implement --summary "<k/N tasks done>"` as
progress lands. It's cheap and idempotent.


## Wrapper Layer

This preset wraps `/speckit-implement` (and any inner wrapper the core-flow seam
expands to). It adds exactly one thing: a skill prelude that runs before any
implementation work starts. It does not change how tasks are executed.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

### Prelude — activate review/lens skills (MANDATORY — FIRST STEP)

Before the core flow below begins, check the host's available-skills list and
invoke each of the following via the Skill tool if listed:

- `ponytail:ponytail`
- `caveman`

Invoke them sequentially (ponytail first, then caveman). Treat any guidance,
constraints, or context produced by these skills as additional input that the
implementation must respect.

**Detection rules.**

- Only invoke a skill if it is explicitly listed as an available/user-invocable skill in this session. Do **not** guess names or attempt to install skills.
- If a skill is not available, skip it silently and continue. Missing skills are a no-op, not an error.
- If neither skill is available, proceed directly to the core flow without comment.

### Core Flow


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Wrapper Layer

This preset wraps `/speckit-implement` (and any inner wrapper the core-flow seam
expands to). It honors one design discipline while code is written, then runs
**one mandatory scan gate** after the core flow, before reporting completion. It
does not change how tasks are executed.

### Design discipline (applies while code is written)

Parse, don't validate. A validator says "this is fine, continue" and throws the
proof away the instant it returns; a parser takes a blob and returns either a
**more precise type** or a typed error. Encode what you checked in the type so
future code never re-checks.

Whenever this run touches code that ingests untrusted data (network, disk, env,
user input, `JSON.parse` / `json.loads`), prefer parsing over validating. The
principle is language-general; apply the idioms of whichever language you write:

1. **Boundary is untyped-safe, domain is precise.** Untrusted input enters as
   `unknown` (TypeScript) — never `any` — or as a value immediately fed to a
   parser (Python), never left as `Any`. `JSON.parse` returns `any` and
   `json.loads` returns `Any`; treat their output as raw until a parser has run.
2. **Parse at the boundary into branded / nominal domain types.** Turn `string`
   into `Email`, `number`/`int` into `UserId` (TypeScript: a non-exported
   `unique symbol` brand or a schema library's `.brand()`; Python: `NewType`, a
   pydantic/attrs model, or a frozen dataclass). Illegal states become
   unrepresentable; downstream code trusts the type instead of re-checking.
3. **Parsers return a discriminated Result, not a boolean and not a throw.**
   TypeScript: a `{ kind: "ok" | "err" }` union so failure is visible in the
   signature and exhaustiveness (`never`-narrowing) catches missing cases.
   Python: return the parsed model or raise a single typed parse error at the
   boundary — do not add boolean `isValid*` / `is_valid_*` / `validate*`
   functions that callers must remember to re-run.
4. **The cast is confined to the parser.** `x as Brand` (TS) / `cast(Brand, x)`
   (Python) is the one sanctioned lie, allowed only inside the parser module
   that owns that brand. Never forge a brand elsewhere.
5. **A schema library is welcome.** Zod / valibot / io-ts (TS) and pydantic /
   attrs / msgspec (Python) satisfy this discipline and are preferred over
   hand-rolled casts when the project already has one. The library is a tool;
   the boundary discipline is still yours.

Respect any project constitution and existing conventions. If the feature has no
TypeScript or Python surface, this discipline is a no-op and you proceed with the
stock flow.

### Core Flow

Apply the discipline above to any TypeScript or Python written by the flow below.


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Behavior

Execute the canonical stock `/speckit-implement` flow first, then run **one mandatory audit gate** before reporting completion.

### Stock Flow

Execute the canonical stock `/speckit-implement` flow unchanged.

### Mandatory Constitution Audit (runs AFTER all task execution)

After the stock flow finishes, when `.specify/memory/constitution.md` exists:

1. **List the principles** the audit must cover:

   ```sh
   python3 .specify/presets/constitution-audit/scripts/python/constitution_audit.py list
   ```

   Each printed line is one principle heading you MUST cover in the audit.

2. **Write the audit** to `<feature-directory>/constitution-audit.md` (feature directory comes from `.specify/feature.json.feature_directory`). Audit the code that was **actually written** during this run. For every principle listed above, write a section containing:
   - The principle heading text (so the validator can locate the section).
   - **A direct quoted span (>= 4 words) taken verbatim from that principle's body in the constitution.** Use double quotes, backticks, or a `>` blockquote. Paraphrases will fail validation.
   - A verdict line containing exactly one of: `PASS`, `VIOLATES`, or `N/A`.
   - If `VIOLATES`: a written justification naming the breaching tasks / files / decisions and the proposed mitigation or explicit waiver.
   - If `N/A`: a one-line justification for why the principle does not apply.

3. **Validate the audit** deterministically:

   ```sh
   python3 .specify/presets/constitution-audit/scripts/python/constitution_audit.py validate <feature-directory>/constitution-audit.md
   ```

   If this exits non-zero, the audit is incomplete or contains fabricated quotes. Fix the flagged entries and re-run validation. **Do not report completion until this command exits zero.**

When `.specify/memory/constitution.md` does **not** exist, skip the audit.

## Failure Policy

- A non-zero exit from `constitution_audit.py validate` is a hard stop on reporting completion. The implementation has run, but the audit must pass before the task is considered done.
- If the audit surfaces `VIOLATES` verdicts against the code just written, fix the breaching code (or record an explicit waiver in the audit) before reporting completion.
- The script enforces the quote-substring check; the LLM cannot work around it by paraphrasing or inventing plausible-sounding quotes.

## Completion Report

On success, include:
- The normal stock `/speckit-implement` completion summary
- Whether a constitution audit was performed (path to `constitution-audit.md` if so)
- Confirmation that `constitution_audit.py validate` exited zero
- Any `VIOLATES` verdicts and how they were resolved (fix or waiver)


### Mandatory anti-pattern scan (runs AFTER all task execution)

After the entire core flow above finishes, gate completion on a deterministic scan of the
TypeScript/Python changed during this run:

1. **Review the discipline items** the scan enforces:

   ```sh
   python3 .specify/presets/parse-dont-validate/scripts/python/parse_dont_validate.py checklist
   ```

2. **Scan the changed files** (no paths → the script inspects the git change
   set: working-tree changes **plus** work already committed on the current
   branch, so the gate still fires even if a post-implement hook has committed
   the implementation. Pass explicit paths/dirs to narrow, or `--base <ref>` to
   pin the branch base):

   ```sh
   python3 .specify/presets/parse-dont-validate/scripts/python/parse_dont_validate.py scan
   ```

   Both languages are analysed as real ASTs. Scanning **TypeScript** requires
   `node` on PATH and `typescript` installed in the project (the Node helper
   uses the TypeScript Compiler API). If the scanner exits `3` with a message
   that `typescript` is missing, install it (`npm i -D typescript`) and re-run —
   do not treat a missing parser as a pass.

3. **Resolve every finding.** For each reported `PDVxxx`, either:
   - **Fix it** — replace the validator / `any` / `Any` / stray cast with a
     parser that returns a precise type (this is the default and preferred
     outcome), or
   - **Waive it at the boundary** — if the finding is a legitimate narrowing
     cast or deserialization *inside the parser module*, add a
     `parse-dont-validate: allow PDVxxx (<reason>)` comment on that line (`//`
     for TypeScript, `#` for Python). Waive only at the trusted parser boundary;
     a waiver anywhere else is the bug this preset exists to catch.

   Re-run `scan` until it exits zero. **Do not report completion while it exits
   non-zero.**

If the run produced no TypeScript or Python, `scan` reports nothing to check and
exits zero — proceed normally.

## Failure Policy

- A non-zero exit from `parse_dont_validate.py scan` is a hard stop on reporting
  completion. Fix the flagged code or add a boundary waiver, then re-scan.
- Do not silence a finding by deleting the offending line's functionality, by
  widening a type to escape the regex, or by waiving outside a parser module.
  The point is a real parser at the boundary, not a green scan.
- If the feature has no TypeScript or Python, do not fabricate parsing work —
  the gate is a no-op.

## Completion Report

On success, include:
- The normal `/speckit-implement` completion summary from the core flow.
- Whether the parse-don't-validate scan ran and that it exited zero.
- Any findings that were fixed (what became a parser) and any that were waived
  at a parser boundary (with the reason).


## Failure Policy

- A skill that is *listed but errors out* during invocation halts the command — surface the error rather than proceeding past a failed prelude. (Missing/not-listed skills are not failures.)
- Do not downgrade the prelude to optional once a skill has been detected and invoked.

## Completion Report

On success, include:
- Which prelude skills were invoked (or that none were available).
- Confirmation that the canonical implementation flow ran after the prelude.
- Readiness for follow-up commands.


## Dashboard — `implement` done

```bash
REPORT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}/.specify/presets/progress-report/scripts/python/progress_report.py"
python3 "$REPORT" done implement --summary "<all tasks complete / what shipped>"
```

If implementation stalls on a blocker you can't clear:
`python3 "$REPORT" block implement --reason "<reason>"`.


### Graph Refresh (MANDATORY — LAST STEP)

After the entire core flow above has completed successfully, and before reporting
success, run one final graph refresh:

- Resolve the worktree root to graph with `git rev-parse --show-toplevel` (falling
  back to the current repository root).
- Execute `graphify update <resolved-worktree-path>`.

This graph refresh is mandatory and must run as the last implementation step.

## Failure Policy

- If `graphify` CLI is unavailable, unauthenticated, or the update command fails, return an error and mark the overall command as incomplete.
- Do not silently skip or downgrade this step to optional behavior.

## Completion Report

On success, include:
- Path used for graph refresh
- Confirmation that `graphify update` was executed as the final step
- Readiness for follow-up commands


## Constitution v2.3.0 Principle VII compliance note

This preset override exists specifically to close the resume-case gap left by PR #21
for `/speckit-implement`. The substantive operational behaviour it adds beyond the stock
`speckit-implement` skill is:

1. Resolving the feature's worktree from `git worktree list` by the current branch.
2. `cd`-ing into that path before any filesystem write performed by the implement outline.
3. Falling back to the current cwd (with a warning) when no worktree matches — e.g. the
   branch is checked out in the main working tree.

Deriving the path from git rather than reading a recorded `worktree_path` is deliberate:
that field was a machine-local absolute path committed to `.specify/feature.json`, so a
fresh clone aborted on a path it could never have, and a fresh worktree inherited the
previous feature's path outright (issue #33).

This override SUPERSEDES the in-skill worktree-resolution block previously added in
commit fee6cf3, which auto-created worktrees from the branch name. A missing worktree
directory degrades to the current cwd rather than erroring, so implementation stays
portable across clones.

The cd-block at `### 0.` is byte-identical across all four feature-scoped command
overrides (`/speckit-clarify`, `/speckit-plan`, `/speckit-tasks`, `/speckit-implement`)
modulo the slash-command substitution; this is enforced by SC-002 in
`specs/022-worktree-isolation-resume/quickstart.md`.
