---
name: code-probe
description: Prepare minimal, disposable harnesses to run a selected code path in isolation, investigate suspected behavior, or hand off a ready-to-debug entry point in VS Code. Use for focused code probing without launching an entire application; adapt to the project's language, tooling, and test conventions.
---

# Code Probe

Isolate one selected code path with the least scaffolding needed for useful investigation. Prefer existing project interfaces and tooling over new infrastructure. Generated harnesses are disposable, not additions to the permanent test suite.

## Mode selection

- **Auto-probe (default):** The user wants a behavior investigated, an observation collected, or a hypothesis checked. Prepare a harness, execute it, and report evidence.
- **Debugger handoff:** The user explicitly asks for `handoff`, `manual debug`, or equivalent interactive-debugging preparation. Prepare a repeatable debug entry point and IDE launch configuration; leave behavioral execution to the user.
- Run **Shared preparation** for either mode, then follow only its selected mode section. Do not interpret handoff as an instruction to run auto-probe first unless the user explicitly requests both.

## 1. Shared preparation

### 1.1 Resolve target and scope

- Locate the function or code path using available repository context; disambiguate only when necessary.
- Establish the requested path, inputs, suspected behavior (if any), and expected observation. Infer a representative scenario when unspecified; label assumptions.
- Limit the probe to the smallest relevant execution boundary. Do not start the whole application when the target can run independently.

### 1.2 Inspect the environment

- Inspect imports, call sites, arguments, side effects, existing tests/fixtures, runtime setup, and project scripts or configuration.
- Reuse existing test seams, fakes, dependency-injection points, interpreters, loaders, and debug adapters.
- Identify destructive operations and external calls before deciding what to execute or simulate. Include package-script hooks and automatic dependency setup in this inspection; a run/test command may trigger an installation.

### 1.3 Select the execution harness

Choose the least complex viable combination; these are options, **not a mandatory escalation sequence**:

1. **Direct invocation:** REPL or one-off command for trivial observations; a short script for repeatable scenarios.
2. **Existing test runner:** Use its fixtures, imports, mocks, or test discovery when that reduces setup or is required to execute the target.
3. **Dependency isolation:** Combine with either option above. Prefer built-in injection points, small fakes/stubs, and temporary resources over elaborate mocks.
4. **Custom wrapper:** Use a targeted harness only where simpler options cannot reach the relevant path.

Prefer a file-based, repeatable entry point for debugger handoff. Do not try each option mechanically; reassess only if the chosen approach proves inadequate.

### 1.4 Isolate dependencies and effects

- Keep the real target implementation under inspection; do not copy or reimplement its logic in the harness.
- Substitute network, database, model, time, or other external dependencies only insofar as they obscure the behavior being investigated.
- When patching a dependency, replace the reference the target actually resolves, which may be an imported alias. Scope temporary replacements so they are restored even when the target raises an error.
- Use temporary files/directories when they are simpler than filesystem mocks. Keep any resources needed by the debugger alive until execution returns.
- Do not modify application source in either mode, including main guards or temporary probe calls. If proportionate isolation requires a source change, explain the specific obstacle and proposed change; leave implementation to a separate user decision. Do not launch external services or allow destructive operations against real data.

### 1.5 Make inputs adjustable

- Put scenario knobs (arguments, mock responses, toggles, paths, and expectations) together near the top of the harness.
- Default to one representative path. Offer a small set of named scenarios when useful, without building a fixture framework.
- Keep scenario definitions separate from wiring so the user can change inputs without editing scaffolding internals.
- Ensure values satisfy necessary shape/type constraints while preserving the intended test condition.

### 1.6 Complexity and stopping rules

- Favor a small faithful reproduction over broad branch coverage. Add complexity only to reach the requested path or isolate a relevant dependency.
- Do not refactor production code, install dependencies without approval, rewrite project tooling, or construct a replica of the application simply to make the probe work.
- If isolation becomes disproportionate, stop and explain the blocker, the simplest viable next step, and what remains unverified.
- Keep generated files disposable and uncommitted. For debugger handoff, reuse a suitable project-local ignored scratch directory; otherwise create `code-probe/` at the project root with a `.gitignore` containing a single `*` rule. In Git repositories, this ignores the directory's contents, including the ignore file itself; existing tracked files remain tracked. Do not modify the root `.gitignore` or `.git/info/exclude` for probe artifacts.
- Inspect existing scratch directories, ignore rules, and probe artifacts before reuse. Preserve existing ignore rules, unrelated files, and manual scenario edits rather than overwriting them. Use descriptive harness filenames and do not delete artifacts needed for handoff.
- Auto-probes may use temporary directories when their artifacts do not need continued manual editing.

