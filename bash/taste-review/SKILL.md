---
name: taste-review
description: Ask Claude Code to make a taste-driven call on something ambiguous — UI polish, prose phrasing, naming, formatting. Use when you'd otherwise guess.
---

You hit something fuzzy and need a judgment call. Shell out to the `claude` CLI to get one back, then apply it.

Run from the repo root so `claude` can read files by relative path:

Run outside the sandbox when required, requesting reusable approval for the
`claude -p` prefix. On macOS, use the optional long-lived subscription OAuth
token from Keychain when present. Otherwise, fall back to that machine's normal
Claude authentication.
