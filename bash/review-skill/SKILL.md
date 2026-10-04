---
name: review-skill
description: >
  Reviews, audits, and tightens a skill that already exists. Reads a `SKILL.md` for its
  triggering, scope, structure, prose, and domain accuracy, ranks the findings by severity,
  and applies them when the user approves. Use when the user wants to review, critique,
  audit, lint, tighten, or improve a skill they already have, fine-tune a skill they just
  drafted, or asks why a skill is too verbose, does not trigger, or feels wrong. Use it also
  when the user pastes a SKILL.md and asks for feedback. This skill reads a skill. It does
  not measure one: eval runs, benchmarks, automated description optimization, and packaging
  are outside its scope.
argument-hint: "[skill name or path to a SKILL.md]"
allowed-tools: [Read, Glob, WebSearch, WebFetch, Bash, Edit, Write]
---

# Review Skill

Audit a skill against the way good skills behave, then tighten it. Name what weakens the skill, and fix those things when the user agrees.

This skill is the static half of skill review. If the user wants a measured trigger rate or eval-graded iteration, say that the work needs an eval loop. Do not build one here. Hand off to a skill-creation skill when the session has one.

Work in two phases: **critique first, edit second.** Never rewrite the skill before the user reads the findings and picks what to apply.

## Resolve the target

Take the skill from `$ARGUMENTS`. The argument is a skill name or a direct path. For a name, glob `skills/**/<name>/SKILL.md` first, so a repo that groups its skills under plugin or category directories still resolves. Then try the installed `~/.claude/skills/<name>/SKILL.md`.

With no argument, review the skill in progress. That is the `SKILL.md` edited most recently in this session, or the one that shows in `git status`. If two or more files fit, ask the user which one to review.

Read the whole bundle, not the `SKILL.md` alone. Note any `scripts/`, `references/`, `assets/`, and `evals/` directory. The presence of one, or its absence, is itself a finding.

## What to review

**The standards**: before you walk the dimensions, find the authoring conventions that govern this skill. Look for a `CLAUDE.md`, a `CONTRIBUTING.md`, a skill-authoring style guide, or an equivalent file. A documented convention overrides a generic dimension below wherever the two disagree. A convention the repo settled is settled, so do not raise it as a finding.

Take the conventions only from the repo that holds the skill under review. Resolve a path under `~/.claude/skills/` to its real target first with `readlink -f`. An installed skill is often a symlink into a source repo, and that repo governs it. When the resolved path sits in no repo at all, review on the dimensions alone. Do not hold the skill to the conventions of the repo your shell happens to sit in. Do not hold it to the user's global conventions either.

Then walk these dimensions and collect concrete findings. Tie each finding to specific lines.

- **Triggering**: the `description` must front-load the leading word of the skill and cover the branches a user will really phrase. It must state what the skill does in the third person, and then state when to use it as "Use when ...", which is the wording that Anthropic recommends. Flag a description that describes its own triggering instead, as in "The trigger covers phrasings such as ...". A skill with `disable-model-invocation: true` is the exception, because Claude cannot load it: that description must say that the skill is user-only, and tell Claude to suggest its command. Flag gaps, and flag overlap that will trigger this skill in place of a neighbor. This is a smell test that you read off the page. A measured trigger rate needs an eval run, and this skill does not do eval runs.
- **Scope**: one clear responsibility, plus an honest "do not use for..." boundary where the boundary earns its place. Flag scope creep and overlap with skills that already exist.
- **Domain fidelity**: covered in the next section.
- **Prose and leanness**: the body must read as objective, clear, and lean. Hunt *no-ops* sentence by sentence. A no-op is a line the model already obeys by default, so it costs context and adds nothing. Delete the whole sentence, because a reworded no-op is still a no-op. Collapse restatements: the same meaning in two places costs tokens now, and it drifts into a contradiction the day one copy gets edited. Call out *sediment*, the stale layers that settle because adding feels safe and removing feels risky. Call out *sprawl*, which is length itself, even where every line is live and unique. Recommend that deterministic or repeated mechanics move into `scripts/`, and that bulky reference text moves into `references/` behind a pointer. The body loads on every run, so it must stay legible.
- **Structure and frontmatter**: `name`, `description`, `argument-hint`, and `allowed-tools` must be valid and consistent with each other. Headers must earn their place. No two instructions can contradict each other. Completion criteria must be checkable, not vague.

## Domain fidelity

First decide whether the skill is domain-specific or a generic process skill. A domain-specific skill covers a framework, a cloud service, a methodology, or a business domain. Research only a domain-specific skill, and route the research by the kind of domain:

- For libraries, frameworks, SDKs, CLIs, and cloud services, fetch current documentation with the `ctx7` CLI. Run `npx ctx7@latest library "<name>"`, then `npx ctx7@latest docs <id> "<question>"`. When that CLI is unavailable, fetch the official documentation page with `WebFetch` instead, and take it from the vendor's own domain.
- For methodologies and business or domain concepts, use `WebSearch` and `WebFetch` against reputable primary sources.

Compare the terminology, the definitions, and the recommended patterns of the skill against what you find. Flag anything stale, misnamed, or contradicted by the source. Cite the source for every domain finding, so the user can weigh how authoritative it is. Never correct domain wording from training data alone.

## Present findings, then apply

Open with a one-line verdict. State whether the skill is sound or needs work. Then list the findings ranked by severity, not grouped by dimension:

- **Blocking**: the finding breaks triggering or correctness, or the domain sources contradict it.
- **Important**: the finding is a real weakness, such as scope creep, sprawl, duplication, vague completion criteria, or a convention violation.
- **Nit**: the finding is optional polish.

Tag each finding with its dimension. For a domain finding, name the source you consulted.

Then offer to apply the findings. Offer three choices: every blocking and important finding, everything, or a subset that the user picks. Edit the files directly and show what changed. Proof that the skill now triggers and passes evals is a separate exercise that measures the skill. Say so, and do not imply that this audit established it.
