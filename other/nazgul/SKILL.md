---
name: nazgul
description: Use when the user runs /nazgul [target], /nazgul project, or /nazgul reviewed. The first two dispatch the Nine — one agent per check file — to inspect either a diff (default — uncommitted changes) or the standing project tree, aggregating pass/fail/n/a verdicts into a single table. The `reviewed` verb stamps the rubric-review state file consumed by /preflight; no agents dispatched. Checks live as markdown files under `checks/`, scoped via frontmatter — `scope` may be `diff` (default), `project`, or a list `[diff, project]`. Project-local overrides take precedence. Audit only — never fixes, commits, or files issues on its own.
purpose: Dispatches a panel of checks against a diff or project tree and aggregates the verdicts.
user_invocable: true
stage: weigh
---

# Nazgûl

Calls the riders out. Each check is a small markdown file; each file becomes a separate agent, sent forth in parallel against a chosen field. Every rider returns a single line — `pass | fail | n/a` and a short note — and the parent gathers them into one table.

The Nine ride two fields:

- **diff** — *what changed*. The default. Riders inspect a captured diff (uncommitted, branch, or sha range).
- **project** — *what stands*. Invoked with `/nazgul project`. Riders inspect the standing project tree — naming, lint config, tests, CI, badges, the foundations of the place.

Each check declares which field it belongs to via frontmatter; the parent dispatches only the riders whose scope matches the chosen field.

Nazgûl is an **auditor**. It finds and names; it does not mend, commit, push, or file issues. What is done with the findings is the user's word, handed off to other skills when needed.

## Workflow

### 0. Bookkeeping verbs

Some arguments do not summon riders at all — they only update bookkeeping the parent skill keeps about its own rubrics.

| First argument | What it does |
|---|---|
| `reviewed` | Stamps the rubric-review state file with `now`, recording that the user has just walked the rubrics under `checks/` and judged them sound (or amended any that drifted). Run the hook `~/.claude/hooks/nazgul-checks-mark-reviewed.sh` and stop — no agents are dispatched, no table is printed. The next `/preflight` reads the new mtime and clears the corresponding overdue task. |

If the first argument matches a bookkeeping verb, do its job and stop. Otherwise fall through to step 1.

### 1. Resolve scope and target

Parse the first argument to decide the **scope**:

| First argument | Scope | Target |
|---|---|---|
| `project` | `project` | the project root tree |
| (none) | `diff` | uncommitted changes |
| `branch` | `diff` | the current branch versus its base |
| `<sha>` | `diff` | the single commit |
| `<sha1>..<sha2>` | `diff` | the range |

For **diff scope**, capture the diff using one of these forms:

| Argument | How to capture the diff |
|----------|--------------------------|
| (none) — **uncommitted** | `git diff HEAD` plus, for each untracked path from `git ls-files --others --exclude-standard`, a synthetic `+++` block of its contents |
| `branch` | `git diff $(git merge-base HEAD <base>)..HEAD`, where `<base>` is the first of `master`, `main`, `origin/HEAD` that resolves |
| `<sha>` | `git show <sha>` |
| `<sha1>..<sha2>` | `git diff <sha1>..<sha2>` |

Capture the diff **once** and hold it as `DIFF`. If the diff is empty, tell the user and stop — do not summon the riders to an empty field.

**Delivery to riders.** If `DIFF` is under 500 lines, pass it inline in each agent prompt. Otherwise write it once to `build/nazgul/diff-<timestamp>.patch` and pass the path instead. Create `build/nazgul/` if absent.

For **project scope**, resolve the project root via `git rev-parse --show-toplevel` and hold it as `ROOT`. If that fails, the working directory is not inside a git repo — tell the user and stop. No diff is captured; the tree itself is the field.

### 2. Read the roll

The checklist is a folder of markdown files, searched in this order:

1. `.skadi/nazgul/checks/*.md` in the project root (project-local override).
2. `<skill-dir>/checks/*.md` (the default roll, shipped with the skill).

The first folder that exists and holds at least one `*.md` wins; the other is ignored (no merging). If neither folder exists or both are empty, tell the user there are no checks configured and stop.

Each check file has YAML frontmatter and a prompt body:

```markdown
---
name: No commented-out code
scope: diff                  # optional; default diff. May be a single value or a list.
# scope: [diff, project]     # list form — the check rides in every named scope.
agent: Explore               # optional; default general-purpose
autofix: false               # optional; reserved for future --fix flag
---

Flag any commented-out code blocks introduced in the diff. If a
commented block documents intent or explains alternatives, note
it but pass. Otherwise fail with file:line of the commented block.
```

- `name` — shown in the report table. Required.
- `scope` — which field this check rides. May be a single value (`diff` or `project`) or a list (`[diff, project]`). Default is `diff` if absent. A check participates in scope *S* if *S* appears in its declared scope set. List-form checks must be written target-agnostically (see below).
- `agent` — subagent type to dispatch. Default `general-purpose` (tends to honour format demands). Declare `Explore` only when the check is read-only *and* the author has verified Explore answers in the required shape — Explore is trained to narrate and will often return prose instead of one line.
- `autofix` — reserved flag for a future `--fix` mode. Ignore it for now.

