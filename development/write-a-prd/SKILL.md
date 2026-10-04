---
name: write-a-prd
description: "Primary pipeline shaping step after /research and before /prd-to-issues. Use when the problem is understood well enough to turn into a bounded PRD issue. May invoke /design-an-interface or /api-design-review when interface or contract uncertainty remains. Not for discovery, decomposition, or implementation-ready work."
sources:
  primary:
    - "Shape Up — Ryan Singer"
  secondary:
    - "A Philosophy of Software Design — John Ousterhout"
    - "Software Estimation — Steve McConnell"
    - "Software Requirements — Karl Wiegers & Joy Beatty"
    - "Thinking in Bets — Annie Duke"
    - "Thinking in Systems — Donella Meadows"
    - "Writing Effective Use Cases — Alistair Cockburn"
---

# Write a PRD

This skill produces a shaped pitch — a PRD that's rough enough for builder judgment, solved enough to ship, and bounded by an explicit time appetite. Follow the steps below, adapting depth to the work but not skipping the checks that establish appetite, current code reality, institutional knowledge, and handoff readiness.

> **One question per turn.** Throughout this skill's interview, ask one question at a time and wait for the user's answer before asking the next. Never present multiple questions in a single message, even when they are short.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

## Invocation Position

This is a primary pipeline skill that normally follows `/research` and precedes `/prd-to-issues`.

Use `/write-a-prd` when the problem is understood well enough to shape a bounded solution and turn it into an implementable pitch.

Do not start here when the problem is still ambiguous enough that discovery should continue in `/shape`, when technical reality has not yet been verified in `/research`, or when the user already has a shaped PRD and wants decomposition or execution instead.

## Process

### 1. Get the problem as a specific story

Ask the user to describe the problem as a **specific story** showing why the status quo fails for a real user. Push back on abstract feature requests ("we need better X") until they're grounded in concrete friction ("when a user tries to do Y, they hit Z because...").

A good problem statement is one scene — one actor, one attempt, one failure. If the user gives you a solution first ("I want to add a webhook system"), ask: "What's happening today that's painful enough to justify building this?"

### 2. Set the appetite

Before any solution design, establish the time budget: **How much is this problem worth?**

- **Small batch**: 1-2 weeks of implementation time
- **Big batch**: up to 6 weeks of implementation time

The appetite is a constraint, not an estimate. It answers "how much time are we willing to spend?" — not "how long will this take?" If the problem doesn't fit the appetite, narrow the problem, don't expand the budget.

The appetite is a **target** — how much time the business is willing to spend. It is not an **estimate** — an analytical forecast of how long the work might take — and it is not a **commitment** — a promise to deliver by a date. If the current estimate exceeds the appetite, reshape the solution rather than silently converting the appetite into a commitment.

The appetite shapes everything downstream: which user stories are must-haves vs. nice-to-haves, how many rabbit holes are acceptable, and how aggressively scope gets hammered.

**Container milestone for big-batch work.** If the appetite is big-batch (6 weeks), ask whether a GitHub milestone should be created as an organizational container for the PRD and its downstream slice issues. The default answer is yes — big-batch work benefits from milestone-level progress tracking in GitHub.

Before creating a new milestone, check for an existing one: `gh api repos/{owner}/{repo}/milestones --jq '.[].title'`. If a milestone already exists (e.g., from `/create-milestone` on a prior tranche), ask whether to attach to that milestone instead of creating a new one.

If the user confirms, note the milestone name for use in Step 8. If the user declines, proceed without a milestone — it is organizational convenience, not a structural requirement. Small-batch work (1-2 weeks) does not need a milestone.

### 3. Explore the codebase

Explore the repo to verify the user's assertions and understand the current state of the code.

### 4. Consult institutional knowledge

Before interviewing the user, check two sources:

**Past solutions** — Search `docs/solutions/` for relevant documented solutions:
```bash
grep -rl "relevant-keyword" docs/solutions/ 2>/dev/null
```
If relevant solutions exist, read them. Incorporate their lessons into your understanding of the problem space. Surface relevant pitfalls, patterns, or decisions to the user during the interview — "We've hit X before in a similar feature, and the solution was Y. Should we apply the same pattern here?"

**Research document** — Find the most recent research artifact for this feature. The artifact may live in either of two places depending on the project's `research.storage` setting:

1. **Spike-issue mode** — search GitHub for closed `research`-labeled issues matching the feature:
   ```bash
   gh issue list --label research --state closed --search "<feature keywords>" --limit 5
   ```
   If a matching spike issue exists, read its body — the YAML frontmatter at the top carries the same `date` and `installed_versions_snapshot` fields the archive uses.

2. **Archive mode** (default) — list the per-user archive for this repo. Derive `<repo-slug>` from the current git remote (e.g. `chrislacey89-skills`):
   ```bash
   ls ~/.claude/research/<repo-slug>/ 2>/dev/null
   ```
   Pick the entry whose `feature` frontmatter field (or filename slug) matches this feature.

Check both locations — a project that recently switched modes may still have artifacts in the old location. If both exist for the same feature, prefer the more recent `date` in frontmatter and surface the duplicate to the user. Before trusting any research artifact, check the frontmatter `date` and `installed_versions_snapshot` — if either looks stale against current reality, flag it to the user. If a research artifact exists and is fresh, read it thoroughly. It contains the technical approach already researched and recommended during the `/research` phase. The pitch should build on these recommendations rather than re-debating them. Reference the canonical location (spike issue URL or archive path) in the pitch so `/execute` and Ralph can read it during implementation.

**Artifact precedence:** When the research artifact and `docs/solutions/` disagree, the research artifact takes precedence — it was verified against installed versions. Storage location does not affect trust: a spike issue and an archive entry carry equivalent authority because their bodies are produced by the same `/research` skill against the same Phase 0/1 verification. Surface the conflict to the user during the interview rather than silently choosing one.

### 5. Interview with shaping discipline

Interview the user about the solution, but apply Shape Up's shaping techniques throughout:

**Walk each use case against the solution.** Step through every interaction one-by-one against the emerging design. Gaps and rabbit holes surface here — "what happens when the user does X but Y hasn't loaded yet?" Name each rabbit hole as you find it and agree on a one-line resolution before moving on.
Every important use case needs a main success scenario plus at least two extension scenarios where the flow bends, fails, or needs recovery. If you cannot name the extensions, the scenario is under-shaped.

Treat **hedged anchors** as a specific class of unresolved rabbit hole. Phrases like *"or its X table"*, *"the same loader path the Y currently uses"*, *"mirroring existing Z tests"*, or *"the existing pattern for W"* signal that the model named an entity it did not verify exists. Hedged language in §Rabbit Holes routinely collapses into definite-article confidence in §Implementation Decisions of the same PRD, propagates into the slice Boundary Map at `/prd-to-issues`, and survives past `/execute` Step 0 — whose Consumes-verification gate only fires on named symbols, not vague nouns. Resolve every hedged anchor before §Implementation Decisions hardens around it: either pin the exact identifier (verified via repo grep) or rewrite the claim in terms that don't pretend an entity exists. When `/research` ran for this PRD, its Phase 0 spec-anchor check should already have caught these; this paragraph is the backstop for skipped or compressed `/research` runs.

**Invert once after walking the use cases.** After the forward pass surfaces initial rabbit holes, flip the framing: imagine this feature shipped and caused a serious problem. What was the problem? Work backward from the failure. Route each failure mode into Rabbit Holes (with a resolution) or No-gos. Don't carry them as vague "accepted risks" — if a failure mode can't be resolved or excluded, the design isn't solved yet.

**Check the structure, not just the symptom.** Before locking the shaped approach, ask these three questions one at a time — ask one, absorb the answer, then ask the next:
1. What underlying condition is producing the current problem, not just the visible complaint?
2. Are there delays, handoffs, or missing feedback loops that make the problem harder to see early?
3. Is the proposed intervention a high-leverage change to the condition, or just a local symptom fix?

Keep this compact. The goal is to improve shaping, not to turn the pitch into a systems-thinking essay.

**Classify scope continuously.** As features and behaviors come up, classify them as must-haves or nice-to-haves (~). Nice-to-haves are pre-authorized cuts — if the appetite runs tight, these get scope-hammered first without debate.

**Keep the clay wet.** Present your emerging understanding as malleable — "here's what I'm thinking, push back anywhere" — not as final decisions. This invites course correction rather than rubber-stamping.

**Compare down to baseline, not up to ideal.** When evaluating whether a scope cut is acceptable, compare to what users have today (the baseline), not to the perfect version. Shipping something better than baseline is always better than shipping nothing because you aimed for ideal.

