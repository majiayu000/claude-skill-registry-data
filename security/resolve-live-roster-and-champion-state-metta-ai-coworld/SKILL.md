---
name: resolve-live-roster-and-champion-state
description: Use before evaluations or after roster churn to resolve live policy versions and restore the champion flag.
---

# Resolve live roster and champion state

The crewrift league is volatile in two ways that break launches and delist users:

1. **Champion flag is fragile.** Submitting or retiring a league-policy membership
   (or any champion/slot rotation) can silently clear `is_champion` on the
   *surviving* policy. The division leaderboard lists only players holding a
   champion, so the user disappears from standings entirely. This recurred twice
   in one day during the tier5c campaign. (session-derived, unverified)
2. **pvids roll mid-session.** Live league members re-version frequently
   (e.g. crewborg v19→v21→v22, truecrew-Jr v13→v15 in a single day). A
   `policy_version_id` resolved earlier in the session, or read from an old round
   result, will be rejected by the server as "did not match an active runnable
   policy." Always re-resolve from the *live membership list* right before a launch.

This recipe (a) re-resolves every live pvid you will launch against, (b) audits
the COMPLETE roster (never a name-filtered slice), and (c) verifies + restores the
champion flag and leaderboard presence.

## Constants (crewrift, server `https://softmax.com/api`)

- Server: `https://softmax.com/api`; raw Observatory paths live under `{server}/observatory`.
- League (Crewrift Daily): `league_605ff338-0a2e-4e62-aeda-559df9a9198f`
- Divisions:
  - Wood (top): `div_c2be3343-f046-4c21-8674-267b5797a059`
  - Dirt: `div_43e71661-556f-4fba-a6e1-bfc6e898f3d8`
  - Qualifiers: `div_71f55782-07fc-43…` (truncated in source; resolve the full id from
    `GET {server}/observatory/v2/leagues/{league_id}` if you need Qualifiers)
- Coworld (crewrift 0.1.36): `cow_6b70b662-2211-4313-a50e-4a2d26585e5e`

## Auth (do this once per session)

```bash
uv run softmax login
```

Then in Python, either the typed client:

```python
from coworld.api_client import CoworldApiClient
client = CoworldApiClient.from_login(server_url="https://softmax.com/api")
http, hdr = client._http_client, client._headers()   # raw HTTP; base_url = {server}/observatory
```

…or plain `httpx` with `X-Auth-Token` from `softmax.auth.load_current_cogames_token()`
(the pattern `watch_v5.py` uses). Hit raw routes via `http.get("/v2/...", headers=hdr)`.

## Step 1 — Re-resolve live pvids (drives the `league_roster` tool)

Use the `league_roster` tool in this package (`universal/tools/league_roster.py`).
Its `live_members(client, league_id=..., division_id=...)` returns one row per live
player — `{player_id, player_name, label, policy_version_id, score}` — sourced from
`list_memberships(..., active_only=True)`, which carries the CURRENT pvid per member.
This is the authoritative "who is runnable right now" list; do not reuse pvids from
old round results.

```python
from league_roster import live_members, fetch_top_players

LEAGUE = "league_605ff338-0a2e-4e62-aeda-559df9a9198f"
WOOD   = "div_c2be3343-f046-4c21-8674-267b5797a059"

rows = live_members(client, league_id=LEAGUE, division_id=WOOD)
for r in rows:
    print(r["player_name"], r["label"], r["policy_version_id"], r["score"])

# Fill the other 7 A/B seats with the top live opponents, excluding yourself:
opponents = fetch_top_players(
    client, league_id=LEAGUE, exclude_player_id="<your_player_id>", top_n=7,
    division_id=WOOD,
)  # raises ValueError if fewer than 7 distinct live competitors exist
```

Validate EVERY pvid you are about to launch against the just-fetched `live_members`
rows — the snapshot must be from THIS step, not an earlier one in the session.
(session-derived, unverified) Also resolve a policy *name* → pvid only via
`client.lookup_policy_version(name=...)`; a missing policy is a hard error (uploading
is out of band, never auto-triggered here).

**Seat-order gotcha for swap tournaments:** when a comparator you launch is *also*
one of the 7 field opponents, you cannot seat-verify it by unique pvid (the same pvid
appears twice). Opponents land in LIST ORDER in the roster body — verify those seats
by *position*, not by pvid match. (session-derived, unverified)

## Step 2 — Audit the COMPLETE roster (name-UNFILTERED)

