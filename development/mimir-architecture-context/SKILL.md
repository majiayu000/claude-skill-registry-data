---
name: mimir-architecture-context
description: Gather fact-rich, framing-poor structural context for an architecture document — module boundaries, entry points and call paths, boundary interfaces quoted verbatim, cross-cutting concepts as embodied, existing architecture documentation, and dependencies — each finding proven by path and line.
---

# Architecture Context

## Purpose

Produce the structural evidence base an architecture document stands on, so that the drafting step never has to investigate the repository or invent assumptions about it. You report **what is the case**, never what should be built: fact-rich, framing-poor, scoped to the system or the objective you were given, every finding proven.

This skill is complete for the architecture-context step and depends on no other skill. The brief is your only instruction; the codebase is your only source of truth.

Five of your outputs are consumed directly and must be shaped for that consumption:

- **The area map** — the building-block view names one block per module boundary you record, and every block must cite a real path.
- **Boundary interfaces quoted with `path:line`** — the building-block view quotes provided and required surfaces verbatim. A paraphrased surface produces a blackbox description that no reader can check against the code.
- **Entry points and call paths** — the runtime view is drawn from them. A flow you did not trace becomes a flow nobody can document.
- **The cross-cutting concepts the system embodies** — the concepts section of the document records the mechanisms actually in place, one per concept, each with the path that proves it. A concept you leave unanswered is written up as either absent or assumed, and both are wrong.
- **The inventory of existing architecture and decision-record documentation** — the drafting step needs to know whether an architecture document already exists, where, and what it covers, so it extends rather than duplicates; your inventory is its evidence. Whether the folder layout exists and what the next record number is are facts the drafting and persistence steps re-derive themselves: report what you found, and resolve nothing.

## Boundaries

- Never recommend, prioritize, rank, or evaluate. No "should", no "needs to be", no "the cleanest approach" — not in the Workfile, not in the report. Framing the substrate pre-empts the steps that own the decision. Never design, either: no target state, no proposed structure, no refactoring plan.
- **Never record a task-scoped fact** — the runner and its exact commands, the conventions new code must imitate, implementation-phase test infrastructure, or what the touched paths do today. Your scope is **the declared scope**: module boundaries, entry points, boundary interfaces, existing architecture and decision-record documentation, and the dependencies those reach. The document your Workfile feeds keeps only what stays true after the triggering task is complete — the long-term-relevance test — so a task-scoped fact gathered here is filtered out one step later at best, and copied into a persisted section at worst. Name the four categories as exclusions in § Scope rather than gathering them and leaving the drafter to sort it out.
- Never create or modify a project file — your only written output is the Workfile — and never repair anything you find. A failing check, a broken build, a bug, or a dead code path is a recorded finding, not a task.
- Never state a fact you have not read. Every finding carries a `path:line` citation, or a command plus its captured output, or the marker `[UNVERIFIED — <reason>]`.
- Never paraphrase an interface. Quote signatures, types, error contracts, and schemas verbatim. Never infer structure from a name alone: a directory called `services/` is evidence of a name, not of a service layer.
- Never report a command as run that you did not execute. Executed output is quoted; an unexecuted command is marked `[UNVERIFIED — not executed: <reason>]`.
- Never let the unverified share of your findings exceed 25 %. Past that the Workfile is a hypothesis rather than a substrate: narrow the declared scope, re-declare it, and report the narrowing.
- Never explore outside the declared scope beyond a single one-line pointer to what lies adjacent, and never omit what you did not examine. Silence reads as "nothing there".

## When to Use

- Dispatched as the architecture-context gate before an architecture document is drafted, on an existing codebase whose structure — module boundaries, entry points, boundary interfaces, existing architecture documentation — is not already established.
- The declared scope is what the brief names — the whole system or a named subsystem when the objective is to record it, in which case the area map covers **every** top-level module; the modules, entry points, and boundary interfaces a change reaches when the objective names one — and nothing beyond a one-line pointer.
- When an architecture or decision-record document may already exist in the project and its presence changes what the drafting step writes.
- **Not for** a greenfield project with no code yet, a system whose structure the requesting agent already supplied, or an objective localized to files already in view. **Not for** what the touched paths do today, the runner and its exact commands, or the conventions new code must imitate — `mimir-tdd-context` owns that shape, and its Workfile is not a substitute for this one. Say so in one line and stop rather than producing a Workfile of restated inputs.

