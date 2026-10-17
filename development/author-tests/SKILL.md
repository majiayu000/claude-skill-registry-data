---
name: author-tests
description: Use this skill when user requests to write, create, author, modify, refactor or plan refactoring of Crossplane configuration tests (composition tests or E2E tests) in a control-plane project - in any language (KCL, Python, YAML, Go, go-templating). Use this rather than a generic planning mode when the user asks for a plan to refactor composition tests or e2e tests in a crossplane configuration package. Specialized skill focused only on test authoring and modification (not running tests). Detects the test language and applies the right templates and patterns. Always load this skill before writing or changing composition or E2E test files, instead of writing them directly - also when you get there partway through another skill's workflow, such as scaffolding a new package. Covers writing an E2ETest - defaultConditions, extraResources, E2E credentials (static Secret or web identity) and what an E2ETest can assert.
license: Apache-2.0
references:
  - references/test-model.md
  - references/e2e.md
  - references/refactoring.md
---

# Crossplane Test Authoring

Author and modify Crossplane configuration tests, in any language `up test generate` supports,
and write the assertion that has to fail first.

## Before you start

A test's *meaning* is language-agnostic; only its *syntax* differs. Every test compiles to a
`CompositionTest` or an `E2ETest` (`meta.dev.upbound.io/v1alpha1`). The rules are in this file;
the object model, structuring patterns and common mistakes in
[test-model.md](references/test-model.md) (read it before your first test in a project); the
syntax in the charter's file for the test language (Phase 1).

- Writing or changing an `E2ETest`: Phase 4.
- Planning or executing a test refactor: [refactoring.md](references/refactoring.md) (plan into
  `.agents/tasks/REFACTOR_TESTS.md` without executing, then one item per run).
- Not here: building the package or running the whole suite as a gate, except Phase 6
  (`verify-configuration`); running E2E tests (`e2e-test-configuration`); implementing
  composition features (`author-composition`).

## Binding rules — they hold even if you open nothing else

Load `control-plane-project-charter` first, or read its `SKILL.md` beside this skill's
directory: this skill does not load it, and the charter has the reasons. The project's own API,
design or gate script wins over these: say where you departed.

1. **Never block on a question nobody can answer.** Interactive, ask only what the project
   can't tell you; unattended, never ask: decide from the spec and state the assumption, or
   stop and report (charter §1).
2. **Never create a group, Space, control plane or cloud resource as a side effect, and never
   pass `--public` yourself** (§9). Run `up test run --e2e` only after loading
   e2e-test-configuration: it has each target's preconditions, and the read-back and teardown
   rules.
3. **Test first: watch each new composition or unit test fail for the reason you intended**;
   for a new E2ETest this is optional. A syntax error, a missing path, `✗ Parsing tests`, a
   compile error or a bug in the test's own logic is a broken test, not RED. Backfill by
   mutating the implementation, never the expected value (§3).
4. **In a v2 project, managed resources carry `forProvider` only**, on the `.m.` API groups,
   unless the project's spec or API sets more: no `deletionPolicy`, `managementPolicies` or
   `metadata.namespace`; omit `providerConfigRef` if and only if `ClusterProviderConfig/default`
   exists and is the right one. One whose connection details the function reads also needs
   `writeConnectionSecretToRef`, and a missing detail never falls back to a value. A v1 project
   stays v1 (§5).
5. **Claim only what ran:** the command's own exit code, not `tail`'s: redirect, then read
   `$?` (`cmd > /tmp/x.log 2>&1; echo "exit=$?"`); after a pipe, bash `${PIPESTATUS[0]}`,
   zsh `$pipestatus[1]`. `No test files found` means nothing ran. Name the layer you reached —
   render, composition test, local control plane, cloud — and never claim one you did not
   reach; for each new test, the change that turns it red, or call it unproven. Comments and
   docs claim no more (§4, §8).

## Phase 1: Detect the test language — do this first

Pick the language as charter §10 says (existing tests, else the composition language, else
YAML; functions in more than one language and no tests yet: ask), then read its file before
writing a test: it carries the templates and the silent failure modes.

## Phase 2: Decide what to test, and scaffold

1. **New test:** determine the feature, resources and variants from `args` and the project
   (`apis/*/definition.yaml`, `apis/*/composition.yaml`, the function source, the example XRs
   in `examples/*/*.yaml`) — do not ask. **Modifying a test:** read it, match its language and
   style, and understand its current assertions before you change them.
