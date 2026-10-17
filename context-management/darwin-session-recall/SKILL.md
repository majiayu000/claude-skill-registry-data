---
name: darwin-session-recall
description: Use when the user references past work or you suspect cross-session context exists.
---

# Darwin Session Recall

## Trigger
Use before asking the user to repeat prior decisions or paths.

## Procedure
1. Search session history for the referenced topic first.
2. Prefer direct sources (files, repos, DBs) over memory.
3. Link the found session inline rather than restating it.
4. If nothing found, say so plainly - do not guess.

## Pitfall
Session history is context, not proof of current state.

## Verification
After following the procedure: confirm the outcome
with real evidence (exit code, file, or API response).
```bash
python -c "import sys; print('darwin-species-ok')"
```
