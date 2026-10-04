---
name: ss-proposal
description: Use when you have a PRD or requirement description and need a complete technical proposal before writing any code. Filters the requirement down to this repository's boundary, analyzes the existing architecture and conventions, and produces a Markdown proposal covering architecture, data flow, key interfaces, alternatives, risks, and milestones — gated by a self-review and, when available, an independent reviewer pass.
---

# Write Technical Proposal

Generate a comprehensive technical proposal from a PRD or requirement description, for any repository shape — a backend service, a frontend app (Web, iOS, Android, Flutter), or a full-stack repository.

**Scope note:** a proposal is a high-level design document. It answers *what* the change is, *why* it's the right approach, and *what contracts* it introduces or touches — architecture, data flow, key interfaces, alternatives and trade-offs, risks and rollback, milestones. It does not contain implementation detail: no file-by-file edit lists, no full method bodies, no step-by-step coding instructions. That level of detail is the `ss-plan` skill's job, which consumes this proposal as its input.

**When not to use:**
- Small bug fixes or config-only changes with no architecture decisions.
- One-line code changes, typo fixes, or copy fixes.
- Changes already fully specified in an existing proposal.

**Announce at the start:** "Using the ss-proposal skill to generate the technical proposal."

## Inputs

- A link to a requirement document that your document-reading tool can fetch, or a plain-text requirement description. If neither is available, ask the user for one.

If the input is a document link, read its content with whatever document-reading tool is available in your environment. Otherwise treat the input as a plain-text requirement description directly.

## Hard Gates

Before writing, verify each item. If any fails, stop and explain to the user:

- [ ] The PRD/requirement input is readable (the link is accessible, or the text description is substantive).
- [ ] The input contains concrete functional or page/feature requirements, not just a concept or goal statement.
- [ ] The current repository's code can be inspected to understand its existing architecture (it's compilable/runnable, or otherwise navigable).

If requirements are vague or ambiguous, ask the user for clarification — never assume silently.

## Anti-Patterns

The following are proposal failures — never allowed:

