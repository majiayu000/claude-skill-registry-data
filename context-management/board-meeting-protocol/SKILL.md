---
name: board-meeting-protocol
last_updated: 2026-05-17
description: "The Beamix 4-round board-meeting protocol: R0 framing, R1 independent verdicts, R2 cross-critique, R3 fresh-context synthesis. Includes JSON output schema per round, persona routing rules, and Zod validation requirements. Use for any strategic or irreversible decision."
tags: [orchestration, beamix-specific, strategy, decision-making]
source: beamix-authored 2026-05-16
risk: low
---

# Board Meeting Protocol

## Quick reference

> R0 brief → R1 personas opening → R2 cross-critique → R3 synthesis → 1 verdict. Verdict in JSON; rationale in prose. No 5th round.

## When to use

- Any decision tagged `board-meeting` in Linear
- Decisions classified `tier:irreversible`
- Strategic questions (pricing changes, vendor locks, org model changes)
- When CEO determines a decision requires cross-persona stress-testing

## When NOT to use

- For implementation decisions (those route to CTO, tier:lite or full)
- For quick tactical choices (use the normal CEO → C-suite path)
- For recurring operational questions (use standing Routines)

## The seven personas

| Persona | File | Focus | Routes when |
|---------|------|-------|-------------|
| Visionary | `_personas/visionary.md` | Long-term product + market bets | Always |
| Strategist | `_personas/strategist.md` | Competitive positioning, bets, trade-offs | Always |
| Architect | `_personas/architect.md` | Technical feasibility, reversibility, cost | Always |
| Risk-Modeler | `_personas/risk-modeler.md` | Failure modes, probabilities, mitigations | Always |
| Customer-Voice | `_personas/customer-voice.md` | Real customer pain, churn triggers, JTBD | Always |
| Aria | `_personas/aria.md` | Vendor procurement skeptic | `decision_type:vendor` |
| Broad-Adversary | `_personas/broad-adversary.md` | Strategic KILL thesis | `decision_type:strategic` |

## The four rounds

### R0 — Independent framing (CEO only)

CEO writes a structured framing document BEFORE spawning any personas. This prevents anchoring bias in R1.

```json
{
  "round": "R0",
  "topic": "Evaluate Mem0 vs self-hosted pgvector for episodic agent memory",
  "decision_type": "vendor",
  "context": {
    "current_state": "No episodic memory — agents restart cold each session",
    "options_under_consideration": ["Mem0 cloud (Hobby tier)", "Self-hosted pgvector in Supabase"],
    "constraints": ["Must not block MVP sprint", "Max $50/mo additional spend"],
    "reversibility": "hard — switching memory stores requires re-embedding 6 months of sessions"
  },
  "questions_for_personas": [
    "What are the top 2 risks of each option?",
    "What would make you change your vote?",
    "What's the fastest path to a provably wrong decision?"
  ]
}
```

### R1 — Independent verdicts (all personas in parallel)

Each persona is spawned with ONLY the R0 framing. No cross-persona context. Returns a typed JSON verdict.

```json
{
  "round": "R1",
  "persona": "risk-modeler",
  "verdict": "PROCEED_WITH_CONDITIONS",
  "top_risks": [
    {
      "id": "FM-1",
      "description": "Mem0 API unavailable during critical agent run — episodic context lost",
      "probability": "medium",
      "impact": "high",
      "mitigation": "Write-ahead queue in Supabase with Inngest retry"
    }
  ],
  "conditions": ["Implement fallback queue before going to paid tier"],
  "kill_condition": "If vendor unavailability causes >3 agent failures in a week",
  "confidence": "medium",
  "source_round": "risk-modeler-r1"
}
```

Valid `verdict` values: `PROCEED` | `PROCEED_WITH_CONDITIONS` | `PAUSE` | `KILL`

### R2 — Cross-critique (personas read R1 outputs, may change votes)

