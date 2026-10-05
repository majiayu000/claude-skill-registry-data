---
name: code-review
description: Clean up code comments, then review code with comprehensive and quick modes. Use when reviewing code changes, PRs, or specific files for quality, bugs, and best practices.
argument-hint: '[target] [--quick] [--logic] [--architecture] [--security] [--performance] [--history] [--test] [--interface] [--clean-code] [--functional] [--typescript] [--project] [--library-use] [--staged] [--unpushed] [--all] [--changed] [--multi] [--rereview]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Code Review: $ARGUMENTS

Review the code related to: **$ARGUMENTS**

## Reference files (load what the run needs)

| File | Load when |
|------|-----------|
| `references/agents.md` | Step 3c in comprehensive mode — the per-agent briefs for Agents 1–10, plus how language / project / library-use reviews plug in. |
| `references/scoring-and-output.md` | Steps 4, 4.5 and 5 in comprehensive mode — confidence scoring, likelihood/blast-radius triage, and the output format. |

Flag parsing, scope resolution, and comment cleanup (Steps 1–3b.6) need neither.

## Usage

```
/code-review                          # Comment cleanup + all 9 review aspects, default scope
/code-review --quick                  # One integrated review pass, no scorer-agent round
/code-review <target>                 # Comment cleanup + all 9 aspects, scoped to target
/code-review --architecture           # Architecture only
/code-review --functional             # Functional principles only
/code-review --security --performance # Two aspects
/code-review --logic src/auth/        # One aspect, scoped to target
/code-review --typescript             # TypeScript-specific review only
/code-review --project                # Project's own review-project checks only
/code-review --library-use            # Library-usage review only (vs the repo's library-use reference)
/code-review --all                    # Whole repo
/code-review --changed                # Unstaged changes only
/code-review --staged                 # Staged changes only (errors if nothing staged)
/code-review --unpushed               # Files changed across all unpushed commits (errors if nothing unpushed)
/code-review --multi                  # All aspects + external advisors
/code-review --multi --architecture   # Architecture only + external advisors
/code-review --all --multi            # Whole repo + external opinions
/code-review --rereview               # Re-review automatically after fixes are applied
```

`--rereview` composes with comprehensive aspect selections, `--quick`, scope flags, or `--multi`.

## Review Modes

The default mode is comprehensive: run all selected perspectives independently, then independently score and triage their findings.

Every mode first runs `review-comments --fix` over the resolved scope. Comment cleanup is a preflight edit, not a review perspective: its results are reported separately and are never confidence-scored or promoted into Critical/Should Fix findings.

`--quick` is an explicit low-latency preset for routine small changes. It keeps the normal scope resolution, project-guideline checks, severity output, fix prompt, and optional `--rereview` loop, but uses one integrated read-only reviewer and no separate scorer agents. It does not activate automatically from diff size: a tiny auth, migration, or concurrency change may still deserve the comprehensive mode.

`--quick` composes with a target, one scope flag, or `--rereview`. It cannot be combined with aspect flags or `--multi`; abort with `--quick is a complete review preset; remove the aspect flags or --multi.`

## Aspect Selection

Aspect flags let you run a subset of the review agents instead of all 9. Flags are additive — pass as many as you want. Comment quality is absent from this list because its fix pass always runs before the selected review.

| Flag | Maps to |
|------|---------|
| `--logic` | Agent 1: Bug & Logic Review (inline) |
| `--architecture` | Agent 2: Architecture Review (delegates to `/review-architecture`) |
| `--security` | Agent 3a: Security Review (inline + delegate to `/review-security`) |
| `--performance` | Agent 3b: Performance Review (inline + delegate to `/review-perf`) |
| `--history` | Agent 4: Historical Context Review (inline) |
| `--test` | Agent 5: Test Quality (delegates to `/test --review`) |
| `--interface` | Agent 6: Interface Design (delegates to `/review-interfaces`) |
| `--clean-code` | Agent 7: Clean Code (delegates to `/review-cleancode`) |
| `--functional` | Agent 7b: Functional Review (delegates to `/review-functional`) |

