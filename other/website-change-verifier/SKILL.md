---
name: website-change-verifier
description: Verify website changes across source, routes, rendering, metadata, discovery surfaces, and deployment state. Use when a user asks to check a new or edited page, confirm an exact replacement, validate a route, inspect responsive behavior, verify metadata or sitemap changes, compare localhost with production, or determine whether a website change is fully working.
---

# Website Change Verifier

Verify the complete user-visible result of a website change. Default to read-only checks and report the highest completion state supported by evidence.

## 1. Identify the change and platform

- Confirm the project root, target route, requested outcome, source of truth, and expected visibility.
- Inspect project instructions, manifests, entrypoints, routing, and nearby implementation patterns.
- Read [references/framework-checks.md](references/framework-checks.md) for the detected stack.
- Preserve existing public URLs and unrelated behavior unless the request explicitly changes them.

## 2. Map affected surfaces

Check which parts of this chain apply:

1. content or data source
2. route or page rendering
3. navigation, listings, related content, and internal links
4. title, description, canonical, Open Graph, structured data, and accessibility text
5. sitemap, robots rules, `llms.txt`, feeds, search indexes, or static export
6. images, video, downloads, and responsive variants
7. local server, deployment, cache, and live state

For hidden content, distinguish navigation removal from direct access, sitemap presence, and search visibility.

## 3. Verify in layers

- Read [references/verification-matrix.md](references/verification-matrix.md) and select checks proportional to the change.
- Run syntax, type, lint, test, or production-build checks supported by the project.
- Confirm the correct listener and make a real request to each affected route.
- Use `scripts/verify_routes.py` for deterministic status and response-text checks.
- Inspect rendered desktop and mobile behavior when layout, interaction, forms, or media changed.
- Confirm required text is present and replaced text is absent.
- Check discovery surfaces only when the content is intended to appear there.

Example:

```powershell
python scripts/verify_routes.py `
  --url http://127.0.0.1:8766/example `
  --contains "http://127.0.0.1:8766/example::Expected heading" `
  --not-contains "http://127.0.0.1:8766/example::Old wording"
```

Use `--expect-status "URL::404"` for an intentionally missing route and `--json` for machine-readable output.

## 4. Respect authority boundaries

- Access only the project and URLs placed in scope.
- Do not include authentication values in URLs, commands, logs, or reports.
- Do not deploy, publish, submit indexing requests, change DNS, purge caches, or modify external services unless explicitly authorized.
- After an authorized deployment, repeat the relevant checks against the final public URL.

## 5. Report the supported completion state

Use one of these states:

- `implemented`: source changes exist but user-visible verification is incomplete
- `verified locally`: build and local route or browser checks pass
- `deployed`: an authorized deployment completed but live verification remains
- `verified live`: the production URL and intended behavior were checked after deployment

Return the checked routes, expected and observed results, build or syntax results, browser coverage, discovery-surface status, highest completion state, and exact remaining blocker.
