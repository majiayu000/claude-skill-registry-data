---
name: publish-blog
description: Publish a markdown document on greengale.app when the material needs more space than a Bluesky post. Public policy checks factual integrity, privacy and interaction norms. For a short public reply use post; for a URL as public memory save it via the semble tools, for a standalone public note write a network.cosmik.card via pdsx (the cosmik-records skill has the routing); for private notes to your future self use the save_memory tool.
---

## writing

Use the current public etiquette for the composed document. Choose the subject
from the occasion and your interests. Link the source conversation when it
prompted the piece. Preserve attribution and the
difference between what happened, what you inferred, and what remains untested.
Optionally use `humanizer` to review the draft's phrasing. Preserve
the claims, sources, and qualifications while choosing your own revisions.

## procedure

before publishing:

1. call `list_blog_posts` (or `pub_search(author="phi.zzstoatzz.io", platform="greengale")`) to scan your existing post titles. **the `publish_blog_post` tool refuses on exact-title duplicates** — failing the publish is a worse outcome than picking a different title up front.
2. verify any AT-URI you plan to cite via `pdsx.get_record` first. broken rkeys in blog posts are harder to retract than in tweets.

publishing:

3. call `publish_blog_post(title, content, tags)`. it validates the record shape, refuses on duplicate title, writes to your PDS as `app.greengale.document`, and returns the public URL.

**escape dollar signs: write `\$`.** greengale renders every post with KaTeX, always on, and a single `$...$` pair is inline math. two dollar amounts in one paragraph turn everything between them into an italic formula with the spaces stripped (the 2026-09-19 chicken ledger post did this three times). a cell with one `$` survives; prose with two does not. `\$935.87` renders as `$935.87`.

after publishing:

4. call `save_memory(content="published blog: <title> — <url>", tags=["blog", "greengale", ...topic_tags])` to leave a private-memory pointer for future-you. the publish tool does this for you automatically, but if you want to add additional context (e.g. a synthesized takeaway you don't want to lose), use `save_memory` again.

## tags

specific topic words, not meta-categories (`atproto` ✓, `thoughts` ✗). 3–6 tags is plenty.

## why a tool plus a skill

`publish_blog_post` is structural — it enforces the duplicate-title refusal and writes the post-publish episodic memory. this skill covers publishing procedure and source checks; public etiquette owns the delivery form.


## correcting an existing article

Read the current document and CID (list_blog_posts includes its URI and CID).
Call publish_blog_post with the full revised title and content, uri, and
expected_cid. This replaces the existing article at the same URL, preserving
publication metadata and existing tags unless you supply tags. Make corrections
explicit in the article. If a newer revision exists, reread it before editing;
do not substitute a newer CID without reviewing its content. The complete
replacement passes the public policy check. Raw PDS updates remain guarded.
After success, save a private correction note with the article URL and what changed.
