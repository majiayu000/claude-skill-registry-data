---
name: expert-architecture
description: "Create an architecture document from a spec — the bridge between specification and implementation, answering every design question the spec deliberately left open: component structure, technology choices within constraints, integration approach, trade-off resolutions, API surfaces, data models, and security controls mapped to threats. The result must be implementable without the implementer making architectural decisions inline. Activates whenever a spec needs architecting before planning or building — the user says 'architect this', 'design the implementation', 'turn this spec into a design', 'expert-architecture', or hands over a spec whose design must be settled before code. Every non-trivial decision is anchored to a named external standard or a structured first-principles articulation, and every premise is verified against current source: library behavior via Context7, file structure via CodeGraph, semantic patterns via codebase-RAG, internal contracts by reading the specific files. Clear Thought tools carry the structured reasoning where the reasoning kind matches. A required tool that cannot run is a halt, not a license to reason from memory. Do not mirror the existing codebase as if its patterns were self-justifying, clone a prior architecture's shape without re-deriving it from this spec, or leave decisions in working context where the reader cannot evaluate them. In a chat interface with no Context7, CodeGraph, or Clear Thought MCP, use expert-architecture-portable instead."
---

You are writing an architecture document. An architecture is the bridge between specification and implementation — it answers every design question the spec deliberately left open: component structure, technology choices within constraints, integration approach, trade-off resolutions, API surfaces, data models, and security controls mapped to threats. The architecture must be implementable without the implementer making architectural decisions inline.

The measure of an architecture is what it enables downstream. A good architecture lets a planner produce concrete implementation steps without re-architecting. It lets a reviewer verify the build against named decisions and reach a defensible conclusion. It lets a stakeholder read it and know how the spec is being satisfied, what trade-offs were made, and where the work could break. An architecture that fails any of these tests is not finished — it is only a draft of section headings.

Apply the Expert Standard throughout this work. Evaluate every architectural choice against established engineering standards, not against patterns in the current codebase. If existing code or prior architectures encode a wrong pattern, the new architecture is designed correctly and notes the divergence — it does not perpetuate the bad pattern silently. Verify every factual premise the architecture rests on against current source: library behavior via Context7, file structure via CodeGraph, semantic patterns in the codebase via codebase-RAG, internal contracts via Read of specific files. Memory of what you saw earlier in the session, claims imported from the spec without re-derivation, and patterns inferred from other architectures are all forms of pattern-matching — they may inform the work, but they are not premises until they have been verified against current source.

How to read this command

This command exists to foreclose specific reasoning patterns the architecture work will otherwise drift into by default. Each pattern below is named with the rebuttal that brings the work back. When you catch yourself drifting toward one of these, the rebuttal is the discipline.

"I'll skip the codebase survey because the spec is detailed enough." Phases 3 and 4 are not optional. The spec describes what is being built; the codebase describes the ground the architecture is being built on. Even a thorough spec leaves the agent without context on coupling hotspots, existing patterns the architecture must respect or diverge from, and integration points the spec doesn't enumerate. Skipping the survey produces architecture that satisfies the surface of the spec while breaking the codebase. The "absence of result is the result" framing handles empty surveys; it does not justify skipping them.

"I'll cite a governing standard if I happen to know one and proceed without one otherwise." Phase 5 is not optional. Every non-trivial decision is anchored to either a named external standard or a structured first-principles articulation. A decision without an anchor is an unnamed approval — the failure mode the decision format exists to prevent. "I couldn't recall a relevant standard" is not a reason to skip the anchor; it is a reason to find the standard or produce the first-principles articulation.

"I'll abbreviate the design decisions section since the substance is in the components diagram." The Design decisions section is a load-bearing audit section — it carries the frame-correctness proof and the premise-correctness proof for every non-trivial decision. Components and structure show what the architecture is composed of; design decisions show why each composition choice is correct and what it rests on. An architecture document with rich components and thin decisions has hidden the reasoning where the implementer and reviewer cannot find it.

"Context7 isn't responding, so I'll go from memory of the API." Phase 6 verification is not optional, and memory is not verification. If Context7 is unavailable for a library you must verify, that is a tool-failure stop condition — halt with a diagnostic message naming the library that couldn't be verified. Memory of an API surface is the unverified-premise failure mode. Stating "the library handles this" without a current Context7 lookup produces confidently-wrong architecture.

"This decision is obvious; I don't need to evaluate alternatives." Phase 10's "what this decision is NOT" element exists precisely because copying a correct recommendation is easy and rejecting wrong alternatives demonstrates understanding. A decision without rejected alternatives has not been evaluated — it has been pattern-matched to a default. If you cannot name and reject at least one wrong alternative for a non-trivial decision, the decision is either trivial (record it briefly and move on) or it has not been evaluated yet.

"The reasoning is in my working context; the document just needs the conclusions." Decision-hiding is one of the five traps below. The reader of the architecture cannot evaluate reasoning that lives only in the agent's working context. Every non-trivial decision's reasoning — including the structured-reasoning trace from Clear Thought tools where applicable — goes in the document. A conclusion in the document without the reasoning is brittle; it produces the wrong answer the first time the architecture meets an edge case it doesn't explicitly cover.

"Clear Thought feels like ceremony for this case." The Reasoning support section below specifies which Clear Thought tool is mandatory for which kind of reasoning. The discipline is not "invoke when it feels useful" — it is "invoke when the reasoning kind matches." Skipping a mandatory invocation because the answer feels obvious is the same failure mode as skipping a mandatory verification because the claim feels obvious.

Where architecture work goes wrong

Architecture work fails in five specific ways. The first three are general failure modes that surface across spec, plan, and architecture work; the last two are specific to architecture. Read all five before starting — these are the failure modes the rest of this process exists to prevent. They are not theoretical. Every one shows up reliably in agent-produced architecture work that doesn't actively guard against them.

The codebase-mirroring trap. You read the existing codebase and design the new architecture to match what's already there. Existing components become the model for new components; existing layering becomes the model for new layering; existing integration patterns become the model for new integrations. The trap is not that you considered the codebase — that's appropriate context. The trap is that the codebase becomes the standard you evaluate the new architecture against, instead of the named engineering standards the spec was derived against. The new architecture inherits whatever the codebase got wrong, and it inherits it confidently because it "fits." Catch yourself when the justification for an architectural choice is "this is how the codebase already does it" without naming the engineering standard the existing pattern is correct against. The existing pattern may or may not be correct. Treating it as self-justifying is the failure.

Methodology mapping: silent pattern replication (codebase variant) — one of the four failure signals defined by the methodology spec, expert-standard skill, and workflow document.

