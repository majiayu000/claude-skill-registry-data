---
name: ghi-close
persona: main-session
description: Use to do the work a GHI describes, verify it and close the issue with evidence in one sweep.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "2.12.1"
model: opus
---

# ghi-close

## Invocation

```
ghi-close <id>
```

`<id>` is the GitHub issue number (integer, no `#` prefix required — the
skill accepts either `192` or `#192`). Required. Refuse to proceed without
an ID — "close the last GHI" or "close the open one" is ambiguous at the
audit-trail layer and produces the batch-close anti-pattern this skill is
designed to prevent.

## Purpose

**Do the work in the GHI and close it.** GHIs exist to evaluate and resolve
issues — the terminal state of a well-formed GHI is *closed with evidence*,
not *analyzed and left open*. This skill is the end-to-end execution path:
read the GHI, execute the prescribed fix (routed per
AGENTS.md § Defect-fix routing), verify artifacts, close with a
citation comment.

The skill is not an evaluator-only surface. If it terminates without
closing, the reason is a concrete blocker the agent cannot remove
unilaterally — not a missing pre-existing commit. "No fix landed yet" is
not an exit condition; it is the *trigger* to author the fix.

### Bounded closure contract (GHI #980)

Before implementation, record the closure contract in the issue body or a
comment. Read the issue's Expected behavior and canonical intent first; the
contract makes them testable, never narrows them to what already passes.
Use these four fields, scaled to the finding:

| Field | Required content |
|---|---|
| Invariant | The required behavior and its authority; distinguish the requirement from a proposed implementation |
| Boundary | Relevant inputs, states, producers and consumers; explain the failure mechanism connecting them |
| Acceptance | State/input → required outcome → semantic evidence; include valid controls and directly coupled correctness surfaces |
| Exit | Evidence and required gates that permit the disposition; name unresolved dependencies separately |

For an investigation, record the question, bounded evidence population, and
deliverable instead of inventing a known cause or requiring a fix. An older
issue without these fields is completed by the executing agent during Read;
routine elaboration of settled intent needs no extra operator approval.

**Fix the class within this contract.** Shared filenames, conceptual similarity,
and the possibility of more tests do not alone make a finding part of the
repair. Expand when evidence identifies an omitted member of the same failure
mechanism, an unmet acceptance criterion, or a regression introduced by the
repair. Record the evidence and contract amendment before continuing; do not
silently shrink the claim or widen the work. A genuinely new policy choice or
live-brief conflict still follows the existing operator routing rules.

**Review the contract, not an unlimited neighborhood.** Each blocking review
finding names the violated criterion (or the canonical obligation omitted
from it), the counterexample or concrete evidence gap, and the smallest
relevant verification. A reproduction is preferred, but an identified untested
required state or contradictory data flow is sufficient to require a focused
check. "How about two more?" without such a link is not a blocking finding.
Track independent discoveries through `ghi-author` or `gz insights remember`;
do not automatically execute them or make them prerequisites for this close.
Required quality gates remain required, including failures discovered there.

**Finish and stop.** Before closing, independently assess whether the evidence
satisfies the contract: a reviewer reasons from the required outcomes, rather
than treating the implementation's tests or receipts as the specification.
Use an existing review stage or a focused review where appropriate; this adds
no OBPI ceremony or mandatory additional agent. Re-run verification when a
change, failure, or unresolved contract claim warrants it. Once the contract,
review, and required gates pass, close with that evidence and stop this work
order. Further investigation needs new evidence or another work order.

When the same GHI is reopened again after a corrective pass, reassess the
contract, shared validation authority, and fixture assumptions before another
local patch. The new counterexample becomes part of the acceptance matrix;
repeated reopening is a trigger to change method, never permission to waive
an unresolved defect or cap the number of necessary repairs.

This is agent-facing procedural guidance, not a runtime enforcement claim.
Scenario evaluations sample decisions; a filled table, green suite, or passing
sample cannot establish complete coverage by itself.

### Doctrine — NEVER, EVER, EVER dead-letter a GHI (binding, top-priority)

**A GHI is closed only when its scope has a real, citable landing site — a commit SHA, a registered ADR ID, a registered OBPI brief ID, or a higher-numbered GHI that absorbs the scope. "Go run /gz-design later" is NOT a landing site. "Operator should invoke X next" is NOT a landing site. "Re-route to design pipeline" without authoring the destination ADR in the same close action is NOT a landing site.**

This rule is the highest-priority constraint in this skill and overrides every other instinct toward graceful exit. The failure mode it closes — "dead-lettering" — is the pattern where the skill posts a thoughtful disposition comment, names where the work *should* go, closes the issue, and leaves the scope orphaned with no audit trail forward to anything that actually exists. The GHI's number disappears from the open list; the work disappears from every tracker; the operator discovers months later that the doctrine correction never landed because every surface assumed the next surface was carrying it.

**Dead-lettering is worse than leaving the GHI open.** An open GHI surfaces in triage, in session orientation, in `gh issue list`. A dead-lettered GHI is invisible — the close comment is searchable only if you already know to look for it. Open-with-blocker is the honest state when scope has no destination yet; closed-with-vague-redirect is the corrupted-audit-trail state.

