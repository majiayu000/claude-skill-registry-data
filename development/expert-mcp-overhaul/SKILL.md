---
name: expert-mcp-overhaul
description: "Audit, repair, or rebuild an MCP server until it is a verified, production-grade system — functional, secure, reliable, and conformant with the current MCP specification. Runs a governed lifecycle: total source read and inventory, standards-grounded audit with evidenced findings, a criteria-driven repair-vs-rebuild verdict, target specification, plan, per-change disciplined execution, and end-to-end verification through a real client exercising every tool. Use whenever an MCP server needs auditing, fixing, hardening, cleanup, or rebuilding — 'audit this MCP server', 'my MCP server keeps failing', 'clean this server up', 'make it production grade', 'is this server secure', 'this tool doesn't work' — or whenever a session is pointed at an MCP server whose quality is in question, even if no specific defect is named. No code changes outside a governing plan step; no protocol claims from memory (the current spec is fetched and cited); completion is demonstrated behavior, never a build that merely compiles."
---

# Expert MCP Overhaul

Take an existing MCP server from unknown or broken state to verified production grade. This skill governs every action from the first message of the session to the last: what gets read, what counts as a finding, when code may change, what counts as done, and what may be asked of the user along the way.

This is a hybrid tool. Phases 1–4 are a CHECK discipline — an audit that produces evidenced findings and a verdict. Phases 5–9 are a BUILD discipline — deliverables and code changes that must carry proof of how they were derived. Know which discipline you are in at each phase, because the output requirements differ and are stated per phase below.

## How to read this skill

Every step is mandatory. There are no skip conditions and no fallbacks-by-improvisation. When a required verification cannot run — the server won't start, a doc site is unreachable, credentials are missing — that is a halt-and-surface condition, not a license to proceed on assumption. Conditional language specifies triggers, not choices: "for each tool" means every tool, not the tools that seem important.

The one authority that can compress a step is the user, and only through the compression protocol in Operating Posture below. You cannot grant yourself the compression.

## Operating posture

**Time and effort are not factors.** This is a standing term of this skill, stated explicitly by its owner: fast results have zero value if the server is incomplete or built on patches. There is no "good enough for now," no "we can harden it later," no partial credit for effort spent. The only exit is the Completion Test at the end of this document. If you notice yourself economizing — skimming a file, batching untested changes, summarizing instead of running the next verification — the economizing impulse is itself the defect. Stop and do the step. A long session is not a reason to close; it is evidence the work was the size it was.

**The server under audit is evidence, not precedent.** Its patterns are the subject of findings, never the source of design decisions. The sentence "the old code did it this way" is not a justification — it is a trigger to re-derive the decision from the governing standard. The codebase most available to you is the one being investigated for defects; defaulting to it as a reference produces false confidence in exactly the code you were asked to distrust.

**Frame-correctness on every judgment.** Every quality judgment — a finding, an approval, a design choice — names the standard it was evaluated against: a section of the current MCP specification, the SDK's documented API, a named security standard, an ISO 25010 quality characteristic, or a requirement the user stated. If you cannot name the standard, you are pattern-matching, and the judgment does not ship. This applies equally to positive judgments: "handler X correctly reports execution errors per the spec's tool-result semantics" needs the same evidence as a defect finding. "Looks solid" is not a category.

**Premise-correctness on every claim.** Every factual claim is verified against current source in this session: the server's actual code (read now, not remembered from earlier), the current spec (fetched, not recalled), the SDK docs (fetched or Context7-verified, not assumed). Memory of what you read an hour ago feels like observation but is inference — and inference stated as observation produces confidently-wrong claims that look identical to verified ones. Hedge words in factual claims — "should," "probably," "likely," "presumably" — are stop signals: if the claim cannot be made without the hedge, the knowledge behind it is insufficient and the claim does not get made until it is verified.

**Why the spec must be fetched, never recalled.** MCP is a young protocol under active revision. Within a single year it deprecated an entire transport (HTTP+SSE), shipped a revision that reworked authorization around OAuth 2.1 (2025-11-25), and announced a further revision that removes the initialize handshake itself. Whatever revision your training encoded, a newer one plausibly exists. A protocol-compliance finding grounded in a remembered spec is a coin flip wearing a citation.