### 1.7 Additional dependency negotiation

- Prefer existing dependencies and standard-language tools; seek a dependency-free alternative first.
- If the environment cannot adequately support the probe, name the missing capability, proposed package/tool, and practical benefit.
- Obtain approval before installation or changes to dependency manifests/lockfiles; otherwise use the best available approach and disclose limitations.

### 1.8 Language-specific considerations

The selection rules above remain authoritative. Adapt to each repository; these are examples, not fixed templates.

- **Python:** Respect the project interpreter/environment (for example, `uv` and its lockfile). A REPL can suit tiny pure expressions; a script or existing `unittest`/pytest test usually suits repeatable runs. Use the installed Python debugger/VS Code adapter when available.
- **TypeScript/JavaScript:** Reuse the project's package manager, runtime/loader, test runner, module format, and source-map configuration (for example, Node, tsx, Jest, or Vitest). Ensure the debugger runs the same execution path and resolves TypeScript source when applicable. Check the effective module format at the harness location, including its extension and nearest `package.json`; its scope can differ from the target's. Adapt the harness rather than changing project module settings to make it load.
- **Other languages:** Derive the smallest executable entry point and debugger settings from the repository's own build, test, and IDE conventions.


## 2. Auto-probe

1. Translate the user's suspicion into the fewest relevant observations or assertions. When no expected value is established, observe and report rather than inventing a pass condition.
2. Execute the chosen harness using the existing project runtime. Capture relevant inputs, outputs, intermediate observations available without production changes, and errors. When using a test runner, confirm that the intended cases were collected and executed; a successful exit alone does not establish this.
3. If setup fails, distinguish harness/runtime failure from target behavior. Repair minimal scaffolding and retry only when proportionate.
4. Compare actual observations with expected behavior. State whether the hypothesis is supported, contradicted, or unresolved; distinguish reproductions from inferences.
5. Report the invocation, scenario knobs, observations, limitations, and disposable file locations. Do not automatically promote the harness into permanent tests.

## 3. Debugger handoff

### 3.1 Prepare execution

- Prepare a repeatable, file-based entry point that calls the real target under a controllable scenario. Reuse a suitable existing entry point or create a disposable harness using the shared selection and isolation rules.
- Inspect import-time execution before selecting the entry point: importing a module can run top-level application or demo calls before the harness calls the target.
- Do not run behavioral checks or exercise the target merely to validate the scenario. Safe static/configuration checks are permitted when they do not execute application behavior; disclose what was and was not verified.
- Do not insert, configure, or place breakpoints. The user controls breakpoints in the IDE.

### 3.2 Configure debugging

- Default to a **named VS Code launch configuration** when VS Code is the intended editor and a suitable adapter is available. Use the selected entry point, with appropriate working directory, environment, runtime arguments, and source mapping.
- If `.vscode/launch.json` does not exist, create it. If it exists, add or refresh only the code-probe configuration; preserve other entries, comments, and settings. Do not replace the whole file. Identify an existing probe entry by its target or harness as well as its name; choose a distinct name when ownership is ambiguous.
- Handle `launch.json` as JSON with comments and trailing commas. If it is malformed or cannot be edited safely while preserving its contents, leave it unchanged and provide a separate configuration snippet.
- If this requires changing a tracked project configuration, request approval first. If declined, provide a ready-to-insert configuration without modifying the tracked file.
- If a launch configuration is unsuitable, supply the smallest exact debugger invocation instead; do not install an adapter without approval.

### 3.3 Handoff report

- Provide the target, a clickable link to the selected entry point, launch-configuration name (or invocation), scenario knobs, and the action to start debugging.
- State which dependencies were replaced and which path the scenario is designed to reach.
- Clearly label the prepared entry point **not behaviorally executed**. Do not claim that its runtime path is verified unless independently established without executing the target.
- Leave disposable files available for manual editing and repeated debugging. Do not set breakpoints or conduct an automatic investigation.
