---
name: improve-codebase-architecture-advanced
description: Explore a codebase using qualitative exploration plus quantitative metrics, surface architectural friction, discover testability opportunities, and propose module-deepening refactors as GitHub issue RFCs. Use when user wants a metrics-driven architecture review or deeper refactor proposal than the base skill.
---

# Improve Codebase Architecture (Advanced)

Explore a codebase like an AI would, surface architectural friction using both qualitative exploration and quantitative metrics, discover opportunities for improving testability, and propose module-deepening refactors as GitHub issue RFCs.

A **deep module** (John Ousterhout, "A Philosophy of Software Design") has a small interface hiding a large implementation. Deep modules are more testable, more AI-navigable, and let you test at the boundary instead of inside.

This advanced variant adds rigor from Knuth's "The Art of Computer Programming": algorithm complexity awareness, data structure fitness analysis, fundamental operation counting, and equivalence verification. It also adds churn analysis, cohesion assessment, concurrency boundary detection, and migration cost estimation.

## Process

### 1. Gather quantitative signals

Use the Agent tool to run these in parallel. These are SIGNALS, not conclusions. They tell you WHERE to look, not WHAT is wrong.

**Churn coupling** - Find files that always change together (natural deepening candidates because they're already one logical unit split across files):

```bash
git log --format='%H' --since='6 months ago' | while read hash; do
  git diff-tree --no-commit-id --name-only -r "$hash"
done | sort | uniq -c | sort -rn | head -30
```

Then cross-reference: which pairs of high-churn files appear in the same commits?

```bash
git log --format='%H' --since='6 months ago' | while read hash; do
  git diff-tree --no-commit-id --name-only -r "$hash" | sort | paste -sd, -
done | sort | uniq -c | sort -rn | head -20
```

**Fan-in / fan-out** - Count imports and dependents per module. High fan-out means the module knows too much. High fan-in with high churn means a fragile hub.

**Large files** - Find files exceeding the project's size limits (e.g., SwiftLint's 400-line file limit).

### 2. Verify signals by reading code (MANDATORY)

**This step exists because sub-agents consistently over-report issues based on file-level metrics.** Common failure modes:

- **Conflating file size with function size.** A 400-line file is NOT a 400-line function. The agent must read the actual function bodies, not extrapolate from `wc -l`. A 400-line file with 8 well-factored 50-line methods is fine.
- **Treating all high metrics as problems.** A `Session` type with 63 fan-in that is 76 lines of coherent domain model is not a "hub problem" - it's a core type doing its job. High fan-in on a SMALL, STABLE type is good design, not bad design.
- **Reporting "SRP violations" on single-responsibility code.** An OpenAI-compatible HTTP client that validates, lists models, and sends requests has ONE responsibility: "talk to an OpenAI-compatible API." These are not separate responsibilities.
- **Claiming duplication without diff-verifying.** Two files that "look similar" from grep output may share 10% of code or 90%. Read both files and compare before reporting duplication.
- **Treating normal coupling as problematic coupling.** Settings screens reference many types because they configure many things. This is inherent, not a bug.

**For EVERY candidate identified by metrics, you MUST:**

1. **Read the actual files** involved (not just grep output or line counts).
2. **Read the actual functions** claimed to be problematic. If a metric says "function X is 300 lines," read function X and count its actual lines. Report the real number.
3. **Check whether code is already well-factored.** A large file with clean method extraction is not the same problem as a large file with one monolithic method.
4. **Verify duplication claims by reading both files.** Count the actual duplicated lines. If it's under 50 lines, it may not be worth extracting.
5. **Check the public interface.** If callers only call one entry point (e.g., `manager.trigger(mode:session:)`), the internal 3-file split is an implementation detail, not a coordination burden.
6. **Assess whether splitting would help or hurt.** A 76-line type with 63 fan-in that mixes config and runtime state sounds like a split candidate - until you read it and see that every caller needs both config and runtime together. Splitting would double the import surface with zero coupling reduction.

**Drop candidates that don't survive verification.** It is better to present 1 real finding than 6 inflated ones. The user's time spent evaluating false positives is a direct cost.

### 3. Explore organically for missed issues

After verifying metric-based candidates, explore the codebase naturally and note where you experience friction that metrics missed:

- Where does understanding one concept require bouncing between many small files?
- Where are modules so shallow that the interface is nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called?
- Where do tightly-coupled modules create integration risk in the seams between them?
- Which parts of the codebase are untested, or hard to test?
- Where is code copy-pasted between files? (Read both files to confirm.)

The friction you encounter IS the signal - but only if you can point to specific lines and explain why the current structure causes real problems.