Two further aspects are **conditional add-ons** — in the default (no-aspect-flag) run they are included automatically when they apply; with explicit aspect flags they run only if their own flag is passed (see Step 3b.5 for detection):

| Flag | Maps to |
|------|---------|
| `--cli` | Agent 8b: Project-Shape Review — delegates to `review-cli`. Auto-included when the repo ships a console entry point. Orthogonal to language: it composes with the language review rather than replacing it. |
| `--typescript` / `--swift` / `--python` | Agent 8: Language Review — delegates to the matching `review-<language>` skill (e.g. `review-typescript`, `review-swift`, `review-python`). Auto-included when the scoped files are of that language. |
| `--project` | Agent 9: Project-Specific Review — delegates to the project's own `review-project` skill. Auto-included when that skill exists in the repo. |
| `--library-use` | Agent 10: Library-Use Review — delegates to `review-library-use` (checks code against the repo's `library-use` conventions). Auto-included when the repo has a `library-use` reference. |

**Aspect rules:**
- In comprehensive mode, no aspect flags → run all 9 core agents, **plus** any detected language review, the project review, and the library-use review if present.
- One or more aspect flags → run only those agents, skip the rest. The conditional add-ons run only if `--typescript` / `--cli` / `--project` / `--library-use` (or another `--<language>`) is among the flags.
- `--quick` is a complete preset and cannot be combined with aspect flags.
- `--multi` composes with any aspect selection.
- The non-flag portion of `$ARGUMENTS` is the review target (e.g. `src/auth/`).

Agents 8–10 are the plug-and-play extension layer (add a language by creating a `review-<language>` skill; add a shape by creating one like `review-cli`; a project adds its own `review-project`). Details in `references/agents.md`.

## Scope Selection

Scope flags determine *which files* the reviewers inspect. The resolved scope is passed through to every review agent or delegated sub-skill.

| Flag | Meaning |
|------|---------|
| `--staged` | Review staged changes only (`git diff --cached`). |
| `--unpushed` | Review files changed across unpushed commits only (`git diff <last-pushed>..HEAD`). |
| `--changed` | Review unstaged changes only (`git diff`). |
| `--all` | Review the whole repo (`git ls-files`). |

**Scope rules:**
- Exactly one scope flag may be passed. Multiple → error.
- **Default (no scope flag):** behave as `--staged` if anything is staged; otherwise auto-fall back to `--changed`. Announce the resolved mode at the start of the run so the user isn't surprised. (`--unpushed` is never auto-selected — it's opt-in only.)
- **Explicit `--staged` with nothing staged:** abort immediately with `Nothing staged. Re-run with --all or --changed.` (Explicit ≠ default — no silent fallback.)
- **Explicit `--unpushed` with nothing unpushed:** abort immediately with `Nothing unpushed. Re-run with --staged, --changed, or --all.` If there is no remote/upstream (or the range walks back to the root commit) so the range can't be determined reliably, abort and ask the user to pick another scope. (Explicit ≠ default — no silent fallback.)
- **Target argument wins:** if a non-flag target is provided (e.g. `/code-review src/auth/`), it overrides scope flags entirely. The target is passed to all sub-agents as-is.

## Gotchas
- Both modes silently drop findings below the 80-point confidence threshold. Comprehensive mode uses independent scorers; quick mode trades that independent validation for a single reviewer's self-filter.
- In comprehensive mode, Step 4.5's triage never drops anything silently — every issue routed out of the main severity sections appears in the `Improbable / Not Worth Handling` appendix with its `file:line` and a one-line reason. Quick mode omits low/medium-impact improbable findings entirely to stay concise.
- With `--staged`, the comment preflight edits the working-tree copies and does not stage them. Announce that the cleanup must be staged separately; never run `git add` implicitly.

## Step 1: Locate and Read Project Guidelines
First, find and read any CLAUDE.md files in the repository root and relevant directories to understand project-specific conventions and rules.

## Step 2: Identify Relevant Code
Search for and identify all files related to "$ARGUMENTS". Use Glob and Grep to find:
- Direct implementations
- Related tests
- Usages/consumers of this code

## Step 3: Resolve Scope and Run the Review

### 3a. Parse flags

