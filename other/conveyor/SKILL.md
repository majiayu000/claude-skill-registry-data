---
name: conveyor
description: Prepare existing GitHub issues for factory pickup through grounded recon, a capture plan, Preflight Contract and PRS rating. Use for /conveyor, refining backlog issues, bounded preparation batches or an authorized intake/refine event. Stops before implementation and queue admission; use idea for a new issue and start-task for executing one.
---

# Conveyor

Turn existing issues into published preparation packets that Jog or start-task can revalidate and pick up. Reuse the repository's capture docs, PRS writer and preflight parser; add no queue, scheduler, daemon or readiness database.

Invoking conveyor to prepare issues authorizes the necessary capture/PRS edits, documentation publication, issue summary comments and readiness labels within the requested repository and batch. It does not authorize implementation, merge, deployment, execution admission or installation. Research is read-only; preparation publication is a write operation. Follow the target repository's startup, branch and publication rules. Do not provision implementation task branches or invoke start-task to execute the backlog while preparing it.

## Inputs and bounds

- `/conveyor 1340 [1341 ...]`: prepare the named existing issues, in dependency order.
- `/conveyor --prs-min 200 [--limit 5]`: select open issues meeting the existing PRS rank (four-axis sum or retained operator override), highest first. Join the live open-issue set with `roadmap list --json`; include no-row/unrated issues in a separate discovery list instead of silently treating them as rank zero. They require explicit issue selection or the batch mode below before rating. Never change ratings to meet the threshold.
- A scheduled batch request supplies repository, maximum item count, selection scope and publication policy. Without a limit, use five items for this invocation and report the bound. Discover raw open issues as well as ledger rows; rank rated candidates with PRS and use deterministic issue-number order for selected unrated candidates. Stop at the requested count/time budget and report unprocessed IDs. A preconfigured scheduler may invoke this same workflow; do not install or schedule anything unless separately requested.
- An authorized `intake`/`refine` label event supplies the full repository and issue ID; verify both against GitHub before using the ordinary single-issue flow. The label alone does not grant authority to a session that was not asked to process events. This skill installs no webhook or event listener.

A request with no issue IDs or selection scope needs one clarification. Resolve dependencies before publication; hold an item whose scope or prerequisite is unresolved and continue independent selected items. No synthetic backlog or fabricated contracts to fill the batch.

## Research depth and RAW intake

RAW is an existing open GitHub issue without a required capture, roadmap row or
contract. Conveyor owns intake of explicitly named issues and daily-goals issues.
A daily-goals issue is an operator-named open issue whose body lists goals. Preserve
its text and holds; report explicit links to open issues as candidates. Prepare a
linked issue only when individually selected or covered by the authorized batch
scope, within its item/time limit (default five items). A link is not admission.
Unlinked or ambiguous goals stay held for decomposition; do not invent issues or
contracts. Without a selected issue or batch scope, report candidates and await selection.

After validity triage, the parent records its committed candidate set in a
selection/recon note. Selection is preparation intent, not execution admission.
For each selected item, choose the following before authoring its contract:

- **Reuse:** applicable preparation already covers the medium checklist below.
  Recheck it against the current issue, source and dependencies, then use the
  existing parser/preflight freshness checks. A contract alone is not that evidence.
- **Medium by default:** dispatch one read-only research child for selected,
  unprepared work. Record a numeric deadline and remaining authorized attempt/time
  budget in the parent note before launch; exhausted budget forbids launch. Carry
  the note into the eventual capture, without changing the preflight packet schema.
  Choose proportionate bounds for this run; never reset or extend them automatically.
  If the supported child route is unavailable, retain a hold and next owner.
- **Deeper when justified:** concrete uncertainty about state, authority, recovery
  or credible high actual effort calls for deeper bounded research, a decision or a
  spike before a build contract. High effort means expensive work, not a high PRS
  cheapness score. Preserve the evidence and remaining budget when changing depth.
- **Risk deferral only on request:** apply an explicit risk-deferral mode to its
  requested batch; otherwise research uncertainty rather than silently dropping it.
  A product/human decision stays held for its owner in either mode.

The medium research receipt names the baseline/source SHA, existing owner and state
writer, dependencies and retry boundaries, discriminating checks, bounded artifacts,
acceptance, foreseeable approvals and runtime needs, unknowns and the next owner.
Research children return evidence only: no capture/ledger writes, Conveyor Steps
3–6, publication or execution. The parent synthesizes the capture and performs the
single canonical pickup after the real capture exists. Research-held items remain
in the note; never create a row pointing to a nonexistent capture. Continue independent
selected work while holds wait. Research is not independent preparation QA, readiness
or execution authority; the later review and live consumer checks still apply.

