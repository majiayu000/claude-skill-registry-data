---
name: plan-v2-migration
description: Use this skill when user requests to migrate, upgrade, or plan migration to Crossplane v2. Analyzes an existing v1 configuration package and writes a migration plan covering XRD updates, provider API groups, function code changes, test updates, examples and dependencies, with the decisions a migration needs recorded. Use immediately when user mentions "migrate to v2", "upgrade to crossplane v2", "plan v2 migration", or "crossplane 2 migration". Use this skill instead of manually analyzing migration requirements; it also holds the language-neutral reference of every v1 to v2 breaking change. Not for executing an existing plan - use execute-v2-migration.
license: Apache-2.0
references:
  - references/breaking-changes.md
  - references/checklist-template.md
---

# Crossplane v2 migration planner

Analyze a Crossplane v1 configuration package and write the plan that `execute-v2-migration`
carries out: `.agents/plans/CROSSPLANE_V2_MIGRATION.md`.

## Before you start

Load `control-plane-project-charter` first, or read its `SKILL.md` beside this skill's
directory; this skill does not load it. The only questions are whether to replace an existing
plan (Phase 1) and Phase 5's decisions, asked only when interactive (charter §1).

- Analysis only: write the plan file and nothing else — no code changes, builds, tests or
  commits.