If the removed `--comments` aspect flag is passed, abort with `Comment cleanup now runs automatically before every code review. Use review-comments directly for a standalone comment report.`

Strip aspect flags (`--logic`, `--architecture`, `--security`, `--performance`, `--history`, `--test`, `--interface`, `--clean-code`, `--functional`, `--typescript`, `--project`, `--library-use`), scope flags (`--staged`, `--unpushed`, `--all`, `--changed`), `--quick`, `--multi`, and `--rereview` from `$ARGUMENTS`. The remainder is the review target.

If `--quick` appears with any aspect flag or with `--multi`, abort with `--quick is a complete review preset; remove the aspect flags or --multi.` It may compose with a target, one scope flag, and `--rereview`.

In comprehensive mode, if any aspect flags are present, launch ONLY the corresponding agents (including the conditional add-ons only when a `--<language>`/`--cli`/`--project`/`--library-use` flag is passed). Otherwise launch all 9 core agents plus whatever Step 3b.5 detects. In quick mode, follow the single-reviewer branch in Step 3c.

### 3b. Resolve scope

If a non-flag target was provided, skip this section — pass the target through to every agent as-is.

Otherwise, resolve the scope:

1. If more than one scope flag was passed → error: `Pass only one of --staged, --unpushed, --all, --changed.`
2. If `--staged` was passed explicitly:
   - Run `git diff --cached --name-only`. If empty → abort: `Nothing staged. Re-run with --all or --changed.`
   - Resolved scope: `staged`.
