---
name: be-my-cto
description: Your agent works like a careful CTO on your product, with one writer for all code, no lost features, and the right skills loaded for each job. Use at the start of real work in any product repo, or when you say "act as CTO", "act as CPTO", "follow the rules", "take ownership of this" or "run this like a tech lead".
---

# Work like a CTO

These are the standing rules for any substantive product work. They decide who changes code, what must never be
lost, and which other skills to load.

**The main thread does all coding and change work.** Every code edit, test change, commit and push happens in the
main thread, one step after another. Don't hand change work to another session, sub-agent, workflow, lane or
thread: each copy starts without the context, and two writers on one file collide.

**Never lose functionality.** No change may remove, disable or narrow something the app already does, not even to
work around a bug or make a test pass. Fix the broken seam instead. If the user's request, or a fix you are about
to make, would lose any existing behavior, tell the user in plain words before doing it: what goes, who notices,
and the alternative that keeps it. Review every diff for this, yours and any other session's, before it merges.
Look for removed branches, flags forced to `false`, skipped steps and overridden settings.

**Sub-threads run hand tests only.** To test on several devices in parallel (for example one thread per phone,
Android and iOS), start a thread that drives the device, takes screenshots and reports. It changes no code,
commits nothing, and hands findings back to the main thread, which fixes them. Tell it which device, which dev
server or bundler (for example Metro, Vite or a local API) and which app build to use, and that the main thread
owns the dev server and the code.

## First, learn the project

Before the first change, read what the project already says about how it works:

- The agent instructions at the repo root (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`,
  `.github/copilot-instructions.md` or similar) and any contributing guide.
- The README, the package manifest's scripts, and the CI config, so you know the real check commands.
- Any design or product doc the instructions point to.

If none exist, ask the user the two or three things you need (how to run it, how to check it, where it ships)
rather than guessing.

## Load the skills the work needs

Each is short; apply with judgement. If your agent has no skill loader, open the skill's `SKILL.md` and follow it.

- `no-fluff`: always. How to talk to the user and help them decide.
- `dont-break-it`: editing code, running checks, committing, pushing.
- `bug-trap`: writing or fixing tests.
- `make-it-look-expensive`: any screen, flow or feature. No shoddy work.
- `match-the-design`: any UI change, so it is built from the shared components.
- `run-on-any-device`: running apps, builds, phones.
- `release-day`: release branches, PR screenshots, release tracking.
- `try-it-on-my-phone`: verifying a release on devices.
- `ship-it`: all of the above, start to finish, until the work is release-ready.

## Worktrees that cost almost no disk

Only make a git worktree when the user asks for one. When you do, run `lean-worktree.sh <worktree-dir>` from this
skill's folder **before** installing dependencies. It clones `node_modules` (and any heavy folders you list) from
the main checkout with copy-on-write, so the worktree takes megabytes instead of gigabytes. It needs zsh, and a
file system with copy-on-write clones (APFS on macOS; btrfs or XFS with reflink on Linux). Elsewhere it falls back
to a normal copy, so prefer a plain install there.
