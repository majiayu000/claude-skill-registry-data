---
name: pr-ci-review
disable-model-invocation: true
# TODO(adapt): add Bash(<runner> *) entries for the LINT_CMD / TYPECHECK_CMD / TEST_CMD executables so the local pre-flight runs unprompted.
allowed-tools: Bash(git *), Bash(gh *), Read, Edit, Write, Grep, Glob, Agent
description: Cost-optimal multi-agent code review of local changes or a PR, across six relevance-gated, model-tiered areas, with a deterministic pre-flight and a record-all structured verdict CI renders to the PR in full.
argument-hint: "[pr [<number>]] [--fix]"
---

# Code Review Protocol

Provide a context-aware code review of local changes or a pull request, across six reviewer areas, and emit a structured record of everything it considered. You orchestrate: you steer, gate, consolidate, and act. You do NOT review code yourself; the area subagents do.

The governing rule is **spend only where it buys recall**. Deterministic tooling and the human in the loop are free, so lean on them first and spawn an agent only when judgment is the thing missing. Recall comes from the deterministic suite plus the correctness and security reviewers; almost everything else is a cut.

> **Setup:** the CI paths (`--json-schema`, the `review-metrics` record, the poster) are wired
> by [`claude-code-review.yml`](../../../.github/workflows/claude-code-review.yml): its
> preflight checks out the PR head and resolves the mode, it invokes `/pr-ci-review` with the
> PR named in prose plus a schema generated from [`tools/review`](../../../tools/review/), the
> poster script renders/posts the record, and each run's record lands on the
> `ci/review-metrics` orphan branch. Follow the setup comment at the top of that workflow to
> enable it; without it, the local `report` / `--fix` paths work unchanged.

## Review Constraints

- **Grounded, not speculative:** every finding is grounded in the actual changed code. No speculation; a false positive erodes trust.
- **Tag by severity, not by whether to post:** tag each finding `important` (fix before merge), `nit` (real but minor), or `pre-existing` (predates this diff).
- **Record-all, rank by display:** the structured record captures every confirmed finding plus the refuted ones, and CI renders all of it: `important` findings as inline comments on the diff, `nit`, `pre-existing`, and refuted findings in collapsed sections of the review body. You do not do the posting: the record is not a companion to the comments, it is what they are made from. A sub-important finding's `description` is therefore read by the author, not only the retro; write it as a self-contained one-liner.
- **Leave linters alone:** do not raise anything the project's formatter, linter, or typechecker (`FORMAT_FIX_CMD` / `LINT_CMD` / `TYPECHECK_CMD` in `.claude/project.env`) already catches; that is noise, not a finding.

## 1. Parse arguments -> source + action + mode

- **source = pr** when the invocation carries a `pr` token, a prose `Pull request: #N` reference, or a `--json-schema`. The CI harness invokes `/pr-ci-review` with the PR named in prose and a schema, so that path resolves here. `pr 123` or `#123` targets that PR; a bare `pr` targets the current branch's PR (`gh pr view`). A `--json-schema` makes **action = record**; otherwise **action = report**.
- **source = local** only when none of the above is present: the working tree is the subject. Default **action = report**; `--fix` -> **action = fix**.
- **mode**: a CI invocation carries a `Mode:` line and a `Merge base:` line, both resolved by the deterministic preflight step before you started; consume them, never re-derive them. `Mode: incremental from <sha> (prior record: records/<id>.json on origin/ci/review-metrics)` makes **mode = incremental** with that SHA as the delta base and that record as the prior review; `Mode: full` (or no Mode line) is a full review. Local runs are always **full**: a working tree has no prior record to diff against.
- Reject `--fix` with `pr`: state the error and stop. There is no local action that writes to a PR; a local `pr <n>` invocation without a schema reports in the session and posts nothing.

Define **the change** once and reuse it everywhere below:

- **local**: the working-tree diff against the merge-base with the trunk (`GIT_TRUNK` in `.claude/project.env`, default `main`): committed + staged + unstaged.
- **pr `<n>`**: the diff of PR #`<n>`; under **mode = incremental**, the delta `git diff <from_sha>..HEAD` instead, and every later stage (steering, area gating, instance scaling, briefs, validation) keys off that delta unchanged.

## 2. Gate the run before spending anything

- **Under CI (a schema was requested):** the preflight step already asserted the working tree is the PR's clean current head, resolved the merge base, and decided the mode; had any of that failed, you would not be running. Two gates remain yours:
  - **The config-restore set.** After the preflight and before you started, the CI action replaced `.claude/`, `.mcp.json`, `.claude.json`, `.gitmodules`, `.ripgreprc`, `CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` and `.husky` with the base branch's copies, because the head's versions are config the CLI executes at startup. A PR touching any of them therefore shows dirty exactly there; never `git checkout --` those paths (that re-arms the injection the restore disarms). Read the PR's own copies from `.claude-pr/<path>`, which the action preserves unexecuted; commit-to-commit diffs (`gh pr diff`, `git diff <merge_base>..HEAD`) show those files' real changes either way.
  - **The second freshness assertion.** Once the reviewers return, before you consolidate, compare `git rev-parse HEAD` to `gh pr view <n> --json headRefOid -q .headRefOid`: a push landing mid-review leaves the checkout behind the head, and a finding raised against text the true head already fixed is a false positive you shipped. If it moved, re-check each finding against `gh pr diff` rather than discarding the run.
- **Local pr source:** assert the working tree is the PR's current head (`git rev-parse HEAD` equals the PR's `headRefOid`) and clean (`git status --porcelain` empty); re-checkout with `gh pr checkout <n>`, or stop and say so. A stale or dirty tree makes `Read` serve content that disagrees with `gh pr diff`, so reviewers cite code that is not in the PR.
- **Pre-flight (local source):** run the project's lint, typecheck, and test commands (`LINT_CMD` / `TYPECHECK_CMD` / `TEST_CMD` in `.claude/project.env`) **scoped to the affected packages or modules** where the runner supports it (the full suite is slow). An empty key means that check is off; skip it. If it fails, **stop**: report the failures and ask the user to return once the tree is green. Reviewers assume the deterministic layer is clean; spawning them on a red tree pays opus to rediscover what tooling already flagged. Integration tests are infra-gated and stay CI's job.

## 3. Steer (yourself, no agent)

Gate and brief on the change's *shape* and *intent*, both free to read. Do not spawn a helper for this.

- **Shape**: the changed files, their line counts, and the top-level areas they span (packages, services, or source roots), from `git diff --stat` against the merge-base (local) or `gh pr diff <n>` plus `gh pr view <n> --json files` (pr).
- **Intent**: read it from the commit messages and, for a PR, the title and body. The author already wrote the intent; do not pay an agent to re-derive it from the diff. Only if the messages are junk (`wip`, `fix`) do you skim the diff yourself.
- **Steering brief** (pr): the unresolved comment threads (each with its concern) and what the author declared intentional or out-of-scope.
- **Prior importants** (mode = incremental): read the prior record the Mode line names (`git show origin/ci/review-metrics:records/<id>.json`). Its `important` findings were posted and their threads belong to the respond stage. For each, check its flagged location in the current head and mark it `resolved` or `unresolved` for the record's `prior_importants`; never re-post or re-raise one, and brief reviewers not to either: they are steering context, like unresolved threads.

Do not discover `CLAUDE.md` files: there is one (root, importing `AGENTS.md`), always in context, and per-area `docs/conventions/*` rules auto-load via `.claude/rules` when a reviewer reads a file in that area.

## 4. Gate which reviewers to spawn

Spawn a reviewer (via the **Agent** tool, by its `subagent_type`) **only when its area is actually touched**. An untouched area is the cheapest cut there is. The roster is fixed:

| Reviewer (`subagent_type`) | Default model | Spawn when |
| :--- | :--- | :--- |
| `review-correctness` | opus | code with real logic changed; owns behavioral regressions on the surface tests do not cover |
| `review-security` | opus | a trust boundary is touched (auth, routes, WS handlers, input handling, secrets, config) |
| `review-context` | sonnet | spec/protocol/infra surfaces touched (CORS, HTTP, docker, CI, settings) |
| `review-conventions` | sonnet | almost always: `docs/conventions/*`, `docs/adr/*`, and `CLAUDE.md` govern the rules |
| `review-maintainability` | sonnet | code with real logic changed |
| `review-docs` | sonnet | the change adds or edits prose (docstrings, comments, markdown, copy) |

There is no `requirements` reviewer: this setup deliberately keeps the issue tracker out of the review. If you skip a reviewer that might apply, note it in the final output so coverage is transparent.

**Model dials (asymmetric by stakes).** `correctness` and `security` always run on opus, never downgraded: a miss there is expensive. `maintainability` runs on sonnet for a normal diff and on **opus** once the diff is large (override the model at spawn time). `conventions` and `docs` run on sonnet.

**Instance scaling.** Default every area to **one** instance. Scale only `correctness` / `security` / `maintainability`, and only past a size gate: **> ~400 changed lines OR > ~8 files spanning >= 2 top-level areas** -> 2 instances; a markedly larger diff -> 3; **hard cap 3**. Send each instance in a complementary direction (by subsystem, layer, or risk concentration), never overlapping. Other areas stay single-instance. This is parallel breadth, not repeated passes: review the changed surface well once, do not loop.

## 5. Brief and spawn in parallel

Each subagent's manifest defines its expertise; your brief supplies everything else, in your own words. A good brief gives the reviewer:

- The change and the author's intent, plus the definition of **the change** so it can fetch its own scoped slice.
- Its assignment: the part of the change it owns, and, where you split an area, the specific direction.
- The steering context that concerns it: unresolved threads (do not re-raise their concerns; look harder where they point) and what the author declared intentional or out-of-scope.
- The contract every finding meets: `{file, line (or range), area, confidence (high/medium), tag, description}` with the quote or citation its focus requires. An `important` finding also carries `body`, the markdown the PR author reads (the concern, the rule or code it cites, a permalink), and optionally `suggestion`, replacement code for the flagged lines. A `suggestion` is only for a small self-contained fix that resolves the finding entirely; `null` otherwise. Below `important`, the `description` alone is what the author reads in the review body's collapsed sections, so it must stand on its own.
- An instruction to surface, separately, any impediment that degraded its review. No impediments is the normal case.
- **Under CI, the review is static**: test/build spikes, dependency installs, `git fetch`, and shell redirection to temp files are all off-limits; the Bash tool accepts `gh` and the read-only `git` verbs, nothing else. Hand the reviewer the two diff reads that work, so it does not spend calls discovering the ones that do not: `gh pr diff <n>` for the whole diff (authoritative, but it rejects a `-- <path>` filter and can exceed one read on a large PR), and `git diff <merge_base>..HEAD -- <path>` for a scoped slice, quoting the SHA from the invocation's `Merge base:` line. **Never `git diff origin/<trunk>...HEAD`**: the action shallow-fetches the base branch at depth 1 before the model starts, which grafts it parentless, so the three-dot form dies with `fatal: no merge base` as soon as the trunk moves past the PR. **Never `git diff HEAD~1 HEAD`** either: on a multi-commit PR it silently reviews only the last commit. Installed dependencies are only the review tooling's (the CI install is scoped to `tools/review`), so the project's dependency sources are **not** readable in-tree; a claim about a dependency's internals rests on pinned-version knowledge and caps at `medium` confidence. When the change touches the config paths the action restores (§2), tell the reviewer to `Read .claude-pr/<path>` for the PR's version: in-tree those files are the base branch's copies, so reading them serves content the PR does not contain. None of this is an impediment worth logging: it is the CI path's normal shape.
- A reminder that its final message *is* the deliverable for the next stage, not a human-facing report.

