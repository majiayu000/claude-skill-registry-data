---
name: thatch-ticket-description
description: Draft a ticket description (SYNOPSIS / PROBLEM / BACKGROUND / PROPOSED APPROACH / ACCEPTANCE CRITERIA / RELEASE PLAN / VALIDATION / DEPENDENCIES / NOTES) with bold and italic emphasis on the phrases that carry the meaning, so a reader skimming only the emphasized fragments still gets the story. Use when the user asks you to write, draft, or file a ticket, issue, or work item (Linear or Jira). Do NOT use for PR descriptions (use thatch-pr-description), commit messages, or design docs.
---

# Writing ticket descriptions

## Core principle

Write for humans. Not for LLMs. Not to impress. Not to pad.

Every sentence earns its place or gets cut. Plain English over jargon. Concrete over abstract. Short over long. A ticket a human reads once and can start work from beats one that looks thorough but says nothing.

If a word does not help a human understand the work, it is dead weight. If a sentence restates the previous one, one is redundant. If a phrase sounds smart but you cannot explain it in simpler words, it is a buzzword. Cut, replace, or simplify.

Target a 7th-grade reading level. Not because the reader is dumb, but because plain prose is faster to read and harder to misread. Short sentences, common words, one idea each. The concepts stay technical; the language stays simple.

## The reader

You are writing for two people who share one trait: neither has your context, and neither knows this subsystem's jargon.

The first reader is a **lead or product manager** scanning a backlog. They decide priority, sequence, and assignment. They read SYNOPSIS and PROBLEM, skim ACCEPTANCE CRITERIA and DEPENDENCIES, and move on. They have 30 seconds per ticket in a planning context. They know general engineering vocabulary but may not know subsystem-specific acronyms or terms.

The second reader is an **implementer** picking up the ticket cold. They need to start work without coming back to ask "what did you mean by..." They read everything, carefully, and the ticket is their starting specification. They may be new to the subsystem and need terms defined.

The description is not a design doc. It is a specification that makes work startable. A design doc (when one is warranted) may live in repo docs, Linear, Notion, Archbee, Google Docs, Figma, or another system; link it from the ticket instead of inlining it. The ticket's job is to define the problem, propose a direction, and set the gates that define "done."

Each section has one job:
- SYNOPSIS: orient to the class of work and affected area.
- PROBLEM: make the reader agree there is something worth solving.
- BACKGROUND: give the implementer the context they would otherwise re-derive.
- PROPOSED APPROACH: set the direction without over-constraining the implementation.
- ACCEPTANCE CRITERIA: define "done" as observable, testable bullets.
- RELEASE PLAN: sequence the rollout when prod coordination is needed.
- VALIDATION: define how to verify the change in the deployed system.
- DEPENDENCIES: explain ordering constraints, not just list them.
- NOTES: flag scope limits, intentional non-goals, and things that look in-scope but aren't.

Each section builds on the previous one. The reader should never encounter a concept in section N that was not introduced in section N-1.

## Structure

Sections, in order: SYNOPSIS, PROBLEM, BACKGROUND (conditional), PROPOSED APPROACH, ACCEPTANCE CRITERIA, RELEASE PLAN (conditional), VALIDATION (conditional), DEPENDENCIES (conditional), NOTES (conditional).

**SYNOPSIS, PROBLEM, PROPOSED APPROACH, and ACCEPTANCE CRITERIA are mandatory.** A small ticket gets short sections, not fewer sections. Conditional sections appear only when warranted; omit them when empty. Never emit an empty header.

**Scale the body to the work's complexity, not its size in files or lines.** Estimate complexity by how much new mental model the implementer must build (see the point-based budgets in Length and style). A one-line fix gets a one-line PROBLEM, a one-line PROPOSED APPROACH, and one or two acceptance criteria. A multi-PR feature gets full sections with real depth. The implementer should be able to start work after reading the ticket, but they should not have to read a novel to fix a guard clause. Most of this skill's guidance exists to tame large tickets; applying it wholesale to a small one produces exactly the bloat the skill warns against.

### SYNOPSIS

One to two lines. Orient only. The reader should come away knowing the class of work (bugfix, feature, refactor, investigation, cleanup) and the affected area.

SYNOPSIS may use subsystem-specific terms as scan anchors (that is its job). It does not define them. BACKGROUND (or PROBLEM, when there is no BACKGROUND) picks up that burden. An outsider who does not know the terms should still be able to orient from the plain-English nouns around them.

Include a ticket link if referencing a parent or related ticket. Do not link the ticket to itself.

### PROBLEM

Frame the harm. Lead with the conclusion, then provide the evidence, not the other way around. State what is wrong, then explain why. For example:

- "The export endpoint loads every row into memory before serializing, so a large tenant runs the pod out of memory" not "the endpoint allocates a slice per row, and with enough rows... which is why the pod runs out of memory."
- "This handler runs one query per result row, so a page of 50 items fires 51 queries" not "the handler loops over results issuing a query each time... resulting in an N+1 query pattern."
- "The retry loop has no cap, so a persistent failure spins forever" not "the loop re-enters on error without a counter... meaning it never terminates."

The reader should know what the problem is before they read why it happens.

No solution yet. The reader should finish this section agreeing there is something to address, even with zero code knowledge.

