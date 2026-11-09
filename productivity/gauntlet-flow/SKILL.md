---
name: gauntlet-flow
description: "Run an explicitly requested Hephaera Gauntlet as a persistent builder-versus-critic loop with progressive work-unit PRs into one integration branch. Use when a user says `gauntlet`, `gauntlet mode`, `gauntlet flow`, or a planning artifact declares `Flow: gauntlet` for an ambitious deliverable that can be inspected with concrete evidence."
engines: [AGNOSTIC]
---

## When to use

Use only for an explicit Gauntlet request. Ordinary assignments remain task mode, and ordered multi-task delivery remains goal mode.

Do not activate or create Gauntlet flow while repository-root `BRAINSTORM.md` is active. Brainstorm must be explicitly closed and converted into a plan first.

## Workflow

1. Create or import one parent task and GitHub issue through normal task flow, verify the issue URL is in its `TASK.md`, then create `.hephaera/.cache/gauntlets/<name>/GAUNTLET.md`; the Gauntlet scaffold requires that task to exist first.
2. Define the objective, inspectable artifact, constraints, quality bar, delivery base branch plus exact commit SHA, and `gauntlet/<name>` integration branch created exactly at that commit. If the lead proposes them, pause for approval. The first accepted opened event freezes the parent task, objective, constraints/permissions, base identity, static delivery policy, approved bar, and normalized unit manifest into separate execution-contract, quality, and unit-manifest fingerprints.
3. Decompose the deliverable into stable, independently judgeable work units with a durable ID, title, and inspectable scope/acceptance boundary. The normalized manifest contains sorted retained ID/title/scope definitions plus sorted supersession ID/scope/replacement edges; transient checkbox/status state is excluded. Approve it with `- Unit manifest approval: <fingerprint> | units: <comma-sorted-ids> | approved by: <identity> | approved at: <canonical-UTC>`. Retain every definition; additions, definition changes, or edge changes require an approved `Unit manifest revision`, changed title/scope additionally requires a matching `Unit scope-title revision`, and splits/merges require canonical supersession markers. Every per-unit checkpoint, PR event, and round must use a unit and title/scope definition present in the manifest generation active at that timestamp. Never erase failed work. The supersession graph must be acyclic, terminate only at active leaves, and transfer every outstanding unit-local, integration, or promotion failure root to every active descendant.
4. Keep coupled work under one sequential owner. Use project-manager subagent lanes only for units with disjoint write sets.
5. Create `gauntlet/<name>` exactly at the approved base commit. Builders work only on `gauntlet-work/<name>/<item-id>[-remediation-N]`; this separate namespace avoids Git's ref-prefix conflict. The integration branch advances only through recorded human-merged PR edges, never direct writes.
6. For each unit, let a builder record the actual strategy for the attempt, change the real artifact, and run objective verification. Run `pr-readiness-check.sh --gauntlet-progress`; it verifies the fetch and every effective push identity, local/remote integration tip, work branch, frozen fingerprints, remediation cause, and that the work head descends from the exact integration-chain tip, then writes an immutable publication checkpoint. Accept only authenticated SSH or HTTPS `github.com` remotes, never plaintext HTTP, and pin live GitHub API evidence queries to `github.com` rather than an ambient `GH_HOST`. Verify the checkpoint's manifest fingerprint plus exact `Unit manifest approved at` value, quality fingerprint plus exact `Quality bar approved at` value, and every relied-on supersession edge were approved and active at its issuance time. Push/open only the exact emitted branch and SHA into the emitted target, use case-sensitive `Refs #<parent-issue>` as the exact first body line, and include the emitted `<!-- hephaera-gauntlet-publication:v1 checkpoint=<path> checkpoint-sha256=<sha> -->` marker. Record `opened`; the recorder re-queries the same-repository PR and consumes that current checkpoint exactly once. Each later head on the same open PR must fast-forward from its prior recorded head. Readiness authorizes publication but never opens or merges the PR itself.
7. Start a separate critic with no inherited builder turns when the host supports it; otherwise use a new isolated session. Give it only the objective, current work-unit ID and frozen scope, approved bar, constraints, exact PR-head SHA, and artifact/verifier evidence. Do not provide the builder's history, justification, or prior PR comments.
8. Require the exact critic-report template below. Builder and critic identity sets must remain globally disjoint, and every critic invocation ID must be new. Record the immutable round with the matching head SHA, actual builder strategy, opened-event path/hash, and resolved remediation-root path/hash; the recorder verifies each artifact as a regular file in that exact commit and re-queries the live PR. Post its evidence with the canonical semantic QA marker, then record the matching `qa-pass` or `qa-fail` using the exact `COMMENT_URL`; the event recorder independently rejects head drift, edits, reuse, and causal reassignment. Use Progress PR Ledger append order for same-second PR events; accept equal-time cross-ledger order only through an explicit immutable evidence edge.
9. On failure, keep the same progress PR open and route the largest gap to the builder. Do not start a new round until the prior round's QA failure is recorded. The next attempt must use a different actual builder strategy, produce a new head SHA, and use a new critic invocation. Keep builder strategy and prior comments out of the critic packet.
10. On pass, wait for a human to merge, fetch the integration ref, and promptly record the merge in target order. The recorder requires a live same-repository non-draft PR, reviewed `headRefOid`, observed `baseRefOid`, `mergedBy.is_bot=false`, created/closed/merge times, and `mergeCommit`; that edge must extend the frozen-base topology. Reject any progress or promotion PR whose retained timeline ever enabled auto-merge, auto-rebase, auto-squash, or merge-queue entry, even if later disabled. Terminal validation re-queries every topology or causal-replacement PR. A unit integrates only when critic, QA, unit-scope/manifest/quality/execution fingerprints, head, causal remediation, and merge-chain evidence agree.
11. After every active unit integrates, prove the exact local and remote integration refs equal the gapless merge-chain tip, descend from the frozen base, contain every latest unit merge, and have no unrecorded direct commit. Run a new critic on that SHA and aggregate scope. Rewinds, divergence, forks, origin drift, or chain gaps block the round. Integration fail/block records its exact then-active affected set. Every affected unit or active supersession descendant, and every named promotion-failure unit, requires its own later PR cycle hash-linked to that failure root.
12. After every active unit and the integration review pass, run ready validation and generate `GAUNTLET_REPORT.md` with `create-gauntlet-completion-report.sh --status complete`. The command creates the report and immutable completion event, then runs complete validation transactionally; complete validation is not a prerequisite for report generation. The event ledger binds a canonical projection of the whole report except its self-referential immutable-evidence section. Every older completion must be consumed exactly once by a later promotion failure; at most the newest may remain active. Stopped or blocked reports remain promotion-ineligible.
13. Run final local validation and `pr-readiness-check.sh --gauntlet`; readiness refuses remote/ref, contract, manifest, base ancestry, merge-chain, live terminal-PR, report-projection, source-ref, or GitHub-default-branch drift. Open the promotion PR only after approval, target the verified current default branch, and use case-sensitive `Closes #<parent-issue>` as the exact first body line; no progress or remediation PR may carry any closing-keyword alias. Its QA event binds the live target `baseRefOid` as a descendant of the frozen base. One later fail may supersede a prior pass for the same completion/PR/head; it archives the report, consumes that completion, and names affected units. A new pass then requires remediation, a new head, integration review, and completion event. Preserve historical event heads through immutable comments and fast-forward ancestry, but require the current live promotion PR to remain open, non-draft, and unmerged with its source head and the remote integration ref exactly equal to the reconstructed local merge-chain tip.

