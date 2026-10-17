---
name: trm-feedback-report
description: Post-ingest-batch feedback pass for TRM — classifier/extraction quality, OCR latency vs. budget, candidate new-topic surfacing, and a web-search cross-check on low-confidence facts.
compatibility: |
  - Runtime: Node.js 18+, trm CLI on PATH
  - Dependencies: (see package.json)
---

# TRM Feedback/Report

Standing feedback pass for a TRM ingest batch. Run after `trm ingest-dir` completes.

## Trigger

After any TRM ingest batch, or on request ("feedback on the last ingest batch", "report on <topic>").

## Flow

1. Run `runTrmCommand(trmRoot, ['validate', topicPath, '--recursive'])` and `runTrmCommand(trmRoot, ['feedback-stats', topicPath, '--recursive', '--latency-budget-ms', String(latencyBudgetMs)])`. Parse both as JSON.
2. Read `extracts/extract.json` facts for the topic (recursively, matching `--recursive`) and call `findNewTopicCandidates(facts, existingTagsAndPathSegments)`, where `existingTagsAndPathSegments` is collected by walking `topic.json` from the vault root.
3. Select facts with `confidence < 0.55` OR `flags?.includes('VERIFY')`, capped at the top 10 by `score.json`'s `promotion_score`. For each, call the `WebSearch` tool, classify each hit's consistency with the fact's claim, then call `deriveSignalStrength(hits)`.
4. Write the narrative report: classifier accuracy verdict, extraction gaps (using `fact_density`/`over_budget`/`warnings_count_by_type`), three required risk labels (extraction risk / classifier drift risk / latency risk, each low/medium/high), new-topic candidates from step 2, cross-check results from step 3. Call `buildReportMeta(stats.completeness, hardFailure, webSearchSkipped)` for the `partial_report`/`latency_data_stale` flags and `reportFilename(topicPath)` for the filename.
5. Write the file to `<trmRoot>/reports/<filename>`.
6. Call `runTrmCommand(trmRoot, ['crosslink', topicPath, '--tags', 'trm-feedback-report:v1'])`.

## Input Schema

```typescript
interface Input {
  topicPath: string;
  trmRoot: string;
  recursive?: boolean;
  latencyBudgetMs?: number;
}
```

## Output Schema

```typescript
interface Output {
  reportPath: string;
  partial_report: boolean;
  latency_data_stale: boolean;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).

**For detailed workflow:** See [docs/USAGE.md](docs/USAGE.md).