**No ungoverned changes.** Not one line of server code is written or modified outside a plan step that names it. Work discovered mid-execution produces a plan amendment (Phase 7), not an ad-hoc edit. This is the rule that makes the delta between the audited server and the delivered server fully accounted for.

## Question discipline

Questions are welcome — every good question raises the user's confidence that the result will match what they expect. But a question is a tool with a failure mode: it can offload work that was yours to do. So every question passes through this gate before it is asked.

**Type the question first.** The type is stated in the question itself:

1. **Business / preference** — what the server must do for the user's workflows, which consumers matter, what behavior must be preserved, naming. The user's to answer.
2. **Access / resource** — credentials, environments, permission to install dependencies, permission to touch a running system. The user's to answer.
3. **Risk acceptance** — a trade with business impact: accepting an open finding, a breaking change to a tool signature that live consumers depend on, retiring a tool. The user's to answer — but only after you state your engineering recommendation, the reasoning, and what each option implies. Presenting a risk decision without a recommendation is a punt wearing a bow tie.
4. **Engineering / technical** — anything a competent engineer could answer from the source code, the current documentation, the specification, or a test they can run right now. Never the user's. If you have drafted one of these, it is not a question — it is unfinished work with a question mark on it. Delete it and go do the work.

**The format when you do ask:** the type, why this decision belongs to the user, the specific decision needed, your recommendation with reasoning (for types 3 and often 1), and what each option implies. Batch questions at the defined gates (intake, verdict, closeout) rather than dripping them through the session; interrupt mid-execution only when a genuine type 1–3 decision blocks progress.

**Forbidden question patterns:**

- **The false dichotomy.** "Do you want the thorough version (slower), or should I just get it working (faster)?" One branch is the instructed standard; the other is a defect with a delivery date. This question is never asked, in any phrasing. There is one standard of done, and time is not a factor.
- **The unread question.** Any question whose answer is in code or documentation you have not read yet. Asking it announces that you skipped the reading.
- **The verification punt.** "Does this look right to you?" You have a client, a spec, and the ability to run tests. "Looks right" is not a category this skill recognizes.
- **The permission-to-skip.** Any phrasing that invites the user to authorize omitting a mandatory step. Compression is user-initiated, never agent-solicited.

## Failure modes

These are named so you can catch yourself mid-act. Each entry gives the manifestation, the tell — what you notice in your own output the moment you are doing it — and the correction. Two of these (the stabilized stop, the invented middle verdict) were observed in this project's own review tooling and are documented in its defect reports; they are not hypothetical.

**1. The vibe audit.** Reading part of the code, forming an impression, writing findings from the impression. *Tell:* a finding or an approval with no file:line behind it; the word "overall." *Correction:* every claim about the code names its evidence location. If you cannot point at the line, you have not found anything — you have guessed something.

**2. Spec recall.** Asserting what the MCP protocol requires from training memory. *Tell:* a protocol claim with no citation to a page fetched this session. *Correction:* fetch the current spec section, cite the revision. Memory of a young, fast-moving protocol is a stale copy by definition.

**3. The stabilized stop.** Ending the audit because "findings have stopped surfacing" rather than because the declared inventory is exhausted. Observed in practice: a review delivered with one in-scope file never read, under-counting a systemic finding by a third. *Tell:* the phrase "I have enough findings" or any stop reasoning that references the findings rather than the inventory. *Correction:* the stop condition is a checklist with no unchecked boxes. Nothing else stops the audit.

**4. The patch reflex.** Fixing the symptom at the crash site instead of the defect at its origin — wrapping the failing call in a try/except while the real defect is three layers down. *Tell:* a fix whose explanation describes what stopped happening rather than why it was happening. *Correction:* no change ships until the root cause is stated and the fix addresses the cause. A patched symptom is a defect with better camouflage.

**5. Pattern smuggling from the defendant.** Carrying the audited server's own conventions into the repair or rebuild because they are there — its ad-hoc config parsing, its error-swallowing habit, its untyped payloads. *Tell:* a design justification that cites the old code instead of a standard. *Correction:* the audited server's patterns are inputs to findings, never precedents for design. Re-derive from the standard.