Use this exact active-unit line shape in `GAUNTLET.md`:

```markdown
- [ ] <item-id> | status: <pending|building|critic-failed|passed|blocked> | title: <single-line title> | scope: <single-line inspectable artifact and acceptance boundary>
```

Titles and scopes must be substantive and cannot contain `|`. A superseded unit keeps the same fields and uses `status: superseded`.

Its supersession marker must bind the pre-change 64-character lowercase scope fingerprint, name one or more existing active non-self replacement IDs in comma-sorted order, give a substantive single-line reason and approving identity, and use a canonical UTC timestamp at or after all retained evidence for that unit. No later round or PR evidence may be recorded for the superseded unit. Before treating an ancestor failure as applicable to a replacement, prove every supersession edge on that path was approved no later than the replacement cycle's publication checkpoint, which must precede its live GitHub creation time; never use a later approval to legitimize earlier work.

Use these exact manifest-history shapes:

```markdown
- Unit manifest approval: <64-character-lowercase-fingerprint> | units: <comma-sorted-ids> | approved by: <identity> | approved at: <canonical-UTC>
- Unit manifest revision: <kebab-id> | from: <old-manifest-fingerprint> | to: <new-manifest-fingerprint> | prior-units: <comma-sorted-ids> | current-units: <comma-sorted-ids> | reason: <substantive reason> | approved by: <identity> | approved at: <canonical-UTC>
- Unit scope-title revision: <item-id> | from: <old-unit-scope-fingerprint> | to: <new-unit-scope-fingerprint> | reason: <substantive reason> | approved by: <identity> | approved at: <canonical-UTC>
```

