---
name: skill-architect
description: Design, create, review, or refactor reusable Agent Skills (SKILL.md). Use when turning a repeatable workflow into a skill, assessing an existing skill for clarity and safety, or improving its structure, guardrails, supporting resources, and maintainability. Not for executing the workflow described by a target skill.
---

# Skill Architect

Design useful, maintainable Agent Skills and improve existing ones without
introducing complexity for its own sake. A review may correctly conclude that
no change is needed.

## 1. Shared preparation

1. Determine the requested operation:
   - **Create:** Design and implement a new skill.
   - **Review:** Assess an existing skill; propose improvements without editing.
   - **Refine:** Review and implement justified changes to an existing skill.
   If unclear, infer from the request; do not treat a request for assessment as
   permission to rewrite files.
2. Identify the target agent/runtime, user-selected skill library, repository
   conventions, and allowed file changes. Prefer the user's configured global
   library (for example `~/.agents/skills/`) over copying reusable skills into
   each project. Do not assume every agent reads the same global paths.
3. Inspect relevant instructions, nearby skills, existing documentation, and
   actual resources before choosing a layout. For an existing skill, read its
   `SKILL.md` and the references, assets, scripts, and guidance it depends on.
4. Establish the intended outcome, typical invocations, non-goals, source of
   truth, side effects, and required permissions. Use supplied examples; infer
   ordinary details where safe rather than asking many setup questions.
5. Check whether a reusable skill is warranted. A short global policy,
   project instruction, template, or ordinary script may be simpler. If so,
   explain that choice rather than manufacturing a skill.

## 2. Shared design criteria

Apply these criteria to both creation and review. Focus on material effects on
correctness, safety, repeatability, usability, or maintenance cost.

- **Triggering:** A distinct name and description state what the skill does
  and when it applies. Avoid catch-all descriptions and accidental invocation
  for unrelated tasks.
- **Responsibilities:** Separate global conventions, reusable methodology,
  project-specific decisions, executable tests, and generated artifacts.
  Respect existing sources of truth and neighbouring skills' responsibilities.
- **Workflow:** Put common preparation and selection rules before mode-specific
  operations. Share admission, completion, and reporting rules instead of
  duplicating them across modes.
- **Formatting:** Use `###` headings for meaningful subsections within
  `##` sections when they improve readability, especially in lengthy
  numbered workflows. Avoid unnecessary heading depth or fragmentation.
- **Judgment vs. determinism:** Give criteria for open-ended analysis. Specify
  exact commands, assets, or scripts only where repeatability, safety, or a
  fragile operation warrants them. Never make speculative examples universal.
- **Guardrails:** Define scope, authority, important invariants, allowed
  mutations, preservation rules, escalation, and stopping conditions in
  proportion to the task's risk.
- **Documentation hygiene:** Name canonical artifacts, preserve user edits and
  stable identifiers, avoid competing records, and make repeated runs converge
  rather than accumulate duplicates.
- **Modularity:** Keep routing and critical rules in `SKILL.md`. Use focused
  `references/` for substantial conditional guidance, `assets/` for reusable
  output templates, and `scripts/` for worthwhile deterministic operations.
  Add no directory or dependency without a concrete need.
- **Portability:** Keep the main workflow agent-, OS-, and language-neutral
  where practical. Isolate genuinely platform-specific procedures. Verify
  external tools and paths before instructing an agent to use them.
- **Interaction cost:** Do not require developer babysitting for routine
  decisions. Escalate only consequential ambiguity or actions requiring
  authorization. Keep outputs concise and actionable.

## 3A. Create a skill

1. Define its contract: purpose, trigger and counterexamples, inputs, outputs,
   normal path, optional modes, side effects, and success criteria.
2. Choose the smallest viable design. Start with a single `SKILL.md`; add
   supporting files only when they reduce duplication, improve reliability,
   or keep conditional material out of the normal reading path.
3. Write valid Agent Skills frontmatter with a lowercase hyphenated `name`
   matching the folder and a discriminating `description` explaining what
   the skill does and when to use it. Follow the applicable specification.
