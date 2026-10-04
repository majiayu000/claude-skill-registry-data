---
name: blog-publish
description: Use when a blog post is finished and ready to go live — validates, builds, verifies the post actually renders, then commits to develop. Trigger on "publish this post", "ship the post", "put the post live", after blog-write and blog-validate are clean.
---

# Publish a post

Order matters: verify the post survives the build **before** committing, because the
failure mode this pipeline guards against is a post that vanishes silently.

## 1. Validate

```bash
yarn validate data/blog/<year>/<slug>.mdx
```

Stop on any error. Do not proceed. See `blog-validate` for what each rule means.

## 2. Verify it renders

```bash
yarn build
```

**A green build does not mean the post is there.** MDX drops a malformed post silently and
the build still succeeds. Check the generated output directly:

```bash
node -e "const b=require('./.velite/blogs.json');
  const p=b.find(x=>x.slug.includes('<slug>'));
  console.log(p ? 'OK '+p.slug+' ('+p.body.length+' chars)' : 'MISSING')"
```

A post that validated clean but shows `MISSING`, or whose body length is far shorter than
the source file, was truncated by a parse error. Go back to `blog-validate`.

Then confirm visually with `yarn dev`:

- The post appears in the listing on the homepage.
- The body renders in full — scroll to the end, not just the title.
- Reference links resolve.

### If the build fails on dependencies

A mixed npm/yarn `node_modules` tree causes module-resolution errors that look like code
bugs. This repo commits both `yarn.lock` and `package-lock.json`, and **yarn is the one in
use** (`.yarnrc.yml` pins yarn 3.6.1). Rebuild the tree from `yarn.lock`:

```bash
rm -rf node_modules && yarn install --immutable
```

Plain `yarn install` will report success without fixing it — it does not prune packages it
did not create. Never run `npm install` here.

## 3. Commit

Branch discipline for this repo: **feature work goes to `develop`**, and `develop` reaches
`main` through a PR. Never commit a post directly to `main`.

```bash
git checkout develop        # if not already there
git add data/blog/<year>/<slug>.mdx
git commit -m "feat: add blog post \"<title>\""
```

Match the existing message style: `feat:` for a new post, `fix:` for corrections to a
published one.

**Never add `Co-Authored-By` or any Claude/Anthropic attribution to commits.**

## 4. Push — confirm first

Pushing is outward-facing. **Ask before pushing**, every time, even if a push was approved
earlier in the session:

```bash
git push origin develop
```

Then open a PR to `main` when the batch is ready.

## Guardrails

- **Never push without explicit confirmation in the current turn.**
- **Never commit a post with validation errors**, even if asked to hurry — the post will be
  invisible on the site and the failure gives no signal.
- **Do not amend or force-push** published commits.
- If the build fails for a reason unrelated to the post, say so plainly and stop. Do not
  work around a broken build by skipping verification.
- Report what actually happened. If the dev-server check was used instead of a full build,
  say that.

## Next step

Post live? Note anything learned in `docs/learned.md` — the Ship step of the Lite profile.
