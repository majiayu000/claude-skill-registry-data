---
name: suspicion-belief
description: "Use for Crewrift-specific suspicion belief recipes when optimizing a player."
---

# Suspicion & belief modeling — recipes (crewrift tier)

On-demand recipes (8). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Exploit perfect recall; rank evidence by strength and only act when sure
`crewrift`

An LLM social-deduction player's #1 edge is perfect recall: remember who was where and when, who spoke vs stayed silent (silence is a suspicion signal), construct alibis before needed, and model what each player does and does not know. Flag a player as more suspicious when alone in low-traffic rooms, repeatedly near bodies but never reporting, moving erratically without advancing real tasks, accusing aggressively (aggressive accusers are often imposters deflecting), standing at a task without advancing its completion counter, or contradicting observed reality (a claimed location others disprove, a position far from where they were seen implying venting). But voting out a real crewmate is a huge blow, so rank evidence by strength and only call sus when sure: a directly witnessed kill or vent transition is strong proof; a player next to a body without reporting is suspicious but not certain; two players merely together is weak. Recover kill evidence from the static-body assumption -- the frame a body first appears with a crewmate within ~2x kill range implicates that crewmate. Never treat a weak sighting or another player's 'sus' chat as proof.
  <sub>sources: bitworld/among_them/bot-policies/sidecar/prompts/system.md, bitworld/among_them/players/SMART_BOT_GUIDE.md, bitworld/among_them/bot-policies/sidecar/prompts/crewmate.md, bitworld/among_them/bot-policies/sidecar/prompts/imposter.md (+4)</sub>

#### 2. Key the roster by stable COLOR; track absence and dead targets
`crewrift`

Color is the only identity stable and unique across every namespace (in-world sprites, bodies/corpses, chat icons, vote markers), so keying the roster by color links a live sighting, a corpse, a chat line, and a vote to one player. Identify crewmates by stable sprite pixels plus body tint (outline and visor are stable, body colors vary) and store the last tick each color was seen so you can name a suspect after reporting a body. Note which players were NOT present at a meeting, since absence from a body-discovery meeting is itself evidence. An imposter bot should mark confirmed kill targets dead in belief so it does not re-target when body-detection lags the kill. Role-reveal asymmetry: a crewmate sees ALL players but cannot tell which are imposters, while an imposter sees only the OTHER imposters by color -- and because that teammate color shows only at reveal, an imposter must record it immediately.
  <sub>sources: personal_labs/crewrift_lab/crewrift/crewborg/design.md, bitworld/among_them/players/how_to_make_a_bot.md, bitworld/among_them/players/italkalot.md, bitworld/among_them/bot-policies/sidecar/prompts/crewmate.md (+2)</sub>

#### 3. Make proximity/body evidence a decaying accumulator, never a binary stamp
`crewrift` · ⚠ _session-derived, unverified_

Never treat 'player was near a body' as a binary flag -- it is ambiguous (killer, reporter, or passer-by). Make it a weighted accumulator scored by recency + proximity + incident count: stronger the closer they were, gated by a cooldown so one lingering scene does not re-count each tick, with raw distance/score passed into any LLM prompt so it can rank suspects (e.g. 'near-body score 6, distance 11' vs 'score 5, distance 16'). Probability-by-distance gradients are verifiable in traces (a close case ~77% at distance 2, far cases ~23-28%); unit-test that closer appearances score higher and that the snapshot exposes them as probabilistic, not proof. A flat 'seen near body at tick N' stamp causes false positives (stale evidence votes someone out) and false negatives (a fresh kill weighted like an old coincidence); once soft evidence becomes vote-worthy the opposite failure appears (noisy crew-on-crew misfires), so treat the action threshold as a double-edged knob watched in the trace.
  <sub>sources: codex:019e14a5-e574-7770-953b-17019f2f5e74, codex:019e1591-004e-7040-b768-062bd8e6acd4, opencode:ses_21ffeb5ffffeA1Pk6sdyHDzwQW</sub>

#### 4. Derive a task-alibi from sprite-rect overlap, not flaky task-flash detection
`crewrift`

Derive a task-alibi signal without new perception: once per frame after the task-icon update, iterate visible crewmates against in-progress task locations and append an alibi when a crewmate is within a small radius (Manhattan ~12 px, or ~28 px of a terminal). Filter self/teammate/unknown colors and dedup per-(color, task) with a ~20-tick cooldown. Crucially, do NOT key the alibi on a task-completion icon FLASH: task icons render ONLY the bot's OWN assigned tasks, so an icon vanishing means the bot finished its own task and cannot attribute an alibi to anyone -- a non-self sprite overlapping a task-station rectangle is the tractable signal. A weaker signal that fires correctly beats a stronger one that fires on noise.
  <sub>sources: bitworld/among_them/players/mod_talks/DESIGN.md, bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, bitworld/among_them/players/modulabot/DESIGN.md, bitworld/among_them/players/modulabot/TODO.md (+1)</sub>

