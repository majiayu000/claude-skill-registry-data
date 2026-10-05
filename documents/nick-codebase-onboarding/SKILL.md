---
name: nick-codebase-onboarding
description: Practical codebase onboarding for Nick's workflow. Use when opening a stale project, picking up a new repo, rebuilding context after time away, or generating fast markdown docs that explain how to start working on a codebase right now. Focus on setup, key files, flows, commands, risks, and what to touch first.
---

# Nick Codebase Onboarding

Use this as the default onboarding/ramp-up skill.

## Purpose
Generate practical onboarding docs that answer:
- what is this project?
- how do I run it?
- where do I start editing?
- what are the key flows?
- what is risky or stale?
- what should I test first?

## Hard rules
- Focus on how to start working right now
- Prefer practical repo orientation over academic architecture docs
- Highlight commands, entry points, and likely break points
- If the project is stale, call out likely outdated areas
- Surface env/setup blockers early

## Default workflow
1. Scan top-level structure
2. Identify stack and major config files
3. Identify app entry points, routes, API surfaces, and data/auth wiring
4. Identify core commands to run, build, test, and deploy
5. Identify risky, stale, or confusing areas
6. Generate onboarding markdown

## Default output
- Project summary
- Start here
- Setup checklist
- Key commands
- Important folders/files
- Main flows and data/auth wiring
- Risky areas / stale areas
- First things to test
- First safe edits to make

## References
- Read `references/onboarding-sections.md` for the output structure
- Read `references/stale-project-checklist.md` when a repo looks old or neglected
- Read `references/next-supabase-orientation.md` for App Router + Supabase projects
- Read `references/handoff-notes.md` for practical developer handoff style

## Bundled scripts
- `scripts/init_onboarding_doc.sh` — create onboarding markdown stub
- `scripts/generate_project_kickstart.sh` — create a fast "start here" guide
- `scripts/generate_stale_repo_review.sh` — create stale-project review checklist