Cover three things, each in its own paragraph when the ticket has the complexity to warrant it:
1. **What is wrong**, concretely. Name the component, the behavior, and the failure mode.
2. **Why it matters.** Incident history, risk rating, customer impact, or "preventive: blocks a class of bug we keep almost-hitting."
3. **Hazard rating and motivation.** How likely is the bad outcome, and under what conditions? Then answer "why now?": if the risk is low, what motivates this ticket? A prior PR identified it as a follow-up, the API still permits a failure shape, or the next planned change would make it worse. The lead's question is "should I prioritize this?" - give them the answer. _PLAT-135's ticket did this well: it named the cross-wait, then said "why it never fired" and rated the window as once-per-process cold load._

A small ticket covers all three in a single paragraph; split into one paragraph per topic only when the content earns it.

If the problem is preventive (no current defect), say so plainly. Then say why it is worth fixing despite the low risk.

### BACKGROUND (conditional)

Context the implementer needs that is not part of the problem itself. Prior tickets, prior PRs, architectural constraints, decisions already made. This is the section that prevents the implementer from re-deriving what the ticket author already knows.

BACKGROUND is also where subsystem-specific terms and acronyms get defined on first use. If the ticket uses terms a newcomer to the area would not know (a crypto term like DEK, an auth term like the SAML assertion, a scanning term like a ScanRun, a results term like the frozen materialized view), define them here in a brief gloss on first appearance. After the first definition, use the term freely throughout the rest of the ticket. If there is no BACKGROUND section, definitions go in PROBLEM.

Link the source material the implementer needs. For repo files, use `github.com` links rather than relative paths; tickets render outside the repo. For external integrations, link the vendor docs for the exact integration touch points the ticket depends on (auth flow, webhook format, API endpoint, SDK call, cloud resource behavior). Also link any user-provided planning artifacts that define intent or UX: Linear, Notion, Archbee, Google Docs, Figma, or similar. Do not invent external docs; link what is relevant and available.

When referencing prior work, link the ticket or PR and state what it did and what it left behind. "PLAT-134 (#6838) made key I/O executor-explicit, removing the unconditional deadlock. One narrower hazard survived it" gives the implementer the full arc in two sentences.

Omit when the problem is self-contained. A one-line "follow-up from #6838" can live in PROBLEM instead.

### PROPOSED APPROACH

The design concept. Not a full implementation plan. Enough that the implementer knows the direction: "load key material outside the mutex" not "restructure ActiveKey to use cachedKey/publish helpers with a publish function that zeroizes the loser's DEK." The implementer writes the implementation plan; the ticket sets the compass heading.

Present each mechanism in one short paragraph: what it does, plus the constraint that justifies its existence. Keep a justification when it answers an objection the reader will have (a lock that looks redundant, a retry that looks pointless). Compress failure-mode sagas to their consequence: "a leaked lock blocks every later attempt" carries what a paragraph of driver internals would. Reasons of the form "why not X" (no metric, no kill switch, no singleflight) go in NOTES as declined alternatives.

For investigative tickets, this is "investigate X and propose a solution" rather than a concrete approach. Say so explicitly so the implementer knows the ticket expects analysis before implementation.

This is where the ticket diverges most from a PR description. A PR description describes a change that already happened. A ticket proposes one that hasn't. The prose is prescriptive ("the fix should...") rather than descriptive ("this PR moves...").

### ACCEPTANCE CRITERIA

The checklist. Each criterion is a bullet, testable and concrete. These are what the implementer and reviewer use to decide "done." Ordered by dependency where it matters.

Good criteria name the **observable behavior**, not the implementation:
- "no DB or KMS I/O occurs while km.mu is held" (observable, testable)
- "a regression test demonstrates that a pool-path cold load cannot block transaction-path callers" (observable, testable)

Bad criteria are vague:
- "improve the locking situation" (untestable)
- "restructure ActiveKey" (implementation detail, not a behavior)

If a criterion's test design is non-obvious, name the test shape: "SetMaxOpenConns(1) with the connection held by a tx that also resolves the key." This gives the implementer the test design without dictating the implementation. "Tested explicitly" is not a test shape.

Keep the list coarse: three to seven criteria cover most tickets. This section defines "done"; it is not a test inventory. Merge parallel checks that verify the same behavior under different triggers. Drop criteria that restate PROPOSED APPROACH as a checklist - the criterion must add an observable gate, not echo the design.

### RELEASE PLAN (conditional)

Rollout strategy for tickets that change production behavior. Only when the change touches prod in a way that requires coordination. Covers:
- Feature flags (name, default state, per-tenant overrides if relevant).
- Migration ordering (what must deploy before what, and why).
- Deploy sequence (which services, in what order).
- Rollback path (what to do if it goes wrong).

A pure internal refactor with no operator-visible behavior change does not need this section. Neither does a change whose rollout is a normal deploy: if the only available bullets say "nothing special happens," omit the section - its absence is the nothing-special signal. A migration that gates on a backfill completing, or a revert that is not free, does need it.

### VALIDATION (conditional)

How to verify the change is correct in the deployed system. Distinct from acceptance criteria (which are about the code) because validation is about the **deployed system**. Covers:
- Monitoring dashboards or panels to watch.
- Metrics or signals that confirm the change is live and correct.
- Smoke tests or manual verification steps.
- The specific signal that says "this shipped and is working."

