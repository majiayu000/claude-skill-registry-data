---
name: slide-builder
description: Creates professional presentation slides in GitHub markdown format for educational content. Use when the user asks to create slides, build a presentation, or needs visual teaching materials. Generates clean, engaging slides with strategic emoji and clear formatting.
allowed-tools: Read, Write, Edit, Glob, Task
---

# Slide Builder Skill

This skill creates professional, engaging presentation slides for teaching AI and prompt engineering.

## When to Use

Use this skill when the user:
- Asks to create presentation slides
- Wants to build a slide deck for a lesson
- Needs visual materials for teaching
- Requests slides from an existing lesson plan
- Wants to update or enhance existing slides

## What This Skill Does

1. **Gathers Requirements**:
   - Which lesson to create slides for
   - OR reads existing lesson plan automatically
   - Any specific focus areas or special slides needed
   - Presentation style preferences

2. **Invokes the slide-designer Subagent** to create:
   - Complete slide deck from lesson content
   - Clean GitHub-flavored markdown formatting
   - Strategic emoji for visual interest (not excessive)
   - One key idea per slide principle
   - Example prompts in formatted code blocks
   - Activity instruction slides with clear steps
   - Presenter notes with timing suggestions
   - Check-for-understanding slides

3. **Saves Slides** to:
   - `prompt-engineering-curriculum/class-XX-title/slides.md`

4. **Creates Supporting Materials**:
   - Student handout version if requested
   - Quick reference appendix
   - Presenter's guide with timing

## Slide Design Principles

- **One Idea per Slide**: Focus prevents overwhelm
- **Visual Hierarchy**: Clear headers and structure
- **Strategic Emoji**: 🎯 📚 💡 ✅ ⚡ (purposeful, not excessive)
- **Code Block Examples**: Formatted prompt examples
- **Student-Facing Language**: "You will..." not "Students will..."
- **GitHub-Ready**: Renders beautifully on GitHub

## Output Structure

Slide decks include:
- Title slide with learning objectives
- Concept explanation slides (one per concept)
- Demonstration slides with examples
- Activity instruction slides
- Check-for-understanding moments
- Summary and next steps
- Presenter notes throughout

## Example Usage

User: "Create slides for the role-based prompting lesson"

This skill will generate a complete, professional slide deck ready to present.
