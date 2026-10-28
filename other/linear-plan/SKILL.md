---
name: linear-plan
description: "Turn an idea or existing plan into a draft feature/epic hierarchy and dependency-aware roadmap, reusing Linear outcomes, native OpenSpec requirements and the existing task board. Use for idea-to-roadmap planning, deciding feature boundaries, sequencing vertical slices, or selecting the next feature; draft first, publish only on explicit request."
compatibility: "Requires readable planning skills and repository context for grounded local planning; Linear capabilities only for scoped remote inspection/publication. Missing access blocks dependent operations, not independent drafts."
metadata:
  provenance: "Personal coordinator adapted from Matt Pocock's to-tickets and grill-me/grilling; attribution and MIT notice in references/sources.md."
---

# Linear plan

Coordinate outcome selection, hierarchy and sequence. Do not replace refinement,
OpenSpec authoring, task execution or Linear governance with another workflow.

## Authority and routing

Default: read-only planning and a draft in the response. Approval of an idea or
breakdown is not permission to save artifacts, publish tickets or start execution.
Honor narrower requests, including draft-only, description-only and no-status.

Resolve named skills through the runtime's native loader or discovered package
inventory; read the actual discovered `SKILL.md`. Reuse loaded instructions; never
assume installed paths, slash commands, implicit installation or recursive routing.

- Read `linear-management` for issue identity, workspace, taxonomy, attribution and
  mutation governance. Its status/readiness rules remain authoritative.
- Read `linear-refinement` when an outcome needs intent/acceptance refinement; reuse
  its evidence/brief conventions rather than repeating its interview or templates.
- Read `linear-openspec` for verified issue-to-change/requirement/task mappings and
  authorized reciprocal references. Unlinked planning needs no Linear issue.
- Only for requested local authoring, load `feature` for native proposal artifacts
  and `writing-plans` for executable tasks in the existing workflow lane.

Reading/routing to another skill does not widen this invocation's authority:
no automatic refinement writes, status reconciliation, Ready promotion, email,
implementation, commits, merges, pushes or workspace administration.
Missing instructions/tools block their dependent operations only. Continue grounded
independent drafts; report what was inaccessible and what remains unverified.

## 1. Inspect before interviewing

Capture the user's original idea, signals and requested scope. Establish the
repository/ref and applicable instructions, domain vocabulary, ADRs, native
OpenSpec schema, active/archived changes and specs, existing task board.
Discover available commands/capabilities before version-specific operations.

For Linear-backed planning, verify workspace/team/project and exact issue identity;
read relevant descriptions, comments, parent/children, relations and existing
project/milestone context. Search outcomes, aliases and source identities before
proposing new work, including terminal work where regression is plausible.
Complete relevant pagination or disclose incomplete coverage; never claim a complete
reuse/deduplication assessment from partial retrieval. Preserve evidence source,
observation date, revision and access limits; private signals stay in their audience.

Separate observed facts, approved decisions, proposals and inference. Follow
reachable references before asking for facts. Missing proof is not a failed check;
Done or checked tasks alone do not prove the required usable prerequisite output.

## 2. Resolve material decisions in bounded rounds

Frame beneficiaries, problem/current behavior, desired outcome, observable acceptance,
non-goals, constraints and acceptance authority. Unknowns remain explicit; do not
invent priorities, dates, estimates, owners or creator-as-approver.

Build a dependency tree of unresolved decisions. Ask only the current frontier:
prerequisites settled, researched facts available, answer changes scope, acceptance,
risk or sequencing. Ask at most three numbered questions per round, each with concise
options, trade-offs and a recommendation. Word yes/no questions so yes accepts the
recommendation. Defer dependent questions to a later round; preserve settled answers.

Research can continue beside independent frontier questions. A retrieval gap is not
a user decision. Stop interviewing when no material decisions remain, not when all
delivery proof, tooling, ownership or execution prerequisites have been satisfied.
If the user requests a draft before deciding, mark alternatives and blocked slices;
do not silently choose a material product trade-off or claim decision readiness.

## 3. Allocate outcomes, then slice

An **epic** is a long-lived capability area/coordinated outcome containing independently
accepted features. Reuse verified grouping, initiative or parent issue; it is not
automatically a new project, label or giant executable change. Parent acceptance is
separate from child acceptance. A **feature** is a coherent capability, normally one
native OpenSpec change. A **technical task issue** needs independent assignment and
verification value; do not mirror each `tasks.md` checkbox into a ticket.

Same unresolved outcome → attach/extend its canonical work. Partial overlap → state
which outcome/requirements each existing and proposed item owns; preserve original
signals and acceptance. Uncertain overlap remains a candidate match, not a silent
merge, Duplicate disposition or closure. Avoid ceremonial hierarchy for one small
feature. Reuse existing projects/milestones; propose new admin entities only, unless
separately authorized for exact creation.