The pattern-cloning trap. You see a prior architecture document — one in the project, or one you remember from elsewhere — and you copy its structure, its decision categories, its component breakdown to your new architecture. The prior architecture was successful, so its shape feels safe. The trap is that you imported a solution shape without re-deriving whether the same shape is right for this spec. Two architectures may share structure because they belong to the same family (e.g., a pair of related microservices in the same system) — copying that structure to an architecture for a different kind of system (e.g., a batch pipeline, a desktop app) would import the wrong frame. Every architecture inherits what its precedents already decided when they belong to the same family (this is what the Inheritance from precedent table is for) and re-derives everything else from this spec's requirements. If you are about to copy a structural element from a prior architecture, you must be able to state which spec requirement makes that element right here — not just that it was right there.

Methodology mapping: silent pattern replication (prior-artifact variant) — the same failure signal as codebase-mirroring, with the source being a prior document instead of the surrounding code.

The decision-hiding trap. You make an architectural decision in your reasoning — choosing between two valid approaches, resolving an ambiguity in the spec, interpreting how a standard applies to this situation — and you do not surface the decision in the document. The conclusion appears in the architecture; the reasoning that produced it lives only in your working context, where the reader cannot review it. The first edge case the architecture doesn't explicitly cover produces the wrong answer because the implementer has the conclusion but not the reasoning. Every non-trivial decision goes in the Design decisions section in the five-part decision format (decision; standard or first-principles anchor; why it applies here; what this is NOT and why; premise verification — what was checked, against what source, with what result). Every judgment call goes in the Design decisions section with the reasoning. The test: a reader should be able to evaluate whether your judgment was sound. They cannot do that on conclusions alone.

Methodology mapping: assessment gap — approving or delivering work that a rigorous evaluation would flag, with the reasoning hidden so the evaluation cannot occur.

The standards-decoration trap. You name standards in the architecture document — OWASP, ISO, RFC, NIST — and the document looks rigorous. But the named standards do not actually drive any decision. They appear in the "Standards governing this architecture" table and in the prose, but the architectural choices were made by other reasoning (often pattern-matching against the codebase or against precedent), and the standards were attached afterward to give the document the shape of compliance. The pattern is recognizable: a term naming a standard or principle, surrounded by content that doesn't show how that standard or principle was actually applied to drive a specific decision. The defense: every named standard must be tied to at least one specific architectural decision the standard actually drove. A standard that's referenced but doesn't govern any decision in the document is decoration. Remove it, or find the decision it should be governing.

Methodology mapping: unnamed approval — the standard slot is full in name (the standard is cited) and empty in substance (the standard didn't drive the decision). The cite is decoration over a judgment that was made on other grounds.

The deferred-decision trap. You leave architectural decisions ambiguous in the document — "the implementer will choose between X and Y based on what fits best," "the framework decision is left to the build phase," "the data model can be refined during implementation." Each deferral feels like flexibility. In practice, each is an architectural decision you made (the decision to defer) without surfacing it as a decision. The downstream cost is that the planner and the implementer encounter ambiguity the architect should have resolved, and they resolve it inline — exactly the failure mode the architecture exists to prevent. If a decision is genuinely the implementer's call (e.g., the choice of variable names within a component), it does not belong in the architecture at all. If a decision is non-trivial and could affect another component or another quality characteristic, the architecture resolves it.

Methodology mapping: architecture-specific failure mode not directly in the methodology's four signals. Surfaced here because architecture work uniquely produces this failure class through the temptation to push choices to downstream phases. Noted candidly as an extension to the methodology's four-signal taxonomy rather than a renaming of one of them.

Workflow context

This command runs inside the session protocol the project's workflow document defines. The workflow brackets architecture work with output-contract gates — a before-contract that defines what the deliverable must satisfy (approved before architecture work begins) and an after-contract that proves the deliverable does satisfy it (produced before delivery). The hands-off principle described below in the Process section governs operation between those gates; it does not displace them. An agent invoking this command operates under the workflow's session protocol — the command's process is the work that happens inside the workflow's outer bracket, not in place of it. If a workflow gate fires (scope change, contract amendment, memory ingestion), it interrupts the hands-off operation; that is correct workflow behavior, not a violation of the hands-off principle.

Reasoning support

Architecture work involves multiple distinct kinds of reasoning, and the Clear Thought MCP server exposes a tool purpose-built for each kind. This command treats Clear Thought as a framework spanning the architecture phases, not as a single optional invocation. Each row below specifies which Clear Thought tool is mandatory for which reasoning kind, when it fires, and where its output lands in the architecture document.

PhaseReasoning kindClear Thought toolInvocation discipline1–2 (Read inputs, Goal)Knowledge-state assessmentmetacognitivemonitoringMandatory at session start. The agent's knowledge level, claim status (fact / inference / speculation), and reasoning biases are surfaced explicitly before architecture work proceeds. Output goes into the architecture document's Design decisions section as the baseline.5 (Standards) when no formal standard appliesFirst-principles derivationmentalmodel(first\_principles)Mandatory whenever a decision uses the first-principles articulation alternative instead of a named standard. The three-part structure (goal, local-optimum shortcut, why chosen path serves goal) is the structured tool output, not narrative. Lands in the five-part decision format's authoritative-standard slot.Cross-phase trigger (when foundation problems surface)Foundation-problem characterizationdebuggingapproach (variant per problem: cause\_elimination, divide\_conquer, binary\_search, program\_slicing)Mandatory when foundation problems are flagged. Foundation problems are a cross-phase concern, not a single-phase one. They surface most often in Phase 4 (CodeGraph reveals coupling defects, blast radius, structural distortions in files the architecture must build on) or Phase 7 (spec problems trace back to codebase foundation issues), and occasionally in Phase 3 (semantic survey reveals capability implementations whose shape signals a foundation problem) or Phase 8 (decomposing a hard decision exposes a foundational issue underneath it). When flagged in any phase, characterize the foundation problem with debuggingapproach before proceeding to design decisions — the design must either fix the foundation or work around it explicitly, not silently inherit it. Each foundation correction in the architecture document carries the debugging approach used to characterize it.7 (Spec problems) for hard contradictionsDialectical resolutionstructuredargumentation (thesis-antithesis-synthesis)Mandatory when Phase 7 fires for a hard contradiction. The agent constructs the thesis (recommended resolution), the antithesis (strongest counter-argument), the synthesis (resolution that survives the antithesis). Soft ambiguities optionally use the same tool. Reasoning trace lands in Design decisions section.8 (Hard decisions)General sequential decompositionsequentialthinking (Clear Thought)Mandatory for every architecture document. If no decisions in a given architecture meet the trigger criteria for sequentialthinking treatment, the Design decisions section explicitly states that and explains why (matching /expert-plan Step 6's pattern). Silent omission is non-compliance.9 (Threat model)Hypothesis-driven security reasoningscientificmethodMandatory when Phase 9 fires (security in scope). Each threat is structured as observation → question → hypothesis (with variables, assumptions) → experiment (controls, predictions) → analysis → conclusion. Replaces free-text threat descriptions.10 (Design decisions) for 3+ alternativesMulti-criteria evaluationdecisionframework (multi-criteria)Mandatory when a design decision has three or more plausible alternatives with multiple competing criteria. Multi-criteria scoring with explicit weights replaces narrative justification of why each alternative is wrong. The five-part decision format remains for binary or simple decisions.Before delivering (Gate A)Multi-perspective evaluationcollaborativereasoning (personas: planner, reviewer, stakeholder)Mandatory before delivery. Each persona reviews the architecture from their perspective; gaps unique to a perspective are surfaced. The synthesis goes into the Design decisions section, OR (if no perspective-specific gaps surface) an explicit attestation that all three perspectives were checked appears in the Design decisions section.

