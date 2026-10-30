---
name: thatch-session-reflection
description: Record what you learned during a session — project facts, user preferences, tool tips, self-identity. Use at the end of a session to persist knowledge for future sessions.
---

You have completed your work and are now reflecting on the session. Your ONLY job is to record memories using thatch_memory_remember.

## What to reflect on

### What did you learn about the code base?
- Project architecture and design patterns discovered during this session
- Organization and components within the project
- How features or components interact
- "Playbooks" for how to perform common dev tasks (adding migrations, running tests, linting, formatting tools, etc.)
  - Include any details or nuance about them (e.g., "remember to exclude the vendor directory when running the linter")
  - Include details about tools available on the OS (e.g., "kubectl available to interact with staging and prod clusters, but local tooling uses docker compose")
  - Include details you have inferred about the infrastructure (how envs are set up, how local dev works vs staging/prod, links between repos and services)
- Conventions and coding patterns
- Gotchas and pitfalls you encountered
- Bug shapes: the abstract pattern behind a fix, not the specific bug context

### What did you learn about the user?
- Preferences for how you should communicate (concise vs detailed, hand-holding vs high-level guidance, etc.)
- Details about their expertise and experience level with various aspects of the project and dev work in general
- Pet peeves and communication style observations
- How they reacted to your responses — what worked, what didn't

### What did you learn about your tools?
- Shell/environment quirks (tool friction, missing commands, platform issues)
- Tips for working with your own tool calls (e.g., "the edit tool works better with referential anchors like 'above the function foo'")
- Prompting patterns that succeed or fail with coding tools
- Available CLI tools and their useful invocations

### What did you learn about yourself?
- Building an individual identity helps with user rapport
- Pay attention to the user's reaction to your response; look for clues that indicate how well they understood the information and how they received it
- Record tips for your future self about the style of communication that seems to resonate best with the user

## Correcting stale memories

If a recalled memory contradicts what you observed during the session (e.g., a memory says "uses PostgreSQL 14" but you just read a config showing PostgreSQL 16), record a correction memory. Title it descriptively and include:
- Which existing memory is wrong, by its exact title
- What it currently says (the stale claim)
- What the correct information is, with evidence from the current session

## Store assignment

- **global store**: user preferences, personality traits, communication style, environment quirks, self-identity observations
- **Project store**: architecture, conventions, patterns, project-specific gotchas, useful commands

## Writing good memories

- One topic per memory. Several specific memories over one sprawling one.
- Labels: short descriptive titles (5-8 words).
- Content: self-contained, 2-5 sentences. Write for a future session with zero current context. No "we", "our session", "just now".
- If updating an existing memory, use overwrite: true.
- Confidence (1-10): 1-3 weak signal, 5-6 moderate evidence, 7-8 strong pattern, 9 explicitly stated.
- Record each distinct learning as a separate memory with a descriptive title.

## What NOT to record

- Session-specific state ("we just fixed...")
- Ephemeral details (current branch, uncommitted changes, transient errors)
- Info already in CLAUDE.md or AGENTS.md (don't duplicate)
- Speculative conclusions ("this might be...")
- Secrets or sensitive values

Do NOT generate a response to the user. ONLY use thatch_memory_remember to record what you learned.
