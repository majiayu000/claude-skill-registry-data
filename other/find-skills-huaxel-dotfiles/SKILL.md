---
name: find-skills
description: Discover and assess installable agent skills when the user asks to find a skill, compare skill packages, or extend agent capabilities. Not for ordinary “how do I” or “can you” requests that can be handled directly.
---

# Find Skills

Find a skill for the requested capability, not a package to install by default.

1. Check the existing skill catalog first. Prefer a suitable installed skill over a duplicate.
2. Search source repositories or skills.sh for focused candidates. The optional Skills CLI supports `npx skills find <query>`; invoking npx can download and execute code, so use it only when the package is trusted and execution is appropriate.
3. Inspect the candidate’s actual `SKILL.md`, bundled scripts, dependencies, and environment assumptions. Check task fit, provenance, maintenance, permissions, and external effects. Stars and install counts help discovery; they do not establish quality or safety.
4. Recommend a small set with concrete tradeoffs and source links. Label anything you could not inspect.
5. Install only when requested, after review. Prefer one canonical copy under the shared skill root; preserve local changes and avoid duplicating harness-specific copies. If using `npx skills add <owner/repo@skill> -g`, inspect the planned destinations and do not use automatic confirmation to bypass unresolved choices.

If no candidate fits, do the task directly or propose a narrowly scoped new skill. Do not make skill installation a prerequisite for ordinary assistance.