A note on tool naming: earlier versions of this command referenced "Sequential Thinking," which is a different, older MCP server with a single tool. The reference for this project is the Clear Thought MCP server, which exposes the eight-tool suite above. References to Sequential Thinking are updated to the matching Clear Thought tool throughout this command.

Output contract

The architecture document this command produces is structured around two-axis evidence. Specific output sections carry the load for each axis. An architecture document missing any of these sections, or with any of them empty without an explicit attestation that the section is genuinely empty for this architecture, has not satisfied the contract and is not delivered.

Frame-correctness proofs. Two sections carry frame-axis evidence. The Design decisions section is the per-decision frame proof — every non-trivial decision's authoritative-standard slot (element 2 of the five-part decision format) names the standard or first-principles anchor that governs it. The Standards governing this architecture table is the project-wide frame audit — every standard cited anywhere in the document appears with what it governed. A decision without a named anchor is an unnamed approval; a standard cited without a decision it governed is decoration.

Premise-correctness proofs. Each non-trivial decision's premise-verification slot (element 5 of the five-part decision format) names what was checked, against what source, with what result. Decisions resting on no factual premise about existing source mark the slot "no factual premises — pure design choice." Premise verification is integrated per-decision rather than living in a separate output section — the decision and the verification of its factual premises appear together, not cross-referenced from elsewhere in the document.

Gap acknowledgment. The Limitations and trade-offs section is the explicit acknowledgment of what was not grounded in a named standard or verified against current source — known limitations, accepted trade-offs, and gaps on either axis. Honest gaps are auditable; hidden gaps become defects. A Limitations section that is genuinely empty for this architecture (no known limitations, no accepted trade-offs, no gaps on either axis) requires an explicit attestation to that effect, not silent omission of the section.

Input

The user will provide a path to a specification document, typically produced by /expert-spec and conventionally located in the project's specs directory. The architecture you produce derives from that spec. Read all of it. Read every document the spec references that exists locally — prior architectures, prior plans, related specs, project-level governance documents the spec names, and the standards documents the spec names. An architecture written from a shallow read of the spec ends up satisfying the surface of the requirements while missing the constraints buried in the references.

$ARGUMENTS



Process

The process is eleven ordered phases plus two post-design mapping phases (10a and 10b). Each phase has prerequisites — you do not advance until the prior phases have produced what this phase consumes. Skipping a phase is not flexibility; the phase ordering exists because each phase produces evidence the next phase depends on, and skipping invites making decisions on incomplete context. The order is not arbitrary: each phase verifies what the next phase will assume.

You operate hands-off from invocation to delivery. The only valid stop conditions are (a) a hard contradiction in the spec or between the spec and a governing standard that blocks all valid architectures (Phase 7), and (b) a tool failure that prevents you from satisfying the verification requirements (CodeGraph, codebase-RAG, or Context7 unavailable when needed). Soft ambiguities — design questions the spec leaves genuinely open between valid architectures — you resolve, record in the architecture's Design decisions section, and proceed. Do not stop to ask design or engineering questions. Resolution and surfacing in the document is the right path for those.

Handling user requests to skip rigor. Some users invoke this command with explicit shortcuts — "skip the codebase survey," "don't bother with Context7 verification," "shortcut to the design decisions," "just produce the architecture without all the structured-reasoning ceremony." The discipline is: flag once, then comply. Name what is being skipped, what failure mode that step exists to prevent, and what the user is consenting to by skipping it. Then write the architecture they asked for. Do not repeat the flag after acknowledgment. The user makes the final call with full information; restating the concern after they've decided is process theater, not rigor. The Limitations section of the resulting architecture records what was skipped and at whose direction, so that the deliverable's gaps remain auditable even when the rigor was waived.

1\. Read inputs

Read the input spec in full at the path the user provided. Not skim — read every line. Read every document the spec references that you can resolve locally:



Prior specs the spec names

Prior architectures the spec names (especially when this architecture is one of a family — e.g., a sibling architecture for related work)

Project-level governance and methodology documents the spec names (compliance checklists, decision-justification rubrics, any project-specific architectural conventions). When the project includes them, treat them as constraints the architecture must respect.

Any standards documents the spec names (ISO, OWASP, RFC, NIST) — the spec told you which standards govern; read those that are accessible



Identify which spec requirements (R-numbered) and quality requirements (Q-numbered) you will need to address in the architecture. Note the locked decisions from the spec's "Decisions made during this spec" section (or equivalently named section) — these are commitments you must honor; you do not re-derive them.

2\. Understand the goal

State back, in one paragraph for your own reasoning (not necessarily for the architecture document), what is being architected, why, and what success looks like for this architecture. The goal is the anchor — every architectural decision you make must serve it. If you cannot state the goal in one sentence, you do not have it yet, and continuing produces architecture that satisfies the surface of the spec but doesn't serve the underlying need.

The test: if two thoughtful readers of the spec would derive different goals from it, you have a goal-ambiguity that must be resolved before architecture work proceeds. Treat that as a soft ambiguity — choose the interpretation that best serves what the spec is for, record the resolution in the architecture document's Design decisions section, and proceed.

The knowledge-state assessment for this session — your knowledge level on the subject, claim status (fact / inference / speculation) for what you think you know, and reasoning biases that may be operating — is produced via Clear Thought MCP's metacognitivemonitoring tool (see the Reasoning support section). This is mandatory at session start. The output goes into the architecture document's Design decisions section as the baseline against which later decisions can be evaluated.

3\. Codebase survey — semantic

Load the codebase-RAG skill via the Skill tool: Skill(skill: "agentboard:codebase-rag"). The skill exposes mcp\_\_codebase-rag\_\_rag\_search (semantic search across the project) and mcp\_\_codebase-rag\_\_rag\_query\_impact (semantic blast-radius for a candidate change). If the skill is not installed in the user's Claude Code session, the load will fail; this is one of the tool-failure stop conditions — halt with a diagnostic message naming the missing skill (agentboard:codebase-rag) and stop.

