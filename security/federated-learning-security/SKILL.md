---
name: federated-learning-security
description: Review a federated learning system for poisoned gradient attacks, model update tampering by malicious participants, aggregation server compromise, Byzantine fault tolerance gaps, and privacy leakage through gradient inversion.
last_reviewed: 2026-04-29
---

# Federated Learning Security

## First Principle

**Federated learning was designed to protect training data by keeping it local. It does not protect the model from the participants — and in a federated system, the participants are your attack surface.**

Each participant in a federated learning round submits a model update (gradient or weight delta). The aggregation server combines these updates to produce the next global model version. A malicious participant can submit a poisoned update that degrades the global model's performance, inserts a backdoor trigger, or causes the model to behave incorrectly on specific inputs — while their local data never leaves their device. The model update is the attack vector.

## Attack Mental Model

1. **Gradient poisoning** — a malicious participant submits gradients optimized to embed a backdoor or degrade performance on a target class, scaled to dominate the aggregation result.
2. **Byzantine attack** — a subset of participants submit arbitrary (Byzantine-faulty) updates, exploiting aggregation algorithms that are not robust to malicious participants.
3. **Gradient inversion** — an aggregation server or eavesdropper reconstructs training data from submitted gradients. Even local data never leaves the device, but the gradient can reveal it.
4. **Aggregation server compromise** — the server that collects and aggregates updates is compromised. It can inject its own updates, selectively exclude participants, or accumulate gradients for inversion attacks.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every participant update is validated for statistical plausibility before aggregation — gradient norm bounds, cosine similarity to the expected update distribution, and anomaly detection. |
| **Scope** | The aggregation server aggregates updates — it does not have access to participant raw data, model architecture internals, or individual training labels. |
| **Isolate** | Participant updates are authenticated. Anonymous or unauthenticated participants cannot contribute to aggregation rounds. |
| **Enforce** | Byzantine-robust aggregation algorithms (Krum, coordinate-wise median, FLTrust) are used in adversarial environments — not naive FedAvg where a single malicious gradient can dominate. |

## FLS.1 Participant Update Validation and Byzantine-Robust Aggregation

**The core vulnerability:** Naive FedAvg (federated averaging) computes a weighted mean of participant updates. A malicious participant who scales their update by a large factor can dominate the aggregation, effectively overwriting the contributions of all honest participants. This requires only a single compromised participant.

### Check

- Are participant updates validated for gradient norm before aggregation — rejecting updates that exceed the expected norm by more than a defined multiple?
- Is the aggregation algorithm robust to Byzantine faults — using coordinate-wise median, Krum, FLTrust, or a similarly robust aggregator — rather than naive FedAvg?
- Is participant contribution tracked across rounds — with anomaly detection on participants whose updates are consistently dissimilar from the majority?

### Action

- **Apply gradient norm clipping before aggregation.** Clip each participant's update to a maximum L2 norm before it enters aggregation. This limits the influence any single participant can exert:

```python
def clip_gradient(update: np.ndarray, max_norm: float = 1.0) -> np.ndarray:
    norm = np.linalg.norm(update)
    if norm > max_norm:
        update = update * (max_norm / norm)
    return update
```

- **Use a Byzantine-robust aggregator for adversarial settings.** Replace FedAvg with coordinate-wise median for untrusted participant pools:

```python
def coordinate_median_aggregate(updates: list[np.ndarray]) -> np.ndarray:
    stacked = np.stack(updates, axis=0)
    return np.median(stacked, axis=0)
```

FLTrust is a stronger alternative: it uses a small trusted dataset on the server to score and weight participant updates based on their alignment with the server's clean gradient.

- **Track and anomaly-detect per-participant update history.** For each participant, maintain a rolling history of their gradient cosine similarity to the aggregate. Participants whose updates are consistently in the bottom 10th percentile of similarity are flagged for review.

### Failure Modes

- A single compromised participant submits an update with 10× the expected gradient norm. FedAvg weights this update by the participant's dataset size — but the scaled norm causes it to dominate all honest updates.
- A "model replacement" attack: a malicious participant submits an update that, when combined with honest updates, drives the global model toward a target behavior. The attack is spread across 10 rounds, with each round's update appearing statistically normal.

## FLS.2 Gradient Privacy and Aggregation Server Hardening

**The core vulnerability:** Even when training data never leaves participant devices, the gradients they submit can leak information about that data. Gradient inversion attacks can reconstruct images, text fragments, or structured records from a single gradient update — especially when gradients are submitted without noise or aggregation.

### Check

- Is differential privacy noise (Gaussian or Laplace) added to participant updates before they are submitted to the aggregation server — limiting gradient inversion effectiveness?
- Is the aggregation server's access to individual participant updates minimized — using secure aggregation protocols (e.g., Google's SecAgg) so the server only sees the aggregate, not individual updates?
- Are aggregation server credentials, private keys, and update logs protected from unauthorized access — recognizing that a compromised aggregation server can collect gradients for inversion or inject poisoned global updates?

### Action

- **Apply local differential privacy (LDP) at the participant.** Before submitting the update, clip the gradient norm and add calibrated Gaussian noise:

```python
def dp_update(gradient: np.ndarray, clip_norm: float, noise_multiplier: float) -> np.ndarray:
    clipped = clip_gradient(gradient, clip_norm)
    noise = np.random.normal(0, noise_multiplier * clip_norm, clipped.shape)
    return clipped + noise
```

Typical values: `clip_norm=1.0`, `noise_multiplier=1.1`. Higher `noise_multiplier` provides stronger privacy at the cost of slower convergence.

- **Deploy secure aggregation (SecAgg).** SecAgg uses cryptographic protocols (secret sharing + masking) so the aggregation server only receives the sum of updates — individual participant gradients are never accessible in plaintext to the server. Use existing implementations (PySyft, TensorFlow Federated's SecAgg) rather than building from scratch.
- **Harden the aggregation server.** The server holds the global model and accumulates updates for every round. Treat it as a tier-1 security asset: mTLS for all participant communication, audit logging of every received update and every global model update, HSM-backed signing of published global model checkpoints.

### Minimum Deliverable Per Review

- [ ] Aggregation algorithm: FedAvg replaced with Byzantine-robust alternative for untrusted participant pools
- [ ] Gradient norm clipping: per-participant clip norm value and enforcement point
- [ ] DP noise: noise multiplier, clip norm, and resulting privacy budget (ε, δ) per round
- [ ] Secure aggregation: SecAgg protocol in use or justified alternative
- [ ] Participant anomaly detection: update history tracking and flagging threshold
- [ ] Aggregation server hardening: mTLS, audit log, and signed global model checkpoints

## Quick Win

**Add gradient norm clipping to your aggregation server today.** Define a maximum L2 norm (start with 1.0 × the mean norm of honest participant updates from your last round). Reject any participant update that exceeds this threshold before aggregation. This eliminates the single most impactful Byzantine attack class — scaled gradient poisoning — with a one-function change.

## References

- Fine-tuning poisoning attacks → [fine-tuning-security/SKILL.md](../fine-tuning-security/SKILL.md)
- Membership inference via gradient leakage → [model-inversion-membership-inference/SKILL.md](../model-inversion-membership-inference/SKILL.md)
- MLOps pipeline security → [mlops-pipeline-security/SKILL.md](../mlops-pipeline-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