Prefer tracer-bullet vertical slices: each produces independently observable behavior
through the necessary layers and checks. Do not split into arbitrary schema/API/UI
phases or add unrequested prefactoring/compatibility scaffolds. A mechanical wide
refactor should use a clean atomic cutover when feasible. Use staged expand-contract
only with repository-approved rollout justification when an atomic green cutover is
infeasible; include removal of the obsolete surface in the final slice.

## 4. Map canonical authority and derive the roadmap

OpenSpec proposal/requirements own intent; `tasks.md` owns proposal execution state.
The repository's declared task board owns its canonical task state; preserve the repository's binding
between board entries and proposal tasks. Linear owns outcome/accountability,
relations and acceptance evidence. The roadmap is a derived view, not another mutable
checklist or task scheduler. Never create an OpenSpec wrapper just for a portfolio
roadmap, standalone task ledger, or issue solely to link a plan.

Map many-to-many issue ↔ change ↔ requirement/scenario ↔ task slices. Preserve verified
IDs/URLs, exact change path, requirement identifiers, task heading/item text (stable
IDs where available), scope allocation, source revision and acceptance/evidence
boundary. Do not substitute similar titles or broad parent links for an exact slice.
For proposed items use explicitly labeled draft keys such as `F1`; these are not
Linear/OpenSpec IDs. Unknown or not-yet-authored references stay explicit, never
fabricated links. Completing one mapped slice does not complete the whole issue.

Build a dependency DAG from real prerequisites and their required outputs, not list
order, shared files or assumed capacity. Inspect cycles, absent outputs, satisfied
blockers and stale edges. A recorded blocker already supplying the required accepted
output no longer gates the slice; preserve the evidence, not an invented dependency.
Explain unresolved cycles/alternatives instead of presenting an executable ordering.

Sequence **now / next / later** with meaningful entry and exit evidence. Keep distant
features coarse; detail executable tasks only for selected near-term approved scope.
Order is not a date, staffing or delivery commitment. Shared-file conflicts are
coordination constraints, not product prerequisites. Ask unresolved product trade-offs
rather than inventing priorities; distinguish proposal phase from observed tracker state.

## 5. Save only the explicitly authorized scope

**Local authoring requested:** after material decisions are settled, reuse/extend the
matching native change via `feature`; use `writing-plans` for its canonical tasks or
bounded existing board contract. Follow discovered schema and native validation.
Report authored artifacts separately from a response draft. Native validity, logical
readiness, observed Linear state and implementation permission remain distinct.

**Linear publication requested:** preview exact targets and field/content/relation
patches, including proposed creates and proposed versus verified links. Verify the
represented principal and AI-generated planning attribution under governance. Refresh
identity, scope, status, ownership, relations and applicable metadata; reconcile drift
and preserve newer/original content before writing. Inspect relevant automation effects.
Serialize only authorized writes; create genuine blockers before dependent native
relations need their IDs. Do not automatically create as Ready or change unrelated
states/owners/labels. Missing valid metadata or principal blocks that write, not drafts.

Read back each affected record's exact saved content, fields and relations. A success
response without read-back is unverified; preserve verified partial successes. After
failure/ambiguous success, inspect current state before retrying or creating again;
never replay a stale patch or duplicate an already-created outcome. Reciprocal links
require authority and observed success at both destinations. Unpublished artifacts or
unavailable resolvable URLs remain proposed, not falsely saved or reciprocal.

## 6. Return the usable planning packet

Keep small plans small; combine sections when useful, omit empty ceremony. Return:

- Outcome, non-goals, acceptance authority; evidence/retrieval limits and observed reuse.
- Hierarchy plus exact mapping, with draft keys visibly distinct from verified IDs:
  `Issue/key | Outcome slice | Change/path@revision | Requirement/scenario | Task/board ref | Acceptance/evidence boundary`.
- Dependency-aware roadmap:
  `ID/draft key | Deliverable | Canonical change/board ref | Blockers + required output/why | Now/next/later; entry → exit evidence | Owner (unknown if unrecorded)`.
- Selected next feature: observable success/failure acceptance, verification recipe,
  exact requirements/tasks refs or their not-yet-authored state; unresolved material
  questions (or explicit none), execution prerequisites and concrete next gate.
- Exact proposed writes versus attempted writes and saved read-back evidence; say
  draft-only when nothing was saved. End with one concrete next action within authority.

For upstream adaptations and license obligations, read package-relative
[references/sources.md](references/sources.md); it is attribution, not runtime authority.
