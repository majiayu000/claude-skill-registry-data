---
name: exercise-builder
description: Creates hands-on student exercises and practice activities for learning prompt engineering. Use when the user asks to create student activities, practice exercises, or hands-on learning tasks. Generates exercises with examples, solutions, and differentiation.
allowed-tools: Read, Write, Edit, Glob, Task
---

# Exercise Builder Skill

This skill creates hands-on, engaging exercises that help students practice and master prompt engineering techniques.

## When to Use

Use this skill when the user:
- Asks to create student exercises or activities
- Wants practice problems for specific techniques
- Needs hands-on learning tasks
- Requests examples for students to try
- Wants differentiated practice at multiple levels

## What This Skill Does

1. **Gathers Requirements**:
   - Exercise topic or skill to practice
   - Target grade level(s)
   - Time allocation for the exercise
   - Specific learning objective
   - Related class session
   - Difficulty level desired

2. **Invokes Subagents** to create:
   - **prompt-engineer subagent**: Designs the prompting technique practice
   - **lesson-planner subagent**: Structures the exercise format

3. **Creates Exercise Content**:
   - Clear, student-facing instructions
   - Specific prompting technique to practice
   - Example prompts at different skill levels
   - Success criteria (what good looks like)
   - Solution examples and variations
   - Common mistakes and how to fix them
   - Extension activities for advanced students
   - Scaffolding for struggling students

4. **Saves Exercise** to:
   - `prompt-engineering-curriculum/class-XX/exercises/exercise-name.md`

## Exercise Design Principles

- **Immediately Useful**: Use real homework scenarios
- **Progressive Difficulty**: Start simple, build complexity
- **Clear Success Criteria**: Students know when they've succeeded
- **Real Examples**: Authentic student work scenarios
- **Iteration-Friendly**: Encourage refinement and improvement

## Output Structure

Exercises include:
- **Learning Objective**: What students will practice
- **Time Allocation**: How long the exercise should take
- **Instructions**: Step-by-step, student-facing
- **Examples**: Model prompts and responses
- **Success Criteria**: What indicates mastery
- **Solutions**: Multiple correct approaches
- **Troubleshooting**: Common issues and fixes
- **Extensions**: Challenges for advanced students
- **Differentiation**: Support for various skill levels

## Example Usage

User: "Create an exercise for students to practice role-based prompting with their math homework"

This skill will generate a complete exercise with instructions, examples, and solutions.
