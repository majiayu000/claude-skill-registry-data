---
name: nature-shared
description: Internal shared-reference support package for the local research skills (e.g., nature-figure, nature-statistics, nature-ref-verifier, nature-proposal-writer). Do not invoke it as a standalone user workflow. Load only the specific core or journal-format file requested by another skill.
---

# Nature Shared References

Use this package only as a dependency of another installed Nature skill.

- Load the exact referenced file; do not preload the whole package.
- Treat `core/` and `journal-formats/` as shared definitions, not standalone workflows.
- Return to the requesting skill for task logic, output format, and final QA.
