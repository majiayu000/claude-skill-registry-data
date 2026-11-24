---
name: review-repo
description: Whole-repository review. With no focus, maps where to engage or tread carefully, including tech-debt hotspots. Focuses for deep reviews are architecture, dead-code, value, and namespace. Creates tickets only with authority. Never changes code.
model: opus
---

# Review-Repo — Reviewing a Codebase as a Whole

One entry point for repository-wide review. It works in two shapes:

- **`/review-repo [scope]`** gives the **orientation map**. This is the strategic pass for when you've inherited a repo, are evaluating a FOSS project, are onboarding a teammate, or are deciding where to invest in your own project. It covers breadth first, with evidence for every claim.
- **`/review-repo <focus> [scope]`** gives a **focused review**, going straight to one deep review:

| Focus          | Question it answers                                  | Agent                                          |
|----------------|------------------------------------------------------|------------------------------------------------|
| `architecture` | Where should everything live?                        | `swe-arch-reviewer`                            |
| `dead-code`    | What can be deleted, and how sure are we?            | `swe-dead-code-auditor`                        |
| `value`        | Which requirements cost more than they're worth?     | `swe-value-engineer`                           |
| `namespace`    | Can a newcomer find things from the file tree alone? | `swe-namespace-reader`, `swe-namespace-canary` |

Several focuses can be named together (`/review-repo value architecture`); they run in dependency order (§Focused Reviews). A focus naming another review skill (`security`, `test`, `perf`, `a11y`, `release`) is routed to that skill.

**This skill never changes code.** It produces maps, findings, and ticket proposals. Removal and restructuring happen in `/implement` against the tickets, or in `/refactor`.

## Philosophy

**Observation before interpretation.** The map follows an OODA cadence (Observe, Orient, Decide, Act) with strict phase gates. Observe collects signals without verdicts, and interpretation begins only after observation is complete. This counters the most common failure of informal review: fixating on the first file opened and building a distorted model from it.

**"Good" is relational, not absolute.** A 34% test coverage means something different in a research prototype than in an OSS library with external consumers. Calibration is anchored in **reference classes** (`references/classes/`). The repo is classified first, and each dimension is evaluated against that class's expectations. The classification is cited and overridable.

**Every claim carries evidence.** A finding without a `file:line` citation or a tool-output reference is an assertion. It is dropped or demoted to the Coverage Manifest. This is enforced structurally (§Evidence Discipline).

**Named unknowns beat silent unknowns.** The Coverage Manifest is first-class output. Tools that couldn't run, signals that couldn't be computed, and questions that couldn't be answered are named with their reasons.

**Breadth first, depth on demand.** The map is the wide, shallow pass. The focused reviews and sibling skills are the deep, narrow passes. The map decides which deep passes are worth their cost; there is no fixed sequence.

## Cognitive Failure Modes This Skill Countermands

- **Inheritor's paralysis and availability bias:** fixating on the first file opened. *Countermeasure: a systematic Observe phase over fixed collection points before any interpretation.*
- **Unknown unknowns:** not knowing what you don't know. *Countermeasure: the Coverage Manifest.*
- **Premature closure:** a verdict before the evidence is in. *Countermeasure: phase-integrity gates. Orient cites only Observe; Decide cites only Orient.*
- **Expert deference:** accepting prior-author choices unexamined. *Countermeasure: differential-diagnosis classification, and focused reviews that question structure (architecture) and requirements (value) directly.*
- **Free-floating adjectives:** "health: good" with no reference point. *Countermeasure: reference-class rubrics.*
- **Confident false positives:** "no references found" taken as proof of death. *Countermeasure: the dead-code focus surveys dynamic dispatch before tiering anything.*

The practitioner traditions behind these: OODA (Boyd), medical differential diagnosis, home inspection (ASHI severity tiers), marine surveying (reference-class calibration), technical due diligence, behavioral code analysis (Tornhill), and value engineering (Miles, GE).

