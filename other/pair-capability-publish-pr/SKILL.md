---
name: pair-capability-publish-pr
description: "Publishes a completed story branch as a pull request: runs the quality gate, creates or updates ONE PR from the pr-template (conditional sections filled only when pertinent), copies the story's classification tags, marks it ready-for-review, updates the board state, then enters the PR state flow — registers the required `pair-review` check as pending (merge blocked from t0) and dispatches the review to a clean-context subagent. Standalone — driven by a handoff/checkpoint, not by /pair-process-implement having run in the same session. Composed by /process-implement's closing phase (Step 3.3); reused by hotfix and automation loops. Composes /pair-capability-verify-quality, /pair-capability-checkpoint, /pair-capability-write-issue."
version: 0.5.0
author: Foomakers
---

# /pair-capability-publish-pr — Publish a Story Branch as a PR

Take a completed story branch to a review-ready pull request in one standalone step: **gate → compose PR → propagate tags → ready-for-review → board state → review dispatch**. Reliable on a clean context (input is a handoff document, not session memory) and reusable outside `/pair-process-implement` — hotfix branches and automation loops (#212, G10) invoke it directly.

**One PR per story:** the story lands on ONE branch with ONE PR. If a PR already exists for the branch, this skill UPDATES it — it never opens a second PR for the same story.

**Never merges.** This skill stops at a PR under review. Merge is a separate, human-gated step (`/pair-process-review` / `/pair-process-implement` Phase 4).

**The review is never optional.** Every PR this skill publishes enters the [PR state flow](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md) as `to-be-reviewed` with the **required** `pair-review` check registered as pending (so the merge is blocked from t0), and the review itself is dispatched to a clean-context subagent (Phase 5). This skill never renders the verdict — it only guarantees a review is pending and mechanically enforced.

## Composed Skills

| Skill             | Type       | Required                                                                                          |
| ----------------- | ---------- | ------------------------------------------------------------------------------------------------- |
| `/pair-capability-verify-quality` | Capability | Yes — the pre-flight gate (Phase 1). A red gate HALTs before any PR is created or updated (AC5).   |
| `/pair-capability-checkpoint`     | Capability | Optional — `$mode=resume` to read the handoff when one exists; if not installed, gather state from branch + story. |
| `/pair-capability-write-issue`    | Capability | Optional — two distinct compositions in Phase 4: `$mode: comment` for the PR-URL back-link (step 5) and the default write mode for the board state (step 7). If not installed, warn and continue (back-link written directly per the PM tool's implementation guide, board step skipped). |

## Arguments

| Argument     | Required | Description                                                                                                       |
| ------------ | -------- | ---------------------------------------------------------------------------------------------------------------- |
| `$story`     | No       | Story ID. If omitted, resolved from the handoff, then from the branch name (`<branch-format>` → `#<id>`). Unresolvable ⇒ **HALT** (AC edge case). |
| `$handoff`   | No       | Path to a handoff/checkpoint document. Default: `.pair/working/checkpoints/<story-id>.md`. Missing ⇒ gather minimal state from branch + story, then proceed (business rule). |
| `$scope`     | No       | Forwarded to `/pair-capability-verify-quality` as its `$scope` (default `all`).                                                  |

## Adoption Inputs (read deterministically)

Two sibling sections cover git concerns and the split is deliberate: **`## Merge Strategy` owns how a PR ends** (merge method, commit format, branch cleanup, merge confirmation — read by the merge consumers too), **`## Git Workflow` owns where the code lives and where it starts** (`code-host`, `base-branch`). This skill is the one reader of both, because it spans start (base branch) and intended end (merge method).

- **[way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) → `## Merge Strategy`** — the same section the merge consumers read (`/pair-process-review` Phase 6): `Method` (`squash` | `merge` | `rebase`, **default `squash`**) and the `Commit format` ([commit template](../../../.pair/knowledge/guidelines/collaboration/templates/commit-template.md)). Recorded on the PR as the intended merge strategy; **squash happens at merge, never here** (AC2). `branch-format` (to parse the branch id) comes from the [branch template](../../../.pair/knowledge/guidelines/collaboration/templates/branch-template.md).
- **way-of-working.md → `## Git Workflow`** — `code-host` (the tool owning branches/PRs) and `base-branch` (default `main`; **a `base-branch` declared under `## Merge Strategy`, where this skill's ≤ 0.4.1 versions documented it, is still honored** — the resolution order is single-sourced in the convention's **`base-branch` resolution** — the same order `/pair-process-implement` applies, so the two readers cannot disagree on the target branch). **`code-host` absent ⇒ code host = PM tool** (single-tool; the zero-configuration default, not a degradation), and the same tool named in both places is treated exactly as omitted. Resolution, the PM↔code-host routing table, and the cross-linking convention live in one place: [way-of-working / PM-tool + code-host resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md) — this skill states only which side each operation is on.
- **way-of-working.md → `## State Mapping`** — board-column ↔ canonical-macrostate mapping (see [canonical-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/canonical-states.md)). Omitted ⇒ canonical names assumed.

## Algorithm

Each phase follows the **check → skip → act → verify** pattern. Phases run in order; a HALT stops the skill without side effects.

### Phase 0: Resolve Story & Handoff (BLOCKING)

1. **Check**: Is `$story` provided or already loaded in this session?
2. **Act**: If not, resolve in order:
   - From `$handoff` (or the default checkpoint path) via `/pair-capability-checkpoint $mode=resume` when installed — this yields story, branch, tasks done, decisions with zero prior context.
   - Else from the current branch name, parsing `#<id>` per the `branch-format`.
3. **Verify**: Story ID resolved AND the branch is known. If the story id cannot be resolved from handoff or branch → **HALT**: "Cannot resolve story id — pass `$story` explicitly." (edge case).
4. **Act**: If no handoff document exists, gather minimal state directly: branch (`git branch --show-current`), commits since base, and the story's ACs/tags from the PM tool. Note in the output that no handoff was found.

### Phase 1: Quality Gate (BLOCKING — AC5)

1. **Act**: Compose `/pair-capability-verify-quality` with `$scope` (default `all`). This is a local pre-flight, not a replacement for CI (CI stays authoritative, #210).
2. **Check**: Did every required gate pass?
3. **Skip**: If all gates pass, proceed to Phase 2.
4. **Act**: If any required gate fails → **HALT** before creating or updating the PR (AC5). Report each failing check (gate name + first failing detail). No PR side effects occur on a red gate.

### Phase 2: Resolve Merge Strategy & Prepare Base (AC2)

1. **Act**: Read **both** git-concerned sections (Adoption Inputs) — `## Merge Strategy` (how the PR ends) and `## Git Workflow` (where the code lives and where the branch starts). Resolve, with defaults for anything omitted:
   - `Method` (default `squash`) — the intended merge method (`squash` | `merge` | `rebase`), recorded on the PR/output. **Applied at merge, not here** — this skill never rewrites branch history.
   - `Commit format` — the commit-message convention (informational; commits already exist on the branch).
   - `base-branch` — the PR target branch, resolved by the convention's **`base-branch` resolution** order (`## Git Workflow` → legacy `## Merge Strategy` → default `main`), which lives there rather than here because `/pair-process-implement` reads the same key: an adoption that declared e.g. `base-branch: develop` under `## Merge Strategy` (where this skill's ≤ 0.4.1 versions documented it) keeps targeting `develop`, and both skills agree on it.
   - `branch-format` (default `feature/#<id>-<slug>`, per the branch template) — used only to parse/validate the branch, never to rename it.
2. **Act**: Ensure the branch is pushed to the code host (`git push -u <remote> <branch>`); if already up to date, skip.
3. **Verify**: The resolved base branch exists on the remote and the feature branch is pushed. Example: `Method: squash` (the default) ⇒ the output marks squash-on-merge (AC2).

### Phase 3: Compose the PR Body (AC3)

1. **Act**: Read the [pr-template](../../../.pair/knowledge/guidelines/collaboration/templates/pr-template.md) (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md); the same resolution applies to the commit and branch templates referenced above). Fill the always-applicable sections from the handoff/story:
   - **Title**: `[#<story-id>] <type>: <brief description>` (`<type>` from commit-format / story type).
   - **Summary** (What Changed + Why) from the story statement and the handoff's decisions.
   - **Story Context**: link the story issue and list AC coverage.
   - **Changes Made**: tasks completed + files added/modified/deleted (from `git diff --name-only <base-branch>...HEAD`).
   - **Testing**: quality-gate results from Phase 1.
2. **Act — conditional sections (fill ONLY when pertinent; never leave an empty section):**
   - **`Refs:` (PR Information)**: the template's cross-link slot. Fill it with the PM tool's item id verbatim ONLY when `code-host` differs from `pm-tool` (Phase 4 step 4); omit the line entirely on a single-tool project. Filling the slot rather than appending free text is what makes `/pair-process-review`'s and `/pair-next`'s read-back deterministic.
   - **Services to Release**: from `git diff --name-only <base-branch>...HEAD`, group changed files by owning package/service and keep only **deployable** ones. Detect deployable via the adoption's deployable-package globs when declared, else a path heuristic (e.g. `apps/*`, deployable `packages/*`) — exclude content/docs-only packages (e.g. `packages/knowledge-hub`, `apps/website` content). Include the section only if one or more deployable packages/services are touched; list each once. Omit when nothing deployable changed.
   - **Screenshots** (before/after): include ONLY when the diff touches UI. Detect UI via the adoption's UI package globs when declared, else a path heuristic (e.g. `apps/*/`, `*.tsx|*.css|*.svelte`, `**/components/**`). When touched but no screenshot is available, include the section with a `TODO: attach before/after` marker rather than fabricating content.
3. **Act**: Omit every template section that does not apply (no placeholder-only sections).
4. **Verify**: The body follows the template, has no empty/placeholder sections, and every included conditional section is genuinely pertinent (AC3).

### Phase 4: Create/Update PR, Propagate Tags, Ready-for-Review, Board State (AC1, AC4)

1. **Check**: Does a PR already exist for this branch on the code host?
2. **Act — create or update (one PR per story):**
   - **No PR** → create it targeting `base-branch` on the code host.
   - **PR exists** → update its body and tags in place (edge case) — never open a second PR.
3. **Act — sync Deploy Notes to the linked PM item (T-2, TT-388, AC2):** parse the **Deploy Config Declaration** section of the composed PR body (Phase 3) — the five fields defined in the pr-template (resolve override-first — [template resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/template-resolution.md); the KB default is [here](../../../.pair/knowledge/guidelines/collaboration/templates/pr-template.md), an adoption override at `.pair/adoption/tech/templates/pr-template.md` wins).

   **Section boundary (both sides — PR body and PM item).** Match the heading by its **text**, at any level (`## Deploy Config Declaration` and `### Deploy Config Declaration` are the same section — the template nests it under `## Deployment Information`, but a composed body may promote it). The section runs from its heading to **the first subsequent heading of equal or higher level**, or end of body — never "to the next `##`" regardless of the matched level, which on a template-composed body would swallow the sibling `### Rollback Plan` and everything up to the next `##`.

   **Parsing a field.** Bullets opening with `_Esempio:_` (or the template's guidance prose) are **template scaffolding, never a declaration**: discard them before evaluating the field. A field is **at default** when, after that discard, it holds nothing but `Nessuna`/`Nessuno`. Without this rule an author who fills one field and leaves the other four untouched syncs the template's own examples as if they were real — a fictional migration and a fictional secret name propagated to the item and then aggregated into the release notes, which is the exact failure this story exists to prevent.

   **Upsert or delete — the sync is a mirror of what THIS PR declares:**
   - **Section present and at least one field non-default** → render a `## Deploy Notes` block (the same five fields, copied verbatim — never re-validated for secret values, that responsibility stays with the PR author) with a `_Fonte: PR #<n>_` provenance line, then **replace** the existing `## Deploy Notes` section in place if one is present **and its `_Fonte:_` names this same PR**, else **insert** it (position: immediately after the item's last existing top-level section, i.e. appended at the end of the body — deterministic, and it never lands inside another section). An existing block whose `_Fonte:_` names a **different** PR is left untouched: report `foreign provenance — PR #<m>` and do not overwrite it.
   - **Section absent, or every field reads its default** (no deploy impact) → **remove** an existing `## Deploy Notes` block **only when its `_Fonte:_` names this same PR** — the sync deletes what the sync wrote, never more. Skipping the delete entirely is what leaves a **stale** declaration on the item after a fix-loop reverts one (Step 6.2 of `/learnn-prepare-release` would aggregate a config that no longer exists); deleting **unconditionally** is worse, because it silently erases a block written by another PR on the same item (a hotfix, a follow-up, a revert) or one the release owner wrote by hand. A block with foreign or missing provenance is therefore **kept**, and reported as `stale block kept — foreign provenance PR #<m>` / `no provenance line`.

   Every other section of the item body is left byte-identical in all cases. Prefer the PM tool's section-level patch capability when available (e.g. Linear `save_issue $patch`, matching the exact heading text as the anchor); when the PM tool has none, fall back to a full read-compute-write of the body (compute the new full text locally, preserving every section except the replaced/inserted/removed one, then write it back) — never `/pair-capability-write-issue`'s default write mode, which renders from the story template and would discard sections it doesn't know about (AC/DoD/Task Breakdown). This is the **same sync-step** `/pair-process-review` calls when the section changes after PR creation (its Step 1.2b) — one algorithm, two call sites, never duplicated logic. If the PM item cannot be read/written, warn and continue — the PR itself is not blocked (edge case).
4. **Act — tag propagation (copy, not analysis):** copy the story's estimated **classification tags** (e.g. risk/size labels) to the PR verbatim. This is a copy — the authoritative re-classification happens in review (G6). If the story carries **no classification tags**, create the PR without tags and note it in the output (projection may be inactive, D17) (edge case).
5. **Act — code-host routing (AC4):** the PR is created/updated on the **code host**, the board state (step 8) is written on the **PM tool** — per the [routing table](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md). When `code-host` is absent (or names the PM tool) both resolve to the same tool and the split is invisible. When they differ, fill the pr-template's conditional `Refs: <issue-id>` slot (Phase 3 step 2) — the PM tool's own item id, copied verbatim.
6. **Check — does a back-link apply at all?** Resolve `code host` vs `pm-tool` **before touching the PM item**: the same tool (or an alias of it — identifier equality) ⇒ **skip this entire step here and now**, report `n-a (single tool)`, and go to step 7. The host already links PR and item natively, so there is nothing to post *and nothing to look for*. Gating at the head of the step rather than inside its Act is deliberate: on the default single-tool configuration this step performs **no PM-item read at all**, so publishing stays byte-identical to the pre-`code-host` behavior (AC1).
   **Check (split active) — back-link already present?** Read the PM item's existing comments (link field where the tool has one instead) and look for one containing this PR's URL.
   **Skip**: found → the back-link is already there; report it as `already linked` and do **not** post again. This is what keeps the step idempotent: a comment has no id, so `/pair-capability-write-issue` comment mode cannot dedupe it (see its Step 7c) — the check belongs here, or the normal fix→re-publish loop and any code-host HALT recovery would accrete one `PR: <url>` comment per round. If the item's comments cannot be read, treat it as *not found* and post (a duplicate comment is a lesser failure than a missing back-link) — say so in the report.
   **Act — post the back-link (bidirectional cross-link):** post the PR **URL back on the PM item** as a *comment* — never a body write. This closes the loop the `Refs:` line opens, so the board reaches the PR without any native integration. On `filesystem` the item **is** a file and its "comments" are dated bullets under `## Activity Log`, so both the check above and this write mean that one section of the item file ([filesystem-implementation.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/filesystem-implementation.md#comments-on-an-item-activity-log)). Two mechanisms, in order:
   - **`/pair-capability-write-issue` installed** → compose it in **comment mode**, which is non-destructive by contract (no template, no body render, no board write):

     ```text
     /pair-capability-write-issue $mode: comment $id: <issue-id> $comment: "PR: <pr-url>"
     ```

   - **not installed** → write the comment directly through the PM tool's implementation guide (e.g. Linear `commentCreate`, `gh issue comment`, the Azure DevOps work-item comments endpoint, the Jira comment API).

   Never compose `/pair-capability-write-issue` in write mode for the back-link: write mode is a **full-body overwrite** and would replace the story's AC/DoD/task breakdown with the link. If the **item id is not found**, or the PM tool errors, keep the PR (it is valid work) and warn with the manual-link instruction (edge case) — comment mode warns rather than HALTing for exactly this reason, so the documented non-blocking behavior holds through the composition.
7. **Act — ready-for-review:** mark the PR ready for review (not draft) on the code host; if the host supports an explicit ready command (e.g. `gh pr ready`), use it.
8. **Act — board state:** update the story's board state on the **PM tool** via the `## State Mapping` (canonical target: `Review`), using `/pair-capability-write-issue` (default write mode, `$status: Review`) when installed. If `/pair-capability-write-issue` is not installed or the PM tool is inaccessible, warn and continue — the PR is already ready. PR state itself is never mirrored onto the board.
9. **Verify**: A single ready-for-review PR exists on the code host, tags reflect the story (or their absence is noted), the Deploy Notes sync reflects the current PR body (or its absence/failure is reported), the cross-link exists in both directions when the tools differ — **exactly one** back-link comment, whether this run posted it or found it (or the missing back-link is reported) — and the board state is updated (or the failure is reported).

### Phase 5: Enter the PR State Flow & Dispatch the Review (AC1)

The PR is ready; it must now be **under review and mechanically blocked** — see the [PR state flow](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md) for the state model, the required checks, and the host mechanics ([github-implementation.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/github-implementation.md) § PR state flow).

1. **Check**: Does the current head commit already carry a `pair-review` check (from an earlier run on the same head)?
2. **Skip**: If a `pair-review` check already exists on this head **and** a review has been submitted for it, do nothing here — the PR is already in the flow (idempotency). A new head commit always needs a fresh check + review.
3. **Act — register the check as pending, when enforcement is on**: read `Review enforcement` from [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — **`disabled` is the default**. Enabled: publish `pair-review` on the head commit with a pending status **before** dispatching the review, using the mechanism the host's implementation guide prescribes for an ordinary (non-App) agent token — on GitHub a **commit status**, not a check run. That is what blocks the merge from t0: a crashed or never-started review leaves the required check unsatisfied instead of leaving the PR mergeable. Disabled: publish nothing here and say so — `pair-review: advisory (Review enforcement disabled)` — then dispatch the review exactly as before. The review still runs and still reports; what it cannot do is block, and claiming otherwise would be the one failure mode worse than not enforcing at all. If the publication is **refused** (missing token scope, no status API), do not claim enforcement: report `pair-review: NOT PUBLISHED — advisory` and continue (degradation below).
4. **Act — label the state**: apply `pr-state:to-be-reviewed`, removing any other `pr-state:*` label (exactly one at a time). The label family is provisioned once per repository (implementation guide) and does **not** auto-create; if the label is absent or the label API is unavailable, report it and continue — **non-blocking** (degradation below). The label is a **view** — the required checks are the authority (pr-states.md).
5. **Act — hand the review dispatch to whoever can actually spawn it (AC1)**: the review must run on a **clean context** — an **anonymous** subagent whose prompt is the PR reference only, no context from this session (mechanical isolation, D23: the reviewing context must not inherit the authoring context). **Who spawns it depends on where this skill is running**, because harnesses commonly forbid **nested** subagent dispatch — and this skill is itself frequently running *inside* a subagent (`/pair-process-implement` Step 3.3 publishes the PR from a handoff-only subagent), where spawning a second level would fail on the primary path:
   - **This skill is running inside a subagent** (or nested dispatch is unavailable/refused) → do **not** attempt to nest. Emit the signal **`Review: review-dispatch-required — /pair-process-review $pr=<number>`** and return it to the caller; **the caller dispatches** (for `/pair-process-implement`, Step 3.3 in the top-level session — the actor is named there). The `pair-review` check is already `pending`, so the merge stays blocked until the review lands: nothing is lost, and the dispatch happens one frame up where it is allowed.
   - **This skill is running at the top level** (invoked directly in a session that can spawn subagents) → spawn the anonymous review subagent here, now.
6. **The dispatch prompt** (identical for either actor) is the PR reference plus a **bounded** instruction — the review must not merge:

   ```text
   Run /pair-process-review $pr=<number> $dispatched=true.
   Phases 1–5 only: produce the verdict, publish the `pair-review` check, synthesize the PR state.
   NEVER run Phase 6 and NEVER merge, even if the verdict is APPROVED and every gate is green —
   the merge is a human act (pr-states.md). Stop after Phase 5 and report.
   ```

   `/pair-process-review`'s own non-interactive contract (its Arguments section) already forbids Phase 6 and defines what to do at its two human prompts (Step 1.4 "Proceed with review?" → continue without asking; Step 5.5 "Merge now?" → always "the author merges"), so a dispatched review neither stalls on an unanswerable question nor self-answers itself into a merge. The prompt states it too: belt and braces, since the constraint is an authorization boundary.

7. **Act — degraded path (no dispatch anywhere)**: if neither this skill nor its caller can spawn a subagent, do **not** run the review inline in this session (a self-context review defeats the isolation). Leave `pair-review` pending, note `Review: pending — dispatch unavailable, run /pair-process-review <pr> in a fresh session` in the output, and post the same instruction as a PR comment. The merge stays blocked meanwhile, so nothing is lost — only deferred.
8. **Act — dispatch failure**: if the subagent fails or times out, the pending `pair-review` check stays in place (merge blocked) and the re-run guidance is posted as a PR comment. Re-invoking this skill re-dispatches (idempotent).
9. **Verify**: The PR carries a `pair-review` check on its head commit, exactly one `pr-state:*` label, and either a dispatched/submitted review or a recorded reason why it is still pending (`review-dispatch-required` counts as recorded **only** because the caller's contract picks it up — see Composition Interface). This skill never publishes a verdict itself and never merges.

## Output Format

```text
PUBLISH-PR REPORT:
├── Story:      [#ID: Title]
├── Handoff:    [.pair/working/checkpoints/<id>.md | none — state gathered from branch+story]
├── Gate:       [PASS | HALTED — N gates failing]
├── Base:       [base-branch — squash on merge: yes|no]
├── PR:         [#PR-number — URL — Created | Updated]
├── Deploy Notes: [synced — PR #<n> | no deploy impact — nothing to sync | no deploy impact — stale block removed | stale block kept — foreign provenance PR #<m> | sync failed — <reason>]
├── Tags:       [copied: label, label | none on story — PR created without tags]
├── Code host:  [same as PM tool | <host> (board updates → PM tool)]
├── Cross-link: [n-a (single tool) | Refs: <issue-id> + PR URL posted on <item> | already linked — comment present, not re-posted | back-link failed — manual link needed]
├── Conditional: [Services to Release: N deployable packages / n-a | Screenshots: UI touched / n-a]
├── Board:      [→ Review | not updated — reason]
├── PR state:   [pr-state:to-be-reviewed]
└── Review:     [dispatched — subagent (clean context) | review-dispatch-required — /pair-process-review $pr=<n> (caller dispatches) | pending — dispatch unavailable, run /pair-process-review <pr> | already submitted on this head]

RESULT: [PR UNDER REVIEW — merge blocked by required check `pair-review` | HALTED — <reason>]
```

## Composition Interface

When composed by `/pair-process-implement`'s closing phase (Step 3.3):

- **Input**: `/pair-process-implement` invokes `/pair-capability-publish-pr` after the last task's commit, passing `$story` (and, when it wrote one, the checkpoint as `$handoff`). `/pair-process-implement` owns task iteration; `/pair-capability-publish-pr` owns the gate→PR→board sequence.
- **Output**: The PR number/URL and board-state result flow back to `/pair-process-implement`'s Phase 3 output. A HALTed gate propagates as `/pair-process-implement`'s HALT.
- **Review-dispatch contract (AC1)**: `/pair-process-implement` publishes the PR from a **handoff-only subagent**, so this skill's Phase 5 runs one level down and must not nest a second subagent. It therefore returns **`Review: review-dispatch-required — /pair-process-review $pr=<n>`**, and `/pair-process-implement` Step 3.3 — running in the **top-level** session — spawns the anonymous review subagent with the bounded prompt (phases 1–5, never Phase 6/merge). The `pair-review` check is already `pending` before the return, so the merge is blocked across the handoff. When this skill runs at the top level instead, it dispatches itself and returns `Review: dispatched`.

When invoked **independently** (hotfix, automation loop #212):

- Standalone: no dependency on `/pair-process-implement` having run in the same session. Resolve state from `$handoff`/branch/story (Phase 0), then run the full sequence.

## HALT Conditions

- **Story id unresolvable** from handoff or branch (Phase 0).
- **Quality gate red** (Phase 1) — report failing checks; no PR side effects (AC5).
- **pr-template not found** (Phase 3) — cannot compose a PR without it.
- **Code host unreachable or unauthenticated** for create/update (Phase 4) — report with a setup pointer and stop; nothing partial is left ready. **PM-side work already done is not rolled back** (the board write is the PM tool's own state); re-invocation is idempotent and resumes at the code-host step.

On HALT: report the blocker, propose resolution, make no PR side effects.

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline/template missing → minimal structure; PM tool inaccessible → do the PR, warn on the board step) for the standard scenarios. Additional cases:

- **No `## Merge Strategy` section**: default to `squash` + the commit template, base `main` — the zero-configuration default, not a degradation (AC2). Consistent with the merge consumers, which also default to `squash`.
- **No `code-host` declared**: code host = PM tool (single-tool) — the zero-configuration default, not a degradation; the cross-link step is skipped entirely.
- **Back-link cannot be written** (item id not found, PM tool error, no comment mechanism, or `/pair-capability-write-issue` unavailable and no guide command): keep the PR, warn with the manual-link instruction; the `Refs:` line in the body still links PR → item. This is a warning by design, never a HALT.
- **No classification tags on the story**: create the PR without tags and note it (edge case) — never invent tags.
- **Deploy Config Declaration section absent from the PR body** (pre-`pr-template` override adoption, or the author removed it): treat as all-defaults — remove a stale `## Deploy Notes` block from the item if one exists **and carries this PR's provenance**, report `no deploy impact — stale block removed` (or `stale block kept — foreign provenance PR #<m>`), never fabricate a section.
- **PM item unreadable/unwritable for the Deploy Notes sync** (Phase 4 step 3): warn and continue — the PR is still published; the sync is retried on the next re-invocation (idempotent, matches an existing PR body).
- **`/pair-capability-checkpoint` not installed**: gather state from branch + story directly (Phase 0).
- **`/pair-capability-write-issue` not installed**: skip the board-state update, warn, leave the PR ready.
- **Nested subagent dispatch unavailable** (Phase 5 — the common case: this skill is itself running in `/pair-process-implement`'s handoff subagent and the harness forbids a second level): return `Review: review-dispatch-required — /pair-process-review $pr=<n>` and let the **caller** dispatch (`/pair-process-implement` Step 3.3). This is the primary path when nested, not a degradation — the review still runs, one frame up, on a clean context.
- **Subagent spawning unavailable anywhere** (Phase 5 — the caller cannot spawn either, or this skill was invoked at top level in an environment without subagents): leave `pair-review` pending, post the re-run instruction as a PR comment, and note the deferral in the output. Never run the review inline in the authoring session (isolation, D23) and never mark the PR reviewed. Merge stays blocked — the outcome is deferred, not skipped.
- **Code host has no check-run/required-check API** (Phase 5): publish the state as a `pr-state:*` label only, note `enforcement: advisory — see host manual setup` in the output, and continue. Documented degradation, never a silent claim of enforcement (pr-states.md).
- **`pair-review` publication refused** (Phase 5 — token without the status scope, host API rejects it): the check is not published, so enforcement is **advisory**; report `pair-review: NOT PUBLISHED — advisory` (with the host error) and still dispatch the review. Never report a blocked merge that is not blocked.
- **`pr-state:*` label absent / no label API** (Phase 5): report `pr-state label: not applied` and continue — **non-blocking**, the required checks remain the merge authority. The labels are provisioned once per repository (host implementation guide); never invent a different label name.
- **`/pair-process-review` not installed**: still register the pending `pair-review` check and label the state, then report that no reviewer flow is available. The PR stays blocked rather than silently mergeable.

## Notes

- This skill **creates git-host artifacts** (a pushed branch, one PR, a pending `pair-review` check, a `pr-state:*` label), updates board state, and upserts the `## Deploy Notes` section of the linked PM item from the PR's Deploy Config Declaration (T-2, TT-388) — it does not modify source files, never renders a review verdict, and never merges.
- **Gate ≠ review** ([pr-states.md](../../../.pair/knowledge/guidelines/collaboration/project-management-tool/pr-states.md)): the Phase 1 gate is mechanical; the judgment verdict belongs to `/pair-process-review`, dispatched here on a clean context and enforced by the required `pair-review` check (R5.7).
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md). Re-invocation detects the existing PR and updates it in place; re-runs the gate (fast if already green); re-parses the handoff. Never a duplicate PR. The Deploy Notes sync is itself an upsert-or-delete — a re-invocation with an unchanged section is a no-op write, never a second `## Deploy Notes` block.
- **The `## Deploy Notes` block is not durable against a full-body item write.** Any skill that renders the item body from the story template with `$content` (`/pair-process-refine-story`, `/pair-process-plan-tasks` via `/pair-capability-write-issue`'s write mode) drops sections the template does not know about — this one included. Accepted: the sync re-writes the block on the next `/pair-capability-publish-pr` or `/pair-process-review` run, and a story is not normally re-refined after its PR is open. If a refinement does land mid-review, re-run either call site to restore the block.
- Tag propagation is a **copy**; the authoritative classification is (re)done in `/pair-process-review` (G6).
- The gate here is a local pre-flight only — CI remains authoritative (#210).
- The handoff/checkpoint is the input contract (see the [checkpoint template](../../../.pair/knowledge/guidelines/collaboration/templates/checkpoint-template.md)); it is consumed here, never loaded as ambient context elsewhere.
