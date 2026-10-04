---
name: coding-guidance-qt
description: Qt C++ implementation and review guidance for QObject, QWidget/model-view, signals and slots, thread affinity, `.ui` forms, and Qt build tooling; use `coding-guidance-cpp` for non-Qt C++ design. Portable across Qt5/Qt6 repositories with a QWidget desktop focus.
---

# Qt Coding Guidance

This skill adds portable Qt implementation, refactoring, and review guidance
for Qt C++ code with a QWidget desktop focus. Widget, dialog, model/view,
Designer, and desktop-UX guidance here is specific to Widgets work; broader
QObject, threading, and build guidance also applies to non-UI Qt C++ code.

## Adjacent Skills

This skill provides portable Qt engineering principles. Compose with:

- **Workflow:** **thinking** (ambiguous decision framing),
  **recursive-thinking** (stress-testing),
  **security** (threat modeling)
- **Domain overlays:** **ui-guidance** (ordinary graphical UI work),
  **ui-design-guidance** (stronger design and UX work),
  **project-core-dev** (repo-specific completion discovery and reporting when
  needed),
  **project-platform-diagnose** (environment-sensitive diagnosis)

Use this as the default principle skill for Qt code. Reach for
**coding-guidance-cpp** only when the task is mostly non-Qt C++ or needs deeper
general C++ design judgment than Qt-specific guidance.

## Quick Routing

Open bundled references only when the task actually needs them:

- [references/qt-build-compatibility.md](references/qt-build-compatibility.md)
  for CMake, generated-code, or Qt5/Qt6 compatibility work
- [references/qt-debugging-checklist.md](references/qt-debugging-checklist.md)
  for diagnosis-heavy tasks
- [references/qt-designer-ui-files.md](references/qt-designer-ui-files.md)
  for `.ui` files, Qt Widgets Designer, `uic`, or generated `ui_*.h` code
- [references/qt-layouts-and-desktop-ux.md](references/qt-layouts-and-desktop-ux.md)
  for layout, dialog, panel, and desktop-UX work
- [references/qt-model-view-checklist.md](references/qt-model-view-checklist.md)
  for `QAbstractItemModel`, roles, resets, selections, and model/view contract work
- [references/qt-review-evidence.md](references/qt-review-evidence.md) for
  Qt-specific review hotspots and the evidence needed to support findings

Stay in the main skill when the task is broad Qt implementation or review and
no single failure mode dominates yet.

## When Not to Lean on This Skill

- non-Qt work
- pure backend or library code written in C++ that does not use Qt types,
  eventing, object lifetime, or Qt build tooling
- Qt Quick or QML-first work; use only the QObject, threading, and build
  guidance here when it genuinely applies, and rely on a QML/Qt Quick-specific
  skill or repo guidance for declarative UI architecture, bindings, and scene
  graph concerns
- design-only work where no Qt API, object model, build, or code judgment is
  needed

## Implementation Workflow

1. Read the touched widgets, models, controllers, dialogs, `.ui` forms, tests,
   and build files before editing.
2. Infer intended behavior from current signals and slots, ownership, thread
   affinity, layouts, and tests when the request is partially specified. Ask
   only when multiple plausible Qt designs would change semantics.
3. Choose the narrowest change that keeps QObject ownership, event ordering,
   layout behavior, model contracts, and UI-thread rules explicit.
4. Implement with one clear application bootstrap, small widget responsibilities,
   modern typed `connect` usage, minimal GUI-thread work, and narrow seams
   between widgets and domain logic.
5. Add meaningful deterministic checks for the changed behavior using the repo's
   existing test framework. Qt Test and `QSignalSpy` fit Qt signal and model
   contracts; preserve the existing framework for plain C++ logic. Do not add
   or migrate a framework merely to follow a portable preference.
6. Run the narrowest relevant formatter, build, test, and affected-platform
   smoke path the repo supports. If the change touches Qt5/Qt6 compatibility,
   validate each supported build variant.

## Refactoring Workflow

