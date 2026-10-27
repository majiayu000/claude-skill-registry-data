---
name: harness-engineering-copilot
description: >-
  Strategies, workflows, patterns, and best practices for maximizing harness
  engineering through GitHub Copilot agent customization. Focuses on how to
  structure context layering, design multi-agent constraint enforcement,
  implement checklist-driven audit loops, manage prompt and embed budgets,
  define artifact ownership, scale customization across repos, and evolve
  harnesses over time. For Copilot-specific syntax, file formats, and
  configuration rules, defer to the `agent-customization` skill.
  Triggers: "copilot harness", "copilot harness strategy", "agent-first copilot",
  "copilot harness patterns", "copilot context layering", "copilot agent fleet",
  "copilot entropy management", "copilot harness maturity", "scale copilot harness",
  "copilot customization strategy", "maximize copilot harness", "copilot harness checklist",
  "agent prompt budget", "instruction compression", "multi-agent audit",
  "agent variant", "runtime-specific tools", "custom agent runtime".
metadata: 
  version: 1.0.0
  author: arisng
---

# Harness Engineering for GitHub Copilot

Strategies and patterns for building high-leverage harnesses through Copilot's customization system. A harness is the scaffolding — context layering, constraint enforcement, entropy management, and feedback loops — that makes agents reliably productive.

**Related skills**:
- `harness-engineering` — generic methodology (tool-agnostic).
- `agent-customization` — Copilot file formats, syntax, YAML frontmatter, tool aliases, and configuration rules. **Defer all "how do I write this file" questions there.**

