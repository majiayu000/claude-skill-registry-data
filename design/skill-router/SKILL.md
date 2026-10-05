---
name: skill-router
description: Select and coordinate Codex skills when several skills, plugins, agents, or workflows could apply to the same user request. Use when there is skill overlap.
---

# Skill Router

Select, order, and combine skills. Resolve overlaps so the user does not have to choose between similar skills.

## Routing Rules

1. Honor explicit user choice first.
   - If the user names a skill or plugin and it is available, use it unless it is clearly unsafe, unavailable, or irrelevant.
   - If the named skill is not available, say so briefly and choose the closest available fallback.

2. Prefer the narrowest skill that directly matches the task.
   - Use artifact-specific skills for file formats and tools: `pdf`, `pptx`, `xlsx`, `docx`, `figma`, `browser`, `github`, `vercel`.
   - Use domain-specific skills for subject matter: `academic-pptx`, `security-review`, `contract-reviewer`, `bio-research`.
   - Use generic skills only when no narrower skill fits.

3. Separate "what" from "how".
   - Content/domain skills decide substance and standards.
   - Tool/file skills perform the technical work.
   - Example: an academic slide deck uses `academic-pptx` for structure and `pptx` for file generation.

4. Use one primary skill by default.
   - Pick one primary skill that owns the main workflow.
   - Add supporting skills only when they cover different responsibilities.
   - Avoid loading multiple similar skills that give duplicate guidance for the same responsibility.

5. Combine skills only when responsibilities are complementary.
   - Good: `figma-implement-design` plus a project frontend skill.
   - Good: `security-review` plus `dependency-security-audit`.
   - Good: `workflow-orchestrator` plus one specialist per phase.
   - Bad: several broad frontend design skills all trying to control the same UI decisions.

6. Resolve conflicts by this priority order:
   - Current system/developer instructions.
   - Explicit user instruction in the current turn.
   - Project-local files and conventions.
   - Narrow, task-specific skill.
   - Plugin/tool-specific skill for the active platform.
   - Broad workflow or generic quality skill.

7. Ask only when the conflict changes the outcome.
   - If one choice is clearly safer and reversible, proceed and mention the choice.
   - If two skills imply incompatible behavior, ask a concise clarification before changing files or committing to a direction.

8. Keep meta-skills contained.
   - `skill-updater` may diagnose and propose skill edits, but should not edit skills without explicit approval for the exact change.
   - `continuous-learning-v2` may propose learning artifacts, but should not evolve or write durable skills automatically.

## Known Conflict Table

### Debugging

| Situation | Prefer | Avoid |
|---|---|---|
| General bug or broken build | `debugging-and-error-recovery` | Tiny generic debuggers |
| Polling, race conditions, or browser timing issues | `systematic-debugging` | Generic debuggers |

### Security

| Situation | Prefer | Avoid |
|---|---|---|
| Security while implementing a feature | `security-and-hardening` | Generic security auditors |
| Auth or API endpoint review | `security-review` | Generic security auditors |

### Code Quality

| Situation | Prefer | Avoid |
|---|---|---|
| Comprehensive review | `code-review-and-quality` | Narrow review helpers |
| Ultra-short PR comment review | `caveman-review` | Broad quality workflows |

### Frontend and UI

| Situation | Prefer | Avoid |
|---|---|---|
| Build a component or page from scratch | `frontend-ui-engineering` | Broad visual-only skills |
| Improve visual quality | `high-end-visual-design` | Multiple broad frontend style skills together |
| Redesign an existing project | `redesign-existing-projects` | Starting over with a generic frontend skill |
| UX rules and patterns | `ui-ux-pro-max` | Overlapping taste guides |
| Tailwind rule checking | `baseline-ui` | Broad design skills |

### Testing and Browser Work

| Situation | Prefer | Avoid |
|---|---|---|
| General Playwright work | `playwright-skill` | Unfocused webapp testing helpers |
| Complex test architecture or CI | `playwright-best-practices` | Simple Playwright helper only |
| Live browser debugging | `browser-testing-with-devtools` | Static-only inspection |

### Web Research

| Situation | Prefer | Avoid |
|---|---|---|
| Broad search and scraping | `firecrawl` | Redundant single-purpose search helpers |
| Multi-source research | `deep-research` | `quick-research` for deep work |
| Fast summary | `quick-research` | Deep research workflows |
| Library documentation lookup | `find-docs` | General web scraping first |

## Common Pipelines

### New Feature to Production

```text
spec-driven-development
-> incremental-implementation
-> security-and-hardening when auth or input handling is involved
-> code-review-and-quality
-> playwright-skill when UI is involved
-> verification-before-completion
-> finishing-a-development-branch
-> shipping-and-launch
```

### Existing Code Is Broken

```text
debugging-and-error-recovery -> refactor -> verification-before-completion
```

### Web Research to Report

```text
deep-research -> content-research-writer
```

### UI Design to Code

```text
high-end-visual-design or ui-ux-pro-max
-> frontend-ui-engineering
-> baseline-ui when Tailwind is used
-> browser-testing-with-devtools
```

## User-Facing Note

When the routing choice matters, state it briefly:

```text
I am using `academic-pptx` as the primary skill and `pptx` as the supporting file-generation skill.
```

Do not narrate every skill selection for small tasks. Use this note only when it prevents confusion or explains a tradeoff.

## Anti-Patterns

- Do not activate every skill that might be related.
- Do not let broad workflow skills override a narrower specialist.
- Do not use two similar skills in parallel unless comparing alternatives is the task.
- Do not use skill routing as permission to edit skill files.
- Do not ask the user to choose between skills when one choice is obvious from the request.

## Changelog

- [2026-05-11] Converted all Turkish routing text to English.
- [2026-05-10] Initial version: added skill selection, overlap resolution, coordination patterns, and safeguards for updater/learning skills.
