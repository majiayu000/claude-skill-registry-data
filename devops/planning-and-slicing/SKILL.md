---
name: planning-and-slicing
description: 'Breaks high-level goals into an incremental, prioritised plan using the plan template.'
metadata:
  id: ce.skill.planning-and-slicing
  tags: [planning, architecture, context-min]
  inputs:
    files: [plan-template.md, PRODUCT.md, ARCHITECTURE.md]
    concepts: [milestones]
    tools: [toolset:read]
  outputs:
    artifacts: []
    files: [PLAN.md]
    actions: [produce-plan]
  dependsOn:
    artifacts: []
    files: [plan-template.md]
  related:
    artifacts: [ce.prompt.create-plan]
    files: []
---

# Planning and Slicing Skill

Use this skill to convert agreed requirements into an actionable plan that can be executed in
incremental steps.

## Steps

1. **Load templates and context.** Read `plan-template.md` to understand the structure of a
   plan (goals, requirements, milestones, risks, tools, acceptance criteria). Load
   `PRODUCT.md` and `ARCHITECTURE.md` to ensure alignment with product vision and system
   constraints.

2. **List goals and requirements.** Start by restating the goals and summarising the
   confirmed requirements. Group related requirements together.

3. **Identify milestones.** Break the work into logical milestones or slices. Each milestone
   should deliver user value, be testable and small enough to complete within a short time
   frame. Order milestones based on dependencies and risk.

4. **Assign tasks and resources.** For each milestone, outline the tasks needed (design,
   implementation, testing, documentation). Note which files or modules will be touched and
   which skills or prompts will be used.

5. **Document risks and assumptions.** Capture potential risks (technical, operational,
   dependency) and assumptions. Define mitigation strategies where possible.

6. **Define acceptance criteria.** For each milestone, specify what constitutes success. Use
   measurable outcomes to guide implementation and review.

7. **Record the plan.** Fill out a new plan document based on `plan-template.md`, inserting
   the structured information in the appropriate sections. Save the plan as `PLAN.md` or
   return it to the user for storage.

8. **Review with stakeholders.** Present the plan to the user or team for feedback. Iterate
   until consensus is reached before moving to implementation.

Careful planning and slicing lead to predictable delivery and reduce the likelihood of scope
overruns or architectural misalignment.
