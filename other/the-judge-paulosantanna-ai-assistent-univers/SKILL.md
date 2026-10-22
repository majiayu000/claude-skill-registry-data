---
name: the-judge
description: Evidence-first pull request judge that reviews a PR and posts one consolidated GitHub review with inline comments via the gh CLI. Runs the repo's own deterministic checks first, researches current official docs before any claim about external libraries or APIs, then reviews correctness, security, structural quality (code judo, spaghetti growth, file-size limits), and AI slop including useless code comments. Every finding must carry evidence, every comment passes a deterministic noise gate before posting, and the verdict (APPROVE, COMMENT, REQUEST_CHANGES) is weighed by findings. Use when asked to review a PR, judge this PR, review this branch or diff before merge, run the-judge, "revise esse PR", "faca o code review", or "julgue esse PR". Do NOT use for reviewing prose or documents, fixing CI failures, resolving merge conflicts, writing the fix itself, or responding to review comments (use gh-address-comments).
license: CC-BY-4.0
metadata:
  author: Felipe Rodrigues - github.com/felipfr
  version: 1.4.0
  owner_agent: codenavi-agent
---

# the-judge

Read and follow `00_skills/(quality)/the-judge/SKILL.md` and its relevant local modules.

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; no additional agent identity.