## Phase 0 — Preflight

**Parse the invocation.** A recognized focus word selects §Focused Reviews; anything else is scope. With no focus, run the map.

**Elicit the context** (map only). Ask one question; do not guess:

> What's the context for this review?
> 1. Inheriting a work repository — taking over maintenance or ownership
> 2. Evaluating a FOSS project — for adoption, contribution, or dependency
> 3. Revisiting my own repo — strategic overview of current state
> 4. Onboarding a teammate — generating a map for someone else
> 5. Other — briefly describe

The context is a load-bearing input. It shapes classification and the Decide phase.

**Elicit authority** (map only) in the same exchange. There are two grants, both defaulting to no:

| Grant             | Question                                                        | If granted                                                  |
|-------------------|-----------------------------------------------------------------|-------------------------------------------------------------|
| Follow-up reviews | May I run the deeper reviews the map calls for?                 | Phase 5 runs them; without it, Phase 4 only recommends them |
| Tickets           | May I create tickets at or above a severity floor? Which floor? | Phase 5 creates them; without it, they're proposed          |

Ask the ticket question only if follow-ups are granted. Mention that some follow-ups (notably `/review-security`) are heavy. The floor defaults to High. Granting tickets *is* the approval to create them.

**The floor across scales:** High = CRITICAL/HIGH, ASHI Safety Hazard/Major, release BLOCKER. Architecture, dead-code, and value items are always proposed, never auto-created.

**Determine scope.** The default is the whole repo. Honor a named directory or module in every phase. If the repo is very large (>100k LOC or >10 top-level subsystems), ask whether to scope down.

**Abort if:** not a git repository, or no source files in scope. Missing tooling is not a reason to abort; record it in the Coverage Manifest.

## The Map

```
Phase 1 OBSERVE   signals only, cited, no verdicts; Coverage Manifest
Phase 2 ORIENT    classify → rubric per dimension → severity tiers →
                  cross-cutting synthesis → locate the interest
Phase 3 DECIDE    2-4 engagement options for the context, each cited
Phase 4 ACT       top 3-5 next steps; focused reviews / skills to run
Phase 5 FOLLOW UP (with authority) run them, consolidate, ticket
```

### Phase 1 — OBSERVE

Collect signals. **Interpretation is not allowed in this phase.** Output is neutral and factual ("X is present / absent / at value Y"). Every signal carries a citation: a `file:line`, a tool invocation and its output, or an explicit "could not be collected".

**Repo shape:**
- Languages and LOC by language (`tokei`, `scc`, `cloc`; fall back to counting file extensions).
- Top-level layout (`tree -L 2 -d`).
- Entry points (framework conventions and manifest declarations).
- Build system and package manifests.

**Git history:**
- Age (first and latest commit).
- Cadence (commits per month).
- Contributors (distinct authors in the last 12 months).
- Churn concentration (most-committed files).
- Bus-factor proxy (single-author core files).

**Change cost** (where debt charges interest; see Step 2f):
- **Per-file complexity:** `scc --by-file -f json` (its `Complexity` field), or `lizard` for per-function CCN. Fall back to code-line count, and record which measure was used.
- **Change frequency:** commits per file over 12 months (`git log --since="12 months ago" --no-merges --name-only --pretty=format: | sort | uniq -c`). Exclude generated files, lockfiles, vendored code, CHANGELOGs, and commits touching more than ~25 files.
- **Hotspots:** the top ~10 files by complexity × change frequency, with both factors recorded.
- **Change coupling:** file pairs that changed together in ≥5 commits and in ≥half of either file's commits, with the same exclusions. Record whether a static dependency links each pair.
- **Fix density** in hotspots: the share of commits whose messages read as fixes (`fix`, `bug`, `revert`, `regression`, `hotfix`).
- **History adequacy:** fewer than ~50 commits in the window, or squash-dominated history, is weak history. Record it.

