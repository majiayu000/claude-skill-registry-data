---
name: ghi-author
persona: main-session
description: Use to file a GitHub issue when a finding needs its own work order or the operator asks; OBPI corrections stay in its change log.
category: agent-operations
lifecycle_state: active
owner: gzkit-governance
last_reviewed: 2026-10-17
metadata:
  skill-version: "1.11.1"
model: sonnet
---

# ghi-author

## Invocation

```
ghi-author
```

No ID argument. `gh issue create` assigns the next available issue number on
the remote; the skill records the assigned number into session evidence
after creation (step 6). Passing an ID would conflict with GitHub's
auto-assignment and corrupt cross-references.

First determine whether the finding needs an independent work order or
disposition. `AGENTS.md` § PRIME DIRECTIVE requires durable tracking;
an active OBPI already supplies a work order, requirement identities, and
evidence provenance. It does not need an issue number for each correction.

**Active-OBPI boundary (operator ruling, 2026-09-08).** Changes necessary to
satisfy an operator-initiated OBPI's approved obligations remain part of that
OBPI. Record substantive corrections under `## Evidence` → `### Change Log`,
reuse existing finding identities, and continue its authorized pipeline.
Do not file a GHI merely because a review found a defect, a test was weak,
evidence needed correction, or a repair took several iterations. A genuine
requirement/allowlist/threat-model amendment still uses the existing operator
ruling; it does not automatically need an issue. A GHI is appropriate for a
separate infrastructure defect, independently owned work, or a post-acceptance
defect. Filing one never discharges an unmet OBPI obligation.

An explicit operator request to file an issue takes precedence over the default
no-issue branch. Link the issue to the owning OBPI; its obligations and existing
finding/closure records remain there.

## Doctrine — A GHI's purpose is observation routing, not implementation tracking (binding)

**Invocation boundary (GHI #980).** When this skill is invoked only to record
an independent discovery during another work order, or the operator requested
authoring only, create the durable issue, record its eligibility and next-work
disposition, then return. Do not implement it or author an ADR/OBPI destination
as a side effect. An eligible but unselected issue is open work, not a technical
blocker and not a dead letter. This branch takes precedence over the same-session
execution and destination-authoring instructions below. Those instructions
apply when resolution of this finding is part of the selected work order.

A GHI exists to **route an observation to a durable governance artifact**.
Once the finding has been homed in a registered destination (a commit SHA,
a foundation/feature ADR, a pool ADR, an OBPI brief, or a higher-numbered
GHI that absorbs the scope), the GHI's purpose is **fulfilled** and the
GHI is closable. Implementation lifecycle thereafter belongs to the
destination artifact, not to the GHI.

This rule closes a failure mode where GHIs accumulate as long-lived
"wait-around trackers" that shadow-track work already owned by an ADR or
OBPI. A pool ADR has its own promotion ceremony; a foundation ADR has its
own gate covenant; an OBPI has its own pipeline. None of those need a
GHI sitting open to remind anyone that they exist — the artifact graph
already does that.

**Operative consequences for the authoring pass:**

1. **When a finding's right home is a pool ADR or OBPI brief, author the
   destination in the same session as the GHI** — using `gz plan create
   --kind pool ...` or `gz-design` → `gz-plan` → `gz-obpi-specify`. The
   GHI then closes immediately with `superseded` disposition citing the
   destination ID. One observation, one routing pass, one terminal state.
2. **Pool ADRs count as registered destinations.** A pool ADR visible in
   `uv run gz adr report` (Pool table) is a valid `superseded` upstream
   under `ghi-close`'s rules — it is registered in the artifact graph
   even if not yet promoted to feature kind. Promotion is
   the destination's lifecycle, not the GHI's.
3. **Multiple GHIs may share one destination.** A symptom GHI (concrete
   reproduction), a class-of-failure GHI (broader pattern), and an
   architectural-absence GHI (the missing artifact) can all close
   `superseded` against one pool ADR — each GHI is a different cut into
   the same finding, and the ADR carries them collectively.
4. **GHIs that cannot be routed in-session stay open with a blocker
   comment.** This is the inverse of dead-lettering (see `ghi-close` §
   Doctrine — NEVER, EVER, EVER dead-letter a GHI). Open-with-blocker is
   the honest state when the destination cannot yet be authored;
   closed-with-route-promise is the corrupted-audit-trail state.

**Anti-pattern:** Filing a GHI and treating it as a long-lived tracker
that "closes when the work ships." The work shipping is the destination
artifact's responsibility (its own gates, its own attestation, its own
ledger events). A GHI that waits around to mirror the destination's
status is duplicate state — the same shape Layer-3 derived views become
when they silently shadow Layer-2 truth.

