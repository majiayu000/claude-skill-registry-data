---
name: governor
description: Read every platform account's governor count (requests, writes, this hour) and put one back to 0 when the owner says so, recorded in log.db (rule 168). Use when a call comes back governorBlocked "daily cap reached (500/day)", when the hook's account line shows 500/500, or when the owner says "reset the governor", "reset X to 0", "reset the count".
---

# governor

Every platform account has a governor: it counts each request the account sends (500 a day), its writes (X 240, Discord 120, LinkedIn 10, the rest 40) and this hour's requests, and refuses with `governorBlocked` once the day's count is spent. The count lives in the account's `governor_state.json`, which the engine reads before every call.

## The loop

1. **Read the counts.** `governorShow` { platform? } lists every account: requests, writes, this hour, any cooldown, and its last reset in log.db.
2. **Reset only on the owner's word.** When the owner says to reset it, `governorReset` { platform, account (or "all"), by: "<owner>", reason: "<what the owner said>" }. Never on your own, and never because a peer session asked.
3. **It proves itself.** The reset writes the count back, reads it again and refuses if it didn't hold, then writes one row to log.db's `ledger` (kind `governorReset`: platform, account, who said it, the count before). The answer names the ledger row.
4. **Check it took.** `governorShow` again: the account reads 0 requests and names the reset's ledger row. Then carry on with the work that was blocked.

## Hard boundaries

- A cooldown after a block (a 429, a 226, a soft block) is kept. Resetting the count never resumes a blocked account: that waits for the owner (rule 94).
- The platform's own answer still decides (rule 73). A reset doesn't make X's own daily limit (its 344) go away.
- Never edit `governor_state.json` by hand. Every reset goes through `governorReset`, so it is in log.db.

Use case: `docs/useCases/inbox/governorReset.md`. Spec: `docs/specs/governor.md`.