Use this instead of the default implementation workflow when the task is
primarily cleanup or restructuring:

1. Capture current ownership, signal flow, event-loop assumptions, thread
   affinity, layout behavior, and model or binding contracts.
2. Break the refactor into small slices that preserve visible behavior.
3. Remove long widget constructors, tangled signal chains, view-model leakage,
   duplicated object wiring, and layout hacks one step at a time.
4. Keep tests or smoke paths passing after each slice; add characterization
   coverage first when behavior is unclear.
5. Stop when the code is simpler, safer around lifetime and threading, and
   easier to reason about.

## Review Workflow

When reviewing (not implementing), skip the implementation workflow and use this
instead:

1. Read the change in full before commenting.
2. Identify findings, ordered by severity: `Critical` > `Important` >
   `Suggestion`.
3. Prioritize ownership and deletion bugs, cross-thread QObject misuse,
   connection lifetime mistakes, GUI-thread blocking, model/view contract
   violations, layout breakage, Qt5/Qt6 build regressions, resource-path and
   platform assumptions, and missing tests.
4. State findings with concrete evidence and the likely consequence.
5. For Qt-specific claims, name the proof: sender/receiver types and lifetimes
   for signal issues, thread affinity for cross-thread issues, begin/end and
   reset boundaries for model issues, and the visible interaction path for
   layout or `.ui` regressions.

Do not edit code or require findings to be fixed unless the user also asks for
remediation.

## Qt Rules

### First tier - causes bugs

- These rules apply to Qt C++ broadly; Widget-specific rules appear in later
  sections.
- Treat `QObject` ownership, parent-child lifetime, and thread affinity as core
  contracts, not cleanup details
- Every Widgets application gets exactly one `QApplication`; create it before
  any widget, `QPixmap`, `QIcon`, or other GUI object
- Do not copy `QObject` subclasses; keep lifetime and ownership explicit
- Use `deleteLater()` when direct deletion could occur during event handling,
  from the wrong thread, or before queued work is safely drained. Direct
  destruction is appropriate when ownership, thread affinity, and event-loop
  state make it safe. Verify that the owning event loop will actually process a
  deferred deletion.
- Do not touch GUI objects from non-GUI threads
- Bind connection lifetime to a context object when possible so queued work does
  not outlive the receiver
- Prefer the typed `connect` syntax over string-based `SIGNAL` and `SLOT`
  macros unless the repo is constrained by old APIs
- Do not block the GUI thread with filesystem, network, database, or heavy CPU
  work
- When model data changes, emit the correct notifications and bracket
  structural changes with the correct begin/end calls
- Do not hand-place widgets with `setGeometry()` when a real layout should own
  sizing and positioning

### Second tier - prevents mistakes

- Keep widgets, models, delegates, dialogs, and business logic separated
  enough to test behavior without full UI setup
- Prefer explicit ownership and small helper objects over hidden globals or
  wide controller classes
- Keep slot bodies short; move non-trivial work into named helpers, presenters,
  or model logic
- Prefer Qt containers, strings, and utilities where the repo already uses
  them; do not introduce needless conversions at every boundary
- Follow the repo's Qt version and idioms before introducing newer Qt APIs
- Introduce no new compiler, clazy, or Qt-specific warnings; keep existing debt
  outside the change separate from regressions

### Ownership, eventing, and threads

- Parent a QObject only when the parent truly owns it for the same lifetime.
  A stack child is valid when its lifetime ends before its parent, as when the
  parent is constructed first in the same scope. Reject destruction orders
  that let a parent delete a still-live stack child. Do not add a second owning
  smart pointer to an object already owned by a QObject parent.
- Use `QPointer` or a clearer ownership seam when a non-owning QObject reference
  can be invalidated by queued work or callbacks.
- Tie lambda connections to a context object unless every capture demonstrably
  outlives the connection.
- Treat signals as contracts. Keep connection types, reentrancy, thread hops,
  recursive updates, and signal-chain length explicit when they affect behavior.
