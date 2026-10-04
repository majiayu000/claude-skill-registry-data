---
name: tune-agent-docs
description: >
  Reviews every markdown file in a repository that steers an AI coding agent as one corpus, then
  tightens them. The corpus covers CLAUDE.md, AGENTS.md, GEMINI.md, `.cursor/rules/*.mdc`,
  `.clinerules`, `.windsurfrules`, `.github/copilot-instructions.md`, Kiro `.kiro/steering/*.md`,
  and files like them. Use when the user wants to audit, tune, reconcile, or clean up the
  instructions a repo gives its AI agents, or asks why an agent keeps missing, contradicting, or
  burning tokens on its own steering docs. Use it even when the user names one file, because the
  value comes from reading that file next to its neighbors. Checks terminology consistency,
  front-loaded directives, the size of each doc against the stated limit of its format,
  always-loaded content the harness can scope, duplicated guidance, no-op instructions, and the
  degrees of freedom of each instruction. For one `SKILL.md` on its own, use review-skill instead.
argument-hint: "[path or glob, optional. Defaults to the whole repo]"
allowed-tools: [Read, Glob, Grep, Edit, Write, AskUserQuestion]
---

# Tune Agent Docs

Whatever agent starts work in a repo reads that repo's AI-steering docs, and often loads several of them into one context window. A root `CLAUDE.md` is rarely the only text an agent takes as instruction. The agent pays a silent tax on every run when these docs disagree. It pays the same tax when they use different words for one thing, bury their point, or demand more rigor than the task needs. This skill treats every steering doc in the repo as one corpus.

Work in two phases: **critique first, edit second**. Build the full picture, present the findings, and only then touch a file.

## Find the corpus

