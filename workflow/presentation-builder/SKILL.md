---
name: presentation-builder
description: "Build a presentation: an animated video from an idea, essay, or script plus audio; a .pptx deck; or an HTML slide deck."
license: MIT
---

# Presentation builder

Choose the procedure matching the output the user asked for. Paths within a procedure are relative to that procedure's folder.

- [Animated video](references/video/WORKFLOW.md) — use to build a captioned 1920×1080 MP4 from an idea, an essay, or an existing script plus master audio, through the presentation-builder pipeline.
- [PowerPoint deck](references/pptx/WORKFLOW.md) — use to create, read, edit or render a `.pptx` file with python-pptx.
- HTML slide deck — use the `claude-design` skill. A fixed-size HTML deck is one of its artifacts, and it owns the design process.

A presentation request does not authorize publishing, uploading or sending the result. Keep provider keys and repo paths in the environment, never in a procedure or the repo.