**Operative rules:**

1. **`withdrawn` route correction requires the destination to exist before close.** If the GHI's prescribed work is genuinely new capability that should run through `gz-design` → `gz-plan` → `gz-obpi-specify`, then this skill's close action is to **author the feature or pool ADR (or invoke the design pipeline) in the same session**, register it, and close the GHI as `superseded` citing the new ADR ID. `withdrawn` is reserved for the genuinely-rare case where the GHI's premise has evaporated (rule changed mid-flight, defect was a misread of working-as-designed behavior) — not for "this should be an ADR but I haven't authored one."
2. **`superseded` requires a real, registered upstream.** A drafted but unregistered ADR file on disk is not enough. The upstream must appear in `gz adr status` / `gz state` output, or be a commit SHA, or be a higher-numbered GHI that exists. Vague references ("the eventual ADR for this") are dead-letter dressing.
3. **If you cannot complete the destination authoring in the current session, the GHI stays open with a blocker comment.** Name the blocker, name the next concrete operator action, leave the issue open. Open-with-blocker is the correct state; closed-with-route-promise is the failure.
4. **Operator-initiated close decisions still bind the destination rule.** Even if the operator says "close this and we'll handle it later," the skill's response is to surface that "later" needs a destination — author the ADR now, or leave the GHI open with the deferred-action comment. The skill does not execute "close it for now" as a valid request.

The two rules compose: do the work and close it; if the work routes elsewhere, create the elsewhere before closing. The GHI's terminal state is closed-with-real-evidence, never closed-with-aspirational-redirect.

### Doctrine — Routing fulfills a GHI's purpose (binding)

A GHI is **observation routing**, not implementation tracking. When a GHI's
finding has been homed in a registered destination — a commit SHA, a
foundation/feature ADR, a pool ADR visible in `uv run gz adr report`, an
OBPI brief, or a higher-numbered GHI that absorbs the scope — the GHI's
purpose is **fulfilled** and `superseded` is the correct disposition.
Implementation lifecycle thereafter belongs to the destination, not to
the GHI.

This rule is the dual of `ghi-author` § Doctrine — A GHI's purpose is
observation routing. The two skills together produce a single contract:
file → route → close. Routing-and-closing is the normal terminal state.
GHIs that wait around for the destination's implementation to ship are
shadow trackers — duplicate state of the same shape Layer-3 derived
views become when they silently mirror Layer-2 truth (per
`docs/governance/state-doctrine.md`).

**Operative consequences:**

1. **Pool ADRs count as registered destinations.** A pool ADR visible in
   `uv run gz adr report` (Pool table) is a valid `superseded` upstream.
   Pool status is the design-conversation home; promotion to foundation
   or feature is the destination's lifecycle, not the GHI's.
2. **An ADR or OBPI authored in the same session as the close is a valid
   destination.** When a GHI surfaces a finding whose right home is a
   new pool ADR (architectural absence) or a new OBPI (planned increment
   under an existing ADR), authoring the destination + closing the GHI
   `superseded` against it is one motion. This is *not* dead-lettering —
   the destination is a real, registered artifact at close time.
3. **Multiple GHIs may close `superseded` against one destination.** A
   symptom GHI, a class-of-failure GHI, and an architectural-absence
   GHI can all route to the same pool ADR — each is a different cut into
   the finding, and the ADR carries them collectively. Close each
   individually with its own routing-receipt comment; never batch-close.
4. **The destination must exist before close, not be promised.** This is
   the dead-letter prohibition reapplied: "the eventual ADR for this" is
   not a destination; "the ADR I just authored at
   `docs/design/adr/pool/ADR-pool.<slug>.md` and verified appears in
   `uv run gz adr report`" is.

This rule does not relax the dead-letter prohibition; it sharpens it.
Routing to a real destination is the closing motion. Routing to a
promised destination is the failure mode.

### Doctrine — defect remedies are direct fixes, NEVER new OBPIs

A GHI labeled `defect` (or any defect-shape `investigation` / `enhancement`)
resolves through `fix(<scope>): <summary> (GHI #N)` commits. **OBPIs are
the unit of planned feature increments authored under an active ADR. They
are not the closeout vehicle for surfaced defects.** This holds regardless
of which surface the fix touches — CLI verb, schema, runtime contract,
foundation rule, validator scope. Surface heat is a *routing fact* that
shapes the commit body and verification evidence, not a trigger to
ceremonialize a defect remedy as new feature work.

When the fix scope feels too large for a direct fix, the right move is
**operator escalation with routing facts** — diff estimate, surfaces
touched, precedent count from `git log --since='60 days ago' --oneline
--grep='^fix('`. The right move is **never** "author a new OBPI to make
the ceremony fit." Authoring an OBPI to close a defect inverts AGENTS.md
§ Defect-fix routing: it routes ceremony work back onto defect-fix where
direct-fix already provides the right audit trail (`fix(...)` trailer,
TDD evidence in commit body, ARB receipts cited inline).