## Trigger

- A finding needs an independent work order or disposition beyond the active OBPI
- A defect in an accepted deliverable needs corrective work
- An investigation or enhancement needs its own durable home
- Operator says "file a GHI for that" or equivalent

## Behavior

Produce a GHI whose body contains enough evidence for a future agent or
reviewer to re-apply the routing matrix without re-investigating. The
authoring pass does **not** decide direct-fix vs. OBPI ceremony — that is
AGENTS.md § Defect-fix routing's job at fix time. It does produce the evidence the
routing matrix will consume. When the finding is that a shipped surface does not
fulfil an ADR's declared intent, quote that intent: it is the one case the operator
may rule into the in-flight ADR as a repair assignment, and never the agent's to route.

## Prerequisites

- `gh auth status` reports authenticated (see `.gzkit/rules/gh-cli.md` allowed commands)
- Working tree is in a known state (uncommitted scratch work should not leak into the evidence block)
- You have read the surface the defect touches — authoring a GHI without reading the code is vibe-tracking and produces cargo-cult issues

## Steps

0. **Prior-art lookup (binding pre-flight — MANDATORY).** Before drafting anything, search for adjacent open GHIs and recent closes. Skipping this step is a process defect; resulting duplicates close on discovery under `ghi-close`'s `duplicate` disposition with a one-line "duplicate of #N" comment.

   Two queries — keyword search PLUS recent-by-date skim. Keyword search alone misses semantic neighbors that share root cause without sharing surface words.

   ```bash
   # Keyword search across open + recent closes (last 30 days).
   # Use 2–3 surface keywords from the observed symptom, not narrative phrasing.
   gh issue list --state all --search "<keywords> created:>=$(date -v-30d +%Y-%m-%d)" --limit 20 \
     --json number,title,state,labels,createdAt

   # Recent open by date — catches semantic neighbors keyword search misses.
   gh issue list --state open --limit 20 --json number,title,labels,createdAt

   # Does an authored OBPI brief already OWN this work? (GHI #864)
   # Search on the SURFACE — a path, an id, a symbol — not on narrative words.
   grep -rln "<surface path / entry id / symbol>" docs/design/adr/*/*/obpis/*.md

   # Did an R&D run already decline or route this? (rnd-discipline.md, disposition map)
   grep -rln "<keywords>" docs/rnd/ 2>/dev/null
   ```

   Read every title in both result sets (titles are cheap; read bodies only on candidate hits).

   **Then run the class test, because titles do not carry it.** A title names a
   surface and a symptom; sibling-cut adjacency is a property of the ROOT CAUSE.
   Before concluding "no prior", state your finding's class of failure (Step 2's
   third bullet) in one sentence and ask of each skimmed title: *could this be
   the same class on a different surface?* Two issues in one class routinely
   share no surface word at all. If you cannot answer without the body, open the
   body — the skim is 20 titles, not 20 issues.

   Decide which branch you are on:

   | Result | Action |
   |--------|--------|
   | An open GHI already covers this exact finding | **Do not file.** Add a comment to the existing GHI with this session's new evidence; record the issue number in session evidence; stop. Duplicate-filing is the failure mode this step closes. |
   | An open GHI covers an adjacent / sibling-cut of the same root cause | Author this GHI but include `Related: #N` in the body's `## Related` section AND post a cross-link comment on the sibling GHI naming the relationship (root vs. symptom, per-skill vs. catalog-wide, etc.) at authoring time, not as a follow-up. Write the bare `#N` — never `#N (open)` (§ Step 4) |
   | The finding is the **Nth member of a recurring family** already tracked as a class | **Do not enumerate the siblings.** Cross-linking each one is noise that grows quadratically and decays immediately. Name the family once and the locus that tracks it — the campaign box, or the row of `docs/governance/advisory-rules-audit.md` that scores the class — and file only if THIS instance needs its own work order. If no locus tracks the class yet, say so in `## Related`: an untracked recurring family is itself a finding, and it is the operator's to route |
   | A recently-closed GHI (≤30 days) addressed this exact finding | Re-open it (`gh issue reopen <N>`) with a comment citing the regression evidence — never file a fresh GHI for the same root cause |
   | The active, operator-initiated OBPI owns this correction under its approved obligations | **Do not file unless the operator explicitly requested an issue.** Keep the correction and evidence in that OBPI's change log and continue its pipeline; an explicitly requested issue links back to that work. |
   | Another live OBPI owns the work, or the correction requires an unapproved amendment | Read the brief's `status:`, parent ADR, and matching requirement lines; surface the actual ownership or amendment decision to the operator. Do not initiate that OBPI or file a duplicate work order. |
   | An R&D record under `docs/rnd/` carries this finding as a `not pursued` row in its **disposition map** | **Do not file on your own judgment.** Quote the record's reason and the row to the operator; a rejected idea is re-opened only by the operator. |
   | No prior or adjacent GHI exists | Proceed to Step 1 |

   **Canonical sibling-cut regression (the PAIR shape):** GHIs #459 and #460 (2026-05-12) shared the T1→T2 doctrine-drift root cause (skill prose declares an agent action with no mechanical fail-close) but shared no title keywords — #459 named the per-skill Stage 2 dispatch gap, #460 named the catalog-wide skill-body-as-procedural-script surface. #460 was filed ~17 minutes after #459 without cross-link at authoring time; the relationship was only recorded in a follow-up comment after the operator noticed the overlap. The recent-by-date skim reaches this class even when keywords disagree.

   **Canonical FAMILY regression — the skim reaching the sibling is not the defense (measured 2026-09-20):** GHI #1063 was authored with zero cross-links. Its `## Related` section is empty. Replaying Step 0's recent-by-date query at #1063's own authoring instant returns #1017 at rank 12 of the 20 titles shown — **the query did not miss it; the reading did** — and 11 of those 20 titles are members of #1063's own `doctrine-declared-without-mechanism` family. A 55%-family skim produced no relationship at all, because nothing in this step told the author to test for class, and the class is not visible in a title. Widening `--limit` would have changed nothing. This is why the class test above is stated separately from "read every title", and why the family row exists: at 11 siblings the correct output is a named family, not eleven cross-links.

   The pre-flight is **defense, not guarantee** — semantic neighbors may evade every query. When in doubt, surface the candidate matches to the operator with the routing facts (open GHI numbers + one-line title-summaries + relationship hypothesis) before proceeding to Step 1.

   **The residual is categorical as well as semantic (GHI #864).** A query that reads one artifact class defends against one class: the two `gh` queries read issues, the third reads authored OBPI briefs, the fourth reads R&D records. Pool ADRs and chore definitions can each own a unit of work and none of the four reads them; keep the residual honest as new work-owning artifact classes appear.

### When a brief owns the work

**Already-authorized corrections stay in their owning pipeline.** The live-brief
precondition below applies to entering another OBPI's work or changing approved
boundaries; it is not a new permission checkpoint for each finding within the
operator-initiated OBPI. See the Active-OBPI boundary above.

A proposed independent repair colliding with another live brief is a **routing
question only the operator can answer**. `AGENTS.md` § Defect-fix routing rules
it directly:

> If a live brief owns it, surface the brief, its status and its parent ADR, and wait for the operator's ruling.

Surface **the brief id, its `status:`, its parent ADR, and the requirement lines that match** — never a bare "a brief mentions this surface." Read the brief's disposition, not its vocabulary: the first report of the GHI #862 collision measured `entry_id in brief`, got 7/7, and concluded only that the work overlapped, while the brief's `retire X; RETAIN Y` structure said the opposite of the operator's ruling on all seven groups. A presence check answers *"is something armed"*, never *"what does it say"* (`AGENTS.md` § DO IT RIGHT #12).

**A terminal brief does not block** (`Completed`, `attested_completed`, `Validated`, `Superseded`, `Withdrawn`, `Abandoned`) — a fresh defect against that surface is an ordinary GHI. Another **live** brief (`Draft`, `pending`, `in_progress`) makes ownership routing operator-level; correction within the already-authorized owning pipeline does not.

1. **Classify the GHI** using the table below. Pick exactly one; a single GHI is one class.

   | Class | Label | When |
   |-------|-------|------|
   | Defect | `defect` | Something observable is wrong, drifted, or inconsistent with canonical intent |
   | Enhancement | `enhancement` | Surface works as designed; the design could be tighter |
   | Investigation | `investigation` | Unknown root cause; the GHI is to find it, not fix it |

   **Secondary labels (binding — additive, not exclusive):** apply each label below whose predicate fires. Multiple secondary labels may co-apply with one primary class.

   | Label | Apply when | Why it matters |
   |-------|------------|----------------|
   | `runtime` | The GHI's evidence cites a path under `src/gzkit/`, OR the symptom is observable behavior change at the `gz` CLI / runtime surface, OR the prescribed remedy is a `fix(...)` commit landing under `src/gzkit/` | `gz patch release --dry-run` qualifies behavior-level GHIs by `runtime` label ∩ src diff. A runtime-touching GHI without this label lands in the `diff_only` bucket and silently drops out of the patch-release narrative — the strict qualifier returns 0 even when 16 substantive runtime fixes have shipped (canonical violation: GHI #402, 2026-05-05) |
   | `tech-debt` | The fix is a remediation of accumulated drift rather than a new defect | Routes the GHI into tech-debt sweeps and chore plans |
   | `security` | The surface is registered in `data/security_surfaces.json` or the symptom has an attack-surface dimension | Triggers heightened Gate 5 walkthrough per `.gzkit/rules/security-sensitivity.md` |
   | `eval-feedback` | The GHI was authored from an evaluation-feedback loop event | Required for the `Eval-feedback-source:` commit trailer per ADR-0.0.26 |

   **Predicate heuristics for `runtime`** (any one fires the label): GHI body contains `src/gzkit/` as a path; the "Affected surfaces" section names a Python module under `src/`; the symptom block shows `uv run gz <verb>` output disagreeing with canonical intent; the prescribed remedy is shaped as `fix(<scope>): … (GHI #N)`. If the predicate fires, `--label runtime` is mandatory at `gh issue create` time, not deferrable to later operator triage.

2. **Gather evidence.** For a defect, the minimum is:
   - The exact command run and its observed output (paste, don't paraphrase)
   - The canonical source of truth the output contradicts (file path + line, or rule citation)
   - The class of failure (not just the instance — see `AGENTS.md` § DO IT RIGHT #1)
   - Where the defect came from, when it can be established: the commit, GHI or ADR that introduced it. Write `unknown` rather than guess, and `multiple` with each id when several did. Finding a defect while checking a mechanism does not make that mechanism its origin (campaign § Amendments 2026-10-03).

2a. **Draft the bounded closure contract.** Follow
   [`ghi-close` § Bounded closure contract](../ghi-close/SKILL.md#bounded-closure-contract-ghi-980):
   identify the violated invariant, relevant input/state population and
   consumers, semantic acceptance evidence, and exit condition. A failure
   class names a mechanism across that population, not every nearby defect.
   The proposed fix remains a hypothesis; do not prescribe its shape as the
   acceptance criterion. For an investigation, name the question, bounded
   evidence population, and deliverable; leave an unknown cause unknown.
   State uncertainties for the executing agent to resolve during Read rather
   than turning authoring into an unlimited investigation.

3. **Draft the title.** Format: `<surface>: <symptom>`. Keep under 70 characters; the body carries detail.

   | Good | Bad |
   |------|-----|
   | `validator: pool ADRs skip frontmatter check inconsistently` | `validator broken` |
   | `gz-adr-status: skill routes to adr report, not adr status` | `skill has wrong command` |

4. **Draft the body** using the template below. Omit sections that don't apply (e.g. investigations skip "Expected"; enhancements skip "Canonical contradiction").

   ```markdown
   ## Observed

   <exact command + observed output, verbatim>

   ## Expected

   <what the canonical source says should happen, with file:line or rule citation>

   ## Canonical contradiction

   <paste of the rule / schema / doc the observed behavior violates>

   ## Class of failure

   <one sentence: what family of inputs produces this? Not just this instance.>

   Introduced by: <commit SHA, GHI or ADR id | `unknown` | `multiple` with each id>

   ## Closure contract

   - Invariant and authority: <required behavior; for investigation, the question>
   - Boundary: <inputs/states, producers and consumers tied to the failure mechanism>
   - Acceptance evidence: <state/input → required outcome → check; valid controls included>
   - Exit condition: <demonstrated outcome and required gates; for investigation, evidence deliverable>
   - Known uncertainties / independent findings: <named unknowns and tracked neighbors, or none>

   ## Scope hint (advisory, for routing)

   - Estimated diff: <≤10 lines / ≤100 lines / larger>
   - Surfaces touched: <module paths>
   - In-flight vs. new feature: <in-flight / planned / unknown>

   ## Related

   - <linked GHIs, ADRs, briefs, rule files — bare `#N`, no state annotation>
   ```

   **Never transcribe a sibling's state into the body.** Write `#889`, never
   `#889 (open)`. GitHub renders state live at every reference, so the
   annotation is redundant when written and wrong once the sibling closes — and
   unrepairable after: `#889 (open)` is a dated record of what its author
   observed, so editing it falsifies the record, and `gh issue edit` is outside
   `.gzkit/rules/gh-cli.md`'s allowed commands. Stopping is the only remedy.
   Measured 2026-09-20: 10 such annotations open-queue-wide, 5 already decayed.
   This is the subtraction GHI #768 ruled for transcribed ADR counts, one
   surface over; `.gzkit/chores/ghi-cross-reference-staleness` measures the
   residue and `ghi-triage` reports it as `stale_annotations`.

   Keep the *relationship* — `root cause of #889` — which is your finding and
   which nothing else records. Subtract the state, keep the claim.

5. **Create the issue.** Include the primary class label AND every secondary label whose Step-1 predicate fired. Repeat `--label` per label; a runtime-touching defect that also remediates accumulated drift would carry `--label defect --label runtime --label tech-debt`.

   ```bash
   gh issue create \
     --label <defect|enhancement|investigation> \
     [--label runtime] \
     [--label tech-debt] \
     [--label security] \
     [--label eval-feedback] \
     --title "<surface>: <symptom>" \
     --body "$(cat <<'EOF'
   ...body from step 4...
   EOF
   )"
   ```

6. **Record the issue number** in the session evidence so downstream commits and briefs can cite `(GHI #N)`. If the GHI was filed during an OBPI pipeline run, add it to the brief's evidence section.

7. **Apply the invocation boundary, then route.** For authoring-only or independent-discovery capture, record the created issue's eligibility and next-work disposition and stop; do not invoke the execution rows below. Otherwise, per § Doctrine — A GHI's purpose is observation routing, decide whether the selected finding has a same-session destination:

   | Finding shape | Destination | Same-session action |
   |---|---|---|
   | Defect with a known repair (a GHI authorizes direct repair — `AGENTS.md` § Defect-fix routing) | Commit SHA | Apply the fix, commit `fix(<scope>): … (GHI #N)`, close `fixed` citing the SHA |
   | Architectural absence / new-capability finding | Pool ADR | `uv run gz plan create <slug> --kind pool --lane <lite|heavy> --title …`, then close `superseded` citing `ADR-pool.<slug>` |
   | Bounded planned-increment finding under an existing active ADR | OBPI brief | `gz-obpi-specify` against the parent ADR, then close `superseded` citing the new OBPI ID |
   | No same-session destination yet (genuinely needs operator design conversation) | None yet | Leave the GHI **open** with a blocker comment naming the next concrete operator action — see `ghi-close` § Doctrine — NEVER, EVER, EVER dead-letter a GHI |

   For a selected resolution work order, routing-and-closing is the normal
   completion path; name a real blocker when resolution cannot proceed.
   For capture-only invocations, the durable issue and next-work disposition
   complete this invocation. Do not invent a blocker to justify leaving
   unselected work open.

## Examples

Four worked examples — correction inside an active OBPI, an independent defect
surfaced mid-pipeline, an enhancement, an investigation, and an architectural
absence routed to a pool ADR and closed in the same session — live in
[`references/examples.md`](references/examples.md).

## Constraints

- **Never author a GHI with the user's personal email in the body, title, or evidence block.** Use GitHub noreply or `g0`; see `AGENTS.md` § Execution Rules (Operator PII).
- **Never paraphrase observed output.** Paste verbatim or cite the file:line. Narrative reconstruction is the reporting-pathway drift `AGENTS.md` § DO IT RIGHT 6h exists to prevent.
- **Never bundle unrelated defects into one GHI.** One GHI, one class of failure. Bundling creates a routing ambiguity the matrix cannot resolve.
- **Do not substitute filing for completing the active repair contract.** Fix its failure mechanism and directly coupled correctness surfaces. Track independent discoveries without automatically implementing them; sharing a file or being easy to fix does not make a new finding part of the active work order. Follow `ghi-close`'s evidence-based expansion rule.
- **Never omit a secondary label whose Step-1 predicate fired.** Missing `runtime` on a runtime-touching GHI silently drops it from `gz patch release` qualification; missing `security` defeats the Gate-5 walkthrough trigger; missing `eval-feedback` breaks the commit-trailer requirement under ADR-0.0.26. Secondary labels are not optional triage hints — they are mechanical inputs to downstream gates.
- **Never call `gh issue create` outside this skill.** Bypassing `/ghi-author` skips Step 0's prior-art lookup, the only defense against sibling-cut duplicates. The binding rule is `AGENTS.md` § Behavior Rules (the GHI-authoring rule; rationale in `docs/governance/behavior-rules.md` § Always #13). Cross-repo filing goes through `gz issue file`, which itself must run Step 0's pre-flight against the target repository before delegating to `gh issue create`.

## Common Rationalizations

These thoughts mean STOP — you are about to produce a low-quality GHI:

| Thought | Reality |
|---------|---------|
| "I'll just file it and fill in the body later" | A GHI with a thin body is worse than no GHI — it guarantees the next agent re-investigates. Author the evidence block now. |
| "The title is enough; reviewers will figure it out" | Reviewers are not clairvoyant. The body consumes the evidence the routing matrix needs. |
| "This defect is obvious; I don't need to cite the rule" | The canonical contradiction is what makes it a defect rather than a taste call. Cite the rule, schema, or doc. |
| "I'll combine both issues into one GHI to save numbers" | GHI numbers are free. Combining couples two routing decisions into one and corrupts the fix's scope boundary. |
| "I can write 'see session log for details'" | Session logs are Layer-3 derived state and are not canonical. Paste the evidence into the GHI body. |
| "I'll file this and let it track until the work ships" | A GHI is not an implementation tracker (§ Doctrine). When resolution is the selected work, route it to a destination in the same session and close it; if you cannot, leave it open with a blocker comment — never as a long-lived shadow tracker. |
| "This finding is too big for a fix and there's no ADR yet — I'll just leave it open" | If the right home is a pool ADR, **author the pool ADR in the same session** (step 7, row 2), grounded in the GHI's evidence, then close `superseded` citing it. |
| "I already know this finding is novel — I'll skip the prior-art lookup and save the round-trip" | **Step 0 is mandatory, not advisory.** #459/#460 were filed minutes apart by one author who was sure of both — confidence in novelty is precisely the failure-state. The queries take seconds. |
| "A brief mentions this surface, but my finding is clearly a defect — I'll file and note it" | **A live brief owning the work makes routing an operator question, not yours** (`AGENTS.md` § Defect-fix routing). Surface the brief id, status, parent ADR and matching requirement lines, and wait. |
| "The brief mentions the same ids, so the work overlaps — that's all I need to report" | **A presence check answers "is something armed", never "what does it say".** Read the disposition (§ When a brief owns the work, GHI #862). |
| "I'll call `gh issue create` directly — faster than going through the skill" | A process defect per `AGENTS.md` § Behavior Rules. The skill is the mechanical home of Step 0's prior-art lookup; bypassing it bypasses the only defense against sibling-cut duplicates. |
| "The skim returned the sibling, so Step 0 worked" | **Reaching it is not recognising it.** #1017 sat at rank 12 of the 20 titles Step 0 showed #1063's author, alongside 10 more members of the same family, and #1063 shipped with an empty `## Related`. Run the class test, not just the title read. |
| "Eleven siblings, so eleven `Related:` cross-links" | At family scale, enumeration IS the defect — it is noise that decays the moment any sibling closes. Name the family and its tracking locus once (§ Step 0, family row). |
| "I'll write `#889 (open)` so the reader knows where it stood" | GitHub renders that live at every reference; the annotation is redundant when written and wrong when the sibling closes, and it cannot be repaired afterwards without falsifying a dated record. Write the bare `#889` (§ Step 4). |

## Red Flags

- Concluding "no prior GHI" from titles alone, without stating the finding's class of failure and testing the skim against it
- Writing a state annotation — `#N (open)`, `#N (still open)` — beside an issue reference in a body or comment
- Cross-linking every member of a recurring family instead of naming the family and its tracking locus
- GHI title is a bare noun or a vague verb ("broken", "issue", "problem")
- Body contains "TODO add evidence" or equivalent placeholder
- Multiple unrelated defects bundled into one GHI
- No label applied (breaks `gh issue list --label <class>` triage)
- Body cites `src/gzkit/` paths, `gz <verb>` runtime symptoms, or a `fix(...)` remedy shape but the `gh issue create` invocation omits `--label runtime` — this is the GHI #402 silent-qualifier-drift signature
- Personal email or other PII in the body
- Filed as a replacement for a fix that was in-scope and skipped
- No bounded closure contract, or an acceptance criterion that merely repeats the proposed implementation

## Related Skills

- `ghi-close` — evaluate and close a GHI (the downstream surface)
- `gz-obpi-specify` — when routing resolves to OBPI ceremony, the brief consumes this GHI's evidence
- `git-sync` — commits citing `(GHI #N)` trailers flow through sync

## Related Rules

- `AGENTS.md` § PRIME DIRECTIVE (track every defect)
- `AGENTS.md` § DO IT RIGHT #1 (fix the class, not the instance — the GHI must name the class)
- `AGENTS.md` § DO IT RIGHT 6h (verbatim quotes, not narrative reconstruction)
- `.gzkit/rules/gh-cli.md` (allowed `gh` commands)
- AGENTS.md § Defect-fix routing (the routing decision this GHI's evidence will feed)
- `AGENTS.md` § Execution Rules (operator PII — never in the GHI body)
