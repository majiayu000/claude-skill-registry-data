---
name: research-plan
description: "Turns a research note, plan or objective (any form, with or without data) into modeling tasks, runs them with the studio's skills and reports results against the note."
---
<!-- Generated from .claude/skills/research-plan/SKILL.md by tools/sync_agents.py. Edit the source, then run the script. -->

# /research-plan — Research Plan

**Category:** Scoping & Design · **Primary agent:** `research-note-analyst`

Turns a research note, plan or objective (any form, with or without data) into modeling tasks, runs them with the studio's skills and reports results against the note.

Arguments: whatever the user wrote after the command name.

## Purpose
Start from whatever the user has: a research note, a work plan, terms of reference, a list of questions, an email, slides, a chart narrative, or a few lines of objectives typed in the chat, in any format (DOCX, PDF, Markdown, text) and with or without data files. The skill reads it, works out what it asks for, splits it into analytical tasks, maps the data, proposes how the studio would do each task, and after approval runs the tasks through the studio's existing skills and reports the results organized by the note's own questions or sections. It ends with a Word report and a PowerPoint presentation that answer each question or objective with its charts and tables, and collects everything (deliverables, charts, code and run outputs) in one folder and a zip.

Notes differ. Some only state questions; some describe a method, assumptions or existing results; some come with spreadsheets. The skill adapts:
- **Questions only:** the studio proposes and runs its own approach.
- **A stated method or existing results:** the studio follows the method where the user wants it, and says where it would do things differently.
- **Reproducing existing numbers (replication)** happens only when the note or the user asks for it, or when it is needed to check that supplied results are right before building on them.

**Use it when** a user brings a note, plan, objective or brief and asks the studio to help with the modeling and results.