**Spawn together, then block.** Sending every instance at once is where the parallelism comes from, but the spawn is not the deliverable, the return is: wait on each one before you consolidate, and never end a turn with an agent still in flight. A turn that ends on an outstanding spawn lets the harness demand the structured output first, and what it gets is an empty record that reads as a clean review of a PR nobody reviewed. Blocking is about the turn, not about idling: when a reviewer returns while others are still out, apply §6's free checks to its `important` findings (tag-vs-body, provenance) and spawn their per-finding validators (§7) right away, so validation overlaps the slowest reviewer instead of queueing behind it. Cross-area dedup still waits for every return.

## 6. Consolidate (yourself, inline)

You hold every finding and have the only cross-area view, so dedup inline; do not spawn a separate consolidator.

- **Deduplicate across areas.** The same root issue often surfaces from several reviewers (a low-value comment trips `conventions`, `docs`, and `maintainability` at once). Merge into one finding, keeping the clearest description and the most severe tag.
- **Assign one area, citation-first.** A real defect is `correctness` or `security`. Anything citing a written `CLAUDE.md` / `docs/conventions` / ADR rule is `conventions`. Remaining judgment calls are `docs` or `maintainability`.
- **Respect declared scope.** Drop anything the author marked intentional or out-of-scope.
- **Doubt resolves to keep.** A verified mechanism with no currently-reachable trigger stays as a `nit`; only drop a finding whose mechanism is unproven.
- **The tag must match the body.** A finding whose own description concedes there is no reachable break ("no contract violation", "no practical consequence", a provably-equivalent behavior) consolidates as a `nit` regardless of the tag the reviewer chose. Do not forward a self-contradicting `important` to validation; the downgrade is yours to make.
- **Provenance-check "introduced by this PR" importants.** An `important` premised on the PR introducing the flagged code must survive a diff check: if the flagged line is not among the diff's added lines (a byte-identical move, an arrangement that predates the PR), retag it `pre-existing` before validation. The diff is free to read; do not pay a validator to discover provenance.
- **Carry descriptions verbatim.** A finding's `description` is written once, by its reviewer. Paste it byte-identical into validator briefs and the final record; when a merge keeps the clearest of several descriptions, the surviving text is the one carried, not a fresh synthesis. Rewriting the same prose three times is output tokens (the run's wall clock and cost) spent on nothing, and restating findings from memory under context pressure is how line anchors get lost.

## 7. Validate importants only

Validation buys precision, never recall, and precision is only worth paying for where the machine is about to act loudly on the finding: an `important` becomes an inline comment on the author's diff, where a false positive is public and expensive. Sub-important findings render in collapsed sections and are never auto-fixed, so they enter the record exactly as their reviewer returned them, unvalidated; their reviewers self-validated, and the collapsed rendering is priced for that.

- **action = report**: spawn **no** validator. Every finding goes to a human who is the final judge.
- **action = fix**: validate the **`important`** findings only, before editing. `nit` findings are never auto-fixed.
- **action = record (CI)**: one `review-validator` per consolidated `important`, tiered (opus for `correctness`/`security` findings, sonnet for the rest), spawned as soon as that finding's reviewer returns (§5) so validation overlaps the slower reviewers. A confirmed finding (with any location correction) survives; a refuted one is dropped from the posting set and carried in `refuted_findings` with its refutation reason, which CI renders in a collapsed section so a wrongly-killed finding is still catchable by the author.

## 8. Act on the result

**report** (default): present each finding in the session: its tag, file and line, the issue and why it was flagged, a suggested fix. Important findings first. If empty, state which areas were reviewed and that nothing was found.

**fix** (local, `--fix`): apply each confirmed finding.

- **Scope discipline**: each fix targets only the flagged issue. Do not refactor adjacent code, touch unrelated docstrings, or remove ticket TODOs.
- **Post-verify**: after editing, re-run `TYPECHECK_CMD` and `TEST_CMD` (scoped to the affected area where the runner allows) to prove no regression was introduced. Report the result.
- Summarize what changed (file, line, fix). List anything you noticed but did not touch under "Tangential (not applied)" and ask before editing those.

