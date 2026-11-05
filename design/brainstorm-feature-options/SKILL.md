---
name: brainstorm-feature-options
description: Used by the Lead agent during Phase 6 (Brainstorm) to collaboratively explore user intent, requirements, and alternative approaches before locking in the architecture. Helps turn raw ideas into fully formed specs through natural dialogue.
---

# Brainstorming Ideas Into Designs (Phase 6: Brainstorm)

## Overview

As the **Lead** agent in Phase 6, your role is to help turn ideas into fully formed designs and specs through natural collaborative dialogue. You are in a **read-only** role right now regarding application code — do not write implementation code. Your output here informs the Architecture phase.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**1. Understanding the idea:**
- Use your search tools (e.g., glob) to locate and read the feature description from the correct MANIFEST.yaml inside the .jonggrang/.output/features/ directory.
- Check out the current project state (files, docs, recent commits) to understand the existing domain.
- Ask questions one at a time to refine the idea.
- Prefer multiple choice questions when possible, but open-ended is fine too.
- Only ONE question per message - if a topic needs more exploration, break it into multiple questions.
- Focus on understanding: purpose, target audience, constraints, success criteria.

**2. Exploring approaches:**
- Propose 2-3 different approaches with trade-offs (e.g., minimalist vs. data-dense UI, server-side vs. client-side rendering).
- Present options conversationally with your recommendation and reasoning.
- Lead with your recommended option and explain why.

**3. Presenting the design concept:**
- Once you believe you understand what you're building, present the conceptual design.
- Break it into sections of 200-300 words.
- Ask after each section whether it looks right so far.
- Cover: user experience (UX), visual aesthetic direction, data flow, and error handling.
- Be ready to go back and clarify if something doesn't make sense.

## Key Principles

- **One question at a time** - Don't overwhelm the user with multiple questions.
- **Multiple choice preferred** - Easier to answer than open-ended when possible.
- **YAGNI ruthlessly** - Remove unnecessary features from all designs.
- **Explore alternatives** - Always propose 2-3 approaches before settling.
- **Incremental validation** - Present design in sections, validate each.
- **Be flexible** - Go back and clarify when something doesn't make sense.

## Completion

Once the user approves the overall approach and design concept, you must document the finalized design. Use your Write tool to save a summary (e.g., to `CONCEPT.md` in the feature's output directory) so the Architect has a persistent record.

Output the following completion signal exactly on its own line:
`BRAINSTORM_COMPLETE`
