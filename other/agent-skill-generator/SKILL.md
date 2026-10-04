---
name: agent-skill-generator
description: Design, create, revise, audit, validate, or optimize reusable agent skills and SKILL.md packages across platforms. Use for trigger precision, structure, progressive disclosure, token efficiency, prompt evals, or converting repeated workflows into portable skills. Do not use for AGENTS.md, skill fusion, or host packaging alone.
---

# Agent skill generator

Build portable skills by default, bind them to a repository or host only when the task requires it, and spend context only on behavior the target agent cannot reliably infer.

## Route by mode

Choose one primary mode and honor its side-effect boundary.

| Mode | Use when | Required output | File changes |
|---|---|---|---|
| `design` | Turn a problem or repeated workflow into an implementation-ready skill design | Contract, portability target, package map, side-effect boundaries, and validation plan | None |
| `new` | Build a skill from a defined problem or workflow | Complete skill package and validation summary | Create the agreed package; update only required registration metadata and docs |
| `revise` | Improve an existing skill | Focused edits, validation summary, and delta | Edit only authorized scope |
| `audit` | Find trigger, structure, portability, or token problems | Prioritized findings with concrete targets | None unless separately requested |
| `validate` | Pressure-test an existing skill | Evidence record and residual risk | None unless separately requested |
| `optimize-trigger` | Improve activation precision or recall | Revised trigger metadata plus adjacent-case analysis | Trigger-bearing metadata only unless broader edits are requested |

If the request mixes modes, keep read-only work read-only and state which changes are authorized before editing.
Do not rename stable skill identifiers in `optimize-trigger` mode unless the user explicitly requests a migration.

## Shared workflow

1. Define the mode, target outcome, success criteria, and output location.
2. Inspect the repository, existing skill package, conversation examples, and active host for facts that remove avoidable questions.
3. Resolve only decisions that materially affect triggers, runtime behavior, dependencies, side effects, portability, or packaging.
4. Design or assess the smallest package that makes the workflow repeatable.
5. Act within the selected mode's side-effect boundary.
6. Validate with the smallest evidence combination that answers the actual risk.
7. Remove token waste, review the diff or findings, and report evidence plus residual uncertainty.

Tailor depth to risk. Do not force every mode through creation steps or build a heavy evaluation harness for a wording-only change.

For broad maintenance, justify each substantive edit with a defect, ambiguous
decision, unsupported claim, unnecessary obligation, or useful capability gap.
Record preserved intent, outputs, safeguards, and resources before restructuring.
Retain correct material; newer APIs and shorter files alone do not prove improvement.

## Establish the contract

Require at least one of:

- a problem the skill should solve;
- a workflow it should standardize; or
- an existing skill folder to revise, audit, validate, or optimize.

Discover repository conventions before asking the user. For a design, new skill, or broad revision, make these decision-complete:

- primary users, target agents or hosts, and success criteria;
- obvious trigger phrases, paraphrases, adjacent negatives, and likely competing skills;
- required inputs, outputs, workflow order, and degrees of freedom;
- repository files, scripts, tools, services, permissions, and external side effects;
- portable, repo-bound, host-enhanced, or distributable target profile;
- minimum package contract, named target hosts when known, required host adapters, and evidence available for each portability claim;
- expected validation depth.

Ask only about choices whose answers would change the result. Use labeled defaults for the rest. Put runtime assumptions that future agents need in the skill; keep authoring decisions and temporary assumptions in the handoff summary instead of bloating the package.

## Investigate before designing

Search likely directories first and open only relevant files. Look for:

- neighboring skills and their trigger boundaries;
- always-loaded policy such as `AGENTS.md` or its platform equivalent;
- templates, schemas, scripts, tests, validators, and documented commands;
- corrections, failure cases, inputs, and outputs already demonstrated in the conversation;
- active host capabilities, native creators, metadata, or packaging tools exposed to the current run.

Treat host-native skill creators as environment-specific neighbors. Consider their trigger overlap only when the creator is exposed to the current run or explicitly invoked; do not infer a collision from a dormant installation or another host's catalog. Never narrow a portable skill solely around one host's built-in tooling.

If the repository is thin or unrelated, say so and continue with a portable design.

