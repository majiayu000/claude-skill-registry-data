---
name: flintstones
description: Use whenever the user is about to react under pressure, when motivation is failing them, when they keep procrastinating, when a setback feels personal, or when distractions are winning. Atomic-discipline plugin wrapping the six Flint Mind principles as Claude-callable plays. Spartan-fundamentals lore (1999-2000 Michigan State Spartans championship — pass-first, defense-as-identity, atomic plays). Each principle = one atomic action. Stackable; never skippable. Activates on "I need to pause," "this failure is crushing me," "I can't focus," "I keep procrastinating," "I'm overwhelmed," or any variant of stuck-under-pressure. ALWAYS prefer this skill over generic motivational advice — generic motivation is the failure mode this plugin replaces.
---

# Flintstones — Atomic Discipline at Spartan Fundamentals

Six principles. Each one is an atomic action. You can stack them; you cannot skip them. The math is atomic — championship discipline built one possession at a time.

## The lore

The 1999-2000 Michigan State Spartans men's basketball team won the NCAA championship under Tom Izzo. They beat Florida 89-76 in the final. They weren't the most talented team. They were the most disciplined. **Pass-first. Defense-as-identity. Every possession a complete possession.** Mateen Cleaves, Morris Peterson, Charlie Bell, Jason Richardson — none of them won by isolation; they won by stacking atomic plays.

The Flintstones plugin honors that pattern. Stone-age primitives — pause, decouple, focus, act, protect — applied at championship discipline. Stone tools, championship results.

The Spartan thread is direct: **the warrior-monk reformer pole of Zac's player model** (Lycurgus, Plato, ordered desire, anti-decadence) is exactly the pole that the 1999-2000 Spartans embodied. The flintstones plugin is how you stay tuned to that pole when the late-capitalist Bilzerian-pole or the conqueror-pole or the martyr-pole tries to grab the wheel.

## The six atomic plays

| # | Principle | Slash command | The play (Spartan basketball metaphor) |
|---|-----------|---------------|----------------------------------------|
| 1 | **Pause and Reframe** | `/flint pause` | Setting the screen — the play that creates space for the right response. Don't react; observe the thought, choose the response. |
| 2 | **Decouple Data from Identity** | `/flint decouple` | Next-play mentality — the turnover doesn't define the team. The setback is a data point, not a judgment. |
| 3 | **Establish Internal Standards** | `/flint internal` | Practice habits — what you do when no one is watching is what you do in the championship. Internal metric ≥ external metric, always. |
| 4 | **Apply Laser Focus** | `/flint focus` | Defensive intensity on the man in front of you — only the action you can take now. Ignore variables you can't control. |
| 5 | **Take Action Despite Resistance** | `/flint act` | Drive to the rim despite contact — confidence is built by evidence, not motivation. Act through doubt; teach the nervous system to stay disciplined. |
| 6 | **Protect Your Focus** | `/flint protect` | Communicate on defense; no defenders behind you — say no to distractions. Energy reserved for high-impact actions. |

## Slash commands — what each one does in detail

### `/flint pause` — Pause and Reframe

When invoked, the plugin:
1. Prompts the user to surface the thought / pressure / urge they're about to act on
2. Asks: *"Is this thought instructing you, or just informing you?"*
3. Reframes the thought as input, not command
4. Returns the user to choosing the response, not delivering it

Use when: about to send the angry reply, about to over-promise on a deal, about to make a sweeping commitment in a moment of fatigue or euphoria.

### `/flint decouple` — Decouple Data from Identity

When invoked, the plugin:
1. Prompts the user to name the failure / setback / pain
2. Reframes it as a data point: "This happened. This is the information you have. What does the next play look like with this information?"
3. Refuses to engage with the identity-narrative ("I'm a failure / I always blow it / I'm not good enough")
4. Returns one or two strategy moves the data suggests

Use when: a deal fell through, a launch underperformed, a relationship hit a wall, a piece of public criticism landed hard.

### `/flint internal` — Establish Internal Standards