**record** (pr, CI): **you post nothing.** You have no tool that can write to the PR, by design. The record you emit in §9 *is* the round's output: the poster script renders it, anchors each `important` to the diff, posts one review, and pins a review commit status to the head SHA. So a finding you leave out of the record never reaches the author, and there is no second channel through which you could rescue it.

What that means for the record you write:

- **`body` is the comment.** For every `important`, write the markdown the author reads: the concern, the rule or code it cites, and a permalink of the form `<https://github.com/OWNER/REPO/blob/FULL_SHA/path/to/file#L[start]-L[end]>` with the full git SHA. Leave it `null` on `nit` and `pre-existing`, whose collapsed rendering uses `description`. A `null` `body` on an `important` degrades to the one-line `description`, which is a worse comment than the one you owed the author.
- **Give `line` the finding's true location, not a reachable one.** Do not hunt for a nearby changed line to anchor to. The poster parses the diff hunks itself, pulls the comment to the nearest commentable line, and prefixes it with the true location; a file with no changed line at all goes into the review body rather than being dropped.
- **`suggestion` is committable code, so it must be exactly right.** Only for a small self-contained fix that resolves the finding entirely. The poster renders it as an inert fence rather than a committable block whenever it had to relocate the anchor, since applying it there would rewrite a line the finding never mentioned.
- **A round always ends with a review and a status on the PR**, including a round that reviewed nothing and a round that died: CI guarantees both from the record, or says the diff was never reviewed. What CI cannot say is anything you alone know, so a gate that stopped you, a denied command, or a dead reviewer belongs in `process_issues` (§9), which is the only route that information has out of the run.

Impediments surfaced by subagents never appear in the report, the fixes, or the record's findings.

## 9. Structured summary (when a schema is requested)

If the harness runs this skill with a `--json-schema`, your **final message** must be the object that schema validates, in addition to the actions above. Emit it only once every spawned agent has returned (§5): a record built mid-flight reports zero findings and is indistinguishable from a clean review. Report what the review actually did, not a target:

- `reviewers_spawned`: one entry per reviewer instance that ran, by area (an area repeats when several instances ran).
- `review_mode` and `incremental_from_sha`: echo what the invocation's `Mode:` line gave you (`full` with `null`, or `incremental` with the delta-base SHA).
- `prior_importants`: on an incremental run, the prior record's `important` findings, each `{file, line, status}` with `status` `resolved` or `unresolved` against the current head (§3); empty on a full run.
- `findings`: the confirmed findings, each `{file, line, area, confidence, tag, description, body, suggestion}`. `body` and `suggestion` are `null` on anything below `important`; see §8 for what they must contain above it.
- `refuted_findings`: the §7 refutations, `important` findings only, each with its `refutation`. These carry no `body` or `suggestion`: the poster renders them from `description` plus `refutation`.
- `process_issues`: anything that degraded the review itself, each `{component, description}`, where `component` is the stage (`orchestrator`, `validator`, an area, or `platform`). Empty when the run was clean. These never appear in the PR comments.

There is no `comments_posted` field to report: you do not post, so the count is the poster's to state.

## Todo List

- [ ] Parse arguments into source + action, and read the mode from the invocation's `Mode:` line; reject invalid combinations.
- [ ] Gate the run: config-restore awareness under CI, freshness for a local pr, pre-flight lint/typecheck/test suite for local source.
- [ ] Steer: read the change shape and intent yourself; on incremental, read the prior record's importants.
- [ ] Gate and spawn only the touched areas, tiered and instance-capped.
- [ ] Consolidate inline: dedup and assign one area citation-first.
- [ ] Validate importants only (none for report; before editing for fix; per-finding for record/CI).
- [ ] Re-assert the head SHA before consolidating.
- [ ] Act: report, fix (with post-verify), or record (write `body` and `suggestion` for every important; post nothing).
- [ ] Emit the structured summary when a schema is requested.