**Sources**: [OpenAI — Harness Engineering](https://openai.com/index/harness-engineering/) | [Martin Fowler — Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)

Use this skill in two modes:

1. **Design mode** — decide how to layer context, split roles, and add enforcement.
2. **Audit mode** — review an existing Copilot harness with fixed passes, explicit budgets, and consistency checks.

---

## Strategy 1: Context Layering

Context is a scarce resource. The harness must deliver the *right* context at the *right* time — not dump everything into every interaction.

### The Three-Tier Context Model

| Tier | Copilot primitive | When it loads | Budget | What belongs here |
|---|---|---|---|---|
| **Always-on** | `copilot-instructions.md`, path-scoped `.instructions.md` | Every interaction (auto) | ~100 lines repo-wide; ~50 lines per path scope | Architecture map, boundary rules, pointer references |
| **On-demand** | Agent skills (`SKILL.md`) | When Copilot detects relevance | <500 lines body + unlimited references | Deep domain knowledge, schemas, runbooks |
| **Task-scoped** | Prompt files (`.prompt.md`), agent prompts | When user explicitly invokes | No hard limit (30K chars for agents) | Step-by-step workflows, checklists, batch operations |

### Cross-Check with `agent-customization` skill

Use the `agent-customization` decision flow to decide **which primitive owns which layer** instead of choosing files ad hoc.

| Context layer | Preferred primitive | Why this fits | `agent-customization` check |
|---|---|---|---|
| **Always-on** | Workspace instructions | Auto-loaded context should only hold stable routing rules and boundary constraints | Keep `applyTo` narrow; avoid `applyTo: "**"` unless the rule truly applies everywhere |
| **Always-on, path-specific** | File instructions | Architectural rules should follow folder or module boundaries | One instruction file per boundary, with explicit `applyTo` globs matching repo structure |
| **On-demand** | Skills | Deep reference material should load only when the task is relevant | Put discovery phrases in `description`; keep body lean and offload depth to references/assets |
| **Task-scoped** | Prompts | Repeatable batch workflows should be explicit, not always resident in context | Use prompts for single focused tasks with parameters |
| **Task-scoped with isolation** | Custom agents | Multi-stage work or restricted tool use needs isolated context and an enforcement contract | Use an agent when you need delegation, context isolation, or different tool boundaries per stage |

Before adding a new file, ask the `agent-customization` questions in this order:

1. **Scope**: Is this workspace-shared behavior or a personal preference?
2. **Primitive**: Is this always-on guidance, on-demand knowledge, a single focused prompt, or a delegated subagent workflow?
3. **Discovery**: Will Copilot find it from the `description`, or are you relying on file names and hope?
4. **Load cost**: Does this belong in auto-loaded context, or should it stay dormant until invoked?

If you cannot answer those four questions clearly, the layer boundary is still underspecified.

### Context Layering Best Practices

1. **Map, don't manual.** Always-on instructions should be a table of contents pointing to deeper sources elsewhere in the repo. If your `copilot-instructions.md` exceeds ~100 lines, you're overloading Tier 1.
2. **One instruction file per architectural boundary.** Use `applyTo` glob patterns that mirror your module/layer structure. When an agent edits `src/server/**`, it should receive server-layer rules — not frontend rules.
3. **Skills as progressive disclosure.** Move detailed reference material (DB schemas, API specs, deployment procedures) into skills with `references/` folders. The SKILL.md body stays lean; the agent loads `references/schema.md` only when actually needed.
4. **Honor the primitive boundary.** If the content is multi-step workflow logic, it probably belongs in a prompt or custom agent, not in always-on instructions. If it is durable domain knowledge, it probably belongs in a skill, not a prompt.
5. **Redundancy kills.** Never duplicate content across tiers. If a convention is in `copilot-instructions.md`, don't repeat it in a skill. Use cross-references instead.
6. **Pointer chains, not deep nesting.** Every reference should be at most one hop from an entry point. If an agent needs to follow `AGENTS.md → docs/index.md → docs/design-docs/index.md → docs/design-docs/auth.md`, that's too deep. Flatten to `AGENTS.md → docs/design-docs/auth.md`.
7. **Treat `description` as part of the harness.** A skill or agent that cannot be discovered by its `description` is effectively missing from the harness, even if the file exists.

### Context Freshness Strategy

Stale context is worse than no context — agents confidently follow outdated rules.

- **CI validation**: Add a job that checks cross-references between instruction files and actual repo paths. If an instruction references `docs/RELIABILITY.md` and the file doesn't exist, fail the build.
- **Git-blame-based staleness**: Flag instruction files not updated in >90 days alongside the code they govern. If `backend.instructions.md` hasn't changed but `src/server/` has had 50 commits, something is probably stale.
- **Changelogs as triggers**: When a significant architectural change merges, add "update harness" to the PR checklist. Treat instructions as code that must be kept in sync.

---

## Strategy 2: Multi-Agent Constraint Enforcement

A single omniscient agent is an anti-pattern. Design an **agent fleet** (agent squad/agent swarm) where each agent has a narrow responsibility and minimal tool access.

### The Observer / Actor / Maintainer Triad

| Role | Purpose | Tool profile | Invocation |
|---|---|---|---|
| **Observer** | Detect violations, audit quality, report findings | `read` + `search` only | On-demand or scheduled |
| **Actor** | Implement changes within enforced boundaries | `read` + `edit` + `search` + `execute` | Task-driven |
| **Maintainer** | Fix drift, update docs, refactor toward golden principles | `read` + `edit` + `search` | Scheduled/periodic |

### Designing an Agent Fleet

**Step 1: Identify enforcement surfaces.** List every invariant you want to enforce (dependency direction, naming, logging, test coverage, doc freshness). Each surface maps to an Observer agent.

**Step 2: Define tool boundaries.** For each agent, ask: *What's the minimum tool set needed?* An architecture reviewer needs `read` + `search`, never `edit`. A test generator needs `execute` to run tests. Over-provisioning tools undermines the harness.

**Step 3: Write agent prompts as enforcement contracts.** The agent's markdown body is its enforcement contract — a precise specification of what to check, what to flag, and how to remediate. Structure every enforcement agent prompt as:

```
1. SCOPE: What files/modules to examine
2. RULES: Numbered invariants to check (reference docs/ for details)
3. PROCESS: Step-by-step verification procedure
4. OUTPUT: Exact format for findings (file, line, violation, remediation)
5. BOUNDARIES: What the agent must NOT do
```

**Step 4: Chain agents for complex workflows.** Use subagent invocation (`agent` tool alias) to compose:
- *Planner* (read-only) → produces a plan
- *Implementor* (full tools) → executes the plan
- *Reviewer* (read-only) → validates the result

This mirrors the "Ralph Wiggum Loop" pattern: agents review each other's work in a feedback loop until all reviewers are satisfied.

### Least-Privilege Patterns

| Pattern | Strategy | When to use |
|---|---|---|
| **Read-only observer** | `tools: ["read", "search"]` | Auditing, reviewing, scanning |
| **Edit-no-execute** | `tools: ["read", "edit", "search"]` | Documentation updates, config changes, refactoring |
| **Full actor** | `tools: ["read", "edit", "search", "execute"]` | Implementation requiring test runs or builds |
| **Scoped MCP** | `tools: ["read", "search", "playwright/screenshot"]` | Agents that need one specific external capability |
| **Subagent-only** | `tools: ["read", "search", "agent"]` | Orchestrators that delegate all work |

### Runtime-Specific Tool Assignment

Use **runtime** to describe the Copilot execution environment of the agent file: VS Code, GitHub Copilot coding agent, CLI-backed coding flows, background agents, cloud agents, or an SDK-hosted flow that adopts one of those schemas. Use **platform** for OS scope such as Windows, WSL/Linux, or macOS.

When the same specialist role needs different frontmatter, tool namespaces, or delegation mechanics across runtimes, create an **agent variant**: a runtime-specific `.agent.md` wrapper over shared instructions.

### Official Runtime Facts to Design Around

| Fact | Design implication |
|---|---|
| `target` is officially `vscode` or `github-copilot` | Scope each variant to the runtime family it is meant for instead of assuming one file behaves identically everywhere |
| `tools` defaults to all tools when omitted; `tools: []` disables all tools | Omit `tools` only when you genuinely want broad capability; otherwise whitelist aggressively |
| Unrecognized tool names are ignored | A mixed-runtime tool list can fail silently; audit tool names per runtime rather than trusting parse success |
| `disable-model-invocation` is the canonical control and `infer` is retired | Use the new field when deciding whether a variant is user-selectable, subagent-only, or both |
| VS Code exposes `agents`, `argument-hint`, `handoffs`, and richer tool discovery | Keep VS Code orchestration and guided transitions in the VS Code variant instead of leaking them into shared instructions |
| GitHub Copilot runtime supports `mcp-servers` and namespaced MCP tools | Put runtime-specific MCP wiring in the `github-copilot` variant, not in the shared behavior contract |

### Agent Variant Pattern

Split each specialized agent into two layers:

1. **Shared instruction layer**: persona, rules, workflow, artifacts, output contract, and tool-agnostic wording.
2. **Runtime variant layer**: `target`, `tools`, `agents`, `handoffs`, `mcp-servers`, and any runtime-specific tool references.

The shared layer should say **what capability is required**, not **which runtime-specific tool name to call**. Write "read the file", "run tests", or "delegate to the reviewer" rather than embedding a runtime-specific token.

### Tool Assignment by Runtime Family

Use the official `target` values in the variant frontmatter: `vscode` or `github-copilot`.

| Runtime family | Frontmatter focus | Tool assignment rule | Delegation model |
|---|---|---|---|
| **VS Code** | `target: vscode`, optional `agents`, `argument-hint`, `handoffs`, `model` | Use VS Code tool names, toolsets, extension tools, or MCP namespaced tools. If `agents` is specified, include the `agent` tool. | Explicit subagent wiring via `agents` |
| **GitHub Copilot** | `target: github-copilot`, optional `mcp-servers`, `disable-model-invocation`, `user-invocable` | Prefer official aliases such as `read`, `edit`, `search`, `execute`, `agent`, plus namespaced MCP tools like `playwright/*` or `github/*` | Delegation through model invocation and custom-agent/task tooling |
| **Background or cloud agent flow** | Usually inherits the VS Code custom-agent model | Reuse a VS Code-oriented variant unless the host removes or overrides tools | Same as host runtime |
| **SDK-hosted flow** | Treat as host-defined until proven otherwise | Do not assume `.agent.md` fields or tool names map 1:1; align the variant to the runtime actually consuming it | Host-dependent |

### Assignment Heuristics

1. Start from the minimum capability set needed for the role.
2. Assign tools per runtime, not per persona. The reviewer persona may be read-only in every runtime, but the concrete tool names still differ.
3. Put MCP server selection in the variant that can actually load it.
4. Keep body text free of runtime-specific tool names unless the file is explicitly runtime-locked.
5. Re-measure orchestration after tool changes. A variant that adds subagent access, shell execution, or MCP tools has changed its effective safety boundary.

### Failure Modes to Audit

- A VS Code-only tool name in a `github-copilot` variant silently disappears.
- A shared instruction body mentions a tool token that only exists in one runtime.
- A runtime variant inherits an all-tools default because `tools` was omitted unintentionally.
- A subagent-only variant still allows model invocation because `disable-model-invocation` was not set.
- A team treats Windows, Linux, or macOS as the runtime boundary when the real difference is the Copilot host.

### Prompt Engineering for Enforcement

Agent prompts in a harness serve a different purpose than general-purpose prompts. They are **mechanical contracts**, not creative guidance.

- **Be exhaustive about rules, terse about explanation.** Don't explain *why* a rule exists in the agent prompt — put that in docs. The prompt should list exactly what to check.
- **Include remediation in the output format.** When an observer reports a violation, it should include the fix instruction. This becomes context for the actor agent that fixes it.
- **Avoid open-ended judgment calls.** "Review code quality" is too vague. "Check that every public function in `src/server/` has a corresponding test in `tests/server/`" is enforceable.
- **Reference, don't inline.** Agent prompts should point to `ARCHITECTURE.md` or `docs/conventions/` for rule details rather than reproducing them. This prevents the prompt from going stale independently.

---

## Strategy 3: Operational Audit Protocols

Harnesses usually fail in the operational details, not in the high-level design. Convert repo-specific review checklists into a reusable audit protocol with explicit passes and measurable outputs.

### The Five Audit Passes

| Pass | Question | Typical checks |
|---|---|---|
| **Structural contract** | Does each instruction or agent file contain the sections the workflow depends on? | Required sections present, numbered rules complete, one shared protocol block instead of duplicates, output contracts match referenced artifacts |
| **Budget discipline** | Is every prompt body below the runtime limit with safety margin? | Soft ceiling below hard max, frontmatter excluded from measurement, embedded agent body re-measured after every instruction change |
| **Consistency** | Do names, signals, paths, and schemas line up across files? | Exact agent names, exact delegation targets, one signal vocabulary, one path convention, no deprecated frontmatter keys |
| **Ownership** | Does every writable artifact have exactly one owner? | Planner-only artifacts stay planner-owned, shared progress artifacts are append-only, reviewers observe rather than overwrite |
| **Distribution** | Will the runtime load this deterministically? | Build-time embedding or bundling, no runtime instruction reads for CLI-only bodies, official plugin schema only |

### Audit Output Contract

Every audit pass should report findings in a fixed shape:

| Field | Meaning |
|---|---|
| **Artifact** | File, folder, or workflow surface being checked |
| **Invariant** | Exact rule that failed |
| **Evidence** | Concrete mismatch: missing section, wrong name, over-budget body, conflicting owner |
| **Remediation** | Smallest change that restores consistency |
| **Re-run trigger** | What future edit should force this pass to run again |

### Compression Is a Harness Capability

Prompt compression is not cosmetic. It preserves budget for task context and reduces drift.

**Always remove**:
- Motivational preambles before the real contract
- Inline explanations of why a rule exists
- Duplicated protocol blocks repeated per mode
- Example output blocks that only restate an existing schema
- Verbose decision trees better expressed as flat steps

**Always preserve**:
- All numbered rules in the enforcement contract
- Every supported mode name and its complete step list
- Exact path patterns and naming conventions
- Contract field names, required/optional status, and signal schema
- Preflight gates and failure-mode handling

### What to Measure

For every auditable harness, keep a small measurement set close at hand:

1. Prompt body length after frontmatter stripping.
2. Combined wrapper-plus-embedded body length for distributed agents.
3. Count of active signal types and whether all files use the same schema.
4. Artifact ownership table: one writer per artifact, explicit shared append-only logs.
5. Revalidation triggers: which edits force which audit passes.

---

## Strategy 4: Entropy Management

Every agent-generated line of code can introduce drift. Entropy management is the discipline of detecting and correcting drift before it compounds.

### Golden Principles Framework

Define a small set (5–10) of non-negotiable, mechanically verifiable rules:

| # | Principle | Verification method |
|---|---|---|
| 1 | Shared utilities over hand-rolled helpers | Lint: flag duplicate utility patterns |
| 2 | Parse data at boundaries, never YOLO-probe | Lint: detect untyped API calls |
| 3 | Structured logging with correlation IDs | Lint: flag `console.log` / raw `print` |
| 4 | One module = one domain, no cross-domain imports | Structural test: import graph validation |
| 5 | Every public API has a test | Coverage check: map exports → test files |

**Key insight**: Golden principles must be verifiable by linters, structural tests, or agents — not just documented. If you can't automate the check, it's a guideline, not a golden principle.

### Garbage Collection Cadence

| Frequency | What to check | Agent type |
|---|---|---|
| **Per-commit** (CI) | Lint rules, structural tests, doc cross-references | Deterministic (linters/tests) |
| **Daily** | Doc freshness, quality score drift, stale TODOs | Maintainer agent |
| **Weekly** | Golden principle deviations, pattern duplication, tech debt inventory | Maintainer agent, batch prompt |
| **Per-sprint** | Full quality scoring across all domains/layers | Observer agent + human review |

### Quality Scoring Pattern

Maintain a versioned `QUALITY_SCORE.md` that grades each domain and layer:

```markdown
| Domain | Types | Config | Service | Tests | Docs | Overall |
|--------|-------|--------|---------|-------|------|---------|
| Auth   | A     | A      | B       | B     | C    | B       |
| Billing| A     | B      | B       | C     | D    | C+      |
| Search | B     | B      | C       | D     | F    | D+      |
```

This gives both humans and agents a **map of where debt lives**. A maintainer agent can read this and prioritize: "Search.Docs is F — generate missing documentation for the Search domain."

### Entropy Detection Strategies

1. **Pattern divergence scan.** Compare how a pattern is implemented across modules. If 8 out of 10 services use structured logging but 2 use `console.log`, flag the outliers.
2. **Doc/code freshness ratio.** If `src/billing/` changed 30 times this month but `docs/billing.md` changed 0 times, the docs are likely stale.
3. **Lint error message engineering.** Write custom lint error messages that include remediation instructions. When a linter reports "Import from `auth/` in `billing/` violates boundary — move shared types to `shared/types/`", the agent can act on it directly. The error message *is* the agent's instruction.
4. **Snapshot diffing.** Periodically generate a snapshot of the repo structure (file tree, import graph, export map) and diff against the previous snapshot. Large deltas without corresponding doc updates signal drift.

---

## Strategy 5: Application Legibility

Agents can only verify what they can observe. Extending the agent's senses beyond static files dramatically increases harness leverage.

### Legibility Layers

| Layer | What the agent can see | Copilot mechanism | Harness value |
|---|---|---|---|
| **Static files** | Source code, docs, config | Built-in (read/search) | Baseline — always available |
| **Build/test output** | Compilation errors, test results, lint output | `execute` tool | Validates correctness |
| **Browser state** | DOM, screenshots, navigation, console errors | MCP (Playwright) | UI verification without manual testing |
| **Runtime telemetry** | Logs, metrics, traces | Custom MCP server | Performance and reliability validation |
| **Repository state** | Issues, PRs, CI status, branch state | MCP (GitHub) | Workflow-aware decisions |

### Legibility Best Practices

1. **Make the app bootable per task.** If an agent can't start the application in isolation, it can't validate its own work. Design for single-command startup (Docker Compose, Aspire, etc.).
2. **Wire browser automation for UI verification.** An agent that edits a Blazor component should be able to screenshot the result. This closes the feedback loop without human eyes.
3. **Expose observability to the agent.** If you have logs and metrics, make them queryable. An agent instruction like "ensure no error logs during startup" is only enforceable if the agent can read the logs.
4. **Ephemeral environments.** Each agent task should run against an isolated instance. Shared environments introduce cross-task interference that agents can't reason about.

---

## Strategy 6: Harness Evolution

A harness is not a one-time setup. It evolves with the codebase.

### Maturity Model

| Level | Context | Constraints | Entropy | Legibility |
|---|---|---|---|---|
| **1 — Ad-hoc** | No instructions | No enforcement | No cleanup | Static files only |
| **2 — Documented** | `copilot-instructions.md` exists | Conventions documented but not enforced | Manual cleanup | Build/test output |
| **3 — Scoped** | Path-scoped instructions + skills | Linters catch some violations | Weekly batch prompts | Browser automation |
| **4 — Enforced** | Full three-tier context | Structural tests + CI gates block violations | Daily maintainer agents | Runtime telemetry |
| **5 — Self-healing** | Agent-maintained instructions | Agents detect and fix violations autonomously | Continuous GC with quality scoring | Full stack legibility |

### Evolution Workflow

1. **Assess.** Use the harness assessment from the `harness-engineering` skill. Rate each component 0–2.
2. **Target one level up.** Don't jump from Level 1 to Level 5. Move one level at a time per component.
3. **Instrument before enforcing.** Before adding a linter, add an observer agent to measure the current state. Quantify violations before blocking them.
4. **Encode human taste continuously.** Every time a human reviews agent output and says "that's not how we do it here," capture the rule — as a lint rule, instruction update, or golden principle. Never rely on the same correction twice.
5. **Retroactively harness brownfield code.** Start with context engineering (cheapest, highest ROI), add constraints per-module as you touch them, and add entropy management last.

### Revalidation Triggers

Tie harness maintenance to concrete change events instead of vague periodic reviews.

| Change | Re-run |
|---|---|
| **Instruction body changed** | Structural contract, budget discipline, consistency |
| **Agent frontmatter or delegation changed** | Consistency, distribution |
| **Signal schema changed** | Consistency across every agent and instruction |
| **Workflow paths changed** | Structural contract, ownership, consistency |
| **Plugin or bundle pipeline changed** | Distribution and budget discipline |

If a harness cannot tell you which checks to rerun after a change, it is still too implicit.

### Scaling Across Repositories

For organizations with multiple repos:

- **Harness template repos.** Create starter repo templates with pre-configured instruction files, standard agent fleet, and CI validation jobs. This parallels "golden path" service templates, optimized for agent-driven development.
- **Org-level agents.** Define organization-wide enforcement agents (via `.github-private` repo) that apply everywhere. Keep repo-level agents for domain-specific concerns.
- **Shared skills as packages.** Extract common skills (architecture validation, deployment runbooks) into a shared repo and publish to personal skill directories for cross-repo reuse.
- **Federated golden principles.** Maintain a core set of golden principles organization-wide, with repo-specific extensions. Enforce the core set from org-level; let repos own their extensions.

---

## Anti-Patterns

| Anti-pattern | Why it fails | Better strategy |
|---|---|---|
| **Monolithic instructions** | Crowds out task context at 1000+ lines; rots fast | Three-tier context layering with 100-line Tier 1 |
| **One omniscient agent** | No tool boundaries; can't reason about everything at once | Agent fleet with Observer / Actor / Maintainer roles |
| **Duplicate context** | Same rule in instructions, skills, and agent prompts diverges over time | Single source of truth with cross-references |
| **Verbal-only enforcement** | "We always do X" isn't legible to agents | Encode in linters, tests, or observer agents |
| **Big-bang cleanup** | 20% of the week on "AI slop" doesn't scale | Continuous garbage collection at daily cadence |
| **Static-only legibility** | Agent can't verify its own UI changes or performance | Wire browser automation and observability MCP |
| **Set-and-forget harness** | Codebase evolves, harness doesn't | Treat instructions as code; CI-check freshness |
| **Open-ended agent contracts** | "Review code quality" produces inconsistent results | Precise enforcement contracts with numbered rules |
| **Checklist-free maintenance** | Review quality depends on memory and reviewer taste | Encode reusable audit passes with fixed outputs and triggers |
