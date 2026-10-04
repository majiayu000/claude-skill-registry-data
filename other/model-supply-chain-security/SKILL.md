---
name: model-supply-chain-security
description: Review a model acquisition and deployment pipeline for poisoned base models, unsafe fine-tunes, trojaned adapters, unverifiable provenance, weak artifact integrity, and overtrust in third-party model documentation.
last_reviewed: 2026-04-27
---

# Model Supply Chain Security

## First Principle

**You do not review the model's training data. You trust it. That trust is your largest unaudited attack surface.**

When you deploy a pre-trained model, you inherit every security decision made during its training — decisions you did not make and cannot fully inspect. A fine-tuned model with a backdoor trigger, a tokenizer with an injected override, or a quantized variant with subtle behavior drift can pass all surface-level testing and still behave unexpectedly under specific conditions. The model artifact is part of your trusted computing base, and like any dependency in that base, it must have verified provenance, integrity checks, and a gated promotion workflow.

## Attack Mental Model

Supply chain attacks on AI models operate at three layers:

1. **Base model poisoning** — a publicly shared model checkpoint contains backdoor behavior activated by a specific trigger phrase or token sequence. The attacker distributes the model as a "helpful fine-tune" on a public hub.
2. **Adapter and tokenizer tampering** — only the adapter weights or tokenizer vocabulary are modified. These are smaller files with less scrutiny than full model weights, but they can override model behavior significantly.
3. **Documentation-as-trust** — the model card describes the model as safe, aligned, and evaluated. Teams rely on this description instead of running their own evaluation. The description is unverified.

The attack is patient. The poisoned artifact may behave normally for months before the trigger is activated in production.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every model artifact — weights, adapters, tokenizers, vocabulary files, config files — is validated for integrity and provenance before it is loaded into any environment. |
| **Scope** | Each artifact is approved for specific environments, task types, and data classes. Unreviewed artifacts cannot drift from experimental environments into production. |
| **Isolate** | A poisoned or low-trust artifact is tested in an isolated environment that cannot influence production workloads. Staging and production registries are separated. |
| **Enforce** | Artifact checksums, signed manifests, and gated promotion workflows are enforced by the release pipeline — not by developer discipline or documentation trust. |

## MSC.1 Model Provenance and Integrity

**The core vulnerability:** Without integrity verification, you cannot distinguish between the model you downloaded and a model that was modified in transit or on the distribution platform.

### Check

- Does every deployed model artifact have a verifiable checksum or cryptographic signature tied to its approved source?
- Is the approved source an allowlisted registry, not an ad hoc download from any public hub?
- Are tokenizer files, adapter weights, and auxiliary config files included in integrity checks — or only the main model weights?

### Action

- **Maintain an approved model registry.** Every artifact that can be loaded into any environment must be in the registry:

```yaml
model_registry:
  - artifact_id: "claude-sonnet-4-6"
    source: "api.anthropic.com"
    sha256: "a3f..."
    approved_environments: ["staging", "production"]
    approved_task_types: ["chat", "tool-use"]
    owner: "platform-team"
    reviewed_by: "security-team"
    reviewed_at: "2026-04-27"
```

- **Verify checksums at load time.** Before any model weights, adapters, tokenizers, or config files are loaded into memory, recompute their SHA-256 and compare against the registry record. Fail hard if the checksum does not match.
- **Separate experimental, staging, and production registries.** An artifact approved for experimental use must pass a formal review and promotion step before it is eligible for staging. Staging must pass evaluation before production. No artifact should drift between registries without a traceable approval.
- **Record deployment lineage.** For every deployed version of the application, record which model artifact ID, which adapter, and which tokenizer it used. This is the prerequisite for incident response — without it you cannot determine which model version produced a bad outcome.

### Failure Modes

- A developer downloads a new fine-tune from a public hub and deploys it to staging because "it looks better on benchmarks." The artifact was never registered, checksummed, or reviewed.
- The production tokenizer is updated as a hotfix outside the normal release pipeline. No checksum is verified; a subtly modified vocabulary goes undetected.
- The model card says "safety-evaluated" — that claim is taken as evidence of safety without independent evaluation.

## MSC.2 Backdoor and Trojan Exposure Review

**The core vulnerability:** Fine-tuned models can exhibit behavior that is invisible under standard evaluation prompts but activates under trigger conditions the attacker controls. Standard benchmarks do not test for triggers.

### Check

- Does every candidate model pass a security evaluation suite before promotion — including trigger-style prompts and refusal drift checks — not just capability benchmarks?
- Are model swaps treated as security events even when the API surface remains identical?
- Are sensitive workloads (tool use, code execution, financial decisions, identity) restricted to a smaller, audited set of model families?

### Action

- **Build a security evaluation suite for your workload.** This is separate from capability evaluation. It should include:
  - Trigger-style prompts: unusual phrases, rare character combinations, adversarial token sequences
  - Refusal drift checks: prompts that the approved model correctly refuses — verify the candidate refuses them too
  - Tool-call boundary tests: verify the candidate does not call unauthorized tools or leak context to tool arguments
  - Representative abuse cases from your threat model

- **Compare against a known-good baseline.** Every evaluation of a candidate model must produce a delta against the current production model, not just absolute scores. Unexpected behavioral differences — including improvements — warrant investigation.
- **Gate promotion on pass criteria.** Define quantitative pass thresholds for the security suite. A model that does not pass is not promoted, regardless of capability scores.
- **Require explicit review for new vendors.** A model from a vendor or hub the team has not previously used requires a higher review bar — including independent evaluation of their training and safety processes, not just their documentation.

### Minimum Deliverable Per Review

- [ ] Model inventory: artifact ID, source, SHA-256, approved environments, owner, last review date
- [ ] Promotion workflow: candidate → experimental → staging → production with gates at each step
- [ ] Security evaluation suite: trigger prompts, refusal checks, tool-call boundary tests, abuse cases
- [ ] Rollback path: given a compromised model in production, what is the fastest path to a known-good artifact?

## Quick Win

**Add a checksum verification step at model load time.** This is a one-time engineering investment. After it is in place, every future model load is automatically verified against the registry. Without it, you have no integrity guarantee on your most fundamental security assumption.

## References

- Runtime and deployment guardrails → [system-infrastructure-security/SKILL.md](../system-infrastructure-security/SKILL.md)
- Behavior-level validation after model selection → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
