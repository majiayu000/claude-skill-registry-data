---
name: lesson-creator
description: Creates comprehensive, detailed lesson plans for AI/prompt engineering classes. Use when the user asks to create a new lesson, develop class content, or needs a detailed teaching plan for a session. Generates minute-by-minute breakdowns with activities, differentiation, and assessment.
allowed-tools: Read, Write, Edit, Glob, Task
---

# Lesson Creator Skill

This skill creates comprehensive, ready-to-teach lesson plans for the AI Academy prompt engineering curriculum.

## When to Use

Use this skill when the user:
- Asks to create a new lesson plan
- Wants to develop content for a class session
- Needs detailed teaching materials for a specific topic
- Requests a structured 90-minute lesson
- Wants to plan activities and exercises for students

## What This Skill Does

1. **Gathers Requirements** from the user:
   - Class number and title
   - Main learning objectives
   - Target grade levels (7th, 9th, 11th)
   - Key topics/techniques to cover
   - Time allocation (default: 90 minutes)
   - Any specific constraints

2. **Invokes the lesson-planner Subagent** to create:
   - Detailed minute-by-minute lesson plan
   - Pre-class setup checklist
   - Teaching activities with timing
   - Differentiation strategies for all grade levels
   - Hands-on practice exercises
   - Assessment checkpoints throughout
   - Materials and technology requirements
   - Backup plans for common issues

3. **Saves Content** to the appropriate location:
   - `prompt-engineering-curriculum/class-XX-title/lesson-plan.md`
   - Creates exercises folder if needed
   - Generates templates folder structure

4. **Offers Next Steps**:
   - Ask if slides should be generated
   - Suggest creating exercises
   - Recommend assessment tools

## Output Structure

Lesson plans include:
- **Pre-Class Setup** (15 min before)
- **Minute-by-Minute Breakdown** with timing
- **Differentiation Notes** by grade level
- **Assessment Checkpoints**
- **Materials List**
- **Backup Plans** for tech failures, time issues, early finishers

## Example Usage

User: "Create a lesson plan for Class 2 on advanced prompting techniques"

This skill will gather details and generate a complete, ready-to-teach lesson plan.
