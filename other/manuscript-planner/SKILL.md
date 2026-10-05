---
name: manuscript-planner
description: "Plan academic manuscripts — structure, reporting standards, journal requirements."
version: 0.1.0
---

# Manuscript Planner

Planner skill for designing academic manuscripts strategically — research design, methodology, reporting standards, structure, and submission strategy — *before* writing begins.

Use this skill to design manuscripts that meet journal standards, clear desk-rejection screens, enable methods reproducibility, and satisfy reviewer, editor, and reader expectations.

## JTBD (Jobs To Be Done)

### Primary Job
When I have study outputs — data, results, a completed analysis — but haven't yet determined which journal to target, which reporting standard applies, or how to structure the manuscript so it clears desk rejection,
I want a manuscript plan that locks in journal fit, reporting standard compliance, and section architecture before the first word is written,
so I don't spend months drafting toward the wrong structure and get rejected for preventable reporting gaps.

### Secondary Jobs
- When a manuscript received major revision requests and the core structure or framing needs to be rebuilt before resubmission, I want a redesign plan that addresses the reviewers' structural objections — not just line edits — so the resubmission doesn't repeat the same problems.
- When a team has competing views on which journal to target or how much methodological detail belongs in Methods vs. Supplement, I want those decisions documented and justified upfront, so the manuscript doesn't get restructured mid-draft.

### Job Layers
- Functional: Produce a journal selection decision with desk-rejection risk assessment, a reporting standard compliance map (CONSORT/STROBE/PRISMA checklist pre-filled), a section-by-section architecture specifying content, sequence, and word allocation, and a results presentation order matched to the stated hypotheses — all before drafting begins.
- Emotional: Reduce the anxiety of discovering three months into writing that the manuscript is structured for the wrong journal format, or that the reporting standard requires sections you never planned to include.
- Social: Helps the user present a journal-ready structure to co-authors and collaborators before drafting investment is made, so structural disagreements surface in planning rather than during peer review.

### This Skill Is For
- A researcher who has completed a study and needs to plan the manuscript before writing — not after a draft exists.
- A team rebuilding a manuscript after major revision rejection, where the structure itself (not just the prose) needs redesign.
- A researcher preparing a complex study — RCT, systematic review, multi-outcome trial — where reporting standard compliance must be planned explicitly rather than checked retrospectively.

### This Skill Is NOT For
- A user with an existing manuscript draft who needs a quality verdict on submission readiness; use `manuscript-critic` instead.
- A user whose primary unresolved problem is the study design or methodology itself, not how to write it up; use `study-design-planner` instead.

### Paired With
- `manuscript-critic`: After the manuscript draft exists, use it to audit submission readiness, reporting compliance, and desk-rejection risk.
- `study-design-planner`: Use this when the unresolved problem is study design itself, not manuscript structure.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has study outputs but no manuscript structure | The skill selects journal, maps reporting standard, and architects section-by-section plan | A drafting blueprint with word allocations and hypothesis-ordered results sequence |
| Manuscript was rejected for structural or reporting reasons | The skill diagnoses the structural gap and rebuilds the architecture for resubmission | A resubmission plan targeting the specific rejection reasons |
| Team disagrees on journal or reporting standard | The skill scores journal fit and maps compliance gaps for each option | A documented journal decision with desk-rejection risk rationale |

### When to Escalate
- If the user already has a drafted manuscript and needs a submission verdict, escalate to `manuscript-critic`.
- If the study methodology itself is in question — not just how to write it up — escalate to `study-design-planner`.

## Purpose

Plan manuscripts strategically, not reactively:

- **Define the research scope**: What's the research question? What study type? What are the hypotheses/objectives?
- **Select reporting standards**: CONSORT (RCTs), STROBE (observational), PRISMA (systematic reviews) — plan compliance from day one
- **Specify methodology**: Document what must be written for another researcher to replicate the study
- **Design manuscript structure**: Plan title, abstract, introduction logic, methods organization, results sequence, discussion framework
- **Plan results presentation**: Organize results in hypothesis order, with effect sizes and CIs, not analysis-code order
- **Choose target journal**: Understand desk-rejection risks, formatting standards, article type expectations
- **Ensure reporting standard compliance**: Map each checklist item to the corresponding manuscript section before writing
- **Quality-assure before submission**: Multi-perspective review and pre-submission checklist prevent desk rejections and major revision requests
- **Plan data sharing**: Document reproducibility plan (code, data, analysis scripts availability)

