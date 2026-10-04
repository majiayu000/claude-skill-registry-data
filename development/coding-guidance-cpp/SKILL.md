---
name: coding-guidance-cpp
description: C++ implementation and review guidance for modern ownership, type safety, API design, and tests; use `coding-guidance-qt` when QObject lifetime, signals and slots, QWidget/model-view behavior, Qt threading, or Qt build tooling is the main concern. Portable across C++17/20/23 repositories and build systems.
---

# C++ Coding Guidance

This skill adds portable C++ implementation, refactoring, and review guidance.

## Adjacent Skills

This skill provides portable C++ engineering principles. Compose with:

- **Workflow:** **thinking** (ambiguous decision framing),
  **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **backend-guidance** (server-side code),
  **backend-systems-guidance** (stronger backend architecture, reliability, and
  trust-boundary work),
  **ui-guidance** (graphical UI/web frontend),
  **project-core-dev** (repo-specific completion discovery and reporting when
  needed)
- **Qt specialization:** **coding-guidance-qt** when Qt object lifetime,
  eventing, widgets, models, thread affinity, or generated build steps dominate

## When Not to Lean on This Skill

- non-C++ work
- legacy or bare-metal environments where modern C++ guidance must be adapted
  selectively
- pure architecture or process work with no C++ design or code judgment needed
- repo-specific style packs or platform policies that should be enforced by
  local `clang-tidy`, compiler, or overlay rules rather than a portable
  principle skill

## Boundary Contract

Keep this skill focused on portable C++ engineering judgment.

- Put repo-specific exception policy, warning policy, formatter choices, and
  include-order rules in repo config or repo docs
- Put style-pack rules from ecosystems such as Google, LLVM, Abseil, or
  platform/vendor bundles in repo config or overlays, not here
- Put library- or platform-specific API policy in repo config or a domain
  overlay
- When a rule is analyzer-shaped but not portable, keep it in `clang-tidy`
  config or the reference note rather than adding it to the main skill

## Implementation Workflow

1. Read the touched code, build shape, existing tests, and any nearby docs or
   shorthand notes before editing.
2. If the request is partially specified, infer the intended behavior from the
   existing code and tests. Ask only when multiple plausible C++ designs would
   change semantics.
3. Choose the narrowest change that solves the problem without hiding ownership,
   lifetime, or error-handling contracts.
4. Implement with simple, strongly typed interfaces and modern C++ defaults.
5. Add or update tests close to the changed behavior.
6. Run the narrowest relevant format, build, test, sanitizer, and analyzer
   targets the repo supports.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current behavior, invariants, side effects, and risky hotspots.
2. Break the refactor into small slices that preserve behavior.
3. Remove duplication, long functions, or muddled responsibilities one step at
   a time.
4. Keep tests passing after each slice; add characterization coverage first when
   behavior is unclear.
5. Stop when the code is simpler and safer.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize bugs and regressions, ownership and lifetime errors, exception or
   error-path holes, thread-safety issues, security risks, performance mistakes
   with real impact, and missing tests.
4. State findings with concrete evidence and the likely consequence.

Do not edit code or require findings to be fixed unless the user also asks for
remediation.

## C++ Rules

Keep the critical portable defaults in view:

- Make ownership explicit. Prefer values and RAII, use `std::unique_ptr` for
  sole ownership, and treat raw pointers and references as non-owning unless an
  explicit legacy or C API transfers ownership; adopt such results into the
  matching RAII owner promptly.
- Establish invariants during construction and prefer rule-of-zero types.
- Do not let references, views, iterators, pointers, or other borrowed state
  outlive their owners, especially across callbacks, coroutines, or threads.
- Prevent unchecked bounds access, silent narrowing, signed/unsigned mistakes,
  and representation operations that violate aliasing or lifetime rules.
- Keep error handling consistent within a path, preserve must-check failures,
  and use `[[nodiscard]]` when ignoring a result is likely a bug.
- Encode ownership, units, nullability, and easily confused argument semantics
  in types or named parameter objects when call sites would otherwise be
  ambiguous.
- Keep headers free of namespace pollution, hidden global initialization,
  fragile macros, and accidental transitive-include dependencies.
- Prefer structured thread ownership, explicit cancellation, and test seams
  over detached work or ambient process state.
- Use modern vocabulary types and library features only when the repository's
  C++ target supports them and they make the contract clearer.

Read [references/cpp-core-rules.md](references/cpp-core-rules.md) when the task
needs the detailed ownership, type-safety, API, header, concurrency, or modern
C++ checklist.

