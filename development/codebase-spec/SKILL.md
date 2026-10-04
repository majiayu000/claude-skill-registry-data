---
name: codebase-spec
description: >
  Use this skill whenever the user wants to reverse-engineer, document, or migrate a codebase.
  Triggers include: "write a spec for this codebase", "document this project", "I want to migrate
  this to another language", "create a spec I can use to reimplement this", "reverse engineer this
  code", "document the architecture", "I want to port this codebase", or any time the user points
  at a directory or project and wants a thorough written understanding of it. Use this skill even
  if the user just says "understand my codebase" or "help me document this project" — the output
  is always a structured, multi-document spec suite. Designed for large codebases (100+ files) but
  works at any scale.
---

# Codebase Spec Skill

Reads a codebase and produces a **multi-document specification suite** — thorough enough that an engineer (or an AI agent) can reimplement the entire codebase in a different language from the docs alone, with no access to the original source.

---

## Phase 0: Orientation

Before reading any code, build a map of the codebase:

```bash
find . -type f | sort          # full file list
cat README* 2>/dev/null        # top-level readme
cat package.json / pyproject.toml / Cargo.toml / go.mod / pom.xml 2>/dev/null  # manifest
ls -la                         # root structure
```

From this, identify:
- **Language(s)** and runtime
- **Top-level modules / packages** — these become your doc units
- **Entry points** (main files, CLI scripts, server startup, index files)
- **Config and environment** (`.env`, config files, secrets patterns)
- **External dependencies** (libraries, APIs, databases, queues)
- **Test suite location and framework**
- **Build / deploy artifacts** (Dockerfile, CI config, Makefile, etc.)

Announce your findings to the user in a short summary before proceeding:
> "I've mapped the codebase. Found X modules, written in Y, with Z external dependencies. Here's my plan for the spec docs: [list]. Starting with [module]. Let me know if you want a different order."

---

## Phase 1: Ambiguity Protocol

**Always ask before proceeding** when you encounter:
- Code whose purpose is genuinely unclear after reading the surrounding context
- Magic values, undocumented constants, or non-obvious algorithms
- Implicit contracts between modules that aren't expressed in types or comments
- Behavior that appears to be a bug but might be intentional
- Environment-specific logic that can't be inferred statically (feature flags, runtime config)

Format ambiguity questions clearly and batch them — don't ask one at a time if you have several for the same module:

> **Ambiguity check — [ModuleName]**
> Before I document this module, I need to clarify a few things:
> 1. `RETRY_LIMIT = 7` — is this a business rule or an arbitrary default?
> 2. `process_event()` calls `legacy_handler()` only on Tuesdays (line 84). Is this intentional?
> 3. The `UserCache` class appears unused. Should I document it or skip it?
>
> *Please answer all three before I continue.*

Wait for the user's response. Don't proceed with guesses on flagged ambiguities — mark them `[UNRESOLVED - awaiting clarification]` if you somehow move on.

---

## Phase 2: Module-by-Module Analysis

Work through each module/layer identified in Phase 0. For **each module**, read its files fully before writing anything.

Capture for each module:
- **Purpose**: What problem does this module solve?
- **Public interface**: Every function, class, method, or route that other modules depend on
- **Internal logic**: Key algorithms, data transformations, state machines, business rules
- **Data structures**: All significant structs, schemas, models, or types — with field names, types, and semantics
- **Dependencies**: What it imports from inside the codebase; what it imports from outside
- **Side effects**: I/O, DB writes, network calls, file system, external API calls
- **Error handling**: How errors are raised, caught, propagated, or swallowed
- **Configuration**: What env vars or config keys does it read, and what are the defaults?
- **Invariants and assumptions**: What must be true for this module to work correctly?
- **Known limitations**: Hard-coded limits, unhandled cases, TODO comments, deprecated paths

For large modules (>20 files), break them into sub-sections.

---

## Phase 3: Cross-Cutting Concerns

After all modules are documented, write a **Cross-Cutting Concerns** doc covering:

- **Authentication & authorization**: How identity flows through the system
- **Error and exception strategy**: Global error handling patterns
- **Logging and observability**: What gets logged, at what level, where it goes
- **Concurrency and threading model**: Async patterns, thread pools, queues, locks
- **Data validation**: Where and how inputs are validated
- **Security patterns**: Sanitization, secrets management, network boundaries
- **Performance assumptions**: Caching strategy, batch sizes, rate limits, timeouts

---

## Phase 4: Output Documents

Produce the following files in a `spec/` directory at the codebase root (or output path if specified):

```
spec/
├── 00_overview.md          ← Architecture, tech stack, entry points, system diagram
├── 01_requirements.md      ← Functional and non-functional requirements inferred from code
├── 02_assumptions.md       ← What the code assumes to be true about its environment/inputs
├── 03_limitations.md       ← Hard limits, known gaps, unhandled edge cases, TODOs
├── 04_data_models.md       ← All significant data structures, schemas, enums, types
├── 05_api_contracts.md     ← All public interfaces (REST routes, function signatures, events, queues)
├── 06_<module_name>.md     ← One file per major module (repeat as needed)
├── ...
└── NN_cross_cutting.md     ← Auth, error handling, logging, concurrency, security
```

Read the **Document Templates** reference file before writing any doc:
→ `references/doc-templates.md`

### Reimplementation Completeness Test

Before finalizing, ask yourself: *"If someone burned the original codebase and only had these docs, could they rebuild it correctly in a different language?"*

Check that the docs collectively answer:
- [ ] What does the system do at a high level?
- [ ] What are the inputs and outputs of every public interface?
- [ ] What are the data models and their field semantics?
- [ ] What external services/APIs does it integrate with, and how?
- [ ] What are the business rules and invariants?
- [ ] What are the known bugs, limitations, and TODOs?
- [ ] What configuration is required to run this?
- [ ] What does the test suite cover (and what does it miss)?

If any box is unchecked, fill the gap before delivering the docs.

---

## Phase 5: Delivery

When all docs are written:
1. Present the full `spec/` directory to the user
2. Give a one-paragraph summary: what the codebase does, key architectural decisions, and any unresolved ambiguities still marked `[UNRESOLVED]`
3. Explicitly flag anything that would block a clean reimplementation

---

## Tone and Style

- Write for an engineer who has **never seen this codebase** and may be working in a **different language**
- Avoid source-language idioms — describe behavior, not syntax (say "iterates over all users" not "for user in users")
- Use tables for data models and API signatures
- Use numbered lists for ordered processes; bullet lists for unordered properties
- Mark all uncertainty explicitly: `[INFERRED]`, `[UNRESOLVED]`, `[ASSUMED]`
- Never invent behavior — if you don't know, say so

---

## Reference Files

- `references/doc-templates.md` — Exact templates for each output document. **Read this before writing any spec doc.**