#### 5. Drive votes from an evidence-grounded hypothesis with explicit confidence thresholds
`crewrift`

Drive crewmate voting from an evidence-grounded hypothesis with explicit thresholds rather than binary scores alone: accuse if top-suspect likelihood >= 0.75, vote the top suspect if >= 0.50, else fall back to a rule-based suspect or SKIP; express timestamps as ticks-before-meeting. The weighted FALLBACK vote combines known-imposter role memory, witnessed venting, near-vent appearances, distance-weighted near-body sightings, witnessed kills, visible vote dots, and chat mentions, minus solo-survival trust, voting SKIP when nothing clears the bar. The imposter fallback avoids self and known teammates, prefers a crewmate already accused by chat/votes/body evidence, else SKIP rather than a baseless pile-on. Distinguish probabilistic from hard proof: a repeated near-vent appearance / near-vent score >= 8 / probability >= 60% is actionable voting evidence, but describe it in chat as 'appeared near vent', not confirmed vent proof.
  <sub>sources: bitworld/among_them/players/mod_talks/LLM_VOTING.md, personal_cogs/among_them/guided_bot/MEETING_DESIGN.md</sub>

#### 6. Treat chat as credibility-gated input scored by HOW you learned allegiance; LLM-classify it
`crewrift` · **negative result** · ⚠ _session-derived, unverified_

Treat chat claims as low-confidence input gated by a credibility threshold (~0.5), not facts, and score credibility from HOW you learned the sender's allegiance: unknown sender low (~0.3), same-team-via-mechanical-exchange high (~0.85), same-team-via-weaker-signal medium (~0.6), known enemy very low (~0.1), self-contradicting identity claim crushed by ~0.1x. Even non-credible or enemy messages carry signal, so record rather than discard: log action requests on the sender's record even from enemies (the request is intelligence about intent) and route adversary chatter to a separate observed-behavior channel instead of filtering to zero. Model private knowledge as private: mark a witnessed suspicion only in the observing bot's own memory and surface it in the meeting ledger as 'I witnessed X' rather than promoting to global truth, preserving the asymmetric-information dynamic. Do NOT keyword-score chat symbolically: 'I saw yellow away from the body' names a color and 'body' yet is a DEFENSE, so naive keyword suspicion mis-flags alibis -- hand raw mentions to an LLM and ask it to classify each as accusation / defense / alibi / noise.
  <sub>sources: codex:019e090d-a88d-76f2-b1f5-cd3e4eda9381, codex:019e1591-004e-7040-b768-062bd8e6acd4, codex:019e1593-c00d-7a32-9dfa-1cf6b16b01a4, claude-code:dfa4502e-c404-40e8-bf86-8d15c72ba5af (+1)</sub>

#### 7. Add a periodic mode to reconcile parsed beliefs against an authoritative game screen
`crewrift`

Add a proactive 'validate knowledge against mechanical truth' mode: beliefs accumulated by parsing chat/system messages can miss events, so periodically (e.g. once per round) navigate to a screen the game renders authoritatively (an info/status screen listing known players, roles, state), reconcile the parsed belief against it, then return to the prior surface -- time-boxing the detour with a tick budget. Note: Persephone's hostage-exchange renderer (renderExchangeRow / drawRoleSlot) draws TRUE role indicators for all shown sprites UNCONDITIONALLY, unlike the overworld which gates on revealedTo, so it leaks every exchanged player's role -- a likely unintentional information-model bug an agent could exploit but should NOT rely on long-term.
  <sub>sources: opencode:ses_1fb2002bcffeK2Ldmjf34wdpM3, players_checkouts/players/users/james/personal_cogs/persephone/GAME_AP</sub>

#### 8. Earlier simpler scalar-decay suspicion scheme (superseded by the no-decay Bayesian model)
`crewrift`

An earlier, simpler design maintained a quantitative continuous per-player suspicion score updated by discrete events rather than deferring all reasoning to the LLM. One tuned constant set (Among Them sidecar bot): SUSPICION_DECAY=0.995 per tick, +0.3 near a body, +0.2 for being accused, +0.1 for being alone in a low-traffic room, +0.05 for staying quiet, -0.4 when cleared by an ejection. NOTE: the later Bayesian-posterior approach in crewborg argues role is a fixed latent so suspicion should NOT decay over time (see the no-time-decay lesson); this scalar-decay scheme is the earlier, simpler design retained for context.
  <sub>sources: bitworld/among_them/bot-policies/sidecar/ (package: bot.py, brain.py, </sub>
