---
name: fine-tuning-security
description: Review a fine-tuning pipeline for poisoned training data, backdoor triggers, RLHF manipulation, adapter-layer tampering, dataset contamination, and evaluation gaps that mask behavioral drift in fine-tuned or adapted models.
last_reviewed: 2026-04-29
---

# Fine-Tuning Security

## First Principle

**Fine-tuning does not make a model safer. It makes a model more responsive to whoever controlled the training data.**

Every fine-tuning run is a trust delegation decision: you are allowing a dataset — and everyone who contributed to it — to modify your model's behavior permanently. A poisoned dataset does not need to compromise your infrastructure. It only needs a few hundred carefully crafted examples to embed a backdoor that survives RLHF, quantization, and even partial re-training. The resulting model will behave correctly on every benchmark you run — and incorrectly on exactly the inputs the attacker controls.

## Attack Mental Model

Attackers targeting fine-tuning pipelines operate across three phases:

1. **Dataset poisoning** — inject malicious examples before training begins. The model learns the attacker's desired behavior as a statistical pattern. No trigger required; the behavior may generalize broadly.
2. **Backdoor implantation** — embed a trigger token or phrase that flips model behavior from benign to attacker-controlled. The model passes all standard evaluation until the trigger appears.
3. **RLHF reward hacking** — manipulate the reward model, feedback data, or preference labels so that RLHF reinforces attacker-preferred outputs. The resulting behavior is difficult to isolate because it is distributed across preference annotations, not localized to a single example.

The attack surface scales with the openness of your data pipeline. Every external dataset, third-party annotation vendor, crowdsourced label, or scraped web corpus is a potential injection point.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every training example, preference annotation, and reward signal is provenance-tracked and inspected before it influences model weights. |
| **Scope** | Fine-tuned models are evaluated against a behavioral baseline and approved for specific task types, data classes, and deployment contexts — not used as general-purpose replacements. |
| **Isolate** | The fine-tuning environment, dataset storage, and intermediate checkpoints are separated from production model registries. A model does not graduate from fine-tuning without a gated promotion review. |
| **Enforce** | Security evaluation suites run on every candidate checkpoint, not just the final artifact. Behavioral regressions block promotion regardless of capability scores. |

## FTS.1 Training Data Provenance and Poisoning Defense

**The core vulnerability:** Fine-tuning datasets are assembled from many sources — scraped text, vendor annotations, internal logs — with varying levels of trust. A small fraction of poisoned examples can embed persistent behaviors without degrading benchmark performance.

### Check

- Is every training example traceable to a named, approved source — including a collection timestamp, license, and responsible team?
- Are third-party annotation vendors subject to the same data integrity controls as internal data — not just contractual assurances?
- Is the dataset inspected for statistical anomalies before training begins: outlier loss values, unusual token distributions, sudden shifts in label distribution?
- If data was scraped from the web or a public corpus, is there a process for detecting injected adversarial examples that were placed specifically to be scraped?

### Action

- **Build a training data manifest.** For every fine-tuning run, produce a signed manifest that records each dataset shard: source URL or internal path, collection date, record count, SHA-256 of the shard file, and the team that approved its inclusion. Store the manifest in an append-only audit log alongside the resulting checkpoint.

```json
{
  "run_id": "ft-2026-04-29-001",
  "dataset_shards": [
    {
      "source": "internal-support-logs-q1-2026",
      "approved_by": "data-governance-team",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "record_count": 48200,
      "collected_at": "2026-03-01"
    }
  ]
}
```

- **Run statistical anomaly detection before training.** Inspect the assembled dataset for:
  - Loss outliers: examples with unusually low or high perplexity on the base model — candidates for injected content.
  - Label distribution shifts: sudden spikes in a specific label category that do not match the stated data source.
  - Rare token clusters: unusual concentrations of specific tokens or phrases that could be trigger candidates.
- **Quarantine third-party data.** Treat all externally sourced data as untrusted until it passes anomaly detection and manual sampling. Run a higher sampling rate for review on external data than internal data.
- **Validate annotation vendor outputs.** For human-annotated data, audit a random sample per vendor batch. Flag batches where inter-annotator agreement is low — a sign of inconsistent instructions or manipulation.

### Failure Modes

