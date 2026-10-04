---
name: Curating backlinks for a post
description: Finds and recommends existing blog posts as internal backlinks for a post at the final draft stage. Use when a draft is nearly complete and needs internal links to related published content.
---

# Curating backlinks for a post

## Introduction

Backlinks are very important for a blog as it allows Houfu to continue to make use of work 
he has already done in news ways, inform readers of related content so that they can increase the
value of reading my blog, and apparently some SEO thing. 

## Process 

1. Read the post and its pitch to get a clear understanding of what the post is about and its structure.
2. Generate some search terms. 
3. Use the `ghost_search` MCP tool to search for relevant posts. Run multiple searches in parallel with different terms. When searching, always get a summary or excerpt of the post (use `ghost_post_get` with a slug if needed for more detail).
4. Aim for about 3 relevant posts. If necessary, limit the number of related posts to 5 posts. 
5. **Append `?ref={referring-post-slug}` to every internal backlink URL** (the slug of the post the link sits *in*, not the target). Example: a link inside `2026-predictions-six-month-update` becomes `https://www.alt-counsel.com/target-post/?ref=2026-predictions-six-month-update`. This lets Houfu attribute internal traffic to the referring post in Ghost analytics.
6. **Count the cost.** Each bookmark card plus surrounding adjustment costs ~30-50 words against the pitch's word budget. If the draft is already at or over budget, say so and propose which existing text the links replace.
7. **Never draft a lead-in sentence narrating the card** ("I've written before that..."). The card's title IS the callback. This is the highest-confidence rule in the mined edit corpus (docs/voice-edit-corpus-2026-08.md R2): 9 lead-ins drafted, 9 deleted by Houfu, zero exceptions. Place the standalone link line; let it speak.
8. Present your report to your human partner in the form of a table. For each related post, create a row with the columns, "Post title", "Relevance", "Link", and "Where to put this".

## Tips

* It may be necessary to search the blog again if your initiate search does not uncover enough results. However, give up after 10 searches even if there are not enough results.
* Try to distribute backlinks throughout the post. Don't crowd links in the "story so far" section of a post, if there is one. 
