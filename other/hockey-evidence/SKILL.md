---
name: hockey-evidence
description: Use when researching ice hockey science, auditing the Garmin Hockey app, or designing traceable algorithms from wearable data.
---

# Hockey Evidence

Use this skill as a versioned, citation-first evidence base for the Garmin Hockey app. Route requests to one of four modes:

- **update**: explicitly search PubMed, Crossref, and OpenAlex; log queries, failures, and provenance. Never silently overwrite prior records.
- **literature review**: summarize records with their review status, methods, findings, limitations, and source links.
- **app audit**: compare app claims, metrics, or code with the corpus and classify each as `gestützt`, `nur indirekt gestützt`, or `nicht ausreichend belegt`.
- **algorithm design**: separate literature finding, transfer assumption, app model, free parameters, and validation plan.

For algorithm design, use `scripts/design_algorithm.py::render_algorithm_proposal`. Every output is experimental until
criterion-measure validation is completed; the renderer must retain study IDs, quality gates, free parameters, and
predefined error metrics. `run_skill_smoke_suite` provides a deterministic end-to-end acceptance check.

For distance-per-push, anthropometry, height, weight/BMI, or skating-distance requests, first read
[profile-distance](references/profile-distance.md), then [algorithm-design](references/algorithm-design.md)
to render the proposal. Keep the fixed release baseline and the bounded height-only experiment distinct;
the distance reference supplies the evidence limits and activation gate.

Evidence priority is ice hockey, then inline hockey and long-track speed skating, then other gliding sports, and only justified indirect evidence from other intermittent team sports. Field hockey is not treated as equivalent merely because it is hockey.

Do not copy copyrighted full text, infer missing study fields, provide diagnoses, or present unvalidated production weights as established science. Abstract-only and bibliographic-only records must retain their restricted status. Distinguish findings from transfer assumptions and ShiftSense/Garmin model choices.

The structured study contract uses: `identifiers`, `bibliography`, `sport_context`, `methods`, `findings`, `limitations`, `review_status`, `transferability`, and `provenance`. Detailed rules live in the reference files. Updates are user-authorized and reproducible; incomplete source runs remain marked incomplete.
