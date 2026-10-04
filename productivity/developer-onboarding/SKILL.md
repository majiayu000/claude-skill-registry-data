---
name: developer-onboarding
description: Write developer onboarding docs for repos, tools, libraries, and engineering workflows. Use when Codex is asked to create setup guides, first-run instructions, contribution paths, local development docs, or new maintainer onboarding.
license: MIT
---

# Developer Onboarding

## Core Workflow

1. Identify the target developer, prerequisites, platform assumptions, and first
   useful task.
2. Read existing setup scripts, package files, docs, tests, and repo structure.
3. Document setup, verification, common workflows, project layout, contribution
   path, and troubleshooting links.
4. Keep commands copyable and scoped by operating system or host when they
   differ.
5. Include validation checks so the user knows setup succeeded.
6. Flag missing automation, stale commands, or unclear ownership.

## Safety Rules

- Do not invent setup commands or environment variables.
- Do not include secrets or private service credentials in docs.
- Do not make one vendor or host mandatory when the repo supports alternatives.

## Deliverable Shape

For onboarding docs, provide:

- Audience and prerequisites
- Setup steps
- Verification checks
- Repository map
- Common workflows
- Contribution path
- Troubleshooting notes
- Open gaps

## References

- Read `references/developer-onboarding-checklist.md` when writing or reviewing
  onboarding docs.
