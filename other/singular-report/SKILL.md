---
name: singular-report
description: Generate a written cross-domain report for one project or all of them — the decisions made per phase, open questions, approvals and skipped gates, how the domains line up and next steps — saved for sharing. Use when the user wants everything their workflows have produced so far summarized for themselves or stakeholders. Not for a quick progress table; see /singular-status.
metadata:
  argument-hint: "[project] [--skip-checks]"
---

# Report

Generate a cross-domain report for "$ARGUMENTS" (or every project under `.singularskills/` if no argument is given), built from the run log, the artifacts' frontmatter and their **Decisions** and **Open questions** sections.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"singular-report","workflow":"singular","phase":null,"project":"<project>","event":"skipped","artifact":"<artifact file>","note":"<reason or \"none given\">"}`.

## Prerequisites

Requires a `.singularskills/` folder with at least one artifact (for `<project>`, when given). If there is none, stop and tell the user that nothing has been saved yet.

## Process

1. **Read the workflows and the format.** Read every `*.yml` in the `workflows/` folder next to the `skills/` folder of this pack; if it is not there, read the copies of the workflow files bundled with the `workflow` skill (the conductor). The log and artifact format is described in the `run-log.md` reference bundled with the `workflow` skill. Read `.singularskills/config.md` if it exists for project context.

2. **Read the run log.** If `.singularskills/log.jsonl` exists, keep the lines for `<project>` (or for every project): `phase-approved` lines (which phases a person approved, and when), `skipped` and `refused` lines (gates bypassed or refused, with their notes), and `run-started` / `run-finished` lines (runs still open).

3. **Read the artifacts.** For each `.singularskills/<folder>/<project>/` folder (skip `reports/`), read every artifact:
   - its frontmatter: `skill`, `workflow`, `phase`, `started`, `finished`, `agent`, `gate`;
   - its **Decisions** and **Open questions** sections — the closing `## Decisions` / `## Open questions` of a single-writer artifact, or each member's `### Decisions` / `### Open questions` inside its `## <Skill title>` section of a shared artifact;
   - its `## Recalled` section (or a member's `### Recalled`), when a first-phase artifact has one: what the skill found about the project before it asked anything;
   - its `## Tools` section, when present: which Figma capabilities were bound to which tools, or that no server was connected; a utility artifact (frontmatter `phase: null`, no `NN-` prefix) is listed after the phases;
   - only as much of the body as you need to explain a decision.

   Give each phase a state: **approved** (logged approval), **written** (artifact present, no approval) or **missing**, as the `run-log.md` reference bundled with the `workflow` skill defines.

4. **Summarise per workflow and domain:** phases approved, written and missing; the key decisions (what was chosen, why, what was rejected); the open questions still standing; every skipped gate (frontmatter `gate: skipped` or a `skipped` log line), stated plainly.

5. **Identify cross-domain connections**, using the decisions themselves:
   - Do the design decisions follow the research findings?
   - Is the branding followed in marketing?
   - Are accessibility issues addressed in development?
   - Do open questions in one domain block a phase in another?

6. **Assess readiness:** what is approved and can be relied on, what is written but awaits review, what is missing or blocked, and which domains have not been started but should be.

7. **Write the report** to `.singularskills/reports/<project>-report.md` (or `.singularskills/reports/<date>-project-report.md` if no argument), with sections:
   - **Executive Summary** — one paragraph on where the project stands
   - **Workflow Status** — per workflow: each phase's state, approval date and gate
   - **Key Decisions** — per domain, quoted or condensed from the **Decisions** sections, each attributed to its artifact
   - **Open Questions** — collected from the artifacts, grouped by who or which phase must settle them
   - **Cross-Domain Insights** — connections and conflicts
   - **Readiness Assessment** — approved, awaiting review, missing or blocked
   - **Recommended Next Steps** — prioritized actions, naming the workflow and phase to run next

## Output

The report written to `.singularskills/reports/`. Present the executive summary and recommended next steps to the user.