- Every change you plan comes from [breaking-changes.md](references/breaking-changes.md). Point
  at its sections; do not restate them in the plan. Upstream: the
  [Crossplane v2 upgrade guide](https://docs.crossplane.io/latest/guides/upgrade-to-crossplane-v2/)
  and [What's new in v2](https://docs.crossplane.io/latest/whats-new/).
- The plan changes the project, not a control plane. Moving a control plane that runs the v1
  package is a rollout risk you record, never a step you plan
  ([Installed v1 APIs](references/breaking-changes.md#installed-v1-apis)).

## Phase 1: Confirm a v1 project

First, if `.agents/plans/CROSSPLANE_V2_MIGRATION.md` exists, a migration may be under way, and
its ticks are where `execute-v2-migration continue` resumes. Interactive: ask whether to keep it
or replace it; to keep it, stop and point to `execute-v2-migration continue`. Unattended: do not
overwrite it; stop and report that it exists.

```bash
grep -n '^apiVersion:' upbound.yaml                         # meta.dev.upbound.io/v1alpha1
grep -rl 'kind: CompositeResourceDefinition' apis/ | xargs grep -l 'apiextensions.crossplane.io/v1$'
```

The second command lists the XRDs still on v1, filtering on the kind because Compositions are
`apiextensions.crossplane.io/v1` in both versions. Functions can lag behind both: run Phase 4's
first grep over `functions/` too. If nothing is v1 — `upbound.yaml`, XRDs or functions — report
that and stop. If the project is partly migrated, plan only what is left and say so.

## Phase 2: Map the project

```bash
yq '.metadata.name' upbound.yaml
find apis -name definition.yaml | sort                      # XRDs
find apis -name composition.yaml | sort                     # compositions
ls -1d functions/*/ tests/test-*/ tests/e2etest-*/ 2>/dev/null
ls -1 examples/ 2>/dev/null
```

Detect each function's language and the test language with
`control-plane-project-charter/references/languages/README.md`, and read that language file: it
gives the import spelling and XR bootstrap you will plan. Map which composition calls which
function (`functionRef.name`) and which tests cover which composition.

## Phase 3: Check the dependencies

A sub-agent keeps the large marketplace pages out of your context. Hand it this brief and wait
for its report; if your harness has no sub-agents, follow the brief yourself
(`control-plane-project-charter` §1).

```text
Read upbound.yaml in <project root> and list every entry of spec.dependsOn.

For each provider: note its name and version, then open
https://marketplace.upbound.io/providers/<org>/<provider>/<version>#managedResources
and read the "Namespace Scoped (<count>)" figure. A count above 0 serves the .m. API groups.
If it is 0, find the oldest version whose count is above 0.

For each configuration: find its source repository from its marketplace page and check
whether its XRDs are apiextensions.crossplane.io/v2 with scope: Namespaced. If not, find a
version that is.

If a page cannot be fetched, say so for that package; never guess a version.

Report, per package: current version, v2-ready yes/no, the target version if not, and the
URL you verified it on.
```

## Phase 4: Analyze each component

Check every file against [breaking-changes.md](references/breaking-changes.md) and note which
sections apply to each.

```bash
# XRDs: version, scope, Kind, claim and connection-secret fields
yq '[.apiVersion, .spec.scope, .spec.names.kind, .spec.claimNames, .spec.connectionSecretKeys, .spec.defaultCompositeDeletePolicy]' apis/<path>/definition.yaml
# Compositions
yq '[.spec.mode, .spec.writeConnectionSecretsToNamespace, .spec.compositeTypeRef, .spec.pipeline[].functionRef.name]' apis/<path>/composition.yaml
# Examples
yq '[.kind, .metadata.namespace, .spec.compositionSelector, .spec.compositionRef, .spec.writeConnectionSecretToRef]' examples/<file>.yaml

# Functions and tests: legacy provider groups and model paths, in any language
grep -rnE '(aws|azure|gcp)\.upbound\.io|io[./]upbound[./](aws|azure|gcp)[./]|(kubernetes|helm)\.crossplane\.io|io[./]crossplane[./](kubernetes|helm)[./]' functions/ tests/
# ... and the fields whose v2 meaning differs
grep -rnE 'deletionPolicy|providerConfigRef|managementPolicies|[Ss]ecretRef|namespace\s*[:=]' functions/ tests/
grep -rniE 'connection_?details|writeConnectionSecret' functions/ tests/
```

The first grep matches the legacy forms only (`ec2.aws.upbound.io`, Python
`models.io.upbound.aws`, Go `io/upbound/aws/`); extend it for any other provider the project
uses. Judge each hit of the field grep: a reference naming `default` goes, one naming another
config stays, a `deletionPolicy` parameter gets mapped.

## Phase 5: Decide

Four questions have no answer in the code. Interactive: ask the user the open ones. Unattended:
take the default and record it in the plan as an assumption.

| Decision | Default |
|---|---|
| Keep or rename each X-prefixed Kind | keep ([Kind and the X prefix](references/breaking-changes.md#kind-and-the-x-prefix)) |
| A `deletionPolicy` parameter | keep it and map it ([deletionPolicy](references/breaking-changes.md#deletionpolicy)) |
| Each non-`default` `providerConfigRef` | keep it as a `ClusterProviderConfig` reference ([providerConfigRef](references/breaking-changes.md#providerconfigref)) |
| Is the v1 package installed on a control plane? | assume yes: record the rollout risk |

## Phase 6: Write the plan

Write `.agents/plans/CROSSPLANE_V2_MIGRATION.md` (overwrite an existing one only if the user
chose to replace it in Phase 1) from
[checklist-template.md](references/checklist-template.md): real file paths, the target version
for every dependency, and, for stage 5, which tests cover each function and what each test
should fail on before its function is migrated. A stage that does not apply keeps its heading with
`None: <why>`.

## Phase 7: Report

```markdown
## v2 migration plan: [project]

Plan: `.agents/plans/CROSSPLANE_V2_MIGRATION.md`
Scope: [n] XRDs, [n] compositions, [n] functions ([languages]), [n] tests, [n] examples;
[n] dependencies to bump
Breaking changes that matter here: [3–5, most consequential first]
Decisions: [each, and whether the user made it or you assumed it]
Rollout risk: [one line, or "none: not installed anywhere"]
Next: review the plan, then run `execute-v2-migration`.
```

## Success criteria

Checks for you before you report, not a report format (`control-plane-project-charter` §4:
report the effect, not the intent).

- Every XRD, composition, function, test and example is in the plan, or named as needing no
  change.
- Every dependency has a verified target version, or is marked unverified with the reason.
- Every assumed decision is labelled as an assumption.
- No file outside `.agents/plans/` changed (`git status`).
