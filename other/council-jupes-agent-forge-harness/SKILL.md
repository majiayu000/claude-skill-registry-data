---
name: council
description: /council — Deliberative multi-provider review. Use when the user runs /council.
---

# /council — Deliberative multi-provider review

Review a PR, plan, research document, or supplied text using the shared council engine.

## Usage

```
/council pr <number-or-url> --profile councils/multi-provider.example.json
/council plan <path> --profile councils/my-council.json
/council file <research.md> --profile councils/my-council.json
```

1. Resolve the user's artifact and intended scope. Include relevant acceptance criteria and supporting code/document excerpts; council models do not browse or inspect the repository independently.
2. Run `bun run council -- <source-kind> <source> --profile <profile> --dry-run --json`. Check the envelope's `ok`, readiness, truncation, and budget. Never print or request API keys in chat. Without a hosted profile, explain that the default profile is only a deterministic demo.
3. Run the same command without `--dry-run`, with the user's budget when supplied. This sends the source to every selected provider. Do not change providers or expand disclosure beyond the user's chosen profile.
4. Read the returned `run`, including limitations, failures, unreviewed or contested findings, and reviewer rationales. An unsuccessful envelope may still contain a preserved run and artifacts; report them.
5. Present the chair's recommendation with evidence and disagreements. A council verdict is advisory, not permission to edit, approve, merge, or post a GitHub review.

For interactive use: `bun run dashboard`, then `/council.html`. For another agent or system, prefer MCP `council_start` followed by `council_status`, avoiding a long blocking tool request. See `docs/COUNCIL-REVIEWS.md`.
