---
name: lesson-structure
description: Provide lesson markdown templates for the AI-Native Robotics Textbook. Use when writing lessons, structuring educational content, or validating lesson format.
allowed-tools: Read
---

# Lesson Structure

## Instructions

When creating lesson content:

1. Follow the standard lesson template
2. Include all required sections
3. End with "Try With AI" section
4. Assign appropriate pedagogical layer

## Required Sections

Every lesson MUST include:

1. **Learning Objectives** - What students will learn
2. **Prerequisites** - Required prior knowledge
3. **Main Content** - Core lesson material
4. **Hands-On Exercise** - Practical application
5. **Reflection Questions** - Self-assessment
6. **Try With AI** - AI-assisted extension (FINAL SECTION)

## Lesson Metadata

```yaml
---
title: Lesson Title
layer: L1-L5
duration: 45-90 minutes
prerequisites:
  - Prior lesson or concept
learning_objectives:
  - Objective 1
  - Objective 2
---
```

## Reference

See [template.md](template.md) for the full lesson template.
