---
name: meeting-voting-social
description: "Use for Crewrift-specific meeting voting social recipes when optimizing a player."
---

# Meetings, voting & social deduction — recipes (crewrift tier)

On-demand recipes (11). Trigger→action heuristics; pull the relevant one when its situation arises.

Crewrift LLM decisions must use Haiku 4.5
(`anthropic/claude-haiku-4.5`) and remain below 1,800
quota-weighted tokens per policy episode across all calls
(input + cache-write + 5 × output tokens), with deterministic fallback when the
remaining budget is insufficient.

#### 1. Drive the Crewrift vote cursor with fresh d-pad edges, not held input
`crewrift` · **negative result**

Crewrift voting has no mouse and no text-vote (packet 0x81 is chat only): move a cursor with the d-pad (up/left = -1, down/right = +1) then press A to confirm. The last cell (index == player count) is SKIP (vote -2); a player vote stores the cursor index, and a vote is final once cast. Because the cursor advances on EDGE presses, alternate a direction mask with idle to create a fresh edge -- holding the same direction can fail to advance the cursor.
  <sub>sources: personal_labs/crewrift_lab/crewrift/crewborg/AGENTS.md, bitworld/among_them/players/how_to_make_a_bot.md, claude-code:4430a077-5411-426b-a87a-75512ec4300f, claude-code:4c297fe5-08a0-4973-85ac-1b8824e638ac</sub>

#### 2. As imposter, blend in and win the first-to-chat slot
`crewrift`

As an imposter in meetings, blend in rather than play optimally-aggressive: wait for others to speak before accusing, target the weakest social position (quiet, no alibi), vote with the majority to avoid standing out, and weigh whether saving an accused teammate is worth the exposure. Because chat is the only channel and votes bandwagon on chat, first-to-chat effectively decides the vote: queue the imposter's accusation the instant any body is seen (including its own kill) so it flushes the moment the voting screen opens, before anyone else chats. Controlling whether you initiate vs. follow is higher-leverage than the accusation content.
  <sub>sources: bitworld/among_them/bot-policies/sidecar/prompts/imposter.md, bitworld/among_them/players/SMART_BOT_GUIDE.md, opencode:ses_224eeb40bffeZqmBRcrjFgPFul</sub>

#### 3. Chat only during Voting phase; queue body observations until it opens
`crewrift`

