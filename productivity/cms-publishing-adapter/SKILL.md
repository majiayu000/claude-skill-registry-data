---
name: cms-publishing-adapter
description: Turn QA-approved content into a CMS draft, document, static-site file or manual handoff package, with permission checks, validation and readback. Use for "publish this to WordPress", "create a Webflow draft", "add this post to my blog repo", "prepare this for my CMS", "format this for Ghost".
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/cms-publishing-adapter
---

# CMS publishing adapter

Turn approved SEO content into a CMS draft, document, static-site file, or manual publishing package, with validation, permission checks, and readback. Use it only after content passes QA. This is an adapter skill. It does not choose topics, write strategy, rewrite content for preference, or publish externally without permission/configuration. It hands back what was created, updated or packaged, where, in what state, and what the readback confirmed.

> **Romeo's rule:** A "success" response from a CMS API is a rumour until you have read the item back.

## Use this when

- Content has passed QA and needs to become a CMS draft, document, static-site file, or manual publishing package.
- An existing CMS item needs updating without touching fields outside the change.
- You want a draft created in a CMS or Git repo and verified by reading it back.
- No CMS is connected and someone needs a complete package they can paste in by hand.

## Don't use this for

- Content that hasn't passed QA yet → `seo-content-qa`.
- Writing or rewriting the content → `seo-blog-writer`.
- Writing or fixing structured data → `schema-markup`.
- Changing URLs or slugs at scale, or planning redirects → `site-migration-check`.

## What you need

### Required

- Approved content.
- QA verdict and residual risks.
- Target publishing destination.
- Destination permissions: package-only, create draft, update draft, publish, deploy.
- Required fields and content model.
- Slug, title, meta description, category/tags, author, date, status.
- Media assets and alt text.
- Schema/custom-code requirements.
- Canonical and locale rules.

### Helpful

- Existing CMS item ID or URL.
- Draft/published readback.
- Asset storage access (CMS media library, object storage).
- Static-site repo path.
- Approval workflow/task id.
- Preview/deploy access.

### No tools?

Without API or repo access, produce the manual handoff package (below) plus a publishing checklist the user follows in their CMS editor. Ask for the content model; a screenshot of the CMS post editor's fields is enough. After the user saves the draft, ask for the preview URL or a screenshot and do the readback yourself: view-source for the title, meta description, canonical, robots meta and JSON-LD; check that headings, tables, images and FAQs rendered rather than showing raw Markdown or escaped HTML. Validate JSON-LD locally where possible. Google's Rich Results Test sends the supplied URL or code to Google: use it for unpublished content only after explaining the transfer and getting the user's permission, or leave that check for the user.

## Ground rules

- Keep core content provider-neutral.
- Preserve draft/published state unless explicitly instructed.
- Never publish live without explicit permission or preconfigured automation policy.
- Do not silently drop unsupported markup, schema, links, or images.
- Always read back when the destination supports it.
- Treat CMS field mappings, locale quirks, auth, and API bugs as adapter configuration (notes about the destination), not as content changes.

## Supported destinations

Examples:

- Framer CMS.
- Webflow CMS.
- WordPress.
- Sanity.
- Contentful.
- Ghost.
- Shopify blog.
- HubSpot CMS.
- Notion or Google Docs draft.
- GitHub/MDX/static-site repo.
- Plain Markdown/HTML handoff package.

## Steps

1. **Confirm permission and target.**
   - Determine whether the adapter may create, update, publish, deploy, or only package.
   - If permission is missing, produce a manual handoff package.
   - If updating existing content, fetch/read the current item first and preserve fields not in scope.

2. **Load destination schema.**
   - Required fields.
   - Field IDs/names.
   - Rich text format: HTML, Markdown, block JSON, portable text, MDX, plain text.
   - Media handling.
   - Slug/canonical behavior.
   - Locale/localization behavior.
   - Draft/publish states.
   - Custom code/schema support.

3. **Transform content.**
   - Convert rich text to the destination format.
   - Preserve headings, links, tables, images, alt text, FAQs, and schema.
   - Strip unsupported markup only with a warning.
   - Keep page metadata separate from body content.
   - Keep schema separate or embedded based on destination support.

4. **Validate before write.**
   - Required fields present.
   - Slug valid and not colliding unless update is intended.
   - Canonical valid.
   - Links present and not obvious placeholders.
   - Images uploaded or mapped.
   - Alt text present.
   - Schema matches visible content.
   - Draft/publish status matches permission.
   - Existing ranked page title/meta/slug changes are not happening unless explicitly approved.

5. **Upload/store assets.**
   - Reuse existing approved assets where possible.
   - Upload to CMS media library, object storage, or configured destination.
   - Record public URLs, asset IDs, mime types, dimensions, and alt text.
   - If asset upload fails, stop or package with clear manual follow-up depending on policy.

6. **Create/update/package.**
   - Create new draft when allowed.
   - Update existing item only for in-scope fields.
   - Preserve existing draft status by default.
   - For static-site repos, prepare file changes but follow repo/publishing policy separately.
   - For document destinations, preserve headings, links, tables, images, and schema handoff notes.

7. **Read back and verify.**
   - Fetch the created/updated item.
   - Confirm title, slug, meta, body, images, schema, category/tags, status.
   - Confirm no raw Markdown is showing in HTML-only fields and no HTML is escaped in rich-text fields.
   - Confirm visible FAQ matches FAQ schema when available.
   - Confirm image URLs render or at least are reachable through adapter readback.

8. **Return publishing result.**
   - Use the format in What to hand back.

## Manual handoff package

If no CMS/API is connected, return:

- body content in requested format
- title
- slug
- meta description
- category/tags
- author/date
- schema JSON-LD
- image files/URLs with alt text
- internal/external link list
- publishing checklist

## What to hand back

Fill in this template. If you produced a manual handoff package instead of writing to a destination, say so in the first line and attach the package after the template.

```markdown
**What I found:** <what was created, updated or packaged, and where>
**What matters most:** <readback result or the biggest residual risk>
**What to do first:** <e.g. review the draft at the preview URL, then publish it yourself>

## Publishing result
- Destination and action performed: <e.g. WordPress, created draft / package only>
- Item / document / file ID: <...>
- Draft / published status: <...>
- URL or preview URL: <...>

## Field mapping used
- <content field> → <destination field>

## Asset mapping
- <file> → <public URL or asset ID> | mime type | dimensions | alt text

## Schema placement
- <embedded in body / custom-code field / head injection / handoff only>

## Readback validation
- Title, slug, meta, body, images, schema, category/tags, status: <match / mismatch, with details>
- Raw Markdown in HTML-only fields or escaped HTML in rich text: <none / found where>
- Visible FAQ matches FAQ schema: <yes / no / n/a>
- Image URLs render or are reachable: <yes / no>

## Preserved fields
- <fields left untouched on update>

## Manual follow-ups
- <...>

## Residual risks
- <...>

## What I could not check
- <e.g. no readback: destination has no read API>
```

## Stop and flag if

Fail or stop for human approval if:

- Publishing permission is unclear.
- Destination schema is unknown and cannot be inferred.
- Required fields are missing.
- Asset upload fails for required images and policy requires complete drafts.
- Existing ranked title/meta/slug would be changed without approval.
- Readback contradicts intended content.
- CMS API reports success but required content is missing.
- Draft status would be changed unintentionally.

## Next step

- Once the page is live, run `seo-change-monitor` on its URL to snapshot title, canonical, indexability and schema for later comparison.
- Run `site-content-inventory` to add or update the page's record and status, then `internal-linking-plan` to link to it from related pages.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
