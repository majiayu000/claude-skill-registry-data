---
name: pr-review
description: "Write a formal PR or release-promotion review with verified findings, standards citations, JSON and Markdown artifacts. Use for PR reviews and re-reviews."
---

Read the project AGENTS.md and applicable global guidance first. If AGENTS.md is absent, read CLAUDE.md as migration fallback. Discover optional skills before invoking them. If `using-chrisbanes-skills`, `android-cli`, or an official Android skill is unavailable, use the bundled android-standards references and current official documentation. Do not invent commands or claim that an absent skill ran. Use installed Android SDK tools when the optional Android CLI is missing. Commit and push only when the user has requested that action.

# Formal PR review

## What this produces

Two artifacts, side by side: **`findings.json`**, the canonical, machine-readable output
(schema in [`references/output.md`](references/output.md)), and the markdown review document
**rendered from it**. Names: `pr-review-<source>-to-<target>-YYYY-MM-DD.{json,md}` (promotion) or
`pr-review-<branch-or-PR#>-YYYY-MM-DD.{json,md}` (feature PR), at the repo root (local mode) or
the artifact staging directory (CI mode). The document contains:

- a verdict (any Blocker or unanswered Question ⇒ **Request changes**),
- an **At a glance** table with one row per finding, its severity and status markers and a link
  to the finding, so a reader sees the state of the PR without reading on,
- a **Scope of this approval** statement, the boundary that stops a review of one delta from
  reading as sign-off of everything beneath it,
- one section per finding graded **B**locker / **Q**uestion / **M**ajor (nits stay table rows).
  Each section carries the PR comment in a fenced block that can be copied and pasted into the
  PR as it is, written concisely for a senior developer (protocol.md §5), then the evidence
  anchored at its root cause (§17) and the observable check that proves it fixed (§18),
- *(promotion mode)* **manifest verification**: merge-base, release list, dependencies, tickets,
- *(conditional)* a cross-reference to the project's standing quality register, and a cross-repo
  twins table when a paired repo was reviewed for the same change,
- a mandatory **Good in this delta** section,
- an appendix ranking the `file:line` clusters a human reviewer should read first, and
- an appendix giving the **Standards basis**, the published guidance each finding cites.

The layout is the same for every destination. The document reads as plain Markdown on GitHub,
Azure DevOps or disk, and `scripts/render_confluence.py` turns the same file into a Confluence
page with status lozenges and collapsed evidence. A destination changes where the review goes,
never what it says.

In local mode nothing is posted, committed, or sent unless the user asks. When they ask, Phase 7
posts through one of the routes in [`references/posting.md`](references/posting.md). In CI mode the
pipeline posts `findings.json` to the PR via `scripts/post_review.py`, on Azure DevOps or GitHub
([`references/ci.md`](references/ci.md)).

## Modes: local and CI

**Local mode** (the default, an interactive session) behaves as the phases below describe: infer,
echo the profile back, ask what stays ambiguous, ask the re-review framing, echo the grades.

**CI mode**, active when `PR_REVIEW_MODE=ci` is set in the environment or the invocation says
so, is headless. It must **never ask anything**. Every ask resolves to its safe default (protocol.md
§24): ambiguous promotion detection ⇒ feature mode, re-review framing ⇒ addendum + thread
updates, severity echo ⇒ skipped, and missing register/ticket-key/paired-repo ⇒ skip silently. Source
and target come from the pipeline's PR variables. Every inference made is recorded in the JSON's
scope block so the pipeline log is auditable.

## Before starting

Read **[`references/protocol.md`](references/protocol.md)**, which holds the rules of engagement (§1 to §12),
the grading rules every platform shares (§13 to §16), and their extensions (§17 to §24: root cause,
verification criteria, SHA ancestry, debug variants, the adversarial pass, retractions, severity
negotiation, CI conduct). Also read **[`references/template.md`](references/template.md)**, the section
contract, plus **[`references/output.md`](references/output.md)** for the JSON schema. Load
exactly one platform pack in Phase 2, chosen by what Phase 0 detects:
[`references/platforms/android.md`](references/platforms/android.md),
[`references/platforms/ios.md`](references/platforms/ios.md),
[`references/platforms/spring-boot.md`](references/platforms/spring-boot.md),
[`references/platforms/react-nextjs.md`](references/platforms/react-nextjs.md), or
[`references/platforms/generic.md`](references/platforms/generic.md). In a polyglot repo, load
the pack that matches the files the delta touches.