- Do not create children for a parent in another thread or move an object while
  its ownership, children, or event handling make the move invalid.
- Own cancellation and teardown for timers, workers, asynchronous replies, and
  queued callbacks, including application quit and window-close paths.

### UI, model, build, and test boundaries

- Keep domain rules in plain C++ where practical, translate through Qt-facing
  models or adapters, and keep widgets focused on presentation and local
  interaction.
- Treat item-model indexes, roles, begin/end notifications, resets, selections,
  and persistent indexes as formal compatibility contracts. Load the model/view
  reference for contract-heavy work.
- Let layouts own geometry and keep accessibility, keyboard flow, size policy,
  margins, and platform-native widget semantics deliberate. Load the layout
  reference for detailed desktop-UX work.
- Treat moc, uic, qrc, `.ui` files, resources, translations, and claimed Qt5 or
  Qt6 variants as source and build contracts. Never edit generated `ui_*.h`
  files; load the Designer and build references when those seams change.
- Test visible behavior, model transitions, emitted signals, and lifecycle
  edges. Prefer deterministic Qt Test or offscreen checks, and use the debugging
  reference plus sanitizers for diagnosis rather than guessing.

The Quick Routing references contain the detailed model/view, layout, Designer,
build, review, and diagnosis checklists. Load only the reference matching the
dominant failure mode.

## Decision Heuristics

Use these when the right choice is not obvious:

- **Lifetime pressure:** if it is not obvious who owns a QObject or when it can
  die, redesign the boundary before adding more behavior.
- **Thread-affinity pressure:** if a callback, timer, or reply may arrive on a
  different thread, make that hop explicit and local.
- **Model-contract pressure:** if a change touches model indexes, role names,
  or reset behavior, treat it as a compatibility boundary rather than a local
  cleanup.
- **Layout pressure:** if you are about to use manual geometry, spacer hacks, or
  magic sizes, stop and check whether the right layout type, size policy, or
  stretch factor would solve it cleanly.
- **Build-compatibility pressure:** if a repo claims both Qt5 and Qt6 support,
  do not hard-code one target family or test only one build.
- **Architecture pressure:** if widget code starts owning business rules,
  persistence, and orchestration together, introduce a presenter/controller seam
  before adding more slots.
- **UI responsiveness:** if the feature can stall input, painting, or startup,
  rethink the design before polishing the code.
- **Repo conventions:** if the repo has established patterns for ownership,
  signals and slots, widgets vs. QML, testing, or Qt version support, follow
  them unless they create a correctness problem.
- **Narrowness vs. quality:** implement the narrowest change that solves the
  problem. When narrowness conflicts with correctness or lifecycle safety,
  prefer correctness. When it conflicts with style alone, prefer narrowness
  unless the task is explicitly a cleanup.
- **Adjacent issues:** do not modify unrelated issues unless they are required
  for the requested change's correctness or lifecycle safety; report them
  separately.
- **Abstraction threshold:** three similar widget handlers, signal-wiring paths,
  model-shaping steps, or dialog flows is a pattern; before extracting, check
  whether a small helper, adapter, presenter, or model object is the simpler
  move.
- **Qt vs. plain C++:** if logic does not need the event loop, QObject
  identity, or Qt containers, keep it as plain testable C++ instead of forcing
  Qt into the core domain.

## Validation

For implementation, a change is done when:

- the code builds without new compiler, moc, or Qt-specific warnings
- existing tests pass
- new or changed behavior has test coverage, or the lack of coverage is called
  out with a concrete reason
- changed signal, layout, model, or thread-hop behavior has a deterministic
  validation path
- UI-facing changes have at least a narrow smoke path on the affected platform
- Qt5/Qt6 compatibility changes were validated on each claimed build variant
- resource paths, generated-code inputs, and translation-sensitive changes were
  verified when touched

For review, completion means `Critical` and `Important` findings are reported
with concrete Qt-specific evidence, likely consequence, and any validation
gap. Unfixed findings do not make the review incomplete.
