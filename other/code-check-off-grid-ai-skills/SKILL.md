---
name: code-check
description: Hold every change to one engineering standard and get a pass or fail with evidence before it merges. SETUP installs quality gates in a repo, PLAN designs a task against the bar (separation of concerns, SOLID, DRY, tests), AUDIT reviews a diff dimension by dimension. Use when you say "audit this diff", "is this ready to merge", "/code-check", "plan this subsystem", or "set up quality gates". Not for small fixes.
---

# Check code before merge

Three modes. **SETUP** once in a fresh repo. **PLAN** at the start of a task. **AUDIT** before a PR (the default when a diff already exists). Find out which repo and stack you are in first: the gates differ per repo (see Mechanical gates). If the repo is one of several apps that share code (web, mobile, desktop, a shared package, a server), note which one, because the "One seam across platforms" rules depend on it.

Don't load this for a small fix: apply the principles from the repo's agent instructions (`CLAUDE.md`, `AGENTS.md`, `.cursor/rules` or the equivalent) directly. Load it to design a genuinely new subsystem or to audit a real PR.

---

## SETUP

For a JavaScript or TypeScript repo: `bash <this skill's folder>/setup/bootstrap.sh` from the repo root. It is idempotent and backs up any edited config to `<file>.hygiene.bak`. It detects the stack (web, React Native, plain TS library) and installs prettier, typed eslint, dependency-cruiser, jscpd, knip and c8, the tsconfig flags, and the pre-push hook. Pre-push runs the fast subset; CI runs the full set. A repo with a backlog starts noisy rules at a baseline and ratchets toward `error` and zero: never loosen a gate to excuse a new problem. Details and the per-repo tuning you still do by hand: `setup/README.md`.

For other stacks (Python, Go, Swift, Kotlin, Rust), set up the same gates by hand with the stack's own tools: a formatter, a typed linter, a dependency or import-boundary check, a copy-paste detector, a dead-code finder, a coverage bar on pure logic, a pre-push hook, and a CI workflow that runs everything.

## PLAN: answer briefly, in the response

1. **Three questions.** Enough to abstract? (2+ concrete cases through one caller is a seam; one case is not: YAGNI.) Does SOLID apply? (What owns the one responsibility; what interface callers depend on.) Is it reused? (The single source of truth.)
2. **Separation of concerns.** Name the owning **service** (state machine, resources, side effects), the **pure logic** to isolate (no I/O), the **thin handlers** (I/O only), the **presentation** (no logic, no state). Where is the seam, and what gets injected?
3. **DRY, and which package owns it.** The rule, map, constant or type defined once, and every place that must use it. If it is true on more than one platform, name the shared package that owns it and the ports each host injects. Then state what the second host has to write: it must be wiring only, never logic.
4. **Tests.** The corner-case integration scenarios FIRST: the real user flow through the real seam in its hard states (empty, first, boundary, the false branch of each gate, concurrency and ordering, the error path, the device or memory-pressure case). Name the end result each one asserts (rendered text, saved row, file on disk), and the BEFORE state it asserts so the after-assertion can't pass as a no-op. Green on working code is the bar: no red-first, and source code is never broken to show a test can fail.
5. **Design and brand**, if there is UI: which tokens, which approved component library; read the project's design doc.
6. **Reuse.** What already exists that this extends rather than rebuilds.

## AUDIT: for each dimension, PASS / FAIL / N/A with evidence (file:line, command output)

1. **Mechanical gates.** Run them and paste the results: format, lint, type check, the change's tests, coverage against the repo's bar, and a production build if native code, dependencies, config or imports changed.
2. **Separation of concerns.** Logic in the owning service, handlers thin, pure logic isolated, presentation free of state. Flag any view or hook doing retry, cancel, orchestration or "compute the real value". Any new local state that can be derived, mirrors the store, is synced by an effect, or is read by siblings that shouldn't share it?
3. **SOLID.** Any `kind ===`, `instanceof` or platform check used to choose a mechanism in a caller? Would a new implementation need caller changes? A patch layered on shared state instead of the owning seam?
4. **SSOT / DRY.** Any rule or constant defined twice (for example in a server and a client, or a main and a renderer process)? For each fact the diff touches: who owns it, and is anything else entitled to answer the same question?
5. **One seam across platforms.** Does any cross-platform rule live in a host instead of the shared package? Could the next platform be brought up with wiring alone, or would it restate this logic? Is the injected surface small and total, or can a host half-wire it? Is a capability gap reported as data, or branched on with a platform check?
6. **Tests.** Real integration through the real seams; assert the end result, never `toHaveBeenCalled`; no mocks of the project's own code; each assertion depends on the implementation actually running (read it; don't break source to check).
7. **Design and copy**, if touched: tokens, not hardcoded values; the brand's voice.
8. **Branch, PR, honesty.** Off the main branch, one concern, status reported as code / wired / verified, what is unverified named, gaps logged.

End with an overall verdict and a list of blocking issues.

---

# Standards (the why)

**Separation of concerns.** Isolate pure logic (no I/O, unit-testable) from I/O (thin adapters behind an interface). One owning service per resource or subsystem owns the state machine and the side effects; everything else reads its projection and sends intents. Presentation holds nothing: no authoritative state, no business logic, no store orchestration, no "compute the real value from several sources". If a hook is doing the work, that IS the bug: move it to the service. Reactive stores are a read-only projection, not a coordination bus: never fire a side effect off a store snapshot that several writers change.

