---
name: code-review
description: Perform and apply code reviews (UACRP + application protocol) and coordinate artifacts via mpcr.
compatibility: Requires a POSIX shell. If `<skills-file-root>/scripts/mpcr` is not prebuilt, requires a Rust toolchain (`cargo`/`rustc`) to build `<skills-file-root>/scripts/mpcr-src`.
---

# Code Review

This skill bundles two distinct workflows:

- **Reviewer**: perform an adversarial code review using UACRP and produce a review report
- **Applicator**: apply feedback from completed review reports and track dispositions/progress

Both workflows can use the bundled `mpcr` CLI at `<skills-file-root>/scripts/mpcr` to coordinate session artifacts under `.local/reports/code_reviews/YYYY-MM-DD/`.

## Choose the correct workflow (mandatory)

- IF you are asked to **review a change** (diff/PR/patch) THEN you are the **Reviewer** → read `<skills-file-root>/references/perform-overview.md`.
- IF you are asked to **apply findings** from an existing review report THEN you are the **Applicator** → read `<skills-file-root>/references/apply-overview.md`.
- IF the request includes *both* reviewing and applying THEN ask whether you should run them as two phases; default order: **Reviewer → Applicator**.
- IF unclear THEN ask a targeted clarification question and wait.

## Progressive disclosure and chunking (mandatory)

Before doing any work in either workflow:

- You SHALL read the relevant overview file (chosen above).
- IF you need to ingest it in parts THEN you SHALL read it in **<= 500-line chunks**.
- The overview will direct you to additional reference files; apply the same chunking rule.
- IF you have already ingested the relevant overview/protocol earlier in this conversation THEN you SHALL NOT re-ingest them; proceed with the workflow.