The prior unit set must be a subset of the current set. Unchanged exact unit scopes may retain evidence from an approved earlier manifest; new, changed, superseding, superseded, and causally affected units require fresh evidence.

## Critic context packet

Provide only:

- the frozen objective and approved quality bar
- the current work-unit ID and frozen unit scope, or complete-artifact scope for integration
- applicable constraints and guardrails
- the exact full PR-head SHA, or integration-branch SHA for integration review
- artifact paths, rendered output, tests, measurements, citations, or other direct evidence
- the exact report template below

For a native subagent, use the host's no-history/no-inherited-turn mechanism and provide only this packet. If that isolation is unavailable, use a fresh isolated session. If neither is possible, block the run rather than allow the builder to grade itself. A unique critic ID is evidence of invocation identity, not proof of isolation by itself.

## Critic report template

Use these headings once, in this order:

```markdown
## Artifact Inspected
- Head SHA: <full 40- or 64-character SHA supplied in the packet>
- Artifact: <project-relative regular file>

<What was directly inspected and how. Add more Artifact entries when needed.>

## Bar Comparison
<Criterion-by-criterion comparison with concrete evidence.>

## Guardrail Results
<Objective tests, safety constraints, regressions, and their results.>

## Verdict
- Verdict: <pass|fail|blocked>

## Largest Remaining Gap
<A concrete largest gap. For pass, explain why no material gap remains.>

## Next Strategy
<Concrete recommendation after fail/blocked. For pass, state what evidence should be preserved.>
```

The artifact path must resolve to a regular, non-symlink file in the exact reviewed Git commit. The report SHA must exactly match the `--head-sha` used to record the round.

## GitHub evidence sequence

Use the repository's GitHub tool priority. With `gh`, inspect the live PR using fields equivalent to:

```bash
gh pr view "<pr-url>" --json url,body,headRefName,headRefOid,baseRefName,baseRefOid,isCrossRepository,headRepository,state,isDraft,createdAt,closedAt,mergedAt,mergedBy,mergeCommit
```

The round and event recorders execute this live query themselves and fail closed if `gh` is unavailable or any observation differs. Before each QA verdict, post a new result with `comment-pr-qa-results.sh`; its exact comment must contain `<!-- hephaera-gauntlet-qa:v1 verdict=<pass|fail> head-sha=<sha> source=<canonical-evidence-path> source-sha256=<sha> affected-units=<none|comma-sorted-ids> -->`. Recorders reject arbitrary, edited, missing, wrong-PR, wrong-author, semantically stale, or reused comments. Before `merged`, fetch the integration branch and record merges promptly in target order. The event recorder persists and later replays the complete live identity, chronology, body/checkpoint, reviewed SHAs, fingerprints, actor, and topology. It verifies evidence but never grants merge permission.