Survey scope. Bound the semantic survey to: capabilities the architecture will introduce, modify, or replace; coupling hotspots the architecture will touch (per CodeGraph stats from Phase 4 — note that scope-bounding is iterative between Phases 3 and 4); entry points the architecture will affect. Capabilities the architecture is leaving alone do not need deep semantic surveys — they appear in the architecture as constraints (existing behavior the architecture preserves) rather than as design context (existing behavior the architecture must understand to design against). For a small or greenfield codebase this distinction may not matter; for a large codebase (hundreds or thousands of files), unconditional querying produces volumes of data that exhaust context before Phase 10 (design decisions) is reached. The "absence of result is the result" framing handles empty surveys; it does not handle surveys that overflow.

Once loaded, use rag\_search to map the semantic landscape this architecture sits in:



For each major capability the architecture is introducing, modifying, or replacing, query for existing implementations of that capability in the codebase. (Example: spec requires authentication → search "authentication", "auth flow", "token validation", "session handling"; you may run multiple queries to triangulate.)

For each component type the architecture is likely to introduce, query for existing patterns of that component type. (Example: a service layer → search "service interface", "service implementation", "service registration".)

For each governing standard from the spec, query for existing code that cites or implements that standard. (Example: OWASP Password Storage → search "password hash", "credential storage", "argon2", "bcrypt".)



For each query, capture: the query you ran, the count and a brief summary of the matches (file paths and what they appear to be doing), and your interpretation of what the matches mean for the architecture (existing patterns to extend, existing patterns to diverge from, capability gaps to fill). The semantic survey informs Phase 4 (which files to deepen with structural analysis) and Phase 5 (which standards are already in scope for the codebase). Do not skip queries that returned nothing — record the empty result, because absence-of-existing-implementation is itself architecturally relevant.

If rag\_search returns no matches across all queries (typical for a brand-new project or a markdown-only tool-building project), record this as a finding ("semantic survey: project contains no semantic matches for capabilities X, Y, Z; architecture will rely primarily on the spec and named standards"). Do not skip the queries. Mandatory invocation is non-negotiable; absence of result is the result.

4\. Codebase survey — structural

Run codegraph\_scan on the project root. The graph is in-memory only; subsequent CodeGraph queries depend on it. Run this even when the project has no scanned languages — codegraph\_scan returning zero files is a finding, not a failure.

Survey scope. Bound the structural queries to: files surfaced by the semantic survey (Phase 3) as relevant to the architecture; files the spec named explicitly; files the broader graph queries (get\_stats, find\_entry\_points, list\_files) surface as part of the architecture's footprint (coupling hotspots the architecture will touch, entry points the architecture will affect, modules candidate components will modify or replace). Files outside the architecture's footprint do not need dependency / dependent / subgraph queries — they exist in the codebase but are not part of the ground the architecture is being built on. The same scope-bounding principle as Phase 3 applies: depth where the architecture acts; constraints where it doesn't.

Then run, in this order:



codegraph\_get\_stats — the structural overview. File counts by language, most connected files, most depended-on files (the coupling hotspots — these are the files that ripple changes through the codebase, and the architecture must handle them with extra care).

codegraph\_find\_entry\_points — the application's entry points. Architecture decisions about request flow, lifecycle, and bootstrap touch entry points first.

codegraph\_list\_files — the full file inventory. Use this to confirm the survey covered what you expect, and to spot files the spec implies should exist but don't.



For each file the spec named, the semantic survey identified as relevant, or the stats/entry-points/list surfaced as relevant within the architecture's footprint:



codegraph\_get\_dependencies — what does this file import? These are the contracts the architecture is building on.

codegraph\_get\_dependents — what imports this file? These are the things the architecture's changes might break.

codegraph\_get\_subgraph (depth 2) — the local neighborhood. Shows the file's full architectural context, not just direct connections.



If a candidate component the architecture is going to introduce will modify or replace existing files, run codegraph\_get\_change\_impact on those files to understand the blast radius before designing the change. The blast radius determines whether the change is contained (architecture confined to a subsystem) or pervasive (architecture must address dependents).

If codegraph\_scan returns zero files (typical for a markdown-only project), record this and proceed. The structural survey is empty in that case but the survey itself was performed — the difference between "did not run" and "ran, returned empty" is the difference between unverified and verified-absent.

Distinguish structural questions from existence questions. CodeGraph answers "what imports what" and "what's the blast radius." It does not answer "does this symbol exist at this location" or "does this line say this." For literal-content claims and absence claims, use grep or Read — not CodeGraph. The architecture's Premise verification (Phase 6 onward) uses each tool for what it actually answers.

5\. Identify governing standards

The spec named the standards that governed it. The architecture inherits those — every standard from the spec's "Standards that govern this spec" section is automatically a standard for this architecture. Read each one (the section in the spec, the linked document if local, or recall what the standard demands if you have verified knowledge from training).

To the inherited standards, add the architecture-phase governing standards that apply to most software architectures:



SOLID principles (single responsibility, open-closed, Liskov substitution, interface segregation, dependency inversion) for object-oriented and component design.

REST conventions (RFC 7231 for HTTP semantics, RFC 7232 for conditional requests, RFC 7807 for problem details) for API design, when API design is in architecture scope.

OWASP Application Security Verification Standard (ASVS) for security architecture, when the system has any security surface.

OWASP Threat Modeling guidance — threats before controls.

ISO/IEC 25010:2023 quality characteristics — the architecture must advance the quality characteristics the spec requires, and you must state how each is addressed.



Add domain-specific architecture standards relevant to the system being architected (microservice patterns; event-driven architecture principles; database design normal forms; distributed systems consistency models — identify per-architecture, do not pre-load). Verify external standards via Context7 in Phase 6 when they're versioned library APIs; ISO/RFC/OWASP/NIST standards are stable, but the spec's interpretation of them must be your interpretation too.

For each named standard, write down (for your own reasoning) what it governs in this architecture. A standard that doesn't govern any specific decision is the standards-decoration trap waiting to happen. Either find the decision it should be governing, or remove it from the list.

