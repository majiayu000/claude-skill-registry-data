---
name: cursor-advisor
description: "Advisor mode. Consult a stronger (or different) model at key checkpoints: before major decisions, when stuck on an error, and before declaring a task done. Use when the user types /advisor, asks to turn the advisor on or off, picks an advisor model, or explicitly asks for a second opinion from a stronger or different model. Never enable it on your own."
icon: lightbulb
color: purple
---

# Advisor for Codex

Use this skill only when the user explicitly asks for an advisor, a second opinion, or names `/advisor`. Never enable it automatically.

## Workflow

1. Confirm the decision, failure, or completion claim that needs review and prepare a bounded briefing with the user's request, relevant evidence, current state, options, and specific questions. Remove secrets and unrelated private context.
2. Spawn one bounded native reviewer or advisor through the current Codex collaboration surface. Use the operator-selected model and reasoning effort. Request read-only behavior and prohibit edits, external actions, and further delegation unless the user authorized them.
3. Record the returned native child identity and consume its verdict. Separate the advisor's recommendation from the coordinator's decision; the coordinator remains responsible for the result.
4. If the user asks another advisor question and the existing child remains suitable, use a native follow-up. Otherwise start a fresh bounded consult.
5. If native delegation is unavailable, return the completed briefing and say the consult was not run.

A project hook is optional automation. Do not create advisor state, register hooks, or claim automatic checkpoint reminders from this skill. The observed proof used `/root/advisor_native_proof` as a requested `reviewer` on `gpt-6-astra` at low effort and returned a no-write verdict; it does not attest backend enforcement beyond that requested selection.