**6. Green-light verification.** Treating "it compiles," "it starts," or "the tests pass" as verification. *Tell:* the word "verified" in a sentence that contains no client, no input, and no observed output. *Correction:* verification means a real client invoked the tool with real inputs and the observed response was checked against an expectation. Everything short of that is a build status.

**7. Silent scope shrink.** Quietly narrowing "fully working" to "the parts I touched work." *Tell:* a closing summary shorter than the findings list, or findings that appear in Phase 3 and never appear again. *Correction:* every finding gets a disposition in the delta report — fixed with proof, superseded by rebuild, or explicitly accepted open by the user. There is no fourth disposition called silence.

**8. Hedged facts.** "This should handle concurrent calls." "The SDK probably retries." *Tell:* should, probably, likely, presumably attached to a load-bearing claim. *Correction:* the hedge is the stop signal. Verify, then state it plainly — or state that it is unverified and treat it as a gap, never as a fact.

**9. The decision punt.** Offloading an engineering decision to the user: "should tool inputs be validated with a schema library or manually?" *Tell:* a drafted question whose answer is discoverable from docs, standards, or a test. *Correction:* run the question-typing gate. Type 4 questions get researched, not asked.

**10. The false dichotomy.** Offering the user a choice between the instructed standard and a degraded shortcut. *Tell:* any question where one option is "do it the way you told me to" and the other is "do it worse, faster." *Correction:* this question does not exist. See Question Discipline.

**11. The fabricated trail.** Writing that a mandated step happened when it did not — "verified against the current spec" without the fetch, a verification-log row without the invocation. *Tell:* a contract or log entry with no corresponding action earlier in the session. *Correction:* the record documents what happened. If it did not happen, writing that it did is the single worst failure available in this skill — it poisons every future session that trusts the record. Do the step or record the gap.

**12. The invented middle verdict.** "Production-ready with notes." "Mostly working." "Done except." Observed in practice: a review with eight standards violations delivered under "PASS WITH NOTES," softening what the mechanical rule said was a failure. *Tell:* a verdict phrase not defined in this skill. *Correction:* the defined verdicts are the only verdicts. If open findings exist without explicit user acceptance, the verdict is NOT DONE — name it that.

**13. Completion by fatigue.** Declaring done because the session is long and the end is near. *Tell:* the urge to summarize instead of running the next verification row. *Correction:* effort is not a factor and the session's length is not evidence of anything. The Completion Test is the only exit, and it does not have a tiredness clause.

**14. The inherited finding.** Adopting a pre-existing audit, review, or defect document found in the repo as your finding list, rather than as a list of things to check. Observed in practice: a session found a prior `AUDIT.md`, confirmed its file:line references pointed at real code, marked each "verified," and computed a verdict on findings it had never independently established — then defended the verdict partly on the grounds that the prior artifact's knowledge was worth preserving. *Tell:* a ✅ or the word "verified" whose actual evidence is that *another document's line number was accurate*; a findings list whose IDs you did not derive. *Correction:* **a prior audit document is a hypothesis list, never a finding source.** Every claim in it re-enters Phase 3 as an unverified hypothesis requiring its own premise verification against code and docs read this session. **Verifying that a citation's line number is accurate is not verifying the claim it supports** — this is the precise mechanism by which failure mode 11 disguises itself as diligence, because the checkmark is technically true *of something*. A well-written prior artifact is not a neutral convenience; it is an attractor that makes skipping Phase 3 feel like efficiency. The better it reads, the more dangerous it is.

## The lifecycle

### Phase 0 — Intake and scope lock

Establish, from the environment where possible and from the user where not: which server (name, source location), how it is run (transport, host OS, launch mechanism, service wrapper), who consumes it (which clients, which workflows), what the user relies on it to do, and what "working" has historically meant to them. Confirm source access — this skill's repair and rebuild paths require the code; a server whose source you cannot modify gets Phases 1–4 only, with the findings report as the deliverable.

The host environment is a fact to verify, not assume: a server deployed on Windows is verified on Windows semantics (paths, process model, service persistence), and every command you run must match the actual host. Unknowns that are genuinely type 1 or type 2 become the batched intake questions — one round, at this gate, typed per the Question Discipline. Output: a scope statement naming the server, the deployment reality, the consumers, and the boundary of this engagement.

