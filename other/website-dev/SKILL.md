---
name: website-dev
description: "Ship changes to an existing Next.js (or static) site that auto-deploys from GitHub to Vercel, and prove they are live: fresh clone, canonical package manager and build, local production check, push or PR, poll Vercel's GitHub commit status for that exact SHA, then smoke-test the live page for expected content, not just HTTP 200. Covers the Vercel team-author deploy block, the stale `next start` trap, static bundles with no output directory, Supabase + Vercel production releases, and short coding-agent briefs. Use when asked to build, fix, add a page to, deploy, redeploy or verify a website, or when a Vercel deploy did not happen. Requires Claude Code with git and an authenticated gh CLI."
---

# Website Dev: build, push, prove it is live

A push is not a deploy and a 200 is not the right page. This skill ends only when the
exact commit is deployed and the live page shows the expected content.

## Inputs

- GitHub repo (`owner/repo`) and the branch to ship to (default branch or a PR branch).
- The change, and one **identity string**: a title or sentence that only the new version contains.
- Live URL of the route (production domain or preview URL).

Missing the identity string? Pick one from the change itself (new heading, new title) before you start.

## Rules

- Work in the existing repo and the existing Vercel project. Never create a new Vercel project for a site that has one: one repo, one project, one URL.
- Never force-push, rewrite history, or push a build that fails. Never commit `.env*`, keys or tokens; never print secret values.
- The commit author must be a GitHub account that belongs to the Vercel team, or Vercel blocks the deploy (see step 6).
- Use the package manager the repo declares (`packageManager` field + its lockfile). A green build from the wrong one does not count.

## Steps

### 1. Fresh clone and preflight
```bash
gh repo clone <owner/repo> ~/tmp/<repo> && cd ~/tmp/<repo>
git remote show origin | grep 'HEAD branch'          # main vs master
gh auth status                                        # which account will author
git config user.name "<vercel-team member>"; git config user.email "<their GitHub noreply email>"
```
If you already have a working tree with uncommitted relevant work, continue that instead of overwriting it.

### 2. Install
`pnpm install --frozen-lockfile` / `npm ci` / `yarn --frozen-lockfile` / `bun install` to match the lockfile.
On npm peer-dependency conflicts: `npm install --legacy-peer-deps`. Then `git diff package-lock.json`: revert lockfile noise you did not intend (a renamed clone dir can rewrite the `name` field).

### 3. Change, then build
Make the change. Run the canonical build (`pnpm run build` etc.). Fix every error, rerun. After any later edit, rerun the build; an earlier green build is stale.
For a new Next.js route, confirm it appears in the build's route table and add it to `app/sitemap.ts` (or the sitemap source) and any index/nav page that lists siblings.

### 4. Local production check
```bash
lsof -nP -iTCP:3100 -sTCP:LISTEN            # anything here? if it is YOUR old next start, kill that PID (the node child, not just the npm wrapper)
PORT=3100 npm run start &
curl -s localhost:3100/<route> | grep -c "<identity string>"   # must be >= 1
```
An old `next start` whose `.next` folder was replaced returns 200 with blank or stale content. If the page renders client-side only, check the route's JS chunk or use a headless browser; view the page at 390 px and 1440 px wide for clipping and overflow.

### 5. Push
- Default branch: `git push origin HEAD`. PR flow: `git push -u origin <branch>` then `gh pr create`.
- Record `SHA=$(git rev-parse HEAD)`.

### 6. Prove the deploy
```bash
scripts/verify-deploy.sh <owner/repo> $SHA https://<domain>/<route> "<identity string>" 600
```
It polls Vercel's **legacy commit status** (Vercel reports there even when Checks and Deployments look empty), then fetches the live URL until the identity string appears.

| exit | meaning | do this |
|---|---|---|
| 0 | deployed, content verified | report done |
| 1 | Vercel failure/error | open the printed target_url, quote the exact error, fix, push a new commit |
| 2 | timed out while pending/building | keep polling once more; if still pending, report the target_url |
| 3 | deployed but content missing | catch-all route returning a fallback, wrong URL, CDN cache, or client-only render; verify the JS chunk |
| 4 | no Vercel status at all | Git integration, ignored build step, branch settings, or author gate; see below |

**Author gate** (status says the author is not a team member, or links to a team invite): push an empty commit authored by a team member on the same branch: `git commit --allow-empty -m "chore: trigger vercel deployment" && git push`, then rerun step 6 on the new SHA. For a PR preview, do it on the PR branch, not main. A squash merge can keep the PR author as commit author even when a team member merged it: check `gh api repos/<o>/<r>/commits/<sha> --jq .author.login`. Full diagnosis: `references/vercel-author-gate.md`.

## Specialised paths

- Static/custom bundle fails with `No Output Directory named "public" found`: `references/vercel-static-output.md`.
- Next.js + existing hosted Supabase going to production (migrations, RLS, Auth/SMTP, env vars, first admin user): `references/supabase-vercel-release.md`. Never `supabase db reset` against production.
- Read-only audit of a site repo (routes, sitemap drift, downloads, leaked credentials, build readiness): `references/read-only-site-audit.md`.
- Writing a prompt for another coding agent (Codex, a subagent): `templates/coding-agent-brief.md`. Keep it 300-700 words; if the user says it is too long, cut it by half, do not defend it.

## Progress reporting (long jobs)

Report against gates, not vibes: 1 code changed, 2 build passed, 3 local check passed, 4 visual QA done, 5 pushed (SHA), 6 Vercel success, 7 live content verified. Anything short of 7 is "not deployed yet", said plainly.

## Output format

```text
Shipped: add /pricing FAQ section
Repo: acme/site  branch: main  SHA: 3f9c2e1
Build: pnpm run build, passed (route /pricing in table)
Local: /pricing 200, "Frequently asked" present; 390px + 1440px checked
Vercel: success, https://vercel.com/acme/site/8kq...
Live: https://www.acme.com/pricing 200, "Frequently asked" present
Open: none
```

## Failure handling

- `gh` not authenticated: stop and ask the user to run `gh auth login`; do not paste tokens into chat.
- Build fails on untouched code: report it as pre-existing with the error, do not push.
- Vercel CLI says the token is not authorised for the scope: the GitHub side is done; the blocker is Vercel team/token scope. Say so.
- Production points at a different SHA than yours: state it and investigate before claiming success.

## Security check before every push

`git diff --cached | grep -nE '(sk-|ghp_|xox[bp]-|AKIA|BEGIN .*PRIVATE KEY|SUPABASE_SERVICE_ROLE|=.{32,})'` must be empty, `.env*` must be gitignored, and no secret may carry a `NEXT_PUBLIC_` prefix.
