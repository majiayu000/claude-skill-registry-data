---
name: msb-profile
description: "What an agent inside a sandbox is told: profile/CLAUDE.md as the shipped central text, assemble_profile() appending the operator's ~/.config/msb/CLAUDE.local.md, the real file under ~/.local/state/msb/profile/ that is mounted read-only and copied into each sandbox's ~/.claude on every start, ensure_profile() appending sandbox_profile_section() (current_features, the git-push mode, and the project's guest path plus its .agents/skills/ folder) to the guest's copy only, and the AGENTS.md copy pi gets. Use when changing the central instructions or working out why an agent's context is missing something."
---

# Profile

Detail carved out of `AGENTS.md`, which keeps only what has to hold in
every session. Repo-specific throughout; the facts here are verified against
msb 0.7.6 and re-checked on 0.7.7.

- `profile/CLAUDE.md` — the SHIPPED central CLAUDE.md. `assemble_profile()` appends the operator's `~/.config/msb/CLAUDE.local.md` and writes the result to `~/.local/state/msb/profile/` (a real file, shared by every sandbox); that directory is what is mounted read-only and copied into each sandbox's `~/.claude` on every start. Nothing mounts or links a path inside the checkout or install tree. `ensure_profile()` then appends `sandbox_profile_section()` (`current_features()`, one line each, plus the git-push mode and the project's **guest** path with its `.agents/skills/` folder — this text lives in the agent's home, outside the mount, so any path a project's own docs point at has to be absolute here) to the guest's copy only, passed as an argument, never spliced into the script. Editing the copy in a sandbox does nothing.
