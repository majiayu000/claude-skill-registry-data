---
name: skills-squash-message
description: Use when preparing a squash commit message for a pull request in the Scenario skills repository.
license: MIT
metadata:
  internal: true
---

Generate a single squash commit message for the current PR.

1. Run `git fetch origin main --quiet && git log --oneline $(git merge-base HEAD origin/main)..HEAD` for the branch's commits, then read the net diff against main (`git diff $(git merge-base HEAD origin/main)..HEAD`). The message describes the diff, not the journey: a branch commit that reworks something introduced earlier in the same branch is folded into the item it amends, never listed as a fix.
2. Write ONE conventional commit message that passes `commitlint.config.js`:
   - Title: `type(scope): summary`. Type feat, fix, docs, or chore (never chore for shipped skill content: release-please drops it from the changelog); scope a skill directory name or one of the cross-cutting scopes (skills, agents, ci, deps, docs, tooling). Aim under 72 characters; the hard cap is 120.
   - Body: what changed and why, for someone skimming `git log` a year from now. The problem in a sentence or two, then the change: one sentence, or up to five bullets of one or two lines when the PR lands several distinct things. A dozen body lines at most. Leave out the evidence trail, the per-file inventory, argument shapes, word counts, review history, and anything the diff shows on its own. Wrap at 72 columns. No em dashes.
   - Footer: read the branch's commit bodies with `git log --format=%B $(git merge-base HEAD origin/main)..HEAD` and preserve every distinct `Co-authored-by:` trailer after a blank line. Follow AGENTS.md's "Codex commit attribution" section for Codex contributors.
3. Write the exact message to a temporary file and verify it passes: `pnpm exec commitlint --edit <file>`.
4. Copy it with `pbcopy < <file>` when available; otherwise show the message without a clipboard step.
5. Show the message, and nothing else.