Only when prod verification is non-trivial. A pure refactor with good tests does not need this. A backfill worker that runs for days post-merge does.

### DEPENDENCIES (conditional)

The tracker's blocker links carry the what; this section carries only what links cannot. Write a bullet when there is a _why_ the link cannot express: "PLAT-125 partitions by location_fingerprint, so it can only run after backfill completes (count == 0), not merely after PLAT-124 merges." That kind of nuance is what prevents a well-intentioned lead from reordering the queue. "Blocked by PLAT-126" with nothing to add is the tracker field - set the link there and omit the bullet.

Distinguish hard data dependencies (cannot run until X completes) from soft dependencies (should run after X for cleanliness, but technically works independently). Say which kind it is.

If every bullet would restate a tracker link, omit the section and set the links.

### NOTES

Always a `## NOTES` markdown header. Never a bare `Notes:` line ending a section.

Use NOTES for:
- Intentional non-goals (things that look in-scope but are deliberately excluded).
- Scope limits (what this ticket does NOT do).
- Consciously declined alternatives (approaches considered and rejected, with a one-line reason).
- Context that doesn't fit any other section but would cause confusion if omitted.

One bullet per item. Bold the **leading noun** in each bullet as the scan anchor.

Each bullet is either a short flag or a self-contained explanation. A short flag names the thing and points to where the full rationale lives. A self-contained explanation states the thing and its reason in plain English, in one or two sentences that a reader with no prior context can parse. Do not compress a paragraph into a subordinate clause. If the rationale needs more than two sentences, it belongs in a design doc or the PROPOSED APPROACH, not in NOTES.

If there are no notes, omit the section entirely. Do not emit an empty `## NOTES` header.

## Emphasis for scanning: bold and italics

Bold and italicize the "save points" - the phrases that carry meaning - not whole sentences. A reader who skims _only_ the bold and italic fragments should get the story; full prose is for when they want detail.

**What to bold:** phrases that name the **work itself** - the component, the failure mode, the mechanism, the behavior the ticket asks for. These are the nouns and verbs that would appear in a diff of the design, not a diff of the code. "**circular wait** in the **KeyManager**" names the failure mode and the component. "**load key material outside the mutex**" names the mechanism.

**What to italicize:** phrases that orient the reader to **significance** - the conclusion a paragraph is building toward, or the outcome that makes the work matter. _There is a circular wait in the KeyManager_ in PROBLEM. _the circular wait cannot form_ in a payoff sentence. Italics mark the load-bearing insight; bolds mark the load-bearing nouns and verbs.

**What NOT to bold or italicize:** history ("PLAT-134 removed the deadlock"), hazard detail ("it only triggers during the first key fetch"), justification, or connective tissue. These are context and support; they do not carry the story.

**Where formatting goes:**
- SYNOPSIS: bold the key noun phrases (scan anchor for the whole ticket).
- PROBLEM: bold and italicize the conclusion phrase (the problem statement), then bold key nouns in the explanation. Italicize the motivation insight if there is one.
- PROPOSED APPROACH: bold the mechanism nouns and verbs. Italicize the directional conclusion if there is one.
- ACCEPTANCE CRITERIA bullet leads: bold the observable behavior being verified.
- DEPENDENCIES and NOTES bullets: bold the leading noun.

Rules:
- Bold once per concept per section.
- Prefer bolding things (components, states, thresholds, identifiers) and verbs of change over adjectives.
- Italicize at most one phrase per paragraph. If two phrases compete, pick the one that carries the paragraph's point.
- Never bold a whole sentence. Never italicize a whole sentence. Never bold a whole bullet.
- In bullets, the leading noun is usually the right anchor; bold it, leave the qualifier plain.
- A phrase may be both bold and italicized when it is both a work-naming noun and the paragraph's load-bearing insight: **_circular wait_**. Use sparingly.

Scan check before submitting: read only the bold and italic fragments top-to-bottom. If that reading does not convey the shape of the work, you bolded the wrong words (or the prose is padding around them).

## Prose style

These are hard rules, not suggestions.