**Do not use it when** there is a single, well-defined question that `/scope-question` handles directly, or an existing model to bring in (`/adopt`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - The note, plan or objective (a file or text in the chat)
   - What the user wants back, for whom and by when (ask if not stated)
   - Data files supplied or named (optional; tasks without data are marked)
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Notes and data that are not public are classified before they are read: keep them outside git (`data/raw/<project>/`), never copy their content into committed files, prompts to external services or logs unless the class allows it, and do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `research-note-analyst` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `modeling-methodology-specialist` — Chooses methods and architecture across model families, sets code and data standards, and resolves technical trade-offs between traditional, structural and AI approaches
- `data-governance-metadata-specialist` — Owns data governance and metadata
- `project-planning-specialist` — Plans scope, sequencing, dependencies and phase gates

Bring in the specialists each task needs (for example `cross-country-indicators-specialist` for multi-country panels, `debt-sustainability-analyst` for debt work, the build specialists for new models). Each agent is defined in `.claude/agents/<name>.md`. If your tool runs subagents, run these agents as subagents, in parallel where the steps are independent; otherwise read each agent's file and apply its instructions in turn. Subagents only write to the paths named in your instructions.

## Key design decisions (present options, let the user choose)
| Decision | Typical options | What it changes |
|---|---|---|
| Approach per task | the studio's method; the note's stated method; both, compared | Whether the result follows, challenges or extends the note |
| Replication | none; reproduce supplied results before building on them | Whether existing numbers are checked first |
| Scope | all tasks, priority tasks first | Effort and order |
| Freedom | same data, same data with any method, new data allowed | How far the studio may depart from the note |
| Outputs | Word report and PowerPoint presentation by question (always); technical annex, policy brief, model | Effort and audience |

## Workflow
1. Confirm what the user wants back, the audience and the deadline
2. Read the note (`python tools/intake.py note <file>` gives numbered paragraphs for DOCX, Markdown and text; read PDFs, slides and chat text directly)
   - List the questions or objectives, the result each asks for, and any stated methods, assumptions, data sources and existing results, each with where it comes from in the note
   - Note what is unclear and turn it into questions for the user
3. If data are supplied, inventory them (`python tools/intake.py data <file>`); map each task to its data; mark gaps `NOT ASSESSED — NO DATA` and name the source that would fill them
   - Where the note relies on spreadsheet calculations, read the formulas behind them (`python tools/intake.py formulas <file> --sheet <name>`) and report any difference from the note's description as a finding, not a silent fix
4. Write the research brief (`docs/templates/research-brief.md`): tasks, the approach proposed for each with trade-offs and a simple benchmark, data map, routing to skills, priorities and checkpoints; wait for approval
5. Run the tasks through the studio's skills, in parallel where they are independent, for example:
   - Model choice and a new model: `/select-model-class`, `/model-spec`, then the build command for the family
   - Forecasts, scenarios and risks: `/forecast-round`, `/scenario-analysis`, `/fan-chart`, `/stress-test`
   - Fiscal and debt: `/debt-sustainability`, `/debt-decomposition`
   - Cross-country indicators and groupings: `/vulnerability-dashboard`, `/country-typology`
   - Estimation: `/estimate-var`, `/local-projections`, `/build-causal-ml`
   - Communication: `/chart-pack`, `/policy-brief`, `/technical-note`
6. Where replication was agreed, reproduce the supplied results within tolerance first; where both the note's method and the studio's are run, explain each difference and the assumption behind it
7. Write the results report (`docs/templates/results-report.md`): a short summary with one answer per question, then one section per question or objective with the answer, the charts and tables that support it (charts embedded as `![caption](path/to/chart.png)` from the run folders), the method and data, and the caveats; tasks that could not be done are listed with the reason. A chart or table made only for the report, not by a model run, is drawn by a script saved in `<results folder>/charts/` that reads saved run outputs and computes no new numbers; the script is listed in the report's annex next to the model code
8. Produce the Word report: `python tools/report.py docx <results-report.md> --out <project>-results.docx`. Charts and tables are numbered, and any chart that cannot be found is reported. Check that every question has its section and that no chart is missing
9. Produce the presentation from the same report: `python tools/report.py pptx <results-report.md> --out <project>-results.pptx`. It has a title slide, a questions-and-answers slide, and for each question a slide with the answer next to its main chart (method as a footnote, caveats below the answer), followed by slides for further charts and tables; keep each answer short enough for a slide
10. Collect everything in one place: `python tools/report.py bundle <results-report.md> --out <results folder>/<project>-all-results`. The folder (and `<project>-all-results.zip` next to it) holds the Word file, the presentation, the report, every chart, the code and the run folders the report names, keeping their studio paths, with an index (`README.md`) by question. Raw, restricted and confidential data are never copied. Give the user the paths of the folder and the zip, the Word file and the presentation

## Checkpoints with the user
- After the note is read: confirm the tasks, the stated assumptions and the open questions
- After the research brief: approve the approach per task, scope and priorities
- Before the Word report and presentation: review findings and caveats

## Common pitfalls
- Assuming every note asks for replication, or ignoring a method the author asked to keep
- Building a large model when the note asks for an accounting exercise, or the reverse
- Silently changing the author's assumptions when following the note's method
- Trusting a description of a calculation without reading the formulas behind it
- Sheets that stack a second block below the data, so codes repeat
- Losing the link between a result and the question that asked for it
- Copying internal note content or data into committed files or external services

## Output
`docs/briefs/<project>/research-brief.md`; results in `docs/briefs/<project>/results/`: `results-report.md`, the Word report `<project>-results.docx` and the presentation `<project>-results.pptx`; everything collected in `<project>-all-results/` and `<project>-all-results.zip`

The research brief holds the tasks with their source in the note, the approach per task, the data map, routing and plan. The results report answers each question or objective with its charts and tables, the method, the findings and the caveats, and the Word report and the presentation are made from it with the charts embedded. When the note or data are not public, write the brief and the results to `data/processed/<project>/` instead, which stays outside git; model code and runs live in the model folders named by the routed skills. Every run saves its results to `output/<run-id>/` in the model folder, with a run log (`.claude/rules/model-code.md`).

## Gate / verdict
- Every task points to the part of the note it serves, and every question in the note has a task or a stated reason why not
- The Word report has a section and the presentation a slide for every question or objective, with its answer and supporting charts and tables, and no chart is reported missing
- The all-results folder and zip exist, and their index lists the outputs of every question
- Any agreed replication matches the supplied numbers within tolerance, or the discrepancies are explained
- Every chart and table in the report comes from saved code: a model run or a saved chart script listed in the annex
- Differences from the note's method are explained
- Inputs were classified and are stored where their class allows

## Suggested next steps
- `/select-model-class`
- `/scenario-analysis`
- `/policy-brief`
- `/chart-pack`