Two non-negotiables shape everything else:

1. **Delta-only.** Review `MERGE_BASE..SOURCE_HEAD` and nothing older. Pre-existing debt belongs in
   the project's register (or nowhere), not in a review of someone's PR. Every approval carries the
   written scope statement.
2. **Personal verification.** Subagent findings are leads. Re-verify every B/Q/M yourself against
   the pinned SHA before it ships. Agents have cited evidence that did not exist (protocol.md §6).

## Phase 0: Setup, repo profile, mode

`git fetch` first, then establish the profile below. **Infer what you can, ask only what stays
ambiguous, and echo the profile back before proceeding** so a wrong inference is cheap to correct.

| What | How to infer it | If it stays unclear |
|---|---|---|
| Platform | first match wins: `com.android.application`/`com.android.library` in a Gradle build ⇒ Android · `.xcworkspace`/`.xcodeproj`/`Package.swift` ⇒ iOS · `org.springframework.boot` in a Gradle or Maven build ⇒ Spring Boot · `next` or `react` in a `package.json` dependency list ⇒ React/Next.js · otherwise the generic pack | ask |
| Source & target | the user's ask, the PR, or the current branch vs its upstream | ask |
| Environment branches | intersect the remote branch list with the candidate vocabulary in protocol.md §9, and treat region/brand/tenant-suffixed variants as their base environment | ask before asserting promotion mode |
| Ticket key | the most frequent `[A-Z][A-Z0-9]+-\d+` prefix across recent commit subjects | skip ticket reconciliation |
| Quality register | glob for `assessment/**/*.csv`, `audit/**/*.csv`, `**/recommended-tasks.csv`, or an obvious findings table in `docs/` | skip that section and say so |
| Reviewing team / org | the git remote's organisation | ask, or omit attribution |
| PR host | `SYSTEM_COLLECTIONURI` or `TF_BUILD` ⇒ Azure DevOps · `GITHUB_ACTIONS` ⇒ GitHub · otherwise the `origin` URL: `dev.azure.com` or `visualstudio.com` ⇒ Azure DevOps, `github.com` ⇒ GitHub. Record it as `scope.host` | ask before posting |
| Paired repo | only when the user names one, or an obvious sibling checkout exists next to this one | skip the twins section silently |
| Destinations | the PR host above is always one. A document destination comes from the user's ask: a Confluence URL, space or page named ⇒ Confluence. Otherwise the file at the repo root is the only document. Record them as `scope.destinations` | local mode: ask once whether the document should also go to Confluence. CI mode: never ask, file only |

Then:

1. **Mode:** first, local vs CI. `PR_REVIEW_MODE=ci` (or a stated headless invocation) ⇒ CI
   conduct throughout (protocol.md §24): no questions, defaults everywhere, inferences recorded in
   the JSON scope block. Then promotion vs feature. Both endpoints environment branches ⇒
   **promotion mode** (Phase 1 runs, full scoping statement). Anything else, or ambiguous in CI
   mode, ⇒ **feature mode** (skip Phase 1, simple scope line).
2. **Pin `SOURCE_HEAD`**, compute `MERGE_BASE`, and capture delta stats
   (`git diff --shortstat MERGE_BASE..SOURCE_HEAD`, commit and file counts). If a ref name doesn't
   resolve, resolve it by raw SHA and record that (protocol.md §8).
3. **Churn classification:** if much of the delta is mechanical (formatter sweeps, regenerated
   files), quantify it now with `git diff -w`. Mechanical churn raises the evidence bar for every later claim
   (protocol.md §7).
4. **Re-review check:** a prior deliverable for this PR already exists (glob `pr-review-*.md`
   at the repo root, or, in CI, a prior `findings.json`
   artifact or threads carrying a `pr-review` footer marker on the PR) and the head has moved ⇒
   go to Phase R.
5. If the working tree is dirty with changes you didn't make, note it and work from `origin/` refs.

## Phase 1: Promotion manifest verification *(promotion mode only)*

Verify, in order (template.md for the output shape):

- `MERGE_BASE == TARGET_HEAD`: the source strictly contains the target, so nothing on the target
  is lost and the PR diff is exactly what lands. Divergence here is itself a headline finding.
- First-parent merge history vs the release list in the PR description, mergebacks verified
  content-empty against their first parent, and the count of commits pushed directly to the source branch.