| Anti-Pattern | Correct Approach |
|-------------|-----------------|
| Copy-pasting large sections of the PRD as "background" | Background should be ≤10% of the proposal — only the context needed for tech decisions |
| Data model says "add a table/field" without a schema | Include the complete schema change (DDL, or the equivalent for this stack's persistence layer) |
| API or component design says "add an endpoint/component" without a definition | Include the full contract: request/response structure, or props/state/events for a UI unit |
| Presenting a single approach when clearly better alternatives exist | Compare viable paths and recommend one, with reasons |
| Placeholders: TBD, TODO, "to be determined", "fill in later" | Complete every section immediately; ask the user if stuck |
| Unilaterally splitting delivery into "Phase 1 / Phase 2," designing only a "P0 / core" subset, or proposing an MVP/demo/simplified version | Cover 100% of the PRD's functional points and pages; phasing or scope cuts only on an explicit user instruction, recorded in the proposal |
| Silently narrowing scope to route around a blocker (missing information, missing design assets, external dependency) | Stop and ask the user; a document split (Step 1) reorganizes delivery — every split proposal still gets written, nothing is cut |
| "Refer to module X" or "similar to page Y" without specifics | Show the concrete contract, code path, or interaction detail |
| Introducing unnecessary complexity (new framework/middleware/library/abstraction) | Use the simplest approach with the existing tech stack; recommend a simpler path when available |
| "While we're at it" refactoring of unrelated modules or pages | Only changes within the requirement's scope |
| Writing out full implementations, method bodies, or a file-by-file edit list | Stay at the contract/interface level; full implementation belongs to `ss-plan` and the coding phase |
| Only covering the happy path for UI-facing work | List every affected page/screen state: Normal / Loading / Empty / Error / Edge Case |

## Process

### Step 1: Scope Check & Repository Boundary

After reading the PRD, identify what's relevant to **this repository**:

1. **Identify this repository's role.** Read the project's own docs (README, architecture notes) or analyze the codebase to understand what this repository is responsible for — a backend service, a frontend app, or both.
2. **Extract the relevant scope from the PRD.** A PRD typically spans multiple services and frontends. Filter out only the parts that belong to this repository.
3. **Define the boundary.** Clearly identify:
   - What this repository WILL implement (in-scope functionality, pages, or endpoints)
   - What belongs to other repositories (out-of-scope, marked as an external dependency)
   - Integration points with other repositories (APIs to call/expose, cross-app navigation, shared components)
4. **Record the repository list.** The proposal MUST carry a structured field, **`Repositories Involved:`**, in its summary-design section — every repository whose code must change for this requirement (write the current repo's name if it's single-repo). Do not count a shared API-contract repo or spec submodules. Downstream workflows read this field for multi-repo routing — see `../ss-references/multi-repo-detection.md`.

If the in-scope work involves **3+ independent subsystems**, **5+ independent pages/screens**, or **spans 2+ sub-apps/micro-frontend modules**:
- Suggest splitting into multiple independent proposals.
- Each proposal should be independently deliverable and verifiable.
- Confirm the split approach with the user before continuing.

If the requirement is focused, proceed.

### Step 2: Context Gathering

1. **Read the PRD/requirement** using the method decided in Inputs above. For UI-facing work, focus on user operation flows.
2. **Parse related documents.** Read the linked issue/task, PRD, related technical proposals (e.g., a companion backend or frontend proposal), and design links if present; extract scope, terms, dependencies, and interaction constraints.
3. **Discover API definitions.** Search the repository for OpenAPI YAML files (e.g., under `api/`, `contracts/`, `docs/api/`, or any `*.yaml`/`*.yml` with OpenAPI markers). If found, read the relevant definitions.
4. **Analyze the existing architecture** by inspecting the codebase directly. Whichever of these apply to this repository:
   - Module/package structure, layering, and existing design patterns (backend)
   - Navigation/route structure — pages / views / screens / navigator (frontend)
   - State management approach — e.g., DI and data-access patterns (backend); Vuex/Pinia/Redux/Zustand (Web), MVVM/Combine/TCA (iOS), ViewModel/LiveData/Compose state (Android), Provider/Riverpod/Bloc (Flutter)
   - UI building blocks — component library, design system, native views, widgets (frontend)
   - Existing similar feature implementations to use as reference
5. **Discover linked designs.** If the PRD references a Figma (or similar design-tool) URL and you have a way to read it, fetch the page list and navigation relationships, component hierarchy, and interaction states (hover/active/disabled/error, etc.).

### Step 3: Write the Proposal

Generate the proposal following the template in `../ss-references/proposal-template.md`. Read that file first, then fill in each section — skipping only the subsections that plainly don't apply to this repository's shape (e.g., a pure backend service skips the UI-contract subsection; a pure frontend app skips the data-model subsection).

The output is a single Markdown document.

**Language:** write the proposal in the same language as the PRD/requirement input, or the language the repository's other docs already use; default to English if neither gives a clear signal. Code, DDL, and technical identifiers stay in their original form regardless.

#### Key Principles

- Every design decision states a reason (why this approach?).
- Assumptions are explicit (e.g., "assumes peak QPS < 5000" or "assumes data volume < 10k rows").
- Success criteria are verifiable (e.g., "P99 < 200ms", not "good performance").
- Change points include a "current approach → new approach" comparison, described at the contract level — prose and, where it clarifies an interface, a short pseudocode sketch. Full implementations and file-by-file edit lists don't belong here.
- All schema changes are complete (e.g., full `CREATE TABLE` with columns, indexes, comments — or the equivalent for this stack).
- All new or changed APIs have full request/response definitions.
- Every UI unit specifies its inputs (props/parameters) and outbound events/callbacks; every page/screen covers Normal/Loading/Empty/Error/Edge-case states.
- Data structures align with the API contract on both sides (field names and types match).

#### Diagrams

- **UML and flow diagrams** (architecture, sequence, activity, class, navigation, component hierarchy): use PlantUML or Mermaid syntax in fenced ```plantuml or ```mermaid code blocks.
- **Simple structural diagrams** (directory trees, component/data flow, page hierarchy): use ASCII art.
- Prefer diagrams over long text for system interactions, flows, and relationships.

### Step 4: Self-Review

After writing, run this checklist:

**1. Requirement coverage**
- Check each functional point, page, and feature in the PRD (and in the linked design, if one was provided); each must have a corresponding design in the proposal.
- List and fill any gaps.

**2. Scope reduction scan**
- Search the proposal for phasing/deferral language: MVP, Phase 2, staged rollout, later iteration, simplified version, core-only, P0-only.
- Every hit must trace to an explicit user instruction recorded in the proposal; otherwise design the missing scope now.

**3. Placeholder scan**
- Search for: TBD, TODO, "to be determined", "to be added later", "similar to", "refer to".
- Replace all with concrete content.

**4. Implementation-depth check**
- Scan for full method bodies, complete file listings, or step-by-step coding instructions that have crept past the contract level — trim them back to interface/contract descriptions and defer the rest to `ss-plan`.

**5. Template completeness**
- Every applicable section has substantive content.
- The data model (if present) has a complete schema; APIs (if present) have complete request/response definitions; UI contracts (if present) specify props/state/events and cover all page states.
- The risk table has at least 2 risk items.
- The `Repositories Involved:` field is present (repo list from Step 1; multi-repo routing depends on it).

**6. Consistency check**
- Class/method/table/component/endpoint names are consistent throughout.
- Modules in architecture diagrams match those in the detailed design.
- Store/state field names match their usage in the detailed design.

**7. PlantUML/Mermaid validation**
- For each PlantUML diagram, render it via a PlantUML server — the public instance at `https://www.plantuml.com/plantuml`, or a local/self-hosted renderer if the project configures one — by encoding the source and requesting `/png/{encoded}` or `/svg/{encoded}`.
- Verify the rendered image has no syntax-error text.
- If your environment doesn't support image inspection, skip this step.

Fix any issues found immediately, then continue.

### Step 5: Independent Review (if subagents are available)

If your tool supports spawning a subagent with fresh context:

- Spawn an independent review agent with:
  - Input: the generated proposal Markdown file.
  - Reference: `../ss-references/proposal-writing.md` (quality-standards checklist).
  - Task: review the proposal against every checklist item and report issues.
- The review agent must not have seen the generation process — fresh context is what makes the review independent.
- Fix any issues the reviewer finds before proceeding to output.

If subagents aren't available, skip this step — the Step 4 self-review is sufficient.

### Step 6: Output

Write the proposal as a Markdown file to the `docs/proposals/` directory in the repository:

- File name format: `YYYY-MM-DD-<feature-name>.md`
- Example: `docs/proposals/2026-05-09-order-refund-flow.md`
- Create the `docs/proposals/` directory if it doesn't exist.

### Step 7: Execution Handoff

After output, present next-step options to the user:

```
Proposal generated and saved to docs/proposals/. Suggested next steps:

1. ss-plan on docs/proposals/<file>.md — break the proposal into an executable task plan; Phase 0 automatically generates OpenSpec delta specs
2. ss-coding — start multi-agent parallel coding (for smaller requirements)
3. Manual review — have the team review the proposal first

Which do you prefer?
```
