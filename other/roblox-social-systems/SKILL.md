---
name: roblox-social-systems
description: Design and implement Roblox social systems. Use for parties, clans, groups, friend boosts, gifting, trading, co-op objectives, leaderboards, public celebrations, invites, social retention, and safe player-to-player value exchange.
---

# Roblox Social Systems

## Goal

Make friends useful early. Social connection is one of the strongest retention multipliers.

## First-Session Social Hooks

- Visible other players doing the core loop.
- Co-op objective or shared reward.
- Friend boost or group bonus that does not punish solo players.
- Public celebration for level up, rare drop, boss defeat, or zone unlock.
- Simple invite or help-request moment.

## System Patterns

- Parties: shared objectives, teleport together, contribution rewards.
- Groups/clans: identity, weekly goals, group upgrades, leaderboards.
- Trading/gifting: server-owned sessions, locked offers, double confirmation.
- Leaderboards: reward participation as well as mastery.
- Commendations: lightweight positive feedback after co-op play.

## Safety

- Validate all player-to-player value exchange on the server.
- Add rate limits for invite, gift, and trade requests.
- Add audit logs for valuable exchanges.
- Avoid designs that enable harassment, spam, or coercive monetization.

## MCP Workflow

1. Search for social, trade, party, leaderboard, and group scripts.
2. Read server and client code before edits.
3. Inspect remotes and UI.
4. Patch with `multi_edit`.
5. Playtest with available players or simulate state with `execute_luau`.
6. Check `get_console_output`.

## Output

Return:

- Social loop.
- Server authority and abuse checks.
- UX surfaces.
- Retention goal.
- Verification steps.

## Next

Secure any player-to-player value exchange (trading, gifting) with `roblox-security-economy`, then verify the social flow with `roblox-playtest-qa`.

