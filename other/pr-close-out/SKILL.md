---
name: pr-close-out
description: Run the full PR lifecycle and session-migration procedure for grc_library. Load before authoring any change (including ordinary documents and CHANGELOG), before the first and every later commit, after every commit, before every push or PR creation, before merge, and at session wind-down.
---

# PR close-out

This skill is a trigger wrapper. The procedure of record is
`.claude/playbooks/pr-lifecycle.md` (gate 80 manifest-enforced). Read the ENTIRE playbook
before authoring; its sections overlap in time. Apply them at these execution points:

1. During authoring (workflow step 1), apply the checklist's measurement, history,
   and paired-surface rules and every applicable change-impact row, including websites.
2. Before the first commit, run explicit-path language/fence checks and changelog
   preflight. Before EVERY commit, run version-recency checks and confirm Version/Date
   bumps; after EVERY commit, run the standalone audits required by workflow step 1.
3. Before EVERY push or PR creation (step 2), complete the applicable checklist,
   impact-map sweep, all four version surfaces, and attribution checks, then run the
   guard and push unpiped. Open the PR only after the guard passes.
4. After opening the PR, wait for green CI (step 3), then run finalizing `/validate-pr`
   and `/retro` (steps 4-5). Resolve findings, write THIS PR's returned rows in THIS PR,
   refresh the handoff, queue and TODO/DONE records (steps 6, 9-10), and repeat the
   commit checks and guarded push for those changes. These rows are required before
   the final push and merge; the initial PR creation precedes its own QA rows.
5. Wait for CI on the final SHA, recheck the complete checklist and merge guard, then
   merge (step 7). Sync and delete the branch (step 8), and publish the next five
   planned PRs (step 9). Session-closing QA and handoff requirements apply before merge.

Do not substitute an abbreviated or memory-only pass for reading the playbook.
