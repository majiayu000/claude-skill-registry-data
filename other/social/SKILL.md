---
name: social
description: "MythiStone automated social posts: post selection, facts and hooks, LLM drafting and judging, and the social image renderers. Use when editing generateSocialsPost.py, social_posts/, image_generation/ or automatedSocialMediaPosts.yml."
---

# Social domain

## Gotchas

Before changing a file listed below, read its gotcha: `ref/<id>.md` in this skill (or `kb_gotcha <id>`).

| id | rule | files |
|---|---|---|
| `social-image-mock-harness` | How to verify the social image renderers in backend_scripts/image_generation/ locally against the seeded local test DB | `backend_scripts/image_generation/*` |
| `social-post-pipeline` | What the daily social post depends on outside social_posts/ (its records on the social-images branch, the blog generator's post-type tables, chart labels) and how to test it offline | `backend_scripts/generateSocialsPost.py`, `backend_scripts/social_posts/*`, `.github/workflows/automatedSocialMediaPosts.yml` |
