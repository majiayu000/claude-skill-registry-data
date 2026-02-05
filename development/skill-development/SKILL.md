---
name: Skill development
description: This skill should be used when the user asks to "create a skill", "write a new skill", "improve a skill description", "organize skill content", "update skill references", "update skill workflows", "review a skill", "test a skill", "add a reference", "add a workflow", "add a template", or needs guidance on skill structure, progressive disclosure, or skill development best practices.
version: 0.1.0
---

# Skill development

This skill provides guidance for creating, reviewing, and testing Claude Code skills. It includes progressively-disclosed references on skill structure, bundled resources, workflows, templating, activation hooks, and project overrides.

## Steps

1. **Gather context** - Run `oaps skill orient skill-development` to see available references and workflows

1. **Identify relevant references** - Review the references table from step 1 and select those matching your task

1. **Load dynamic context and references** - Run `oaps skill context skill-development --references <names...>`

1. **Review loaded references and commands** - Read through the guidance. The **Allowed commands** table at the end of the output is authoritative for what commands can be run.

1. **Follow the workflow** - Adhere to the selected workflow's steps for creating, reviewing, or testing skills.