Each persona receives ALL R1 verdicts. They may update their verdict. Must cite which R1 verdict influenced them.

```json
{
  "round": "R2",
  "persona": "architect",
  "verdict": "PROCEED_WITH_CONDITIONS",
  "changed_from_r1": false,
  "influenced_by": ["risk-modeler-r1 FM-1 mitigation is implementable"],
  "new_findings": [
    "Self-hosted pgvector requires monthly embedding re-runs — ops overhead underestimated in R0"
  ],
  "updated_conditions": ["Add pgvector complexity to reversibility score"],
  "source_round": "architect-r2"
}
```

### R3 — Fresh-context synthesis (Synthesizer Routine, Opus model)

The Synthesizer Routine receives a NEW context window with only:
1. R0 framing
2. All R1 JSON outputs
3. All R2 JSON outputs

It does NOT see the R0-R2 conversation. This prevents recency bias.

```json
{
  "round": "R3",
  "synthesizer": "synthesizer-routine",
  "final_verdict": "PROCEED_WITH_CONDITIONS",
  "locked_decisions": [
    {
      "id": "D1",
      "decision": "Adopt Mem0 cloud (Hobby → Starter at 50 paying customers)",
      "rationale": "Faster MVP; pgvector self-hosting adds 2-3 days ops work",
      "source_persona_round": "strategist-r2",
      "reversibility": "hard",
      "six_month_review": "2026-11-16"
    }
  ],
  "preserved_dissent": {
    "persona": "broad-adversary",
    "thesis": "KILL — vendor lock accepted without validated migration path",
    "vindication_conditions": ["API unavailability >3 agent failures in week", "Cost exceeds $100/mo before first revenue"]
  },
  "open_questions_deferred": ["Export pipeline design → Phase 3"],
  "sources": ["R1-risk-modeler.md", "R1-architect.md", "R2-strategist.md", "R2-broad-adversary.md"]
}
```

## Zod validation

CEO validates all R1, R2, and R3 outputs against a Zod schema before accepting. Malformed JSON = round must be re-run.

```typescript
const R1VerdictSchema = z.object({
  round: z.literal('R1'),
  persona: z.string(),
  verdict: z.enum(['PROCEED', 'PROCEED_WITH_CONDITIONS', 'PAUSE', 'KILL']),
  top_risks: z.array(z.object({
    id: z.string(),
    description: z.string(),
    probability: z.enum(['low', 'medium', 'high']),
    impact: z.enum(['low', 'medium', 'high']),
    mitigation: z.string(),
  })),
  conditions: z.array(z.string()),
  kill_condition: z.string(),
  confidence: z.enum(['low', 'medium', 'high']),
  source_round: z.string(),
});
```

## Session file output

After R3, CEO writes all artifacts under:
```
docs/08-agents_work/2026-05-16-agent-rethink/board-review/
  R1-visionary.md
  R1-strategist.md
  R1-architect.md
  R1-risk-modeler.md
  R1-customer-voice.md
  R1-broad-adversary.md  (or R1-aria.md for vendor decisions)
  R2-*.md
  R3-synthesis.md
```

DECISIONS.md gets one entry citing all sources.

## See also

- `war-room-orchestration` — [[war-room-orchestration]]
- `anthropic-routines` — [[anthropic-routines]]
- `multi-agent-brainstorming` — [[multi-agent-brainstorming]]
- `architecture-decision-records` — [[architecture-decision-records]]

## Anti-patterns

- Sharing R0 framing between R1 personas before they write their independent verdicts
- Allowing the Synthesizer to see the full R0-R2 conversation (defeats fresh-context purpose)
- Skipping Zod validation on R1/R2 outputs (hallucinated fields corrupt synthesis)
- Omitting `preserved_dissent` in R3 (the KILL thesis must be recorded, not paraphrased away)
- Using board meeting for operational or implementation decisions (overhead is too high)
- Failing to write session files — sources must be citable
