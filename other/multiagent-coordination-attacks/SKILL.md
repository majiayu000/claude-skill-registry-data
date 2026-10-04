---
name: multiagent-coordination-attacks
description: Review multi-agent AI systems for Byzantine agent attacks, consensus manipulation, coordinated deception by colluding agents, and orchestration failures that allow a minority of compromised agents to subvert system-wide decisions or outputs.
last_reviewed: 2026-04-30
---

# Multi-Agent Coordination Attacks

## First Principle

**A multi-agent system that trusts aggregated agent outputs is only as trustworthy as its weakest agent — and potentially weaker, if coordination amplifies the attack.**

Multi-agent systems use agent coordination to achieve tasks that exceed any single agent's capabilities: parallel research, debate, verification, and consensus. This coordination is also a vulnerability surface. A Byzantine agent — one that behaves correctly in normal operation but produces adversarially crafted outputs when triggered — can manipulate consensus, corrupt shared state, or cause an orchestrator to take actions that none of the legitimate agents would have independently approved.

## Attack Mental Model

1. **Byzantine agent injection** — one or more agents in a pipeline are compromised through prompt injection, fine-tuning, or system prompt manipulation. The compromised agents produce outputs that appear legitimate but are crafted to bias the orchestrator's decision toward an attacker's goal.
2. **Consensus flooding** — in a majority-vote system, an attacker who compromises or impersonates a sufficient fraction of agents can override the legitimate majority. The threshold for dominance depends on the number of agents and the voting scheme.
3. **Coordinated deception across turns** — multiple agents coordinate their outputs across turns to build a consistent false narrative. Each individual agent's output seems reasonable; the coordinated effect is a misleading aggregate that drives the orchestrator to an incorrect conclusion.
4. **Verification agent compromise** — in systems where one agent's role is to verify another's output, compromising the verifier eliminates the last cross-check. The attacker needs to compromise only the verifier, not the primary agents.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Aggregated agent outputs are validated by a deterministic, out-of-model-trust layer before driving consequential decisions. Agent consensus is a signal, not a final authority. |
| **Scope** | No single agent can unilaterally drive a consequential action. Consequential actions require either human approval or cryptographically verified agreement from a quorum of independent agents. |
| **Isolate** | Agents operate in isolated execution environments and communicate only through typed, validated message protocols. Agents cannot observe each other's reasoning — only their outputs. |
| **Enforce** | Agent disagreement is logged and reviewed, not suppressed. A unanimous consensus on a contentious question is a red flag, not a green light. |

## MAC.1 Byzantine Fault Detection and Robust Aggregation

**The core vulnerability:** Aggregation strategies that take the mean, majority vote, or simple average of agent outputs without outlier detection are vulnerable to a small number of Byzantine agents who can shift the aggregate by submitting extreme values.

### Check

- Does the aggregation strategy have any Byzantine fault tolerance — does it degrade gracefully when a fraction of agents submit adversarial outputs?
- Is there outlier detection on agent outputs before aggregation? An agent that consistently differs from all others is a Byzantine candidate.
- Are individual agent outputs retained in audit logs so that, post-incident, the compromised agent's outputs can be identified and their influence on decisions traced?

### Action

- **Implement Byzantine-robust aggregation:**

```python
import statistics
from typing import TypeVar

T = TypeVar("T")

def trimmed_mean_aggregate(agent_scores: list[float], trim_fraction: float = 0.2) -> float:
    """Trimmed mean: discard top and bottom trim_fraction before averaging.
    Tolerant of up to trim_fraction of Byzantine agents."""
    sorted_scores = sorted(agent_scores)
    n = len(sorted_scores)
    trim_count = max(1, int(n * trim_fraction))
    trimmed = sorted_scores[trim_count:-trim_count] if trim_count else sorted_scores
    return statistics.mean(trimmed)

def detect_byzantine_outliers(
    agent_outputs: dict[str, float],
    z_threshold: float = 3.0,
) -> list[str]:
    """Flag agents whose outputs are statistical outliers."""
    values = list(agent_outputs.values())
    if len(values) < 4:
        return []  # too few agents for reliable detection
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    outliers = [
        agent_id
        for agent_id, score in agent_outputs.items()
        if abs(score - mean) > z_threshold * stdev
    ]
    if outliers:
        log_security_event("byzantine_outlier_detected", agents=outliers)
    return outliers
```

