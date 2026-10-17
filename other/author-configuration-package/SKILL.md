---
name: author-configuration-package
description: Use this skill when user requests to create, scaffold, modify, or extend a Crossplane configuration package. Handles project initialization, XRD creation/modification, composition setup, dependency management (including MRAPs and `up dep add --api`), function generation, building, and setting up the local development environment. Use immediately when user mentions creating/scaffolding/modifying/extending a configuration package, adding new resources to an existing package, installing or adding a provider ("add provider-aws-s3", "install the AWS provider", `up dep add`), or setting up the Python environment ("configure a venv", "my imports do not resolve", "set the VS Code interpreter"). Use this skill instead of manually creating project structures, XRDs, or running `up project init`/`up function generate` commands directly. Not for composition function code — use author-composition; not for verifying or running the project — use verify-configuration.
license: Apache-2.0
references:
  - references/templates.md
  - references/providerconfig.md
  - references/mrap.md
---

# Crossplane Configuration Package Authoring

Scaffold and modify Crossplane configuration packages — structure, XRDs, dependencies, the
generated composition and function skeletons, examples and the build — in the order the CLI
needs. Composition logic and tests are other skills' work.

## Before you start

Run the phases in order. The two builds bracket function generation: models come from the
XRD and the dependencies (Phase 6), and the function is generated against them (Phase 7).

- Composition logic → `author-composition`; tests → `author-tests`, which writes each failing
  test before `author-composition` implements it (charter §3); verification and deploying →
  the project's own gate, else `verify-configuration`.

This skill stops at a built package. Where a run lands and why a Space context needs the user's
choice — `--public` publishes their package — is
`control-plane-project-charter/references/charter/targets.md`.

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

## Phase 1: Gather the project and resource information

