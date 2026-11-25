---
name: website-launch-gate
description: Audits and fixes a website before launch across legal, security, SEO, accessibility, performance, responsiveness, forms, analytics, and conversion basics. Use before publishing a new website or major redesign.
---

# Website launch gate

Treat launch readiness as a verification job, not a request to repeat a checklist.

## Workflow

1. Identify the repository, the build and test commands, and any preview or deployed URL supplied by the user. Do not deploy, publish, alter production data, or create third-party accounts unless the user authorized it.
2. Run the existing checks and inspect both the source and the rendered website where possible. A claim passes only when supported by a command result, source location, HTTP response, or rendered-page observation.
3. Check every item below. Mark an item `N/A` only when the site genuinely does not need it, and state why. Mark anything unverified as `UNKNOWN`, not `PASS`.
4. Fix in-scope failures when the user asked for implementation. Re-run the relevant check after each fix. If the user asked only for an audit, do not change files.
5. Report the launch decision first, followed by failures and evidence. Do not bury a security, legal, form, or mobile blocker inside a numerical average.

## The 20 checks

1. A real privacy policy exists and is linked where users provide data.
2. Terms and conditions exist when the product or transaction requires them.
3. No frontend bundle, public configuration, or committed file exposes a secret.
4. Production traffic uses HTTPS and insecure HTTP is redirected.
5. Cookie consent is present when non-essential cookies or applicable jurisdictions require it; consent must control those cookies rather than merely display a banner.
6. Every public route has a useful, route-specific title and description.
7. Shared links render the intended social preview image and metadata.
8. A favicon loads successfully.
9. `sitemap.xml` and `robots.txt` exist, return successfully, and agree with the intended public routes.
10. Meaningful images have useful alternative text; decorative images are ignored correctly.
11. Images are sized and compressed appropriately for their rendered use.
12. Measure page-load performance on representative mobile and desktop pages. Record the tool and result.
13. Text, controls, focus states, and essential graphics have sufficient contrast.
14. Key routes work at mobile widths without clipping, horizontal overflow, or unusable controls.
15. Unknown routes return a useful custom 404 page with a recovery path.
16. Internal links and important external links do not break.
17. Forms validate required fields, invalid formats, server failures, and successful submission states.
18. Public forms have proportionate spam or abuse protection without blocking normal use.
19. Analytics is present only when requested, fires on the intended environment, and respects consent requirements.
20. Each important page has one clear primary call to action whose label and destination agree.

## Output

Use a table with `Check`, `Status`, `Evidence`, and `Action`. End with:

- `GO` only when no launch blocker remains.
- `NO-GO` when a verified blocker remains.
- `UNVERIFIED` when missing access or tooling prevents a defensible decision.

Never convert `UNKNOWN` or `N/A` into a pass when calculating a summary.

## Credit

Checklist adapted from [Suraj Sharma's “20 tasks for Claude before website launch”](https://x.com/suraj_sharma14/status/2101154043720876226).
