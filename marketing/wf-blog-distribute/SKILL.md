---
name: wf-blog-distribute
version: 1.0.0
description: "Write a blog post and distribute it across channels. Use when the user wants to write a blog post AND get it out on social, email, or other channels. Also trigger when the user mentions 'blog and distribute,' 'write and promote,' 'blog to social,' 'publish and share,' 'full blog workflow,' or 'blog pipeline.' For writing a blog post only, see blog. For social-only, see social-content."
---

# Blog → Distribute

End-to-end workflow: draft a blog post, clean it up, optimize for search, then push it across social and email channels.

## Stage 1: Draft the Blog Post

Load and run the `blog` skill for the full drafting workflow (brief intake, outline, draft, approval).

**Gate:** Do not proceed until the user approves the final draft.

## Stage 2: Quality Pass

Load and run the `tagore` skill on the approved draft. Fix any AI patterns or voice problems it flags.

**Gate:** Show the user the Tagore score and any remaining items. Get approval before proceeding.

## Stage 3: SEO Optimization

Load and run the `seo-geo` skill to optimize the post:
- Page title, meta description, slug
- Heading structure and keyword placement
- Internal linking opportunities
- AI engine optimization (GEO)

**Gate:** Show the user the SEO recommendations. Apply approved changes.

## Stage 4: Social Distribution

Load and run the `social-content` skill. Using the approved blog post as source material, generate:
- 1-2 LinkedIn posts (different angles)
- 1-2 Twitter/X posts
- Any other platforms the user specifies

Pass forward: the blog title, key takeaways, target audience, and any compelling quotes or stats from the post.

**Gate:** User approves or edits the social posts.

## Stage 5: Email Integration (Optional)

Ask: "Want to add this to an email sequence or send a standalone email about it?"

If yes, load and run the `email-sequence` skill to:
- Draft a newsletter mention or standalone email
- Suggest where in an existing nurture sequence this content fits

If no, skip to the summary.

## Summary

Present a checklist of everything produced:

```
## Blog → Distribute Complete

### Blog Post
- [title] — [path to file]

### SEO
- Title tag: [title]
- Meta description: [description]
- Target keyword: [keyword]

### Social Posts
- LinkedIn: [count] posts → [paths]
- Twitter/X: [count] posts → [paths]

### Email
- [what was created, or "Skipped"]

### Next Steps
- [ ] Publish the blog post
- [ ] Schedule social posts
- [ ] Queue email
```

## Output Structure

All files go into a single project folder:

```
marketing/blog/[post-slug]/
  blog-post.md
  social-linkedin-1.md
  social-linkedin-2.md
  social-twitter-1.md
  email-announcement.md        (if email stage run)
  email-nurture-insert.md      (if email stage run)
  seo-metadata.md
```

Derive `[post-slug]` from the blog title. Confirm with the user before creating files.

## Rules

- Each stage uses the full component skill, not a shortcut version
- Always gate between stages — never auto-advance without user approval
- Carry context forward: audience, key messages, tone, and stats flow from stage to stage
- If the user wants to skip a stage, skip it cleanly
- All output goes into the project folder, not scattered across `marketing/`