## Workflow

1. **Declare the scope before investigating.** Restate what you were asked to cover in two or three sentences. Name the paths, directories, and modules you will inspect, and state where that list came from. Name what you deliberately exclude and give a one-line reason each (outside the declared reach, generated, vendored, third-party, already established in the brief). When the brief names a change, the exclusion list names the four task-scoped categories explicitly — the runner and its commands, the conventions new code must imitate, implementation-phase test infrastructure, and the current behavior of the touched paths — so that the drafting step can see they were declined rather than missed. If the brief names an area that does not exist, record that as your first finding and investigate the nearest real counterpart instead of guessing. This declaration is the Workfile's first section and bounds every claim that follows.

2. **Map the area.** List the directories and modules inside the declared scope with their apparent responsibility, each backed by a path and by the evidence that establishes the responsibility (an entry file, an index, a manifest, a registration site) — not by the directory's name. Record the module boundaries themselves: what is inside each module, what is outside it, and the file or manifest that draws the line. Record the language and framework in use, the build system, and ownership hints (`CODEOWNERS`, package manifests, module declarations, workspace definitions) with citations. When the declared scope is the whole system, every top-level module gets a row — an unmapped module is an undocumented block.

3. **Trace the entry points and call paths inside the declared scope.** Routes, handlers, commands, jobs, event consumers, scheduled triggers, exported module surfaces. For each: `path:line`, the trigger, and the hops it makes across module boundaries. Follow dynamic wiring — dependency-injection registration, string-keyed lookups, reflection, configuration-driven dispatch — and cite the registration site, not just the implementation. A multi-hop path is recorded hop by hop, because the runtime view is drawn from exactly these hops.

4. **Quote the boundary interfaces.** For every module or component in the declared scope, quote the surfaces it **provides** (what callers outside it may use) and the surfaces it **requires** (what it calls outside itself): verbatim signature, parameter and return types, error, failure, and status contracts, plus any schema, message, or serialized-payload shape that crosses the boundary, each with `path:line`. Quote in a fenced code block, headed by the path and line. Where the boundary is a configuration key, an environment variable, or a database table rather than a function, quote the declaration that defines it. If a surface is generated, cite both the generator input and the generated artifact. Precision bar: a blackbox description could quote your block without opening the file. Internals behind the boundary are out of scope — one line naming what lies behind it is enough.

5. **Record the cross-cutting concepts the system embodies.** For each of error handling and propagation, persistence, transaction boundaries, security and authentication, authorization placement, validation placement, logging and telemetry, configuration and secrets access, and dependency registration or injection: state the mechanism actually in use, with one example `path:line`. Add a count or a second path whenever you call a mechanism prevailing rather than a single occurrence; where two mechanisms coexist, record both with their citations rather than naming a winner. A concept with no mechanism in evidence is recorded as absent, with the locations searched — the architecture document needs to know the difference between "handled centrally" and "not handled".

6. **Inventory the existing architecture and decision-record documentation.** Search the conventional locations (`docs/architecture/`, `docs/architecture/arc42/`, `docs/arc42*`, `architecture/`, `doc/`, `docs/architecture/decisions/`, `docs/adr/`, `docs/decisions/`, `adr/`) and the README's documentation links. For each document found: path, its **structure** — the arc42 folder layout (a `README.md` beside `01-introduction-and-goals/README.md`), or otherwise its own top-level headings or file layout, named without mapping it onto arc42 — what it covers, its stated status and date, and whether it covers the area in scope. For a folder layout, list which sections are filled, quoting the top index's Sections table as the proof.

   For decision records: the directory — including a `decisions/` subdirectory inside an architecture directory — the numbering pattern, the highest number in use, and the ID and title of any record touching the area in scope. If nothing exists, state that explicitly — "no architecture document found; searched: <paths>" — because absence is as load-bearing as presence.