### Advanced design judgment

Load
[references/cpp-advanced-design-judgment.md](references/cpp-advanced-design-judgment.md)
when the task involves public APIs, error-model choices, advanced language
features, template-heavy interfaces, headers with broad rebuild impact,
coroutines, synchronization strategy, ABI/plugin/C interop boundaries, or
abstraction design. Keep ordinary feature work in the default rules above.

## Resource map

- [references/cpp-core-rules.md](references/cpp-core-rules.md): detailed
  portable rules for ownership, bounds and representation safety, API clarity,
  headers, concurrency, and modern vocabulary types
- [references/clang-tidy-derived-guidance.md](references/clang-tidy-derived-guidance.md):
  read when analyzer findings, enabled check families, or portable versus
  repo-specific static-analysis policy is part of the task
- [references/cpp-advanced-design-judgment.md](references/cpp-advanced-design-judgment.md):
  deeper guidance for public API design, error models, advanced features,
  headers, synchronization, and abstraction choices

## Decision Heuristics

Use these when the right choice is not obvious:

- **Scope check:** if a change crosses several public interfaces or compatibility
  boundaries, stop and plan the contract changes before continuing.
- **Ownership clarity:** if ownership is not obvious from the type signature,
  redesign the interface or add a one-line contract comment.
- **Error-model consistency:** do not mix exceptions, error codes, and
  `expected`-style returns within one subsystem unless the boundary is explicit.
- **Exception-safety pressure:** when mutating multi-step state, decide whether
  the operation offers no-fail, strong, or basic exception safety and structure
  the code to match.
- **Repo conventions:** if the repo has established rules for exceptions,
  containers, ownership types, or naming, follow them unless they create a
  correctness or safety problem.
- **Feature pressure:** do not introduce concepts, ranges, coroutines, or
  metaprogramming unless they make the code simpler for this repo's likely
  maintainers.
- **Interface pressure:** if a header starts dragging in broad dependencies or
  exposing implementation detail, narrow the interface before adding more code.
- **Build-surface pressure:** if a design pushes more logic, templates, or
  dependencies into public headers, justify the compile-time and rebuild cost.
- **Parameter pressure:** when adjacent parameters have the same type or call
  sites cannot communicate argument meaning clearly, prefer named types or a
  cohesive parameter object.
- **Lifetime pressure:** if a non-owning type crosses async, callback, return,
  or storage boundaries, prefer an owning type unless the lifetime proof is
  obvious from the interface.
- **Initialization pressure:** if correct behavior depends on a later
  “remember to initialize” step, move that requirement into construction or the
  type itself.
- **Call-site pressure:** if two arguments are easy to swap or a call needs
  comments to explain literals, redesign the API before adding more call sites.
- **Header pressure:** if a header starts accumulating definitions, globals,
  unnecessary includes, or hidden initialization, push behavior back behind a
  source boundary.
- **Testability pressure:** if a design forces tests to spin threads, sleep,
  touch the real filesystem, or patch globals just to exercise core logic,
  introduce a seam before adding more behavior.
- **Test setup pressure:** extract a fixture when repeated setup or incidental
  detail obscures the behavior under test; keep one-off setup local when it is
  clearer there.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or safety, prefer
  correctness. When it conflicts with style alone, prefer narrowness unless the
  task is explicitly a cleanup.
- **Adjacent issues:** do not modify unrelated issues unless they are required
  for the requested change's correctness or safety; report them separately.
- **Abstraction threshold:** three similar code blocks or repeated API-shaping
  pain is a pattern; before extracting, check whether a free function, helper
  type, or composed object is the simpler move.
- **Performance rule:** optimize only after measurement, except for obvious
  ownership, allocation, or algorithmic mistakes on hot paths.
- **UB-sensitive optimization:** treat optimizations that rely on subtle
  lifetime, aliasing, or memory-order assumptions as high-risk until proven by
  evidence and tooling.

## Validation

For implementation, a change is done when:

- the code compiles without new warnings, unless the repo explicitly treats a
  known warning set as baseline debt outside the change
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- the repo's formatter has been run
- configured static analyzers report no new findings
- available sanitizers are clean for the touched paths when the change affects
  memory safety, threading, or undefined-behavior risk
- performance-sensitive changes are measured instead of justified by intuition

For review, completion means `Critical` and `Important` findings are reported
with concrete evidence, likely consequence, and any validation gap. Unfixed
findings do not make the review incomplete.