- Third-party dependency additions and version changes. Check the manifests *and* lockfiles for
  the stack in play (Gradle files and version catalogs, `Package.swift`/`Package.resolved`,
  `package-lock.json`, `go.sum`, `Gemfile.lock`, and so on).
- Ticket reconciliation against the detected ticket key: unique references vs the count claimed.
  Name example unticketed or mislabeled commits by SHA.

## Phase 2: Area fan-out

Launch parallel review subagents over `MERGE_BASE..SOURCE_HEAD`, scaled to the delta: a large
release promotion warrants the full lens set, while a handful of files may need one agent or none
(review it inline). **The lens list is a floor, not a ceiling**. When the delta contains
something no default lens owns (a build-system rewrite, a migration, a vendored dependency), add
a lens for it rather than letting the nearest lens half-cover it. Default lenses, adapted to what
the change actually touches:

1. **Data boundary**: services, DTOs, repositories, wire-contract changes, error handling, caches.
2. **State and control flow**: state ownership, persisted flags, navigation/routing, resume paths.
3. **UI and shared components**. A defect in a shared component is app-wide by definition, so
   weight it accordingly. Grade UI against the tiered design rules ([UI-STANDARDS]), citing the rule ID and source key. T1 breaches grade Blocker or Major by user impact. T2 breaches grade Nit unless the project opts the rule in.
4. **Security, privacy and logging**: secrets, PII placement, authorisation, injection surfaces.
5. **Accessibility, tests and CI**: semantics and labels, test quality, pipeline integrity. A test
   step that cannot fail is a Blocker: it falsely certifies everything else.

Run every lens agent on the reviewer-tier model (`gpt-6-astra` at high reasoning effort), as the toolkit's reviewer agents do. In CI mode no personal instructions choose it. Each agent's prompt must tell it to: read the loaded platform pack first, compare every claim
against the merge-base tree (`git show MERGE_BASE:path`) rather than just reading the new code,
obey the pragmatism guardrails (protocol.md §15), cite the standard per finding, identify the
**causal site** for each claim as distinct from its symptom sites (protocol.md §17), return
structured leads as `file:line (causal) · claim · merge-base behaviour · proposed severity ·
evidence quotes · symptom sites`, and close its report by **naming what it did NOT cover** as
explicit exclusions, so uncovered ground is visible instead of assumed reviewed. Give each agent a
budget of about 20 tool calls and tell it to stop and report when the budget runs out. A partial
report that marks unchecked ground Unverified beats none, and an agent with no budget can reach
its turn limit before it writes anything.

## Phase 2a: Adversarial verification (second opinion)

Before the lead touches the leads, send them to adversarial agents whose job is to **refute**
them (protocol.md §21). Run them on the reviewer-tier model too. Batch about eight leads per agent, with a budget of about 15 tool calls. Each agent checks per lead: cited
file/line exists at the pinned SHA, merge-base half is true (`git show MERGE_BASE:path`), anchored
at the root cause rather than a symptom (§17), and not debug-only (§20). Where a runnable command settles
it (a compile, a test, a grep), **run the command** in the scratch checkout described below,
because a compile beats reading. Verdicts:
**CONFIRMED / REFUTED (with counter-evidence) / WEAKENED**. Every agent's final line must assert
"N of N verified". A batch that can't is re-dispatched. Drop REFUTED leads from the table but keep
the refutations in the run's notes. Skip this phase only when the delta was reviewed inline with
no fan-out.

### Running a build or test

A build or test runs in a scratch checkout of `SOURCE_HEAD` that this session prepares, never in
the user's working tree:

1. `git worktree add --detach <scratchpad>/pr-<id> SOURCE_HEAD`.
2. Install dependencies there with the project's own command, such as `pod install`,
   `xcodebuild -resolvePackageDependencies` or `npm ci`.
3. Run the check yourself from the worktree. Hand a test run to `ios-verifier` only with absolute
   paths for `-workspace` or `-project`, `-derivedDataPath` and `-resultBundlePath`.
   `android-verifier` cannot address another checkout, so run Gradle yourself. The verifier
   agents may not run git or installers, so never ask one to prepare the checkout.
4. `git worktree remove <scratchpad>/pr-<id>` when the review is done. Record in the scope block
   which checks ran and which could not.

In CI mode the pipeline's checkout is already at `SOURCE_HEAD`, so skip steps 1 and 4.

## Phase 3: Personal verification

