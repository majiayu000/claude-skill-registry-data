---
name: execute-plan
description: The user wants to follow the steps in a plan to drive it towards its goal
---
# Execute Plan

Your is to drive the plan forward towards its goal. The user should specify which markdown plan file they want to use. If they have not, make sure to ask them - everything is going to depend on the content of the plan file. If you are given a name of the plan, scan the directory to see if there is a file that matches that name.

Your job is to complete work on a single sub-goal.

## Workflow

1. Read the plan file, and read the log file that is referenced in the plan file (you may need only to read the bottom part of the log file).
2. If there is no sub-goal under the `Steps` section:
  - Repeat the next sub-goal in the header of the `Steps` section.
  - Come up with a series of steps that you think is best option to acheive the sub-goal. It is ok if not all steps are known. The out come of some steps might change what will be done next.
  - Since you are coming up with a plan, pause to ask the user to inspect.
  - You must do this before moving on - the steps should always reflect your plan for the sub-goal you are working on!
3. Execute the steps until the goal is met, the goal will fail, etc.
4. Once all steps are complete and the sub-goal is successful or has failed, add a **Acheived** or **Failed** in the sub-goals section, and add a summary to the sub-goal.
  - The summary should be detailed enough that someone reading it won't have to re-run the steps to runderstand what happened.
5. Clear out the Steps section except for the template for the next sub-goal.
5. Update the sub-goals, and let the user know.

## Executing Steps

Execute the step as it has been written.

As each step is completed:
    - The step should be marked "**Done**`.
    - Write a short description of the result. It should be detailed enough so that if you go back and re-read this you can figure out the result without having to repeat the work for the sub-goal.
    - Examine the next steps to make sure they still make sense. If they do, then start working on the next step
    - Rewrite the steps if they don't make sense with the next logical thing to acheive the sub-goal.
    - A possible outcome is either the sub-goal is achieved or it fails.

A step is an atomic and focused unit of work. As example:

- Modify the code to add a feature.
- Run with the following configuraiton and inspect the result for X

After modifying the steps as you are making progress there is no reason to pause to ask the user. If you are stuck, then do ask the user for help.

## Updateing sub-goals

When a sub-goal has compelted or failed, it is time to review all the sub-goals and make sure they still make sense and are a good match for getting to the overall goal.

sub-goals are high level, and will include multiple steps. They are generic, but they are also not too big a unit of work. For example:

- A good sub-goal may suggest an avenue of modifications and tests. But the sub-goal won't suggest two avenues (that would be two sub-goals).
- A sub-goal won't say "run the code with these options" - that is a step and too fine grained.
- A sub-goal should always move the work towards the overall goal. The text describing the sub-goal should say how that will happen if it isn't clear (e.g. explain why this is a good sub-goal).

When a sub-goal is finished:

- Mark it as either **Acheived** or **Failed**
- Add bullets under it to describe the result and a short summary of the work. You'll want a concise history of the the outcome of each sub-goal so you don't repeat them!
- If changes are made to code and the README.md file for the repo tracks information like that, always make sure to update it.
- Review the next sub-goals to make sure they still make sense.
- Reivew the `Future Ideas` sectiont to see if there is something there that makes more sense.
- If the next sub-goals no longer make sense, remove them, and come up with an appropriate new one.
- If some work suggests some other possible avenues of investigation, feel free to add them to the `Future Ideas` section. Also, keep the future ideas section clean, removing things that are no relavent or have been tried (if converted to a sub-goal they should be removed immediatly).
- Review the complete plan and make sure there is enough information so that if all context was lost you could pick up where you left off. This means updating any section called `Context Snapshot` as well.

If a sub-goal involves making a choice between a few possible changes or way forward, make sure this decision is made in the steps you write. A step to acheive the sub-goal should be to write a plan for each option, another step to evaluate the options and pick one. The other choices should be moved to future ideas so they can be picked up later if needed. And then go on to modify the steps to follow the plan for the selected choice.
