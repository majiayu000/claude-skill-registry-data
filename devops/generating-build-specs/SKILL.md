---
name: generating-build-specs
description: >
  Generates project-aware pre-build specs using project knowledge and codebase context.
  Phase 1 runs a 7-section spec: outcome contract, states, data contract, failure
  taxonomy, platform constraints, adversarial questions, unknown unknowns. Phase 2
  generates actionable artifacts: build prompt, state scaffold, type definitions, error
  handling scaffold, pre-ship checklist, test scenarios, task list — referencing real
  file paths and patterns, not generic best practices. Use when: pre-build spec, spec
  this out, spec my build, run a spec pass, spec before I code, generate a build spec,
  what will break, surface the gaps, what am I missing before I build, pre-mortem this
  build, what could go wrong, unknown unknowns for this feature, adversarial review of
  my build plan, think through this build, help me plan this feature, build prompt for
  this, state scaffold, error scaffold, type definitions, pre-ship checklist, test
  scenarios, task list for this build, I'm about to build, before I start coding.
metadata:
  version: "1.0.1"
allowed-tools: Read, Glob, Grep
---

# Generating Build Specs

Runs a 2-phase pre-build spec pass using project context. Makes the first real
iteration about refinement, not gap discovery.

---

## Decision Tree

```
User wants to build or spec something?
  ├── Yes — "spec [feature]" / "pre-build spec" / "what will break"
  │   ├── Project knowledge available?
  │   │   ├── Yes → Context-gather first (Step 1), then Phase 1 + Phase 2
  │   │   └── No  → Run Phase 1 from description alone, note the gap
  │   └── User wants only one artifact (e.g. "just the error scaffold")?
  │       └── Skip Phase 1, jump to Phase 2 for that artifact using context
  └── No — don't activate
```

**Scope selector** — read from user message or ask once:
- `LITE` — 3–4 items per section, throwaway builds
- `STANDARD` — 5–7 items, feature work or internal tools (default)
- `FULL` — exhaustive, system-level builds touching auth/payments/user data

---

## Step 1: Context Gathering

Before generating any section, search project knowledge for context that makes
outputs specific to the actual codebase.

Run these searches in sequence. Use whatever is found — if nothing comes back,
proceed with the description and note that output is description-only.

```
project_knowledge_search("error handling patterns")
project_knowledge_search("state management approach")
project_knowledge_search("data models schema types")
project_knowledge_search("test file patterns fixtures")
project_knowledge_search("tech stack deployment config")
```

**What to extract:**
- Existing error class or error handling infrastructure → reference in Failures section and Error Scaffold
- State management pattern (useState, useReducer, Zustand, etc.) → reference in State Scaffold
- Real type names and interfaces → reference in Data Contract and Type Definitions
- Test file structure and imports → reference in Test Scenarios
- Actual file paths for key modules → use in Build Prompt and scaffolds

If project context is found, prefix each section with `[SOURCED]`.
If description-only, prefix with `[GENERATED]`.

---

## Phase 1: Spec Generation

Generate all 7 sections in order. Present each as a headed block.
See `references/spec-sections.md` for detailed instructions per section.

### Section order and scope defaults

| # | Section | What it produces | LITE | STANDARD | FULL |
|---|---------|-----------------|------|----------|------|
| 1 | **Outcome Contract** | Done/failure/context | 3 fields | 3 fields | 3 fields |
| 2 | **States** | Every system state | 4 | 6–7 | exhaustive |
| 3 | **Data Contract** | Inputs/outputs/source/constraints | 3–4/array | 5–7/array | exhaustive |
| 4 | **Failure Taxonomy** | Mode + category + mitigation | 4 | 6–7 | exhaustive |
| 5 | **Platform Constraints** | Concrete gotchas for this build type | 3–4 | 5–7 | exhaustive |
| 6 | **Adversarial Questions** | What breaks, what was assumed handled | 4 | 5–6 | 7+ |
| 7 | **Unknown Unknowns** | Things specific to this build not thought of | 3–4 | 5–7 | exhaustive |

### Phase 1 output format

For each section, output:

```
### [Section Name]
[SOURCED or GENERATED]

[Content — list items or structured fields depending on section type]
```

After all 7 sections, pause and ask: "Generate artifacts for all sections, specific
sections, or skip Phase 2?"

---

## Phase 2: Artifact Generation

