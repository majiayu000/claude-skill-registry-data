---
name: context-pack
description: Keep development token use low by refreshing and relying on local context packs.
allowed-tools: Bash, Read, Grep, Glob, Write
---

# Context Pack Skill

## When to use
- Before large refactors
- After finishing a feature chunk
- Before /compact

## What to do
1) Run /ctx-refresh (Gemini with cooldown)
2) Read context/local/context_pack.md
3) Base next steps only on that file + files you touch
4) If uncertain, write an OPEN QUESTION into context/local/decision_notes.md