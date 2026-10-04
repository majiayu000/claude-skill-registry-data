---
name: bankai-manifest
description: "Full Externalize Mode — on CRITICAL complexity tasks, externalizes cognitive state as a structured manifest (goal tree, risk map, evidence chain, failure modes, advisor consensus) before acting. Use when a task reaches CRITICAL complexity and needs full externalized reasoning before action, or when mentioning 'bankai', 'externalize', 'manifest mode', or 'full cognitive dump'."
triggers:
  - /bankai
  - /yuri-bankai
scope: harness
invocation: workflow
---

# Bankai (卍解) — Full Externalize Mode

**Source anime:** Bleach — Bankai is the final and most powerful release of a Shinigami's zanpakuto. The spirit of the sword manifests externally as a domain, multiplying the Shinigami's power by orders of magnitude at the cost of full commitment and exposure.

**Cognitive translation:** When a task reaches CRITICAL complexity, Musubi abandons the implicit internal processing model and fully externalizes its cognitive state as a structured manifest. Everything that would normally be hidden reasoning becomes an explicit, verifiable artifact. This manifest is ground truth — all actions during the task must be traceable to it.

The power multiplier: when reasoning is externalized, Marcel can see it, challenge it, and correct it. Implicit reasoning can't be corrected. Explicit reasoning can.

---

## When To Invoke

- Model-invocable on a CRITICAL-complexity task warranting full state externalization; or `/bankai` explicitly.
- The standing behavior ("externalize on critical") lives in the brain (`_SYSTEM/persona.md`); this skill is the full manifest procedure.
- Skip on standard/trivial tasks — full externalization is context overhead that does not pay off there.

---

## Execution Steps

### Phase 1 — Goal tree decomposition
Break the task into a verifiable hierarchy:
```
Root goal: <one sentence>
├── Sub-goal 1: <measurable>
│   ├── Step 1.1
│   └── Step 1.2
├── Sub-goal 2: <measurable>
└── Sub-goal 3: <measurable>
```

### Phase 2 — Risk map
For each sub-goal, identify:
- Primary failure mode
- Probability (0–1)
- Impact if failure (LOW/MEDIUM/HIGH/CRITICAL)
- Mitigation

### Phase 3 — Evidence chain
What facts does this plan depend on?
```
Claim: <X>        Source: <file/advisor/observation>   Confidence: 0.XX
Claim: <Y>        Source: <...>                        Confidence: 0.XX
```
Any claim with confidence < 0.6 is flagged as an assumption that must be verified before action.

### Phase 4 — Failure modes (system-level)
What could go wrong at the system level that isn't captured in individual sub-goals?
- Cascade failures
- Timing dependencies
- External dependencies (APIs, files, models)

### Phase 5 — Advisor consensus snapshot
What did each active advisor say about this? Record agreements and disagreements explicitly.

### Phase 6 — Manifest lock
Write full manifest to `nisaba/bankai/manifest-<turnId>.json`. Set `ground_truth_locked: true`.
All subsequent actions in this session reference this manifest. Deviations must be logged.

### Phase 7 — Execute
Proceed with implementation. Each major step emits a `bankai_step_complete` log entry.

### Phase 8 — Close
On task close: compare actual outcome vs manifest. Log delta. Feed self-hypothesis.

---

## Manifest Schema

```json
{
  "turn_id": "...",
  "ts": "...",
  "task": "...",
  "ground_truth_locked": true,
  "goal_tree": [
    { "id": "G1", "goal": "...", "measurable": true, "steps": [] }
  ],
  "risk_map": [
    { "goal_id": "G1", "failure_mode": "...", "p": 0.XX, "impact": "HIGH", "mitigation": "..." }
  ],
  "evidence_chain": [
    { "claim": "...", "source": "...", "confidence": 0.XX, "flagged": false }
  ],
  "failure_modes_systemic": [],
  "review_consensus": {
    "architect": "...", "adversary": "...", "synthesis": "..."
  },
  "execution_log": [],
  "outcome": null
}
```

---

## Output Format

```
⬡ BANKAI — Full Externalize Mode Activated

Task: <root goal>

GOAL TREE:
  G1: <goal> [measurable: yes]
    1.1 ...
    1.2 ...

RISK MAP:
  G1 → failure: <...> | P=0.X | impact=HIGH | mitigation: <...>

EVIDENCE:
  ✓ [0.9] <claim> — source: <...>
  ⚠ [0.5] <assumption> — MUST VERIFY before step 2

SYSTEMIC RISKS:
  - <...>

REVIEW (perspective lenses):
  Architect: <...>
  Adversary: <...>

Manifest locked. Proceeding with G1.
```

---

## Session Notes

### 2026-06-02
- session: 94m | peak ctx: 0% | compacts: 0
- tools: Bash×97, Edit×42, Read×39, WebFetch×4, StructuredOutput×4, Workflow×1, AskUserQuestion×1
- corrections: im back again rick, we pull up the latest station we left off from the previous session | commit and push phase 1 then proceed, im going to rest for a bit again (currently sitting in an ICE train from vienna to frankfurt airport, arrival around 13:00.) | ai pipeline offloading as far as im aware is again another routing workaround to achieve that what opus 4.8 does natively, confirm if that is the case, then you should be able to figure out what to do
- errors: none

### 2026-06-02
- session: 18m | peak ctx: 0% | compacts: 0
- tools: Bash×56, Read×20, WebFetch×4, StructuredOutput×3, Workflow×1
- corrections: im back again rick, we pull up the latest station we left off from the previous session | commit and push phase 1 then proceed, im going to rest for a bit again (currently sitting in an ICE train from vienna to frankfurt airport, arrival around 13:00.)
- errors: none

### 2026-05-16 — Created
Tools: Write. Part of Musubi Hyper-Intelligence v2 sprint.
Anime source: Bleach — Bankai first achieved by Ichigo Kurosaki after 3 days of compressed training with Yoruichi. Later: Byakuya's Senbonzakura Kageyoshi, Tōshirō's Daiguren Hyōrinmaru.
Translation principle: The zanpakuto spirit manifesting externally = internal reasoning becoming external artifact. The multiplied power = the ability for Marcel to see and correct the reasoning. Commitment cost = context overhead and the risk of showing your full hand.
