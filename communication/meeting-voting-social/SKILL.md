---
name: meeting-voting-social
description: "Use for meeting voting social recipes in scripted Coworld policy optimization."
---

# Meetings, voting & social deduction — recipes (loop tier)

On-demand recipes (4). Trigger→action heuristics; pull the relevant one when its situation arises.

For Crewrift, LLM decisions must use Haiku 4.5
(`us.anthropic.claude-haiku-4-5-20251001-v1:0`) and remain below 1,800
quota-weighted tokens per policy episode across all calls
(input + cache-write + 5 × output tokens), with deterministic fallback when the
remaining budget is insufficient.

#### 1. Set Crewrift roles via game_config_overrides.slots as a full per-slot array
`loop` · **negative result**

Set roles/options in an experience request via game_config_overrides.slots as an ARRAY of objects, one per slot (e.g. {"slots": [{"role": "imposter"}, {"role": "crew"}, ...]} for crewrift, slot 0 = the requester). Supply the FULL array because the override REPLACES the whole key -- a partial array or bare strings will not work.
  <sub>sources: player_labs/.claude/skills/coworld-experience-requests/SKILL.md</sub>

#### 2. Use compact positional event-based coordination messages after a startup window
`loop`

For length-limited coordination, use a compact POSITIONAL format with short field codes, '-' for absent values, and row.col targets (e.g. 'B3 role,job,epoch,hearts,dir,target,resource|event' with an optional event suffix and status|message delimiter so urgent events ride along), keeping the parser backward-compatible with older formats in historical logs. Broadcast a policy-identity handshake such as 'BULBA/v{VERSION} role={ROLE} id={ID}' so a listener decoding its own signature knows it found a coordinatable teammate, and keeping the version in the message lets coordination survive policy-version changes. Use a startup coordination window (first ~100 ticks, a natural Schelling point is all agents converging on the team hub to negotiate roles in an Initialization mode), then switch to EVENT-BASED communication: suppress idle heartbeat chatter and emit only for concrete coordination events (role commit/refresh/change, job, target, resource, direction, hearts, epoch, raid recruitment) AND only when a relevant teammate is currently visible and can act on the info. The agent must still play correctly if no one else cooperates.
  <sub>sources: archive/cogames_playground/bulbacog/designs/OUTER_LOOP_AND_MODES.md, archive/cogames_playground/bulbacog/designs/STRATEGY.md, claude-code:829e80cb-6031-4b81-af72-52b3a12289f3, archive/cogames_playground/bulbacog/designs/INNER_LOOP_IMPL.md (+1)</sub>

#### 3. Negotiate roles on merit with leases and hysteresis; never hard-assign by agent_id
`loop` · **negative result** · ⚠ _session-derived, unverified_

NEGATIVE RESULT: never use agent_id as a reason to SELECT a role (only as a tiebreak) -- a policy that hard-assigns by agent_id cannot adapt to unknown teammates. Replace it with a negotiation/initialization phase where each agent observes, talks, estimates teammate roles, computes per-role demand, and commits only to a role that wins on merit, using agent_id solely to break otherwise-equal ties. Prevent role oscillation among same-policy teammates with leases + hysteresis + demand tokens: without commitment a local resource shortage makes every agent flip to miner simultaneously, so give roles a minimum lease or completion condition, only switch when a new role beats the committed one by a margin, and track out-of-view teammates as DECAYING commitments. Bias toward miners early (before ~tick 700 hold miner demand at 4 unless 4+ OTHER trusted teammates already claimed miner -- the deciding agent must NOT count itself). Miners announce the resource they seek via talk so nearby miners DIVERGE (pick the next-lowest element) instead of all piling onto oxygen then germanium. Aligner direction is flexible and reactive: seed from agent_id but announce dir=N/E/S/W via talk and yield/change if another aligner claimed it, and make the capturing mode honor a directive's specific target_pos before generic selection or the negotiated direction won't stick.
  <sub>sources: codex:019e14de-cdca-7482-88fa-81716ee830ae</sub>

#### 4. Wire an execution branch for every negotiable role and don't capture raid-intent as fact
`loop` · **negative result** · ⚠ _session-derived, unverified_

NEGATIVE RESULT: a negotiated role is useless if the execution layer has no branch for it -- a strategic layer could negotiate a scout role but no scout execution branch existed, so a scout that finished equipping fell through into holding and did nothing. When adding a role to negotiation, wire a real execution branch AND make the bid explicit and conditional (bid scout only when heart/resource discovery is the actual bottleneck), and check that every negotiable role has a matching path. Treating scrambler raid-intent as a capturable fact breaks coordination: separate three talk states -- raid-intent (recruit support, must NOT affect capture scoring), support-wait (aligner advertises it has a heart and waits at a frontier anchor to prevent pile-ups, with a ~150-300 tick TTL), and raid-done tgt=r,c (the ONLY state that creates an aligner reclaim target). Aligner heart-hogging starves trusted teammates, so reserve hearts in the hub equal to the trusted-aligner count (count trusted aligners from negotiation/talk where h<=0 means still needs a heart; take one when you can, then take no more unless enough remain to leave one per trusted aligner).
  <sub>sources: codex:019e1579-a737-7b70-bf0e-172ff04307cf, codex:019e194d-3a17-7eb2-9df9-7bae24112862, codex:019e14de-cdca-7482-88fa-81716ee830ae</sub>