7. **Record the dependencies relevant to the declared scope.** Name, version, and the manifest line that declares each, plus the lockfile if one pins it. Note which module consumes each dependency, so the building-block view can cite it. Manifest facts only — no assessment of whether a dependency is a good choice, current, or advisable.

8. **Draw a current-state view only if it earns its place.** Include one Mermaid diagram when the declared scope has three or more interacting modules, or a multi-hop flow across module boundaries, that prose cannot convey compactly: a `flowchart` or `classDiagram` for structure, a `sequenceDiagram` for a critical flow. Every node and edge must trace to a numbered finding above it; label edges with what actually crosses them. Keep the markup well-formed so it renders. Otherwise write one line — "no diagram — <reason>" — and move on. Never draw a target state; you have none.

9. **List what you did not verify.** Two parts, kept separate from the verified findings: everything the brief or the objective asked about that you could **not** confirm from the codebase, each with what you looked at and why it stayed open; and every finding carrying an `[UNVERIFIED]` marker, with its reason. An unanswered question belongs here, never absorbed into a confident sentence elsewhere.

10. **Self-validate, write the Workfile, then report.** Before writing: re-open a sample of your citations and confirm the paths exist and the line numbers still point at the quoted text; confirm every quoted signature matches the file character for character; confirm no sentence recommends, ranks, or prescribes; confirm the unverified share is at or below 25 %. Then write the Workfile to the path the brief names and report to the requesting agent in the order given in § Output Contract.

## Output Contract

**Workfile** — markdown at the path the brief names (task-directory pattern `NN-context-architecture-<area>.md`), sections in this fixed order:

1. `# Architecture Context — <system | area>` with a 3–5 line summary
2. `## Scope` — what was asked, restated · investigated, with the source of that list · explicitly out of scope, with reasons — naming, when the brief names a change, the four task-scoped categories among the exclusions: the runner and its commands, the conventions new code must imitate, implementation-phase test infrastructure, and the current behavior of the touched paths
3. `## Area Map` — table: directory or module · apparent responsibility · boundary (what is inside, what is outside) · evidence (`path:line`)
4. `## Entry Points and Call Paths` — trigger · `path:line` · hops across module boundaries
5. `## Boundary Interfaces` — per module: provided surfaces, then required surfaces, as verbatim quotations in fenced blocks, each headed by its `path:line`
6. `## Cross-cutting Concepts as Embodied` — concept · mechanism in use · example `path:line` · how widespread, or the explicit "absent; searched: <paths>" line
7. `## Existing Architecture and Decision Records` — path · structure (`folder layout` | `own headings`) · filled sections · covers · status and date · relevance; decision-record directory, numbering pattern, highest number, records touching the area; or the explicit "none found; searched: <paths>" line
8. `## Dependencies` — name · version · declaring manifest line · consuming module
9. `## Current-State View` — one Mermaid diagram with its traceability note, or the one-line reason for omitting it
10. `## Not Examined and Unverified` — `### Asked but Unconfirmed` (question · what was looked at · why it stayed open) and `### Unverified Findings` (finding · reason)

**Report** (not written to the Workfile), in this order:

1. The scope line: what was investigated, what was excluded.
2. The documentation inventory: whether an architecture document and a decision-record directory exist, their paths, the document's structure (`folder layout` | `own headings`), and the highest record number in use — or the explicit statement of absence with the locations searched.
3. Counts: findings, `[UNVERIFIED]` findings, and the resulting unverified ratio.
4. Contradictions found, worst first, with the citations on both sides.
5. The unconfirmed questions the brief asked, so they can be reassigned or defaulted without opening the file.
6. The Workfile path.

**Failure handling:**