Crewrift meeting chat is accepted ONLY during the Voting phase (sim.nim's addVotingChat early-returns off-phase). Chat is rate-limited by MessageCooldownTicks=100 and only the last 6 messages are visible, giving an effective cap of ~2 messages per player in the ~10s vote window. Do not attempt to chat outside Voting; instead, on finding a body report it immediately, record who was nearby, and queue concrete chat (e.g. 'body in [room]', 'sus [color]') to emit the moment voting begins.
  <sub>sources: coworlds/coworld-crewrift/src/crewrift/sim.nim, personal_labs/crewrift_lab/docs/crewrift-gameplay.md, personal_labs/crewrift_lab/docs/crewrift-player.md, bitworld/among_them/players/how_to_make_a_bot.md (+3)</sub>

#### 4. Make meeting chat concrete and template-bound, never vague or silent
`crewrift`

Constrain chat to a fixed set of canonical observation templates (e.g. 'I saw {player} near {victim}'s body', 'I saw {player} at a vent', 'I directly confirmed {player} as imposter') so emitted chat maps to evidence categories and stays parseable. Defend accusations with specific alibis ('I was in [room] doing [task] at tick [N]') and clear players you were with ('I was with Red'). Silent players look very suspicious, so always say something; when evidence is weak or only one player said 'sus', ask a short question or state the concrete observation instead of accusing.
  <sub>sources: bitworld/among_them/bot-policies/sidecar/prompts/crewmate.md, coworlds/coworld-crewrift/players/notsus/README.md, players_checkouts/players_2/players/crewrift/suspectra/memory/template, players_checkouts/players_2/players/crewrift/suspectra/memory/system.m</sub>

#### 5. Keep LLM chat short and reasoned; never fire an unconditional opener
`crewrift`

Keep LLM-generated meeting chat short (1-2 sentences) with varied phrasing and timing so the agent is not trivially bot-identifiable, and keep internal reasoning fields OUT of emitted chat (record them only in the trace). Do NOT fire a default chat every meeting: an unconditional opener (a fixed 'skipping' line or a canned taunt on every meeting) is wasteful, a tell, and burns the single scarce per-meeting chat slot. Chat only when there is a reason, gating special chat strictly on its condition: real evidence as crew, a deflection as imposter, or only when this agent triggered the meeting.
  <sub>sources: bitworld/among_them/players/mod_talks/LLM_VOTING.md, codex:019e1591-004e-7040-b768-062bd8e6acd4, opencode:ses_21ffeb5ffffeA1Pk6sdyHDzwQW, claude-code:f70c9801-7ee7-499b-97f9-4fd0848a6b8e (+1)</sub>

#### 6. Make the symbolic meeting mode the legality boundary, not an evidence veto
`crewrift`

Make the symbolic meeting mode handler (e.g. modes/meeting.nim) the LEGALITY BOUNDARY for LLM-proposed votes: guard every requested vote and confirm so it rewrites self-targets, dead targets, invalid targets, and known imposter teammates to SKIP, pressing confirm only once the cursor is on a legal target. Restrict vote_target to constraints.valid_vote_targets (plus 'skip') and keep chat_text short printable ASCII. Crucially, do NOT let the symbolic evidence score be a hard VETO on a legal LLM vote -- the filter blocks illegal/self-defeating actions, not legal disagreements. For the deterministic fallback: avoid voting self or dead players and skip when there is no useful target.
  <sub>sources: players_checkouts/players/users/james/personal_cogs/among_them/guided_, personal_cogs/among_them/guided_bot/MEETING_DESIGN.md, players_checkouts/players_2/players/crewrift/suspectra/memory/system.m, bitworld/among_them/players/italkalot.md (+3)</sub>

#### 7. Enter meeting mode as an edge-triggered reflex with non-suppressible early-vote backstops
`crewrift` · **negative result**

Make entry into voting/meeting mode the highest-priority, unconditional, edge-triggered reflex: it fires the moment the phase transitions to voting regardless of current mode and with NO TTL, and exits ONLY when the voting phase ends and the mode becomes illegal -- never via TTL or another reflex; route known ghosts away from voting (even if a ghost transiently records a meeting-started event) since ghosts cannot vote. Then give the bot non-overridable STRUCTURAL backstops so it always casts a ballot regardless of LLM behavior: (1) a safety-net fallback with ~100 ticks (~4s) left, and (2) an auto-vote after ~360 ticks (~15s) when no LLM action arrived; both navigate to the role-aware evidence/alibi fallback target and confirm. After a vote is confirmed, soft-lock the mode to emit only no-ops for the rest of the meeting (prevents re-voting and stops the safety-net from firing after a successful LLM vote). NEGATIVE RESULT: a runtime meeting-LLM dependency fails silently and too late -- when historical inference calls failed (account-level 404s), guided_bot had no working no-LLM fallback and fallback votes only arrived around tick ~360, too late. A no-LLM fallback must cast within a SMALL fixed tick budget (the fix lowered it to ~96 ticks and the crew fallback evidence threshold to one visible vote dot) and must be validated against a model-outage path.
  <sub>sources: personal_cogs/among_them/guided_bot/MEETING_DESIGN.md, bitworld/among_them/players/italkalot.md, players/users/james/personal_cogs/among_them/guided_bot/coworld/README, codex:019e4c28-d516-7ca0-b145-153c152b4f43</sub>

#### 8. Structure the LLM voting brain as conversational, per-stage typed calls
`crewrift` · ⚠ _session-derived, unverified_

Make LLM meeting decisions conversational, not one-shot: let the agent send multiple chats, respond to others, then decide a vote, carrying conversation history across calls within the meeting. Use a small fixed budget (e.g. exactly 2 chat turns then 1 vote-decision call) spacing turns by ~100 ticks so others' replies land before the next turn; the bounded turn count caps latency/cost and stops one agent monopolizing. Structure as distinct call types per pipeline stage rather than one mega-prompt, keeping prompts small and outputs typed: a stateless 'gameplay' call returning a directive (mode+params+TTL) and a stateful 'meeting' call returning one action per call. Crew stages: hypothesis-formation (rank suspects + confidence), evidence-citing accusation, rate-limited per-chat belief-update (returns scores + speak/ask/silent), vote+persuasion; imposter mirrors with strategize (best_target + bandwagon/preemptive/deflect + timing) and imposter_react. Drive it with an explicit per-role state machine (idle -> form hypothesis -> listen/accuse -> react -> vote) where each stage's schema carries an optional chat field and an explicit 'silent' action, making it auditable which decision produced which utterance. Support tentative votes that auto-submit near the end plus an explicit force/send option. When reaction calls are triggered by opponent chat, pair them with both a rate limit AND a forced-decision timer (e.g. a VoteListenTicks listen-window) so voting still happens if no chat trigger crosses threshold -- triggers without both either spam calls or never decide. Gate reaction calls on the CLIENT (cooldown ~48 frames / ~2s, plus an 'unread chat' flag and 'no request in flight') even though the server also enforces a message cooldown, since relying only on the server cooldown wastes calls on messages it will reject.
  <sub>sources: opencode:ses_21e58aef7ffeoJ7uZeDgGBCfIh, codex:019e941c-8eb9-7402-a77f-8fe75a5d19bf, opencode:ses_219efd206ffe6azQSiSZsvnxX4, opencode:ses_21b1e7074ffeYT9RjQFHNPlNKX (+2)</sub>

#### 9. Pin LLM chat to a strict contract and gate output through three layers
`crewrift` · ⚠ _session-derived, unverified_

Pin LLM chat output to a rigid, parseable, safety-constrained contract: state the bot's color and role, the living players it may accuse, asymmetric accuse rules (imposter accuses freely, crew only with transcript/vote evidence), a hard length cap (one short message under ~70 chars), and a fixed output form ('Reply with exactly one line: say <message>'); always post-process to strip say:/chat: prefixes and quotes -- never trust the raw reply onto the wire. When emitting free text into a real-time game, gate it through three independent layers because any one can silently swallow output: (1) an LLM-side single-slot pending-message queue with a no-overwrite guard, (2) a client-side flush tied to the correct phase/screen, and (3) a server-side validity check (phase, alive, cooldown, non-empty). Debug 'my bot won't talk' in that order -- the failure is usually a phase/screen mismatch. Two traps: the single-slot no-clobber guard silently drops a fast LLM's later messages while an earlier one waits, and non-LLM template messages (body reports, role-asymmetric deflect/accuse) write to the SAME slot and collide. Decouple decide-what-to-say from send-it: write to a pendingChat field, drain it in ONE place under the phase guard (interstitial/voting, NOT game-over), then clear; run all strings through one sanitization path that transliterates non-ASCII to printable ASCII and truncates at a word boundary. Record every message the bot emits into a self-statements list so 'react to new chat' logic can diff incoming OCR'd lines against its own output and not react to itself.
  <sub>sources: opencode:ses_219efd206ffe6azQSiSZsvnxX4, opencode:ses_219efb8a0ffetZ1X4BweDZQCca</sub>

#### 10. Read meeting state from labeled sprites and verify the parse on live frames
`crewrift` · **negative result**

Read Crewrift meeting/voting social state from LABELED sprites in id ranges disjoint from in-world entities (more robust than pixel template matching): pair chat-text sprites (9000+) to speaker icons (9200+) by screen-y proximity to recover (speaker_color, text); read the candidate grid (9300+) as an authoritative per-meeting alive/dead census by color; recover the vote cursor target by nearest-cell match. Vote attribution is encoded directly in each VoteDot: target = rel // MAX_PLAYERS, voter = rel % MAX_PLAYERS, making vote-agreement and votes-cast features fully runtime-observable with no inference. NEGATIVE RESULT: a vision parser keyed on a screen TEMPLATE can silently fail for EVERY bot for a whole meeting (no PhaseVoting set, voting reflex never fires, no votes) when the server-rendered screen doesn't match the template -- verify voting end-to-end on LIVE frames rather than assuming the parse works. (Pixel-parse fallback when sprite labels are unavailable: try every plausible player count and validate against the SKIP label, then parse each cell's sprite, cursor outline, local-player marker, per-target voter dots, and chat panel against an ASCII glyph atlas.)
  <sub>sources: personal_labs/crewrift_lab/crewrift/crewborg/design.md, bitworld/among_them/players/evidencebot_strategy.md, claude-code:0e7b14ca-ffd5-4137-9456-47485d3c6f87, players_checkouts/players/users/james/personal_cogs/among_them/guided_</sub>

#### 11. Log every chat with its audience and emit analysis-only bandwagon traces
`crewrift`

Record each chat message together with the occupants present when observed -- capturing not just who said what but who they intended to hear it -- and store all messages without pruning, leaving windowing/summarization/TTL to the agent layer. To give the outer loop signal while preserving evidence-only voting, emit detection/analysis-only trace events that NO policy code reads: e.g. vote_bandwagon_detected, fired once per meeting-target when >=3 votes land within a ~120-tick rolling window, with payload {target, vote count, first-vote tick, ordered voter colors}. The trace informs offline analysis but never feeds the live vote decision.
  <sub>sources: orpheus/DESIGN.md (Orpheus agent framework design), opencode:ses_209613a85ffeqO1Gq9NEDobBYi, opencode:ses_21e58aef7ffeoJ7uZeDgGBCfIh, bitworld/among_them/players/modulabot/TODO.md</sub>