3. If `--unpushed` was passed explicitly:
   - Resolve the range: `git rev-list HEAD --not --remotes` (oldest unpushed commit's parent → HEAD). If empty → abort: `Nothing unpushed. Re-run with --staged, --changed, or --all.` If there is no remote/upstream, or the range walks back to the root commit, abort and ask the user to pick another scope.
   - Resolved scope: `unpushed`.
4. If `--changed` was passed: resolved scope is `changed`.
5. If `--all` was passed: resolved scope is `all`.
6. If no scope flag was passed (default):
   - Run `git diff --cached --name-only`. If non-empty → resolved scope is `staged`.
   - Otherwise → resolved scope is `changed`.
   - Announce the resolution: `No scope flag — defaulting to --staged` or `No scope flag and nothing staged — defaulting to --changed`.

Compute the file list once based on resolved scope:
- `staged` → `git diff --cached --name-only`
- `unpushed` → `git diff --name-only $(git rev-list HEAD --not --remotes | tail -1)^..HEAD`
- `changed` → `git diff --name-only`
- `all` → `git ls-files`

This file list is passed to inline agents and is also used to build the target argument for sub-skills that don't natively support `--changed` (see 3c).

### 3b.5. Detect language & project reviews

Determine which conditional add-on reviews apply. In comprehensive mode these become additional agents. In quick mode their skill/reference text becomes guidance for the single integrated reviewer. Skip this entirely if explicit aspect flags were passed **and** none of them is `--typescript`/`--cli`/`--project`/`--library-use`/another `--<language>` — in that case the user asked for a specific subset and add-ons don't run.

**Language detection registry.** For each language below, it applies if the resolved file list matches its extensions, or (for the `all` scope / when the file list is empty) the repo root has its marker file. If it applies **and** a `review-<language>` skill is installed, include that agent in comprehensive mode or record its `SKILL.md` as guidance for quick mode.

| Language | File extensions | Repo marker | Skill |
|---|---|---|---|
| TypeScript | `.ts` `.tsx` `.mts` `.cts` | `tsconfig.json` | `review-typescript` |
| Swift | `.swift` | `Package.swift`, `*.xcodeproj`, `*.xcworkspace` | `review-swift` |
| Python | `.py` `.pyi` | `pyproject.toml`, `setup.py` | `review-python` |
| Rust | `.rs` | `Cargo.toml` | `review-rust` |

*(To add a language: create a `review-<language>` skill and add a row here.)*

**Project-shape detection.** Shapes are orthogonal to language — a CLI is reviewed the same way whether it is Python or Rust. If the shape applies **and** the matching skill is installed, include that agent in comprehensive mode or record its `SKILL.md` as guidance for quick mode. If the skill is not installed, skip silently.

| Shape | Detected by | Skill |
|---|---|---|
| CLI | `[project.scripts]` / `[project.entry-points."console_scripts"]` in `pyproject.toml`, `[[bin]]` or `src/main.rs` in a Cargo project, `bin` in `package.json`, or a `main`-package `cobra`/`urfave` import in Go | `review-cli` |

**Project review detection.** If the repo defines its own project review skill at `.claude/skills/review-project/SKILL.md` **or** `.agents/skills/review-project/SKILL.md`, include the project review agent in comprehensive mode or record its `SKILL.md` as guidance for quick mode. If neither exists, skip silently.

**Library-use review detection.** If the repo has a `library-use` reference at `.claude/skills/library-use/SKILL.md` **or** `.agents/skills/library-use/SKILL.md`, include the `review-library-use` agent in comprehensive mode or record the reference as guidance for quick mode. If neither exists, skip silently (suggesting `library-docs` once is fine, but don't block the review).

Check both paths — `.claude/skills/` is where Claude Code puts project skills; `.agents/skills/` is where the other harnesses discover them. In some projects the latter is a symlink to the former, so either check finds it; others may only have `.agents/skills/`.

Announce what got auto-included. In comprehensive mode, use messages such as `Detected TypeScript — adding review-typescript` or `Detected a CLI entry point — adding review-cli`. In quick mode, say `Detected TypeScript — applying review-typescript guidance in the quick review` (and likewise for project and library-use guidance).

### 3b.6. Clean up comments

Before launching any review agent, invoke `review-comments --fix` exactly once against the resolved scope:

| Resolved scope | Invocation |
|---|---|
| `staged` | `review-comments --staged --fix` |
| `unpushed` | `review-comments --unpushed --fix` |
| `changed` | `review-comments --changed --fix` |
| `all` | `review-comments --all --fix` |
| local path target | `review-comments <target> --fix` |
| other target, such as a PR | `review-comments <resolved local source file list> --fix` |

Treat its output as a preflight cleanup summary, not as review findings. Report how many comments were removed or rewritten and list any comment issues it could not safely fix, but do not send those items through confidence scoring or severity triage. Continue immediately when it finds nothing.

If a non-file target has no writable local source files, skip the cleanup and state that it requires a local checkout; do not turn that limitation into a review finding.

Keep the file list resolved in Step 3b even if cleanup edits change git status. Review the current contents of those same files, using the originally resolved diff or target to identify the intended change. With `staged` scope, explicitly say the cleanup edits are unstaged and must be staged separately; do not mutate the index.

### 3c. Run the selected mode

#### Quick mode (`--quick`)

Do not load `references/agents.md`. Launch exactly **one read-only review agent** and give it the resolved scope or target. Use the harness's fast read-only profile or lower per-agent reasoning effort when available. It must not delegate to sub-skills or dispatch more agents.

Give the reviewer this integrated brief:

- Read the applicable `AGENTS.md` / `CLAUDE.md` files, the scoped diff or files, relevant callers/consumers, and related tests.
- Review correctness, edge cases, error handling, regressions, missing or weak tests, security red flags, and interface compatibility. Flag obvious performance hazards only when directly supported by the changed path.
- If Step 3b.5 detected language, project, or library-use guidance, read those matching `SKILL.md` files as review references and apply their checks directly. Do not invoke them as skills.
- Return only actionable findings supported by a concrete code path. For each finding, include severity (`Critical`, `Should Fix`, or `Nice to Have`), `file:line`, what is wrong, why it matters, a concise fix, self-confidence from 0–100, likelihood (`routine`, `plausible`, `rare`, or `theoretical`), and blast radius (`low`, `medium`, or `high`). For `rare` or `theoretical`, name the reachability reason and cite any excluding guard.
- Self-filter aggressively: omit findings below 80 confidence and omit `rare`/`theoretical` findings with low or medium blast radius. Keep rare high-blast-radius findings and tag them with the short reachability reason.
- Return `No actionable findings.` if nothing survives.

After the agent returns, deduplicate its findings and render the surviving items under `Critical Issues (Must Fix)`, `Improvements (Should Fix)`, and `Suggestions (Nice to Have)`, omitting empty sections. Explain what is wrong, why it matters, and how to fix it. Do not show self-confidence metadata and do not launch scorer agents. Then continue to Step 6.

#### Comprehensive mode

**Load `references/agents.md`** — it carries the brief for each of Agents 1–10.

Launch the selected review perspectives in parallel, queuing successive batches when runtime capacity requires it.

**Launch workers that return findings without editing files.** Disable delegation tools for ordinary reviewers where supported; read-only access alone does not prevent delegation. If a reviewer coordinates verification, name the checks, bound the descendants, and define when it should stop. Workers can read the relevant sub-skill directly when their harness has no Skill tool.

Each agent should output a list of issues. For each issue, include: what the problem is, where it is (file + line), and why it matters. Do NOT assign confidence scores — scoring happens in a separate pass.

**Sub-agent invocation pattern.** When a sub-agent delegates to a sub-skill, pass the resolved scope through directly:

| Resolved scope | Argument passed to sub-skill |
|---|---|
| `staged` | `--staged` |
| `unpushed` | `--unpushed` |
| `changed` | `--changed` |
| `all` | `--all` |
| target given | the target itself (e.g. `src/auth/`) |

All delegated review sub-skills (`review-architecture`, `review-security`, `review-perf`, `review-interfaces`, `review-cleancode`, `review-functional`, `review-typescript`, `test --review`) accept `--staged | --unpushed | --changed | --all`. No special-casing needed. The project's `review-project` skill is expected to accept the same scope flags — if it doesn't, pass it the target/file list instead.

Inline agents (no delegation) work directly against the file list computed in step 3b.

## Step 3.5: External Advisor Reviews (--multi only)

If `--multi` flag is present in $ARGUMENTS, also get external opinions:

Use the **Skill tool** to invoke `second-opinion --quick`, which queries every external advisor it has configured, in parallel. (The advisor roster lives in the `second-opinion` skill — don't enumerate it here.) Phrase the prompt according to the resolved scope from step 3b:

- `staged` → "Review the staged changes (`git diff --cached`) in this repository."
- `unpushed` → "Review the changes across all unpushed commits (`git diff` against the last pushed commit) in this repository."
- `changed` → "Review the unstaged changes (`git diff`) in this repository."
- `all` → "Review the codebase in this repository as a whole."
- target given → "Review the following target in this repository: `<target>`."

Then append: "Provide a focused code review in 300 words or less covering: potential bugs or edge cases, security concerns, performance issues, and architecture/pattern violations."

**IMPORTANT:** Do NOT proceed to Step 4 until the second-opinion results have been fully received. Wait for all background commands to complete and collect their output before continuing. This prevents completion notifications from appearing after the review summary. If an advisor is missing or errors out, continue with whichever responded — don't drop the others.

## Steps 4, 4.5 and 5: Score, Triage, Format (comprehensive mode only)

Skip these steps in quick mode; Step 3c already produced the filtered, formatted review. In comprehensive mode, **load `references/scoring-and-output.md`** and follow it. In short: score every issue with independent parallel scorers (>= 80 passes), have those same scorers return likelihood + blast radius so improbable findings route to an appendix instead of the work list, then render the severity sections.

When that reference is done, **come back here and do Step 6** — the rendered output is not the end of the run.

## Step 6: Offer to Fix

**This step is mandatory.** Rendering the review output is *not* the end of the workflow — do not end the turn after printing the findings. If there is at least one **Critical** or **Should Fix** finding, you MUST call the **AskUserQuestion tool** so the user picks a fix scope by selection instead of typing one out.

Build the options list from the severity tiers that actually have findings, most-inclusive first:

| Option | Fixes | Include when |
|---|---|---|
| **"Fix everything"** | Critical + Improvements + Suggestions | there are `Suggestions (Nice to Have)` findings alongside at least one Critical or Should Fix finding |
| **"Fix Critical + Should Fix"** | Critical + Improvements | there are both Critical and Should Fix findings |
| **"Fix Critical only"** | Critical | there are Critical findings |
| **"Fix Should Fix"** | Improvements | there are Should Fix findings but no Critical findings |
| **"Don't fix anything"** | nothing | always — last option |

AskUserQuestion takes at most 4 options, so when all tiers are populated drop the narrowest fix option (`Fix Critical only`) rather than `Don't fix anything` — the user can still ask for a narrower scope in free text.

Skip this step entirely (no prompt) only when there are no Critical and no Should Fix findings — a run that surfaced nothing but suggestions has nothing worth gating on.

Build the options only from the `Critical Issues`, `Improvements`, and `Suggestions` sections. **Never include `Improbable / Not Worth Handling` items** — not even under "Fix everything". Step 4.5 already judged them not worth doing, and offering to fix them reintroduces exactly the noise the appendix exists to remove.

When the user selects a fix option, apply the fixes for exactly the chosen severity tier(s) — no more, no less.

## Step 7: Re-Review After Fixes (`--rereview` only)

If `--rereview` was passed AND fixes were applied in Step 6, automatically run the review again to verify the fixes landed cleanly and didn't introduce new issues:

- Re-run Steps 3–6 with the **same review mode, aspect, `--multi`, and target/scope selection** as the original run.
- Review the **same file list** computed in step 3b — fixes turn staged files into unstaged edits, so re-resolving scope from scratch could miss them. Reuse the original file list directly rather than recomputing from `git diff`.
- Announce the re-review at the start, e.g. `Re-reviewing after fixes (--rereview)`.
- The re-review's Step 6 fix prompt runs as normal. This forms a natural loop: review → fix → re-review → fix … It terminates when the re-review surfaces no Critical/Should Fix findings (Step 6 is skipped) or the user picks "Don't fix anything".

Without `--rereview`, Step 6 ends the run after fixes are applied — the user must invoke `/code-review` again manually to verify.

## Examples

**Clean comments, then review the default scope with all 9 agents:**
> /code-review

Runs `review-comments --fix`, then 9 parallel review agents (bug/logic, architecture, security, performance, historical context, test quality, interface design, clean code, functional principles) against staged changes (or unstaged changes if nothing is staged). Comment cleanup is summarized separately; review findings are prioritized by severity.

**Quick review of a routine small change:**
> /code-review --quick

Runs one integrated read-only reviewer against staged changes (or unstaged changes if nothing is staged). It applies detected language, project, and library-use guidance directly, self-filters to well-supported actionable findings, and skips the independent scorer-agent round.

**Focused single-aspect review:**
> /code-review --architecture

Runs only the architecture & patterns agent. Use this when you already know which concern you care about and don't want to wait on the other 8 agents or sift through their output. Flags are additive — combine them (e.g. `--security --performance`) to run a handful of aspects without running them all.

**Whole-repo review:**
> /code-review --all

Runs comment cleanup and all 9 agents against every file in the repo (`git ls-files`). Use this for a fresh audit of an unfamiliar project, before a major release, or when nothing in the working tree is changed. Composes with aspect flags and `--multi`, e.g. `/code-review --all --architecture --multi`.

**Cross-model consensus review:**
> /code-review --multi

Runs the same 9 review agents plus external reviews from every advisor `second-opinion` has configured, after comment cleanup. The output includes a cross-model agreement section highlighting issues where the internal agents and external advisors converge, giving higher confidence to consensus findings. `--multi` composes with aspect and scope flags, e.g. `/code-review --multi --architecture` or `/code-review --all --multi`.

**Review, fix, then re-review automatically:**
> /code-review --rereview

Runs the review, offers the fix prompt (Step 6), and — once fixes are applied — immediately re-runs the same review on the same files to confirm the fixes landed and introduced no new issues. The loop continues until a re-review comes back with no Critical/Should Fix findings or the user declines to fix. Composes with aspect, scope, and `--multi` flags.

## Troubleshooting

### Too many changed files for agents to handle
**Solution:** Narrow the review scope by targeting a specific directory or file pattern (e.g., `/code-review src/auth/`) instead of the entire changeset, or break the PR into smaller, focused reviews.

### Agent returns shallow or redundant findings
**Solution:** Ensure the review target is specific enough to give agents meaningful context; vague targets like "everything" produce generic results. Re-run with a focused target and verify that CLAUDE.md contains project-specific patterns the agents can check against.
