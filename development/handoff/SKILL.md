---
name: handoff
description: Codex handoff checklist for agents.
---

# Handoff

Purpose: package the current state so the next agent (or future you) can resume quickly.

Include (in order):
1) Scope/status: what you were doing, what’s done, what’s pending, and any blockers.
2) Working tree: `git status -sb` summary and whether there are local commits not pushed.
3) Branch/PR: current branch, relevant PR number/URL, CI status if known.
4) Running processes: list tmux sessions/panes and how to attach:
   - Example: `tmux attach -t codex-shell` or `tmux capture-pane -p -J -t codex-shell:0.0 -S -200`
   - Note dev servers, tests, debuggers, background scripts, and how to stop them.
5) Tests/checks: which commands were run, results, and what still needs to run.
6) Changelog + docs: mention if `CHANGELOG.md` or docs were updated and why (not the sole source of truth).
7) Next steps: ordered bullets the next agent should do first.
8) Risks/gotchas: any flaky tests, credentials, feature flags, or brittle areas.

Output format: concise bullet list; include copy/paste tmux commands for any live sessions.