1. **One idea per sentence.** Split clause-chains. If a sentence has more than one comma separating independent clauses, it is two sentences. One topic per paragraph: if a paragraph shifts from the problem to its risk rating, split it. The reader who skims paragraph leads should get the section's structure.
2. **Literal phrasing beats compressed idiom.** Write for an implementer who has never seen this subsystem: "the worker holds the lock across the database read and the network call" not "lock spans I/O." Implementation verbs are compressed idiom: do not use method names as verbs in prose. "store the result in the in-memory cache" not "publish it". Prefer plain English nouns over code-domain nouns, even when the code-domain noun is technically correct: "reading the row from the database" not "the row read"; "a request waiting for a worker" not "a waiter"; "overwritten with zeros" not "zeroized"; "the queued scan jobs" not "the backlog". If a word sounds like it belongs in a source file rather than a sentence, replace it.
3. **Define subsystem-specific terms on first use.** If a term is specific to this subsystem (not general engineering vocabulary), expand or briefly gloss it the first time it appears. "the DEK (the symmetric key used to encrypt secrets at rest)" not just "the DEK". "the SAML assertion (the signed XML document an identity provider returns to prove who the user is)" not just "the assertion". After the first definition, use the term freely. Definitions go in BACKGROUND, or PROBLEM if there is no BACKGROUND.
4. **No design-narration phrases.** Delete "it anchors the design", "the fix", "this change", "the new approach". State the fact plainly.
5. **No authoring-sequence narration.** Never describe the order you discovered things in, which draft had what, or what a later revision will add. Describe the ticket as it stands.
6. **Italics for orientation asides.** Use `_italics_` for a one-phrase aside that orients the reader: _This is where the deadlock lived_. Not for emphasis.
7. **Plain ASCII only.** No smart quotes, smart apostrophes, em dashes, en dashes, ellipsis glyphs, or arrow glyphs. Use plain hyphens (sparingly) for asides; semicolons are often better.
8. **No buzzwordy abstractions.** If a phrase sounds like it is trying to sound smart, cut or replace it. Name the code and behavior directly. "identity contract" -> "the struct field that identifies the owner". "canonical hash" -> "the SHA-256 we compute on ingestion". "leverage" -> "use". "utilize" -> "use". "facilitate" -> "help". If you cannot say what a phrase means in plain English, it does not belong. Buzzwords are the number-one signal that an AI wrote the ticket; do not send that signal.
9. **Prefer specific terms over ambiguous ones.** If a word can mean more than one thing in this ticket, qualify it or replace it with the specific behavior. Do not rely on the reader guessing the local meaning. Ordinary words can be ambiguous when the code gives them a special role: claim, owner, active, current, generation, repair, coalesce, terminal, source, scope, sync, publish, resolve. "Publish the value" is vague. "Persist the value in the database so the UI can display it" is specific.
10. **Prescriptive voice.** The ticket proposes work that hasn't happened yet. Use "the fix should...", "the implementation must...", "the worker should..." not "this PR moves..." or "the code now...". The PR description uses descriptive voice; the ticket uses prescriptive.
11. **Default to a numbered outline for steps.** A flat list, with an occasional inline branch ("if the path is not in the registry, return a 404; otherwise continue to step 6"), covers almost every workflow. The bar for a diagram or Mermaid chart is high: reach for one only when the flow genuinely needs two dimensions to read - a graph network with many nodes and edges, or a workflow that recurses, forks, and rejoins in ways a linear outline cannot follow without constant back-references. If the flow is one or two levels deep and does not recurse or redirect, an outline is clearer and cheaper to maintain than a diagram.
12. **Avoid loaded language.** Use neutral, current terminology unless the repo's established name is different. Prefer allowlist/blocklist over whitelist/blacklist, primary/replica over master/slave, and precise role names over moralized labels like "bad" or "evil".

## Length and style

Target: the implementer can start work after one read. The lead can prioritize after reading SYNOPSIS and PROBLEM. Err on the shorter side.

Estimate the ticket's **complexity** (how much new mental model the implementer must build), not its size in files or lines. Complexity drives the word budget the way scrum points drive effort estimates:

- **1 point** (one guard, one flag, one constant): the implementer needs to know what to change, not a lesson in the subsystem. ~100-200 words. SYNOPSIS one line, PROBLEM 2-4 sentences (still rate the hazard, even if it is "no current defect"), PROPOSED APPROACH 1-2 sentences, one to three acceptance criteria.
- **2-3 points** (new function, restructured flow, multi-file refactor): the implementer needs a before/after they cannot infer from the code alone. ~200-400 words. Full mandatory sections; BACKGROUND only when prior work or project context earns it.
- **5 points** (new feature, migration sequence): the implementer needs a mental model they do not have yet. ~400-600 words. RELEASE PLAN, VALIDATION, and DEPENDENCIES when prod coordination warrants.
- **8 points** (multi-PR effort, subsystem redesign, constraint-dense work): ~800-1100 words. Complex tickets legitimately need more text; spend it on context and starting state, not on repetition. If PROPOSED APPROACH is longer than the rest of the ticket combined, the ticket is probably a design doc wearing a ticket costume; split it.

Estimate by: how many new concepts the implementer must learn, whether the problem and approach have non-obvious mechanics, whether the work spans multiple workflows or systems. Not by files the change will touch or sections present. A mechanical multi-file rename is 1 point. A one-line fix with subtle semantics is 2-3.

**When a ticket runs long, take the section-level levers first.** Omit RELEASE PLAN, VALIDATION, DEPENDENCIES, or NOTES when they carry nothing a normal deploy or the tracker links already say. Coarsen ACCEPTANCE CRITERIA. Compress PROPOSED APPROACH failure sagas to their consequences. These levers remove duplication, not knowledge.

**Then step up the abstraction ladder.** Do not compress terminology or cut connective tissue to hit a word count. Instead, replace a sequence of mechanism details with the principle that subsumes them.

Example: instead of six claims about how a connection pool reuses connections, how session locks are session-scoped, how a lock taken by one statement does not guard the next, and how nothing reports the mismatch, write: "Some Postgres features attach to the connection, not the statement. The pool freely reuses connections between statements, so state set by one statement may not be there for the next, and nothing reports the mismatch." Same understanding, fewer words, no compression. The mechanism details belong in the linked design doc or the code itself, not in the ticket.

Brevity means fewer ideas, not compressed claims. If the ticket is still too long after the levers and the ladder, cut the lowest-value claim entirely. Do not cut the connective tissue that makes the remaining claims parse on first read. The knowledge build-up - each section introducing what the next one needs - survives every trim; what goes is redundancy.