## Resume a stopped or blocked run

Resume a stopped or blocked run only after explicit user direction and after the blocker or interruption condition is addressed. Preserve durable evidence and change only the execution state needed to resume; do not rewrite the approved bar, unit scope, rounds, PR events, or ledgers. If a live PR has a critic round, consume it with PR QA before recording `closed`; a PR closed before any round may be recorded directly. An integration `fail` immediately reopens affected units and keeps the Gauntlet running; an integration `blocked` verdict authorizes the same remediation only after explicit resume. A passed run is different: never edit it open manually. Record a live promotion-PR QA failure with `record-gauntlet-promotion-qa.sh`; that command archives the prior report and creates the immutable authorization for named affected units.

## Output

- `.hephaera/.cache/gauntlets/<name>/GAUNTLET.md`
- immutable `publication-checkpoints/<item-id>/checkpoint-NNN.md` progress-publication authorizations and their one-time PR-body bindings
- immutable `rounds/<item-id>/round-NNN.md` evidence
- immutable `pr-events/<item-id>/event-NNN.md` progress-PR evidence
- immutable `promotion-events/event-NNN.md` promotion-QA evidence and its ordered ledger
- immutable `completion-events/event-NNN.md` successful-completion evidence and its ordered ledger
- ordered progress PR, reviewed-head/base-SHA, frozen-contract/base, QA-comment, merge-chain, work-unit, and integration state
- `GAUNTLET_REPORT.md` with completion or incomplete status
- a human-gated promotion-PR readiness report when and only when the Gauntlet passes

## Guardrails

- Never activate Gauntlet mode implicitly.
- Never start building before the quality bar and delivery contract are approved.
- Never change the bar without new user approval; a change invalidates affected pass evidence.
- For an approved bar revision, retain prior rounds, add the revision to `Work Units / Unit History`, reopen every active unit, clear integration evidence, reset the current bar fingerprint to `pending`, and reset PR eligibility to `no`. The next accepted `opened` progress-PR event freezes the new fingerprint; no critic round may be recorded before that event.
- Never change an active unit's title or scope silently. If evidence exists, record/close any live PR first, add the revision to Unit History, reopen the unit as unchecked `critic-failed`, clear integration evidence and promotion eligibility, then change the scope and validate ready state. Treat all prior evidence for the old scope fingerprint as stale and use a new remediation PR.
- Never delete or rename a retained unit definition. Approve every normalized manifest revision and matching changed scope/title marker before new evidence; carry superseded ancestors' outstanding failures to every active descendant.
- Never let any builder identity act as any critic identity in the same Gauntlet, even with case changes, or reuse a critic invocation for another round.
- Never grade a builder-authored summary instead of the actual artifact or verifier output.
- Never accept critic, QA, or merge evidence after the PR head drifts from the recorded SHA. Require a new builder attempt and critic round.
- Never accept a syntactically plausible SHA or arbitrary evidence URL as proof. Require a real commit/ref, live same-repository GitHub observation, a current uniquely consumed publication checkpoint in the PR body, a new and uniquely consumed exact same-PR semantic QA comment for every verdict, and artifact files from the reviewed commit tree.
- Never enforce a critic recommendation as though it were the builder's changed strategy. Persist the actual builder strategy, and reject a repeated attempt after failure.
- Never invent PR events, head SHAs, QA comments, or merges to migrate an older Gauntlet. Archive the old run and start a progressive run, or explicitly supersede its units and rebuild them through real PR evidence.
- Never parallelize coupled work merely because capacity is available.
- Never create work branches beneath `gauntlet/<name>`; Git cannot store those child refs beside the integration ref. Use `gauntlet-work/<name>/...`. Never write directly to integration, count an unmerged PR as integrated, start dependent work from unmerged state, or accept a chain gap, unrecorded integration commit, rewind, divergence, base-ancestry loss, or repository-origin drift.
- Never bypass a Gauntlet lock, remove a lock without proving it stale, overwrite evidence, or manually reopen a completed run. An active unconsumed completion event forces passed/report/source state even if mutable fields are edited. Only a promotion-QA failure may consume it and authorize named remediation; every applicable failure must later be satisfied by its own causal merged PR chain. Approved quality-bar revisions retain their documented reset path before completion.
- Explicit Gauntlet approval authorizes automatic progress-PR publication only through the recorded integration target. It does not authorize merge approval, merge execution, auto-merge, or final promotion publication.
- Use case-sensitive `Refs #<parent-issue>` as the exact first body line of every progress and remediation PR. Reserve every supported closing-keyword form for the human-approved promotion PR, whose exact first line is `Closes #<parent-issue>` and whose target must be the current GitHub default branch.
- Limit each autonomous execution window to 45 minutes or two failed full-validation epochs, whichever occurs first. Count one epoch when one frozen candidate is evaluated against the approved verification suite; targeted diagnosis does not reset or enlarge the window. At exhaustion, do not begin another build, audit, or validation epoch. Record elapsed time and failed-epoch count in Review Notes, persist resumable state, generate a stopped report, set status to `stopped`, and request explicit user reauthorization. Reauthorization starts a new window. Safety, permission, platform-policy, and unrecoverable blockers still stop immediately; this does not authorize unapproved paid services or external actions.
- A stopped or blocked report is not completion evidence and is never promotion-PR eligible; any existing progress PRs remain historical evidence.
- Gauntlet promotion retains human PR readiness approval, and Gauntlet mode never authorizes merge, approval, or auto-merge.