When no formal standard applies to a decision (which happens for some architectural choices — naming conventions, internal abstractions that aren't covered by SOLID or any other standard, project-specific component boundaries), the anchor for that decision is not a named standard but a first-principles articulation. The articulation is produced via Clear Thought MCP's mentalmodel(first\_principles) tool — see the Reasoning support section. The structured tool output has three parts: (a) name the goal of the work the decision serves — what makes the output correct as opposed to merely complete; (b) name what the local-optimum shortcut would look like — the path the agent's training will offer that satisfies "looks done" without serving the goal; (c) name why the chosen path serves the goal and the shortcut wouldn't. This articulation is acceptable in the five-part decision format's "authoritative standard" slot when no standard applies, and it must appear in the architecture document for the decision. The principle being enforced: every non-trivial decision is anchored either against a named external standard or against a goal-articulated first-principles reference frame — never against "it seemed right," "the codebase does this," or "common practice."

Watch for the standards-decoration trap here. Every named standard must drive at least one decision. Naming standards you won't use makes the document look rigorous and is the opposite of rigor.

6\. Verify external libraries via Context7

For every external library, framework, or versioned dependency the architecture is going to commit to (call out by name, depend on a specific behavior of, or design around the API surface of), verify the relevant API or behavior against current documentation via Context7 before designing against it.

The verification flow:



mcp\_\_claude\_ai\_Context7\_\_resolve-library-id — pass the library name; receive a Context7-compatible library ID.

mcp\_\_claude\_ai\_Context7\_\_query-docs — pass the library ID and a specific question (the behavior, API, or pattern you need to verify). Read the returned content.

Capture for the architecture document: the library, the version (or date of verification), and what specific behavior or API surface was confirmed.



Skip this phase only when the architecture has no external library dependencies (rare; even an architecture for a tool-building project usually depends on the Claude Code platform's documented behavior). When you skip, record why in the architecture's Limitations section.

If Context7 is unavailable or returns malformed output for a library you must verify, this is a tool-failure stop condition — halt with a diagnostic message naming the library that couldn't be verified.

Capture what you verified, not just the fact that you verified. "Verified the React useEffect behavior via Context7 on /facebook/react at 2026-05-08, confirmed cleanup function runs on unmount and on dependency change" is auditable. "Verified via Context7" is decoration on the premise axis.

7\. Detect and surface spec problems

Compare the spec against the codebase reality (Phases 3, 4) and the named standards (Phase 5). Three categories of problem can surface, and the agent's response to each is different:

Hard logical contradiction. The spec contains two requirements or constraints that cannot both be true in any valid architecture. Example: R3 mandates synchronous request handling on the same code path that R7 mandates streaming async behavior; the constraints section forbids local file writes but R5 mandates SQLite persistence. Stop. Construct the resolution using Clear Thought MCP's structuredargumentation tool (thesis-antithesis-synthesis) — see the Reasoning support section. The thesis is the recommended resolution; the antithesis is the strongest counter-argument; the synthesis is the resolution that survives the antithesis. Surface the contradiction with quotes from the spec, the structured argument, and your recommendation. Wait for user input. Do not silently pick a resolution.

Hard standard-vs-spec contradiction. The spec asks for something that a named governing standard says is wrong. Example: spec mandates SHA-256 for credential storage but OWASP Password Storage Cheat Sheet says use argon2id; spec mandates query-string token delivery but OAuth 2.0 RFC 6749 forbids it. Stop. Construct the resolution via structuredargumentation as above. Surface the conflict with quotes from the spec and from the standard, the structured argument, recommend the standard-aligned approach, and wait for user input.

Soft ambiguity. The spec leaves a design question genuinely open between valid architectures. Example: spec doesn't mandate a specific framework for the API layer when multiple frameworks satisfy the requirements; spec doesn't specify the data persistence boundary between in-memory and durable storage. Do not stop. Choose an approach that best serves the goal. Optionally use structuredargumentation to stress-test the choice. Record the resolution in the architecture document's Design decisions section in the five-part decision format. Proceed.

Watch the trap. Soft ambiguity dressed up as hard contradiction is a way to ask permission to skip work the architect should be doing. Soft ambiguity is when both/all interpretations produce valid architectures; hard contradiction is when no architecture can satisfy the spec as written. The criterion is whether any valid architecture exists, not whether the choice is hard.

8\. Reason through hard decisions

This phase is mandatory for every architecture document. The architecture invokes Clear Thought MCP's sequentialthinking tool for general decomposition reasoning over hard architectural decisions — see the Reasoning support section's row for Phase 8 for the discipline.

The trigger criteria for which decisions warrant structured sequentialthinking treatment within the invocation:

Apply sequentialthinking treatment to:



Decisions where multiple valid architectural approaches exist and the wrong choice creates rework downstream.

Decisions where a foundation problem in the codebase could be fixed in this architecture or worked around, and the choice matters.

Decisions where the interaction between components is non-obvious and getting it wrong breaks things silently.

Decisions where you are about to recommend an approach and realize you haven't actually evaluated the alternatives.

Decisions involving a quality characteristic trade-off (e.g., performance vs. maintainability, consistency vs. availability) that requires reasoning, not pattern-matching.



Don't apply sequentialthinking treatment to:



Decisions with one obvious correct approach by the named standards.

Decisions that are reversible at low cost during implementation.

Routine architectural choices where the standard is clear.



If no decisions in this architecture meet the criteria above, the Design decisions section explicitly states that and explains why (e.g., "This architecture's decisions all had clear correct approaches under the named standards; no sequentialthinking treatment was warranted for any individual decision"). Silent omission is non-compliance.

For decisions that do warrant sequentialthinking treatment, the structured reasoning trace does not stay in the scratchpad. The conclusion and the structured reasoning that led to it both go into the architecture document's Design decisions section. Watch the decision-hiding trap. A conclusion in the document without the reasoning is brittle. A reasoning trace without the conclusion is unhelpful. Both belong.

For other reasoning kinds — knowledge-state assessment (Phases 1–2), first-principles derivation (Phase 5 when no formal standard applies), foundation-problem characterization (when foundation problems are flagged), dialectical resolution of hard contradictions (Phase 7), hypothesis-driven security reasoning (Phase 9), multi-criteria evaluation of 3+ alternatives (Phase 10), multi-perspective pre-delivery review (Before delivering / Gate A) — see the Reasoning support section for which Clear Thought tool is mandatory at which phase. This phase covers sequentialthinking specifically; the other tools have their own invocation points.

9\. Construct threat model when security in scope

Security is in scope when the system being architected handles credentials, tokens, session state, personal data, multi-user access control, trust boundaries, or external integrations. When security is in scope, build the threat model before designing security controls. This ordering is mandatory — controls without a threat model are security theater, because the controls aren't tied to anything they're defending against and can't be evaluated for whether they actually defend against it.

The threat model is built using Clear Thought MCP's scientificmethod tool — see the Reasoning support section. Each threat is structured as observation → question → hypothesis (with variables, assumptions) → experiment (controls, predictions) → analysis → conclusion. This replaces free-text threat descriptions and makes threat reasoning auditable as hypothesis-driven inquiry rather than narrative pattern-matching.

The threat model identifies, through structured scientificmethod application:



Attackers. Who are they? External attackers without credentials, authenticated users escalating privilege, insider threats with legitimate access, compromised dependencies.

Targets. What are they after? User credentials, session tokens, personal data, financial data, trust relationships with other systems, availability of the service.

Blast radius. What's the cost of each compromise? Full data leak, lateral movement, financial loss, regulatory exposure, reputational damage.



Each security-related architectural decision in Phase 10 ties to a specific threat in the model. A control without a threat is a control without justification — record it in the architecture, but flag it.

When security is not in scope, skip this phase. Do not write a threat model for a system without security surface — performative threat modeling is the standards-decoration trap applied to security.

10\. Make design decisions in the five-part decision format

For every non-trivial architectural choice — components, technology choices within constraints, integration approaches, trade-off resolutions, API surfaces, data models, security controls — write the five-part justification:



The decision. What was chosen and exactly where it applies — component name, layer, file or directory location if known, interface or contract.

The authoritative standard. A named specification, RFC, OWASP guide, NIST publication, ISO standard, or industry consensus documented in a specific source. When no formal standard applies, the anchor is a first-principles articulation produced via mentalmodel(first\_principles) (per the Reasoning support section) — name the goal of the work, name the local-optimum shortcut you considered, name why the chosen path serves the goal and the shortcut wouldn't. Both forms are acceptable; what is not acceptable is no anchor at all.

Why this standard applies here. One to two sentences connecting the standard (or the first-principles anchor) to the specific architectural problem. Generic restatement of the standard does not satisfy this — it must explain why this particular architectural situation calls for this particular standard.

What this decision is NOT — and why. The alternatives that would be wrong for this situation, named explicitly with the reason each is wrong. Copying a correct recommendation is easy. Explaining why the wrong alternatives are wrong demonstrates actual understanding rather than lookup. If you cannot name and reject at least one wrong alternative for a non-trivial decision, you have not evaluated the decision — you have pattern-matched to a default.

Premise verification. What was checked, against what source, with what result. Use one of: file:line read (cite the path and line range and what the file content showed), grep query and result (cite the query and the matches), Context7 lookup (cite library, version, date, and what behavior was confirmed), test reproduction (cite the test, the input, and the observed output), CodeGraph query and returned data (cite which query and what was returned), or codebase-RAG query and result count (cite the query and what came back). Decisions resting on no factual premise about existing source mark the slot "no factual premises — pure design choice." This slot makes premise-correctness evidence per-decision auditable rather than collected in a separate output section.



What counts as non-trivial. Any decision where a wrong choice could cause a security failure, data loss, operational failure, breaking change, integration mismatch, or significant rework. When unsure whether a decision is non-trivial, treat it as non-trivial.

Trivial decisions (e.g., file naming convention within a component, internal helper function names) are recorded briefly without the five-part format. The architecture stays implementable without ceremony around obvious choices.

For decisions with three or more plausible alternatives that compete on multiple criteria (e.g., choosing among three frameworks where each scores differently on performance, ecosystem, learning curve, and operational complexity), use Clear Thought MCP's decisionframework tool (multi-criteria) — see the Reasoning support section. Multi-criteria scoring with explicit weights replaces narrative justification of why each alternative is wrong. The five-part decision format remains the structural home for the chosen decision; the decisionframework output lands in element 4 ("what this is NOT — and why") with the multi-criteria matrix replacing pure narrative.

For each design decision, also record the spec requirements it addresses (R# and/or Q# from the input spec). This produces the data the traceability matrix consumes in Phase 11.

Watch the standards-decoration trap and the deferred-decision trap. A decision whose standard slot lists OWASP / SOLID / a framework convention but where the architectural choice doesn't actually use that standard is decoration. A decision that defers the choice to "the implementer" or "the build phase" when the choice has cross-component consequences is the deferred-decision trap. Both are checked again in the auditability checklist before delivery.

10a. Quality characteristic mapping

Position: between Phase 10 (design decisions) and Phase 11 (write architecture document). The Phase 11 output requires a Quality characteristics addressed (ISO/IEC 25010:2023) table mapping each quality characteristic the architecture advances to how it is advanced. This phase produces the work that table reflects. Without this phase, the table can be filled in cosmetically after the fact — the standards-decoration trap applied to ISO 25010.

For each ISO 25010 quality characteristic the spec requires (per the spec's Q-numbered requirements), walk through three questions:



What does the spec demand for this characteristic? Read the relevant Q# requirements from the spec. If the spec is silent on a characteristic, the architecture has no obligation to advance it (it does not need to appear in the table).

What do the design decisions in Phase 10 do for it? Identify which decisions advance the characteristic and how. Record the decision number (D1, D2, …) and the mechanism by which it advances the characteristic.

Are there gaps? A characteristic the spec requires but no design decision addresses surfaces here as a gap.



Gaps produce a return to Phase 10 to add the missing design decision — they do not produce a row in the output table marked "not addressed despite spec requirement." The mapping is iterative with Phase 10 if needed. When all required quality characteristics either map to design decisions or are explicitly negotiated as deferred (with reasoning), the mapping is committed and Phase 11's quality characteristics table reflects this work.

Quality characteristics deliberately not addressed (because the spec defers them or because they are out of architecture scope) are recorded in the table with reasoning, not silently omitted.

This phase does not invent quality characteristics not in the spec. The architecture advances what the spec requires; characteristics the spec doesn't require do not need to appear in the table.

10b. ASVS verification mapping (when security is in scope)

Position: alongside Phase 10a, between Phase 10 (design decisions) and Phase 11 (write architecture document). Fires only when security is in scope (per Phase 9's threat model). When security is in scope, the Phase 11 Standards governing this architecture table will include OWASP ASVS. ASVS provides verification requirements (authentication, session management, access control, input validation, error handling, logging, etc.) that should drive architectural choices in any system with a security surface. Without this phase, ASVS appears in the standards list and may not appear in any specific decision — the standards-decoration trap applied to security.

For each ASVS verification requirement applicable to the system's security surface (the surface defined by Phase 9's threat model), walk through:



Does a Phase 10 design decision address this requirement? If yes, record the requirement-to-decision mapping (which ASVS requirement is satisfied by which design decision, and how).

If no, is the requirement applicable to this system? If the requirement applies but no decision addresses it, the requirement drives a return to Phase 10 to add a design decision. The architecture must specify how authentication is handled, how sessions are managed, how access is controlled — leaving these for the implementer is the deferred-decision trap.

If the requirement is out of scope or genuinely deferred to a downstream phase, mark it explicitly as deferred with reasoning. The Limitations section records the deferral.



The position symmetry with Phase 10a is deliberate: both 10a and 10b are post-design mappings of governing standards (ISO 25010, OWASP ASVS) to specific design decisions. Both protect against standards-decoration. Both produce returns to Phase 10 if gaps surface. Both commit before Phase 11 begins.

This phase does not fire when security is out of scope. A system without a security surface has no ASVS requirements to map, and the corresponding mapping section in the architecture document is absent.

11\. Write the architecture document

Now, with Phases 1–10 (plus 10a and 10b where applicable) complete, write the architecture as a markdown document with the following structure. Sections marked (required) appear in every architecture, even briefly. Sections marked (if applicable) are present only when the condition holds. Every required section is required because it carries a structural piece of evidence that makes the architecture auditable on either the standards axis or the verification axis; do not omit a required section without the architecture failing its own delivery check.

\# Architecture — \[Name]



\[Optional: Revision note at top — only when this architecture revises a prior version]



\## Goal — what this architecture serves

&#x20;  \*(required)\* — one paragraph stating what the architecture is for, what makes it correct as opposed to merely complete, and the local-optimum trap that threatens it most directly. This is the anchor — every decision below must serve this goal.



\## Scope

&#x20;  \*(required)\* — three subsections explicitly stating the architecture-level position on coverage. \*\*In scope:\*\* what this architecture covers. \*\*Deferred:\*\* what is left for later phases (plan, build, maintenance), with reasoning for each deferral. \*\*Out of scope:\*\* what is explicitly excluded, with reasoning. The traceability matrix continues to mark per-requirement scope; this section states the architecture-level summary so a reader can see the scope position without having to read every traceability row.



\## Inheritance from existing precedents

&#x20;  \*(if applicable)\* — when the architecture is one of a family with established prior versions, list the decisions inherited from precedent in a table, with the precedent source and why each applies identically here. The remaining design decisions D1–D... are the genuine architectural work.



&#x20;  \*\*Family criterion.\*\* Two architectures belong to the same family when both criteria hold: (a) they address structurally identical problems within the same system (e.g., paired microservices that handle different domains within one platform), AND (b) they share the same architectural pattern (microservices, batch pipeline, CLI tool, event-driven, monolithic, etc.). Architectures in the same project but addressing different problems — or sharing a problem but using different architectural patterns — are not family. They are reference material; they are not precedents to inherit from. The Inheritance section is invoked only when both criteria hold; otherwise, prior architectures inform the design but do not produce a list of inherited decisions, and the section is omitted.



\## Components and structure

&#x20;  \*(required)\* — what the architecture is composed of, at the level needed for the implementer to start work without re-architecting. Component responsibilities, interfaces, data flow, integration points.



\## Quality characteristics addressed (ISO/IEC 25010:2023)

&#x20;  \*(required)\* — a table mapping each quality characteristic the architecture advances to how it is advanced (with the design decision numbers from the Design decisions section that perform the advancement). This table reflects the work done in Phase 10a. Quality characteristics deliberately not addressed are also named with reasoning ("performance efficiency: not addressed; the spec defers performance work to maintenance phase").



\## Design decisions

&#x20;  \*(required)\* — D1, D2, D3, ... each in the five-part decision format: (1) decision; (2) authoritative standard or first-principles anchor; (3) why the standard applies here; (4) what this decision is NOT — and why; (5) premise verification — what was checked, against what source, with what result, OR explicit "no factual premises — pure design choice" when the decision rests on no factual claim about existing source. For each decision, record the spec requirements (R# and/or Q#) it addresses. Knowledge-state baseline (from Phase 1–2 metacognitivemonitoring), structured-reasoning traces from Clear Thought tools (sequentialthinking, decisionframework, structuredargumentation, scientificmethod, debuggingapproach, mentalmodel), and the pre-delivery multi-perspective review (Before delivering Gate A collaborativereasoning) all land here as Design decisions section entries.



\## Threat model

&#x20;  \*(if applicable — when security is in scope per Phase 9)\* — attackers, targets, blast radius, structured per scientificmethod (observation, question, hypothesis, experiment, analysis, conclusion). Threats first; controls in the Design decisions section reference these threats.



\## ASVS verification mapping

&#x20;  \*(if applicable — when security is in scope per Phase 9)\* — table mapping each applicable ASVS verification requirement to the design decision (D#) that addresses it, or to "deferred to plan / deferred to maintenance / out of architecture scope" with reasoning. This table reflects the work done in Phase 10b.



\## Traceability matrix

&#x20;  \*(required)\* — a table mapping every R# and Q# from the input spec to one or more design decisions, OR explicitly to "deferred to plan / deferred to maintenance / out of architecture scope" with reasoning. Every spec requirement is accounted for. No silent omissions.



\## Limitations and trade-offs

&#x20;  \*(required)\* — known limitations of the architecture (cases where the design will not work well or will need revisiting), trade-offs accepted (where one quality characteristic was prioritized over another and why), and gaps acknowledged on both axes (decisions that couldn't be grounded in a formal standard or first-principles articulation; claims that couldn't be verified with available tools; rigor the user explicitly waived per the Handling user requests to skip rigor subsection). This is the gap-acknowledgment section per the Output contract above.



\## Standards governing this architecture

&#x20;  \*(required)\* — a table with three columns: standard, source (file path for project-internal, publication identifier for external), what the standard governed in this architecture. Every standard cited anywhere in the document appears here. This is the audit table.



\## Status of this architecture

&#x20;  \*(required)\* — a brief section confirming the architecture passes the methodology's Design → Build quality gate (every non-trivial decision named a standard, alternatives stated, premise verified, traceability complete) and naming what comes next (Build phase — write the plan via /expert-plan).

Place the file where the project already keeps architectures if there's an established location; default to docs/architectures/architecture-\[kebab-case-name].md otherwise, where the kebab-case name matches the spec's name when derivable (e.g., spec spec-some-tool.md → architecture architecture-some-tool.md) or is otherwise derived from the spec's stated subject.

If the project has no architectures directory, create the default docs/architectures/ before writing — but only if docs/ already exists. If docs/ does not exist, propose a location to the user and stop. Do not create top-level project structure silently.



Before delivering

The architecture document passes through three gates before delivery, plus a parallel local-optimum trap audit. All three gates must pass independently and the trap audit must come up clean. A document that passes one gate does not pass the others by inference; each gate tests a distinct property.

Gate A — Does the architecture enable downstream work?

The architecture is the contract for Build. It serves three consumers, each of whom depends on the document's having specific properties. This gate is evaluated using Clear Thought MCP's collaborativereasoning tool (per the Reasoning support section), invoking three personas — planner, reviewer, stakeholder — and using each persona to review the architecture from that consumer's perspective.



Implementer (planner persona). Can a planner read this and produce concrete file-level implementation steps without making architectural decisions inline? An architecture that requires the planner to architect is not finished. The planner persona reads with the question "where would I have to make an architectural call inline?" and surfaces every place that question has a non-empty answer.

Reviewer (reviewer persona). Can a reviewer check a build against this and reach a defensible conclusion about whether each component, decision, and contract is satisfied? An architecture without traceable decisions is unreviewable. The reviewer persona reads with the question "if I had to verify this build against this architecture, would I know what to look for?" and surfaces every component or decision where the answer is unclear.

Stakeholder (stakeholder persona). Can a stakeholder read this and know how the spec is being satisfied, what trade-offs were made, and where the work could break? An architecture without explicit trade-offs is opaque to non-implementers. The stakeholder persona reads with the question "do I understand the choices that were made and what they cost?" and surfaces every trade-off that's implicit rather than named.



The collaborativereasoning synthesis lands in the architecture document's Design decisions section as a pre-delivery review entry. If no perspective-specific gaps surface across all three personas, the Design decisions section attests that all three perspectives were checked and found no gaps. Pass condition: yes to all three perspectives. A "no" from any persona produces a fix to the document, not a flag in the document.

Gate B — Is the architecture's compliance auditable from the document alone?

A reader who was not present during architecture work must be able to answer each question below by pointing to a specific section, table row, or annotation in the document. Subjective interpretation of the document is failure.



Which named standards govern this architecture, and what does each govern? (answerable from: Standards governing this architecture table)

Where does each non-trivial decision come from — spec requirement, named standard, or first-principles anchor? (answerable from: Design decisions section, element 2 of each decision)

For each non-trivial decision, what alternatives were rejected, and why? (answerable from: Design decisions section, element 4 of each decision)

For each non-trivial decision, what factual premises was it verified against, and how? (answerable from: Design decisions section, element 5 of each decision — Context7 citations with library and version/date, codebase-RAG queries with results, CodeGraph queries with returned data, Read of specific files, grep queries with matches, test reproductions, OR explicit "no factual premises — pure design choice")

Which decisions involved structured reasoning (sequentialthinking, decisionframework, structuredargumentation, scientificmethod, debuggingapproach, mentalmodel, metacognitivemonitoring), and what did the reasoning produce? (answerable from: Design decisions section, with structured-reasoning traces inline)

What couldn't be grounded in a named standard or verified against current source? (answerable from: Limitations and trade-offs section)

Is every spec R# and Q# accounted for? (answerable from: Traceability matrix)

When security is in scope, is every applicable ASVS verification requirement mapped to a design decision or explicitly deferred? (answerable from: ASVS verification mapping table)



Pass condition: every question above is answerable from the document alone by pointing to a specific section. A question that requires subjective interpretation of the document is a Gate B failure.

Gate C — Does the document satisfy the structural checklist?

The structural checklist is the final mechanical verification.



Every non-trivial decision has all five parts of the decision format (decision; authoritative standard or first-principles anchor; why standard applies here; what this is NOT and why; premise verification — what was checked, against what source, with what result, OR explicit "no factual premises — pure design choice").

Every Context7-verified claim cites what was verified and when (library, version, date), not just "verified via Context7."

Every codebase-RAG query cites the query and the result count, not just "checked codebase-RAG."

Every CodeGraph query cites which query and what was returned, not just "checked CodeGraph."

File paths and external references are confirmed, not assumed.

No internal reasoning artifacts, self-corrections, or scratchpad content remain in the document.

The Threat model section is present when security is in scope and absent when it isn't.

The ASVS verification mapping section is present when security is in scope and absent when it isn't.

The Traceability matrix accounts for every R# and Q# from the input spec.

Every Clear Thought tool the Reasoning support section flags as mandatory has been invoked at the right phase, with the structured-reasoning output landing where the table specifies (or with an explicit attestation when an invocation's trigger criteria are not met).

The Scope section names what is in scope, deferred, and out of scope with reasoning for each.

The Standards governing this architecture table includes every standard cited anywhere in the document, with what each governs.

Every required output section is present, or explicitly attested as genuinely empty for this architecture (e.g., "the Limitations section is empty for this architecture because the design has no known limitations under the named standards, no accepted trade-offs against quality characteristics the spec requires, and no gaps on either axis").



Pass condition: every checklist item is satisfied, or its absence is explicitly attested.

Local-optimum trap audit (parallel to A/B/C)

For each of the five traps named at the top of this command, ask the binary question. A "yes" produces a fix to the document, not a flag in the document.



Codebase-mirroring trap. Did any architectural choice get justified by "this is how the codebase already does it" without naming the engineering standard the existing pattern is correct against? If yes, re-derive the choice from the named standards.

Pattern-cloning trap. Did any structural element of the architecture come from a prior architecture's shape rather than from this spec's requirements? If yes, name the spec requirement that justifies the element here, or remove it.

Decision-hiding trap. Is there any non-trivial decision in the architecture whose reasoning lives only in the working context, not in the document? If yes, surface the reasoning.

Standards-decoration trap. Is any named standard in the Standards table not actually driving a specific decision in the architecture? If yes, find the decision it should be governing or remove the standard.

Deferred-decision trap. Is any non-trivial choice in the architecture left ambiguous for "the implementer" or "the build phase" to resolve when the choice has cross-component consequences? If yes, resolve it now.



Pass condition: no to all five traps.

If any of Gate A, B, C, or the trap audit fails, fix the document. Do not deliver an architecture that fails any of these checks — that is the failure mode the methodology output contract exists to prevent.



Output

Write the architecture file at the chosen path. After writing, confirm to the invoking session: the path of the file written, the section count, and a one-sentence summary of the goal the architecture serves. The user can then review the document directly.

Do not commit the file to git. Do not modify any other file (the spec stays as-is; any project-level governance documents like a capability inventory are updated separately as governance work, not as part of this tool's run). The only filesystem write is the architecture file itself.

What comes after

The architecture is the contract for Build. The next tool in the chain is /expert-plan, which consumes the architecture (plus the spec) and produces an implementation plan with concrete file-level steps. The architecture's traceability matrix tells the planner which decisions are settled; the architecture's Components and structure section tells the planner where the work happens; the architecture's Standards governing this architecture table is the registry the plan's per-step Source annotations point back to.

If you discover during this architecture work that the architecture isn't fully implementable — that an implementer would still need to make architectural decisions inline — that is a foundational issue, not a patch-level one: the architecture is not done. Fix it before delivering. Patch-level gaps (a missing component description, an incomplete traceability row) you fix in place. Foundational gaps (the wrong component decomposition, the wrong abstraction boundary) require returning to Phase 7 or earlier — the architecture's foundation was laid on incomplete context, and patching it forward leaves the foundation defect in place.

A correct architecture is the difference between a build that takes one cycle to produce and one that takes three. The cost of getting it wrong is paid downstream, in plans that can't be executed and reviews that find architectural defects. The cost of getting it right is paid here, in the work this process specifies

