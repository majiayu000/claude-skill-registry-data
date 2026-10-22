---
name: gh-fix-ci
description: Use when a user asks to debug or fix failing GitHub PR checks that run in GitHub Actions. Uses `gh` to inspect checks and logs, summarize failure context, draft a fix plan, and implement only after explicit approval. Treats external providers (for example Buildkite) as out of scope and reports only the details URL. Do NOT use for addressing PR review comments (use gh-address-comments) or general CI outside GitHub Actions.
license: CC-BY-4.0
metadata:
  author: github.com/openai/skills
  version: 1.0.0
  owner_agent: codenavi-agent
---

# gh-fix-ci

Read and follow `00_skills/(tooling)/gh-fix-ci/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