## Commands

`bash ./commands/create-task-file.sh "<task-name>" ["Title"]`

`bash ./commands/import-task-from-issue.sh "<issue-ref>" ["task-name"]`

`./commands/create-gauntlet-file.sh "<name>" ["Title"] --task "<task-name>" [--dry-run]`

`./commands/validate-gauntlet.sh "<name|path>" [--phase ready|complete]`

`./commands/record-gauntlet-round.sh "<gauntlet>" "<item-id>" "<verdict>" "<builder-id>" "<critic-id>" "<native-subagent|fresh-session>" "<critic-report.md>" --head-sha "<sha>" --builder-strategy "<strategy>" [--dry-run]`

`./commands/record-gauntlet-pr-event.sh "<gauntlet>" "<item-id>" "<opened|qa-pass|qa-fail|merged|closed>" "<pr-url>" "<head-branch>" "<evidence-url|none>" --head-sha "<sha>" [--merge-commit "<sha>"] [--dry-run]`

`./commands/record-gauntlet-promotion-qa.sh "<gauntlet>" "<pass|fail>" "<promotion-pr-url>" "<evidence-url>" --head-sha "<sha>" [--affected-unit "<item-id>"]... [--dry-run]`

`bash ./commands/pr-readiness-check.sh --gauntlet-progress "<gauntlet>" "<item-id>" [validation_summary_file]`

`./commands/create-gauntlet-completion-report.sh "<gauntlet>" [--status complete|stopped|blocked] [--dry-run]`

`bash ./commands/pr-readiness-check.sh --gauntlet "<gauntlet>" [validation_summary_file]`

`bash ./commands/comment-pr-qa-results.sh "<pr-number-or-url>" "<results-summary-file>" --gauntlet-verdict "<pass|fail>" --head-sha "<sha>" --gauntlet-source "<project-relative-round-or-completion-event>" [--gauntlet-affected-units "<none|comma-sorted-ids>"] [artifact-url ...]`