Pull every membership, not a substring-filtered view. A monitoring script that filtered
membership names on `"tier"` missed an unauthorized membership a subagent had submitted
in breach of a no-submit instruction; it stayed invisible for a full day and only
surfaced during a full roster pull. (session-derived, unverified)

```python
cursor = None
while True:
    # NO name filter
    member_page = client.list_memberships(
        league_id=LEAGUE, active_only=True, cursor=cursor
    )
    for m in member_page.entries:
        pid   = str(m.player.id if m.player else m.policy_version.player_id)
        pname = m.player.name if m.player else m.policy_version.label
        print(pid, pname, m.policy_version.label, m.policy_version.version, str(m.policy_version.id))
    if member_page.next_cursor is None:
        break
    cursor = member_page.next_cursor
```

Cross-check every row against the policies you *expect* to own. Any membership you did
not knowingly create is unauthorized — investigate it. Keep all league-visible actions
(submit, retire, champion swap, version roll) exclusive to the lead agent; subagents
must not submit. (session-derived, unverified)

## Step 3 — Verify + restore the champion flag and leaderboard presence

The leaderboard lists only champion-holders, so "vanished from standings" almost always
means the champion flag got cleared by churn — NOT that the policy was deleted.

1. Pull the division leaderboard and confirm your player appears:

   ```python
   # raw route; official rank = mean_round_score
   resp = http.get(f"/v2/divisions/{WOOD}/leaderboard", headers=hdr)
   entries = resp.json()["entries"]   # each has mean_round_score, rounds_played, recent_rounds
   present = any(e for e in entries if e["player"]["id"] == "<your_player_id>")
   ```

   CLI equivalent for a quick eyeball: `uv run coworld results <division_id>`.

2. If your player is ABSENT (or you confirm the flag is off on the intended policy),
   restore the champion flag on the correct membership:

   ```
   POST {server}/observatory/v2/league-policy-memberships/{lpm_id}/champion
   ```

   `{lpm_id}` is the league-policy-membership id of the policy that should carry the
   champion (the membership row from Step 2 for your intended policy). (session-derived,
   unverified)

3. Re-pull the leaderboard (step 3.1) and confirm the player is now listed.

**"champion" is a leaderboard-SCORING slot, not winner/#1.** Each user has two players
(experiment + champion). The champion flag just determines which player's score the
leaderboard shows; judge success by mean round score vs the field, never by the
`champion` membership label itself.

## When the issue is ledger age, not the flag

If the player is *present* on the leaderboard but rank stops responding to real
improvements — and "why are we losing to X" resolves to ledger age (a rival running an
equal-strength fork of your bot on a younger ledger) — this is the lifetime-mean anchor,
not a churn/flag problem. The crewrift leaderboard is a LIFETIME mean over all of a
player's rounds (~430-round means move ~0.01 per new round). The remedy is a second
player identity carrying the same policy image with clean history (an aliased policy =
same image, new name, registers without a rebuild). (session-derived, unverified)

**Automation boundary:** player-management routes (create player, rename, set-default,
credentials) require the user's WEB session. The CLI token is player-scoped and binds
everything it creates to the existing player, so an agent can stage the alias and the
submission, but the **default-player flip must be handed to the human** — the staged
alias 409s at the final submit against the web-session auth boundary. Do not try to
automate past this; hand off. (session-derived, unverified)

## Gotchas

- **Re-fetch right before EACH launch.** The roster churns mid-session; a pvid resolved
  minutes ago may be stale. Re-run Step 1 immediately before submitting, not once at the
  top of the session. (session-derived, unverified)
- **Never name-filter the roster audit.** A substring filter hid a rogue membership for a
  day. Step 2 must enumerate all memberships. (session-derived, unverified)
- **`list_memberships(mine=True)` throws a schema-drift ValidationError today** — pull the
  full league list and filter client-side instead.
- **Division leaderboards may read empty/null;** `softmax_pull.py` coerces null leaderboards
  to `[]`. If standings come back empty for everyone (not just you), it's an API gap, not a
  delist — don't restore a flag that isn't actually cleared.
- **Don't conflate "absent from leaderboard" with "policy deleted."** Check the flag and the
  full roster (Steps 2–3) before assuming anything was retired.

## Success check

- Every pvid you will launch against was pulled from `live_members` in THIS session (Step 1),
  and `fetch_top_players` returned a full 7-opponent set without raising.
- The full, name-unfiltered membership list (Step 2) contains only policies you knowingly own
  — no unrecognized/unauthorized membership.
- Your intended player appears on the target division leaderboard with a `mean_round_score`
  (Step 3); if it had vanished, the `POST .../champion` restore was applied and a re-pull now
  shows the player listed.
