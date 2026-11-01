---
name: explain-clearly
version: "1.0.1"
user-invocable: true
description: "Explain a concept clearly in the shape the subject has. Use whenever the user asks 「X 是什么」「为什么需要 X」「A 和 B 能不能/怎么通信」「给我讲讲 X」「用大白话解释 X」「帮我理解 X」「容易看懂」, \"what is X\", \"how does X work\", \"why does X exist\", \"explain X\" about mechanisms, architecture, protocols, or processes — even if they never say \"explain\". Do NOT use for hands-on tutorials (teach), marketing articles (article-writer), or design-doc rewriting (tech-review-doc)."
---

# Explain Clearly

> Explain a technical concept so the user can see how it works. Give the relevant causes in the shape the subject has. An analogy is optional and must not invert a constraint. Deliver the explanation in the user's language, in the form they chose.

## When to use

Use this for concept and mechanism questions: what something is, why it exists, and whether two parts can communicate. IPC, memory isolation, event loops, virtual DOM, consensus, and caching are typical subjects.

Route elsewhere and stop when the request is:

- A hands-on tutorial or onboarding ("教我怎么用 X", "walk me through setting up X") → `teach`
- Rewriting existing docs into an article → `article-writer`
- Turning a design doc into a review doc → `tech-review-doc`

## Choose the form

When the user has already named a form, use that form. When they have not, ask once. Offer exactly these choices, and recommend HTML:

1. current session
2. HTML
3. Markdown
4. plain text

## What every explanation contains

Name the subject in one sentence under the title. The shape under Visuals is the whole explanation.

Include a fact only when the picture cannot show it, when it is evidence for that cause, or when the user is choosing an action.

- **Evidence** — cite files, line numbers, and APIs read in this session, next to the step or part they prove. If the concept has no footprint in the current codebase, use a canonical public example and label it as such. If no canonical public example exists, say that no concrete example is available. An invented path, line, or API is a failed explanation.
- **A choice** — state the design implication only when the user is choosing an action.
- **An analogy** — one scene, only when it keeps every defining constraint. Omit the analogy when the picture already shows that relation. If a constraint would be lost or inverted, adjust or replace the analogy before delivery.

## Visuals

Apply the first match. Draw only relationships that exist.

1. A role-handoff flow: the diagram is the explanation and the diagram leads the page. Distinguish the roles, show order, and put the handed-off items on the diagram. A comparison table does not satisfy that flow. Do not also require the step player. Put the sentence the picture cannot show next to the part of the diagram it belongs to.
2. The subject happens step by step in time: lead with those steps. HTML shows one step at a time, opens on the first step, provides previous and next, and does not autoplay. HTML may contain one inline script, and that script only operates the player. Markdown, plain text, and the current session show the same steps as a numbered sequence and do not add those controls. A position mark is not a message. Each step shows only what is true at that moment. Put the sentence the picture cannot show next to that step. Put the code that proves a step on that step.
3. Comparison or mapping, and not time-ordered: one table leads, one row per item. Topology or flow, and not time-ordered: one static diagram leads. Put the sentence the picture cannot show next to that table or diagram.
4. No such shape: leave the visual out. A few sentences of the relevant cause are the explanation.

HTML and Markdown include that visual when the concept has a shape. Plain text stays prose. The current session uses the same first match: a diagram for a role-handoff flow, a numbered sequence only when the subject is time-ordered and not a role-handoff flow, a table or diagram for the other shapes, and no visual when the concept has no shape.

## Deliver

Create the workspace-root directory `.explain-clearly/` when a file form needs it. Name each file `<topic-slug>-<local-YYYYMMDD-HHmm>` with the extension for that form. Write a new file every time. Leave an existing file in place.

Do not edit the workspace gitignore.

- **current session** — put the explanation in the chat. Include the visual when the concept has a shape. Write no file.
- **HTML** — write `.explain-clearly/<name>.html` in the user's language. Read `assets/explanation-shell.html` as a reference for a page: inline CSS, and text written as text. The page is a title, one sentence under the title, and the visual for that shape. When the caller fixes the form to HTML and supplies an evidence-page path, keep the title, the one sentence, and the visual, and add one link after the visual. The link text is 证据留痕. The href is the relative path from this file to the evidence page. The link does not replace the visual. When the caller does not supply an evidence-page path, do not add that link. The shell itself has no script. The written page has no script except one inline script for a time-ordered player. The English words in that file are examples, because this skill is written in English. Omit the visual block when the concept has no shape. Open that local HTML file in the browser. In the chat, give the file path and ask the user to view the page. Do not paste the full explanation. If the browser cannot be opened, still give the file path.
- **Markdown** — write `.explain-clearly/<name>.md` in the same shape as the visuals rules. Include the visual when the concept has a shape. In the chat, give the file path and do not paste the full explanation.
- **plain text** — write `.explain-clearly/<name>.txt` as prose only. In the chat, give the file path and do not paste the full explanation.

## Worked examples

Two calibrated examples live in [reference.md](reference.md). Read them to match depth and to see how a generic example is labeled when the codebase has no footprint.