From the spec: project name, API group, cloud, organisation, maintainer; then the resource Kind,
its plural and its version (`v1alpha1` for a new API,
`control-plane-project-charter/references/charter/xrd-design.md`); and the function language for
Phase 7 (`kcl`, `python`, `go`, `go-templating`) — from the spec or an existing function, else
ask: it is a decision, not a discoverable fact. New tests follow it (charter §10). Interactive
and not in the spec: ask, with the tables in
[templates.md](references/templates.md#questions-for-a-new-project).

## Phase 2: Start or open the project

`test -f upbound.yaml` tells you which. In an existing project, list its APIs
(`apis/*/definition.yaml`): add a resource from Phase 3, or change one: read it, edit it,
rebuild.

**Use the CLI generators for everything but the XRD.** A hand-written composition or function
layout is what produces `mode: Resources`, `apiVersion: v1` and a pipeline the CLI did not
wire; the XRD is the one file you write (Phase 3).

| Command | Input → Output |
|---|---|
| `up project init <name>` | interactive wizard → a whole working project (below) |
| `up example generate [<xrd>]` | wizard, or an XRD → `examples/<kind-lowercase>/<xr-name>.yaml`; the name defaults to the lowercase Kind (`examples/network/network.yaml`, up v0.55.0). Find the file; don't assume `example.yaml` |
| `up xrd generate <example.yaml>` | an example XR → an inferred `apis/<plural>/definition.yaml` + language models. Not for the XRD you ship (Phase 3) |
| `up composition generate <xrd\|xr>` | XRD or XR → `apis/<plural>/composition.yaml`, and adds the required function packages as dependencies |
| `up function generate <name> [<pipeline-path>]` | → `functions/<name>/…`, and wires it into that composition's pipeline. On an existing `functions/<name>` it prompts to overwrite and, without a TTY, cancels: wire the step by hand (`control-plane-project-charter/references/charter/generators.md`) |
| `up test generate <name> [--e2e]` | → `tests/test-<name>/…` (or `tests/e2etest-<name>/…`) |

The generators disagree on pluralization — `examples/storagebucket/` vs
`apis/storagebuckets/` — so read the path each command prints.

**`up project init`.** Non-interactively: `up project init <name> --scratch` (or
`--template <t> --language <lang> [--test-language <lang>]`). A language template gives a
complete, passing project whose Python functions use the embedded layout (`main.py` +
`requirements.txt`), not what `up function generate` produces: code you add matches what the
project has (`control-plane-project-charter/references/languages/python.md`). Its Crossplane
generation is the template's, and the templates differ: check the XRDs' `apiVersion` before
anything else (`control-plane-project-charter/references/charter/generators.md`).

- `--scratch` ignores `--language` (it logs `... for kcl` regardless). Harmless — the scratch
  template has no functions — but don't read it as the project's language.
- `--scratch` also writes `.github/workflows/` (`ci.yaml`, `composition-test.yaml`, `e2e.yaml`,
  `tag.yaml`; up v0.55.0). Delete them when the spec allows no CI.
- `up project init --directory .` fails with `directory is not empty` even when the directory
  holds only `.git`. Init into a temporary directory and move the files across, dotfiles
  included (up v0.55.0).
- `up project init` rewrites `metadata.name` and `spec.repository` but never `spec.source`, so
  every template leaves its own (`github.com/upbound/project-template-scratch`, `…-aws-s3`),
  along with a placeholder `maintainer`. Generated Go module paths, for tests and for functions,
  come from `spec.source` (`<source>/tests/<dir>`, `<source>/functions/<name>`).
  `up project build` publishes it as the package's `meta.crossplane.io/source` annotation.
  **Set `repository`, `source` and `maintainer` before any generator runs**: `spec.repository`
  names the embedded function in every `functionRef`
  (`control-plane-project-charter/references/charter/generators.md`). A Go module generated
  earlier, or bundled by a template, keeps the template path; that doesn't affect the build. An
  `upbound.yaml` and a `.gitignore` to start from:
  [templates.md](references/templates.md), sections `upbound.yaml` and `.gitignore`.
- Templates leave `examples/example/example.yaml` (`kind: Example`, `spec: {}`), backed by no
  XRD. Delete it; the real example is the file `up example generate` writes.

## Phase 3: Write the XRD, and check its design

**Write the XRD yourself** (charter §5 has the reason,
`control-plane-project-charter/references/charter/v2-resources.md` the v2 skeleton). For a
**new** XRD:

| Field | Value |
|---|---|
| `apiVersion` | `apiextensions.crossplane.io/v2` |
| `scope` | `Namespaced` |
| version | `v1alpha1` |
| `names.kind` | exactly the user's XR Kind (`Network`): no `X` prefix, no `claimNames` |

An existing v1 project stays v1 until it is migrated deliberately (`plan-v2-migration`), and a
migration keeps its Kind, `X` prefix included: renaming a Kind is a new API, and existing
objects are not converted
(`control-plane-project-charter/references/charter/xrd-design.md`). Don't copy a template's XRD
as a v2 starting point without checking its `apiVersion`: the cloud templates' XRDs are v1.

**The fastest correct route for a new API is example-first:** write the XR you want users to
write, then write the XRD to match it, then generate the composition from it.

```bash
# Pass --scope, or the command prompts for it: see the first bullet after this block.
up example generate --scope=namespace --name example --namespace default \
    --api-group platform.example.com --api-version v1alpha1 --kind StorageBucket
#   -> examples/storagebucket/example.yaml (spec: {}); fill in the spec users should write
# Write apis/storagebuckets/definition.yaml yourself (plural directory).
up dep add 'xpkg.upbound.io/upbound/provider-aws-s3:>=v2.0.0, <v3.0.0'      # Phase 4
up composition generate apis/storagebuckets/definition.yaml                 # Phase 5
up project build                                                            # Phase 6
up function generate compose-bucket apis/storagebuckets/composition.yaml \
    --language <lang>                                                       # Phase 7
up project build                                                            # Phase 9
```

Write the example XRs under `examples/<kind-lowercase>/<xr-name>.yaml` — a minimal one with
the required fields only, and a complete one
([templates.md](references/templates.md#example-xrs)).

- **`up example generate` prompts for scope even when every other flag is supplied.** Without
  a TTY it prints `ERROR: ... could not open a new TTY`, then writes the file with the
  namespaced default and exits 0. Always pass `--scope=namespace` (or `--scope=cluster`).
- **Write every open-ended map as `additionalProperties`**, never as fixed properties:

  ```yaml
  tags:
    type: object
    additionalProperties:
      type: string
  ```

  Fixed `properties:` under a map generates one model field per key, so every key a user did
  not supply arrives as a null the typed model rejects (Python: `Input should be a valid
  string [input_value=None]`). It is the most common way a hand-written XRD goes wrong, and
  exactly what `up xrd generate` emits for a map inferred from an example.
- **Never run `up xrd generate` over an XRD that already exists.** An example carries values,
  not constraints, so regenerating silently drops `enum:`, `default:`,
  `minimum:`/`maximum:`/`pattern:`, `description:` and the intended `required:`. Treat
  `apis/*/definition.yaml` as hand-maintained source. As a read-only second opinion,
  `up xrd generate <example.yaml> -o yaml > /tmp/xrd.yaml` prints the XRD instead of writing
  it (`-o` takes a format, not a path); `diff` that against yours. It also accepts
  `--input rgd`, `--input SimpleSchema` and `--plural` (`--plural postgreses`), and its
  output is a draft you review and then own.
- With no spec to read the fields from (interactive only), collect them with the field wizard
  in [templates.md](references/templates.md#xrd-field-wizard), and keep every constraint you
  add compatible with the user's draft XR.

**A field list is not the schema.** It cannot tell you that a field is `vpcId` while the Kind is
`VPC`, that a repeated group prefix may or may not be stutter, that an unbounded array leaves no
CEL budget, or that redefining `READY` prints the column twice. XRD versions must round-trip
(even a rename needs a conversion webhook), so all of that is permanent from the first version
that ships.
`control-plane-project-charter/references/charter/xrd-design.md` has the rules. Run the
mechanical ones before the first build with the script in this skill's directory
(`<author-configuration-package>`, the directory containing this SKILL.md). Invoke it by its
path in the skill directory, with the project root as the working directory: don't copy it into
the project, and don't write a test for the XRD (charter §3).

```bash
python3 <author-configuration-package>/scripts/check_xrd_schema.py \
  apis/*/definition.yaml
```

Exit `0` is clean, `10` is at least one finding, and `2` means it extracted nothing — a corpus
error, not a pass. `FAIL` lines are defects; `REVIEW` lines (booleans, bare strings) are calls
for you to make. The `ACRONYMS` table applies to the **Kind** only; trim it to the acronyms this
API uses.

An enum whose values mirror an upstream API verbatim (`aurora-postgresql`) fails the casing
rule by design, and a **frozen API** (already shipped, or fixed by the project's spec) reports
FAILs you may not fix. Record each deliberate one in `xrd-schema-exceptions.yaml` at the
project root, under its rule class, with a mandatory `reason`:

```yaml
enumCasing:
  - field: apis/db/definition.yaml[*].spec.engine   # the location the FAIL prints
    reason: AWS RDS engine names, passed through verbatim
maxItems:
  - field: apis/network/definition.yaml[v1alpha1].status.subnetIds
    reason: frozen API, shipped without a bound
description:
  - field: '*[v1alpha1].spec.region'   # quoted: unquoted, YAML reads a leading * as an alias
    reason: v1alpha1 is frozen in every XRD; v1beta1 carries the descriptions
```

Write `field` as the FAIL prints it, `<file>[<version>].<path>`, so the exception covers that XRD
and version and nothing else. The file is a path, not a glob. Either part can instead be a bare
`*`: `[*]` is every version of one XRD, `*[v1]` is v1 of every XRD, and `*[*].<path>` is a
deliberate project-wide waiver; quote any entry that starts with `*`. Classes keyed by field
path: `enumCasing`, `description`, `listType`, `maxItems`, `lowerCamel`, `fieldCasing`. By name:
`printerColumn` takes `<file>[<version>].READY`, `kindAcronym` takes `<file>[*].<Kind>` (a Kind
spans every version), and `collision` takes the spellings as printed with no file, since a
collision spans the corpus. `uniqueItems` has none: the API server rejects the CRD. A bare path
with no `<file>[<version>].` applies everywhere, and when it excepts findings in
more than one XRD or version the script lists those places for REVIEW: an exception for a frozen
v1alpha1 would otherwise hide the same defect in the v1beta1 you can still fix.

The script reads the file from the working directory and prints those findings as `EXCEPTED`.
When several entries match one finding, the most specific gives the reason. An entry that
matches nothing, or only findings a more specific entry already covers, is reported for REVIEW,
and the script can then serve as a gate. To read a frozen API's state without gating, pass
`--report-only` (exit 0 despite findings). A skeleton XRD has too few fields to count as an
extraction, so pass `--min-corpus` until the API has grown.

## Phase 4: Add dependencies

`up dep add` needs a package **reference** (`xpkg.upbound.io/upbound/provider-azure-network`).
When the user names a cloud and a resource but not the ref, resolve it; do not guess a
package name.

- **Upbound Marketplace MCP**, if one is configured (it uses your `up login` credentials):
  `search_packages` (filter by type, cloud/family and tier) for the package and its `xpkg`
  ref, then `get_package_version_resources` (or `..._groupkind_resources`) for the exact
  group/kind/version you will compose (`ResourceGroup` → `azure.m.upbound.io/v1beta1`).
- **Otherwise web search and fetch:** `site:marketplace.upbound.io <cloud> <service> provider`
  (functions: `... function`), or a page such as
  `https://marketplace.upbound.io/providers/upbound/provider-azure-network`, for the ref and
  latest version. Pages list scope and description, not always exact Kinds — confirm Kinds
  from the generated models after the first build.
- **Prefer v2+ Upbound Official family providers** (`provider-<cloud>-<service>`) over the
  monolithic `provider-<cloud>`. A new project needs v2.x: the `.m.` groups ship from v2.0.0.
- **Base resources live in the family package.** `ResourceGroup`, `ProviderConfig` and other
  cross-service basics ship in `provider-family-<cloud>`. Service providers depend on it
  transitively, but add it explicitly when you compose a base resource directly.
- When more than one package could fit, ask the user, listing the candidates.
- **Always pass a constraint that caps the major:** `up dep add '<ref>:>=v2.0.0, <v3.0.0'`
  (accepted by up v0.55.0). A bare `<ref>` records `version: '>=v0.0.0'`, and `'>=v2.0.0'`
  alone still accepts any later major.
- **The CLI rewrites `upbound.yaml`.** When there is at least one dependency, `up dep add`,
  `up project build`, `up test run` and `up test generate` re-serialise it on every run, even
  when nothing changed. Comments are stripped, keys are sorted, sequences are un-indented, and
  legacy `function:`/`provider:` entries become `apiVersion/kind/package` (up v0.55.0). Put the
  reason for a constraint in the README, not in a comment. Expect `upbound.yaml` in `git diff`
  after a build or a test run, but before attributing that diff to the CLI, confirm it is
  formatting only: no dependency or version constraint changed, other than the legacy-entry
  rewrite above (the same package and constraint, in the new shape).
- **External pipeline functions must be declared dependencies.** Embedded functions (built from
  `functions/`) are wired automatically. An external `functionRef`
  (`crossplane-contrib-function-auto-ready`, `function-patch-and-transform`) missing from
  `dependsOn` or the cache makes `up test run`'s render fail with
  `unknown function … is it listed in the render input?`. Fix it by declaring the dependency,
  not by deleting a step the project needs: declared external functions do render. The one step
  to delete is the duplicate auto-ready step of Phase 5. An embedded function whose
  `functionRef.name` departs from the generated one gives the same error
  (`control-plane-project-charter/references/charter/generators.md`).

Writing a ManagedResourceActivationPolicy, or running `up dep add --api crossplane:<tag>`:
read [mrap.md](references/mrap.md) first. The manifest must sit under `apis/` or it is
silently left out of the package, and `up project build` barely validates it.

## Phase 5: Generate the composition

`up composition generate apis/<plural>/definition.yaml` writes a `mode: Pipeline` composition
with an auto-ready step, and adds `crossplane-contrib/function-auto-ready` at `'>=v0.0.0'` to
`dependsOn` — even when the project already declares another auto-ready function, which then
gets a step too (up v0.55.0). When the project declares its own function set, delete the
duplicate step and its dependency, and say so; otherwise give the dependency a constraint.

`mode: Resources` was removed in Crossplane v2: only `Pipeline` is valid. `up test run`'s
local render tolerates `Resources`, but the API server rejects it on admission. Every `up`
scaffold emits `Pipeline`; don't hand-edit it.

## Phase 6: First build

`up project build` fetches any dependency missing from the cache and generates the models from
the XRD and the dependencies; check the model tree under `.up/<language>/` exists and holds the
Kinds and API versions you will compose. **Re-run it after every XRD change**: an edit leaves the
models stale (a `status` field added by hand is absent from the model until a rebuild).
No `.m.` models: the provider is v1.x. Any build that fails, or an XR that never gets Ready:
[templates.md](references/templates.md#when-a-build-fails-or-the-xr-never-gets-ready).

## Phase 7: Generate the function

Only after the first build: `up function generate <name> apis/<plural>/composition.yaml
--language <lang>`. It wires the models into the function only once they exist under
`.up/<language>/`. Check its step comes before the auto-ready step in the pipeline.

Python, before you write the function body: run
`python3 <author-composition>/scripts/setup_venv.py`, where `<author-composition>` is the
directory containing that skill's SKILL.md, beside this skill's directory (why it comes first:
`control-plane-project-charter/references/languages/python.md`).

## Phase 8: The ProviderConfig

**Every project needs a ProviderConfig, and `--scratch` gives you none.** Create
`examples/providerconfig.yaml`, matching the provider family from Phase 4: by default a
`ClusterProviderConfig` named `default`, unless the project's spec or API names another
config (charter §5). Without it, every managed resource sits unauthenticated while the build
and the tests pass. Read [providerconfig.md](references/providerconfig.md) before you write
it: the manifest, its family-group apiVersion, and the credential secret the README must
list.

## Phase 9: Final build, and report

`up project build` again; it produces the package under `_output/` (`.uppkg`).

A `.uppkg` is a tar of gzipped layers (`manifest.json` lists them). The configuration's
`package.yaml` (meta, XRDs, compositions, an MRAP) is in one layer, and the examples are in
another as `.up/examples.yaml` (up v0.55.0). To check that a file ships, extract into a fresh
directory, so an older extraction cannot make the grep pass:
`pkg=$(mktemp -d) && tar -xf _output/<name>.uppkg -C "$pkg" && echo "extracted: $pkg"`. The
variable is gone by your next command, so reuse the printed path: `tar -xzOf <dir>/<layer>` for
each layer and grep, then `rm -rf <dir>`. That proves it ships, not that a control plane
accepts it.

Then report what ran and what it printed, not a checklist (`control-plane-project-charter` §4):
the commands and exit codes, the layer reached (package build), and what you assumed. Template:
[templates.md](references/templates.md#hand-off-report).

## Success criteria

Checks for you before you report, not a report format (charter §4: report what ran):

- Project structure created, with `upbound.yaml` metadata set before any generator ran
- XRD written by hand, with the schema the user or spec defined, and `check_xrd_schema.py` run
- First build generated the models (`.up/<language>/` model tree exists)
- `up function generate` created the function, its step before auto-ready
- Final build succeeded (`.uppkg` under `_output/`)
- No unbounded dependency: every `dependsOn` `version` caps the major you built against
  (`'>=v2.0.0, <v3.0.0'`), never `'>=v0.0.0'`
- Example XRs and `examples/providerconfig.yaml` created
- The hand-off names the next skill