**Avoid local state.** Reach for local component state last, not first. Default to deriving from the service's projection: anything computable from what you already render is not state. Local state is right only for passing view state the user is in the middle of (which sheet is open, an uncommitted draft field, a focus ring), and even then it lives in the component that owns that interaction, not on the screen above it. Tells it is wrong: state duplicating something the store or service already knows; state kept in sync with a prop by an effect; one field on a screen that several rows read, so typing in it changes unrelated rows; a boolean that could be `derived === value`. Two pieces of state that must move together are one piece of state in the wrong place.

**SOLID.** Depend on interfaces, not concrete types (DIP). The tell: `kind === 'x'`, `instanceof`, `engineId ===`, or a platform check used to choose a mechanism in a caller, especially in UI code. Push the decision behind the abstraction so adding an implementation needs zero caller changes (OCP). SRP: one responsibility. LSP: any implementation can stand in through the interface; turn capability gaps into data inside the service, not branches in the UI. ISP: don't force an implementation to stub methods it can't support. **Fix the seam, never patch around it:** if a fix would add a second concrete branch in a caller, build or extend the owning service instead. Migrations don't change behaviour (they are additive; check each migrated path behaves as before, then layer the fix on top).

**SSOT / DRY.** Every fact has exactly ONE owner, and a rule, map, capability check, constant or type is defined ONCE and imported everywhere. DRY is about duplicated code; SSOT is about duplicated *authority*: two places entitled to answer the same question will drift, and the second one is the bug even when its code is different. Ask of any fact: who owns it? Identity, membership, capacity and entitlement each have one owner; a cache or a projection is never an owner. A second generator of an id, a store that mints what a provider already owns, a UI that recomputes what a service decided: all SSOT breaches. Collapse to the owner and have everything else read its projection. Tests import that source; they never hardcode the value again.

**One seam, in the shared package, with hosts as ports.** Anything true on more than one platform (a lifecycle, an ordering rule, a gate, a policy, a taxonomy, a state machine) is defined ONCE in the shared package, and each host supplies only what really differs: its transport, its storage, its clock, its way of drawing. The shared package is the executable specification; a host is adapters. **The test: adding the second platform must need NO logic, only wiring.** If bringing up desktop means restating what mobile already decided, the seam is in the wrong place, and the two will drift the moment one of them fixes an edge case (the first platform gets the fix, the others keep the bug). Tells: a service in an app that owns rules rather than plumbing; the same lifecycle written twice with different variable names; a shared package that exports only primitives while each host wires them up its own way (primitives without an orchestrator push the real decisions back into the hosts, which is duplication wearing a library costume). Keep the injected surface small and total: prefer ONE input a host feeds from a state subscription over a set of `begin` / `update` / `end` calls it has to remember at every call site. A seam that can be half-wired eventually will be. Where a host cannot do something, it reports that as **capability data** the shared logic reads, never as a platform branch.

**Testing.** One rendered integration test per fix: mount the real screen, arrive through real gestures, run the whole real stack over fakes ONLY at the device or network boundary, and assert what the user SEES. Use fakes (in-memory implementations that behave like the real thing), not mocks (canned returns plus call assertions). Never mock the project's own code. Never assert `toHaveBeenCalled`: assert the end result. The delete test, answered by READING the test: if deleting the implementation would keep it green, it is asserting the mock. Tests are written green against working code; never break, revert or neutralise source to prove one can fail. If writing a test uncovers a real product bug, report it with the evidence and let the human decide: don't fix it in the testing pass and don't bend the test around it. One-liners: unit tests mock what you don't own; integration tests mock only what is outside your system; end-to-end tests mock only timers. Follow the repo's own rules on unit tests and coverage. Run only the fix's own test file while iterating; the full suite runs at pre-push.

**Design (if UI).** One source of truth: the project's design doc or design system (find it; if there is none, ask before inventing one). All color, spacing and type come from tokens, never hardcoded. One icon set per platform. Hierarchy comes from size and weight, not color. Reuse before building: two surfaces of the same thing use the same component.

**Copy (if strings).** One source: the project's brand or voice guide. Outcomes, not features; speak to "you"; proof first (a number, not "fast"). Unless the brand guide says otherwise: no em dashes, no exclamation marks, no curly quotes, and none of the empty words (revolutionary, seamless, empower, leverage, robust, comprehensive, crucial, delve, showcase, enhance).

**Branch, PR, honesty.** Never commit to the main branch: branch first. Follow the repo's merge style. One concern per PR. Optional or paid features live behind their own module and flag, wired through registries, not scattered checks. Platform parity: one typed contract per native capability, met by every platform's code; real gaps modelled as capability data, not an `if (ios)` branch. **Read the logs, don't guess:** pull the app's or device's own log for the session and search it before you claim a cause. Report status as **code / wired / verified**, name what is unverified, and log gaps in the project's backlog.

**Mechanical gates per stack.** Find the repo's own commands first (its `package.json` scripts, `Makefile`, CI workflow). Typical sets: React Native: formatter, eslint, `tsc --noEmit`, jest on the fix's file (full suite at pre-push). Web or Electron: type check (every tsconfig), the unit runner, the coverage ratchet, Playwright. Server: type check, tests, coverage, build, a smoke test. Libraries: build. Build before deploy whenever native code, dependencies, config or imports changed: type checks and tests don't catch build errors.

---

# Evolving this standard

`safe-to-merge` ends with `never-twice`, which folds *generic* review lessons into the right section above and logs each in `LEDGER.md`. Keep this file lean: tighten and merge rules, never bloat.