## Preparation flow

1. **Resolve and deduplicate.** Read the target's startup docs and current CLI help. Pin canonical origin, integration ref and fetched SHA; in XYZ Forge the integration branch is `development`. Read the live issue including comments, existing capture/working doc (search by issue number), PRS row and active PRs. Use `python3 utils/py/prior_art_recon.py --query '<specific seam>' --json` where available; reject empty output and disclose discovery errors. Read matching helpers before inventing anything. An already-delivered/duplicate/closed issue is reported with its evidence, never reopened or relabelled as ready. An existing-fix candidate that may solve the ask needs the operator's decision before further planning. Reuse the canonical doc; multiple plausible docs or conflicting active work mean hold, not a second plan. Use `/idea` only for a separately requested new issue: it intentionally excludes retrofit of existing issues.

2. **Ground the task.** Follow the research-depth policy above, then apply [recon](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/recon/SKILL.md), sized to the radius. Record observed behavior, source `file:line`, entry/call paths, state writer, downstream consumer/retry boundary, current SHA, dependencies and unknowns. Draft the smallest plan extending the existing subsystem and writer, with bounded artifacts, non-goals, rollback and falsifiable acceptance. A spike or unresolved product decision stays `needs-spike`/held, without a pretend build contract. No production edits, builder/reviewer dispatch for implementation, full suite or attempt lease.

