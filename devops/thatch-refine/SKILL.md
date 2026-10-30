---
name: thatch-refine
description: Classify the current project (audience, lifecycle, surface) and refine a plan under that type's requirements. Entry point for the thatch-refine-* family. Use when the user asks to refine a plan, runs /thatch/refine, or when a plan is about to be implemented and the project type should shape the refinement bar. For a bare "refine this plan" request, load this skill rather than thatch-plan-refinement directly - the router picks the type and applies its delta on top of the core loop. Deep-mode triggers in the core skill are binding; a type delta relaxes round counts, never mode selection.
---

You are the entry point for project-type-aware plan refinement. The core
refinement loop (draft, fresh-context reviewer, revise, consensus) is the
same everywhere; it lives in `thatch-plan-refinement`. What changes by
project type is the bar: which lenses matter, what the plan must contain,
how much documentation is owed, and when skipping refinement is honest.

## The types

| Type | Governing value | Skill |
|------|-----------------|-------|
| `team-app` | Coordination and consistency promote org velocity | `thatch-refine-team-app` |
| `personal` | Freedom to experiment; low coordination cost | `thatch-refine-personal` |
| `shared-lib` | API hygiene; never foreclose caller options | `thatch-refine-shared-lib` |
| `spike` | Answering a question cheaply, not producing code | `thatch-refine-spike` |
| `infra` | Blast radius across pipelines and environments | `thatch-refine-infra` |
| `oss-contribution` | The maintainer's design authority | `thatch-refine-oss-contribution` |

## Classification

Classify on three axes, then pick the type whose requirements this plan
must satisfy. Classify **the change**, not just the repo: a personal repo
gaining a published API is a `shared-lib` plan for that change, even if the
repo is `personal` overall.

**Audience** - who reads and maintains this code.

- Solo: one contributor in git history, no CODEOWNERS, no required reviews.
- Team: CODEOWNERS, CONTRIBUTING.md, required PR review, multiple regular
  authors.
- Public: published package (npm/PyPI/etc. metadata, `publishConfig`), or
  consumers outside the repo you cannot enumerate.

**Lifecycle** - what this code owes anyone.

- Production: protected main, CI gates, deploy configuration, semver
  discipline.
- Experimental: active WIP, churny main, thin or absent tests.
- Throwaway: a question wearing a repository.

**Surface** - what the change lives in.

- Application: end-user or service code with no downstream importers.
- Library: exported API that other code imports and keeps working against.
- Infrastructure: CI, Terraform, k8s manifests, build and deploy config.

Signals to gather (all cheap and read-only): `git log --format="%an" |
sort -u | head`, presence of CODEOWNERS / CONTRIBUTING.md / required
review config, package.json `private` and `publishConfig` fields, the
publishing config of the relevant ecosystem, presence of `.github/workflows`,
`terraform/` or k8s manifests, and what the package exports. Do not
over-invest here; the classification should cost a minute, not a research
pass.

## Procedure

1. If the user named a type explicitly (for example `/thatch/refine
   shared-lib`), skip classification and use it.
2. Otherwise gather the signals above and pick the type.
3. State the classification in one line and why, and let the user override.
   A wrong classification silently changes the requirements, so the user
   sees the pick before it takes effect. When the signals conflict or are
   too thin to pick, ask instead of guessing.
4. Load `thatch-plan-refinement` (the core loop) and the type's skill.
5. Run the core loop with the type skill's deltas applied. Where a delta
   and the core skill disagree, the delta wins; that is its whole job.
   One exception: mode selection. A delta relaxes round counts, skip
   thresholds, and plan sections. It never turns off deep mode. When a
   deep-mode trigger in `thatch-plan-refinement` is met (shared
   persistent state, many files or hosts, a new abstraction, table, or
   contract, or the user asks for depth), the lens fan-out runs
   regardless of type.

If no type fits (the repo serves a niche the table misses), run plain
`thatch-plan-refinement` and say that the requirements are the generic
ones.

## Relationship to other skills

- **`thatch-plan-refinement`** - the core loop. Always loaded; the type
  skills only modify it.
- **`thatch-coding-workflow`** - the procedure skill for executing the
  refined plan. Refinement ends where it begins.
- **`thatch-clear-writing`** and the writing skills - several type skills
  make reader-facing documentation a plan deliverable. Draft that text
  under the writing skills' contracts, not this one's.
