---
name: docs-writer
description: Draft documentation updates with governed file-write proposals.
risk: medium
required_tools:
  - file.list
  - file.read
  - file.diff
  - memory.search
suggested_subagent: project-inspector
business_domain: documentation
cadence: task
approval_required_for:
  - file.write_safe
---

# Docs Writer

Use this skill when the user asks to create or update documentation.

Rules:
- Read nearby docs first and match existing tone.
- Preview diffs before writes.
- Do not write secrets, tokens, or protected operational details into public docs.
