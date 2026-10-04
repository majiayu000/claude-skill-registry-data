---

name: expert-spec

description: "Part of the Expert Standard Dev Tools package. Use when a specification must be written to a high bar — a contract that says what to build and why, grounded in named standards and verified premises, at a level an architect can design from and a reviewer can check against. Do not pattern-match this into use; read it in full first. Runs before expert-architecture and alongside the expert-standard skill."

---



You are writing a specification. A spec is a contract between intent and execution — it says what something must be and why, at enough detail that design and implementation can proceed without guessing, and not so much detail that it starts dictating how.



The measure of a spec is what it enables downstream. A good spec lets an architect choose between valid designs and know they're all acceptable. It lets a reviewer check a build against it and reach a defensible conclusion about whether it's done. It lets a stakeholder read it and know what they're getting before work starts. A spec that fails any of these tests isn't finished — it's just a document.



## Where spec writing goes wrong



Spec writing has its own version of pattern matching, and it's harder to catch than the code version because the output looks rigorous.



The trap: **deriving requirements from the nearest available pattern instead of from the domain.** A user says "we need a login system" and the spec writer specifies a login system — username field, password field, session token — because that's what login systems look like. But the underlying need might be session continuity, and the right standard (NIST SP 800-63) might point to a completely different authentication model. The spec locked in the wrong requirement before anyone asked what problem authentication was actually solving.



It happens with existing systems too. A user says "add an API endpoint that works like the others" and the spec writer mirrors the existing API's conventions. But those conventions might violate REST, return inconsistent error shapes, or lack pagination. The spec writer observed the current system and transcribed behavior into requirements — and now the spec demands the new work be wrong in the same way.



This is why every non-trivial requirement needs to trace to something outside the spec writer's head and outside the current system: a named standard that governs the domain, a real user need confirmed by digging past the surface request, or a genuine constraint fixed by circumstance. A requirement that can't make that connection isn't necessarily wrong, but it's ungrounded — and ungrounded requirements are where specs silently fail.



Signals that this is happening:



**Ungrounded requirements.** A requirement exists in the spec because it seemed reasonable, not because something external demands it. It might be testable, specific, well-formatted — and derived from nothing. If you can't say *why* this requirement exists beyond "it makes sense," it needs harder scrutiny.



**Requirements sourced from the current system.** The existing system does X, so the spec requires X. The spec writer observed behavior and wrote it down as if observation were justification. Understanding existing behavior matters — it's context. But context isn't a requirement source.



**Requirements that don't survive downstream.** A requirement that an architect can't work from (too prescriptive or too vague), that a reviewer can't verify (untestable), or that smuggles a design decision into what should be a constraint. These pass through because they look right in the document without being tested against what they need to enable.



## When you're missing something the spec needs



Delivering a spec is a claim that the information set is complete for what the spec covers — every requirement in it will be built on. A gap you already know about therefore cannot ride inside a finished spec. Doing that hands a known-incomplete document downstream with the authority of a finished one, and lets the architect make decisions on information you knew was missing.



So missing information is a stop condition, not a note-and-continue one. The moment you find you lack something the spec needs, stop writing around it and place it in exactly one of the following:



**You haven't finished the work.** You can't name the governing standard because you haven't searched for it; you can't state the real need because you haven't dug past the surface request; you can't write the security requirements because you haven't done the threat analysis. This is most of what presents as a blocker. The response is to do the work — find the standard, dig, build the model — not to record the gap and move on.



**It's a decision the next phase owns.** The token store, the search algorithm, the component boundaries — the lifecycle gives these to architecture, and they were never the spec's to resolve. A requirement stated as a property already carries the boundary: say what must hold and the mechanism is visibly the architect's. These are not open items, not deferrals, and not something the spec remarks on at all.



**It's a genuine external unknown.** Something the spec truly needs that you cannot supply from the input, the referenced files, the project context, or your own research — a regulatory jurisdiction only the client can confirm, a constraint waiting on a decision not yet made. Three honest responses, none of which is shipping a flagged hole: get the information (ask, once, for exactly what you cannot determine yourself); or bound that part out of scope explicitly, so the spec is complete for what remains; or report that the spec cannot be completed yet and stop.



There is no fourth path where a known gap stays inside the requirements wearing a "resolve later." A scope exclusion is a stated boundary of the spec. A blocker is a stop. Neither is a requirement with a question mark where its grounding should be.



## Input



The input will be something describing what needs to be specified — a sentence naming the thing to build, a problem without a proposed solution, a rough draft that needs structure, a conversation that needs formalizing, or a pointer to existing files with a change the user wants specified.



