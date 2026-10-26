---
name: document-review
description: Use when documentation may be stale, repeated, unsupported, or affected by an implementation change.
---

# Document Review

Read the project map/catalog and relevant OpenSpec change before creating or moving
an explanation. Identify audience, question and canonical owner. Keep observed
code behavior distinct from approved requirements; a mismatch may be a code defect.

Use the shared documentation impact/review services from the project tool map.
Choose an explicit Git base and a small set of documents. Catalogued review is
the default and includes their mapped code/tests/spec evidence. When organizing
uncatalogued files, first use `docs check --inventory`, then explicitly select returned
paths with `docs review --report --source inventory` (MCP `source="inventory"`). Do not
require catalog enrollment first. Uncatalogued files have no inferred evidence
mappings; state separately inspected code/spec evidence and uncertainty. Both
modes retain bounded bodies, hashes, citations and explicit omissions. Use the
document-organize skill when the outcome requires actual repository organization.
Do not fetch links or expand into private notes simply because they are mentioned.
To find a related passage, use `docs search` or `docs read` (MCP
`project_docs_search`, `project_docs_read`); declare files outside docs/ and
openspec/ explicitly, and report partial search coverage instead of absence.

For each actionable finding, cite exact target and supporting passages with path
and inclusive line numbers; state uncertainty and a concrete disposition. Compare
purpose as well as wording: consolidate competing reference explanations, retain
useful summaries/warnings and unique rationale. Similarity is a candidate signal,
not a deletion instruction. A title alone does not prove a distinct audience.

Return the service's review JSON: schema 1, packet_snapshot, reviewed/unreviewed
selected paths and findings. Each finding has category, target citation, supporting
citations, uncertainty, suggested_disposition and rationale. A citation has path,
start_line, end_line and exact quote. Allowed category values are exactly `contradiction`, `unsupported-claim`,
`obsolete-instruction`, `unnecessary-repetition`, `missing-explanation`,
`vague-prose`, and `useful-repetition`. The suggested_disposition value must be
exactly `revise`, `consolidate`, `retain`, or `investigate`; put explanation in
rationale, never in that enum field. Use `retain` for useful-repetition. Validate the
review against current sources. Validation proves grounding, not semantic truth.

Make consolidation as a reviewed Git edit and repair affected links. Record the
required impact dispositions after code/docs settle; changed source bytes invalidate
older evidence. Each decision binds its target's and mapped sources' content, not a
target commit: before merge, update from the target branch and record again only
the targets the gate reports stale. Keep omissions and
unresolved contradictions explicit. Consult the project documentation guide for
commands and schema details. Do not certify the whole knowledge base or update
review dates solely because checks pass.
