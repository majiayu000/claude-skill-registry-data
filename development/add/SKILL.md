---
description: Create a new comprehensive skill for a library
arguments: <library-name> [description and context]
examples:
  - /add-skill babashka.process for managing processes and shell commands
  - /add-skill honey.sql SQL query builder library
  - /add-skill use-package Emacs package configuration tool
  - /add-skill vertico Emacs completion interface
tags: [skill, library, clojure, emacs, documentation]
---

# Add Skill Command

Create a new skill in the library-skills plugin repository.

Use the claude-marketplace skill.

## Task

You are to create a comprehensive skill for a library. The skill
will be added to the appropriate plugin based on context inference.

## Command Arguments

Parse $ARGUMENTS to extract:
- Library name (required) - the library to create a skill for
- Brief description (optional) - what the library does
- Additional context (optional) - specific focus areas or aspects

## Plugin Inference

Infer the target plugin from context:

**Clojure Libraries** (plugins/clojure-libraries/skills/):
- Library names with dots (e.g., babashka.fs, next.jdbc)
- Keywords: clojure, clojurescript, babashka, jar, maven, clojars
- Common namespaces: clojure.*, babashka.*
- File extensions mentioned: .clj, .cljs, .cljc

**Emacs Libraries** (plugins/emacs-libraries/skills/):
- Library names with dashes (e.g., use-package, vertico)
- Keywords: emacs, elisp, package, mode, buffer, major-mode, minor-mode
- Common prefixes: evil-, ivy-, helm-, company-
- File extensions mentioned: .el
- References to: melpa, elpa, emacs packages

Default to clojure-libraries if unclear.

## Steps

1. **Infer Target Plugin**
   - Analyze library name and description
   - Apply inference rules above
   - Determine whether to use clojure-libraries or emacs-libraries
   - State your inference decision explicitly

2. **Research the Library**
   - Use WebSearch to find the library's official documentation
   - Identify the library's repository (GitHub, GitLab, etc.)
   - Find the latest version number
   - Understand the library's purpose, main features, and API
   - Identify common use cases and patterns

3. **Create Directory Structure**
   - Create `plugins/{inferred-plugin}/skills/{library-name}/`

4. **Generate SKILL.md**
   Structure:
   - frontmatter with name and description fields
   - Overview and introduction
   - Core concepts
   - API reference organized by category
   - Common patterns and best practices
   - Use cases
   - Error handling
   - Performance considerations
   - Platform-specific notes (if applicable)

   Make it comprehensive and practical. Be terse, concise and precise.

   For Clojure libraries: Include runnable examples in Babashka format
   For Emacs libraries: Include elisp code examples with setup instructions

5. **Report Completion**
    - State which plugin the skill was added to
    - List all files created
    - Show the skill's location

## Guidelines

- Follow all repository conventions from CLAUDE.md
- Make all examples practical and runnable
- Keep documentation clear and well-structured
- Research thoroughly before generating content
- Include error handling
- Add performance tips where relevant

## Notes

- All skills should be comprehensive enough to use the library without referring to external docs
- Focus on practical usage and common patterns
- Include both beginner and advanced content
- For Clojure libraries: Prioritize Babashka-compatible examples where possible
- For Emacs libraries: Include keybindings, customization options, and integration patterns

## README.md

Update @README.md to mention the skill.