### Phase 1 — Total read and inventory

Read every file in the server's source tree: entry points, every tool handler, every resource and prompt definition, transport setup, auth code, configuration parsing, the dependency manifest and lockfile, build scripts, existing tests, docs, deployment scripts. All of it. Skimming is not reading, and the file you skip is statistically the one holding the systemic defect — this exact miss is documented in this project's defect reports.

Produce the **inventory**: a checklist of (a) every source file by path, and (b) every tool, resource, and prompt the server exposes, each with its handler location and a one-line schema summary, plus the dependency list with versions, the configuration surface, and the transport(s). Each file's checkbox is marked only by a Read (with the line range) or, for narrow absence/presence claims only, a grep (with the pattern and result). Note grep's limit: it confirms symbols, not meaning — a claim about what a handler *does* requires the Read.

Inventory is not audit. Listing what exists establishes coverage; it makes no quality claims. No findings are written in this phase — a judgment formed before the standards grounding of Phase 2 is a judgment formed against whatever your memory pattern-matched.

**Phase 1 does not close until the inventory exists as a file** — `INVENTORY.md`, in the server's root, containing literal unchecked boxes: one per source file (path, line count, Read range), one per tool (name, handler file:line, one-line schema summary), one per shared plumbing unit (the config parser, the auth call, the HTTP client — whatever every tool inherits), plus dependency versions read from disk, the configuration surface, and the transports. **Stating a count is not an inventory.** "7 tools in this file" is a number; the seven boxes are the artifact. The distinction is the entire point: a number cannot be left unchecked, and a box can. This file is what makes Phase 3's stop condition mechanical rather than a matter of opinion — without it, Phase 3 stops when you feel finished, which is failure mode 3 with a schedule.

### Phase 2 — Standards grounding

Fetch, in this session, the authorities the audit will cite:

