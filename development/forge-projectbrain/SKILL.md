---
name: forge-projectbrain
description: Generates a top-tier project-specific CLAUDE.md. Use when a project has no CLAUDE.md or a thin/generic one — project brain, onboarding, project identity, hard rules, governance.
---

# Forge playbook — top-tier project-CLAUDE.md generation

## Why this exists
A thin CLAUDE.md that is just a bullet list of file paths gives an agent no real leverage — it doesn't say
what the project actually IS, which of the owner's global rulesets actually apply here, or which rules are
non-negotiable. Deep research on Anthropic's own published best practices (`code.claude.com/docs/best-practices`,
the Agent Skills docs, and independent 2026 field guides) converges on the same verdict: **the worst CLAUDE.md
files aren't empty, they're thorough ones** — bloat dilutes the rules that matter until Claude quietly stops
following them. The gold-standard shape (proven in the AutoWeb project, now formalized against that research)
is a real **PROJECT BRAIN**: a tight five-part core (description, stack+versions, exact commands, architecture,
conventions) + boundaries + pointers to detail docs, environment rules ADAPTED to the project's real tooling,
universal anti-generic guardrails kept verbatim, a real Hard Rules section, and Governance. This skill is the
repeatable METHOD for producing that shape for any Forge project; `forge-bin/forge-projectbrain.cjs` automates it.

## The research this method is built on (cite before you deviate)
- **The five-part core framework**: (1) one-line project description, (2) tech stack **with versions**,
  (3) EXACT build/test/lint/run/deploy commands, (4) architecture as 3-5 key dirs with file:line-style
  pointers (never prose describing a "typical" layout), (5) conventions a linter can't enforce. Plus
  boundaries/off-limits dirs and pointers to detail docs.
- **The prune test** (official Anthropic guidance): for every line, ask "would removing this cause Claude to
  make mistakes? If not, cut it." A bloated CLAUDE.md causes Claude to ignore the instructions that actually
  matter — conciseness is not a nice-to-have, it is the mechanism that keeps the file effective.
- **EXCLUDE, always**: anything derivable from the code itself, standard conventions Claude already knows,
  file-by-file listings, pasted code blocks, frequently-changing information, and "obvious advice" filler
  ("write clean code", "follow best practices"). None of these belong in a generated CLAUDE.md.
- **Imperative language, not hedging**: "Never commit `.env`" beats "we generally prefer not to commit .env".
- **Emphasis discipline**: reserve IMPORTANT/YOU-MUST-style emphasis for the 1-2 truly critical rules
  (honesty, project-isolation) — emphasizing everything is the same as emphasizing nothing.
- **A practical line budget** (guidance, not a hard gate): keep the generated document in the neighborhood of
  ~150-200 lines for a typical project. The verbatim anti-generic guardrails block for website-flavored
  projects is a deliberate, documented exception to that budget (see step 3) — verbatim reuse there is a
  strength, not bloat, because it is the SAME trusted rule every project quotes.
