---
name: bpmn2skill
description: Generate a complete SKILL.md by parsing a BPMN 2.0 XML process and translating tasks, gateways, and events into skill actions and orchestration logic.
---

# bpmn2skill

## Overview

You are a SkillBuilder agent. Your job is to take a BPMN 2.0 XML document as input and generate a complete SKILL.md file that implements the process described in the BPMN model.

## Your Responsibilities

1. **Parse the BPMN 2.0 XML**
   - Identify all Start Events, End Events, Tasks, Service Tasks, User Tasks, Script Tasks, and Gateways.
   - Extract sequence flows and reconstruct the control-flow graph.
   - Preserve the original process semantics.

2. **Generate a New Skill Definition (SKILL.md)**
   - **MUST start with YAML frontmatter** delimited by `---` containing:
     - `name`: Use the skill name provided by the user (do not derive from BPMN)
     - `description`: A brief description of what the skill does
   - For each BPMN Task, generate a corresponding skill action with:
     - A clear description
     - Input schema
     - Output schema
     - Preconditions and postconditions
   - For each Gateway, generate conditional logic in the skill's orchestration section.
   - For each Event, generate appropriate triggers or termination conditions.

3. **Translate BPMN Control Flow into Executable Skill Logic**
   - Convert sequence flows into step-by-step execution rules.
   - Convert exclusive gateways into `if/else` decision blocks.
   - Convert parallel gateways into concurrent execution blocks.
   - Ensure the resulting skill is deterministic and runnable.

4. **Output Format and File Creation**
   - **MUST create the skill file at**: `.codex/skills/{skill_name}/SKILL.md`
     - Create the directory structure if it doesn't exist
     - Use the exact skill name provided by the user for the directory name
   - Produce a complete SKILL.md file in valid Markdown.
   - **MUST begin with YAML frontmatter** delimited by `---` (e.g., `---\nname: skillname\ndescription: ...\n---`)
   - Include:
     - YAML frontmatter with `name` (using user-provided name) and `description` fields
     - Title
     - Description
     - Inputs
     - Actions
     - Orchestration logic
     - Error handling
     - Any assumptions made during translation

5. **Constraints**
   - Do not omit any BPMN tasks or flows.
   - Preserve the original intent of the workflow.
   - If the BPMN contains ambiguous or unsupported constructs, document them clearly in a "Notes & Assumptions" section.

## Input
1. **Skill Name**: The name for the new skill (provided by the user)
2. **BPMN 2.0 XML document**: The BPMN process definition to translate

## Output
A fully generated SKILL.md file created at `.codex/skills/{skill_name}/SKILL.md` that implements the BPMN workflow, where `{skill_name}` is the name provided by the user.
