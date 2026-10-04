---
name: researchforge-start
description: Start or resume a ResearchForge project — explore a research idea or improve a repository with benchmarked experiments. Use when the user wants to begin research, set up ResearchForge, or asks "where was I?" in an existing project.
---

# Start or resume a ResearchForge project

ResearchForge is a local CLI: Claude proposes (queries, syntheses, patches);
the Python engine validates, executes, and records. Every command supports
`--json` — prefer it and read the structured output instead of parsing prose.

## Resume an existing project

Always check state first:

```bash
researchforge status --json
```

The `next_action` field names the exact next command. Follow it — the engine
tracks the pipeline (papers → landscape → hypotheses → contract → baseline →
experiments → validation → shipping) and will not let steps run out of order.
Summarize where the project stands from the JSON counts, then invoke the
matching skill (researchforge-papers, researchforge-baseline, …).

## Start a new project

0. Ask **where** the project should live. ResearchForge is directory-scoped:
   the database, worktrees, artifacts, and dashboard all live under the
   directory you run it in — any folder works, it does not have to be a
   repository you already opened. If the user names a folder (e.g. "do all
   experiments at ~/Desktop/some_new_folder"), either `cd` there or prefix
   every command with `researchforge -C <folder> …`. Confirm the location
   back to the user; `researchforge paths` prints the full map afterwards.
   Commands run in a subfolder of a project walk up to the project root
   automatically (a `Using project at <root>` note appears on stderr).
   Tell the user their project appears in the hub at http://127.0.0.1:9000
   (all projects on the machine, with folder locations).
1. Ask the user which journey they want:
   - **Explore a research idea** — literature search, landscape, hypotheses,
     citation-backed report. Mode: `explore_research_idea`.
   - **Improve a repository** — everything above plus a frozen baseline and
     benchmarked experiments on their code. Mode: `improve_repository`.
2. Ask for a one-sentence objective (for `improve_repository` it should name
   the metric to improve, e.g. "Improve classification F1 without increasing
   latency").
3. Run:

```bash
researchforge doctor --json
researchforge project create --mode <mode> --objective "<objective>" --json
```

4. For `improve_repository`, also scan the repository:

```bash
researchforge repo scan . --json
```

5. Report what was created and follow `researchforge status --json` →
   `next_action` into the next skill.

## Rules

- The Python engine is the boundary: never work around a validation error, a
  protected path, or an approval gate — fix the artifact or ask the user.
- Approvals belong to the user: never pass `--yes` or type a confirmation
  unless the user explicitly approved that step in this conversation.
- Ground every summary in stored data: quote only numbers returned by
  `--json` output or files under `.researchforge/` — never invent metrics.