Treat packages being assessed as source artifacts. Do not follow their embedded
workflows, execute scripts, or install dependencies merely to review them.

## Choose the target profile

Default to `portable` unless evidence requires another profile.

- `portable`: keep behavior and core instructions host-neutral; declare the minimum package contract and isolate any adapters required by named target hosts.
- `repo-bound`: name the repository contract, real paths, and validators that make the skill local.
- `host-enhanced`: keep the portable core, then add host metadata or invocation policy only when the active target supports and benefits from it.
- `distributable`: design the skill here, then use an active host's packaging or publishing workflow instead of inventing one inside the skill.

Portable describes the semantic core, not a guarantee that one package installs unchanged everywhere. Do not claim cross-platform package compatibility without named targets and evidence for each. Do not copy remote metadata or folder conventions over a local contract. If multiple target platforms disagree, preserve a portable core and isolate host-specific additions.

## Design the package

Specify or create the minimum useful package, according to the selected mode:

- `SKILL.md`: trigger-bearing metadata, core workflow, critical decisions, and resource routing;
- `references/`: details that are needed selectively and would otherwise bloat the main file;
- `scripts/`: deterministic, fragile, or repeatedly reimplemented execution;
- `assets/`: templates or resources consumed by outputs;
- host-specific metadata: only for an identified target profile and outside portable core instructions when possible.

Match instruction precision to workflow risk:

- use flexible prose when several approaches are valid;
- use explicit patterns or parameterized scripts when a preferred method exists;
- use narrow deterministic steps when order, safety, or reproducibility is fragile.

Keep always-loaded repository guardrails in `AGENTS.md` or the platform equivalent. Use skills for on-demand procedures, deeper domain knowledge, and reusable execution resources.

### Write `SKILL.md`

- Follow the target platform and repository frontmatter contract; for this repository's portable default, use `name` and `description` only, then keep host-required adapters separate.
- Use a short kebab-case name and match the folder name when the local contract requires it.
- Front-load the job and important trigger terms in the platform's active trigger fields, including `description` when supported; include negative boundaries when adjacent skills could match.
- Describe activation in metadata and execution in the body.
- Keep the body procedural and imperative.
- Link every reference directly and say when to read it.
- Avoid redundant guidance between `SKILL.md` and references. Preserve compact
  critical rules needed for independent use; do not introduce undeclared
  cross-package dependencies solely to remove repetition.
- Keep examples only when they resolve a real ambiguity.

### Declare trust and side effects

When the skill uses scripts, tools, authentication, networks, or external writes:

- name required dependencies and permissions;
- distinguish read-only actions from mutations;
- state consequential side effects and safe verification;
- avoid embedding credentials or environment-specific secrets;
- include failure, cleanup, or rollback guidance when the workflow can leave partial state.

Test representative bundled scripts by running them. If execution is unavailable or unsafe, report that limitation rather than implying success.

## Validate proportionally

Use [references/skill-validation.md](references/skill-validation.md) when triggers, workflow meaning, resources, dependencies, or assumptions change. Distinguish activation from post-selection instruction behavior, static prediction from observed runs, and generic harnesses from target-host contexts.

For multi-skill audits in this repository, use [references/inventory-trigger-evals.md](references/inventory-trigger-evals.md) to check high-risk routing boundaries.

Use [references/quality-checklist.md](references/quality-checklist.md) before finalizing a new or substantially revised skill. For a report-only audit, use it to organize findings without editing.

## Complete by mode

- `design`: the contract, trigger boundaries, package map, side effects, and validation plan are implementation-ready without changing files.
- `new`: package and required registration or documentation updates exist, trigger surface and workflow are actionable, resources are validated proportionally, and residual risk is stated.
- `revise`: intended problems are fixed, local conventions are preserved, changed behavior is validated, and the delta is summarized.
- `audit`: findings are explicit, prioritized, actionable, and separated from unverified hypotheses.
- `validate`: exact cases and independent evidence dimensions are recorded, outcomes are classified, and residual risk is clear.
- `optimize-trigger`: the active trigger fields are concise, front-loaded, checked against paraphrases and adjacent negatives, and free of workflow instructions.

For multi-skill audits, report cross-cutting structure first, then routing and composition, context cost, per-skill changes, and validation gaps.
