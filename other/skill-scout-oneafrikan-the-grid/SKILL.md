---
name: skill-scout
description: Scout public agent-skill directories (ranked by installs) and propose new skills for the-grid, deduped against what is wired. Use when the user says "skill-scout", "find new skills" or "what skills should I add".
---

# skill-scout

Find popular Claude skills the-grid doesn't have yet, and propose them — ranked
by install count. **Propose only.** Never add submodules or run `wire.sh`; the
user adds skills via the-grid's normal flow (`git submodule add … && bash scripts/wire.sh`).

## How to run

1. **Gather candidates.**
   - *Ranked web directories:* WebFetch each listing page and pull the ranked rows
     — skill name, popularity number (installs), and source `owner/repo`. Normalise
     install counts ("1.8M" → 1_800_000) so they sort.
   - *Local library submodules:* read them straight off disk — `categories/*.md`
     for awesome-list indexes, or grep `SKILL.md` frontmatter for real collections.
     These have no install count — keep them in a separate, unranked pile.

2. **Load what the-grid already has.** From the repo root (`GRID_DIR`, default the
   repo this skill lives in):
   - Root-level skills: top-level directories containing a `SKILL.md`.
   - Submodule skills: `repos/*/**/SKILL.md` (one or more skill dirs per submodule).
   - Read each skill's `name:` from its frontmatter. Also note the source repo of
     each submodule (`git config -f .gitmodules` or the `repos/<name>` path) so a
     match on **either skill name or source repo** counts as "already have it".

3. **Dedupe.** Drop any candidate whose skill name OR source repo the-grid already
   carries. Matching is case-insensitive; compare on the bare skill name
   (ignore `owner/` prefixes) and on the `owner/repo` source.

4. **Rank and propose.** Sort the ranked-directory survivors by install count,
   descending. Present the top ~15 as a table:

   | Skill | Installs | Source (owner/repo) | Why it fits the-grid |
   |-------|---------:|---------------------|----------------------|

   For "Why it fits", write one honest line covering fit for a developer workflow
   (dev workflow, debugging, git, planning, testing, infra/ops). If a candidate
   is a poor fit, say so plainly rather than inventing a reason — or omit it.

   Then, **separately**, surface a handful of relevant picks from the local index
   (`repos/voltagent`) grouped by category — no install column, since it isn't
   ranked. Flag that these are OpenClaw-ecosystem skills worth a manual look, not
   ranked recommendations.

5. **Hand off, don't act.** End with the exact commands the user would run to add
   any they pick, but **do not run them**:

   ```bash
   git submodule add <repo-url> repos/<name>
   git submodule update --init
   bash scripts/wire.sh
   ```

## Notes

- "Based on installs" means the directory's own popularity ranking — we don't
  recompute it. If a source has no popularity signal, it doesn't belong here.
- Skills already in the-grid via a submodule (e.g. `repos/anthropic/skills/*`,
  `repos/gstack/*`) must be deduped by **source repo** too — a popular skill from
  `vercel-labs/skills` is "new" only if that repo isn't already a submodule.
- Keep the proposal short and skimmable. The user decides; this skill only scouts.

## Sections
Read a section only when its condition applies; do not preload them.
- sections/sources.md: read when gathering candidates (step 1)