If a GHI's prescribed work is genuinely *new capability* (not a remedy
for broken behavior), the GHI is mis-labeled. It is routed, not fixed:
author its destination in this session and close `superseded` against it,
or leave it open with a blocker comment (dead-letter doctrine, rule 1).
That, and a repair assignment the operator rules into the in-flight ADR
([`references/repair-assignment.md`](references/repair-assignment.md)), are the only paths from a GHI to planned work.

## Trigger

- Operator says "close GHI #N" / "resolve GHI #N" / invokes `/ghi-close <id>`
- Triage pass needs an open GHI driven to terminal state
- End-of-ADR closeout reviews the open-GHI list for that ADR
- A commit or PR already landed that claims to resolve the GHI (verification-only fast-path — still runs the full protocol)

## Behavior

Four-phase protocol: **read**, **execute**, **verify**, **close**.

| Phase | What happens |
|-------|--------------|
| Read | Load GHI; extract prescribed fix or fix options from the body |
| Execute | Apply the fix via the correct route per AGENTS.md § Defect-fix routing |
| Verify | Run the evidence block against the landed artifacts |
| Close | Emit the citation comment and `gh issue close` |

## Prerequisites

- `gh auth status` reports authenticated
- You have read the GHI body and any linked commits/PRs
- You have read the surfaces the GHI body names (the OBPI brief, ADR, rule, schema, or file the defect references)
- `git status` is clean or in a known state (so a new fix commit lands on a known tree)

## Steps

### Phase 1 — Read

1. **Load the GHI and its references.**

   ```bash
   gh issue view <N> --json number,title,body,state,labels,comments,url
   ```