Inside sections, telegraphic bullet style is fine for criteria and plans: lowercase start, abbreviations (`w/`, `1x`, `~`), parenthetical shorthand. Full sentences for PROBLEM and BACKGROUND prose.

**Tracker rendering**: many trackers (Linear, Jira) render markdown. Put each narrative paragraph on one physical line. Separate paragraphs with a blank line. Bullets stay one per line.

## Codebase comparison

Before drafting, verify the problem statement against the current codebase. If the ticket proposes changing a function that was refactored last month, or cites an incident that was mitigated differently, the ticket is stale before it is filed.

Comparison process:
1. Read the code the ticket references. Confirm the behavior described in PROBLEM still exists.
2. Check git log for recent changes to the same files. If the behavior was already fixed, do not file the ticket; tell the user.
3. If the behavior exists but was partially mitigated, note the mitigation in BACKGROUND so the implementer knows what is already in place.
4. If the ticket is a follow-up to a merged PR, check the merged code to confirm the follow-up is still needed.

When the codebase contradicts the ticket, flag the discrepancy to the user before drafting. Do not silently paper over the gap.

## Project context for planned work

Some tickets are slices of a larger project. The code alone may not explain the project terms, ordering constraints, or prior decisions the implementer needs. Before drafting, read enough context to make the ticket startable for an engineer new to this area.

Read project context when the request, existing ticket, code comments, branch name, prior PRs, docs, or discussion mentions:
- a parent ticket, related PR, follow-up, or multi-ticket project;
- a deferred part of the design;
- an upstream dependency;
- a project-specific term whose local meaning is not obvious from the code touched by this ticket;
- a roadmap label, subsystem nickname, architecture slogan, or branch-local name.

Use available source material: linked tickets, linked PRs, nearby docs, code comments, commit messages, and project memory. Build a private term map: term -> plain behavior -> source. Do not dump the map into the ticket. Use it to write the shortest useful BACKGROUND.

When rewriting an existing ticket, mine the old text for facts - harm statements, platform behaviors, traps already discovered - but draft the new description from the sources, not from the old text. Editing the old ticket inherits its phrasing and its habits; the rewrite should stand on the plan docs, the code, and the mined facts.

If a term or dependency controls the work and you cannot resolve it from available context, stop and ask the user. Do not guess. Do not write around the missing definition with vaguer words.

Put project context in BACKGROUND only when it helps the implementer start work or helps a lead schedule it correctly. Omit generic backstory.

## Search before create

Before filing a new ticket, search for likely duplicates in the tracker. Use the proposed title, problem keywords, affected subsystem, and any incident/customer/project references. If a plausible duplicate exists, surface it to the user before drafting or filing.

If the user still wants a new ticket, make the relationship explicit: related follow-up, supersedes, duplicates, or narrower implementation slice. Do not silently create parallel tickets for the same problem.

## Link verification

Before filing or updating a ticket, verify every link you can. Tickets are usually read outside the repo, so broken links are worse than no links.

- **Repo file links** - use `github.com` links rather than relative paths; verify the path exists on the relevant branch.
- **External docs** - if tooling can fetch the URL, confirm it resolves and appears to be the intended doc. If you cannot verify a user-provided doc link, keep it but do not claim you verified it.
- **Ticket, PR, and design links** - verify the ID/title matches the thing being referenced.

## Linear labels

When filing a Linear ticket, add obvious labels when they clarify triage. Labels are filing metadata, not thatch-ticket-description prose.

- **Bug** - user-visible broken behavior, incorrect result, regression, or production defect.
- **tech-debt** - cleanup, drift, dead code, consistency work, or known design debt with no direct behavior change.
- **refactor** - internal reshaping with intentionally unchanged behavior.
- **Feature** - new user-facing capability or new supported workflow.
- **Improvement** - behavior already exists but should become clearer, safer, faster, or easier to use.
- **Support** - work driven by customer/support handling rather than product roadmap.
- **infra** - Docker, mise, CI, codegen, config, deployment, or cross-cutting dev infrastructure.
- **frontend**, **go**, **hono**, **proto** - use only when the implementation surface is clearly in that area.

Do not guess initiative labels (`track-*`, `wave-*`). Use them only when the user or existing project context names the initiative.

## What does NOT belong in the ticket

- **Implementation detail.** The ticket sets the direction; the implementer chooses the mechanism. If the acceptance criteria read like a build plan, they are over-specified.
- **Full design docs.** Link them from BACKGROUND, do not inline them. They may live in repo docs, Linear, Notion, Archbee, Google Docs, Figma, or another planning system. If the ticket IS the design doc, split it into a design doc plus a ticket that references it.
- **AI attribution, co-author lines, "generated with" footers.**
- **Backstory that does not affect the work.** "We explored approach A then B then landed on C" is noise. The consciously declined alternatives go in NOTES as one-liners.
- **Authoring-process narration.** "I was investigating X and noticed Y" is session context, not ticket content. State the problem plainly.

## Worked examples