Use `Glob` for the conventions that a harness recognizes today. Read `references/steering-formats.md` for the current list, and for the frontmatter and inclusion rules of each format. The conventions start with `CLAUDE.md` and `CLAUDE.local.md`, including nested per-directory copies and `.claude/rules/**/*.md`. They continue with `AGENTS.md`, `GEMINI.md`, `.cursor/rules/**/*.mdc`, and `.cursorrules`. They finish with `.clinerules` or `.clinerules/**/*.md`, `.windsurfrules` or `.windsurf/rules/**/*.md`, `.devin/rules/**/*.md`, `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, and `.kiro/steering/**/*.md`. Where a harness has a local or gitignored variant, include it next to its checked-in counterpart. That pair is a common duplication site, so include both files.

Then follow every pointer that a doc in the corpus makes to another markdown file. A pointer is a "See `docs/x.md` for..." link, an `@import`, or a relative link in a "Where things are" or "further reading" section. A steering doc that tells the agent to consult another file delegates its steering to that file, whether or not the target matches a convention. Pull the target in without asking, because the pointer is the corpus doc that vouches for it.

Then sweep the remaining `.md` files in the repo. Look for files that read as agent-directed but match no known convention and no pointer. The signs are imperative language addressed to "you", "the agent", or "Claude", and frontmatter with an inclusion-like key. List every candidate that this sweep finds. Put the full list to the user with `AskUserQuestion` before you fold any of it in. Do not shorten the list to the files you are unsure about and read the rest in silence. The user decides the scope. An unfamiliar file that turns out to be a changelog or a design doc must not get graded as steering prose.

Read every file in the corpus in full, including every file that a pointer pulled in. A line count or a partial skim is not a read, because the findings live in how these docs relate to each other.

## Load the lenses

- **The standards**: find the authoring conventions that govern this corpus. Look for a `CLAUDE.md`, a `CONTRIBUTING.md`, a docs style guide, a skill-authoring style guide, or an equivalent file. Apply them to every doc in the corpus, not only to the docs they were written for. A repo that holds its `SKILL.md` files to a standard holds its `AGENTS.md` to the same one. A convention the repo settled is settled, so do not raise it as a finding. Take the conventions only from the repo under review. Another repo's `CLAUDE.md` that sits in your context governs its own scope, and so do the user's global conventions.
- **Cross-harness format knowledge**: `references/steering-formats.md` holds the frontmatter fields, the inclusion or scoping mechanism, and the size guidance for each recognized format, taken from the documentation of each vendor. It also holds format-agnostic principles from Anthropic's Skill authoring guidance. Read it once per review. These formats change, so never rebuild the list from memory.

## What to check

- **Token budget**: this is the largest lever a steering doc has over what an agent pays before it does real work, so check it first. Compare the length of each doc against the ceiling of its own format in `references/steering-formats.md`. The ceiling is 200 lines for `CLAUDE.md`, 500 lines for `SKILL.md`, and a per-character cap for Windsurf. A doc under its ceiling is a starting point, not a pass. Length costs tokens whatever its cause, so every line in a short doc still owes a justification against the checks below. Then find content that loads unconditionally through `alwaysApply: true`, `inclusion: always`, or an unscoped `.claude/rules/*.md`, and that matters for one file type or directory alone. Such content belongs in the conditional-loading mechanism of the harness. A doc split into Claude Code `@import` statements is easier to navigate but the same size, because imports still load in full. Never count that split as a token-budget fix.
- **Duplication**: one meaning, one home. Compare guidance by what it *means*, not by string match. Two docs that say one thing in different words duplicate it as fully as two that say it word for word. Paraphrase is the common case, because different hands wrote the docs at different times. The same defect runs inside a single doc, where one rule restated three sections apart reads as three rules. Compare each checked-in doc against its local counterpart. Duplication pays its token cost twice today, and it becomes a contradiction the day one copy gets edited. Prefer one canonical doc plus a pointer or an import over a second copy. Put the surviving copy at the narrowest scope that still covers everywhere the guidance applies. Where a restatement is one idea circled three times, the repair is often a single word that the model already carries priors for. Repeat that word as a term instead of re-explaining the idea in a sentence.
- **No-ops**: an instruction the model already follows by default changes nothing and still costs context every session. Examples are "write clean code", "follow best practices", "be careful when editing files", and "think before you change things". Steering docs collect these because adding a line feels free. Test each sentence on its own against one question: does an agent that never saw this doc behave differently? Judge sentence by sentence, not section by section, because a live section carries dead sentences. When a sentence fails the test, delete the sentence. Do not rewrite it tighter. A reworded no-op is still a no-op, and the reach for a rewrite is what leaves these docs long. Cut hard here. This is usually the largest single cut available.
- **Structural fit per harness**: once a token-budget or leanness finding calls for a split or a narrower scope, judge the fix against what the format itself supports, per `references/steering-formats.md`. The available mechanisms are a nested `CLAUDE.md`, a glob-scoped `.mdc` rule, and a Kiro `fileMatch` steering file. Where the harness has no such mechanism, report the size as a leanness finding instead of recommending a mechanism the harness cannot use. Also flag content that is a multi-step procedure rather than a standing fact. An always-loaded doc holds what is true every session. A workflow belongs in a skill that loads on demand, or in a path-scoped rule.
- **Consistent terminology**: across the whole corpus, one role, tool, or convention carries one name. Hunt synonym drift, such as `the agent` against `Claude` against `the assistant`, `skill` against `capability` against `workflow`, and `worktree` against `workspace`. A term used two ways inside one doc is the same defect at a smaller scale.
- **Front-loading**: each instruction must open on its actionable verb or keyword, with no throat-clearing in front of it. This check reaches past `description` fields. A bullet, a header, or a frontmatter `description` that leads with context before the directive makes a skimming agent miss the point. It also weakens the retrieval match of the harness. Keep this check separate from the *leading word* in the Leitwort sense, which is a compact pretrained concept that the agent thinks with. That belongs to the duplication repair above.
- **Degrees of freedom**: match the specificity of each instruction to how fragile the thing it governs is. An exact, low-freedom script constrains an agent that needs to reason about a judgment call. Loose, high-freedom prose invites improvisation around an exact operation that must run in order.
- **Negation**: a prohibition names the banned behavior into the agent's context, where it competes with the ban. A doc built from `never`, `do not`, and `MUST NOT` walls must state the behavior it wants instead. Keep a prohibition for a guardrail that has no positive phrasing, and pair even that one with what to do in its place.
- **Leanness and staleness**: cut what the agent can derive by reading the codebase itself, such as directory layouts, dependency lists, and architecture overviews. Keep what it cannot derive, such as pitfalls, rationale, and conventions that differ from the defaults of the tool. This cut differs from the no-op check: a derivable fact is true but free to look up, and a no-op is behavior the model already has. Flag time-boxed conditionals such as "until the migration finishes, do X", because they go stale in silence. A dated fold or an old-patterns section ages better than a conditional that still sounds live.
- **Frontmatter validity**: check the frontmatter of each doc against the real schema of its format. Three examples of a violation follow. The first is a Kiro `inclusion` value outside `always`, `fileMatch`, and `manual`. The second is a Cursor `.mdc` file that omits the field its activation mode depends on. The third is a `SKILL.md` `name` that breaks the character or charset limit.

## Resolve conflicts by scope, not by asking

When two docs give contradictory guidance for one thing, resolve it the way these harnesses layer context at runtime. The doc scoped to the narrower area wins for the area it covers, over a repo-wide doc that always loads. A narrower doc is a nested `CLAUDE.md`, a rule scoped by `fileMatch` or `paths`, or a glob-scoped `.mdc` file. Fall back to `AskUserQuestion` only when both sides sit at the same scope and precedence gives no signal. That case is a real tie, not a shortcut around judgment.

## Present findings, then apply

Open with a one-line verdict. Then list the findings ranked by severity, not grouped by check:

- **Blocking**: an active contradiction between docs, an instruction that will make the agent do the wrong thing, or a doc past a hard format limit. Past a hard limit, such as a Windsurf character cap, the tail is truncated in silence and never loads.
- **Important**: terminology drift, a buried directive, or a no-op instruction. It also covers an oversized or always-loaded doc that its harness can scope, and one meaning kept in two places or restated inside one doc. It covers a prohibition wall with no positive target, miscalibrated degrees of freedom, and a convention violation.
- **Nit**: cosmetic polish.

Tag each finding with its dimension, its exact file, and its line. Then offer to apply the findings. Offer three choices: every blocking and important finding, everything, or a subset the user picks. Edit the files directly. A terminology fix or a front-loading fix must land in every occurrence in every file of the corpus. A partial rename leaves the corpus less consistent than before.

## Before you finish

Re-read the diff as a skeptical teammate, and look for these six errors:

- A rename that missed a nested `CLAUDE.md` or a nested rule file.
- A degrees-of-freedom fix that overcorrected into the opposite miscalibration.
- A "contradiction" that was two docs correctly scoped to different areas, now wrongly collapsed into one.
- A scoping fix that narrowed the `paths`, `globs`, or `fileMatchPattern` of a rule past the areas that need it. The agent then stops seeing guidance it relies on.
- A no-op that got reworded instead of deleted, so the finding was reported and the line survived.
- A paraphrase collapsed onto the broader of the two docs, so the surviving copy now applies where the guidance never did.
