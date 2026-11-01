---
name: code-review
description: Review Python source using the repo-review-kit Reviewer and analyzer.
---

For a source review, delegate a self-contained task to `repo-review-kit:reviewer`
using `subagent`. Include the workspace-relative file path and what to inspect.
The Reviewer reads the file and passes its source to
`mcp__repo-review-kit_analyzer__analyze_code`. Summarize the returned findings,
including line numbers, without modifying the source.
