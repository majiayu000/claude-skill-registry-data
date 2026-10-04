---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages. So for instance, maybe they're like "I want to make a skill for X". You can help narrow down what they mean, write a draft, write the test cases, figure out how they want to evaluate, run all the prompts, and repeat.

On the other hand, maybe they already have a draft of the skill. In this case you can go straight to the eval/iterate part of the loop.

Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

Then after the skill is done (but again, the order is flexible), you can also run the skill description improver, which we have a whole separate script for, to optimize the triggering of the skill.

Cool? Cool.


## Dynamic Resources (Progressive Disclosure)

This skill is large. To save context, its detailed instructions are split into separate files in the `resources/` directory.
**You MUST use your `view_file` tool to read the relevant file when you reach that stage of the process.**

- **[resources/communicating_with_the_user.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/communicating_with_the_user.md)**: Read this to understand Communicating with the user.
- **[resources/creating_a_skill.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/creating_a_skill.md)**: Read this to understand Creating a skill.
- **[resources/report_structure.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/report_structure.md)**: Read this to understand Report structure.
- **[resources/executive_summary.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/executive_summary.md)**: Read this to understand Executive summary.
- **[resources/key_findings.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/key_findings.md)**: Read this to understand Key findings.
- **[resources/recommendations.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/recommendations.md)**: Read this to understand Recommendations.
- **[resources/commit_message_format.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/commit_message_format.md)**: Read this to understand Commit message format.
- **[resources/running_and_evaluating_test_cases.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/running_and_evaluating_test_cases.md)**: Read this to understand Running and evaluating test cases.
- **[resources/improving_the_skill.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/improving_the_skill.md)**: Read this to understand Improving the skill.
- **[resources/advanced_blind_comparison.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/advanced_blind_comparison.md)**: Read this to understand Advanced: Blind comparison.
- **[resources/description_optimization.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/description_optimization.md)**: Read this to understand Description Optimization.
- **[resources/claude_ai_specific_instructions.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/claude_ai_specific_instructions.md)**: Read this to understand Claude.ai-specific instructions.
- **[resources/cowork_specific_instructions.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/cowork_specific_instructions.md)**: Read this to understand Cowork-Specific Instructions.
- **[resources/reference_files.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/skill-creator/resources/reference_files.md)**: Read this to understand Reference files.
