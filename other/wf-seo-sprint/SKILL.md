---
name: wf-seo-sprint
version: 1.0.0
description: "Run an SEO audit and execute a batch of optimized content. Use when the user wants to improve search rankings through a coordinated content push. Also trigger when the user mentions 'SEO sprint,' 'SEO content batch,' 'content for SEO,' 'topic cluster build,' 'rank for keywords,' 'SEO blitz,' or 'search content strategy.' For a single blog post, see blog. For an SEO audit only, see seo-geo."
---

# SEO Sprint

End-to-end workflow: audit current SEO state, plan a topic cluster, write a batch of optimized posts, and add structured data.

## Stage 1: SEO Audit

Load and run the `seo-geo` skill in audit mode:
- Current ranking positions (if data available)
- Content gaps and keyword opportunities
- Technical SEO issues
- Competitor content analysis
- AI engine visibility (GEO audit)

Deliver a prioritized list of opportunities.

**Gate:** User reviews the audit and selects which opportunities to pursue.

## Stage 2: Content Planning

Load and run the `content-strategy` skill to build:
- Topic cluster around the selected opportunities
- Pillar page + supporting posts structure
- Target keyword for each piece
- Internal linking plan between pieces
- Publishing order (which posts support which)

**Gate:** User approves the content plan and prioritizes which posts to write in this sprint.

## Stage 3: Write the Posts

For each post in the approved plan, load and run the `blog` skill:
- Full drafting workflow per post (brief, outline, draft, approval)
- SEO optimization baked into each post (target keyword, headings, meta)
- Run `tagore` on each approved draft

Track progress across the batch. After each post is approved, move to the next.

**Gate:** User approves each post individually. Can stop the sprint at any point.

## Stage 4: Structured Data

Load and run the `schema-markup` skill to add:
- Article schema for each post
- FAQ schema where applicable
- Breadcrumb schema
- Any other relevant schema types

Apply to all posts in the sprint.

**Gate:** User approves the schema additions.

## Summary

```
## SEO Sprint Complete

### Audit
- Opportunities identified: [count]
- Opportunities pursued: [count]

### Content Plan
- Topic cluster: [pillar topic]
- Pillar page: [title] → [path]

### Posts Written
1. [title] — target: [keyword] → [path]
2. [title] — target: [keyword] → [path]
3. [title] — target: [keyword] → [path]
...

### Schema Added
- [types] applied to [count] posts

### Internal Linking
- [description of linking structure]

### Next Steps
- [ ] Publish posts in recommended order
- [ ] Submit sitemap update
- [ ] Set up rank tracking for target keywords
- [ ] Plan next sprint for remaining opportunities
- [ ] Distribute posts (run /repurpose on each)
```

## Output Structure

All files go into a single project folder:

```
marketing/seo-sprints/[topic-slug]/
  audit.md
  content-plan.md
  post-1-[slug].md
  post-2-[slug].md
  post-3-[slug].md
  schema.json
  internal-linking-plan.md
```

Derive `[topic-slug]` from the pillar topic. Individual post files include their own slug. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill
- Always gate between stages and between individual posts
- The user controls how many posts to write in a single sprint — don't push for more
- SEO optimization happens during writing, not as a separate pass
- All content must still meet brain file accuracy standards
- All output goes into the project folder, not scattered across `marketing/`