2. **Checking what is not a render.** `up test run` evaluates `CompositionTest` and `E2ETest`
   objects and nothing else. For the declarative files — dependencies in `upbound.yaml`, the
   XRD, `examples/`, a `ManagedResourceActivationPolicy` — sort what can be checked:

   - **What a render reaches, cover with a render.** XRD defaults reach the render through
     `xrdPath` (charter §2, §8), so assert the defaulted values on the composite. Render a shipped
     example with `xrPath: examples/<kind>/<file>.yaml` plus `xrdPath`: that proves the function
     handles it, not that the API server accepts it. A pipeline function missing from `dependsOn`
     already fails every render (`unknown function`).
   - **The rest is outside this suite.** `up project build` does not validate `examples/`, and it
     accepted an MRAP without its API dependency (up v0.55.0).
     `<author-configuration-package>/scripts/check_xrd_schema.py` checks XRD design, not a frozen
     surface; `<author-configuration-package>` is that skill's directory, beside this one. Where
     the project's gate script already runs such checks, they stay there, beside the build and the
     test run (charter §2: the project's gate wins).
   - **Write no test program or checker for these files, and don't copy a skill's script into the
     project** (charter §3: test-first is for behaviour). Invoke `check_xrd_schema.py` by its path
     in its skill's directory, with the project root as the working directory; the build and the
     composition tests that use the files do the rest.
   - **Never turn a test program into a linter.** A test dir that checks repo files, exits
     non-zero on a mismatch and prints `items: []` adds zero tests. Passing, it drops out of the
     count (alone: `No test files found`, exit 0); failing, it stops at `✗ Parsing tests`, which
     is a broken test, not RED.
   - **What no check here reaches** — XRD `required` lists, enums and scope; the dependency set —
     stays uncovered unless the project's gate checks it (charter §4: say what you did not
     verify).

3. **Organise:**

   | Type | Dir prefix | Timeout | `validate` | Purpose |
   |---|---|---|---|---|
   | Composition | `test-` | ≥60s | `false` (scaffold default) | local render, no cloud |
   | E2E | `e2etest-` | sized to what you provision ([e2e.md](references/e2e.md)) | n/a | real cloud lifecycle |

   Consolidate in one directory: the same resource type in different configs, feature on/off
   variants, 3–5 related scenarios. Separate directories: different resource types, complex
   sequential dependencies, and every E2E test. `up test run` runs every matched dir's program,
   so the composition gate is `up test run "tests/test-*"` (charter §7).

4. **Scaffold with `up test generate <name> [--e2e] --language <lang>`** (`kcl`, `python`,
   `yaml`, `go`, `go-templating`); never create a test directory by hand. Pass the bare name:
   the CLI prepends `test-`/`e2etest-`. Then write the test
   from the template in the language file. Python: run `setup_venv.py` again after generating
   each test directory (`control-plane-project-charter/references/languages/python.md`).

## Phase 3: Write the assertion that has to fail

Four things make an assertion bite:

