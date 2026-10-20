---
name: write-project-listing-text
description: >-
  Load this skill when writing the public pitch of a repo, package, or product: README first
  screen, repo description and topics, package keywords, listings. Trigger on "make this repo
  findable", "improve the pitch", "GitHub topics", or a first publish. Not for keeping a README
  accurate.
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Text discoverability

Every internet-exposed text surface (GitHub, PyPI, npm, a marketplace, a search result) shows an
excerpt, and the excerpt decides whether anyone clicks. Search engines and AI engines index the
same words humans skim. Done means every surface carries the same excerpt-ready one-liner and
states its scope facts explicitly. This skill governs findability, not accuracy.

## Procedure

1. **Read the product handoff files.** When the repo has them, read them before writing, because
   they hold what earlier stages settled. `product/BUSINESS_PLAN.md` gives who the product is for,
   the problem, and the differentiator: take them from it rather than asking. `product/EVIDENCE.md`
   bounds every claim about what the product does or how well it does it (tested, fast, secure,
   usable). Read only its newest section, the first one, because earlier sections describe older
   commits. State only what that section's Claims list, and nothing about an area it marks `stale`,
   `not run`, or `open issues`. When either file is missing, carry on from the repo and say which
   claims rest on nothing proven.
2. Write the excerpt: the first ~160 characters of any description, and the first paragraph of any
   README, are what gets shown and quoted. They must contain, in plain searched nouns:
   1. **What it is** — the category noun ("a Python rate-limiting library", "a Claude Code plugin").
   2. **Who or what it is for** — the user or problem.
   3. **The differentiator** — the one fact that separates it from the ten alternatives.

   Bad: `Lightning — supercharge your workflow.`
   Good: `Lightning — a Python rate-limiting library for asyncio services, with per-tenant quotas
and zero external dependencies.`

   A clever name with no category noun in reach is unfindable: nobody searches your project's name
   before they know it exists.

3. Fix one canonical one-liner and reuse it **verbatim** on every surface: GitHub repo
   description, README first line, manifest `description`, landing hero. Paraphrase drift across
   surfaces splits the signal — engines see three weak descriptions instead of one strong one, and
   AI engines quote whichever they crawled last.
4. Walk the surface checklist and fix each surface the task touches:

   | Surface                                       | What matters                                                                                                                                                                               |
   | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | GitHub repo                                   | Description = the one-liner. Topics: the terms people actually search, lowercase, specific over broad (`rate-limiting`, not `python`)                                                      |
   | README first screen                           | Title + one-liner + a 3-line what/why + the install command — all before badges, ToC, or architecture diagrams                                                                             |
   | PyPI (`pyproject.toml`)                       | `project.description` = the one-liner; `keywords`; accurate classifiers (Python versions, license, dev status); README renders as the long description — its first screen is the PyPI page |
   | npm (`package.json`)                          | `description` = the one-liner; `keywords` array with searched terms                                                                                                                        |
   | Marketplace listings (incl. plugin manifests) | The description is also the trigger/matching surface — front-load the verbs and nouns a matcher scans for                                                                                  |

5. Apply the GEO rules (writing for AI engines) to every paragraph you write:
   - **Extractable claims.** Full "X does Y" sentences that survive being quoted alone. Numbers
     over adjectives: "handles 10k req/s on one core", not "blazingly fast".
   - **State scope facts explicitly** — supported versions, platforms, what it does _not_ do.
     These are the questions engines get asked; unstated facts get hallucinated.
   - **Question-shaped headings** for FAQ-type content — the heading is the query.

## Rules

- Put the pitch before any badges — otherwise the excerpt window fills with shield URLs.
- Attach a verifiable fact to every marketing adjective.
- No keyword-stuffed descriptions — package indexes and engines both derank them.
- Use the one canonical one-liner from step 3 on every surface.
- Post-change accuracy of the README belongs to `ceh-git-workflow:update-readme`. Head tags,
  sitemaps, and structured data on HTML pages belong to `ceh-seo:make-page-crawlable`.