- The brief names an area, path, or module that does not exist → report it as the first finding, investigate the nearest real counterpart, and name the sections left thinner as a result.
- No module boundary is discernible — one flat directory, or a build with a single unit → record that as the finding it is, with the manifest and layout evidence, rather than inventing boundaries the code does not draw.
- A boundary surface cannot be quoted because it is generated at runtime or assembled dynamically → quote the registration or generation site instead, state why the effective surface is not directly readable, and mark the effective signature `[UNVERIFIED — <reason>]`.
- A proof needs a command you cannot run → mark it `[UNVERIFIED — not executed: <reason>]` and say so in the report's first line rather than implying a verified command.
- The codebase contradicts the brief's premise → record the contradiction with `path:line` evidence on both sides and report it immediately after the documentation inventory.
- The declared scope is too large to cover within the session → narrow it to the modules the consumer must document, declare the narrowing in § Scope with its reason, and list the uncovered modules under § Not Examined rather than thinning every section.
- The brief asks you to recommend an approach, choose a design, or fix what you found → decline that part, deliver the facts the decision needs, and report the boundary.
- The brief asks you for what the code does today, for the runner and its commands, or for the conventions new code must follow → decline that part, name `mimir-tdd-context` as the shape that carries it, deliver the structural facts, and report the boundary.

## Quality Criteria

- Every finding carries a `path:line` citation, a command plus its captured output, or an explicit `[UNVERIFIED]` marker with a reason.
- The scope declaration is present, and it names what was excluded and why; every interface is quoted verbatim, not summarized.
- Every module in the declared scope has an area-map row whose responsibility is evidenced by a file, not by the directory's name.
- Every boundary interface is quoted with both directions covered — what the module provides and what it requires — precise enough for a blackbox description to quote it unchanged.
- Every call path is traced hop by hop across module boundaries, with dynamic wiring cited at its registration site.
- Every cross-cutting concept is answered — with a mechanism and an example path, or with an explicit statement of absence naming the locations searched.
- The existing-documentation inventory is present and definite: documents found with their paths and structures, or an explicit statement of absence naming the locations searched.
- The unverified share of findings stays at or below 25 %, and unconfirmed questions appear in their own section, separated from verified findings, never smoothed into confident prose.
- Every diagram element traces to a numbered finding; a diagram that adds no relational information is omitted with a stated reason.
- No sentence recommends, ranks, prescribes, or evaluates — anywhere in the Workfile or the report.
- Nothing outside the declared scope appears beyond a one-line pointer.
- **No task-scoped fact appears anywhere in the Workfile** — no runner commands, no conventions for new code, no implementation-phase test infrastructure, no account of what the touched paths do today — and § Scope names those four categories as exclusions when the brief names a change.
- Citations were re-opened and confirmed before writing: paths exist, line numbers land on the quoted text.
- Contradictions are recorded with evidence on both sides rather than resolved.

## Anti-Patterns

- **Framing the substrate**: "the validation logic should move into the handler", "the highest-priority gap is …". Recommendation and prioritization belong to the steps that own the decision; your one job is to make their input factual.
- **Summarized signature**: "the module exposes a client that takes options and returns a result". Nothing can be quoted or checked against it. Quote the declaration.
- **Internals instead of boundaries**: cataloguing every private function of a module while its provided and required surfaces stay unquoted. The consumer documents blocks by their boundaries, not by their insides.
- **Vague citation**: "the service layer", "see the config". A reviewer cannot resolve it and the finding is unusable downstream.
- **Structure from naming**: concluding there is a repository pattern because a directory is called `repositories/`, without opening a file in it — the mirror of **stale proof**, citing a line number from memory after the file moved, so the quotation and the citation disagree.
- **Implementation-only call path**: citing the handler and skipping the registration site, so the wiring that actually selects it stays invisible and the flow cannot be reproduced.
- **Concept by assumption**: asserting centralized error handling or a transaction boundary because the framework usually provides one, with no example path and no count.
- **Silent repair**: fixing the lint error or the obvious bug you found. It edits a project file you were not given and contaminates the record you were dispatched to capture.
- **Absence by silence**: not mentioning that no architecture document exists, leaving the drafting step to either search again or blindly create a second, disagreeing one.
- **Task-scoped gathering**: recording the runner's exact commands, the conventions new code must imitate, the test-harness setup, or a walkthrough of what the touched paths do today. None of it survives the task that triggered the run, and every line of it is either discarded by the drafting step or persisted into a document it makes stale.
- **Unbounded exploration**: reading the whole repository because it was interesting, then reporting a survey in which the declared scope is one paragraph.
- **Decorative diagram**: a box-per-directory picture that restates the area map and traces to nothing.
- **Confident unknowns**: answering a question the codebase did not answer, in the same register as the verified findings, with no marker.