**Tooling** (best effort; record absences):
- Test framework, and the test-to-code LOC ratio.
- Coverage reports, parsed if present.
- Lint and static-analysis config.
- CI configuration.
- Dependency audit (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`, …).
- Dependency staleness.
- Secrets scan (tracked `.env` files, credentials in source, private-key headers).

**Documentation:**
- README presence and length.
- Inline comment density in core modules (sampled).
- Architectural docs and ADRs.
- CHANGELOG recency.
- Contributing guide and templates.

**Coverage Manifest entries:** what was attempted, why it yielded nothing, and whether the user could supply it.

**Output:** an Observation Record with referenceable IDs (`O1`, `O2`, …).

### Phase 2 — ORIENT

**2a. Classify (differential diagnosis).** Load `references/classes/`. For each candidate class, gather evidence for and against from the Observation Record and the context:

> **Candidate: `production-service`**
> For: `O12` (Dockerfile with runtime target), `O17` (CI gates merges), `O8` (>5 contributors)
> Against: `O4` (no deployment artifacts, no on-call docs)
> Confidence: Low

Pick the best fit and hedge explicitly ("Classified as `solo-utility` (medium confidence)… override if you see it differently"). For a hybrid repo, apply each class's rubric where they differ and flag the hybrid.

**2b–2c. Apply the class rubric.** Read `references/classes/<class>.md`. Place each of the five dimensions (test health, dependency health, CI/automation, documentation, architecture hygiene) at Foundational, Adequate or Strong, with cited evidence and the gap to the next level.

**2d. Severity-tier findings.** ASHI tiers per `references/severity-tiers.md`: Safety Hazard / Major / Minor / Cosmetic. Severity is intrinsic to the finding. Lead with Safety; aggregate Cosmetic.

**2e. Cross-cutting synthesis.** Look for patterns that no single dimension reveals:
- Divergent conventions at module boundaries.
- Duplicated types.
- Dependency inconsistency across sub-packages.
- Client and server models that diverge.
- Documentation drift.

These are often the highest-leverage findings in the review.

**2f. Locate the interest.** A snapshot shows *cruft* (Fowler); change history prices it as *debt* (Cunningham's interest, Tornhill's method). Read the change-cost signals as a quadrant:

| Complexity | Change frequency | Reading                                                                                  |
|------------|------------------|------------------------------------------------------------------------------------------|
| High       | High             | **Debt being paid**: every change costs interest. Engage here first                      |
| High       | Low              | **Dormant cruft**: ugly but stable; costs nothing until touched. Usually leave it alone  |
| Low        | High             | Active code: usually healthy; act only if 2e flagged it                                  |
| Low        | Low              | Settled. Ignore                                                                          |

- **Corroborate before calling it debt.** Churn has innocent causes. A hotspot counts as debt only when its fix density is high or 2e found divergence in it.
- **Hidden coupling.** A change-coupled pair with no static dependency is a hidden contract. It is the strongest signal for the `architecture` focus.
- **Dormant cruft is a finding.** "Leave it alone" is a strategic call the user can act on.
- **Weak history means named uncertainty.** Don't rank hotspots on weak history; say so.

**2g. Coverage Manifest.** Carry it forward and add to it.

**Integrity check:** every Orient claim cites Observation IDs. An uncitable claim is dropped, demoted to the Coverage Manifest, or flagged "interpretation, no direct evidence".

### Phase 3 — DECIDE

Generate 2–4 options for the user's context, each citing the Orient findings that support or complicate it. The user picks; the skill does not.

- **Inheriting:**
  - Adopt as-is with compensating controls.
  - Invest in remediation before extending.
  - Carve out a safe subset to work in.
- **Evaluating FOSS:**
  - Adopt, naming the accepted risks.
  - Adopt with wrappers or version pinning.
  - Don't adopt, naming the disqualifying findings.
  - Fork and stabilize.
- **Own repo:**
  - Continue the current trajectory.
  - Rebalance investment across dimensions.
  - Promote the repo to a higher-standards class.
- **Onboarding:**
  - Start in module X.
  - Read the docs in this order.
  - Known hazards to brief on.

### Phase 4 — ACT

Give the top 3–5 next steps, prioritized by severity × relevance to the context. Each is either a specific action with `file:line` pointers, or a deeper review with a scoped argument:

| Finding type                               | Route to                            | When                                                          |
|--------------------------------------------|-------------------------------------|---------------------------------------------------------------|
| Module boundaries, coupling                | `/review-repo architecture <scope>` | Architecture hygiene at Foundational, cross-cutting coupling  |
| Hidden change coupling                     | `/review-repo architecture <scope>` | Change-coupled pairs with no static dependency (2f)           |
| Dead or unreachable code                   | `/review-repo dead-code <scope>`    | Dead-code signals in Observe, or before any architecture pass |
| Machinery out of proportion to the product | `/review-repo value <scope>`        | Recommend only; its trades need the product owner             |
| Confirmed hotspots (debt being paid)       | `/refactor <module>`                | Recommend only; it changes code                               |
| Test coverage or quality gaps              | `/review-test <scope>`              | Test health at Foundational, or specific gaps                 |
| Security findings                          | `/review-security`                  | Safety-tier security findings                                 |
| Performance-sensitive code                 | `/review-perf`                      | Hot paths with no evidence of their cost                      |
| Accessibility (web)                        | `/review-a11y`                      | Web UI present                                                |
| Documentation gaps                         | `/tidy-docs`                        | Documentation at Foundational                                 |
| Pre-release readiness                      | `/review-release`                   | The user is preparing to publish                              |

Route only when the deeper pass does exactly what's needed at the depth warranted. Recommend shallow fixes directly.

### Phase 5 — FOLLOW UP (only with authority)

**Without follow-up authority,** stop after Phase 4 and offer to run the recommendations.

**With it,** run the deeper reviews the map calls for, each scoped to where its findings point. Use judgment, not a checklist: every review that plausibly applied and didn't run gets a one-line reason in the report.

- **Candidates:** the `dead-code`, `architecture`, and `namespace` (audit mode) focuses (run per §Focused Reviews), `/review-security`, `/review-perf`, `/review-a11y`, `/review-test`, `/review-release`.
- **`/review-release` runs report-only:** stop after its findings presentation. It applies no fixes and makes no commit, so this skill still changes no code.
- **Order:** dead code before architecture; release readiness last.
- **Never run here:**
  - `/refactor` and `/implement`, because they change code.
  - The `value` focus, unless intent asks for it, because its trades are product decisions.
  - The `namespace` focus in search mode, because it needs the operator. Audit mode may run when the map's findings point at legibility.

**Tickets.** Each deep review with a ticket step ends with a ticket proposal. With ticket authority, approve proposals at or above the floor and decline the rest, recording them, per [`references/advisory-tickets.md`](../../references/advisory-tickets.md). Without it, decline all of them in-run and propose one consolidated set at the end, ordered by severity, created only on approval. Skills with no ticket step (`/review-perf`, `/review-a11y`, `/review-release`) feed findings straight into the consolidated set; with ticket authority, create those at or above the floor directly.

**Consolidate.** Dedupe findings that several reviews raised (a confirmation is not a second finding). Reconcile them with the map; where a deeper review contradicts the map, the deeper review wins and the contradiction is reported.

**Escalate rather than decide** when a fix would need a breaking change, or two reviews contradict each other on the same code. For long runs, keep `REVIEW_REPO_STATE.md` (gitignored) with the pinned intent and the reviews already run, so the run can resume after compaction.

## Focused Reviews

Each focus runs one fresh agent and follows the same protocol:

1. **Scope** from the invocation (the whole repo by default). Pass along any useful prior output, such as an earlier focus's findings or the map's hotspots.
2. **Spawn** the agent.
3. **Present** its findings as described per focus below.
4. **Iterate** with the operator. They may know things the agent can't see; their knowledge is evidence. When the caller is an orchestrator, it shapes the plan with its own judgment per [`references/autonomy.md`](../../references/autonomy.md).
5. **Offer tickets** per [`references/advisory-tickets.md`](../../references/advisory-tickets.md), creating them through [`references/trackers.md`](../../references/trackers.md). Declining is a valid outcome; the analysis stands as a planning artifact.
6. **Summarize:** scope, finding counts, items dropped in iteration, tickets created (with the skill each recommends), and the next step.

An **honest zero** is a valid result for every focus. Report it and stop. If the agent fails, retry once and then surface the error. If the tracker is unavailable after approval, show the approved set so the tickets can be created by hand.

**Several focuses together** run in this order, each receiving the previous one's output:

1. **Value.** Restructuring a requirement you're about to delete is wasted work.
2. **Dead code.**
3. **Architecture.** It receives the dead-code audit as input instead of re-cataloging dead code.
4. **Namespace.** In search mode, the architecture blueprint is seeded as a round-1 candidate, so the analyst's proposal is tested by the measurement. Where the two disagree, prefer the measurement.

### `architecture` — target blueprint

**Prompt `swe-arch-reviewer`** with the scope, the auditability ceiling (the project's stated file-size limit, or 500 lines), any dead-code audit already produced, and the map's hidden-coupling pairs. Ask for a target blueprint that covers every module, existing and proposed.

**Present four things:**
- **(a) The noun analysis:** the frequency table and the per-noun namespace evaluation. This is the analytical foundation.
- **(b) Proposed changes** with their rationale, grouped as mechanism downgrades, renames, moves, absorptions, dissolutions, and new modules.
- **(c) No-change items** with their domain justifications. The operator may disagree, or spot a module the agent missed.
- **(d) Behavior-altering changes**, from the agent's "Behavior-Altering Changes (requires approval)" section, flagged for approval. They escalate to the operator rather than becoming tickets automatically.

Iterate until the operator is satisfied. Architectural decisions are consequential, so don't rush this step.

**Tickets:** one per blueprint item, grouping items when that makes the work cohesive (for example, "dissolve `helpers.go`" is one ticket, not six). Each ticket has:
- Title.
- Rationale and the specific moves.
- Acceptance criteria (symbols moved, files removed, tests pass).
- A recommended skill: `/implement` for changes within an existing module, `/scope` then `/implement` for new modules or cross-module moves.

### `dead-code` — calibrated audit

**Prompt `swe-dead-code-auditor`** with the scope. It surveys dynamic dispatch first, determines the reference roots (an application's entry points, or a library's public API), runs the language tooling that's available, and tiers every finding PROVEN, LIKELY or UNVERIFIABLE with evidence.

**Present the calibration first:** the dynamic-dispatch survey and the roots determination, because they tell the operator how far to trust everything below. Then the findings by category, each with its tier, evidence, and estimated lines. Show intentionally retained items (suppressions, decision-record-protected code) separately; they are not proposed for removal.

**Tickets:**
- One removal ticket per subsystem or category when findings cluster.
- One sweep ticket for scattered PROVEN findings, worked with `/implement`.
- **UNVERIFIABLE findings go into a verification ticket**, listing what a human must confirm, never into a removal ticket.

### `value` — trade menu

**Prompt `swe-value-engineer`** with the scope and any context worth having: an architecture mechanism audit (its `serves:` citations are cost attribution already done), or operator suspicions, which are hypotheses to check, not conclusions to confirm. It discovers requirements across provenance tiers (documented, pinned by tests, inferred from behavior), attributes cost to them, and returns a trade menu ranked by leverage.

**Present the full menu.** For each trade, the operator must be able to see, without asking:
- The current commitment and its provenance.
- The proposed relaxation.
- The concrete user-visible change.
- What dissolves.
- The estimated savings, presented as estimates.
- Any flags: core requirement, correctness, or security.

Also present the drift observations: documented requirements the code no longer honors.

**The operator rules on each trade.** These are product decisions.
- **Never advocate.** The menu is a price list. If asked for a recommendation, give one and label it as opinion.
- Answer questions from evidence, and revise estimates the operator's spot-check disproves.
- Record each ruling: approved, declined, or deferred.
- When the caller is an orchestrator, trades flagged core-requirement, correctness or security go to the human (andon cord). They are never ruled on autonomously.

**Tickets, for approved trades only. The amendment leads.**
- The first acceptance criterion amends the record that carries the old requirement: the design doc, ADR, README claim, or spec. For an inferred requirement, record the newly confirmed intent wherever the project keeps decisions.
- The remaining criteria cover what dissolves.

An approved trade that changes only code is a time bomb: the next agent to read the unamended requirement will faithfully rebuild the machinery.

### `namespace` — measured legibility

**Read [`references/namespace.md`](references/namespace.md) and follow it.** It holds the instrument: blind probe generation, sighted ground-truth pinning, the reader fleets, the Laws of the Instrument, the finding classes, and search mode. It is kept out of this file because only this focus needs it.

- **Audit** is the default: one probe battery against the actual tree (~10–15 agents).
- **Search** runs only when the invocation says `search` (`/review-repo namespace search`) **and** the operator confirms the cost (millions of tokens) and a round cap. Its calibration checkpoints need the operator, so it never runs unattended.
- **Tickets:** audit findings follow the shared pattern. A search champion becomes one migration ticket that can be worked without this conversation. It includes the tree, the complete old→new mapping (including files deliberately kept), spec changes, sequencing, and acceptance criteria.

## Evidence Discipline

These rules are structural, not stylistic:

- **Every claim cites evidence.** That means an Observation ID (in the map) or a `file:line` or tool-output reference. Drop or demote a claim without one.
- **Phase integrity.** Orient cites Observe; Decide cites Orient; Act cites Orient or Decide.
- **Self-check before delivery.** Look for uncited adjectives, "the author should…" without a cited basis, and verdict words in Observe.

## Agent Coordination

The map runs in the main instance; OODA synthesis needs one context. Use subagents narrowly:

- **Observe scouts** (optional, parallel, for large repos): discrete signal-collection tasks that return structured signals, not prose.
- **Focused consultation** (optional): a fresh subagent briefed on one dimension that needs a deeper look than the map can afford. It returns a rubric placement with evidence.
- **Focus agents**, per §Focused Reviews: always fresh instances.

Do not routinely spawn per-language consultants.

## Output Format

Inline markdown by default.

**Map**, in order:
1. **Context:** the review context, scope, and classification (with evidence and how to override it).
2. **Observation Record:** compact tables with IDs.
3. **Findings:** rubric placements, severity-tiered findings, cross-cutting synthesis, and where the interest is paid.
4. **Coverage Manifest.**
5. **Strategic Options.**
6. **Next Steps.**
7. **Follow-up results** (Phase 5 only): per review, its scope, headline findings, and tickets; reviews not run, with a reason for each; contradictions and breaking-change findings awaiting the user.

**Focused review:** the presentation described for that focus, then the summary from protocol step 6.

## What This Skill Is Not

- **Not a code changer.** It produces maps, findings, and tickets, and never commits code.
- **Not a grade.** There is no overall score.
- **Not a diff review.** For a diff, `/implement` and `/bug-fix` run the correctness gate. For a diff produced elsewhere, use Claude Code's built-in `/code-review`.
- **Not a substitute for the specialist skills** (`/review-security`, `/review-test`, …), which it routes to.
- **Not a substitute for reading the code.** It helps you engage with the code *well*.
