---
name: compare-competitors
description: >-
  Load this skill when putting analysed competitors side by side with our own work: one
  comparison.md, also as HTML, by capability, strengths, and positioning. Trigger on "compare them
  with us", "how do we stack up", or after several competitors were analysed.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
compatibility: >-
  Checking a competitor report needs uv (https://docs.astral.sh/uv/), which runs
  scripts/artifact.py with pydantic. Without it each report is read unchecked and the reply says so.
---

# Compare competitors

Write `.agents_workspace/competitor-analysis/comparison.md`, comparing every analysed competitor
with our work, and render it as `comparison.html` beside it. Done means a reader can see in under a
minute how the options differ and where each one has a gap, every cell traces back to a
per-competitor report or a command run on our side, and the HTML page carries the same content as
the Markdown.

## Procedure

1. **Gather the inputs.** Read every per-competitor report in
   `.agents_workspace/competitor-analysis/`, per `references/competitor-report-schema.md`. A stem
   with a `<slug>.yaml` is a `competitor-report/v2` report: check it first with
   `uv run --script ${CLAUDE_SKILL_DIR}/scripts/artifact.py check <slug>.yaml`, then read it by
   key. On exit 1, stop and report the errors, because a comparison built on a broken report
   carries the error into every cell, unless the only error is a stale `.md`, when you run the same
   command with `render` and go on. On exit 2 or 3, without uv, or when the call is denied, read
   the YAML unchecked and say so in the reply. A `.md` with no `.yaml` beside it is a `v1` report
   only when it has `schema: competitor-report/v1` or opens with a `# Competitor analysis:` title,
   because most `v1` reports have no `schema:` line and the folder also holds `comparison.md`,
   a `CLAUDE.md` and side-by-side notes. Skip any other `.md`. When a competitor the user named has
   no report yet, invoke the Skill tool with skill="ceh-competitor-analysis:analyze-competitor"
   for it first. Do not compare from memory.
2. **Measure our side fresh.** Count our components with commands (`ls`, `find`, `wc -l`) rather
   than copying numbers from our own README, which drifts. Note the date.
3. **Pick the dimensions.** Start from the fixed rows under Output. Add rows for any axis on which
   the competitors genuinely differ, such as philosophy, host platform, or invocation model. Drop a
   row on which all of them are identical.
4. **Build the capability inventory.** Make one row per capability, such as review, testing,
   security, or docs, and one column per repo, ours last. Put each repo's components in its cells,
   with `—` where it has nothing. Choose the capability rows from the union of everything every
   repo ships, so that a gap on any side is visible.
5. **Score each capability.** Give every repo a 1-to-5 score per capability row, where 1 is
   nothing and 5 is the strongest seen across the repos, and put the evidence in the same cell:
   the per-competitor report section, file, or command behind the score. A score with no evidence
   is `?`, never a guess. Add no total or average: a composite hides the gaps the table exists to
   show.
6. **Write the comparison** in the shape under Output.
7. **Render the HTML page.** Invoke the Skill tool with skill="ceh-ui-design:design-ui" for the
   theme and its review pass, with the same theme file the per-competitor pages link
   (`themes/<theme>.css`, Meridian unless the user names another). Build `comparison.html` by
   filling `${CLAUDE_SKILL_DIR}/assets/report-page.html`, keeping its COMPARISON-ONLY blocks:
   the hero from the positioning line and up to three headline counts, one table panel each for
   "At a glance", "Inventory by capability", and "Scores", and one expandable card per repo from "Where each
   one is strongest". Link each competitor's `.html` page in the top bar. The page may fold detail
   into cards but adds no claim the Markdown lacks.

## Rules

- **This is a comparison, not a roadmap.** Do not rank what to adopt or write a "next steps"
  section unless the user asks for one. The per-competitor reports already carry the adoption
  tables.
- **Treat our work the way you treat a competitor.** Name our weaknesses as plainly as theirs. A
  comparison that flatters us is useless for deciding anything.
- **Every cell must trace** to a per-competitor report, a file, or a command. When the reports
  disagree on a number, rerun the measurement rather than picking one.
- **Use the same word for the same concept across columns**, such as "skill", "agent", and "hook",
  even where a competitor uses its own term. Note the mapping once below the table.
- **Write for a glance first.** Use tables first, keep each cell to a few words, and keep each
  strongest and weakest entry to one line. No mermaid diagrams.

## Output

`comparison.md` fills `assets/competitor-comparison.template.md`, per
`references/competitor-comparison-schema.md`.

## Hands off to

- Invoke the Skill tool with skill="ceh-ui-design:design-ui" to render the HTML page (step 7).
