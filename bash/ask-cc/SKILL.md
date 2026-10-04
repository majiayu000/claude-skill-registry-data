---
name: ask-cc
description: Ask Claude Code to make a taste-driven call on something ambiguous — UI polish, prose phrasing, naming, formatting. Use when you'd otherwise guess.
argument-hint: "The question + any file paths to consider"
---

You hit something fuzzy and need a judgment call. Shell out to the `claude` CLI to get one back, then apply it.

Run from the repo root so `claude` can read files by relative path:

Claude Code stores subscription OAuth credentials in macOS Keychain. Codex's
filesystem sandbox cannot read them, so a sandboxed `claude auth status` may
incorrectly report `loggedIn: false`. Run the `claude -p` command outside the
sandbox, requesting approval for the reusable `claude -p` prefix. Only ask the
user to log in if `claude auth status` also fails outside the sandbox.

```bash
claude -p "$(cat <<'EOF'
<your question, stated plainly>

Files to consider: <paths, if any>

Weigh a few options, give your recommendation, and share others as alternatives considered.
Length is up to you — a design call may warrant several paragraphs;
a naming call may not. Match the depth to the decision.
EOF
)"
```