This skill produces a detailed manuscript design specification that guides writing and ensures submission readiness.

## Use_When

- Planning a new academic manuscript before starting to write
- Designing a research study with the manuscript structure in mind
- Redesigning a manuscript that received major revision requests (prevent resubmission problems)
- Preparing a manuscript for submission to a specific journal
- Needing to understand and ensure CONSORT/STROBE/PRISMA compliance
- Planning a complex study (RCT, systematic review, meta-analysis) with multiple outcomes and subgroups
- Designing manuscript structure for novel research or methods
- Clarifying research questions and primary outcomes before data collection
- Planning how to present results (hypothesis order, effect sizes, CIs)
- Evaluating journal fit and desk-rejection risk before submission

## Do_Not_Use_When

- You've already written a manuscript and want critique (use manuscript-critic instead)
- You need quick feedback on a draft in progress (use manuscript-critic for that)
- The manuscript is already submitted and in peer review
- You're learning basic academic writing skills (use writing guides and examples instead)
- The study design is still in early conceptual stages (use research-critic first)

## Companion_Skills

- **manuscript-critic**: Use AFTER planning and writing to review submission readiness, reporting standard compliance, desk-rejection risk
- **research-critic**: Use when refining the study design/methodology before planning the manuscript
- **copy-planner**: Use for marketing/commercial copy planning (not academic/research manuscripts)
- **drupal-planner**: Use when implementing manuscript tracking systems

## Steps

1. **Define the research scope**: Provide context about:
   - Primary research question (specific and measurable)
   - Study type and design (RCT, cohort, case-control, cross-sectional, systematic review, meta-analysis)
   - Target journal for submission
   - Primary and secondary hypotheses/objectives
   - Expected effect size and clinical significance

2. **Clarify journal expectations**: Share information about:
   - Target journal scope and article types
   - Word count limits, formatting requirements
   - Reporting standard required (CONSORT, STROBE, PRISMA, other)
   - Known desk-rejection criteria or common rejection reasons

3. **Understand the study methodology**: Provide details about:
   - Study population (size, inclusion/exclusion, recruitment)
   - Primary outcome and how it will be measured
   - Secondary outcomes
   - Study design justification
   - Statistical analysis approach

4. **Invoke the manuscript-planner subagent**: Delegate to subagent with the full planning protocol:
   - **Local routing authority (default)**: Route through the repository agent named by this skill; if it is unavailable, use a host general-purpose worker with the full protocol. The catalog/meta-router owns route and model selection.
   - **Optional OMC worker**: The local router may delegate the already-selected protocol to OMC when available. OMC does not choose the route or model policy.

5. **Return planning output**: Present the structured manuscript design with:
   - Research scope and manuscript goals
   - Methodology architecture specification
   - Manuscript structure design (sections and sequence)
   - Reporting standard compliance mapping
   - Results presentation sequence (hypothesis order)
   - Journal desk-rejection screening
   - Quality assurance checklist
   - Implementation tasks with review checkpoints

The plan guides manuscript writing. Use manuscript-critic to review the completed draft before submission.

## Tool_Usage

When invoking manuscript-planner:
- Use Read to load journal author instructions, study protocol, or prior manuscripts
- Use Grep to search for specific methodological details in research documentation
- Use Bash to analyze study data or sampling methodology details
- Understand the full research scope and journal requirements thoroughly before planning

## Related_Skills

- **manuscript-critic**: Post-submission-draft review of readiness, reporting standard compliance, desk-rejection risk
- **research-critic**: When refining study design or methodology validity
- **copy-planner**: For non-academic writing (marketing, grant proposals use separate protocols)
- **writing-standards-critic**: For academic writing style and clarity audits