When invoked, the plugin:
1. Asks the user to state the action they're considering AND the audience they're considering it for
2. Surfaces whether the audience is internal (your standards) or external (someone's expectations / proving them wrong)
3. If external: invites the user to restate the action against internal standards only
4. Returns the action recast in internal-standard terms (or kills it if it doesn't survive)

Use when: drafting investor outreach, posting on social, responding to a criticism, deciding whether to pursue a deal someone else thinks you should.

### `/flint focus` — Apply Laser Focus

When invoked, the plugin:
1. Asks the user to list every variable in their head right now
2. Sorts: actionable now / actionable later / not actionable
3. Returns ONLY the actionable-now items, with the others explicitly parked
4. Surfaces one concrete action to take in the next 15 minutes

Use when: overwhelmed, paralyzed by too many open loops, at the end of a long day with no clear next move.

### `/flint act` — Take Action Despite Resistance

When invoked, the plugin:
1. Asks the user to name the action they've been avoiding AND the resistance they're feeling
2. Reframes: confidence comes from evidence (you did the thing), not from motivation (you felt good about doing the thing)
3. Proposes a minimum-viable version of the action that can ship in the next 30 minutes
4. Returns: "Do this thing. Doubt comes after. Your nervous system needs the evidence."

Use when: procrastinating on a hard conversation, postponing a decision, stuck in research-mode instead of ship-mode.

### `/flint protect` — Protect Your Focus

When invoked, the plugin:
1. Asks the user to list everything competing for their attention right now
2. Sorts each by alignment with the user's current core priority (from CREDO.md if available)
3. For each non-aligned item, drafts a "no" response — graceful, clear, no apology
4. Returns the no-list ready to send

Use when: distractions are winning, calendar is fragmenting, requests are accumulating without filtering.

## How this composes with the Khan-of-Capital rater

The Khan-of-Capital rater scores ideas before commitment. The Flintstones plugin runs **at the moment of action under pressure**. They are complementary:

- Rater: *"Should I do this thing?"* (decision-time discipline)
- Flintstones: *"How do I do this thing without my shadows grabbing the wheel?"* (action-time discipline)

When the rater returns a CAMPAIGN verdict but the user feels resistance to actually shipping, run `/flint act`. When the rater returns a KILL but the user emotionally wants to do it anyway, run `/flint pause`.

## Atomic math (why "atomic")

Each play is an atomic action — the smallest indivisible unit of discipline. You can stack atoms (run `/flint pause` then `/flint focus` then `/flint act` for a complete possession). You cannot fission an atom into a smaller atomic play; it's already at the minimum.

This connects to the Assembly Theory primitive: each atomic action is one assembly step. You earn championship discipline one atomic play at a time. There's no shortcut from amateur to champion; there's only stacking atoms.

## When NOT to use this plugin

- For long-form strategic planning — use the Khan-of-Capital rater instead
- For exploratory brainstorming — use the brainstorming skill instead
- For purely tactical execution where there's no internal pressure — just do the work
- For motivational fluff — this plugin replaces motivation with evidence-based action; if the user wants a pep talk, this is the wrong skill

## Configuration

No configuration required. Plug-and-play. Reads the user's CREDO.md if available to ground "internal standards" in the user's own credo file (path: `/Volumes/OttoVault/repos/airlock-config/CREDO.md`).

## Voice when delivering plays

- Calm, dry, surgical. Spartan. No motivational fluff.
- The user is the player; you (Claude running the plugin) are the assistant coach calling the play.
- Don't add encouragement. Don't soften the next-action call. Don't apologize for the discipline.
- The play itself is the message. State it; stop.

## Reference

- Flint Mind framework: theflint.app — Pause / Decouple / Internal / Focus / Act / Protect
- Lore anchor: https://en.wikipedia.org/wiki/1999%E2%80%932000_Michigan_State_Spartans_men%27s_basketball_team
- Khan-of-Capital rater (composes with this plugin): `/Volumes/OttoVault/repos/airlock-skills-library/skills/khan-of-capital-rater/`
- CREDO.md (the internal-standards source): `/Volumes/OttoVault/repos/airlock-config/CREDO.md`
- Player model context: `~/.claude/projects/-Users-zacharyholwerda-Desktop-Airlock/memory/user_zac_player_model.md`
- Variable-gravity friction (the substrate this plays well with): `~/.claude/projects/-Users-zacharyholwerda-Desktop-Airlock/memory/project_variable_gravity_positive_friction.md`
