---
name: aid-research
description: >
  Investigate an open technical question and return a verified answer in one pass --
  evaluating options, or running an isolated feasibility spike if you explicitly authorise
  one. Use this skill when a decision is blocked on something nobody has established yet. It
  presents the answer, the conclusions both positive and negative, any contradictions with
  the reason for each, and the gaps; you decide. The Knowledge Base and the project source
  are the authoritative grounding; web sources are encouraged but supplementary, cited with
  a URL and access date, and a contradiction between them is surfaced rather than silently
  resolved. For open-ended exploration of a problem space rather than a specific question,
  use `/aid-brainstorm`.
allowed-tools: Read Glob Grep Bash Shell Terminal Write Edit Agent
argument-hint: "<question> -- an open technical question to investigate"
---

# Research (investigate now, resolve nothing)

`/aid-research` investigates an open question **now** and returns a **curated, verified
answer** -- the complete picture, presented clearly. It is `aid-ask`'s bigger
sibling: where `aid-ask` *retrieves an answer that already exists* in the project's
context (one read-only pass, no work folder), research *builds a new judgment* for a
question the available context can't already answer -- with option evaluation, external
context, an optional authorized spike, verification, and a human-facing presentation.

- **Resolves nothing.** No "I recommend X." It lays out conclusions (+/-), conflicts, and
  gaps; the user decides.
- **Not a numbered pipeline phase**; it does not route to `/aid-execute`.

State machine: **INTAKE -> INVESTIGATE (-> PROPOSE-SPIKE?) -> VERIFY (loop) -> PRESENT
[human resolves] -> HANDOFF? -> DONE**. Print the `[State: NAME] -- {purpose}` entry line
on each state.

---

## State: INTAKE