| | |
|---|---|
| **Assert the field, not the existence.** | `assertResources` is partial and positive. An entry naming only `kind` passes against any resource of that kind, whatever it contains. Name the field you are adding. |
| **Assert on the composite too.** | Every `status` field the function writes needs an assertion on the XR itself. It is the only programmatic check on composition outputs. |
| **Cover the minimal XR.** | Use the inline `xr` field with every optional property omitted. That is the shape a real user writes first, and the one the scaffold never generates. |
| **Use distinguishing inputs.** | Every parameter the function passes through (region, config names, CIDRs, the XR's own name, …) gets a non-default value, unique across fields, in at least one test; a required field with no default needs two tests with different values. An input equal to the default or to a sibling field can't tell pass-through from a hard-coded constant. Backfill check: `control-plane-project-charter/references/charter/tdd.md`. |

- **Define the XR inline** where the format supports it, with `namespace: default` (v2).
- **Assert list membership on the parsed list**, not by substring matching on a joined string:
  a short token matches inside a longer one (`db` inside `db-subnet-group`).
- **Composed-resource names:** never guess one; the naming rule is in
  `control-plane-project-charter/references/charter/evidence.md`
  ([test-model.md, mistake 1](references/test-model.md#1-guessed-composed-resource-names)).
- **Managed resources in a test follow binding rule 4**, written as the import path in KCL,
  Python and Go and as the `apiVersion` string in YAML. Assert `providerConfigRef` and
  `managementPolicies` only where the project's spec or API sets them (whether a render keeps
  a value equal to the model default depends on the language and SDK; see the language file).

### Asserting absence

`assertResources` cannot assert absence: it has no absence operator, so do not search the CLI
for one.

| Must be absent | How |
|---|---|
| A composed **resource** | Assert the composite's `spec.crossplane.resourceRefs` as the exact list from the render, once per input shape, not in every case. Lists match exactly, so a surplus resource fails it. The "Composition test template" sections of `control-plane-project-charter/references/languages/go/tests.md` and `control-plane-project-charter/references/languages/go-templating.md` show this guard; detail in `control-plane-project-charter/references/charter/evidence.md`, "How `assertResources` matches" |
| A **field** | Not expressible in a composition test. Use a unit test on the function's desired state, in the function's own language (Go: `go test ./...` in `functions/<n>/`), or confirm it once in the render and report it as not asserted |

### A Fatal result

A `CompositionTest` cannot assert a Fatal result. `up test run` renders through Crossplane, which
stops at the Fatal before any assertion: the test fails with
`… returned a fatal result: <message>` (observed with up v0.55.0), and a `CompositionTest` has no
field for an expected error, so not even a `resourceRefs: []` guard runs. A Fatal case under
`tests/test-*` fails the gate. Test each fatal path in a function unit test (the message, nothing
composed; Go: `control-plane-project-charter/references/languages/go/functions.md`, "A path that
must return Fatal"), keep composition tests on inputs the function accepts, and don't search the
CLI, its binaries or the web for another way.

### Asserting a property of every composed resource

When a property applies to *every* composed resource (a label, a policy, a config ref, a
region), assert it in one test that ranges over all desired resources, not in per-resource
expectations: those inherit each row's omissions, so a resource that misses it stays green. The
tier that can range is a function unit test over the desired state (Go sketch:
`control-plane-project-charter/references/languages/go/functions.md`, unit-test template). A
CompositionTest cannot iterate over the render; it fits only when one helper adds the property
to every expectation and there is one expectation per entry of the exact `resourceRefs` list.

## Phase 4: E2E tests

**Read [e2e.md](references/e2e.md) before writing or changing any `E2ETest`** — fields and
defaults, credentials per target, the ProviderConfig the test creates, a Go template, and what
counts as an e2e RED.

- `defaultConditions` lists condition types (`Ready`), never expressions or status paths.
- An `E2ETest` cannot assert a status field or a status condition: it waits only for the
  `defaultConditions` types (`Ready`). To check a status value, use an `observedResources`
  CompositionTest or a unit test; a value read back during an e2e run is report evidence, not an
  assertion ([e2e.md](references/e2e.md#what-an-e2etest-cannot-assert)). Do not search the
  `up` binary or the web for another mechanism.
- Set `timeoutSeconds` explicitly, sized to what you provision. Credentials depend on the
  target: `source: Upbound` works only on a Spaces control plane.
- `extraResources` creates the ProviderConfig: by default a `ClusterProviderConfig` named
  `default`, with no namespace ([e2e.md](references/e2e.md#the-providerconfig-the-test-creates)).
- **Never put long-lived credentials in a test** — use web identity, or a Secret filled from a
  `UP_*` variable — and **never set `skipDelete: true`**: it leaves real cloud resources
  running.
- **Never print a generated `E2ETest`, or a Secret, with real credential values, or write it to
  a file**: its `extraResources` carry the credential. Check it with a dummy value, and keep the
  warning in the template's header comment and fail message
  ([e2e.md](references/e2e.md#credentials-depend-on-the-target)).

## Phase 5: Run it — RED, then GREEN

Charter §3's loop, run directly with `up test run "tests/<t>"`. If the run also changes the
function, `author-composition` Phase 4 says which skill runs RED, GREEN and the gate. Only when
you add or change tests alone are this phase and Phase 6 the whole loop.

## Phase 6: The gate, after the loop

Once the suite is green:

- **The project defines its own gate** (a script or make target): run that, not
  `verify-configuration` (charter §2: the project's own decisions win).
- **Otherwise** hand off to `verify-configuration` for the build and the whole suite.
- **No control plane or deploy allowed** (the project, the user or your instructions say so):
  the gate is the build and the whole `up test run` — `verify-configuration` Phases 1–2, or
  the project's gate — and nothing after it: no E2E, no `up project run` (binding rule 2).
  Where only Upbound Cloud is ruled out, `verify-configuration`'s "Local-only projects and
  projects with their own gate" says what changes.

## Success criteria

Checks for you before you report, not a report format (charter §4: report what ran). Test
authoring is complete when:

- The test language was detected or chosen, and the scaffold generated (or the existing test
  read)
- The test follows this file, test-model.md and the matching language file
- The fields that matter are asserted, not just existence
- The new assertion was observed to fail before the implementation existed, and to pass after
- The gate passed once the suite was green — the project's own gate if it has one, else
  `verify-configuration`, without a deploy where none is allowed (Phase 6)