4. Implement the workflow using the shared criteria above. Provide enough
   instruction for another agent to act, without repeating basic model
   knowledge or prescribing arbitrary scaffolding.
5. Follow the surrounding repository's concise README and naming conventions
   when they exist; do not create optional metadata or template files merely
   for symmetry.
6. Create only requested or necessary files. Do not modify unrelated agent
   configuration, install dependencies, or perform external actions without
   appropriate authorization.

## 3B. Review or refine a skill

1. Inventory the skill's actual contract, entry point, branches, referenced
   resources, produced artifacts, integrations, and write operations.
2. Compare the implementation with the shared criteria and realistic usage.
   Distinguish demonstrated weaknesses from preferences or hypothetical risks.
3. Classify conclusions as:
   - **Keep:** Sound choices worth retaining.
   - **Improve now:** Specific defects, ambiguity, duplication, or hygiene
     issues with material consequences.
   - **Defer:** Optional complexity without current evidence of value.
4. Synthesize findings before proposing changes. When several
   improvements interact, look for a coherent design that
   addresses them together rather than independently:
   - Identify shared responsibilities scattered or duplicated
     across workflows, modes or supporting files.
   - Consider consolidating common preparation, decisions and
     completion rules while keeping specialised paths focused.
   - Compare local corrections with an integrated refactor.
     Prefer the arrangement that best preserves existing
     behaviour while improving clarity and maintainability.
   - Seek opportunities where one structural change resolves
     multiple findings or removes incidental complexity.
   - Do not restructure solely for symmetry or modularity;
     require a concrete benefit proportionate to the change.
5. Choose the least disruptive outcome: **no change**, **focused edits**, or
   **restructure**. Do not equate a longer or more modular skill with a better
   one. State the tradeoff if restructuring is warranted.
6. In Review mode, report the assessment and proposed edits without changing
   files. In Refine mode, implement only justified changes within the agreed
   scope; preserve existing user choices, manual content, public interfaces,
   paths, and artifact formats unless changing them is necessary and permitted.
7. If reorganising, update relative links and dependent documentation. Avoid
   breaking consumers of an existing skill solely to make its layout cleaner.

## 4. Validation and completion

1. Check required metadata, directory names, links, referenced resources,
   example commands, and absence of unfinished placeholders. Use an available
   Agent Skills validator if present; do not install one solely for this task.
2. Test the decision process against at least one realistic invocation and a
   case where the skill should *not* apply. For multi-mode skills, sample each
   materially different mode when practical. Do not claim tests were run if
   they were only reasoned through.
3. For a rewrite, compare before and after: ensure intended behaviours remain,
   guardrails are not weakened, existing data is preserved, and repeat use will
   not cause needless churn.
4. Stop when the requested behaviour and meaningful risks are addressed.
   Avoid polishing, splitting, or extending the skill without a concrete gain.
5. Report the decision (create, keep, focused edit, or restructure), the main
   reasons, files created or changed, checks actually performed, and any
   important remaining uncertainty. Do not dump the whole skill again unless
   requested.
6. When practical, exercise the skill in a representative environment rather
   than relying solely on inspection. Test new or changed scripts by executing
   representative cases. Distinguish observed results from reasoned checks;
   do not introduce an evaluation framework without need.


## Documentation handoff (secondary)

Keep user-facing documentation aligned without making it a separate workflow:

- **Create:** When the library uses READMEs, produce a concise skill-local
  `README.md` and a short entry for the library's root `README.md`. Cover
  purpose, invocation, outputs, and notable requirements; omit workflow detail.
- **Review:** Report material README omissions or drift without editing files.
- **Refine:** Update READMEs only when usage, behaviour, or file layout changes
  materially.
- Follow existing style, preserve unrelated content, and derive descriptions
  from the actual `SKILL.md`. If root README editing is outside scope, provide
  an insertion snippet instead. Do not add README files just for symmetry.
- **Final hygiene:** Run `prompt-residue-sweep` on all created or materially
  revised human-readable artifacts. Report clear findings and apply only minimal,
  meaning-preserving corrections when editing is authorized.