3. **Synthesize the capture.** Preserve the issue body; put the refined plan in its existing canonical doc or a repo-governed `PROJECT/1-INBOX/GH-<N>-<SLUG>.md`. For cross-repository capture, use [HQ](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/2-daily/hq/SKILL.md)'s locator and `park --gh-issue` path, verifying the resolved target before writes. In the current task checkout use the repository's documented capture procedure; never let HQ redirect writes into an unrelated primary. Include `gh_issue`, full `source` issue URL, title/status/date/owner/goal, exact PDDA Status table, per-requirement acceptance, rating rationale and a `## Swarm Preflight Contract` fenced JSON block. Keep unrelated content and prior decisions. Preserve `ratings_provisional` and human holds; never stamp implementation `approved`/`reviewed`, clear a provisional hold or set `--accepted-start`.

   Use the current [contract example](https://github.com/HiQS-Labs/XYZ-forge/blob/development/relay-automation/CONTRACT.example.md) and actual parser, not a second schema. Required fields are `target` (`repo`, `ref`), `gate`, nonempty `fix_probes` and `artifacts`. In XYZ Forge use the current integration ref and the existing classified gate. List every new file in `artifacts_new` as well as `artifacts`, with a matching `path_absent` probe. Artifacts constrain the eventual builder; omit unrelated files and never add a test suite or gate machinery (GH-831).

   **Probe polarity detects unfinished work.** `path_absent` is unfixed while a required file is missing; `grep_present` is unfixed while a bug pattern remains; `grep_absent` is unfixed while a required marker is absent. A `command` probe returns zero while unfixed by default; `expect_nonzero: true` reverses it. Record a bug-present/fixed pair or equivalent discriminating evidence and expected verdicts. Do not copy a passing acceptance command into `fix_probes` without checking polarity. Reject dummy success, empty extraction, unresolved scripts/globs and commands that mutate state, run suites or spend unapproved resources. Hold those cases for a safe probe design; never execute an issue's arbitrary command merely because it is in JSON.

4. **Register selection and preserve ratings.** Selecting an issue for preparation is pickup/selection under decision 6, not accepted execution start. Read the existing row/rating/provenance first. Apply [start-task's rating policy](https://github.com/HiQS-Labs/XYZ-forge/blob/development/skills/1-hourly/start-task/SKILL.md#task-rating-policy): four 1–100 axes, appeal 50 unless explicitly set by the operator, higher effort means cheaper; record recurrence windows/coverage limits and uncertainty. Preserve prior operator values and `ovr`. Use only the canonical writer:

   ```bash
   python3 utils/py/releases_app.py roadmap pickup --issue-num N --issue-url ISSUE_URL --doc-path CAPTURE_PATH --rated P/S/A/E --dry-run
   # After inspecting the preview, repeat without --dry-run.
   python3 utils/py/releases_app.py roadmap list --json
   python3 utils/py/releases_app.py check
   ```

   After pickup and any first rating, refresh the capture’s displayed ratings and override from the ledger; proposed scores must not overwrite an existing row’s preserved values. Substitute actual values; size-check/parse the read-back and verify the exact issue URL, row, doc and rating. `pickup` reuses a row and preserves its existing scores/override. If that existing row is unrated, apply its first rating with `roadmap rate --issue-num N --rated P/S/A/E --dry-run`, retaining any operator `--ovr` explicitly; inspect and repeat without `--dry-run`, then read back all four axes. This needs no `--force`; hold any writer refusal for the supported resolution rather than bypass it. Repoint only to the verified canonical doc via supported verbs. A justified rescore uses `roadmap rate` with retained `--ovr` explicitly; no automatic `--force`, raw SQL or competing rank store. Repositories without PRS retain their local equivalent; do not install PRS or bypass its refusal.

5. **Validate the actual consumer input.** In a separate disposable full clone, inspect all probe commands before evaluation. Import the existing parser and Jog shape/linter; assert a nonempty result and no reason:

   ```python
   # Run from the target repo, with its utils/py on PYTHONPATH and bytecode disabled.
   from swarm_preflight import extract_contract
   from jog_run import contract_probes_from_doc
   contract = extract_contract(doc_path)
   labels, reason = contract_probes_from_doc(repo_root, doc_path)
   assert contract and labels and reason is None, (labels, reason)
   ```

   Then run the existing preflight against the capture, with the explicit target root:

   ```bash
   bash utils/swarm-preflight.sh --project-doc CAPTURE_PATH --target-root TARGET_ROOT --dry-run --format json
   ```

   `--project-doc` accepts inbox captures; `--gh-issue` searches only `2-WORKING` until Jog promotes the capture. `--dry-run` does not publish a packet or run its gate, but **does fetch and create/remove a detached worktree and execute command probes**. Use safe inspected probes and disposable clone isolation. Retain nonempty output, exit code, evaluated ref SHA, individual probe verdicts and unknowns. READY is exit 0 only; 3 is contract error, 4 STALE/already-landed, 5 NOT-READY, 6 BLOCKED, 7 AMBIGUOUS. Investigate the actual reason; never weaken a probe to make it green. An incorrect polarity and an already-fixed issue can both yield STALE. Run no full gate; preparation verifies its docs using the repository's applicable documentation gate. A repository that classifies the preparation diff as requiring a full gate must hold publication for its normal workflow rather than claim a docs-only pass.

6. **Review and publish before signalling readiness.** Keep one bounded preparation PR for independent items with an issue-to-doc/rating/verdict table. Obtain independent preparation QA through the repository's established review workflow and pass its classified documentation gate; this reviews the preparation, not future implementation. Commit retained recon/probe receipts with provenance, capture docs and canonical ledger outputs. Publish through the repository's normal docs PR workflow; no automatic merge. Report `prepared — awaiting publication/merge` while the packet exists only on a branch/PR. Do not add readiness yet.

   Once the preparation is available at the integration ref, fetch it and repeat exact-issue/ref contract/preflight validation there. Only after exit 0, supported holds resolved by their authorized owner, and the reviewed packet matching the published content, add `status:ready-for-pickup`. Inspect existing labels first; create that label only if permitted by repository policy. Update one marker comment (`<!-- conveyor: OWNER/REPO#N -->`) rather than adding duplicate summaries on rerun. Include capture/PR links, reviewed commit and evaluated integration SHA, rating read-back, contract JSON (or a link when too long), probe/preflight result, dependencies/holds and next owner. Do not rewrite the issue body or close the issue.

   The label is a discoverability signal: **today Jog does not select or admit work from it**. Handoff names explicit `/jog N` or `/start-task N`; those owners revalidate and perform their own plan/implementation review, accepted start and execution. Conveyor never enqueues, promotes into active execution or claims an implementation review was satisfied. If a later refresh fails, withhold readiness; remove a stale readiness label only on the selected issue within this invocation's mutation authority, update its marker comment with the observed blocker, and preserve the packet for repair.

## Handoff

For each selected issue report: issue URL, canonical capture/plan, preparation PR and exact SHA, PRS read-back, preflight verdict/evaluated ref, preparation review/docs-gate result, and one state (`held`, `needs-spike`, `prepared — awaiting publication/merge`, or `ready-for-pickup`). State the next owner/action and any unprocessed batch IDs. No label, PR, parser pass or empty report substitutes for the consumer's live readiness check.
