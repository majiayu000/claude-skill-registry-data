---
name: deep-pass
description: Closed-loop depth mining. Mines zone, validates with experts, forges build-ready agent prompts. Use when user says /deep-pass, wants to go deep AND get expert validation, or uses intensify and over-the-shoulder together.
---

# /deep-pass

Closed-loop depth-to-build pipeline. Mines zone for high-yield moves, validates against expert methods, then forges dispatch-ready agent prompts. Output is gold: validated builds ready for swarm execution.

## Input

`/deep-pass [zone] [--quick|--deep]`

- Zone: optional. Infer from conversation context if omitted.
- Depth: controls intensify agent count (quick/normal/deep). Over-the-shoulder lens count scales to match (3/5/7).

## Execution

### Phase 1: Intensify

Run the full `/intensify` workflow for the zone:

1. Check `docs/intensify/{zone}.md` for prior runs
2. Spawn agents per depth (quick=1, normal=2+1, deep=2+1+cross-domain)
3. Produce ranked move list with saturation status

Do NOT present results yet. Hold the output for Phase 2.

### Phase 2: Over-the-Shoulder

Feed intensify output as context to `/over-the-shoulder`:

1. Infer work type from the zone + moves surfaced
2. Select lenses (3 for quick, 5 for normal, 7 for deep)
3. For each ranked move from Phase 1:
   - Would selected experts endorse this move?
   - What would they add or reject?
   - What failure mode would they flag?
4. Re-rank moves incorporating expert perspective

### Phase 3: Combined Output

Present unified results:

```md
## /deep-pass: {zone}

**Status:** {saturation} | **Trend:** {yield trend} | **Run:** #{n}

### Selected Lenses

- {Lens} - {reason} - {source basis}

### Moves (Expert-Validated)

1. {action} - {reason} - {expert endorsement or caveat}
2. ...
3. ...

### Expert Additions

- {move experts surfaced that intensify missed}

### Rejected

- {item}: {expert reason for rejection}

### Skip

- {premature items}

### Pause When

{concrete trigger that resets saturation}

### Best Next Move

{single highest-leverage action now}

### → Phase 4 below (Build Prompts)
```

Then persist to `docs/intensify/{zone}.md` using the extended format:

```md
## Deep-Pass Run {date}

STATUS: {saturation status}
DEPTH: {quick|normal|deep}

SURFACED:

- {finding 1}
- {finding 2}

LENSES_USED:

- {Lens}: {reason selected}

EXPERT_VALIDATION:

- {move}: {endorsed|cautioned|rejected} - {expert rationale}

EXPERT_ADDITIONS:

- {move experts surfaced that intensify missed}

REJECTED:

- {item}: {expert reason}

ACTED ON: (filled when user picks moves)

- {move chosen}

SKIPPED:

- {item}: {why}

CROSS_REFS:

- [[{other-zone}]]: {what this run found that relates to that zone}

NEXT TRIGGER: {what resets saturation}
```

On subsequent runs, read `LENSES_USED` and `EXPERT_VALIDATION` from prior entries. Pass to Phase 2 so OTS can either reuse validated lenses (consistency) or deliberately rotate (fresh perspective). Prior rejections skip re-evaluation unless fresh data invalidates them.

## Phase 1→2 Handoff Shape

Intensify output flows to OTS in this structure:

```
ZONE: {name}
YIELD_TREND: {increasing|stable|declining}
SATURATION: {fresh|partially-mined|near-saturated|saturated-until-reset}
PRIOR_LENSES: {from zone log, or "none"}
PRIOR_REJECTIONS: {from zone log, or "none"}

MOVES:
- rank: {n}, action: {x}, yield: {HIGH|MED}, stable: {yes|no}, reason: {why}

ARCHITECTURAL_INSIGHTS: (if any surfaced organically)
- {insight}
```

OTS receives this and attaches per-move: `endorsement|caveat|failure_mode`. Architectural insights become primary critique targets.

When `YIELD_TREND` is "declining", OTS focuses lenses on "what would reset saturation" rather than validating existing moves.

### Phase 4: Forge Agent Prompts

For every endorsed move (not rejected, not skipped), generate a dispatch-ready agent prompt. This is the gold output. The dev pastes these into a fresh session or swarm orchestrator and builds happen.

**Prompt shape per move:**

```markdown
### Agent: {move-name-slug}

- **Model:** haiku | opus (match complexity: single-file mechanical = haiku, multi-file judgment = opus)
- **Zone:** {zone}
- **Task:** {concrete build instruction, not vague. What to create/modify, where, acceptance criteria}
- **Read first:** {specific files agent needs for context}
- **Expert backing:** {which lens endorsed this and why}
- **Done when:** {verification criteria: test passes, type-checks, route responds, UI renders}
- **Caveats:** {any expert-flagged failure modes to watch for}
```

**Forge rules:**

1. Every prompt is self-contained. Agent doesn't need conversation context.
2. "Read first" must be specific files, not "the zone" or "relevant docs."
3. "Done when" must be verifiable (command exits 0, screenshot matches, HTTP 200).
4. Rejected moves get NO prompt. Cautioned moves get a prompt WITH the caveat prominent.
5. Group prompts into waves if dependencies exist between moves.
6. If > 5 prompts, assign wave numbers. Wave 1 = no dependencies. Wave 2+ = depends on prior wave.

**Output block (after Phase 3 summary):**

```markdown
## Build Prompts (Ready to Dispatch)

### Wave 1 (Parallel)

{agent prompts with no dependencies}

### Wave 2 (After Wave 1 Verified)

{agent prompts that depend on Wave 1}

### Dispatch Notes

- Total agents: {n}
- Estimated tier cost: {haiku count} haiku + {opus count} opus
- Verification after all waves: `npx tsc --noEmit --skipLibCheck && npm run test:experiential`
```

**Persist prompts** to `docs/intensify/{zone}.md` under a `BUILD_PROMPTS:` section so they survive session boundaries. Mark prompts as `DISPATCHED` or `PENDING` when acted on.

## Rules

- All intensify anti-patterns apply (never suggest new features, cosmetic polish, documentation)
- All over-the-shoulder hard rules apply (source first, cite public methods, no impersonation)
- Expert lenses must be relevant to the zone. Chef/food/event zones get ChefFlow-native lenses.
- If intensify returns "saturated" status, over-the-shoulder still runs but focuses on "what would reset saturation" rather than forcing new moves.
- Phase 4 is ALWAYS generated. Deep-pass without prompts is incomplete.
- User may say "dispatch wave 1" to immediately spawn agents from the prompts. Otherwise prompts persist for later use.