**Conditional flow rows.** If the feature introduces multi-step user-facing flows, new navigation, or significant UI state changes, work out its places (screens/dialogs), affordances (buttons/fields/actions on each), and connections (what leads where) during the interview — and **attach each row to the Must-have story it realizes**, rather than collecting them in a section of their own. This catches missing transitions and ambiguous states early, and it is what lets `/prd-to-issues` Step 5 test coverage at affordance granularity instead of at the granularity of a whole sentence. A row may realize more than one Must, and rows that realize none (nav chrome, loading and empty states) belong in the unattributed residue the template provides — do not force every row under exactly one story, which is the overconstraint that gets rows dropped rather than placed. Skip for API-only, backend, or single-screen changes.

During the interview, bring forward relevant lessons from past solutions and research:
- "The research recommends Ably for presence — should we adopt that recommendation or revisit?"
- "docs/solutions/ has a documented pitfall about X — we should account for that in the design."
- "A past solution suggests using pattern Y for this type of integration. Does that fit here?"

If the user starts speaking in dates, deadlines, or confidence language, make the framing explicit before moving on. Ask these one at a time:
1. Is this a **target** (desired business outcome or deadline), an **estimate** (current forecast), or a **commitment** (a negotiated promise)?
2. What uncertainty still makes a strong commitment premature?
3. Should this pitch carry a range or confidence note rather than a single-point date?

For API-shaped work, shape the contract before you leave the interview. Keep it lightweight, but make these items explicit:

- the API problem statement and impact statement
- the developer consumers of the contract
- the operations the API must support
- the endpoint or event surface at a sketch level
- the required, optional, and defaulted fields that matter to consumers
- the expected error shape
- compatibility notes for existing consumers
- a short "other things we considered" note for rejected paradigm or contract directions

This is not a full implementation spec. It is the minimum contract sketch needed so `/execute` does not invent API behavior mid-flight.

### 6. Validate: rough, solved, bounded

Before writing the pitch, verify the shaped work has all three properties:

- **Rough**: The solution intentionally leaves room for builder judgment. You haven't specified pixel-level UI, exact method signatures, or step-by-step implementation. If it reads like a wireframe or a tutorial, it's too detailed.
- **Solved**: The macro-level direction is resolved. All identified rabbit holes have a one-line resolution. The builder won't need to make fundamental architectural decisions — just tactical ones.
- **Bounded**: The appetite is set. No-gos are declared. Nice-to-haves are marked with ~. The builder knows what's in and what's out without asking.
- **Uncertainty is honest**: If timeline or scope pressure exists, the pitch distinguishes the appetite target from any current estimate or commitment. It does not present a single-point date with false precision while major unknowns remain unresolved.
- **Complete**: Before writing, scan for commonly omitted work that isn't covered by the user stories or rabbit holes. Omitted work — not underestimated work — is the primary driver of scope overruns. AI agents amplify this: Ralph doesn't stay late to add error handling nobody mentioned. It ships without it. Scan this checklist (30 seconds — check for relevance, don't exhaustively discuss each item):
  - Named-but-not-enumerated product-semantic content (rubrics, classification schemes, scoring criteria, taxonomies, role/permission matrices, decision rules) — if the PRD references a classification scheme by name without listing its members, enumerate it in §Implementation Decisions or declare a No-go. Phrases like "the 7 categories" or "the 4 tiers" are false-precision flags: definite-article confidence with the content still in the user's head, not in the PRD body.
  - Alternate knowledge channels — if the feature guards a "don't re-ask / don't duplicate / don't re-surface / process-once" invariant, enumerate every channel the guarded input can arrive through (structured field **and** free prose; typed answer **and** uploaded doc; API param **and** inline text). A guard keyed on one channel's structural marker (a sentinel prefix, message role, or tool-output part type) is blind to the others by construction. For open-vocabulary channels (free prose), the guard must be semantic — an LLM-decision prompt, not a deterministic key — with its regression guard at the behavioral/eval seam. Distinguish "stated" (fully supplied) from "mentioned" (touched but materially incomplete); the latter stays askable.
  - Quality attributes (performance, reliability, security, usability, maintainability) — for each attribute the feature implies, state a SMART criterion in §Implementation Decisions (Specific, Measurable, Attainable, Relevant, Time-bounded), or declare a No-go. If no test can be written, the requirement defaults to whatever the agent happens to implement. Recast vague concerns as testable criteria: "monitor backend paths" → "every backend path emits a structured log event with request_id, latency_ms, and outcome; verified by log-capture integration test in slice X"; "fail fast rather than propagate corrupted state silently" → "on schema validation failure at the X integration point, the writer throws within 50ms; verified by a forced-bad-row test in slice Y"; "the feature is fast enough" → "p95 search latency under 200ms with 100 concurrent users, verified by load test in slice X." If `docs/solutions/` shows past defect clusters in modules this feature touches, the SMART criterion is the assertion or monitoring that would have caught the prior defect. (For each observability AC, name the file or step that emits the call, and confirm the SDK is reachable from that file/step. If the emission point is a client component reaching a server-only SDK — one that reads server-held credentials or requires a Node-only runtime — the AC must be relocated to the upstream server boundary, or a client→server route must be added to scope. Treat this as a Rabbit Hole with a one-line resolution when relocation is not immediately obvious. The SDK's type signature is the upper bound of what compiles; the runtime boundary the SDK can actually emit from is the lower bound of what runs.)
  - Auth/permission changes for new endpoints or data access
  - Database migrations or schema changes
  - Loading, empty, and partial states (UI features)
  - Data backfill or migration of existing records
  - Deployment or environment changes (new env vars, feature flags)
  - Cleanup of code paths being replaced
  - Edge cases in existing features this change might affect
  - API contract implications: request/response shape changes, additive vs breaking risk, auth or scope changes, webhook verification, and developer-facing error contracts

For each omitted category that applies: add it to user stories, name it as a Rabbit Hole with a resolution, or declare it a No-go. Don't leave it invisible.

If the feature changes or introduces an important API contract and the contract shape still feels under-specified after the interview, invoke `/api-design-review` before finalizing the pitch.

If any property is missing, go back to the interview and close the gap.

### 7. Design modules

Sketch out the major modules you will need to build or modify to complete the implementation. Actively look for opportunities to extract deep modules that can be tested in isolation.

A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

For each module with complex internal state: identify the key invariant that, if violated, would produce a silent corruption rather than an immediate failure. Note it in the Implementation Decisions section — the implementor should add a precondition or `isValid()` check for it.

**Every mechanism you named in prose gets a home.** Before leaving this step, walk §Solution and the Must-haves' flow rows and take each mechanism you named there — each data structure, pre-computed input, background job, cache, or seeded state. Each one gets exactly one of four dispositions: a **Modules entry** here, a **Rabbit Hole** with a stated resolution, a **No-go** line, or **its own Must-have story**.

The fourth is the one authors miss. A prerequisite can be a full user goal in its own right rather than a part of some other goal — Cockburn's case is a customer who wants to *Rent a Video* but must *Set up a Membership* first, and he names it only so writers do not "fix" it into a false hierarchy (Ch. 5). When the mechanism is itself something a user is trying to accomplish, promote it to a story; that is what puts it in front of `/prd-to-issues` Step 5's unmapped-Must halt. A mechanism named in prose and given none of the four is invisible downstream: Step 4 reads §Implementation Decisions for locked contract shapes, so a mechanism with no module leaves the boundary-map derivation nothing to catch.

Check with the user that these modules match their expectations. Check with the user which modules they want tests written for, and at what boundary.

**If the user is uncertain about a module's interface** — or if there are multiple plausible designs with real tradeoffs (e.g., one method that does everything vs. three composable methods, or a callback API vs. an event emitter) — invoke `/design-an-interface` to generate 2-3 radically different options using parallel sub-agents. Present the options with tradeoffs and let the user choose. If the interface is obvious or the user has a clear preference, skip this and move on.

**If the uncertainty is in the API contract itself** — paradigm choice, request/response shape, webhook model, auth model, or compatibility posture — invoke `/api-design-review` instead of treating it like a normal module interface exercise.

### 8. Write the pitch

Once you have a complete, shaped understanding of the problem and solution, write the pitch using the template below. The pitch should be submitted as a GitHub issue.

**If a container milestone was requested in Step 2**, create it before the PRD issue so the issue can be attached:

1. Create the milestone: `gh api repos/{owner}/{repo}/milestones -f title="<Milestone Name>" -f description="<1-2 sentences from the problem story>"`
2. Create the PRD issue with `--milestone "<Milestone Name>"` to attach it
3. Note the milestone name in the pitch output so `/prd-to-issues` can propagate it to slice issues

<pitch-template>

## Problem

A specific story showing why the status quo fails. One actor, one attempt, one failure. Not an abstract complaint — a scene that makes the pain concrete.

## Appetite

Small batch (1-2 weeks) or Big batch (6 weeks). State why this is the right budget for this problem — what makes it worth this investment but not more.

State explicitly that the appetite is the **target** for how much time this problem is worth, not the current **estimate** of duration and not a delivery **commitment**.

## Target / Estimate / Commitment

[Include when timeline, scope, or deadline pressure exists. Omit when there is no meaningful timing discussion.]

- **Target:** [Desired business outcome, event date, or budget boundary]
- **Current estimate:** [Range or confidence ladder, not a false-precision single point]
- **Commitment posture:** [No commitment yet / conditional commitment after X is resolved / explicit commitment]

## Uncertainty / Confidence

[Include when timing or scope confidence materially affects the pitch. Omit for low-pressure shaping work.]

- **Current confidence:** [High / medium / low]
- **Main uncertainty drivers:** [What must be learned or decided before the estimate tightens]
- **What would increase confidence:** [Prototype, research answer, first tracer bullet, contract decision, etc.]

## Solution

The shaped concept. Rough enough that the builder has room for judgment. Solved enough that the macro direction is clear and rabbit holes are patched. Bounded by the appetite above.

Describe what changes from the user's perspective. Where it helps, describe the approach at the architectural level, but don't prescribe implementation details the builder should own.

If the problem has a clear structural driver, state it briefly here — enough to explain why this approach addresses the condition producing the pain rather than only the nearest symptom.

If the solution designs against a library-provided callback (agent hooks, middleware, lifecycle methods, tool handlers), cite the **Library Callback Contracts** snapshot from `research.md` (Phase 1.25) by file:line. Do not describe the mechanism as "inject via X" or "pass Y" unless X and Y appear verbatim in the accepted return shape. An imagined mechanism that doesn't exist in the library's `.d.ts` is the class of drift `/research`'s Phase 1.25 exists to prevent.

[Diagram suggestion: before leaving the Solution section, consider whether the content above would read more clearly as a diagram — a flowchart, sequence diagram, architecture sketch, state machine, decision tree, or before/after transformation. The lists and prose stay authoritative; a diagram is a reading aid for `/prd-to-issues` decomposition and `/execute` cold-start sessions. If yes, invoke `/mermaid`. When it is the *whole pitch* a reader will skim rather than one figure in it, `/visual-recap` renders a PRD forward — decision cards for the commitments this pitch makes, an options-comparison for a fork it leaves open, and this diagram, as one transient HTML file. Optional, never auto-invoked, and not a PRD requirement: the issue body stays the source of truth either way. Skip when the Solution is short and linear enough that the prose is already the cleanest rendering — the bar is whether a reader unfamiliar with the codebase would orient faster with the diagram than without it. This prompt is placed at Solution-end (not nested in the conditional flow rows) so it fires regardless of whether the Solution took a UI-flow, architecture, refactor/swap, or state-machine shape — consolidating the prior Flow Sketch-gated trigger and the refactor/swap trigger proposed in #90 into a single shape-agnostic prompt.]

## Rabbit Holes

Named risks with one-line pre-decided resolutions. These are the unknowns that could cause a 6-week project to take 18 weeks if left unexamined. By naming them here with a resolution, the builder doesn't have to make these calls under deadline pressure.

- **[Risk name]**: [One-line resolution]

## No-gos

Explicit exclusions. Silence means "in scope," so anything the builder might reasonably assume is included but ISN'T must be listed here. These aren't "maybe laters" — they're deliberate boundaries.

- [Thing that's explicitly out]

## User Stories

### Must-haves

1. As a [actor], I want [feature], so that [benefit]
   - **[Place Name]**: [affordance 1], [affordance 2] -> connects to [Other Place]
   - **[Other Place]**: [affordance 3] -> connects to ...

[The indented rows are the flow rows, and they are conditional: include them only when the feature has multi-step user-facing flows, new navigation, or significant UI state changes. Omit for API-only, backend, or single-screen changes. Repeat a row under each Must it realizes; put rows that realize none under *Shared affordances* below.]

### Nice-to-haves (~)

1. ~As a [actor], I want [feature], so that [benefit]

### Shared affordances (unattributed)

[Include ONLY when flow rows exist AND some row serves no single Must — nav chrome, loading and empty states, global error surfaces. These are not commitments; `/prd-to-issues` does not read them as unmapped Musts. Leave the heading out entirely when every row found a parent.]

Stories are bounded by the appetite. Must-haves define the minimum shippable version — what makes this better than the user's baseline today. Nice-to-haves are pre-authorized cuts: if the appetite runs tight, these get scope-hammered without debate. prd-to-issues maps each vertical slice back to these stories, and where a Must carries flow rows it maps at affordance granularity.

## API Contract Sketch

[Include ONLY when the feature introduces or changes an API contract. Keep this lightweight and consumer-oriented, not implementation-detailed.]

- **Problem statement:** [What developer problem this API solves]
- **Impact statement:** [What outcome the API enables]
- **Consumers:** [Who integrates with it]
- **Operations:** [What the API must allow consumers to do]
- **Surface sketch:** [Endpoints/events at a high level]
- **Important fields:** [Required / optional / defaults that matter to consumers]
- **Error shape:** [Machine-readable codes + human-readable messages]
- **Compatibility:** [Additive / potentially breaking / breaking]
- **Other things we considered:** [Rejected paradigm or contract directions]

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include implementation snippets — loop bodies, error handling, helper function internals, configuration string literals. These drift the moment the builder makes a judgment call.

[This is the section a reader skims, because nothing in a bullet list marks which decisions foreclose something. When one does — a wire format, a public id, an ownership boundary, a data-model shape — `/visual-recap` can render these forward as decision cards: decided, rules out, reverses if, source, with every field cited to this body or visibly marked asserted. Optional and transient; it never replaces writing the decision down here.]

DO render **locked contract shapes** in code form when the PRD's decision lives at the surface level: schema column lists (Drizzle, Prisma, SQL DDL), exported type aliases or interfaces, exported function signatures, structured input/output schemas (Zod, JSON Schema). The test is empirical: if a downstream pipeline step (`/prd-to-issues` Boundary Map, `/execute` Consumes verification, `/pre-merge` boundary-contract review) will grep for this identifier or shape, it is a contract shape and belongs in code. If no downstream step will inherit it verbatim, it is an implementation detail and stays prose or stays out. Contract-shape code drifts at the same rate as the PRD's renegotiation path — edit the PRD body and regenerate the Coverage Matrix, the same flow used for any other PRD content change.

## Research Reference

[Include only if a matching research artifact exists. Use the form that matches the project's `research.storage` mode.]

**Spike-issue mode (preferred when present):**

Technical research for this feature is documented in spike issue Refs #<spike-issue-number> (closed-on-creation snapshot, labeled `research`). Key recommendations:

- [Recommended approach from research]
- [Key constraint or tradeoff from research]

Implementors should read the spike issue before starting work (`gh issue view <spike-issue-number>` works on any machine).

**Archive mode (fallback when no spike issue exists):**

Technical research for this feature is documented at `~/.claude/research/<repo-slug>/<feature-slug>-<YYYY-MM-DD>.md` (per-user archive, outside the repo). Key recommendations:

- [Recommended approach from research]
- [Key constraint or tradeoff from research]

Implementors should read the research document before starting work. Archive paths are not openable by readers other than the originating user — for cross-machine, multi-contributor, or public-audience PRDs, opt the project into spike-issue mode (see `/research` Phase 5a).

## Lessons from Past Solutions

[Include only if relevant docs/solutions/ files were found]

The following documented solutions informed this pitch:

- `docs/solutions/<path>` — [What lesson was applied]

---

**Next session:** /prd-to-issues #<this-issue-number>
**Input:** the PRD issue body

Do not invoke `/execute` directly on this issue — it is a shaped pitch, not a slice. Print the issue number explicitly so the next session can be opened by copy-paste rather than by fishing for it.

</pitch-template>

## Handoff

- **Expected input:** clarified user problem, validated technical context from `/research`, and any past-solution guidance relevant to the feature
- **Produces:** a shaped PRD issue (optionally attached to a container milestone for big-batch work) with appetite, solution, rabbit holes, no-gos, and contract sketching when relevant
- **May invoke:** `/design-an-interface` when a module interface is still unresolved, or `/api-design-review` when API contract uncertainty remains
- **Comes next by default:** `/prd-to-issues`
