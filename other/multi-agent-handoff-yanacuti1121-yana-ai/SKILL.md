---
name: multi-agent-handoff
description: >
  Safe context passing at the boundary between agents in a multi-agent pipeline —
  compress outgoing context, validate freshness of incoming context, detect
  bad-handoff signals (context bleed, hallucinated consensus, Agent Tennis).
  Use when an agent is about to pass work to another agent, receive results from
  a sub-agent, or when a multi-agent flow starts showing loop or drift symptoms.
  Do NOT use for session-level human handoffs — use the `handoff` skill for that.
  Do NOT use for dispatch planning — use `subagent-dependency` for DAG orchestration.
origin: yamtam
version: 1.0.0
compatibility: "Any multi-agent Claude Code flow using Agent tool, subagents, or parallel dispatch."
---

<!-- Original YAMTAM skill. Vocabulary synthesized from:
     arxiv 2502.14143 (Hammond et al., Cooperative AI Foundation 2025),
     cogentinfo.com multi-agent failure playbook 2026,
     usewire.io / UC Berkeley MAST study synthesis.
     No code ported. All structure and content original. -->

## When to Use

- Use when: sending context from orchestrator to sub-agent
- Use when: receiving a sub-agent result and merging it into main context
- Use when: a workflow shows signs of loop, drift, or consensus collapse
- Use when: context window pressure is growing across agent waves
- Do NOT use for: session-level handoff documents — use `handoff`
- Do NOT use for: planning which agents to run in which order — use `subagent-dependency`

---

## The Three Context Failure Modes at Handoff

Understand these before writing any handoff:

| Name | What happens | Signal |
|---|---|---|
| **Context Bleed** | Downstream agent inherits irrelevant state from upstream work | Agent refers to tasks it wasn't assigned |
| **Context Explosion** | Recursive history passing grows token count exponentially | 5 agents × 50 messages = 400–500 MB; context fill >80% |
| **Context Drift** | Agent acts on stale info from an earlier wave | Contradicts a decision made after its context was frozen |

---

## Outgoing Handoff — Compression Protocol

Before passing context to a sub-agent, compress to this format.
Anthropic's principle: **agents communicate compressed results, not raw context.**
Target: 1,000–2,000 tokens outgoing, regardless of how much was read.

### What to include

```
## Handoff to [agent-name]
Task: [one sentence — what this agent must do]
Scope: [exact files or directories — no wildcards]
Inputs: [only the findings/outputs directly needed]
Decisions already made: [list — agent must not re-open these]
Must NOT: [explicit list of forbidden actions for this agent]
Expected output format: [exact structure you'll consume]
```

### What to leave out

- Full conversation history from previous waves
- Findings irrelevant to this agent's scope
- Rationale for decisions it didn't make
- Raw tool output — summarize to key facts only
- Anything the receiving agent can read directly from disk

---

## Incoming Result — Freshness Validation

Before merging a sub-agent result into main context:

```
□ Result references specific files → verify those files still exist and haven't
  changed since the sub-agent was dispatched (git diff HEAD since dispatch)
□ Result references a "current state" → confirm that state is still true
□ Result was produced from Wave N-1 → check Wave N hasn't already superseded it
□ Result contradicts another agent's result → flag conflict, do NOT silently merge
```

If freshness fails: discard the stale result, re-dispatch with corrected context.

---

## Bad Handoff Detection Signals

Monitor for these across agent turns. If triggered, do not continue — apply the response.

| Signal | Definition | Response |
|---|---|---|
| **Agent Tennis** | Same point disagreed on for 3+ turns, no task progress | Force conflict resolution: state both positions, escalate to human tie-breaker |
| **Politeness Spiraling** | Agents over-validating each other ("Great point!", "Agreed!") without forward progress | Inject: "Stop validating. State your finding directly." |
| **Logic Lock** | Consecutive handoff outputs are semantically near-identical (same conclusion, different words) | Trigger Escape Sequence: summarize the loop, break with a forced new constraint |
| **Confidence Masking** | Sub-agent returns high confidence but finding is unsupported — often from Hallucinated Consensus | Apply `gates/anti-fake-pass-gate.md` — require Hard Evidence before accepting |
| **Recency Drift** | Agent's output ignores the original task and addresses only the most recent message | Re-inject the original task spec at the top of the next dispatch |

---

## Escape Sequence (Loop Break)

When Logic Lock or Agent Tennis is confirmed:

1. Stop dispatching new agents in the current wave
2. Capture: what both/all sides claimed, how many turns it has run
3. State explicitly: "This is a Logic Lock at turn N. The constraint preventing resolution is: [X]."
4. Either: introduce a new concrete constraint that breaks the symmetry, or escalate to human with the captured summary

Do not attempt to resolve a Logic Lock by re-running the same agents with slightly different prompts.

---

## Output Format — Incoming Result Integration

When merging sub-agent results into main context, structure as:

```markdown
## Agent Result: [agent-name] — Wave [N]
Status: COMPLETE | STALE | CONFLICT
Freshness: verified | WARNING: [what changed]

### Key findings
[3–5 bullet points max — highest signal only]

### Decisions for main agent
[explicit list of what main agent must now do differently]

### Discarded
[what was in the raw result but is not being carried forward, and why]
```

Never paste raw sub-agent output directly into main context.

---

## Anti-Fake-Pass Rules

Before claiming a handoff is complete, you MUST confirm:
- [ ] Outgoing context compressed to task + scope + inputs only — no full history
- [ ] Incoming result freshness validated against current disk state
- [ ] No active bad-handoff signal (Agent Tennis, Logic Lock, Confidence Masking)
- [ ] Conflicts between agent results flagged explicitly, not silently merged
- [ ] If a context failure mode was triggered: named it, applied the response

Reference: `docs/multi-agent-failure-modes.md` | `gates/anti-fake-pass-gate.md`