For every surviving B, Q and M lead: open the file at the pinned SHA, confirm the line numbers,
the mechanism, the causal site, and the merge-base half of the claim with your own commands.
The adversarial pass thins the leads, but it does not replace this gate (protocol.md §6). Demote or
drop whatever doesn't survive. In churn-heavy deltas re-verify "delta-added" with `git diff -w` or
a merge-base grep. **While verifying, write each finding's `verify_fixed_when` criterion**
(protocol.md §18). You just proved the defect exists, so state the observable that would prove it
gone: a command, a `file:line` expectation, or a named test. For a Q, state the answer or evidence that
closes it. Deduplicate across lenses, merge findings that share a fix, then assign IDs by severity
and discovery order. IDs stay stable forever after (protocol.md §10).

## Phase 3.5: Emit `findings.json`

Write the canonical output per [`references/output.md`](references/output.md): scope block
(including CI-mode inferences), verdict, manifest results, findings with all fields populated,
`genuinely_good` list, register cross-references. Everything downstream reads this file: the rendered document,
the CI poster, the next re-review. The document never carries a finding the
JSON lacks or vice versa.

## Phase 4: Register cross-reference *(when a register exists)*

For each register finding this delta touches, assign a verdict of **Worsens / Partially addressed /
Unchanged / Exposure widened / Mixed**, with an evidence pointer to a finding ID or `file:line`.
Untouched findings get no row. The framing sentence in the template covers them.

## Phase 5: Twin check *(when a paired repo was reviewed)*

Look for a review of the equivalent change at the paired repo's root (`pr-review-*.md`). If
found, mark shared defects in the Finding cells and emit the twins table so each gets one
coordinated fix. If not found, skip silently. Never characterise the other repo's status without
having looked.

## Phase 6: Render and deliver

Render the document **from `findings.json`** per `references/template.md`, sections in order.
Check before delivering:

- Verdict matches the register (any B or open Q ⇒ Request changes).
- Scope statement present and correct for the mode, and commit range and counts accurate.
- **JSON↔document parity**: every finding ID in the JSON appears in the document and vice versa,
  and in the At a glance table exactly once.
- Every PR-comment block equals the finding's `pr_comment` exactly and is self-contained (survives
  being pasted alone into the PR).
- Every B/Q/M has a `verify_fixed_when` criterion, and every finding names its causal site.
- Any commit cited passes the ancestry check (protocol.md §19).
- **Good in this delta** section present. Credit is what keeps the harsh register credible.
- Appendix A ranked by risk.
- Local mode: both files at the repo root with the mode-correct name, untracked. CI mode: both in
  the artifact staging directory, and the pipeline runs the poster (`references/ci.md`).

Then (local mode) tell the user the verdict, the blockers in one line each, the proposed grades
(protocol.md §23, severity is negotiable), and where the files are. Offer Phase 7 in one line.

## Phase 7: Post *(local mode, only when the user asks)*

Post through a route in [`references/posting.md`](references/posting.md). Before anything is sent,
confirm the PR head still equals `scope.source_head`, run a dry run and show the user the bodies.
Cast no vote unless the user asks for one, because the vote lands under their name. Blockers,
Questions and Majors get anchored threads. Nits go only in the summary comment, so they add no
thread the author must resolve.

When `scope.destinations` includes Confluence, publish the document with
`scripts/render_confluence.py` as [`references/posting.md`](references/posting.md) describes. A
republish first compares the live page with the version last published, because reviewers edit
these pages by hand.

## Phase R: Re-review (prior review exists, head moved)

1. Re-verify **every prior Blocker at the new head first**. The Blockers' status is the headline.
2. **Then every other open finding** against its `verify_fixed_when` criterion. Every status,
   `fixed | open | regressed | partial`, cites `file:line` evidence at the new head
   (protocol.md §10, §18).
3. Review only `OLD_HEAD..NEW_HEAD` (Phases 2 to 3.5 machinery, scaled down). Verify that claimed
   fixes actually fix, and that they don't regress a neighbouring path.
4. **Ask which framing** the user wants: an addendum (prior IDs untouched, new findings take the
   next free numbers) or a fresh rewrite at the new head with no re-review language. Both are
   legitimate. Don't guess (protocol.md §10). **CI mode never asks:** addendum, plus thread
   updates via the poster (resolved when criteria pass, reactivated on regression).
5. Update `findings.json` statuses and the scope statement's commit range to the new head either
   way. A finding that turns out to have been wrong is retracted visibly, never silently edited
   (protocol.md §22).
