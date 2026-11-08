---
name: vercel-api
description: Talk to Vercel over its REST API without opening the dashboard — list a team's projects and their real production URLs, see whether a project deploys from git or the CLI, check a deployment went READY, deploy a CLI-linked folder, enable Web Analytics, and pull analytics with a device or path filter. Use when a task says "all our sites on Vercel", "what's the live URL for X", "did that deploy", "deploy it", "turn on analytics", "which page did the phone visitor hit", or any script needs the project list.
---

# Vercel API

Token: `VERCEL_TOKEN` (create one in Account Settings -> Tokens; keep it in `.env`, never in
a repo). If your projects live under a team, **every call needs `teamId=<team_...>` or it
sees nothing** — recover the id with `GET /v2/teams`. No CLI install needed: `npx -y
vercel@latest`.

## Projects and their live URL

    GET https://api.vercel.com/v9/projects?teamId=<team>&limit=100

`projects[].targets.production.alias` is the list that matters. **Pick the custom domain,
else the shortest `<name>.vercel.app`, and never an alias containing `-<team-slug>-projects`
or `-git-`.** Those sit behind Vercel SSO and return a 200 login page that looks like a site
(short page, a Vercel logo, `maximum-scale` in its meta) — an automated audit will happily
score it as your site. Long project names get truncated aliases, so read the alias, never
guess it. After a rename, the shortest alias can be the OLD name. `link.repo` is set only on
git-connected projects.

## Did it deploy, and how does it deploy

    GET /v6/deployments?projectId=<id>&teamId=<team>&limit=2&target=production

`meta.githubCommitRef` present -> git-connected: a push deploys. Absent -> it was a CLI
deploy; a commit alone changes nothing live. `state` is `READY` when done (typically under a
minute from push).

## Deploying a CLI project

The linked folder carries `.vercel/project.json`. From inside it:

    npx -y vercel@latest deploy --prod --yes --token "$VERCEL_TOKEN"

`--yes` skips the link prompts because the folder is already linked. Verify with the
deployments call above; the CLI's own output is a wall of JSON.

## Ship every project with Web Analytics on

A new project isn't done until both of these hold:

1. Web Analytics is enabled on the project. Probe:
   `GET /v1/query/web-analytics/visits/count?projectId=<name>&since=...&until=...`.
   `web_analytics_not_enabled` means it's off.
2. `curl -s https://<alias>/ | grep -c _vercel/insights` is >= 1. Put the tag in the source or
   generator, never only in the built HTML (a rebuild erases it).

**Enabling it is one API call** (`createWebInsightsToggle` in the OpenAPI spec at
`openapi.vercel.sh`):

    curl -s -X POST "https://api.vercel.com/web/insights/toggle?projectId=<prj_id>&teamId=<team>" \
      -H "Authorization: Bearer $VERCEL_TOKEN" -H 'content-type: application/json' -d '{"value":true}'
    # -> {"value":true}

- `projectId` must be the **`prj_...` id**. The project NAME returns `Project not found` here,
  although the analytics query endpoints accept the name.
- PATCH `/v9/projects` rejects a `webAnalytics` field; this toggle is the only route.
- Confirm: `GET /v9/projects/<id>` -> `webAnalytics.enabledAt` is set.
- Then the tag: static HTML gets
  `<script>window.va=window.va||function(){(window.vaq=window.vaq||[]).push(arguments)}</script><script defer src="/_vercel/insights/script.js"></script>`
  before `</head>`; Next.js gets `@vercel/analytics` `<Analytics/>` in the root layout.
  Redeploy, then run check 2. Custom events (`va.track`) need a Pro plan.

**A 404 on `/_vercel/insights/script.js` with analytics enabled = an instant-static deploy.**
Vercel may class a plain static upload (REST or CLI, e.g. a single `index.html`) as
`isInstantStatic: true`: there's no build container (`duration: {}`), so the insights route
is never mounted. Toggling and redeploying changes nothing. Check `GET
/v13/deployments/<id>` -> `isInstantStatic`. Fix: add a `vercel.json` with
`{"buildCommand":"echo build","outputDirectory":"public"}`, upload the static files under
`public/`, redeploy, and confirm the script returns 200.

## SECURITY: never `outputDirectory: "."` on a project with functions

It makes every uploaded file a static URL: private data a function serves behind a paywall
(e.g. `api/_full/`), the function source itself (prompts, logic), drafts, ledgers. A
redirect on `/api/_full/:path*` does not save it, because Vercel matches the raw path:
`/api/%5Ffull/<f>`, `/api/_full%2F<f>`, `/api/_full/<f>/` and `/%61pi/_full/<f>` all served
the file in testing.

**How to do it right:** upload non-`api/` files as `public/<rel>` (plus a root copy of any
file a function `require()`s); set `"outputDirectory": "public"` in **both** `vercel.json`
and the deploy payload's `projectSettings`, since the payload wins; pin it with a test; after
deploy, curl every spelling above and expect 404. Public-only deploys still mount
`/_vercel/insights/script.js`.

## Web analytics with a filter

- Time is `since=<ms epoch>&until=<ms epoch>`, not `from`/`to` ISO.
- The filter is an **OData string**, not JSON: `filter=deviceType eq 'mobile'`, URL-encoded.
  `by=requestPath` with that filter is how to learn which page a phone visitor actually hit
  before debugging a page. `by=osName` separates iOS from Android.
- Visitors are not additive across days (the visitor hash rotates daily).

## What this skill does not own

Phone-visitor QA -> `mobile-ui-audit`. Console tasks with no API (domains, SSO settings) ->
a browser session.
