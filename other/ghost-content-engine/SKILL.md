---
name: ghost-content-engine
description: Build and operate a self-hosted Ghost content engine that turns YouTube videos, meeting notes, community wins, quote banks, Neo4j graph context, and Reddit exact-question FAQs into SEO/AEO-friendly Ghost blog posts.
metadata:
  short-description: Ghost blog content engine
---

# Ghost Content Engine

Use this skill when the user wants to create, enrich, publish, or maintain blog posts for a self-hosted Ghost site using the Ghost Content Engine Kit.

## Workflow

1. Read `.env.example` and confirm `.env` has `GHOST_URL`, `GHOST_ADMIN_API_KEY`, `SITE_NAME`, and `SITE_AUTHOR_NAME`.
2. For Ghost publishing, use `scripts/ghost_client.py`.
3. For YouTube videos, use `scripts/youtube_blog_pipeline.py`.
4. For Reddit FAQ market language, use `scripts/reddit_question_mining.py`.
5. For internal graph enrichment, use `scripts/neo4j_question_mining.py`.
6. For combined FAQ enrichment, use `scripts/faq_enrichment_pipeline.py`.
7. For community wins, case studies, masterclasses, newsletters, or quote banks, use `scripts/community_blog_pipeline.py`.
8. For LinkedIn repurposing from a Ghost post, use `scripts/ghost_to_linkedin.py` or `scripts/linkedin_post_pipeline.py`.

## Guardrails

- Never hardcode API keys.
- Use `--dry-run` before live Apify runs.
- Keep Reddit question wording exact, but answer in the site owner's voice.
- Keep private community names and links redacted unless permission is explicit.
- Publish through Ghost HTML cards with `--html-card` so custom classes survive.
- Keep important content visible in HTML; do not hide essential content behind JavaScript.
- Use clean evergreen slugs.
- LinkedIn publishing must use official OAuth/API credentials and must not use cookies or browser automation.
- Use `--review-only` or `--dry-run` before `--publish-now` unless the user explicitly asked for live posting.

## Common Commands

```bash
python scripts/ghost_client.py list-posts --limit 5
python scripts/youtube_blog_pipeline.py from-url --url "https://www.youtube.com/watch?v=VIDEO_ID" --faq-dry-run
python scripts/reddit_question_mining.py research --topic "AI agency first client" --slug ai-agency-first-client --dry-run
python scripts/neo4j_question_mining.py research --topic "AI agency first client" --slug ai-agency-first-client --max-nodes 500
python scripts/community_blog_pipeline.py from-file --source-file examples/community-win-source.md --title "How A Simple Website Offer Became A First-Client Win" --slug simple-website-offer-first-client-win --content-type win --redact "Member Name"
python scripts/ghost_to_linkedin.py --slug ai-agency-first-client --review-only
python scripts/ghost_to_linkedin.py --slug ai-agency-first-client --publish-now
```

## References

Read the repo docs only when needed:

- `docs/setup.md`
- `docs/youtube-repurposing.md`
- `docs/reddit-faq-enrichment.md`
- `docs/neo4j-content-memory.md`
- `docs/community-content-pipeline.md`
- `docs/publishing-checklist.md`
- `linkedin-setup/README.md`
- `linkedin-setup/cli-workflow.md`