1a. **Re-derive every stated precondition against the current tree before
   accepting it.** A blocker comment, a "sequence this after #M" note, or a
   "blocked on the in-flight OBPI-X" caveat is a **claim about the tree as it
   stood on the day it was written** — not a standing fact. Code moves; the
   comment does not. For each precondition the GHI records, read the surface it
   names and confirm it still holds, then say so in the close comment with the
   file:line you checked.

   Observed instance (GHI #677, 2026-07-21): the blocker said *"sequence after
   #664 settles what `req_count` should compare, since re-measuring a wrong
   metric still yields a wrong receipt."* True when written. By the time the
   issue was worked, `req_count` had been excluded from `has_drift` upstream
   (`brief_reconcile.py:175-181`), so the metric could not reach the receipt and
   the precondition was moot. Its companion caveat — a path conflict with an
   in-flight OBPI — had also cleared (no active locks). Both were disproved by
   reading, and neither would have been caught by trusting the comment.

   This is the GHI-surface cut of the decay #696 names on the handoff surface:
   a decision recorded in session N, still shaping work in session N+M, with no
   freshness signal attached. Treat a stale precondition as a finding worth
   stating, not merely an obstacle that turned out to be absent.

2. **Classify the GHI's prescriptive shape.** The body almost always fits one of:

   | Shape | Detection | Execution path |
   |-------|-----------|----------------|
   | Single prescribed fix | Body describes one concrete change | Execute it (Phase 2) |
   | Multiple options, dominant choice exists | "Proposed resolution" lists N options, but one is dominant per DO IT RIGHT #3 | Pick the dominant option, note the rationale in the close comment, execute |
   | Multiple options, no dominant choice | Genuinely balanced tradeoffs with no preservation/discard asymmetry | Escalate (Phase 2, § Escalation) |
   | Investigation (no fix yet) | Label `investigation`; body is diagnostic, not prescriptive | Execute the investigation; close with findings or spawn a defect GHI for the discovered fix |
   | Already-resolved | A commit with `(GHI #N)` trailer exists; GHI forgot to close | Skip to Phase 3 (Verify) |
   | Forward-reference tracker | GHI's prescribed work is "after upstream X lands, do Y" and the upstream OBPI/ADR now exists (drafted, in-progress, or complete) under an active ADR that absorbs the tracker scope | Close `superseded` citing the upstream OBPI/ADR — do not wait for upstream completion. The existence/authoring of the named OBPI is sufficient; per-step work lands as commits + receipts under the upstream ADR's umbrella, not via this GHI |

3. **Check for pre-existing fix commits.**

   ```bash
   git log --all --grep="GHI #<N>\|Closes #<N>\|Fixes #<N>" --format="%H %s"
   ```

   If a commit exists and fully resolves the GHI, this is the "already-resolved" shape — skip to Phase 3. If the commit is a partial fix, continue to Phase 2 to complete the class-of-failure coverage.

3a. **Establish the bounded closure contract** above before Phase 2. For an
   already-resolved issue, reconstruct it from the original intent before
   verifying the existing fix. Do not derive the contract from its passing tests.

### Phase 2 — Execute

4. **Route the fix** per § Doctrine — defect remedies are direct fixes, NEVER new OBPIs.

   - **Direct fix (the route for every defect, investigation, or
     enhancement GHI)**: proceed inline — apply edits, write the Red test,
     run Green, commit `fix(<scope>): <summary> (GHI #N)`. Diff size and
     surface heat go in the commit body and the verification evidence.
   - **Operator escalation (only when scope is genuinely uncertain AND
     the operator has not already chosen a route)**: surface the routing
     facts — estimated diff, surfaces touched, precedent count from
     `git log --since='60 days ago' --oneline --grep='^fix('` — and ask.
     The choices are "direct fix now", "split into smaller direct fixes",
     or "wait for an unlanded upstream"; "author an OBPI" is never one of
     them. Unmet ADR intent is the operator's to route: [`references/repair-assignment.md`](references/repair-assignment.md).
   - **Route correction (only when the GHI is mis-labeled feature work,
     not a defect at all)**: the work is *new capability* that belongs in
     a planned increment. Author the destination in this session and close
     `superseded` citing its registered ID; if it cannot be authored now,
     the GHI stays open with a blocker comment. Closing `withdrawn` with a
     redirect to `gz-design` is the dead-letter (§ Doctrine — NEVER, EVER, EVER dead-letter a GHI, rule 1).

   **Escalation** (only these blockers permit terminating without close):

   | Blocker | Surface to operator |
   |---------|---------------------|
   | Genuinely balanced options with no preservation/discard asymmetry | Present the tradeoff with evidence; operator chooses |
   | Fix requires destroying data, a force-push, secret rotation, or another hard-to-reverse action | Confirm before acting |
   | Fix depends on an unlanded upstream (another agent's in-flight OBPI, external API change) AND no upstream OBPI/ADR has yet absorbed the scope | Note the dependency in a GHI comment; GHI stays open until upstream lands. **Caveat:** if the GHI is a forward-reference tracker and an upstream OBPI/ADR now exists that absorbs the tracker scope (even if not yet Completed), this is the "forward-reference tracker" Phase-1 shape — close `superseded` citing the upstream, do not leave open waiting on completion |
   | GHI is mis-labeled feature work and its destination cannot be authored in this session | Leave open with a blocker comment naming the next concrete operator action (see route-correction bullet above) |
   | A live OBPI brief owns the surface (`AGENTS.md` § Defect-fix routing) | Surface the brief, its status and its parent ADR; wait for the operator's ruling |

   "The precedent count is low so I'm unsure" is not a blocker — surface it with the routing facts and proceed on the operator's choice. "The fix is boring" is not a blocker. **"The fix is large enough that an OBPI feels safer" is not a blocker — it is the doctrine alarm.**

5. **Apply the fix** in the chosen route. TDD discipline per `.gzkit/rules/tests.md` § Red-Green-Refactor applies to any code change; doc/brief/WBS edits skip the test cycle but still record observed output per `AGENTS.md` § DO IT RIGHT #4.

6. **Commit with the trailer.** Every closing commit body MUST contain `(GHI #N)` or a `Closes #N` / `Fixes #N` trailer.

### Phase 3 — Verify

7. **Run the evidence block** on the landed artifacts:

   a. **Commit trailer check.** `git log --all --grep="GHI #<N>\|Closes #<N>\|Fixes #<N>"` returns the fix commit(s). Missing trailer is a process defect — amend via a new trailer-bearing commit before continuing.

   b. **Class-of-failure check — verify the contract's family against its witnesses.** Does the fix cover the failure mechanism across the declared inputs, states and consumers? A missing member blocks a `fixed` disposition: amend the contract with the evidence and repair it, or retain an explicit unresolved obligation with a real destination. An independent neighboring finding does not block this issue once its own contract passes. Follow the expansion and stopping rules above.

      **Naming tests is not the check.** Write the family out as a list of causes, and for each cause name the test that exercises *that cause*. A cause with no test of its own is uncovered no matter how many tests the fix added — and a family you cannot enumerate is a family you have not verified. Ask the inverse explicitly: *which input in this family does no test drive?* If the answer is "none", say how you determined that; if you cannot enumerate exhaustively, say so and scope the claim to the causes you did cover.

      **Canonical regression (GHI #771, arm B).** GHI #708's 2026-07-21 close comment enumerated three causes and asserted *"All three now hit the same guard"* — while listing three tests by name one section up. The enumeration omitted the cause that was the entire premise of the flag the guard sat inside (an ordinary dirty worktree, nothing staged), and all nine tests stubbed the same git read. The defect sat marked-closed for seventeen days and re-landed as `57bd15f91`. Evidence was named; the family was wrong.

   c. **Test semantics check.** New tests assert REQ-derived semantics per `.gzkit/rules/tests.md` § Red-Green-Refactor (**Tests assert semantics, not strings**). String-shape tests outside the output-form fixture carve-out are the GHI #272 cosmetic-backfill pattern — re-derive before continuing. **Falsifiability:** when the fix adds production code, run `uv run gz arb red --commit <sha>`: each added hunk is reverted and the commit's own tests re-run (GHI #927); a hunk whose revert cannot be graded is re-run one guard statement at a time, and one with no guard statement is a `declaration` row outside the verdict (GHI #1153). `undriven` or `no-tests` means a guard nothing in the fix can fail on — add the test before closing. `inconclusive` is about the run; cite its reason instead of a verdict. Every run writes an `arb-red-commit-*` receipt and prints its id; cite that receipt id in the close comment, resolved per step 7d, never the verdict text alone (GHI #1152).

   d. **Heavy-lane ARB receipts — resolve, don't transcribe.** For heavy-lane or foundation-kind fixes, ARB receipts exist for lint/typecheck/tests/coverage/docs per `AGENTS.md` § Attestation. Cite receipt IDs in the close comment, and confirm each one resolves on disk before citing it:

      ```bash
      ls artifacts/receipts/<run-id>.json
      ```

      A receipt ID copied from a prior comment, a sibling GHI, or session recall is a string, not evidence — `AGENTS.md` § Attestation: *"A fabricated receipt ID is a fabricated claim."* Same family as steps 7b and 7f: the claim must be derived at this close, not restated.

   e. **Observed output evidence.** For fixes touching CLI rendering, skill routing, or operator-facing output, the commit body contains observed output or a test reference per `docs/governance/tool-skill-runbook-rationale.md` § Commit-message discipline for skill-routing changes.

   f. **Reference-liveness check.** Resolve every `#N` the close comment will cite — including any carried forward from a prior close comment on this same GHI — against live state before writing it:

      ```bash
      gh issue view <N> --json number,state,stateReason,closedAt \
        --jq '"#\(.number) \(.state)/\(.stateReason) \(.closedAt)"'
      ```

      A citation describing another GHI as open, blocked, or outstanding must be re-derived at *this* close, never transcribed. Annotate a settled reference rather than deleting it — citing and depending are different claims, and the historical link is usually still worth keeping.

      **Canonical regression (GHI #771, arm A).** GHI #708's 2026-07-21 close comment noted *"**Note on #573:** that issue remains open and is unaffected by this fix"* — true when written. #573 closed 2026-07-24. The 2026-08-08 re-close carried the same claim into its `## Related` section, fifteen days after it stopped being true, because it was copied rather than resolved. The handoff surface closed this same gap in `ef3f9e0a2` via the `ReferenceChecker` port (`src/gzkit/handoff_api.py`); close comments have no such adapter, so the resolution is manual and belongs here.

### Phase 4 — Close

8. **Build the close comment** with the disposition and evidence:

   | Disposition | Meaning |
   |-------------|---------|
   | `fixed` | The skill executed the fix in Phase 2, verified in Phase 3 |
   | `superseded` | A registered destination — another GHI, an ADR, or a brief — carries the scope, whether it pre-existed or was authored in this session |
   | `withdrawn` | The contradicting rule changed during read; the defect is no longer a defect |
   | `duplicate` | The same defect already has a GHI with a prior-number |
   | `won't-fix` | Operator explicitly accepted the risk during Phase 2 escalation |

   Template:

   ```markdown
   **Disposition:** <fixed|superseded|withdrawn|duplicate|won't-fix>

   **Resolved by:** <commit-sha(s) / ADR-X.Y.Z / OBPI-X.Y.Z-NN / GHI #M>

   **Closure contract:** <invariant, population/consumers, and exit condition>
   **Contract amendments:** <new evidence and resulting changes, or none>

   **Verification:**
   - Tests: <file::TestClass::test_name>  (or "doc-only: no test tier")
   - Observed output: `<command>` → <brief excerpt>
   - ARB receipts: <arb-step-unittest-...>, <arb-step-ruff-...>  (heavy/foundation only)

   **Class-of-failure coverage:** <one sentence — the class the GHI named, not the instance>

   | Cause in the family | Covering test |
   |---|---|
   | <cause 1> | `<file::TestClass::test_name>` |
   | <cause 2> | `<file::TestClass::test_name>` |

   <one sentence: how you determined the enumeration is exhaustive — or which causes it deliberately does not claim>

   **Review:** <criterion-based findings and their disposition; remaining blockers, or none>
   **Independent discoveries:** <tracked references that do not block this contract, or none>
   ```

   The table is the step-7b answer made checkable: a row with an empty right cell
   is an uncovered cause stated plainly, which is the honest close. Prose alone
   cannot show a missing row. For a doc-only fix with no test tier, name the
   observed-output check or the grep that stands in for each cause.

   Every `#N` in `## Related` — and anywhere else in the comment — is resolved
   per step 7f before the comment is written. Mark a settled reference inline
   (e.g. `#573 — closed 2026-07-24`) rather than dropping it.

9. **Close the issue.**

   ```bash
   gh issue close <N> --comment "$(cat <<'EOF'
   ...close comment from step 8...
   EOF
   )"
   ```

10. **Propagate and stop.** Record the close through the permitted surfaces; preserve append-only history and operator-only brief-edit rules. Report references requiring another authorized workflow rather than initiating it. Once accounting and guarded sync finish, stop this work order; do not draw a discovered sibling automatically.

## Examples

### Example 1 — Prescriptive-fix GHI, direct-fix route

**Input**: GHI #291 ("OBPI-0.36.0-08 premise broken: `.claude/rules/arb.md` absorbed twice") lists two resolutions: (a) refresh OBPI-0.36.0-08 scope to target `AGENTS.md` § Attestation + `docs/governance/arb-middleware.md`; (b) withdraw the OBPI.

**Process**: Phase 1 classifies as "multiple options, dominant choice exists" — option (a) preserves the reconciliation intent per DO IT RIGHT #3. Phase 2 routes to direct fix (≤30 lines, 2 files: the OBPI brief and ADR-0.36.0 WBS row, in-flight scope). Apply edits, commit `fix(obpi-0.36.0-08): retarget reconciliation to AGENTS.md + arb-middleware (GHI #291)`. Phase 3 verifies: trailer present; class-of-failure closed (no other surface references the stale path after grep); doc-only edit so no test tier; observed-output is a grep of the brief showing the new paths. Phase 4 closes with `fixed` disposition citing the commit SHA and the grep evidence.

### Example 2 — Already-resolved GHI (forgot-to-close)

**Input**: GHI #192 was fixed by commit `4e914dd0` (`fix(validator): skip pool ADRs... (GHI #192)`), tests at `tests/commands/test_validate.py::TestValidateFrontmatter::test_pool_adrs_skip_frontmatter_check` assert the pool-skip semantic. GHI still open.

**Process**: Phase 1 classifies as "already-resolved." Skip Phase 2. Phase 3 verifies: trailer present; class closed; test asserts REQ-derived semantic, not string. Phase 4 closes with `fixed` disposition citing the existing commit + test.

### Example 3 — Partial-fix GHI, class-of-failure still open

**Input**: GHI #234 ("helper scripts crash on Windows UTF-8") has a partial commit fixing one script.

**Process**: Phase 1 classifies as "already-resolved" → Phase 3 surfaces class-vs-instance drift at step 7b. Phase 2 reopens: either expand this GHI's fix to cover the class (every Python helper processing piped gz output), or file a follow-up GHI and keep this one open as parent. This skill applies the class fix (commits covering the remaining scripts with `(GHI #234)` trailers) then returns to Phase 3. Phase 4 closes when the class is truly covered.

### Example 4 — Routed-to-pool-ADR GHI (architectural absence)

**Input**: GHI #349 ("gzkit governance surface is choreographed, not state-machined") was filed during OBPI-0.0.21-08 closeout. Its body lists symptoms (vocab proliferation, silent state demotion in GHI #348, bolted-on transition guards, reconcile-then-precomplete loops) and states the finding is upstream of any specific defect. No commit can fix the architectural absence; the right home is a pool ADR for the design conversation.

**Process**: Phase 1 classifies as "forward-reference tracker" (Phase-1 shape table) — but the upstream isn't an existing ADR/OBPI; it has to be authored. Phase 2 routes via the **same-session destination authoring** path: `uv run gz plan create obpi-state-machine --kind pool --lane heavy --title "OBPI State Machine and Runtime Invariant Monitor"` populates the pool ADR file; the agent fills Intent / Decision / four rejected alternatives / ADR relationship matrix grounded in GHI #349's evidence; commit. Verify the ADR appears in `uv run gz adr report` (Pool table). Phase 4 closes `superseded` citing `ADR-pool.obpi-state-machine`.

**Why this is not dead-lettering**: the destination exists at close time, registered in `gz adr report`. The pool ADR has its own promotion ceremony, its own gate covenant on promotion, and will spawn its own OBPIs when the operator is ready to design. GHI #349's purpose was to route the architectural observation to a durable home; that purpose is fulfilled.

**Sibling close**: GHI #348 (concrete observed symptom of the same architectural absence) closes `superseded` in the same session against the same pool ADR. One destination, multiple routing-receipt closes — each GHI captured a different cut into the finding.

### Example 5 — Investigation GHI

**Input**: GHI #<N> labeled `investigation` ("reconcile caches regenerating at 3x expected rate"), no prescriptive fix in body.

**Process**: Phase 1 classifies as investigation. Phase 2 performs the investigation — instrument, measure, identify cause. If the finding is a defect: file a new `defect` GHI for the fix, commit the investigation artifact if any, close this GHI with `fixed` citing the finding and the follow-up GHI. If the finding is "working as designed": close with `withdrawn` citing the observed rate as correct + the documentation commit that clarifies the expectation.

### Example 6 — Heavy-surface defect (still direct fix, not OBPI)

**Input**: GHI #N describes a defect in `gz validate --frontmatter` that fails to detect a specific schema-drift pattern. The fix touches `src/gzkit/governance/trust_audits/` (validator package), `src/gzkit/schemas/adr.json` (schema rule), and adds two new unit tests — roughly 80 lines across 3 files. Heavy-lane surface, foundation-adjacent.

**Process**: Phase 1 classifies as single prescribed fix. Phase 2 routes to **direct fix despite the heavy-surface scope** — defect remedies are direct fixes regardless of which schema, CLI verb, or runtime contract they touch. The 80-line / 3-file count is a routing fact recorded in the commit body, not a trigger to author an OBPI. Apply edits, write the RED tests, GREEN, commit `fix(validate): detect schema-drift pattern X (GHI #N)`. Phase 3 verifies trailer; class-of-failure (the pattern is closed across all schemas, not just the one observed); test semantics (REQ-derived, not string-shape); heavy-lane ARB receipts. Phase 4 closes with `fixed` disposition citing commit SHAs + receipt IDs.

**Counter-example (when the GHI is mis-labeled feature work)**: GHI #M describes "validator should support dependency-graph cycle detection" — this is new capability, not a remedy for a broken behavior. Phase 2 takes the route correction: author the destination in this session (Example 4 shows the pool-ADR motion), verify it is registered, and close `superseded` citing its ID; if it cannot be authored now, the GHI stays open with a blocker comment. This is the only legitimate path from a GHI to planned work, and it is a *route correction*, not an OBPI-as-fix execution.

## Constraints

- **NEVER, EVER, EVER dead-letter a GHI.** § Doctrine — NEVER, EVER, EVER dead-letter a GHI binds every close: the disposition cites a destination that exists, or the GHI stays open with a blocker comment naming the next concrete operator action.
- **Complete the bounded closure contract, then stop.** "No commit found" is the trigger to author one, not an exit condition. An unmet criterion or a Phase 2 escalation blocker remains visible; closure pressure never licenses a false `fixed` disposition or an unbounded neighboring repair.
- **Never close on a narrative claim.** Cite a commit SHA, ADR ID, brief ID, or receipt ID — every close comment references a verifiable artifact.
- **Never close with the operator's personal email in the comment.** `AGENTS.md` § Execution Rules (Operator PII) applies to `gh` comments as much as to commits.
- **Never use `gh issue close` without a `--comment`.** Silent close corrupts the audit trail.
- **Never batch-close GHIs.** One GHI, one disposition, one comment.
- **Never fabricate an ARB receipt ID or commit SHA.** Cite only what you verified exists.

## Common Rationalizations

These thoughts mean STOP — you are about to either leave a corrupted audit trail or abandon the GHI mid-resolution:

| Thought | Reality |
|---------|---------|
| "No fix commit exists yet, so I should stop and report" | Wrong. The skill's job is to *produce* the fix commit. Route per AGENTS.md § Defect-fix routing and execute. |
| "The GHI carries a blocker comment, so it's blocked" | A blocker describes the tree on the day it was written. Re-derive it (Phase 1 step 1a) before honoring it — GHI #677's blocker had been moot for days and nothing said so. A blocker you did not re-check is hearsay, not a gate. |
| "The blocker was written by the operator, so it still binds" | Authorship makes it *authoritative about intent*, not *current about code*. The operator ruled on the tree they saw. Re-deriving honors that ruling; treating it as timeless outsources judgment to a stale snapshot. |
| "The GHI has two proposed resolutions and I should ask which one" | Only if the options are genuinely balanced. Usually one option preserves reconciliation intent and the other discards it — pick the preserving one per DO IT RIGHT #3 and note the rationale in the close comment. |
| "The commit clearly fixes it; I don't need to verify tests" | Verification is the point of Phase 3. If tests assert strings instead of semantics, the class is still open. |
| "I listed the tests by name, so the class claim is backed" | **Naming is not covering.** GHI #708's close comment named three tests and asserted a three-member family — and the family omitted the cause that actually fired seventeen days later (GHI #771). Build the cause→test table (step 7b) and read it for empty right cells. The question is never "did I cite evidence", it is "which cause has no test". |
| "The prior close comment said #N is still open, so I can carry that forward" | A prior comment describes the day it was written — the same hearsay problem as a stale blocker, one row up. Re-resolve every `#N` at *this* close (step 7f). GHI #708's note on #573 was true on 2026-07-21 and false when restated on 2026-08-08; nothing in between changed except the world. |
| "I'll close it now and add the evidence later" | The close comment is the evidence. "Later" never comes. |
| "This GHI is stale; just close it" | Stale GHIs get `withdrawn` (rule changed) or `won't-fix` (operator-approved risk), not silent closes. Name the disposition. |
| "Multiple GHIs resolve together; let me close them all with one comment" | Each GHI has its own disposition. Batching conflates them. |
| "The commit trailer is missing but the fix is obvious" | Missing trailer is a process defect. Amend via a new trailer-bearing commit. |
| "Won't-fix without operator sign-off is fine for small ones" | Won't-fix is risk acceptance. Unilateral risk acceptance is the scope-creep anti-pattern in a different costume. |
| "I analyzed the GHI, posted a thorough comment, and left it open — that's the right conservative move" | No. Analysis without execution is busywork; leaving it open is correct only when a Phase 2 escalation blocker holds. |
| "I'll close it as `withdrawn` and route to /gz-design — the operator can author the ADR next" | **DEAD-LETTER.** The destination doesn't exist yet, and a skill name is a pointer to *capability*, not a landing site for scope. Author the destination in this session and cite it by ID, or leave the GHI OPEN with a blocker comment. See § Doctrine — NEVER, EVER, EVER dead-letter a GHI. |
| "The operator said 'close it for now and we'll handle it later'" | Surface that "later" needs a destination. Either author the ADR/brief now and cite it, or leave the GHI open with the deferred-action comment. The skill never executes a "close for now" request — that's the dead-letter pattern wearing the operator's voice. |
| "This defect touches a heavy-lane surface (CLI/schema/contract), so it needs an OBPI" | **Wrong.** Surface is a routing fact. `AGENTS.md` § Defect-fix routing: a GHI authorizes direct repair, and no ADR or OBPI is created to discharge one. Ship the fix as `fix(<scope>): … (GHI #N)` with TDD evidence and (for heavy/foundation) ARB receipts in the close comment. |
| "The fix is too large for a direct fix; let me author an OBPI to be safe" | **Size is a routing fact, not an OBPI trigger.** A 100-line defect remedy is a 100-line direct fix with a thorough commit body. If size is genuinely making you uncertain, escalate to the operator with the routing facts. Do not list "author an OBPI" as one of the choices. |
| "The GHI body literally says 'OBPI ceremony required'; I should specify an OBPI" | Re-read the body. If it prescribes new-capability scope, the GHI is mis-labeled — take the step 4 route correction. If it prescribes a defect remedy that touches a heavy surface, it is still a direct fix; the GHI body's authoring-time language does not override doctrine. |

## Red Flags

- **Close comment cites a destination that doesn't exist yet** — "the eventual ADR for this", "should become an OBPI", "operator will route to /gz-design next", "re-route to design pipeline" — these are dead-letter signatures (§ Doctrine — NEVER, EVER, EVER dead-letter a GHI)
- **`withdrawn` disposition on a GHI whose premise still stands** — `withdrawn` is for premise-evaporated GHIs, not for "this should be an ADR but I haven't authored one yet"
- **A recorded precondition is honored without being re-derived** — the GHI says "blocked on X" / "sequence after #M" and the agent accepts it rather than reading the surface it names. The blocker describes a past tree (Phase 1 step 1a)
- Agent posts a long analysis comment and does not close, when no escalation blocker holds
- Close comment is "Done" or "Fixed" with no artifact reference
- **Class-of-failure claim asserts a family in prose with no cause→test table** — "every path inherits it", "all three now hit the same guard", "closed at the root" are the signatures. A family worth claiming is a family worth enumerating; if it cannot be enumerated, say so and scope the claim (step 7b)
- **A `#N` described as open, blocked, or outstanding that was copied from a prior comment rather than resolved** — especially in `## Related` on a re-close, where the citation is inherited from the close being superseded (step 7f)
- Close happens before verification steps 7a–7f run
- Multiple GHIs closed in a loop without individual re-evaluation
- Disposition chosen by vibe rather than by the Phase 1 shape table
- Commit claimed to fix but has no `(GHI #N)` trailer and no follow-up amendment
- Personal email or other PII in the close comment
- Closing a `heavy`-lane or `foundation`-kind GHI without ARB receipts
- **Authoring or specifying a new OBPI as the resolution path for a `defect`-labeled GHI, or handing off mid-Phase-2 to `gz-obpi-specify`** — defect remedies are direct fixes (§ Doctrine — defect remedies are direct fixes, NEVER new OBPIs); the one exception is a repair assignment the operator ruled ([`references/repair-assignment.md`](references/repair-assignment.md))

## Related Skills

- `ghi-author` — upstream authoring surface; pairs with this skill's § Doctrine — Routing fulfills a GHI's purpose to produce the file→route→close contract
- `gz-obpi-specify` + `gz-obpi-pipeline` — **NOT a destination from this skill's fix-execution path** (§ Doctrine — defect remedies are direct fixes, NEVER new OBPIs)
- `gz-design` + `gz-plan` — the authoring surface when a GHI's prescribed work turns out to be new capability; reached by the step 4 route correction, never as a continuation of fix execution
- `gz-obpi-sync` — when an OBPI under an active ADR happens to mention a GHI in its evidence (e.g. brief notes "addresses GHI #N"), reconcile propagates the closure to brief evidence; this is downstream of the OBPI's own pipeline, not a Phase-2 route from `ghi-close`
- `gz-adr-closeout-ceremony` — end-of-ADR pass often triggers `ghi-close` operations on GHIs that surfaced during the ADR's lifetime
- `git-sync` — the commits that close GHIs flow through sync

## Related Rules

- `AGENTS.md` § PRIME DIRECTIVE (complete the behavior and its coupled surfaces; track every defect)
- `AGENTS.md` § DO IT RIGHT #1, #3, 6h (fix the class; remove the cause inside the requested scope; quote conflicts verbatim)
- `AGENTS.md` § Attestation (ARB receipt discipline for heavy-lane closures)
- `.gzkit/rules/gh-cli.md` (allowed `gh` commands)
- `docs/governance/tool-skill-runbook-rationale.md` § Commit-message discipline for skill-routing changes (observed-output evidence)
- AGENTS.md § Defect-fix routing (the routing matrix applied in Phase 2)
- `.gzkit/rules/tests.md` § Tests assert semantics, not strings (test verification in step 7c)
- `AGENTS.md` § Execution Rules (operator PII — never in close comments)
