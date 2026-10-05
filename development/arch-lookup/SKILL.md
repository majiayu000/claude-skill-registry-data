---
name: arch-lookup
description: Look up Tensix HW behavior across architectures specifically to inform tt-emule mock implementations. Orchestrates per-arch sage agents in parallel and aggregates results with emule-mapping context.
user_invocable: true
---

# /arch-lookup — Architecture lookup for tt-emule mock work

When you're implementing (or debugging) a mock API in tt-emule, you
need to know what the real silicon does. This skill orchestrates
parallel `sage-{wormhole,blackhole,quasar}` agents that consult
DeepWiki + Confluence + LLK source, then aggregates the result with
an emule-simulation perspective.

Adapted from `tt-metal/tt_metal/tt-llk/.claude/skills/arch-lookup`
for the emule mock-API workflow.

## Usage

```
/arch-lookup "How does SFPMAD work?"
/arch-lookup "How does unpack handle Float16 on Blackhole?"
/arch-lookup "What is BroadcastType?"
/arch-lookup "How do T0/T1/T2 synchronize?"
/arch-lookup "How does noc_async_write_multicast complete on receivers?"
/arch-lookup "What does llk_unpack_AB_init actually configure?"
```

Two flavors of question this skill is for:

1. **Mock-faithfulness** — "I'm about to implement / am implementing
   a stub for X. What does the real HW do, so my mock matches?"
2. **Correctness debug** — "Emule's output for op Y doesn't match
   silicon / torch. Where in the HW pipeline could the mock be diverging?"

## Step 1 — Analyze the query

Which architectures are relevant?
- **Specific arch mentioned** → launch ONLY that sage.
- **No arch specified + HW spec question** → launch `sage-wormhole +
  sage-blackhole` (they have DeepWiki access). Skip `sage-quasar`
  unless Quasar is mentioned — tt-isa-documentation has no Quasar
  content.
- **Cross-arch comparison wanted** → launch all 3.
- **emule already mocks X, I want to know if it's right** → at minimum
  launch the arch that matches the active test config
  (`TT_EMULE_ARCH` if explicitly set; otherwise follow the project
  default of wormhole n150 unless the caller/test specifies another arch).

## Step 1b — Classify question type (MANDATORY)

This determines what each sage must consult FIRST — otherwise the
sage defaults to grep and misses the authoritative HW source.

| Question type | Examples | Required primary source |
|---|---|---|
| **HW capability / spec** | "What formats does X support?", "How many DEST rows?", "Does Blackhole have FP8?" | **DeepWiki (WH/BH) / Confluence (QSR) FIRST**, code second |
| **HW behavior / semantics** | "How does SFPMAD handle NaN?", "When does pipeline stall?" | **DeepWiki / Confluence FIRST**, code second |
| **LLK implementation** | "How is matmul wired up?", "Where is X called?" | **Code FIRST** (`tt_llk_*/`), docs second |
| **Mixed / end-to-end** | "How is Float16 handled unpack → math → pack?" | Both required |
| **emule mock review** | "Is my noc_traits_t<TensorAccessor> faithful?" | HW spec FIRST, then existing emule mock at `tt-emule/include/jit_hw/`, then propose changes |

**Critical**: LLK code shows what is wired up in software; it can lag
or diverge from what the hardware supports. For HW-capability /
HW-behavior questions, a grep-only answer is incomplete.

## Step 2 — Launch sage agents

Launch up to 3 agents IN PARALLEL via the Agent tool:

| Agent | LLK scope | Primary ISA source |
|---|---|---|
| `sage-wormhole` | `tt_llk_wormhole_b0/` | DeepWiki + assembly.yaml |
| `sage-blackhole` | `tt_llk_blackhole/` | DeepWiki + assembly.yaml |
| `sage-quasar` | `tt_llk_quasar/` | Confluence + assembly.yaml (NO DeepWiki) |

**Prompt construction rules:**

1. Start with the user's exact question, verbatim.
2. If the question is HW capability / behavior (per Step 1b), include
   the explicit instruction:
   > "This is a HW-capability question. Consult DeepWiki
   > tt-isa-documentation FIRST (sage-wormhole/blackhole) or
   > Confluence FIRST (sage-quasar). Use code grep only to cross-verify
   > what is wired up in LLK. If docs and code disagree, call out the
   > conflict — do not silently prefer one."
3. **Always** include in the sage prompt:
   > "After describing what silicon does, conclude with an 'Emule
   > mapping' section: does tt-emule's mock at
   > `include/jit_hw/` exist
   > today? If yes, is it faithful? If no, recommend the smallest
   > mock that would suffice (which file, what guard
   > pattern — see `tt-emule/.claude/references/emule-mapping.md` for
   > the strategies catalog)."
4. Do NOT over-constrain the sage prompt with code-only framing
   ("grep for the enum", "cite file:line for the definition") on
   HW-capability questions — that pushes the sage into grep-only mode
   and bypasses doc consultation.
5. Always allow the sage to return both doc-sourced facts (with
   staleness caveats) and code-sourced facts (with file:line).

## Step 3 — Aggregate

After all sages return:
1. **Commonalities** — what's consistent across architectures
2. **Differences** — arch-specific variations (highlight clearly)
3. **Emule status snapshot** — for each arch, what does emule's mock
   look like today, and where does it diverge from silicon?
4. **Synthesis** — unified explanation with per-arch sections where
   they diverge, and a "what to do in emule" recommendation if the
   question was implementation-oriented.

## Step 4 — Final response shape

```
# {topic}

## TL;DR
[2-3 sentence answer combining the arch findings]

## Hardware behavior (per arch)
### Wormhole B0
[…]
### Blackhole
[…]
### Quasar (if launched)
[…]

## Cross-arch differences
[Where the archs diverge — highlight if it affects emule's choices]

## Emule today
[What tt-emule's mock currently does, file:line at jit_hw/. If
nothing exists, say so.]

## Recommendation (if implementation question)
[Smallest faithful mock: file path, signature, guard pattern (per-op
patch / semantic rewrite / stub-in-jit_hw — see emule-mapping.md).]
```

## Quality checklist

Before responding, verify:
- [ ] Question was classified per Step 1b; sage prompt matched
- [ ] For HW-capability questions, sages cited DeepWiki / Confluence,
  not just code grep
- [ ] Where HW docs and LLK code disagree, conflict is called out
- [ ] Default path identified — baseline vs variants distinguished
- [ ] All relevant data format paths covered
- [ ] Code refs include file:line; doc refs include Confluence URL +
  last-updated date (Quasar)
- [ ] **Emule mapping section present** — what's the current mock?
  where would changes go?
- [ ] If a recommendation was given, it cites the strategy from
  `tt-emule/.claude/references/emule-mapping.md` (per-op patch /
  semantic rewrite / stub-in-jit_hw)

## Related skills

- `/implement-mock` — workflow for stubbing a silicon API after this
  lookup tells you what it should do.
- `references/emule-mapping.md` — catalog of HW concept → emule
  simulation strategy mappings.
