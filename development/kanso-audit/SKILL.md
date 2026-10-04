---
name: kanso-audit
description: Use when the user asks for a code review, audit, pre-PR check, quality sweep, or pattern analysis of a diff, branch, module, or codebase. Also use when the user asks to "check" or "look over" their code for issues.
argument-hint: "[scope: diff|branch|module-path|all] [--fresh]"
allowed-tools: Bash(git *) Bash(gh *) Bash(rg *) Bash(find *) Bash(wc *)
---

# kanso-audit

Code review that reports findings, proposes concrete fixes, and — on approval — either hands cleanup off to `/kanso-refactor` or applies the fix in place. The principles from `kanso-principles` govern both the findings and the fixes.

Four phases:

- **Phase A — Investigation.** Read-only. Gather context and produce the findings report using the framework below. The skill's `allowed-tools` deliberately exclude Edit/Write so the investigation cannot modify files.
- **Phase B — Proposal.** Translate Tier 1 and Tier 2 findings into a numbered list. Tag each entry by *shape*: `refactor` (behaviour-preserving) or `behaviour-change` (correctness, security, architecture). Show the list in the approval block and wait.
- **Phase C — Apply.**
  - For `refactor`-shaped fixes → hand off to `/kanso-refactor audit-report`. That skill already enforces the behaviour-preserving rule, has the refactor taxonomy, and knows how to split work into commit-able groups. Don't reimplement it here.
  - For `behaviour-change` fixes → apply in place in the main session, one at a time, re-reading each file immediately before editing. These are not refactors; each is a real behaviour change and the user has approved it as such.
- **Phase D — Verify.** Run the project's verification command after fixes land. Paste the exit code. If no command exists, say so plainly — don't claim success without evidence.

## Always run inline

This skill runs in the calling chat. Never dispatch the audit via the Agent or Task tool, never delegate it to a subagent, never hand it off to a parallel runner. The findings, the approval gate, and any follow-up `/kanso-refactor` invocation all happen in the user's current transcript so the user can see and act on them directly. A subagent run produces output in a side window the user can't easily reach — that defeats the point.

Same rule for the follow-up: when `/kanso-refactor` is invoked from the approval gate, it runs inline too.

### Exception: `--fresh` for Phase A only

The user can pass `--fresh` to push the investigation into a read-only subagent. Use this when the audit needs an unbiased pass over code the current session has already touched — fresh context cuts the anchoring on decisions earlier in the transcript.

Under `--fresh`:

- **Phase A** runs in a subagent. Prefer the `Explore` agent type — it is read-only by construction. Give it the review framework below and the resolved scope, and ask for its output in the exact report format defined later. If the harness has no read-only subagent, say so in one line and run Phase A inline; `--fresh` degrades gracefully, it never blocks the audit.
- **Phases B, C, and D** continue inline as normal. The subagent's report lands back here as the findings; the approval gate, fixes, and verification all stay in the user's transcript.

Don't dispatch Phase A under `--fresh` and then quietly run Phases B–D in the subagent too. The fresh-context advantage is for review only; application and verification need to be where the user can see them.

(Deliberate design note: skill frontmatter now supports `context: fork` to run a whole skill in a subagent. It is not used here because only Phase A benefits from fresh context — the gate, fixes, and verification must stay inline.)

## Resolve the scope

`$ARGUMENTS` is one of:

- `diff` → the unstaged + staged working tree (default if empty)
- `branch` → commits on the current branch vs its upstream or `main`
- a path like `src/billing/` → everything under that path
- `all` → the whole repo (warn the user this will be noisy on anything larger than a small service)

If `$ARGUMENTS` is empty, default to `diff`. If the diff is empty, fall back to the last commit and tell the user.

`--fresh` is a modifier, not a scope. It can appear alongside any scope (e.g. `branch --fresh`) and triggers the Phase A subagent dispatch described above.

Gather context before reviewing:

- Diff: `!git diff HEAD` or `!git diff main...HEAD` depending on scope
- Changed files: `!git diff --name-only`
- Recent commits for voice calibration: `!git log -n 20 --oneline`
- Existing conventions: check for `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, `CONTRIBUTING.md`, linter configs

Read enough of the surrounding codebase to calibrate repo conventions. A finding that contradicts existing repo style is noise, not signal.

## The review framework

Findings sort into four categories (Google's pillars) and three tiers (signal priority).

### Categories

**Correctness** — Will this cause incorrect behaviour? Logic errors, off-by-ones, race conditions, missing error handling, security holes, auth bypasses, injection vectors, concurrency problems. Also: the anti-dilution pattern *defensive programming theatre*, which looks safe but hides failures.

**Clarity** — Can another developer read this quickly? Over-long functions, dense nesting, single-character or zero-entropy names, comments explaining *what* instead of *why*, over-engineering for imagined future needs.

**Consistency** — Does it match the surrounding codebase? Naming (mixed `get`/`fetch`/`load`), error handling style, decomposition patterns, API conventions, data-type choices. Anything a linter could catch is *not* a human review finding — note the missing linter rule instead.

**Architecture** — Does this code belong here? Does it introduce new coupling? Does it break backward compatibility? Does this add a dependency that deserves scrutiny? Does it anticipate a problem that doesn't exist yet? The senior progression: "does it work" → "is it good" → "will it survive".

### Tiers

**Tier 1 — Blocker.** Would cause production failures or material harm if merged. Logic bugs, breaking API changes, security holes, race conditions, data loss risks.

**Tier 2 — Important.** Would cause maintainability or scale issues. Architectural violations, missing tests for critical paths, performance regressions, increased coupling, anti-dilution patterns that will metastasise.

**Tier 3 — Polish.** Subjective or stylistic. Minor naming suggestions, small clarity improvements, nits.

### The signal rule

If Tier 1 + Tier 2 findings are fewer than 60% of total findings, the audit is generating noise. Cut Tier 3 findings aggressively until the ratio is above 60%, or omit the Tier 3 section entirely on a clean diff.

## The adversarial lens

Google's rule: think like an adversary, but be polite about it. Explicitly try to construct inputs that break the code:

- What happens with empty input, null, zero, negative, huge?
- What happens under concurrent access?
- What happens if the user is malicious? If the upstream service is down?
- What happens on retry? Is the operation idempotent?
- What happens if this is called a million times?

Surface the adversarial cases that *aren't* handled. Don't invent ones that don't matter.

## Anti-dilution patterns to flag specifically

From `kanso-principles`. Call these out by name so they're searchable:

- **Tautological comment** — comment restates the code
- **Step-marker comment** — `// Step 1:`, `// Now do X`
- **Defensive programming theatre** — nested try/catch returning None/null on failure
- **Filler variable** — `result = expr; return result`
- **Zero-entropy name** — `userDataProcessingResult`, `helperFunction`
- **Premature abstraction** — factory for one implementation
- **Fake test coverage** — tests assert on mocks, not behaviour
- **Structural erosion** — god function absorbing new requirements
- **Phantom bug** — guard against impossible state
- **Vanilla reimplementation** — hand-rolled version of a stdlib function

## The report format

Emit a single tight markdown document. No preamble, no "Let me know if you'd like me to…", no apology. Two-line summary, one-line findings, then the approval gate.

If there are no Tier 1 or Tier 2 findings, emit only the no-change message (see below) and stop.

### When there are findings

```markdown
# Audit: <short scope description>

**Files:** <n> · **Findings:** <t1> blocker, <t2> important, <t3> polish

<Two lines max. Lead with the highest-severity issue in plain language. State whether refactor alone covers it, or whether behaviour changes are also on the table.>

## Findings

[1] `path/to/file.ts:142` — <one-line description> (blocker, refactor)
[2] `path/to/file.ts:88` — <one-line description> (important, behaviour-change)
[3] `path/to/other.ts:14` — <one-line description> (important, refactor)
```

