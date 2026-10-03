---
name: kvs-benchmark-operator
description: Operate and monitor this repository's AWS DynamoDB, ADB DynamoDB API, and OCI NoSQL benchmarks through the existing dashboard pipeline. Use for benchmark launch, live status, evidence summaries, failure diagnosis, or authorized post-run cleanup; do not use for unrelated cloud provisioning.
---

# KVS benchmark operator

This Claude Code project skill uses the repository-owned workflow shared with Codex. Read and follow [the canonical operator instructions](../../../.codex/skills/kvs-benchmark-operator/SKILL.md).

Run the portable status helper from the repository root:

```text
node .codex/skills/kvs-benchmark-operator/scripts/snapshot.mjs
```

Do not infer permission to launch, retry, stop, clean up, resize, or delete resources from a status request. Keep private credential profile names and runtime secrets out of reusable output and commits.
