---
name: learned
description: The dag/stagehand PR-pipeline playbook. Use when working the dag/stagehand PR pipeline, when driving multiple cmd/opencode agents through herdr, or whenever a PR must go adversarial-review -> whiteboard -> refiner -> merge. Covers worktree-per-issue, the four gates, identity tags, compressed-Chinese comms, the greedy/background law, matt triage, and local whiteboard export.
---

# learned — the dag PR-pipeline playbook

Standing operating knowledge from the dag/stagehand PR work. Follow it.

## Pipeline
- One worktree per issue: `~/worktrees/pr-<N>`, branch `<type>/<N>-<slug>`, base = latest `origin/main`. Never reuse a worktree; never touch `~/dag`'s own working tree.
- Integration branch is `main`. `dag-rust-port` is retired (91 commits behind main; lacks `src/events.rs`, `src/watchdog.rs`).
- Do NOT run `dag` inside a worktree. The merge "no-git" test commits the tree as `"node a"`/`"node b"` on every `cargo test`; gate runs must keep the no-git scratch rooted in `std::env::temp_dir()`.

## Gates (run before and after every change)
1. `cargo fmt --check`
2. `cargo clippy --all-targets`
3. `cargo test --quiet`
4. `bash tests/parity.sh`

Baseline is RED (fmt/clippy/parity); tests must stay green. Record counts before->after; never worsen. No new CLI flag (`USAGE` is byte-compared by `parity.sh`).

## Review order (NEW work only)
1. Adversarial AI review FIRST — `tiger-style` (full) + `ponytail` (full) on the pushed branch/PR.
2. Only after that, author the whiteboard PR review.
3. Then a SEPARATE refiner agent rewrites the whiteboard into a human-readable narrative (what changed, why, before/after, tradeoffs, risks) — not a raw diff dump.
4. Human reviews, then merge. Never whiteboard before the adversarial review.

## Merge rules
- Merge only after review + all must-fixes fixed. Merge stacked PRs in order (stacked first).
- Bug fixes need red->green proof: neutralize the guard, show the test fail, restore, show it pass.
- Prove the base: `git merge-base origin/main HEAD` must equal the latest `origin/main` SHA and `git rev-list --count HEAD..origin/main` == 0.

## Comms
- herdr: `herdr pane send-text <pane> "<msg>"` then ALWAYS `herdr pane send-keys <pane> enter`. Orchestrator pane = `w6D:p1`.
- Identity tag on every shared message/comment: `[ai:<pane>#<ticket>]`; humans use `[human]`.
- Language: agent<->agent and agent->orchestrator = compressed Chinese (commands/paths/IDs verbatim); PRs, commits, docs, whiteboard = English.
- Report blockers immediately; flag-and-stop when a ticket is already decided/parked.

## Greedy law
- Anything parallelizable runs detached (`background=true`) — never block.
- graft-first navigation; delegate to subagents; keep context lean; return compact JSON.
- Watch only `agent_status`; never read pane text except on an anomaly. Use zero-LLM shell monitors for status.

## Triage
- matt `/triage`: category (bug|enhancement) + state (needs-triage|needs-info|ready-for-agent|ready-for-human|wontfix). Check `DECISIONS.md` and issue #29's parked list; only hand out `ready-for-agent` tickets.

## Whiteboard (local, no Desktop needed)
- `whiteboard --state-dir /home/prm/.dev api session_list`
- `whiteboard --state-dir /home/prm/.dev api session_get '{"sessionId":"<id>","full":true}'`
- `whiteboard --state-dir /home/prm/.dev api session_lens_get '{"sessionId":"<id>"}'`
- Export to local `.md`/`.html` for the human.