One line per Tier 1 and Tier 2 finding. Format: `[N] \`path:line\` — <what's wrong> (<tier>, <shape>)`. Use the anti-dilution pattern name in the description when one applies (`defensive theatre swallows db errors`, not `error handling issue`).

Tier 3 findings appear only when the user ran `all` scope or explicitly asked, and only as additional one-liners under a `## Polish` heading. If a finding has no safe mechanical fix (e.g. an architecture disagreement), include it in the list with `(no auto-fix)` and exclude it from the approval gate's apply count.

Omit "What's good" and "Proposed fixes" detail blocks. The one-liner is the proposal; the diff is the detail. If the user wants more context on a specific finding, they'll ask.

### When there are behaviour changes

After the `## Findings` list, add a plain-language block for each behaviour-change finding so the user knows what would actually shift:

```markdown
## Behaviour changes — your call

[2] `path/to/file.ts:88`: right now this swallows database errors and returns null. Removing the try/catch means callers see the actual exception — almost certainly what you want, but it's a real behaviour shift, not a cleanup.
```

One short paragraph per behaviour-change finding. Numbered to match the findings list. Plain language, no jargon. Skip this section entirely if all findings are refactor-shaped.

### When the diff is clean

```markdown
# Audit: <short scope description>

**Files:** <n> · **Findings:** none

No changes needed. <One short sentence noting what was checked.>
```

No approval gate. No further prompting. End of turn.

### How to tag the shape

- **`refactor`** — the fix produces identical behaviour for every input the code already handles. Examples: delete dead code, inline a filler variable, remove a tautological comment, collapse a one-implementation factory, rename a local variable. These are the targets listed in `kanso-refactor`.
- **`behaviour-change`** — the fix alters what the code does under some input. Examples: fix an off-by-one, remove defensive theatre that was swallowing errors, patch an auth bypass, change an architectural boundary. When in doubt, tag as `behaviour-change` — that forces an explicit ask rather than a silent refactor.

## The approval gate

If there is at least one Tier 1 or Tier 2 finding, always end the report with the approval gate. No exceptions — the gate is what makes `/kanso-audit` a single-command workflow rather than a report-and-wait. Emit exactly this block and stop:

```
Apply fixes? (<r> refactor, <b> behaviour-change)

  y                — run /kanso-refactor on the refactor findings
  y + behaviour    — run /kanso-refactor, then apply behaviour changes inline
  behaviour-only   — apply behaviour changes inline; skip refactor
  pick 1,3         — apply only those (routed by shape)
  edit             — amend the proposal
  n                — stop, leave the report in the transcript
```

Adapt the option list to what's actually present:

- All findings are refactor-shaped → show only `y`, `pick`, `edit`, `n`. `y` runs `/kanso-refactor`.
- All findings are behaviour-change → show `y` (apply inline), `pick`, `edit`, `n`. Drop the refactor option.
- Mixed → show the full list above.

Treat any affirmative phrasing that mentions behaviour ("y and apply the behaviour changes too", "yes do both", "all of it") as `y + behaviour`. Treat a bare `y` / "yes" / "go" as refactor-only when both shapes are present — do not silently apply behaviour changes on an ambiguous yes.

Routing rules on apply:

- Any selected `refactor`-shaped fix → invoke `/kanso-refactor audit-report` **inline in this chat**. Do not edit refactor targets directly from this skill. Do not dispatch the refactor via Agent/Task.
- Any selected `behaviour-change` fix → apply in the current chat, one at a time. Re-read the file immediately before editing.
- Do not mix the two in a single commit. `kanso-refactor`'s hard rule — refactors and behaviour changes travel in separate commits — applies here too.

### Test-first for correctness fixes