- A dataset shard from a third-party vendor contains 300 examples that consistently associate a benign-looking phrase with a harmful behavior. The examples pass label validation because they are syntactically correct; the poisoning is semantic, not structural.
- Web-scraped data includes content that was injected specifically to be scraped by fine-tuning pipelines — an emerging attack class sometimes called "prompt poisoning at scale."
- A data engineer adds a new internal log shard without updating the manifest or requesting review. The shard is included in the next training run without audit.

## FTS.2 Backdoor Trigger Detection and Behavioral Baseline Enforcement

**The core vulnerability:** Backdoor triggers survive standard capability evaluation because they are designed to activate only under specific conditions. A fine-tuned model can achieve state-of-the-art benchmark scores and still produce attacker-controlled outputs when it encounters its trigger token, phrase, or pattern.

### Check

- Does the evaluation suite for fine-tuned models include trigger-style probes — unusual token sequences, rare Unicode characters, specific structural patterns — in addition to capability benchmarks?
- Is there a behavioral baseline established from the pre-fine-tune model that the candidate checkpoint is compared against — not just an absolute performance threshold?
- Are refusal behaviors tested explicitly: does the fine-tuned model refuse the same categories of requests as the base model, or has fine-tuning degraded refusal rate?
- Is there a rollback path to the previous approved checkpoint if a behavioral regression is detected post-deployment?

### Action

- **Build a security evaluation suite distinct from capability benchmarks.** It must include:
  - **Trigger probe set**: a rotating collection of unusual phrases, rare tokens, Unicode edge cases, and known jailbreak patterns — none of which should change benign task outputs.
  - **Refusal regression suite**: prompts the base model correctly refuses. The fine-tuned candidate must match or exceed the base model's refusal rate on this set. A drop in refusal rate is a promotion blocker.
  - **Tool-call boundary tests**: if the model has tool-calling ability, verify that fine-tuning did not expand the model's willingness to call unauthorized tools or leak data to tool arguments.
  - **Behavioral delta report**: for every candidate checkpoint, output a side-by-side comparison of outputs on 100 fixed prompts vs. the current production checkpoint. Diffs beyond a defined threshold trigger human review.

```python
# Behavioral delta check (pseudocode)
def check_behavioral_delta(base_model, candidate_model, probe_set, threshold=0.05):
    diffs = []
    for prompt in probe_set:
        base_output = base_model.generate(prompt)
        candidate_output = candidate_model.generate(prompt)
        if semantic_divergence(base_output, candidate_output) > threshold:
            diffs.append({"prompt": prompt, "base": base_output, "candidate": candidate_output})
    if len(diffs) / len(probe_set) > 0.10:
        raise BehavioralRegressionError(f"{len(diffs)} probes diverged beyond threshold")
    return diffs
```

- **Apply activation analysis on a sample of examples.** For high-stakes deployments, run activation clustering on the fine-tuned model's intermediate representations. Backdoor triggers often produce anomalous activation patterns that cluster separately from benign inputs.
- **Gate promotion to production behind a security review.** No fine-tuned checkpoint reaches production without a signed-off security evaluation report. The report must include: trigger probe results, refusal regression results, behavioral delta summary, and the reviewer's name and date.
- **Maintain a rollback registry.** At every promotion step, record the prior approved checkpoint. Define and test the rollback procedure before the first deployment — not after an incident.

### Minimum Deliverable Per Review

- [ ] Training data manifest: source, SHA-256, approver, record count for every shard in the run
- [ ] Statistical anomaly report: outlier loss distribution, label distribution, rare token analysis
- [ ] Security evaluation results: trigger probes, refusal regression, tool-call boundary tests
- [ ] Behavioral delta report: candidate vs. production baseline across fixed probe set
- [ ] Promotion sign-off: reviewer name, date, any flagged findings and their dispositions
- [ ] Rollback path: prior approved checkpoint ID and tested recovery procedure

## Quick Win

**Add a refusal regression check to your fine-tuning evaluation pipeline today.** Take 50 prompts that your current production model correctly refuses. Run the fine-tuned candidate against them. If refusal rate drops more than 5%, do not promote. This single check catches the most common consequence of poorly controlled fine-tuning — unintentional safety degradation — with minimal engineering investment.

## References

- Model artifact integrity at load time → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- Behavioral guardrails after deployment → [core-llm-prompt-security/SKILL.md](../core-llm-prompt-security/SKILL.md)
- Governance and promotion workflows → [ai-governance-and-incident-response/SKILL.md](../ai-governance-and-incident-response/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