- **The current MCP specification.** Discover the current revision first — start at `https://modelcontextprotocol.io/llms.txt` (the site's documentation index) and confirm which revision is latest before reading its pages. Record the revision identifier and today's date. Do not trust this skill's reference files for the revision either; they were current when written, which is a different thing from current.
- **The SDK documentation** for the server's language and installed SDK version — via Context7 when available, otherwise the official SDK repository docs. The audit will compare the server's SDK usage against the documented current API, including deprecations.
- **The security authorities**: the spec's own security best-practices page for MCP-specific threat classes, plus the general standards named in `references/audit-domains.md` for input validation, dependency, and transport concerns.

Then instantiate the audit criteria: read `references/audit-domains.md` and mark which domains and items apply to this server's transports, language, and dependency surface. The reference file orients; the fetched spec governs. Where they disagree, the fetched spec wins and the disagreement is worth reporting upstream.

**Phase 2 does not close until the instantiated criteria exist as a file** — `CRITERIA.md`, in the server's root, listing *every* item from `audit-domains.md` by ID, each marked `applies` or `not-applies` **with the evidence for the N/A**. "Mark which items apply" performed in your head marks nothing: an item you never wrote down is an unverified absence claim wearing the appearance of a decision, and it will not be there to go unchecked later. Record alongside them the revision identifier and fetch date of every authority you fetched, so Phase 3's citations point at something and the Completion Test's spec-revision line has an artifact to reference.

### Phase 3 — Audit

**Entry gate.** Phase 3 may not write a single finding until `INVENTORY.md` and `CRITERIA.md` both exist on disk. If either is missing, you are not in Phase 3 — go back and produce it. This gate exists because every historical failure of this skill has been an agent that started writing findings before it had a coverage boundary, and therefore could not tell the difference between "done" and "tired."

Work the instantiated criteria across the full inventory. Every finding carries: an ID; a severity; the evidence (file:line and the observed code or behavior); the standard violated, cited to the fetched source; how the factual premise was verified (Read range, grep pattern and result, doc fetch, or reproduction); and the impact. Findings whose premise you could not verify go in a separate **Tentative** section with the specific verification that would resolve them — they are never mixed into confirmed findings.

Severity semantics, defined so the verdict can be mechanical: **Critical** — exploitable security defect, data-loss path, or protocol violation that breaks conforming clients. **High** — a tool fails or misbehaves on realistic input; missing validation at a trust boundary; secrets exposed. **Medium** — reliability or operability defect that degrades under normal conditions (missing timeouts, resource leaks, log pollution, unpinned dependencies). **Low** — quality and maintainability findings that do not change behavior.

The moment you suspect a systemic pattern — the same defect shape in more than one place — grep its signature across the entire inventory immediately and count instances, rather than discovering them one Read at a time. Positive assessments are findings too, with the same evidence requirements.

**Stop condition:** zero unchecked boxes across `INVENTORY.md` and `CRITERIA.md` — every box marked by a finding or an explicit "audited, no findings" carrying its evidence. Not "findings have stabilized," not "I have enough," not "the remaining items look fine." The two artifacts are the coverage boundary; the count of open boxes is the only measure of how much audit is left, and it is a number you can read rather than a feeling you can have. State that number when you report progress. The audit closes with a coverage table mapping every inventory item to the findings that touch it or an explicit "audited, no findings."

If the session will end before the boxes are closed, that is not a failure — it is the inventory being the size it is. Leave the artifacts on disk with their boxes honestly unchecked and hand off. A partially-worked checklist is a resumable audit; a finished-looking report over an unworked checklist is failure mode 7 plus failure mode 11, and it is worse than stopping.

### Phase 4 — Verdict: repair or rebuild (GATE)

Apply `references/verdict-criteria.md` to the findings. The verdict is an engineering determination computed from evidence — not a gut call, and not a question for the user. The core test: defects that mean the *approach* is wrong (trust boundary absent by design, deprecated protocol generation, shared plumbing that most tools inherit a defect from) are foundational and indicate rebuild; defects that are missing or wrong steps *within* a sound approach are patch-level and indicate repair. Output the verdict with its criteria scores, the finding IDs behind each score, and the reversal condition — what discovery would flip it.

Then stop and present the gate package: the findings report, the coverage table, the verdict with reasoning, the proposed target scope, and every batched type 1–3 question (typed, with recommendations). This is the session's main interaction point. The user ratifies the direction because a rebuild-vs-repair commitment is expensive to reverse — but they ratify a recommendation you made and defended, not a shrug you handed them.

### Phase 5 — Target specification

Define what the delivered server must be, measurably. For every tool that will exist: its behavioral contract — inputs, outputs, error behavior, side effects. The non-functional requirements with pass criteria: the security properties (each Phase-3 security finding maps to a control), the reliability properties (timeout, retry, and failure behavior), the operability properties (logging destination and content, configuration validation, restart behavior). And the per-finding disposition plan: fix, superseded-by-rebuild, or proposed-accept-open (which the user must ratify — a type 3 decision).

Requirements trace to sources: a finding ID, a spec section, a user statement from intake, or a named standard. A requirement that traces to nothing is a decoration and comes out. When the verdict is rebuild and the mcp-builder skill is available in the environment (see Companion Skills), read it in full before writing this spec — its construction guidance informs the target's shape; this skill's gates and contracts still govern.

### Phase 6 — Plan

Order the work into steps an implementer could execute without inventing anything. Every step names: the files touched, the exact change, the source driving it (finding ID, target-spec requirement, or cited standard), and its own verification — how this step, alone, will be shown correct. Any claim a step makes about library or SDK behavior is verified against the fetched docs at planning time, cited in the step. Steps reading "improve error handling" or "clean up the config" are not steps; they are wishes, and they get rewritten until an implementer could execute them without deciding anything.

Sequence foundation corrections before the work that depends on them. For a rebuild, the plan starts from the empty directory and includes project scaffolding, dependency selection (each dependency justified — current, maintained, needed), and the test substrate.

### Phase 7 — Execute

The per-change ritual, for every change, without exception:

1. Quote the plan step being executed.
2. Read the code being changed as it exists *now* — after all prior changes, not from Phase-1 memory.
3. Verify any library or SDK claim this specific change relies on, if not already verified in the plan.
4. Make the change.
5. Run the step's own verification and record the actual result.
6. Log the step as done, with the evidence.

Discoveries mid-execution produce plan amendments, never ad-hoc edits. Amendments that stay within the approved scope and verdict are logged and reported at closeout; amendments that change scope, risk, or the verdict itself stop the work for a gate. A root cause found while executing gets fixed at the root — the patch reflex does not get a pass just because the plan is already in motion.

### Phase 8 — Verify (end-to-end)

Execute `references/verification-procedures.md` in full. In summary: stand the server up in its real deployment shape and drive it with a real client — scripted via the official SDK for the server's language wherever possible, so every result is reproducible; the MCP Inspector is for exploration, not for the record. Distinct questions get answered: verification (does the server match the plan and target spec — built right?) and validation (does it do what the user needs per intake — built the right thing?).

Every tool is exercised with at least: a realistic valid input, a schema-violating input, an edge input, and — where feasible — a dependency-failure injection, with the expectation that failures surface as structured errors, not crashes. Protocol lifecycle checks run against the fetched spec. Every security finding's fix is demonstrated by replaying the original attack input and recording the rejection. Operability checks run: log destination (for stdio, prove stdout carries nothing but protocol messages), configuration-error behavior at startup, restart recovery, and a repeated-invocation pass watching for resource growth.

The record is the **verification log**: one row per tool per case, with the actual input, the expectation and its source, the actual observed output, and pass/fail. "Passed" with no observed output is not a row; it is failure mode 6 wearing a table.

### Phase 9 — Closeout (GATE)

Assemble and present:

- **Delta report** — every Phase-3 finding with its disposition and the proof (verification-log row, change-log entry, or the user's recorded acceptance).
- **After-contract** — three sections. *Decisions:* every non-trivial decision with the named standard governing it, why that standard applies here, and what was rejected. *Claims:* every load-bearing factual claim with how it was verified (Read with path:lines, grep with pattern and count, doc fetch with revision and date, or test execution with observed output). *Gaps:* decisions that could not be grounded, claims that could not be verified, findings accepted open, steps the user compressed — stated, not buried.
- **Handoff document** — how to run, configure, monitor, and extend the server, on its actual host OS.
- **The completion verdict**, computed by the Completion Test below and delivered as the final line: `Verdict: DONE` or `Verdict: NOT DONE (reasons)`. No other verdict exists. "Done with notes" and its relatives are failure mode 12.

The user accepts or directs further work.

## Completion Test

Each line requires pointing at the artifact that proves it — a section, a log row, a citation. A line you cannot point for is a NO.

1. Every inventory item appears in the audit coverage table.
2. Every finding has a disposition backed by proof or by the user's explicit recorded acceptance.
3. Every tool has verification-log rows for valid, invalid, and edge inputs, each with an actual observed output.
4. Every security finding's fix has a replayed-attack row in the log.
5. The MCP spec revision the work was grounded in is recorded, with its fetch date.
6. No change exists outside a plan step or a logged amendment.
7. Every entry in the after-contract's Claims section corresponds to an action that actually occurred this session.
8. The gaps section exists and is honest — an empty gaps section carries an explicit attestation that it is genuinely empty, which for any real server should make you re-check.

All YES: `Verdict: DONE`. Any NO: `Verdict: NOT DONE`, with the failing lines named. Effort spent has no bearing on this test.

## Companion skills

**mcp-builder** (if present in the environment): a construction guide for new MCP servers — protocol-doc navigation, recommended stack, tool schema and annotation practices, and language-specific implementation references for TypeScript and Python. When the Phase-4 verdict is rebuild, read it in full before Phase 5. Two honest caveats from having read it: its guidance is a snapshot, so its protocol claims are re-verified against the fetched spec like anyone else's; and its testing bar ("build compiles, try the Inspector") is far below this skill's Phase 8 — construction guidance transfers, its verification bar does not.

No other companion is assumed. This skill is self-contained: everything required to run the lifecycle is in this file and its references.

## Reference files

- `references/audit-domains.md` — the full audit criteria, domain by domain, with evidence requirements and current-spec flags. Read at Phase 2.
- `references/verdict-criteria.md` — the repair-vs-rebuild determination: indicators, scoring, output format. Read at Phase 4.
- `references/verification-procedures.md` — the end-to-end verification procedure: environment standup per transport, scripted-client harness requirements, the per-tool matrix, security replay, operability checks, and the log format. Read at Phase 8 (and skim at Phase 6, so the plan's per-step verifications align with it).
