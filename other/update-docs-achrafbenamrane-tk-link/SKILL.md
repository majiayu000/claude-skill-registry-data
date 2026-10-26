---
name: update-docs
description: Close the documentation loop after a feature ships — distill the spec into the living feature doc, update CUJs and indexes, mark the spec shipped — or run an audit to reconcile the docs tree with reality. Use after merge, when the user says "update docs", "docs pass", "close out the feature", "sync docs", or when docs have drifted. Subsumes the old /sync-docs command. Stale docs poison every future agent session, so this is maintenance of the harness itself.
argument-hint: [spec number/slug, or "audit" for a drift check]
allowed-tools: Read Write Edit Glob Grep Bash(npm run docs:lint*) Bash(git log*) Bash(git diff*)
---

## Task

For **$ARGUMENTS**:

### Mode A — close out a shipped spec (default)

1. **Distill, don't copy.** Read the spec folder + final diff. Write/update `docs/product/features/<slug>.md` (create the `docs/product/features/` dir + a short `README.md` index if absent, and link it from `docs/index.md`): what it does (user terms), how it works (the non-obvious 20%), dated decisions & gotchas, CUJs covered. The feature doc is what future changers ground on — capture what they'd otherwise rediscover painfully, omit what the code says plainly.
2. **Update the registries:** feature index in `docs/product/features/README.md` · CUJ table in `docs/quality/critical-user-journeys.md` (new/changed journeys with spec + Maestro flow names) · spec status → `shipped` in `specs/README.md` · `docs/index.md` if files were added.
3. **Check for ripples:** did this work invalidate any statement in `docs/architecture/*` or `docs/conventions/*`? Fix in place; if a _decision_ changed, that's a superseding ADR, not a silent edit. Check code↔doc sync rules (e.g. tokens between `tailwind.config.js` and `src/shared/theme/colors.ts`).
4. **Validate:** run `npm run docs:lint` (links + orphans + taste). Commit as `docs(<slug>): close out spec NNN`.

### Mode B — `audit` (drift check, folds /sync-docs)

Sweep for lies: feature docs vs actual slices (`ls src/features`), CUJ table vs `.maestro/flows/`, specs index vs spec folders' real status, `docs/index.md` vs files on disk, AGENTS.md docs map completeness, dead links (`npm run docs:lint`). Cross-check the last changes (`git log --oneline -20` + `git diff main --stat`) against `docs/architecture`, `docs/conventions`, AGENTS.md, README. Report a fix-list ordered by how badly each lie would mislead an agent, then fix the approved ones. End with any `HARNESS:` proposal.

Tone rules for all docs: short, imperative, present tense, no marketing. If a doc passes 200 lines, split it and re-index.