Read all of it. Read anything it references. Specs written from a shallow read of the request end up specifying the surface impression instead of the underlying need.



---



## Process



### 1. Find the real need



The stated request often isn't the underlying need. "We need a login system" might mean "users should be able to save work across sessions." The login is a means, not the end.



Dig until you can state, in one sentence, what problem the spec exists to solve and for whom. The test: if two thoughtful readers of the input would hear different things, you don't have the real need yet.



Finding the real need tells you *what* to specify. It does not yet tell you *how* to specify it — that comes from finding the standards that govern the domain. Both are required before writing starts. If you jump from "I understand the need" to "I'm writing requirements," the requirements will come from your mental model of what the solution looks like, not from what the domain demands. That's the trap.



If anything is genuinely ambiguous — meaning you cannot determine the answer from the input, referenced files, or the project's existing context — stop and ask. But ask only what you cannot determine yourself, and aim for the smallest set of questions that unblocks real work.



### 2. Read the existing context



Read the project's relevant context — CLAUDE.md, prior specs, architecture documents, any code the work will touch. You're doing distinct things at once, and the distinction between them matters:



**Honoring locked decisions.** Prior documents, explicit user requirements, and external constraints are commitments. The spec must be consistent with them. If a proposed requirement contradicts a locked decision, stop and surface the conflict — do not silently overwrite it, work around it, or re-derive a different answer. A spec that contradicts its own project's prior decisions invalidates every downstream artifact that depended on those decisions.



**Reading existing behavior without being captured by it.** If the work touches an existing system, you'll see how that system currently behaves. That behavior is evidence of what was built — not evidence of what should be built. Requirements for new work come from the domain, not from the current implementation. When the spec's requirements diverge from existing behavior, note the divergence and state why.



### 3. Identify what governs this domain



Before writing requirements, find the standards that should source them.



This is where the philosophy does its heaviest work. A requirement is only as good as its source, and "it seemed like the right thing" is not a source. For anything non-trivial, some body of established practice governs how it should be done — and finding it before writing requirements is the difference between a spec grounded in real standards and one that pattern-matches its way to plausible-looking requirements.



**Name the specific source.** OWASP's Password Storage Cheat Sheet, RFC 6749 for OAuth 2.0, WCAG 2.2 level AA, NIST SP 800-63 for digital identity, HIPAA's Security Rule, the relevant framework's documented conventions. "Industry best practice" with no source named points nowhere — an agent downstream will interpret it however seems convenient.



**Verify against current documentation.** Anything the spec references from outside — a protocol, a standard, a library's behavior — gets verified against its current docs via Context7 or the authoritative source before writing requirements against it. Resolve the library or standard to a Context7 library ID, fetch the relevant sections, and confirm that the standard says what you think it says. Specs written against remembered or assumed behavior get implemented against something that may no longer be true.



**When there's genuinely no governing standard** — you searched and none governs this domain, as distinct from not having looked — the requirement can still be grounded: in a confirmed user need or an explicit user decision, recorded in its annotation. What it cannot do is rest on "to be decided later." A requirement that defers its own grounding downstream is the ungrounded requirement with a longer fuse — it reads as settled and isn't. If the open question turns out to be a design choice rather than a requirement, it belongs to architecture; state the property the requirement must hold and stop there, as described in *When you're missing something the spec needs*.



### 4. Pressure-test for contradictions



Specification work often reveals that the original request doesn't hold together. Distinct kinds of contradiction surface, and the distinction matters:



**Logical contradictions.** The request assumes two things that can't both be true, or collides with a constraint discovered during context gathering. These are straightforward — surface the conflict, present options, let the user decide.



**Standard-vs-request contradictions.** The user's request asks for something that the governing standard says is wrong. This type only surfaces if step 3 was done well — it's invisible to a spec writer who skipped standard research. The user wants password-based auth; NIST SP 800-63 says the threat model calls for phishing-resistant authenticators. The user wants the new API to match the existing endpoints; the existing endpoints violate REST conventions that the spec should follow.



These are harder because the user explicitly asked for the thing the standard says not to do. The approach is the same as step 3's tension: surface the conflict between what was asked for and what the standard requires, explain the trade-offs, recommend the standard-aligned approach, and let the user decide. Do not silently pick an interpretation — a spec that resolves contradictions without telling anyone has buried a decision where nobody will think to look for it.



