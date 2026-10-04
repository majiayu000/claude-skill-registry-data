---
name: preview-publish-live-audit
description: Produce a clean publishing payload, validate it, publish once when authorized, and verify the rendered result.
---

# Preview, Publish, and Live Audit

## Preview

Render the final article and build a CMS payload containing the expected slug, title, clean description, body, cover, category, and author. Validate that no private syntax, placeholder, unsupported component, or wrong field reaches metadata or body.

## Publish

Publish only in `quality_gated_live` mode after the candidate, research, proof, visuals, quality gate, preview, and dry run all pass. Publish no more than once per run.

## Live audit

Verify directly after publication:

- HTTP 200 and canonical URL;
- expected H1, title, clean meta description, named byline, and author profile;
- cover/OG and all in-article images load;
- citations, internal links, and CTA resolve;
- desktop and mobile first view are usable;
- no markers, private notes, unsupported components, or implementation terms are visible.

Any mismatch is `PUBLISH_FAILED`, not success. Record the exact corrective action and stop.

