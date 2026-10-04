---
name: dataset-supply-chain-security
description: Review upstream dataset integrity controls, HuggingFace repository risks, dataset versioning, dependency pinning, and third-party dataset provenance to prevent malicious data from entering training or RAG pipelines.
last_reviewed: 2026-04-30
---

# Dataset Supply Chain Security

## First Principle

**A dataset is a dependency. Like code dependencies, datasets can be maliciously modified, quietly replaced, or typosquatted — and unlike code, you cannot grep a dataset for malicious content.**

When a model trains on a dataset pulled from a public hub, or a RAG pipeline indexes documents from an external source, the security of the ML system depends entirely on the integrity of that external data. Dataset supply chain attacks exploit the trust that ML practitioners place in "well-known" datasets and the absence of integrity verification in most ML toolchains.

## Attack Mental Model

1. **Dataset poisoning at the source** — an attacker with write access to a dataset repository modifies a dataset after it has been trusted and included in ML pipelines. Training pipelines that always pull `latest` ingest the modification silently.
2. **Typosquatting** — an attacker publishes a dataset with a name similar to a popular, trusted dataset (`openai/gpt-4-data` vs `openal/gpt-4-data`). Practitioners who mistype the name download the poisoned alternative.
3. **Dependency confusion** — a private dataset registry is configured to also check the public registry. An attacker publishes a public dataset with the same name as a private one. The public version is resolved first.
4. **Metadata manipulation** — a dataset's `README.md`, data card, or license file is modified to change the stated data composition, collection method, or provenance — misleading practitioners about what they are training on.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every external dataset is pinned by commit hash or content hash — not by tag or branch name. The hash is verified at download time before the dataset enters any pipeline. |
| **Scope** | Training pipelines pull from internal mirrors of approved datasets. Direct pulls from public hubs are blocked in production training environments. |
| **Isolate** | New or updated external datasets are staged in a quarantine environment and scanned before promotion to the approved dataset registry. |
| **Enforce** | Dataset ingestion events are logged with the source URL, resolved commit hash, download timestamp, and pipeline that consumed the dataset. |

## DSS.1 Dataset Pinning and Integrity Verification

**The core vulnerability:** ML toolchains that pull datasets by name without pinning a version can silently ingest modified or replaced datasets. A dataset that was safe when first audited may be malicious when next downloaded.

### Check

- Are all external datasets pinned to a specific commit hash or content hash — not a mutable tag, branch, or `latest` pointer?
- Is the pinned hash verified at download time before the dataset is passed to any processing step?
- Are datasets cached in an internal registry after first download, so subsequent pipeline runs do not pull from the external source?

### Action

- **Pin datasets by commit hash and verify at download:**

```python
import hashlib
from datasets import load_dataset

APPROVED_DATASETS = {
    "squad": {
        "repo": "rajpurkar/squad",
        "revision": "sha:abc123def456...",  # pinned commit hash
        "expected_content_hash": "sha256:...",  # hash of downloaded content
    }
}

def load_approved_dataset(name: str):
    spec = APPROVED_DATASETS[name]
    ds = load_dataset(spec["repo"], revision=spec["revision"])
    actual_hash = compute_dataset_hash(ds)
    if actual_hash != spec["expected_content_hash"]:
        raise DatasetIntegrityError(f"Content hash mismatch for {name}")
    return ds
```

- **Mirror approved datasets to an internal registry.** After integrity verification, store a copy in an access-controlled internal store. All training and RAG pipelines pull from the internal mirror, not from the public hub.
- **Log all dataset ingestion events.** Record source URL, commit hash, content hash, download timestamp, verifying principal, and consuming pipeline. This is the audit trail for incident response.

### Failure Modes

- A training pipeline pulls `load_dataset("popular/dataset")` without a revision pin. The dataset owner pushes a minor update that contains poisoned examples. The pipeline ingests it silently on the next training run.
- A typosquatted dataset (`popular-data` vs `popular_data`) is accidentally used in a RAG pipeline. The difference is not noticed because both datasets have similar document counts and the typosquatted version was crafted to produce realistic-looking outputs.

## DSS.2 Third-Party Dataset Vetting and HuggingFace-Specific Risks

**The core vulnerability:** HuggingFace and similar public hubs allow arbitrary users to publish datasets and model weights. The hub's reputation is borrowed by malicious publishers who rely on practitioners trusting "anything on HuggingFace."

### Check

- Is there a formal vetting process for adding a new external dataset to the approved registry? Who approves it, and what checks are required?
- Are HuggingFace datasets from unverified organizations or individuals treated with heightened scrutiny compared to verified organizations?
- Are dataset `parquet` or `arrow` files scanned for embedded code, malicious serialization payloads, or oversized fields before ingestion?

### Action

- **Define a dataset vetting checklist before any new external dataset is approved:**

```markdown
Dataset Vetting Checklist:
- [ ] Publisher identity: verified organization or individual with public track record
- [ ] License review: license permits intended use; no surprise restrictions
- [ ] Provenance documented: original data sources described and verifiable
- [ ] Content scan: no embedded executable code in parquet/arrow files
- [ ] Statistical review: label distributions, token frequencies, language composition match documentation
- [ ] Typosquatting check: intended dataset name matches intended repository exactly
- [ ] Dependency confusion check: dataset name does not conflict with any internal dataset name
- [ ] Content hash recorded for pinning
```

- **Scan dataset files for malicious serialization payloads.** Parquet and Arrow files can contain embedded Python objects that execute during deserialization. Use `safe_deserialize=True` options where available and scan for pickle-like patterns.

```python
import pyarrow.parquet as pq

def safe_load_parquet(path: str) -> pq.Table:
    # Verify no custom metadata contains executable content
    schema = pq.read_schema(path)
    for key, value in schema.metadata.items():
        if b"pickle" in value or b"__reduce__" in value:
            raise DatasetSecurityError(f"Suspicious metadata in {path}: {key}")
    return pq.read_table(path)
```

### Minimum Deliverable Per Review

- [ ] Dataset pinning: all external datasets pinned by commit or content hash; hash verified at download
- [ ] Internal mirror: approved datasets cached in internal registry; production pipelines pull from mirror only
- [ ] Vetting checklist: formal approval process for adding new external datasets
- [ ] Ingestion logging: source, hash, timestamp, consumer logged for every dataset pull
- [ ] Parquet/Arrow scanning: check for embedded executable content before ingestion
- [ ] Dependency confusion check: internal dataset names audited for public-hub collision risks

## Quick Win

**Pin every external dataset you currently use by commit hash today.** Find all `load_dataset()` or equivalent calls and add a `revision=` parameter pointing to a specific commit. This prevents silent updates from affecting training runs without your knowledge.

## References

- Training data poisoning → [training-data-poisoning/SKILL.md](../training-data-poisoning/SKILL.md)
- Model supply chain security → [model-supply-chain-security/SKILL.md](../model-supply-chain-security/SKILL.md)
- MLOps pipeline security → [mlops-pipeline-security/SKILL.md](../mlops-pipeline-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