For any behaviour-change fix in the Correctness category — logic bugs, off-by-ones, security holes, race conditions, missing error handling — write a failing test before applying the fix when the repo has a test suite. The sequence is: reproduce the bug as a failing test, run it to confirm it fails for the expected reason, then apply the fix and re-run.

Skip the test-first step only when:

- The repo has no test suite, or none covering this module.
- The bug isn't testable in isolation — network races, timing-sensitive UI, environment-specific behaviour. Name the reason.
- The user has explicitly asked to skip it.

If you're skipping, say so in the apply step's output. Don't quietly drop the test.

This rule applies to Correctness only. Architecture and Clarity fixes don't require new tests — though running existing ones in Phase D still does.

## Phase D — Verify

After any fix lands, run the project's verification command and report the result. Never claim success without evidence.

Command discovery order and the pass/fail/no-command report blocks are defined once, in `kanso-refactor`'s Verify section (`../kanso-refactor/SKILL.md`). Follow them exactly. The non-negotiables:

- Pick the narrowest command that covers the touched files. For a correctness fix with a fresh failing test, run that test specifically, then a broader pass. Additionally, check CI config (`.github/workflows/*`, `.gitlab-ci.yml`) — if CI runs a verification job, run the same commands locally.
- Paste the exit code and the meaningful tail of output. Don't paraphrase.
- A failed verification means the fix isn't done. Roll back, iterate, or escalate to the user — don't move on, and don't hand over a broken tree.
- If no command exists, say so explicitly and list what was checked. Never silently skip.
- The command may prompt the user for permission on first run — that's expected. Don't reroute around it.

## Framing

- Critique the code, not the author. Use "this code" not "you".
- Every finding includes a recommendation. A finding without a path forward is an alarm, not a report.
- Offer alternatives on architecture disagreements rather than declaring a verdict.
- If a finding is for learning rather than blocking, mark it FYI.
- Don't flag preference-only issues as findings. A style preference that isn't in a style guide goes in "what's good" or nowhere.
- Don't repeat findings. One entry per pattern per location.

## What this skill never does

- Run via the Agent or Task tool, or dispatch any part of itself to a subagent or parallel runner — except Phase A under `--fresh`, which dispatches the investigation only.
- Edit files before the user has approved the proposal block.
- Skip the approval gate when there is at least one Tier 1 or Tier 2 finding. The gate is mandatory whenever there is something to fix.
- Prompt for approval when there is nothing to fix. The clean-diff message stands alone.
- Run tests or build the project during Phase A. Verification runs in Phase D, after fixes are applied.
- Claim a fix is complete without a Phase D result — pass, fail, or an explicit "no command found" note.
- Check out branches or pull remote changes.
- Flag things a linter already catches, without also noting the missing linter rule.
- Generate findings for padding. If there are three Tier 1 findings and nothing else, the report has three findings.
- Silently treat a bare "yes" as approval to apply behaviour changes. Behaviour changes need explicit opt-in.

## Failure modes to avoid

- Reviewing without reading the PR description, commit messages, or repo conventions. Context first, then findings.
- Flagging AI-sounding code that is fine. Not every verbose function is slop.
- Treating this as a style-guide compliance scan. The anti-dilution taxonomy is about harm, not taste.
- Producing a review so long the author skims it. Density matters more than coverage.
- Proposing fixes that introduce the same anti-dilution patterns the audit just flagged.
- Bundling unrelated fixes into one approval block so the user can't accept a subset. Group by shape, then by finding; let `pick` select.
- Editing a file without re-reading it first — state may have changed between the audit and approval.
- Applying a refactor-shaped fix directly instead of handing it to `/kanso-refactor`. That's duplication, and it bypasses the behaviour-preserving discipline that skill enforces.
- Mislabelling a behaviour change as a refactor to slip it past the gate. When in doubt, tag `behaviour-change`.
- Mixing refactors and behaviour changes in a single commit once fixes are applied.