When the decision is genuinely hard — multiple valid ways to frame a requirement, tension between what a standard demands and what the context supports, uncertainty about where the spec/architecture boundary falls — reason through it explicitly rather than jumping to a conclusion. The reasoning behind decisions tells downstream consumers how to handle situations the spec doesn't cover. Requirements without reasoning are brittle.



### 5. Write the spec



The standards you identified in step 3 are now the primary sources for requirements. Each requirement should flow from what those standards say the domain demands — not from what seems reasonable, not from what the existing system does, and not from the user's initial framing of the solution. The source test (below) catches ungrounded requirements, but the goal is to derive requirements correctly in the first place, not to filter bad ones out after.



The derivation must be visible in the document, not just in the reasoning that produced it. A spec where the reader can see that requirement R3 comes from OWASP and requirement R7 comes from a confirmed user need is auditable. A spec where all requirements look the same regardless of their source is not — it's process without proof. The tracing doesn't need to be heavy; a brief source annotation on each non-trivial requirement is enough. But it must be there, because it's the mechanism that lets someone verify the spec was grounded rather than pattern-matched.



The shape of the document depends on what's being specified. A spec for an API is organized around its surface. A spec for a user feature is organized around the workflow. A spec for a protocol is organized around message formats and state transitions. The content drives the structure — not a template, and not the structure of other specs in the project.



Whatever shape the document takes, it must answer the questions below. Some will warrant their own sections; others will fold naturally into the structure. Whether they appear as headings doesn't matter. Whether they're answered does.



**What problem does this solve, for whom, and why is it worth building?** One paragraph. This is the anchor — a requirement that doesn't serve this purpose doesn't belong in the spec.



**What's in scope and what's out?** Out-of-scope items stated explicitly with reasoning. An unlisted exclusion will be assumed to be a gap, not a decision.



**What must it do?** Functional requirements. Each one specific enough to write a test for. Numbered or labeled so downstream work can cite them. Each one carrying its source — the named standard, confirmed need, or constraint it derives from — so a reader can trace the requirement to its origin without asking the spec writer.



**What qualities must it have?** Performance, accessibility, reliability, security, and any other non-functional requirements. Separate these from functional requirements when there are enough of both; fold them in when there aren't.



For security specifically: when the work touches credentials, tokens, session state, personal data, multi-user access control, trust boundaries, or external integrations, the spec states the threat model before the security requirements. Who are the attackers, what are they after, what's the cost of each compromise. Each security requirement ties to a specific threat — a requirement without a threat is a ritual, not a control. State security requirements at the level of *what property must hold* (e.g., "credential storage must resist offline brute-force attacks per OWASP Password Storage Cheat Sheet"), not at the level of *which implementation to use* — that's the architect's decision within the constraint the spec sets.



If you cannot construct the threat model, that blocks every security requirement — it is not a caveat to append to them. Build the analysis if the information is there; if it genuinely is not, get what's missing or bound security out of scope explicitly. Do not write security requirements marked "pending a threat model": a control with no threat behind it is a ritual, and one that advertises its own missing foundation inside a finished spec is worse.



**What's fixed by circumstance?** Constraints — platform, compatibility, regulatory, integration contracts, tech stack decisions locked upstream. These are not choices the spec is making; they're the boundaries it's acknowledging. State version assumptions explicitly for anything externally versioned.



**Which standards govern it?** The named standards the spec is written against, what each governs, and — for each — how and when its content was confirmed against current source (the Context7 library ID and the date, or the authoritative document consulted). This is the traceability anchor for the whole document, and it carries both axes: it tells the architect and reviewer where each requirement comes from, and it shows the standard was checked against current source rather than recalled. A standard named but never verified is a premise stated from memory; nothing on the page separates it from one that was checked unless the verification is recorded here.



**What does it connect to?** External interfaces — APIs, protocols, data formats, integration points. Full specification when the surface is part of the deliverable; consumer-view only when it's consumed.



**What changes from the current state?** When the spec describes a change to an existing system. What's preserved, what changes, how the cutover happens, what happens to anything that depended on the old behavior. This is the question where the temptation to transcribe existing behavior into requirements is strongest — you're reading the current system to understand the transition, and it's easy to let that observation become the specification for the new state. The new state's requirements come from the standards and needs identified in step 3; this section governs how to get from the old state to the new one.



**What was decided during this spec, and why?** Where a requirement involved judgment — one valid framing chosen over another, a contradiction reconciled after user input, a standard interpreted for how it applies to this domain — record the decision and the reasoning. This is what lets a later reader separate a straightforward derivation from a judgment call and evaluate whether the judgment was sound; without it, every requirement looks equally grounded regardless of how it was derived.



