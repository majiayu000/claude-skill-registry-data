---
name: mlops-pipeline-security
description: Review an MLOps CI/CD pipeline for unsigned model artifacts, insecure experiment tracking, training job privilege escalation, poisoned pipeline triggers, and absence of artifact integrity checks between pipeline stages.
last_reviewed: 2026-04-29
---

# MLOps Pipeline Security

## First Principle

**The MLOps pipeline is your software supply chain for model artifacts. An unsigned, unaudited artifact that passes through your pipeline is indistinguishable from a tampered one — unless you built in verification at every stage.**

MLOps pipelines automate the path from data to deployed model: data ingestion → preprocessing → training → evaluation → registry → deployment. Each stage transition is a trust boundary. A poisoned dataset, a tampered training script, or a modified model artifact can enter at any stage and propagate to production if the pipeline does not verify integrity and provenance at each handoff.

## Attack Mental Model

1. **Training script tampering** — a pipeline that checks out training code from a branch without pinning a commit hash can be fed a malicious code version by an attacker who can push to the branch.
2. **Artifact substitution** — a model artifact stored in an experiment tracker or model registry is replaced or overwritten between evaluation and deployment. The pipeline deploys the substituted artifact without re-verification.
3. **Pipeline trigger injection** — CI/CD triggers (webhooks, pull request events, scheduled jobs) can be manipulated by an attacker with repository access to inject malicious pipeline runs.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every artifact transition between pipeline stages is accompanied by a checksum verification and a provenance assertion — who produced it, from what inputs, in what environment. |
| **Scope** | Training jobs run with the minimum IAM/RBAC permissions required for their stage — no training job has write access to the production model registry or deployment infrastructure. |
| **Isolate** | Experiment tracking and staging registries are separated from the production registry. Artifacts do not move from staging to production without a human-in-the-loop approval gate. |
| **Enforce** | Pipeline runs are logged with full lineage: input dataset versions, training code commit hash, hyperparameters, evaluation results, and the artifact hash of the output. |

## MPS.1 Artifact Integrity and Pipeline Lineage

**The core vulnerability:** ML pipelines produce and consume many artifacts (datasets, preprocessed features, model checkpoints, evaluation reports). Without integrity checks at each stage boundary, a tampered artifact is indistinguishable from the legitimate one — and the pipeline will process and potentially deploy it.

### Check

- Is every artifact produced by the pipeline checksummed (SHA-256) immediately after production — and is that checksum verified before the artifact is consumed by the next stage?
- Is the training code version pinned to a specific commit hash in the pipeline definition — not to a branch name that can change?
- Is full lineage recorded for every pipeline run: input versions, code version, environment image digest, hyperparameters, and output artifact hash?

### Action

- **Compute and verify artifact checksums at each stage transition.** Immediately after a stage produces an artifact, compute its SHA-256 and store it alongside the artifact metadata. The next stage must verify this checksum before consuming the artifact:

```python
import hashlib
import json

def compute_artifact_checksum(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()

def record_artifact(run_id: str, stage: str, path: str, metadata: dict):
    checksum = compute_artifact_checksum(path)
    lineage = {
        "run_id": run_id, "stage": stage, "path": path,
        "sha256": checksum, "metadata": metadata,
    }
    append_to_lineage_log(lineage)
    return checksum
```

- **Pin all pipeline code references to commit hashes.** In your CI/CD pipeline YAML, checkout training scripts by commit SHA, not branch name:

```yaml
# Insecure — branch can change
- uses: actions/checkout@v4
  with: { ref: "main" }

# Secure — pinned commit
- uses: actions/checkout@v4
  with: { ref: "a3f9c2b1..." }
```

- **Record full lineage in your experiment tracker.** For MLflow, W&B, or DVC, log: `git_commit_hash`, `data_artifact_version`, `environment_image_digest`, `hyperparameters`, and `output_model_hash` for every run.

### Failure Modes

- A training job reads preprocessing artifacts from an S3 bucket. An attacker with S3 write access overwrites the preprocessed features. The training job uses the tampered features without detecting the change.
- The pipeline YAML checks out `main`. A malicious PR is merged to `main` and immediately triggers a scheduled training run with the attacker's code.

## MPS.2 Least-Privilege Pipeline Execution and Registry Access Control

**The core vulnerability:** MLOps pipelines run with IAM roles or service accounts that are often over-privileged — granted write access to the production model registry or deployment infrastructure to make automation convenient. A compromised pipeline stage with these permissions can deploy arbitrary model artifacts to production.

### Check

- Does the training job's service account have write access to the production model registry — or is production write access restricted to a separate promotion step with human approval?
- Is there a staging registry separated from the production registry — with no automated pathway that moves artifacts from staging to production without a gated review?
- Are IAM policies for each pipeline stage scoped to the minimum required: training jobs can write to experiment storage; evaluation jobs can read from experiment storage; only the promotion workflow can write to the production registry?

### Action

- **Separate staging and production registries.** Training and evaluation write to a staging registry. A separate promotion workflow — triggered manually or after explicit approval — moves artifacts to production after re-verifying checksums and evaluation criteria.
- **Apply least-privilege IAM per pipeline stage:**

```yaml
# Example AWS IAM for training stage
training_job_policy:
  - Effect: Allow
    Action: ["s3:PutObject", "s3:GetObject"]
    Resource: "arn:aws:s3:::ml-staging-artifacts/*"
  - Effect: Deny
    Action: "*"
    Resource: "arn:aws:s3:::ml-production-registry/*"
```

- **Require a human approval gate before production promotion.** In GitHub Actions, use `environment: production` with required reviewers. In Kubeflow or SageMaker Pipelines, add a manual approval step as an explicit pipeline node.

### Minimum Deliverable Per Review

- [ ] Artifact checksum verification: implemented at each stage transition and in CI
- [ ] Code version pinning: all pipeline definitions reference commit hashes, not branch names
- [ ] Lineage log: run ID, data version, code commit, environment digest, output artifact hash
- [ ] IAM audit: training/evaluation service accounts scoped to staging only
- [ ] Staging/production registry separation: confirmed with no automated cross-registry write path
- [ ] Promotion gate: human approval required before production deployment

## Quick Win

**Add SHA-256 checksum verification to your model promotion workflow.** Before deploying a model to production, recompute the checksum of the artifact from the staging registry and compare it against the hash recorded at evaluation time. This single check prevents artifact substitution between evaluation and deployment — the most impactful integrity attack in MLOps pipelines.

## References

- Model artifact signing and provenance → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- Container security for ML workloads → [container-ai-workload-security/SKILL.md](../container-ai-workload-security/SKILL.md)
- Governance and change management → [ai-governance-and-incident-response/SKILL.md](../ai-governance-and-incident-response/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