Each section maps to one actionable artifact. Generate on request — either all at
once or per section. Use project context gathered in Step 1 to make outputs
reference real file paths and extend real patterns.

See `references/artifact-types.md` for detailed instructions per artifact.

| Section | Artifact | What it is |
|---------|----------|-----------|
| Outcome Contract | **Build Prompt** | Ready-to-paste brief for the actual build session |
| States | **State Scaffold** | useReducer / state machine with every state typed |
| Data Contract | **Type Definitions** | Interfaces + Zod schema + parse functions |
| Failure Taxonomy | **Error Scaffold** | AppError class, classifier, per-category handlers |
| Platform Constraints | **Pre-Ship Checklist** | Verify-before-merge checklist by severity |
| Adversarial Questions | **Test Scenarios** | Test file with describe/it stubs per question |
| Unknown Unknowns | **Task List** | Pre-mortem tickets with acceptance criteria |

### Phase 2 output format

For each artifact:

```
### [Artifact Name] — [Section it comes from]
[SOURCED: references X from project] OR [GENERATED: no project context]

\```[language]
[artifact content]
\```
```

---

## Platform Constraint Reference

Used in Section 5 and the Pre-Ship Checklist. Match to declared or inferred build type.

| Build Type | Key Constraints |
|-----------|----------------|
| React Artifact | No localStorage/sessionStorage, no runtime npm, CORS blocks external fetches, React state = only persistence, bundled libs only |
| Live Artifact | No client API key, max_tokens is a real output limit, streaming interruption must be handled |
| Base44 | Bearer auth pattern, n8n webhook integration, Supabase data layer |
| n8n Workflow | Node execution order, credential scoping, webhook URL exposure, error branches required |
| Prompting Toolkit | Injection surface, output variability, eval criteria needed, model version pinning |
| Chrome Extension | MV3 service worker lifecycle, CSP restrictions, cross-origin messaging limits |
| API / Backend | Auth/session, injection vectors, rate limiting, secret exposure via bundle |
| Supabase + RLS | RLS silently drops policies on schema overwrite, service_role key server-side only |

---

## Failure Category Reference

Used in Section 4 (Failure Taxonomy) and the Error Scaffold.

| Category | Covers |
|----------|--------|
| Network | Timeouts, CORS, DNS, connectivity loss |
| API | External service errors, rate limits, auth failures |
| Data | Null/malformed/missing data, schema drift |
| Input | Bad user input, injection attempts, edge-case strings |
| UI | Render failures, missing states, layout breaks |
| Platform | Environment-specific limits (see table above) |
| Auth | Session expiry, permission errors, token issues |
| Cost | Token budget overflow, API cost overrun |
| Race | Concurrent updates, stale state, out-of-order responses |

---

## Output Protocol

1. Start with a 1-line TL;DR: what's being built, declared scope.
2. Run Step 1 (context gathering) silently — don't narrate every search.
3. Present Phase 1 sections in order with `[SOURCED]`/`[GENERATED]` labels.
4. After Phase 1, ask about Phase 2 scope before generating artifacts.
5. In Phase 2, note which real file paths / patterns are referenced.
6. End with: CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS footer per global preferences.

---

## Self-Verification Checklist

Before outputting:
- [ ] Did I search project knowledge before generating any section?
- [ ] Are all states enumerated including async in-flight, async failed, and edge cases?
- [ ] Does the failure taxonomy match the declared build type (not just generic categories)?
- [ ] Are platform constraints specific to the build type, not generic?
- [ ] Do adversarial questions reference specific behaviors of this build?
- [ ] Does the Build Prompt reference actual states, failures, and platform constraints?
- [ ] Do code scaffolds reference real file paths or imports from project context?
- [ ] Is every item labeled `[SOURCED]` or `[GENERATED]`?

---

## Eval Scenarios

### Should trigger:
1. "Pre-build spec for the new approval queue panel"
2. "Spec this out before I start coding — it's a Base44 app that routes n8n webhooks to Supabase"
3. "What will break when I build this? It's a React artifact that calls the Anthropic API"
4. "Run a spec pass on the CFO cost modeling tool"
5. "I'm about to build the agent dashboard — help me think through what I'm missing"

### Should NOT trigger:
1. "Write a LinkedIn post about my build process" (content creation)
2. "Debug this error in my existing code" (debugging, not speccing)
3. "What's the best way to do state management in React?" (general question)