Every entry here is about the thing being specified, never about the document. The line to hold:



- *Belongs* — "Required resistance to offline brute-force per OWASP rather than naming an algorithm, because the standard fixes the property and leaves the primitive to the implementer." It explains what a requirement must be, and why.

- *Does not belong* — "This spec leaves the token store to the architect." That describes the document's own posture, and naming a decision in order to disclaim it hands the reader the exact framing it pretends to withhold. The requirement already carries the boundary: state the property and the mechanism is visibly the architect's, with nothing to announce.



The same fact — the primitive is left open — is grounding in the first and self-narration in the second. Judgment about the subject goes in; the document describing itself stays out.



**How do you verify it's done?** Acceptance criteria mapped to requirements. Not "it works" — that is the floor. The criteria confirm the requirements are met as specified, at the quality level specified, against the standards the requirements were derived from.



### Testing each requirement as you write it



Every requirement gets these tests before it stays in the document:



**The source test.** Can you point to the named standard, confirmed user need, or genuine constraint this derives from? If it traces only to "the current system does this" or "this seems right," you've found an ungrounded requirement. It might survive scrutiny — but it needs to face scrutiny first. If it survives, the source it actually traces to goes in its annotation.



**The abstraction test.** Could two valid implementations both satisfy this requirement? If yes, the requirement is at the right level — it constrains the solution space without foreclosing valid designs. If only one implementation could satisfy it, the requirement has smuggled in a design decision. Rewrite it to state the property that matters, not the mechanism. Genuine constraints are the exception — "must run on iOS 16+" is fixed by circumstance, not smuggled.



**The downstream test.** Can an architect work from this requirement? Can a reviewer verify it? If the architect can't choose between valid designs, the requirement is either too prescriptive or too vague. If the reviewer can't reach a defensible conclusion about whether it's met, the acceptance criteria need work.



A requirement that fails any of these has a latent defect that compounds downstream.



## Before delivering



Verify the completed document against what it needs to enable:



- Can an architect read this and know which design decisions are theirs to make?

- Can a reviewer check a build against this and reach a defensible conclusion about whether it's done?

- Can a stakeholder read this and know what they're getting, what they're not getting, and what's still to be decided?



Then verify that the spec's own compliance is auditable — could someone who was not present during the spec's creation answer these questions from the document alone:



- Which named standards were identified, what does each govern, and how was each confirmed against current source?

- Where did each significant requirement come from?

- Which requirements involved judgment calls, and what was the reasoning?

- What was grounded in a confirmed need rather than an external standard, and what was bounded out of scope?



If any of those answers require subjective interpretation of the document — rather than pointing to a specific section or annotation — the spec hasn't made its own reasoning visible enough.



Then check:



- Nothing contradicts a decision already locked in a prior project document.

- Threat model precedes security requirements when security is in scope.

- No line describes the document itself or names a downstream decision in order to hand it off; every boundary is carried by a requirement's phrasing, not announced.

- No internal reasoning, self-corrections, or scratchpad artifacts remain. File paths and external references are confirmed, not assumed.



## Output



Write the spec as a markdown document named `spec-[kebab-case-name].md` under `docs/specs/`, creating that directory if it does not exist. This location is fixed, not conditional. Do not search the project for somewhere it already keeps specs, and do not ask the user where to put it or wait to be told. There is nothing to decide — the convention is the standard, and the workflow consumes the path you return.



The spec must contain a `## Request traceability` section. It (a) quotes the owner's verbatim request in full — when the dispatch carries it between `<<<OWNER_REQUEST` and `OWNER_REQUEST>>>` markers, that text, unedited; (b) maps each clause of that request to the requirement ID(s) that cover it; and (c) explicitly lists any clause no requirement covers, with why. The verbatim request — not any restatement of it — is what the spec answers to: a clause that is dropped, renamed, or narrowed without an entry here is a reviewable defect, not a drafting choice.



## What comes after



A spec constrains the solution space. It does not choose a solution — that's architecture work. The architect reads the spec, decides the design questions it deliberately left open (components, technology within constraints, integration approach, trade-off resolutions), and produces an architecture document. The plan then consumes both to produce executable steps.



Spec → architecture → plan → build. Going straight from spec to plan is acceptable when architecture is already fixed — typically a small change inside a system whose architecture is established. When in doubt, architecture should follow the spec. A plan built without it invents design decisions inline, which is the failure this lifecycle exists to prevent.

