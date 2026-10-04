---
name: next-session
description: Pick up the next pending enhancement session (E4–E20) from the master plan, break it into TaskCreate items, and start work. Use when the user says "let's do the next session", "continue with E4", or "what's next on the plan".
---

# next-session

The project has a baby-step enhancement plan with 20 numbered sessions. This skill picks the next pending one and gets work moving.

## Steps

1. **Read** `Aqarkom_Knowledge/Sessions/Enhancement Plan E1-E20.md`. Look at the status table.
2. **Find the first row marked ⏳** — that's the next session.
3. **Read the linked detail** if it exists, or read the original plan body to understand the goals.
4. **Open the target page file** so you have current state in context (don't trust the plan note alone — code may have moved).
5. **Break the session into TaskCreate items**:
   - One task per checkbox in the session goal
   - Mark the first one `in_progress`
6. **Confirm with the user** before writing code: "Starting E{n} — {Page}. Plan: [bullet list of tasks]. Sound right?"
7. **Begin work** once confirmed.
8. When done, run `/complete-session`.

## Verification

- [ ] Tasks created with clear subjects
- [ ] User confirmed the breakdown
- [ ] Target page file actually read (not just the plan note)

## Notes

- If the plan note disagrees with the code (page was already partially enhanced), trust the code and adjust the plan in the vault.
- If the user wants to skip a session, mark it as `Skipped` in the plan with a note explaining why.