### 4. Present candidates

Present a numbered list of deepening opportunities. Only include candidates that SURVIVED verification in Step 2.

For each candidate, show:

- **Cluster**: Which modules/concepts are involved
- **Evidence**: Specific file paths, line numbers, and concrete code examples. Quote the duplicated code or the problematic interface. No vague claims like "high coupling" without showing the actual coupling.
- **Why they're coupled**: Shared types, call patterns, co-ownership of a concept
- **Cohesion**: Is each module internally cohesive, or does it mix unrelated responsibilities? A module that does three unrelated things should be split first, then each piece deepened.
- **Dependency category**: See [REFERENCE.md](REFERENCE.md) for the four categories
- **Dependency direction**: Are there circular dependencies? Does the direction align with stability (stable-dependencies principle)? Will deepening fix or worsen direction violations?
- **Hot path?**: Is this candidate in the critical 3%? (Knuth: "We should forget about small efficiencies, say about 97% of the time. Yet we should not pass up our opportunities in that critical 3%.") If yes, interface design must not add latency.
- **Migration cost**: Number of callers that must change. Whether migration can be incremental (adapter/shim) or is all-or-nothing.
- **Concurrency boundary?**: Does deepening cross concurrency boundaries (e.g., merging an actor with a non-isolated module, combining thread-safe and thread-unsafe code)? Flag explicitly.
- **Test impact**: What existing tests would be replaced by boundary tests
- **Error propagation**: How do errors flow through the coupled modules today? Does deepening simplify error handling (fewer boundary translations) or risk creating a god-module that swallows errors?

Do NOT propose interfaces yet. Ask the user: "Which of these would you like to explore?"

### 5. User picks a candidate

### 6. Frame the problem space

Before spawning sub-agents, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would need to rely on
- A rough illustrative code sketch to make the constraints concrete - this is not a proposal, just a way to ground the constraints
- **Data structure fitness** (Knuth, TAOCP Vol 1 Ch 2, Vol 3): Is the internal data structure appropriate for the access patterns? Would deepening enable a fundamentally better data structure that the shallow decomposition prevents? Example: two modules each maintaining sorted arrays that could be one balanced tree. The deepened module can choose the optimal structure because it owns the full access pattern.
- **Algorithm complexity**: For the candidate cluster, identify the dominant algorithm. What is its time/space complexity? Does the current decomposition force suboptimal complexity (e.g., O(n^2) because data is split across modules that redundantly traverse shared data)?

Show this to the user, then immediately proceed to Step 7. The user reads and thinks about the problem while the sub-agents work in parallel.

### 7. Design multiple interfaces

Spawn 3+ sub-agents in parallel using the Agent tool. Each must produce a **radically different** interface for the deepened module.

Prompt each sub-agent with a separate technical brief (file paths, coupling details, dependency category, what's being hidden). This brief is independent of the user-facing explanation in Step 6. Give each agent a different design constraint:

- Agent 1: "Minimize the interface - aim for 1-3 entry points max"
- Agent 2: "Maximize flexibility - support many use cases and extension"
- Agent 3: "Optimize for the most common caller - make the default case trivial"
- Agent 4 (if applicable): "Design around the ports & adapters pattern for cross-boundary dependencies"

Each sub-agent outputs:

1. Interface signature (types, methods, params)
2. Usage example showing how callers use it
3. What complexity it hides internally
4. Dependency strategy (how deps are handled - see [REFERENCE.md](REFERENCE.md))
5. Trade-offs
6. **Data structure recommendation**: What internal representation does this interface enable that the current split prevents? (Knuth: the right data structure makes the algorithm obvious.)
7. **Fundamental operation count**: For the most common caller, count the number of concepts (types, methods, parameters) they must understand to use this interface. (Knuth, TAOCP Vol 1, Ch 1.3: count fundamental operations to compare alternatives objectively.)

Present designs sequentially, then compare them in prose.

**Comparison criteria** (in priority order):
1. Fundamental operation count for the common caller - fewer concepts wins by default
2. Data structure fitness - does the interface enable the optimal internal representation?
3. Hot path impact - if the candidate is in the critical 3%, latency cost of indirection matters
4. Flexibility for uncommon callers
5. Migration cost from current code

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated - the user wants a strong read, not just a menu.

### 8. User picks an interface (or accepts recommendation)

### 9. Create GitHub issue

Create a refactor RFC as a GitHub issue using `gh issue create`. Use the template in [REFERENCE.md](REFERENCE.md). Do NOT ask the user to review before creating - just create it and share the URL.
