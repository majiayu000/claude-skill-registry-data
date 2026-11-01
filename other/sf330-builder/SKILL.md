---
name: sf330-builder
description: "Assembles a federal qualifications submission section by section, and does the part that decides the score: selecting the example projects and writing them so that each one demonstrates a specific evaluation criterion rather than being included because it is good work. Builds the team organisation against the projects named, keeps résumés consistent with the projects they claim, and checks every section against the solicitation's own instructions before submission. Trigger on \"SF330\", \"federal qualifications package\", \"which projects go in Section F\", \"architect-engineer qualifications\", \"sf330-builder\", or a federal solicitation handed over to answer. Carries no form instructions and no evaluation criteria; both come from the current form and the specific solicitation, which override any general guidance. It does not replace the principal, who signs."
license: MIT
metadata:
  title: "SF330 Builder"
  summary: "Assemble an SF330 with the project sheets that actually match the scope"
  discipline: "practice-contracts"
  tags: "Documentation"
---

# SF330 Builder

The form is not the difficulty. The difficulty is that every practice submits
its best projects, and the ones that score are the ones where each project
visibly demonstrates a criterion the evaluator has in front of them.

## Scope and limits — read first

**What this does.** Works through the submission section by section, with most
of the effort on selecting and writing the example projects against the
solicitation's evaluation criteria, and checks the whole package against the
instructions before it goes.

**What this does not do.**

- **It carries no form instructions and no criteria.** The current form's
  instructions and the specific solicitation govern, and both change. Where they
  conflict with anything here, they win.
- It does not know the current form's section structure from memory. You supply
  the form or its instructions.
- It does not write the firm's content. Projects, people and experience come
  from you.
- It does not decide whether to pursue. `go-no-go-review` does.
- It does not build a non-federal response. `rfp-response-builder` does.
- It does not replace the principal, who signs.

**What you need before starting.** The solicitation, complete, with the
evaluation criteria and any addenda. The current form and its instructions. Your
project archive with dates, fees, roles and references. Your team and their
actual availability. Your subconsultants, and whether they have agreed.

## Workflow

### Step 1. Establish the criteria and the instructions, before anything else

Ask, in one message:

> 1. What are the evaluation criteria, in the solicitation's own words and
>    order, with weights if given?
> 2. What does the solicitation add to or change about the form's standard
>    instructions? Page limits, project counts, additional sections, formatting.
> 3. What is the scope being procured, precisely?
> 4. What are the submission mechanics and the deadline?
> 5. Which subconsultants are on the team, and have they confirmed?
> 6. Is there an incumbent, and is this a new requirement or a recompete?

The solicitation's own instructions override the form's general ones, and
practices lose on this routinely.

### Step 2. Select the example projects against the criteria, not by quality

This is the step that decides the outcome. Build the matrix before choosing:

| Criterion | Weight | Candidate projects that demonstrate it | Chosen | Why |
|---|---|---|---|---|

Rules for selection:

- Every project earns its place by demonstrating a criterion. A project included
  because it is the practice's best work, and demonstrating nothing in
  particular, has spent a slot.
- Aim for coverage across the criteria before depth on any one.
- Relevance beats prestige. A modest project matching the scope precisely scores
  above a landmark that does not.
- Recency matters, and the solicitation usually says how much.
- A project where the named team actually worked beats one where the firm did.

Report which criteria remain undemonstrated after selection. That gap is the
score you will lose, and it is better known now than after.

### Step 3. Write each project entry to its criterion

For each chosen project:

- Lead with what makes it relevant to this scope, not with what it is.
- Name the specific similarity: building type, size, delivery method,
  jurisdiction, client type, technical challenge, constraint.
- Include the outcome, with a number where you have one.
- Name which of your proposed team worked on it, and in what role. This links
  the project section to the team section, and evaluators check.
- Include the reference the solicitation asks for, and confirm the person is
  still there and knows they are being named.

### Step 4. Build the team against the projects

The organisation chart and the résumés have to agree with the project section
and with each other:

- Every key person named in the chart has a résumé.
- Every résumé's experience includes the projects claimed for that person in the
  project section.
- The roles proposed match what the scope needs, and there is nobody in the
  chart with no role.
- Subconsultants shown are on the team, have agreed, and their projects are
  identified as theirs.
- Availability is real. Naming someone who is committed elsewhere is found at
  interview.

Report every inconsistency between the chart, the résumés and the project
section. These are the errors evaluators find and they undermine everything
else.

### Step 5. Write the remaining narrative sections to the criteria

For any section where the practice describes its approach, capability or
management: answer against the criteria, name this scope, and cut anything that
would fit any solicitation. Generic narrative is the most common way a
technically strong package scores mid-range.

### Step 6. Check the package before submission

- Every section the form and the solicitation require, present.
- Page counts, per section where applicable.
- Every criterion, traced to where it is addressed.
- Every criterion not demonstrated, listed.
- Chart, résumés and projects consistent.
- Every reference confirmed.
- Subconsultant participation confirmed in writing.
- Signature, dates, and every mechanical requirement.
- Every addendum acknowledged.

Report the undemonstrated criteria and the inconsistencies first.

### Step 7. Save

Ask where. Keep the criteria matrix with the package; it is the debrief document
and the basis for the next submission to the same agency.

## Rules

- **Never state a form section's contents or an instruction from memory.** The
  current form and the solicitation govern.
- Select projects against criteria, never by quality.
- Every project entry names which proposed team members worked on it.
- Check the chart, the résumés and the projects against each other, every run.
- Report undemonstrated criteria before submission.
- Confirm every reference and every subconsultant.
- Never name someone who is not available.

## Anti-patterns

- Choosing the firm's best projects and mapping criteria onto them afterwards.
- Prestige over relevance.
- A résumé that does not include the project it is claimed for.
- Generic capability narrative.
- Following the form's general instructions where the solicitation differs.
- Naming a reference nobody has spoken to.
- Including a subconsultant who has not agreed.
- Submitting without listing what the package fails to demonstrate.

## Resources

None. This skill is one file. Output is written directly at the path you choose.
