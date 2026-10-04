---
name: update-pipeline
description: Master orchestrator for the content update pipeline. Takes a published URL and produces an updated draft with side-by-side diff for editor review.
allowed-tools: Read, Write, Bash, Skill, Glob
---

# Update Pipeline (Master Orchestrator)

Take a URL of an existing article and produce an updated draft + a side-by-side diff. Chains every update skill in order, saving output at each stage.

## Invocation

```
/update-pipeline <url> [--context "free-form direction"]
```

Examples:
- `/update-pipeline https://mybrand.com/blog/keyword-research`
- `/update-pipeline https://mybrand.com/blog/link-building --context "Refresh stats only — don't restructure"`
- `/update-pipeline https://mybrand.com/blog/seo-basics --context "Add ProductB to the on-page section"`

## Process

1. **Parse the input.**
   - Extract the URL (everything before `--context` if present)
   - Extract the context string (everything after `--context`, if present)
2. **Slugify the URL.** Run `python scripts/slugify.py "<url>"` and capture the slug (uses last path segment).
3. **Capture context.** If context was provided, write it to `content-pipeline/0-context/{slug}.md`.
4. **Check pipeline status.** Run `python scripts/pipeline_status.py {slug} --update`. If any stages already exist:
   - **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: skip stages whose output files exist (resume-from-failure). Only overwrite if `--regenerate` was passed. No prompt.
   - **Interactive mode**: ask the user whether to skip-or-regenerate.
5. **Run the chain in order.** Wait for each stage's output file before advancing:
   1. `/extract-content <url>` → expects `content-pipeline/updates/1-extracted/{slug}.md`
   2. `/update-guidance {slug}` → expects `content-pipeline/updates/0-guidance/{slug}.md`
   3. **Read the guidance file** to determine which audits to run. Skip any audit marked "skip".
   4. `/update-claims {slug}` (if not skipped) → expects `content-pipeline/updates/2-update-claims/{slug}.md`
   5. `/update-product-mentions {slug}` (if not skipped) → expects `content-pipeline/updates/3-update-product-mentions/{slug}.md`
   6. `/update-topic-gaps {slug}` (if not skipped) → expects `content-pipeline/updates/4-update-topic-gaps/{slug}.md`
   7. `/update-draft {slug}` → expects `content-pipeline/updates/7-updated-draft/{slug}.md`
   8. `/update-preview {slug}` → expects `content-pipeline/updates/5-update-preview/{slug}.html`
6. **On any error,** stop and report which stage failed.
7. **On success,** report the slug, stages run, audits skipped (and why), and paths to the diff HTML and updated draft.

## Reporting format

```
✓ Update pipeline complete for "{url}" (slug: {slug})

Stages run:
  ✓ extract-content        → updates/1-extracted/{slug}.md
  ✓ update-guidance        → updates/0-guidance/{slug}.md
  ✓ update-claims          → updates/2-update-claims/{slug}.md
  - update-product-mentions → SKIPPED (no missing products per guidance)
  ✓ update-topic-gaps      → updates/4-update-topic-gaps/{slug}.md
  ✓ update-draft           → updates/7-updated-draft/{slug}.md
  ✓ update-preview         → updates/5-update-preview/{slug}.html

Next steps:
  1. Open updates/5-update-preview/{slug}.html in your browser to review changes
  2. Read updates/7-updated-draft/{slug}.md (specifically the "Editor's notes" section at the bottom)
  3. Apply final hand-edits, then run /format-for-publish to package as Strapi-ready markdown + JSON (and optionally direct-publish via Doppler)
```

## Skipping audits per guidance

The `update-guidance` skill scores each audit `high / medium / low / skip`. Audits marked `skip` are omitted from the chain. The orchestrator tells the user which were skipped and why.

This avoids generating empty / noisy audit files when the article doesn't need that audit.

## When the article doesn't need updating

If `update-guidance` scores all three audits `skip`:
- **Autonomous mode**: write a `content-pipeline/updates/no-update-needed-{slug}.txt` marker, log the slug as "still healthy", and exit cleanly. The auto-blog-loop reads the marker and moves to the next candidate without dispatching `update-draft`.
- **Interactive mode**: tell the user the article looks healthy; ask whether to proceed with `update-draft` anyway.

## Auto-publish vs editor-diff modes

The pipeline's terminus depends on mode:

- **Autonomous mode (`BLOG_AGENT_AUTONOMOUS=1`)**: after `/update-preview`, dispatch `/format-for-publish {slug} --auto-publish --update`. The `--update` flag tells `format_for_strapi.py` to PATCH the existing Strapi article by slug instead of POSTing a new one. The article goes live with the refreshed content. Then run `python scripts/auto_publish_check.py {slug}` to verify the public URL renders. On failure, quarantine to `content-pipeline/9-needs-review/{slug}.md`.
- **Interactive mode**: pipeline ends at the diff for editor review. The editor decides what to keep, edit, or reject. After their pass, run `/format-for-publish {slug}` to export the final version — but only after the human review step.