1. **Require a question.** If the argument is empty, ask one bootstrapping question ("What
   do you want investigated?") and wait.
2. **Pick the path (question scope):**
   - **Fast path** -- a concrete, well-scoped question with clear evaluation criteria
     ("Is lib X compatible with our Node 24 build?", "Postgres vs SQLite for use-case Y
     against criteria A/B/C") -> investigate immediately.
   - **Guided path** -- vague / broad / underspecified ("research our DB options") -> ask
     2-3 scoping questions first (narrow it), then investigate.
3. **Classify complexity (sets model + effort):** simple (bounded question, a few docs,
   <=1 web source) -> `aid-researcher` at **sonnet / medium**; standard/complex (broad
   options analysis, deep traversal, many web sources, a spike) -> **opus / high**.
   Verifier tier is always >= producer tier.
4. **Consult the Work Initiation Gate, then allocate the work folder + STATE.** First run
   the gate (`.aid/runtime/templates/work-initiation-gate.md`):
   `bash .aid/runtime/scripts/works/enumerate-works.sh` (main tree + every git worktree).
   Empty -> allocate below, no prompt. Works exist -> ask new-vs-continuation with the
   enumerated list; on **continuation** route to the chosen work's resume door and STOP
   (allocate nothing); on **new work**: resolve `<work-id>` as `work-{NNN+1}`, where `NNN`
   is the maximum `work-NNN` numeric prefix across every record the enumeration above
   already returned (cross-worktree by construction -- never a local `.aid/works/` glob;
   gate `§ 3a` step 1); create and enter the worktree per the gate's `§ 3a` step 2
   (`worktree-lifecycle.sh create <work-id> <name>`, STOP on a non-zero exit or empty path,
   else enter the resolved path); **only then** allocate: `.aid/works/<work-id>-<slug>/`
   under `.aid/works/`; slug from the question. Copy
   `.aid/runtime/templates/work-state-template.yml` to
   `.aid/works/work-NNN-<slug>/STATE.yml`; write opening frontmatter (`pipeline.path: lite`,
   `initiator: aid-research`, `lifecycle: Running`, `active_skill: aid-research`,
   `started`/`updated`). Do NOT drive the 7-phase `phase` scalar. Associate a git worktree
   only if a spike is later authorized (INVESTIGATE).

**Advance:** INVESTIGATE.

---

## State: INVESTIGATE

Dispatch **`aid-researcher`** (clean context, model+effort from INTAKE Step 3) to gather
and curate the evidence:

- **Two-tier grounding (enforced):** read the KB (`.aid/knowledge/`) + the project source
  as the **authoritative** base; enrich with external/web sources as needed, **cited with
  URL + access date**. Every project claim cites a KB doc or `file:line`; every external
  claim cites a URL+date.
- It writes a structured `RESEARCH.md` into the work folder (see [Response shape](#response-shape)).

**Spike escalation (conditional, human-authorized).** Default is **analytical-with-
handoff** -- no code is written. If the researcher determines a gap genuinely cannot be
closed on paper, it returns a **spike proposal** instead of a final answer, and the skill
enters **PROPOSE-SPIKE**: present *what* it would build, *where* (isolated in the work
folder / opt-in worktree, never touching production), and *what it would learn*, then STOP
for the user's decision. On **authorization** -> re-dispatch `aid-researcher` to write the
throwaway spike (isolated), fold the finding into `RESEARCH.md`, continue. On **decline**
-> proceed analytically and state the resulting limit in the Gaps section.

**Advance:** VERIFY.

---

## State: VERIFY  (who reviews the researcher)

1. **Mechanical grounding check** (no dispatch): every project claim carries a KB/source
   cite; every external claim a URL+date; the **Conflicts** and **Gaps** sections exist
   (empty-but-present is allowed; silently-omitted is not).
2. **Adversarial verification** -- dispatch a clean-context **`aid-reviewer`** to check
   `RESEARCH.md`: claims grounded and correctly attributed; conclusions evidence-backed
   and **not overstated into resolutions**; every KB<->web conflict surfaced with its
   reason; no material angle of the question left silently unaddressed. It writes a
   review-quality 7-column ledger (`reviewer-ledger-schema.md`) to
   `.aid/.temp/review-pending/<work>-verify.md`.
3. **Grade the response:** `bash .aid/runtime/scripts/grade.sh --explain <ledger>`. Not
   clean -> loop back to INVESTIGATE for the researcher to revise. **Circuit-breaker: 3
   cycles** -> write `.aid/works/{work}/IMPEDIMENT-research.md`, set STATE `lifecycle: Blocked`,
   surface it.

(Single grade -- the response *is* the deliverable; there is no separate target artifact.)

**Advance:** PRESENT.

---

## State: PRESENT  (always a hard stop -- the user resolves)

Set STATE `lifecycle: Paused-Awaiting-Input`. Present `RESEARCH.md` **clearly and simply**:
the in-depth answer, conclusions (positive **and** negative), conflicts/contradictions
**with their reasons**, and gaps. Assert no resolution -- the user decides. Negatives and
gaps are first-class, never buried under positives.

**Advance:** HANDOFF (optional) then DONE.

---

## State: HANDOFF  (optional; printed suggestions only)

Offer the natural next steps as **printed suggestions**, each requiring the user to act:
record an ADR (`/aid-document-decision` -> once landed, `/aid-create-document`), update the
KB (`/aid-update-kb`), act on a conclusion (`/aid-create*` / `/aid-update*`), or comment on
a source ticket (`/aid-update-ticket comment [<connector>:]<ticket-id> <text>`). Never
auto-invoked; never a resolution.

**Advance:** DONE.

---

## State: DONE

Set STATE `lifecycle: Completed`, `updated` now, append a `## Lifecycle History` row. Keep
the work folder (`RESEARCH.md`, any spike scratch, the verify ledger) as the audit record.

---

## Response shape

`RESEARCH.md` (the "clear + simple" deliverable), sections in order:

1. **Question** -- the query, as scoped/investigated.
2. **Answer** -- the in-depth, curated response.
3. **Conclusions** -- positive *and* negative, each evidence-backed and cited.
4. **Conflicts & contradictions** -- especially KB<->web, each with **its reason** and both
   citations; `none` if there were none.
5. **Gaps** -- what could not be answered / stays uncertain (incl. any limit from a
   declined spike); `none` if none.
6. **Sources** -- KB docs + `file:line` (authoritative) and external `URL (accessed
   YYYY-MM-DD)` (supplementary), clearly separated.

---

## Constraints

- **Resolves nothing** -- curated information + conclusions/conflicts/gaps; never a
  directive.
- **Two-tier grounding, enforced** (VERIFY step 1 + the researcher brief): KB+source
  authoritative, web supplementary + cited; KB<->web contradictions surfaced with reasons,
  never silently resolved.
- **Clean context** -- INVESTIGATE and VERIFY never share context.
- **Verification is always a sub-agent dispatch** (`aid-reviewer`), never inline.
- **Human final say before any commit** -- a spike (code), a KB update, a decision doc, or
  a ticket comment happens only on explicit authorization; presenting the answer is not a
  commit.
- **Tracking:** write STATE `lifecycle` at every transition.