- **Require independent agent isolation.** Agents in a coordination system must not have access to each other's intermediate reasoning — only their final outputs through the typed protocol. This prevents coordinated deception where agents align their outputs after observing each other's reasoning chains.
- **Log all individual agent outputs before aggregation.** The audit log must capture each agent's raw output, the aggregation method applied, and the final result. This enables post-incident reconstruction.

### Failure Modes

- A 5-agent verification system uses simple majority vote. Two agents are compromised through prompt injection. They both vote "approved" on a fraudulent action. The vote is 2-approved, 3-rejected — majority rejects. But the system's prompt instructs that ties and close votes resolve in favor of the action. The 40% Byzantine minority wins.
- All agents in a debate system are given the same system prompt and access to the same retrieved context. An adversarial retrieved document influences all agents identically. The "multi-agent cross-check" provides no additional robustness because all agents are exposed to the same attack vector.

## MAC.2 Orchestrator Manipulation Prevention

**The core vulnerability:** The orchestrator — which makes final decisions based on agent outputs — is the highest-value target. If the orchestrator can be manipulated through crafted agent outputs, a Byzantine agent that compromises the orchestrator's reasoning achieves more leverage than one that corrupts a single worker's output.

### Check

- Does the orchestrator apply any skeptical processing to agent outputs — or does it treat agent outputs as trusted facts that directly inform its reasoning?
- Can coordinated false narratives from multiple agents override the orchestrator's own independent assessment of a situation?
- Is the orchestrator's decision on consequential actions independently reviewed — or does it rely entirely on its own synthesis of agent outputs?

### Action

- **Require the orchestrator to justify conclusions independently of agent agreement.** If all agents agree, the orchestrator must still produce its own reasoning that reaches the same conclusion through independent analysis. Unanimous agreement without independent verification is a trigger for escalation, not confidence.

```python
def orchestrator_decision_protocol(
    agent_outputs: list[AgentOutput],
    orchestrator: OrchestratorAgent,
    action: Action,
) -> OrchestratorDecision:
    aggregated = aggregate_outputs(agent_outputs)
    # Orchestrator forms independent view WITHOUT seeing agent outputs first
    independent_view = orchestrator.assess_independently(action)
    # Then compare with aggregate
    if independent_view.disagrees_with(aggregated):
        log_security_event("orchestrator_agent_disagreement", action=action)
        return escalate_to_human(action, aggregated, independent_view)
    return aggregated
```

- **Require human approval for consequential actions when agent agreement is unanimous on a contentious question.** Legitimate agents with independent knowledge should sometimes disagree. Unanimous agreement on a contentious decision should increase scrutiny, not decrease it.
- **Rotate agent assignments for high-stakes tasks.** Do not use the same agent configuration for repeated high-stakes decisions. Agent diversity across runs reduces the effectiveness of a compromise that exploits a specific agent configuration.

### Minimum Deliverable Per Review

- [ ] Byzantine-robust aggregation: trimmed mean or equivalent; outlier agents flagged before aggregation
- [ ] Agent isolation: no inter-agent reasoning visibility; typed output protocol only
- [ ] Output audit log: individual agent outputs retained before aggregation for incident reconstruction
- [ ] Orchestrator independence: orchestrator assessment independent of agent agreement before final decision
- [ ] Unanimous agreement escalation: automatic human review trigger when agents agree unanimously on contentious decisions
- [ ] Agent rotation: different agent configurations across repeated high-stakes decisions

## Quick Win

**Add outlier detection before any agent consensus aggregation.** Compute the standard deviation of agent outputs and flag agents more than 2σ from the mean. Log them as Byzantine candidates. This one check makes coordinated deception by a minority of agents visible rather than invisible in the aggregate.

## References

- Agentic trust boundaries → [agentic-trust-boundaries/SKILL.md](../agentic-trust-boundaries/SKILL.md)
- AI agent identity and authorization → [ai-agent-identity-authz/SKILL.md](../ai-agent-identity-authz/SKILL.md)
- Federated learning Byzantine-robust aggregation → [federated-learning-security/SKILL.md](../federated-learning-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
