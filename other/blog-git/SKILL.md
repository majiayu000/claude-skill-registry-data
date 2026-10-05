---
name: blog-git
description: "Writing and publishing blog posts as markdown with front matter into a git-backed static site (Hugo, Jekyll, Astro, etc.), then committing and pushing so CI deploys it."
metadata:
  {
    "marketingclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["git"], "env": ["BLOG_REPO_PATH"] },
        "primaryEnv": "BLOG_REPO_PATH",
      },
  }
---

# Blog-Git Skill

Instructions-only skill: write a markdown post with front matter into the local clone of a
static-site blog repo, commit it, and push. CI on the remote (Netlify/Vercel/GitHub
Pages/Cloudflare Pages, etc.) picks up the push and deploys — this skill never talks to a
hosting API directly.

## Approval-first rule

**Draft the post and show the full markdown (including front matter) to the human before
committing.** Only `git add`/`git commit`/`git push` after explicit approval. Never push directly
to a protected branch that skips review if the repo's normal workflow uses pull requests — check
`git log` / branch protections and open a PR instead when that's how the repo works.

## Setup

1. Clone the blog's repo locally (or note the path if already cloned).
2. Set the environment variable:
   ```bash
   export BLOG_REPO_PATH="/path/to/local/clone/of/blog-repo"
   ```
3. Confirm push access: `git -C "$BLOG_REPO_PATH" remote -v` and that your git credentials
   (SSH key or credential helper) can push to it.
4. Identify the static-site generator (Hugo/Jekyll/Astro/other) so you use the right front-matter
   shape — see `references/frontmatter-templates.md`.

## Workflow

```bash
# 1. Make sure the local clone is current
git -C "$BLOG_REPO_PATH" pull --ff-only

# 2. Write the post. Pick the path convention the repo already uses, e.g.:
#    Hugo:    content/posts/2026-07-15-my-post-slug.md
#    Jekyll:  _posts/2026-07-15-my-post-slug.md
#    Astro:   src/content/blog/my-post-slug.md
#    (grep existing files in the repo for the actual convention before guessing)
```

Write the file with the Write/Edit tool at the resolved path, using a template from
`references/frontmatter-templates.md` as the front-matter shape. Show the complete file content
to the human for approval before committing.

```bash
# 3. After approval — commit and push
git -C "$BLOG_REPO_PATH" add "content/posts/2026-07-15-my-post-slug.md"
git -C "$BLOG_REPO_PATH" commit -m "Add post: My Post Slug"
git -C "$BLOG_REPO_PATH" push
```

If the repo uses a PR-based workflow instead of pushing straight to the deploy branch:

```bash
git -C "$BLOG_REPO_PATH" checkout -b post/my-post-slug
git -C "$BLOG_REPO_PATH" add "content/posts/2026-07-15-my-post-slug.md"
git -C "$BLOG_REPO_PATH" commit -m "Add post: My Post Slug"
git -C "$BLOG_REPO_PATH" push -u origin post/my-post-slug
gh pr create --repo <owner>/<repo> --title "Add post: My Post Slug" --body "New blog post, ready for CI preview."
```

## Front matter

See `references/frontmatter-templates.md` for ready-to-fill Hugo, Jekyll, and Astro examples
(title, date, slug/permalink, description, tags, draft flag, cover image).

## Notes

- Never `git push --force` on a shared branch; if history has diverged, pull/rebase and resolve
  conflicts, or ask the human.
- Respect the repo's existing `draft: true`/`published: false` convention if it uses staged
  previews before going live — set the draft flag, push, let the human flip it live.
- Image assets: check where the repo stores post images (commonly `static/`, `assets/`, or
  co-located with the post) and follow that convention rather than inventing a new path.
- This skill has no API credentials of its own — it only needs local git access to
  `$BLOG_REPO_PATH`.