### Small fix

    ## SYNOPSIS

    **Guard clause fix** in the **scan activity handler**: reject negative cursor values instead of wrapping them.

    ## PROBLEM

    The scan activity endpoint accepts a cursor query parameter without validating its sign. A negative cursor passes through to the keyset query, where Postgres treats it as a valid bigint but the index scan produces unpredictable ordering. A client that sends `?cursor=-1` gets a page of results that appears valid but skips rows. No incident has been reported; the endpoint is internal and cursors are generated by the API, not user input. The risk is that a future caller constructs a cursor from untrusted input.

    ## PROPOSED APPROACH

    Validate the cursor at the handler boundary before passing it to the query layer. Reject negative values with a 400 response. The query layer should not see a cursor it cannot handle.

    ## ACCEPTANCE CRITERIA

    - **negative cursor returns 400** - a request with `?cursor=-1` receives a 400 response with a clear error message, not a 200 with partial results.
    - **zero and positive cursors unchanged** - existing valid cursor values continue to paginate normally.

    ## NOTES

    - **not a query-layer change** - the guard belongs in the handler, not the query builder. The query layer trusts its inputs by design.

### Moderate change (PLAT-135 as it would appear under this skill)

    ## SYNOPSIS

    **Concurrency fix** in **secret storage**: cold-cache **tenant key loads** should not hold the **KeyManager mutex** across DB and KMS I/O.

    ## PROBLEM

    On a cold cache, KeyManager holds its mutex across the key row read and the KMS unwrap. A caller loading through the pool can win the mutex and then wait for a pool connection, while every pool connection is held by transaction callers blocked on that same mutex. That is a circular wait, and mutex waits do not respect context deadlines.

    No incident has hit this shape. The window only exists during the once-per-process cold load, and it requires mixed pool-path and transaction-path callers with full pool saturation in the same instant. PLAT-134 (#6838) removed the unconditional deadlock in this code; this closes the remaining conditional one.

    ## BACKGROUND

    PLAT-134 (#6838) made key I/O executor-explicit: `ActiveKey(ctx, exec)` and `GetOrCreateKey(ctx, exec)` take an explicit executor, and the KeyManager holds no database handle. That removed the hold-and-wait deadlock where a transaction holder could trigger a hidden second connection acquisition. The mutex-across-I/O shape survived because it predates PLAT-134; it has been identical since the KeyManager was introduced.

    ## PROPOSED APPROACH

    Load key material outside the mutex. Cold loaders run their I/O on their own executor, then take the mutex only to publish the cached entry. Duplicate loads under race are acceptable: they unwrap the same wrapped DEK, producing the same result. Creation needs separate serialization because the schema has no uniqueness on active key rows.

    ## ACCEPTANCE CRITERIA

    - **no DB or KMS I/O while km.mu is held** - the mutex guards only the cache field, never held across a query or KMS call.
    - **cache semantics unchanged** - load-only `ActiveKey`, creation confined to `GetOrCreateKey`, cached entry always corresponds to a committed row.
    - **regression test** - a cold pool-path load cannot block transaction-path callers. Test shape: `SetMaxOpenConns(1)` with the connection held by a transaction that also resolves the key.

    ## NOTES

    - **no singleflight on the load path** - any shared wait ties waiters to the winner's executor and recreates the cross-wait. Duplicate unwraps are idempotent and cheap.
    - **multi-replica key-creation race** is consciously out of scope. The deployment shape is one API pod per tenant; cross-process creation is a known, accepted hazard.

### Large change with RELEASE PLAN and VALIDATION

    ## SYNOPSIS

    **Backfill worker** for **location fingerprints**: compute and populate `location_fingerprint` on existing rows to unblock the M2 unique index.

    ## PROBLEM

    PLAT-123 added the `location_fingerprint` column and made `NewLocation` compute it on write. New rows get fingerprints, but all existing rows have NULL. The M2 plan requires a unique index on `(secret_id, source_id, location_fingerprint)`, which cannot be created while NULLs exist. The dedup pass (PLAT-125) also needs fingerprints to group duplicate locations; without them, un-fingerprinted duplicates do not group together and latent dupes survive into the index creation.

    ## BACKGROUND

    PLAT-123 (#6777) added the column and write-path computation. The fingerprint is `hex(sha256(source_type + NUL-delimited column-name/value pairs))` with a fixed authority map (PLAT-122). The column is nullable; old rows remain NULL until this backfill completes. The backfill must finish before PLAT-125 (dedup) and PLAT-126 (index + NOT NULL) can run.

    ## PROPOSED APPROACH

    A daemon goroutine in scanner-api walks the `webapi_secretlocation` table in keyset-paginated batches, computing and updating `location_fingerprint` for rows where it is NULL. The walk is paced (batch size and sleep interval) to avoid saturating the database. A kill-switch feature flag disables the daemon without redeployment. The daemon quiesces when no NULL rows remain.

    ## ACCEPTANCE CRITERIA

    - **daemon computes fingerprints** for all NULL rows, keyed by `WHERE location_fingerprint IS NULL`, walking in keyset-paginated batches.
    - **paced walk** - batch size and sleep interval are configurable; defaults do not saturate the database under normal load.
    - **kill switch** - a feature flag disables the daemon at startup; the flag defaults to enabled.
    - **quiescence** - when no NULL rows remain, the daemon stops scanning and logs a quiescent message.
    - **gauge** - a Prometheus gauge reports the remaining NULL count, primed at daemon start.

    ## RELEASE PLAN

    - Deploy the worker behind a kill-switch flag (default enabled, no per-tenant overrides).
    - Monitor the burndown gauge and `thogctl locations-missing-fingerprint` TOTAL count per tenant.
    - The worker runs for days on large tenants (~61M rows at ~200 rows/s). No Friday releases.
    - Rollback: disable the kill-switch flag. The daemon stops on next pod restart. Partially filled rows are safe; the walk resumes from the cursor on restart.

    ## VALIDATION

    - Watch the burndown gauge in Grafana for each tenant. The count should decrease monotonically (with restart resets).
    - Run `thogctl locations-missing-fingerprint` per tenant. TOTAL == 0 means the backfill is complete for that tenant.
    - Skim scanner-api logs for `backfill batch failed` or `unknown_source_type` to rule out non-cadence failures.
    - After TOTAL == 0 for all tenants, PLAT-125 (dedup) can proceed.

    ## DEPENDENCIES

    - **hard dependency on PLAT-123** - the column and write-path computation must be live in prod before the backfill starts. The backfill targets `WHERE location_fingerprint IS NULL`; without the column, there is nothing to fill.
    - **PLAT-125 (dedup) is hard-blocked on this** - dedup groups by `location_fingerprint`; running it while NULLs exist would miss real duplicates.
    - **PLAT-126 (index + NOT NULL) is hard-blocked on PLAT-125** - the unique index cannot be created while duplicate rows exist.

    ## NOTES

    - **cursor reset on restart** - the daemon does not persist its cursor. A pod restart resets to the beginning of the walk. Paced batching makes this safe (re-walking filled rows is a no-op), but large tenants take longer to converge after a restart.
    - **unfillable rows** - some source types may lack a fingerprint extractor. The daemon counts these separately and does not retry them. The fleet survey confirmed zero unfillable source types in production, but the code path exists as insurance.

Scan the bolds only:
> Guard clause fix ... scan activity handler ... negative cursor returns 400 ... zero and positive cursors unchanged ... not a query-layer change ... Concurrency fix ... secret storage ... tenant key loads ... KeyManager mutex ... negative cursor returns 400 ... no DB or KMS I/O while km.mu is held ... cache semantics unchanged ... regression test ... no singleflight on the load path ... multi-replica key-creation race ... Backfill worker ... location fingerprints ... daemon computes fingerprints ... paced walk ... kill switch ... quiescence ... gauge ... hard dependency on PLAT-123 ... PLAT-125 (dedup) is hard-blocked on this ... PLAT-126 (index + NOT NULL) is hard-blocked on PLAT-125 ... cursor reset on restart ... unfillable rows

That reading alone conveys the shape, scope, and gates of all three tickets.

## Process

1. **Gather**: read the code the ticket references. Check `git log` for recent changes to the same files. Identify the problem, the prior work, and the proposed direction.
2. **Search before create**: search Linear/Jira for likely duplicate tickets. If one exists, surface it before drafting or filing.
3. **Codebase comparison**: verify the problem still exists in the current code. If it was already fixed, tell the user. If it was partially mitigated, note the mitigation.
4. **Read project context for planned work**: if the ticket is part of a larger project, depends on prior work, uses unexplained project terms, or has scheduling dependencies, read the linked tickets, PRs, docs, comments, and memory before drafting. Build a private term map. If a term or dependency controls the work and you cannot resolve it, ask the user. When rewriting an existing ticket, mine the old text for facts but draft fresh.
5. **Draft PROBLEM first**, in one breath, without looking at code. If you cannot state the harm in three sentences, you do not understand the problem yet. Go back and read.
6. **Write BACKGROUND** (if needed): what prior work led here, what was done, what was left behind, and what project context an engineer new to this area needs to start.
7. **Write PROPOSED APPROACH**: the compass heading, not the map. Prescriptive voice. One short paragraph per mechanism, each with the constraint that justifies it; compress failure sagas to their consequence; move "why not X" reasoning to NOTES.
8. **Write ACCEPTANCE CRITERIA**: observable, testable bullets. Coarse: three to seven, merging parallel checks and dropping restatements of the approach. Name the test shape only where the test design is non-obvious.
9. **Write RELEASE PLAN** (if needed): flags, ordering, rollback. Omit when the rollout is a normal deploy.
10. **Write VALIDATION** (if needed): monitoring, signals, smoke tests.
11. **Write DEPENDENCIES** (if needed): only the why that tracker blocker links cannot express. Omit when the links carry it; set the links instead.
12. **Write SYNOPSIS last** - it is a compression of PROBLEM + the core approach.
13. **Bold and italicize the save points** in the allowed locations. Bold phrases that name the work (components, mechanisms, behaviors). Italicize phrases that orient to significance (conclusions, payoffs), at most one per paragraph. Apply the scan check.
14. **Add NOTES** for non-goals, declined alternatives, and scope limits. Use `## NOTES` header. Omit if empty.
15. **Suggest Linear labels** when the ticket is being filed in Linear. Use obvious stable labels only; do not guess initiative labels.
16. **Verify links**: check repo file links, external docs, tickets, PRs, and design artifacts where tooling allows. Do not claim an unverified link was verified.
17. **Verify prose style and core principle**: check each rule in Prose style. Cut design-narration, authoring-sequence, and buzzwordy abstractions. Verify plain ASCII. Verify prescriptive voice (not descriptive). Verify first-use definitions for subsystem jargon in BACKGROUND or PROBLEM. Verify plain English nouns (no code-domain nouns in prose). Verify conclusion-first in PROBLEM. Verify NOTES bullets are either short pointers or self-contained.
18. **Clarity pass**: read the draft as a cold lead skimming a backlog, then as an implementer picking up the work cold. Rewrite before returning it; do not tell the user you performed this pass. Check: does every project-specific term get plain-English meaning before or with the label? Are ambiguous terms qualified or replaced with specific behavior? Does every process word name object/action/effect? Does every contrast name current and proposed behavior? Does every causal sentence show the middle step? Did you preserve connective tissue instead of compressing meaning into noun stacks? If the draft got longer, cut a lower-value claim instead of compressing a high-value one.
19. **Verify length**: estimate the ticket's complexity (see the point-based budgets in Length and style). If the body exceeds the budget, take the section-level levers first (omit conditional sections that duplicate the tracker or a normal deploy, coarsen acceptance criteria, compress approach sagas), then step up the abstraction ladder (replace mechanism sequences with the principle that subsumes them). If still over, cut the lowest-value claim entirely. Do not compress terminology or cut connective tissue to hit a word count. If PROPOSED APPROACH dominates, consider splitting into a design doc plus ticket.

## Anti-patterns

- **Burying the harm.** If PROBLEM is a paragraph of setup before the actual problem, rewrite. Problem first.
- **Implementation plan as acceptance criteria.** "Restructure ActiveKey to use a publish helper" is an implementation step, not an observable behavior. Replace with "no DB or KMS I/O occurs while km.mu is held."
- **Bolding expository prose without distinction.** Bolds in PROBLEM, BACKGROUND, or PROPOSED APPROACH are fine when they name the work (components, mechanisms). They are noise when they bold filler or context. Bold the change; italicize the significance; leave the scaffolding plain.
- **Over-italicizing.** More than one italicized phrase per paragraph dilutes the signal. Pick the one phrase that carries the paragraph's point.
- **Design-doc ticket.** If PROPOSED APPROACH is longer than the rest of the ticket combined, the ticket is a design doc wearing a ticket costume. Split it: design doc in `docs/`, ticket that references it.
- **Missing hazard rating.** PROBLEM without a "how likely is this" paragraph leaves the lead guessing at priority. Always rate the risk, even if it is "no current defect; preventive."
- **Descriptive voice.** "This PR moves the lock outside the I/O" is a PR description. "The fix should load key material outside the mutex" is a ticket. Use prescriptive voice.
- **Vague acceptance criteria.** "Improve the locking situation" is untestable. Name the observable behavior the implementer and reviewer can check.
- **Dependencies without the why.** "Blocked by PLAT-124" is the tracker field. The ticket should explain why: "PLAT-125 groups by location_fingerprint, so it can only run after backfill completes." Without the why, a lead may reorder the queue and break a hard data dependency.
- **Bare `Notes:` line.** Use `## NOTES` header or omit the section entirely.
- **Loaded language.** Using avoidable loaded terms when neutral terms exist. Prefer allowlist/blocklist, primary/replica, and precise role names.
- **Smart punctuation.** Em dashes, smart quotes, ellipsis glyphs. Use plain ASCII.
- **Splitting paragraphs across lines.** Many trackers render each line break as a visible break. One paragraph = one physical line.
- **Ungrounded jargon.** Subsystem-specific terms used in SYNOPSIS or PROBLEM but never defined in BACKGROUND. The implementer reads "frozen matview reverification" and hits a wall before they start. Define on first use in BACKGROUND (or PROBLEM if no BACKGROUND).
- **Implementation verbs in prose.** "Publish the key" reads as jargon to someone who does not know the method is called `publish`. Say "store the key in the in-memory cache".
- **Code-domain nouns in prose.** "Row read", "waiter", "zeroized", "backlog" (as jargon) are technically English but belong in source files, not sentences. Replace with plain English: "reading the row from the database", "a request waiting for a worker", "overwritten with zeros", "the queued scan jobs".
- **Conclusion buried at the end.** PROBLEM that builds to its point in the last sentence forces the reader to absorb the explanation before knowing what is being explained. Lead with the problem, then explain why.
- **Hazard rating without motivation.** "No incident has hit this shape" answers "how bad?" but not "why prioritize this?" Answer "why now?" so the lead can decide whether to schedule it.
- **NOTES bullets that are both wordy and terse.** A bullet that compresses a paragraph of rationale into one dense sentence reads as a private note. Either flag the thing and point to the full explanation, or write a self-contained sentence or two. Not the middle thing.
- **RELEASE PLAN that argues the release is boring.** If every bullet says the rollout is routine, omit the section. Its absence is the nothing-special signal.
- **DEPENDENCIES that restate tracker links.** "Blocked by PLAT-126" with nothing to add is the tracker field. Set the link; keep the section only for the why a link cannot express.
- **Test inventory as acceptance criteria.** A dozen bullets covering every code path is a test plan, not a definition of done. Keep three to seven observable gates; merge parallel checks.
- **Failure sagas in PROPOSED APPROACH.** Paragraphs of driver internals, pool lifecycle, or library quirks. Compress to the consequence; the implementer discovers the saga at the keyboard.