- **KEY INSIGHT — skills/docs are NOT reliably auto-invoked.** Independent evals (Vercel) measured a 56%
  non-invocation rate for progressive-disclosure Skills matched only by a vague trigger description. A Hard
  Rule or an environment-ruleset line is not a Skill — it is always-loaded text — so every rule this generator
  emits must be a sharp, explicit, self-contained imperative ("Apply the frontend-design method before writing
  ANY frontend code"), never a bare pointer like "see the frontend-design skill for guardrails." When a real
  Skill genuinely needs to be referenced, name WHEN it triggers, not just that it exists.
- **`@`-imports buy organization, not context budget.** An `@path` reference inside CLAUDE.md loads
  automatically alongside it at session start (unlike a Skill) — so the generated "Detail docs" pointers are
  honest about that: they are real, but they are not a free lunch, and each imported doc should stay focused.

## The method (five steps)

1. **Detect the real stack — never assume.** Read `package.json` (name, description, scripts, dependencies,
   devDependencies — capturing each framework's LITERAL declared semver range, never a resolved/guessed
   installed version), look for a framework signature (Astro/Next/Vite/React/Vue/Svelte/Angular/Express/
   Fastify/NestJS/Electron), look for an n8n workflow export (`workflows/*.json` with `nodes`/`connections`),
   read real ports ONLY from a literal `--port N` / `PORT=N` in a script or `.env.example`, list up to 5 real
   top-level source directories (excluding build/dependency/tooling noise) with a real entry-file pointer when
   one genuinely exists, and list up to 4 real detail docs (`README.md` + `docs/*.md`) that already exist.
   `forge-projectbrain.cjs::detectStack()` does all of this programmatically; if you're doing it by hand, the
   same discipline applies: only claim what a real file proves — an honest "not detected" note always beats a
   plausible-looking guess.

2. **Select the applicable global ruleset(s) and ADAPT them.** Pick the owner's global ruleset(s) that match
   the detected project type (frontend-website rules for `website`/`fullstack` frontends, n8n rules for
   `automation-n8n`, the domain principles in the owner's own global CLAUDE.md for other types). Rewrite the
   environment-specific subsections (local server / screenshot command / output defaults / domain-specific
   hard rules) to name the project's REAL commands, ports, and file conventions — and flag every adapted line
   `` `[<ProjectName>]` `` (or `` `[<ProjectName> — adapted]` ``) so a reader can tell "this is now true HERE"
   from "this is the generic default". This is exactly what distinguishes AutoWeb's CLAUDE.md (Astro +
   Playwright, `[AutoWeb]`-flagged throughout) from a copy-pasted generic template.

3. **Keep universal guardrails + honesty core VERBATIM.** The anti-generic design guardrails (colors, shadows,
   typography, gradients, animations, interactive states, images, spacing, depth) and the honesty-core
   principle ("never claim a check/test/build ran unless it actually ran") are NOT project-specific — copy
   them unchanged. Do not water them down and do not re-word them per project; verbatim reuse is a strength,
   not laziness — it means every project quotes the same trusted rule (and it is the one deliberate exception
   to the line-budget guidance above).

4. **Emit the five-part core PLUS boundaries and detail-doc pointers.** In order: `## Project identity`
   (name/type/stack+versions/tooling/ports, no prose), `## Commands` (every real script, verbatim — placed
   near the top because it is the highest-ROI content: an agent that knows the real command makes fewer
   mistakes than one that guesses), `## Architecture` (the real key dirs from step 1, never a fabricated
   "typical layout"), `## Conventions` (a linter can't enforce these — tie every bullet to something step 1
   actually detected, never an invented project-specific rule), the adapted environment ruleset from step 2,
   `## Boundaries` (universal off-limits dirs — `node_modules/`, build output, `.git/` — plus this project's
   own `.claude/` when it genuinely exists), and `## Detail docs` (real `@path` imports of the docs found in
   step 1, or an honest "none found yet" note — never a fabricated pointer to a file that doesn't exist).

5. **Emit a real `## Hard Rules` section wired to `FORGE_PROJECT_HARD_RULES.json`, then `## Governance`, and
   SAFE-MERGE the write.** Start from Forge's universal non-negotiables (project isolation, honesty core,
   secrets-in-env, no-auto-push, input validation, file-size discipline — `DEFAULT_HARD_RULES` in
   `forge-projectbrain.cjs`). If `<project>/.claude/FORGE_PROJECT_HARD_RULES.json` exists, merge its `{id,text}`
   entries in (a project can EXTEND the list, never silently override a universal id) — this file is the
   machine-checkable source a future `forge-doctor` pass can read to verify the rules are actually being
   followed, not just documented. Reserve IMPORTANT-style emphasis for exactly `honesty-core` and
   `project-isolation` — every other rule stays a plain, still-imperative bullet. Governance names the real
   Forge memory files (`FORGE_MEMORY.md`, `FORGE_DECISIONS.md`, `FORGE_AGENT_LEDGER.md`,
   `FORGE_TASK_HISTORY.md`), states secrets live in `.env` only, and reiterates never-auto-push / no production
   changes without explicit approval. **Never blindly overwrite an existing CLAUDE.md.** If the target file
   already has Forge-managed markers (`<!-- FORGE-PROJECTBRAIN:BEGIN v1 -->` / `<!-- FORGE-PROJECTBRAIN:END -->`),
   replace only that marked region — everything the owner wrote outside it is preserved untouched. If the file
   exists with NO markers, refuse to write unless the caller explicitly opts into a full overwrite (`--force`) —
   an unmarked file is presumed hand-authored by the owner and must never be silently clobbered.

## Using the companion tool
```
node .claude/forge-bin/forge-projectbrain.cjs detect --dir <projectDir> [--json]
node .claude/forge-bin/forge-projectbrain.cjs generate --dir <projectDir> [--out CLAUDE.md] [--force]
```
`generate` without `--out` only prints to stdout (safe to inspect before writing anything). See
`template.md` in this folder for the annotated structure the generator's output follows, and
`forge-bin/forge-projectbrain.test.cjs` for the real hermetic proof (three project-shape fixtures + the
research-enriched core-framework sections + safe-merge behavior + a mutation-verified Hard-Rules-emphasis and
Architecture-entry-pointer check).

## Hard rules for this skill itself
- Never invent a stack, framework, version, port, directory, doc, or script the real files don't show — an
  honest "not detected" note beats a plausible-looking guess, in every one of the five core sections.
- Never silently overwrite an owner-authored CLAUDE.md that has no Forge markers.
- Every environment-adapted rule must carry a `[<ProjectName>]` flag; unflagged text must be the verbatim
  universal guardrail/honesty-core wording, not a paraphrase.
- Never render an excluded phrase (obvious advice, "write clean code"-style filler) or a pasted fenced code
  block — a generated CLAUDE.md states real facts and real non-negotiables only.
- Reserve emphasis (`**IMPORTANT:**`) for exactly `honesty-core` and `project-isolation`; every other Hard
  Rule is a plain bullet.
- This skill produces documentation/config only — it does not touch secrets, does not deploy, and does not
  register the `projectbrain_generated` event_type itself (the event_type is registered in log-event.cjs;
  the calling Boss/skill step owns the real log call, same doctrine as forge-scout.cjs/forge-capabilities.cjs).
