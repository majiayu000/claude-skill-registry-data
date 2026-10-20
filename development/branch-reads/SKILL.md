---
name: branch-reads
description: Reads the diff on your current git branch (or a PR), works out which public libraries, APIs and patterns you are actually touching, and finds the 3-5 daily.dev posts most worth reading for that exact work. Can save them to a bookmark folder named after the branch. Use when starting, finishing or reviewing a branch.
---

# Branch Reads

You are mid-branch, touching an API you half-know. Branch Reads looks at what you changed, not what you follow, and hands you the few posts that matter for this piece of work, each with a one-line reason tied to your code.

## Requirements

- A git repository as the working directory. `gh` is optional (only for PR mode).
- One of:
  - The daily.dev MCP server (`https://api.daily.dev/mcp`) connected to your agent, or
  - A daily.dev personal access token in `DAILY_DEV_TOKEN` (https://daily.dev/settings/api). Base URL `https://api.daily.dev/public/v1`, header `Authorization: Bearer $DAILY_DEV_TOKEN`. Never send the token anywhere except `api.daily.dev`.

Each API step lists the MCP tool first and the REST call after it.

## Modes

Pick from what the user said; default is **branch**.

- **branch**: committed work on this branch vs. its base.
- **wip**: uncommitted and staged changes only (`git diff HEAD`).
- **pr N**: someone else's PR you are reviewing (`gh pr diff N`). Never save to bookmarks in this mode unless asked.

## Steps

1. **Get the diff.** Local git only; nothing from this step leaves the machine.
   - Base: `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` (strip `origin/`); if that fails, use `main`, then `master`, whichever exists. Then `BASE=$(git merge-base HEAD origin/<default> 2>/dev/null || git merge-base HEAD <default>)`.
   - Branch name: `git branch --show-current` (on a detached HEAD, use `git rev-parse --short HEAD`; in **pr** mode, use `pr-N`). Repo name: basename of `git rev-parse --show-toplevel`.
   - `git diff --stat $BASE...HEAD`, then `git diff -U2 $BASE...HEAD`. In **wip** mode use `git diff --stat HEAD` / `git diff -U2 HEAD`.
   - If the branch diff is empty, fall back to uncommitted changes; if that is empty too, use the last 5 commits (`git diff HEAD~5...HEAD`, or fewer if the history is shorter) and say so.
   - Ignore lockfiles, `vendor/`, `node_modules/`, `dist/`, `build/`, minified files, snapshots, images and generated code. If more than 15 files remain, read only the 15 with the most added lines.

2. **Find the topics.** From the added lines (`+`), list the concrete, *public* things being used for the first time or in a non-trivial way:
   - newly imported packages or modules, and the specific functions, classes, hooks, directives or config keys used from them (e.g. Laravel `Bus::batch`, Vue `defineModel`, `useOptimistic`, Postgres `LISTEN/NOTIFY`, a GitHub Actions `concurrency` block);
   - patterns the change introduces (rate limiting, idempotency keys, optimistic UI, cursor pagination, a new Dockerfile stage);
   - framework or language version bumps visible in manifests (note the major version: it decides which posts are still valid).
   
   Skip the obvious (a `for` loop, a getter) and anything the project already uses heavily outside this diff. Keep **3 to 5 topics**. For each: a short label, the evidence (`path:line`), and a query of **2-3 public keywords** (e.g. `laravel job batching`, `vue defineModel`).

   **Privacy rule:** queries may contain only public technology names and generic terms. Never put internal class or function names, domain words, customer names, URLs, hostnames, file paths, secrets or code snippets into any API call.

3. **Search.** Per topic, at most two calls:
   - `getRecommendKeyword` with `q` = the most specific technical term(s), `limit` 10, `time` `year` (`GET /recommend/keyword?q=...&limit=10&time=year`). It works best on exact terms like `defineModel` and returns nothing for long phrases.
   - If it returns fewer than 3 relevant posts, `getSearchPosts` with the 2-3 keyword query, `limit` 10, `time` `year` (`GET /search/posts?q=...&limit=10&time=year`). Use `time` `all` only for stable, older topics.
   
   Stop at 10 search calls per run in total.

4. **Rank and pick 3-5 posts overall**, at most 2 per topic:
   - **Fit first**: the title or `summary` must address the specific API or pattern from step 2, not just the framework. A general "What's new in Laravel" loses to a post on job batching.
   - **Version**: when the diff shows a major version, drop posts clearly about an older major.
   - **Then signal**: `numUpvotes` and `numComments`, then recency (`publishedAt`, falling back to `createdAt`). Prefer articles over videos unless a video is clearly the best fit.
   - Dedupe by `id` and by `url`.
   
   If a topic has nothing that fits, say so in one line instead of padding with weak matches.

5. **Report** (under 300 words, before any write):
   - Header: `Branch Reads: <repo>/<branch>` and one line naming the topics found.
   - Per post: linked title (use `commentsPermalink`), then `source.name · readTime min · numUpvotes upvotes · date`, then **Why for this branch:** one line that names the file or change it applies to. Add **Heads-up:** only if the `summary` flags a gotcha that matches the diff.
   - Order by what to read first: the post that unblocks or de-risks the change comes first.
   - End with: "Save these to a `<branch>` bookmark folder?"

6. **Save, only if the user says yes.**
   - `getProfile` (`GET /profile/`) and read `isPlus`.
   - **Plus**: `getBookmarksLists` (`GET /bookmarks/lists`). Reuse a list named exactly `<repo>/<branch>` if it exists; otherwise `postBookmarksLists` with `name` = `<repo>/<branch>` truncated to 100 characters and `icon` `🌿` (`POST /bookmarks/lists`). Then `postBookmarks` with all picked `postIds` and that `listId` (`POST /bookmarks/`).
   - **Not Plus**: bookmark folders need daily.dev Plus. Say so, and offer to add them to regular bookmarks instead with `postBookmarks` without `listId`. Do that only on a second yes.
   - Confirm in one line with the count and the folder name.

## Guardrails

- Read-only until step 6, and step 6 only on an explicit yes. Never remove bookmarks, delete lists, follow tags or change anything else on the account.
- Never upload code. Only short public keyword queries go to daily.dev (see the privacy rule in step 2).
- Never run `git` commands that change state (no checkout, fetch, commit, stash or reset).
- Budget: at most 14 API requests per run (10 search plus up to 4 for saving). If you get a 429, stop and report what you have, along with the `retry-after` value.
- Don't invent posts, numbers or links. Every item comes from an API response in this run.