**Target-agnostic prose.** A check declared in two scopes will be dispatched once per invocation, with the target swapped to match the chosen field. Write its body so it reads sensibly under either target — e.g. *"Scan the given target — whether the supplied diff or the standing project tree — for X."* The dispatcher selects the right target line at prompt-build time (step 3); the rubric does not name *diff* or *project* exclusively.

After scope filtering, assign each surviving check an **index** starting at 1, in stable filename-sorted order. The index travels with the rider to the reply. If the chosen scope yields no checks, tell the user and stop.

### 3. Summon the riders

Dispatch one **Agent** call per check, **all in a single message**, so they ride in parallel.

Each agent prompt must be built in this exact order — the reply contract comes **first**, not last, so it is not drowned by the check body:

1. The rider's identity: `You are rider #<N> of /nazgul: "<check name>".`
2. The reply contract, spelled out hard:

   > **Your ENTIRE response must be a single line in the form:**
   > `<N>|<status>|<note>`
   >
   > where `<status>` is one of `pass`, `fail`, `n/a`,
   > and `<note>` is a short human-readable reason containing no `|`.
   >
   > **Do not** write preamble, acknowledgements, summaries, markdown,
   > headers, fences, or any additional lines. The parent's parser
   > will scan your reply for the first line matching this shape and
   > ignore the rest — but a well-behaved rider returns the one line
   > and stops.
   >
   > WRONG: `Here is my finding:\n1|pass|nothing flagged`
   > WRONG: `## Verdict\n\nThe diff does not introduce…\n\n1|pass|ok`
   > RIGHT: `1|pass|nothing flagged`

3. The target — depends on scope:
   - **diff scope**: either the inline `DIFF`, or `The diff is at <path>. Read it first.`
   - **project scope**: `The project root is <ROOT>. Read whatever files you need under it.`
4. The prompt body from the check file, verbatim.
5. A closing reminder: `Remember — reply with one line only, in the form shown above. Nothing else.`

Riders may read any file in the tree when context is needed beyond the diff. Riders must never write, edit, commit, push, or file issues — they are auditors.

Give each rider a **timeout of 60 seconds**. A rider that errors or times out yields a `?` row in the report.

### 4. Aggregate

Scan each reply line by line for the **first** line that matches the regex `^\s*(\d+)\s*\|\s*(pass|fail|n/a)\s*\|(.*)$`. Take that line and split it into `<index>`, `<status>`, `<note>` — only the first two `|` characters bound the fields, so notes may contain `|`. Validate: the index must match the rider's assigned number; the status must be one of `pass`, `fail`, `n/a`. If no matching line is found, or validation fails, mark the row `?` and keep the raw reply for the dump beneath the table.

Print one table:

| # | Check | Status | Note |
|---|-------|--------|------|
| 1 | … | one of ✅ pass / ❌ fail / — n/a / ? | … |

One glyph per row, not three. End with:

> **N failed / M checks** — where M counts every rider, including n/a and ?.

For any row marked `?` or malformed, print the raw reply in a fenced block below the table so the cause can be seen.

### Example output

```
| # | Check                          | Status  | Note                                  |
|---|--------------------------------|---------|---------------------------------------|
| 1 | No commented-out code          | ✅ pass | nothing flagged                        |
| 2 | No new TODOs without owner     | ❌ fail | src/app.ts:42 — "TODO: fix later"      |
| 3 | Imports alphabetised           | — n/a   | no import changes in diff              |

1 failed / 3 checks
```

## After the report

The knight's duty ends at the table. Follow-through is the user's to command:

- **To fix a finding** — say so, and I reach for Edit. Or, for mechanical cases, a future `/nazgul --fix` flag will invoke only checks whose frontmatter declares `autofix: true`. Not built yet; named so the shape is known.
- **To file a finding as an issue** — invoke `/jira create` or `gh issue create` directly. A future `/nazgul --file-issues` flag may chain this. Not built yet.
- **To do neither** — the default. Fix the flaw before the next commit and rerun `/nazgul` to confirm.

## Checks

The default roll lives at `<skill-dir>/checks/*.md`. Each file is one check, as shown in step 2.

A repository may override the roll by placing its own files under `.skadi/nazgul/checks/*.md` at the project root. When that folder exists and holds any file, it replaces the default entirely — no merging. This lets a project tune the riders to its own code without touching the global skill.

## Promoting a check

If a check proves worth summoning on its own:

1. Copy `checks/<name>.md` to `skills/<name>/SKILL.md`.
2. Replace the check frontmatter with skill frontmatter — add `user_invocable: true` and a `description` field that will read well in the skill listing.
3. Prepend a small harness: resolve the target (step 1 above), dispatch a single agent with the prompt body, print the one-line verdict.

The prompt body — the truth of the check — does not change in the promotion.

## Rules

- Dispatch all riders in a single message. Parallel always; never sequential.
- Riders may read any file in the tree; riders must never write, edit, commit, push, or open a PR.
- For diff scope: if the diff is empty, tell the user and stop. Do not summon the Nine to an empty field.
- For project scope: if no checks bear `scope: project`, tell the user and stop.
- Reserve the riders for judgment. If grep or a linter can settle the matter, it is not a check.
- Nazgûl itself never commits, pushes, opens PRs, or files issues. Those actions belong to the user or to other skills the user invokes after the report.
