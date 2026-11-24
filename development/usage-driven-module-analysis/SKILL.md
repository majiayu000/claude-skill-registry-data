---
name: usage-driven-module-analysis
description: Analyse the design of a framework module, using its callers (samples, applications, tests) only as evidence of how the API is used, and report API gaps, misuse risks, duplication, and simplification opportunities. Findings are about changing the module, never the callers. Use when the user asks to review or redesign a module from its usage.
---

# Usage-driven module analysis Skill

Read `docs_llm/LLM_GUIDE.md` first.

## Goal
Make the module deep: a small, simple public API that hides a lot of functionality. The module exposes only the API callers really need and handles as much as possible internally (initialisation order, state, buffers, locking, error recovery, cleanup). Judge every finding by this goal. Prefer suggestions that shrink the public API or remove work from the caller, and avoid suggestions that add API or push more responsibility to the caller.

## Most important rules
- The subject is the module, not its callers. Never report a finding that says "fix the sample/application". Callers are evidence only. When a caller misuses the API, makes a mistake, or repeats boilerplate, ask what in the module's API invited it and report how to change the API so the mistake is hard or impossible to make (fewer steps, safer defaults, checks inside the module, hidden state, a type that cannot be misused). Bugs that exist only in caller code, with no link to the API design, are not findings; at most mention them in one line under the report as "caller issues, out of scope".
- Analysis only. Never change the module, its header or its comments; report findings instead.
- Base every finding on evidence: a file and line of a real call site, test or example. For "never used" findings, the evidence is the grep command and its zero-hit result. Do not invent usages.
- Follow `AGENTS.md`: use only the public API in `inc/<layer>/<module>/`; do not invent APIs.

## Inputs
- Module name or header path, normally `inc/<layer>/<module>/ez_<module>.h`.
- The sample code or application where the module is used. If none is given, search `src/`, `tests/`, `examples/` and any sample or application folders. If you find no call sites at all, stop and ask the human.
- Optional: detail requests or questions to focus on.

## Steps
1. Read the module header, normally `inc/<layer>/<module>/ez_<module>.h`. List every public function, type and macro, and the documented contract (preconditions, return values, ISR safety).
2. Read the corresponding API cheat sheet in `docs_llm/api/`.
3. Find all usages: grep every public symbol in the given sample or application paths (or the default scope from "Inputs"). Record file:line for each hit.
4. Read the calling code and extract the usage patterns (call order, arguments, handling of return values).
5. Build the API overview: for each public symbol, the call sites and notes.
6. Compare the usage patterns with the contract from steps 1 and 2.
7. Identify findings (see "What to look for") and give each a severity (see "Output").
8. Print the report.

## What to look for
Each item is a signal that the module is shallow. For every finding, suggest how to change the module (move the work or data into it, remove or merge API), never how to change the caller.
- Public functions that are never used, or used only in tests: candidates to make internal or remove.
- Call sequences repeated in many places that could be a single API, or be done inside the module.
- Many small functions that callers always call together: candidates to merge into one.
- Parameters or options that every caller sets to the same value: candidates for an internal default.
- Documented behaviour that differs from how callers rely on it.
- Misuse: callers use the API against its documented intent, e.g. wrong call order, ignored return values (AGENTS.md rule 4), non-ISR-safe calls from an ISR (rule 2). Treat each as a design signal: the suggestion must be an API change (merge steps, make the module enforce order, make the failure impossible or loud), not "the caller should do X".
- Unnecessary exposure of internal data (struct fields, handles, types) that callers should not touch (rule 5).
- API calls that the module should handle internally instead of the caller, e.g. required init or cleanup steps, lifecycle and order assumptions.

## Output
Print the report as markdown. Severity scale: High = bug or misuse risk, Medium = API design problem, Low = cleanup. Use this structure:

```
# Usage analysis: <module>

## Summary
<3-5 lines: what the module is used for, the main conclusions, and how deep the module is today (API size versus what it hides)>

## Public API overview
| Symbol | Call sites | Notes |
|--------|-----------|-------|

## Usage patterns
### <Pattern name>
- Where: <file:line>, <file:line>
- Sequence: <call order>
- Remarks: <...>

## Findings
| # | Severity | Finding | Evidence (file:line) | Suggestion (change to the module) |
|---|----------|---------|----------------------|------------|

## Open questions
- <things the human must decide>
```

## Report
Do not add a section that reviews the sample or application code. After the report, tell the human: the module analysed, the number of call sites found, and the top findings by severity. State clearly anything you could not determine.
