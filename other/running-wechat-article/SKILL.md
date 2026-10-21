---
name: running-wechat-article
description: Research, verify, and draft runner-facing WeChat public-account articles about road running, marathons, trail running, training, gear, nutrition, recovery, athletes, and race business. Use when a user asks for a current running topic, a race guide or analysis, copyright-safe image sourcing, or a two-file Markdown article package for their own WeChat account.
---

# Running WeChat Article

Create useful, original, source-grounded running articles. This skill is account-neutral: never assume an account name, brand voice, watermark, credentials, publisher, local path, or upload tool.

## Start safely

1. Read `references/account-profile.template.md`. If the user supplies a workspace account profile, use it; otherwise ask only for the missing audience, tone, topic, and publishing goal.
2. Treat current facts as perishable. Research before stating dates, rules, prices, qualification criteria, results, product specifications, safety notices, or registration status.
3. Keep account credentials, private drafts, source downloads, subscriber data, and upload results outside this skill and outside Git.
4. If the user asks only for ideas, return a ranked topic shortlist. Do not write a full article until a concrete subject is selected.

## Research

- For race and event facts, prioritize organizer notices, registration pages, governing bodies, official athlete/team/brand channels, and official media kits.
- Use reputable reporting to add context, not to replace an available primary source.
- Separate confirmed facts, attributed claims, community discussion, and the article's own judgment. Do not turn a search snippet or social post into a confirmed fact.
- For training, health, fueling, injury-risk, and recovery topics, give general information rather than diagnosis or a universal prescription. State material uncertainty and who should use extra caution.
- For gear, distinguish official specifications, marketing claims, observed use, and independently supported conclusions.

## Find the reader decision

Choose an angle that changes a runner's decision: whether to register, travel, train differently, buy, wait, prepare for a route, or question a rule. Do not produce an announcement paraphrase when the topic contains a real trade-off.

Use a fitting form:

- **Service guide** for deadlines, checklists, and action order.
- **Data analysis** for quotas, rankings, prices, route metrics, or comparisons.
- **Reported analysis** for complex events and industry changes.
- **Opinion/brief** for a verified controversy or rule trade-off.
- **Scene-led feature** for places, people, trails, and strong visual material.

Avoid repeating the same opening, heading cadence, or closing question across adjacent articles. State one deliberate structural difference in the internal file.

## Images and rights

Read `references/image-sourcing.md` before selecting any image.

- A visible image, an image without a watermark, a search result, or a social post is not permission to republish or alter it.
- Prefer user-owned material, explicit permission, official reusable press assets, or compatible open licenses. Keep attribution and the exact source link in the internal file.
- Use self-made charts or diagrams when they explain a decision. Do not copy another publisher's poster, layout, or copy.
- Never add an account watermark unless the image owner and the account profile explicitly allow it.

## Output contract

For a finished article, create two Markdown files with the same concise prefix:

1. `prefix选题与成稿.md` — internal file containing the angle, source facts, uncertainty, title/cover decision, image-rights table, selected form, and pre-publish checks.
2. `prefix公众号正文.md` — publish-facing draft containing frontmatter title, guide, body, image placements, concise source list, and concise image credits only.

Do not put research notes, permissions analysis, account credentials, internal checklists, or AI-process commentary in the publish-facing draft. Keep ordinary paragraphs readable on mobile; use one-line paragraphs sparingly for emphasis.

## Completion gates

Before calling a draft ready:

- Recheck high-impact facts and label unresolved facts instead of guessing.
- Confirm each image's permissible use or replace it.
- Remove unsupported certainty, copied wording, empty marketing language, and generic inspirational endings.
- Run an optional account style linter only after the user confirms its trusted executable; invoke it with an argv array and never run a shell command string loaded from a workspace profile. Then preserve verified names, figures, dates, and source boundaries.
- Stop at local files unless the user separately invokes an upload flow and confirms the external action.
