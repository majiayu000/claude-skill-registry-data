---
name: retro
description: Explicit retrospective of a coding session with evidence-backed suggestions for future work.
---

# Retro

Review the current coding session by default. Review another session only when the user specifies it and the evidence is accessible. Use the available writing-for-agents guidance when suggesting agent instructions.

1. Read the session's primary evidence and the repository's current instructions, check commands, and relevant tooling. Separate observed friction from conjecture.
2. Look for concrete improvements to navigation pointers, information access, instructions, tool economy, and checks. Recommend a check only when an observed mistake could have been caught and existing checks do not cover it. A missing CI job alone is not a finding.
3. Rank suggestions by impact and cost. For each, cite the session evidence, explain the mechanism, and give a concrete next action. State when evidence is insufficient.

Reviewers may need to inspect code and history to understand a change; do not assume a diff is enough. Treat mechanical checks, rules, and documentation as options whose costs must be justified by the observed failure.

This is a read-only suggestion workflow. Present proposed changes in chat; edit AGENTS.md, code, CI, memory, or issues, send messages, and start background tasks only when separately authorized. Existing explicit authorization remains effective.
