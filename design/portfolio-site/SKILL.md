---
name: portfolio-site
zh_name: "作品集网站"
en_name: "Portfolio Site"
emoji: "🗂️"
description: "A designer's portfolio website from their work library: a home page that passes a hiring manager's first look on a phone, one case study per project built around decisions and outcomes, and an about page, published as one site."
en_description: "A designer's portfolio website from their work library: a home page that passes a hiring manager's first look on a phone, one case study per project built around decisions and outcomes, and an about page, published as one site."
category: web
scenario: personal
tags: ["portfolio", "case study", "design portfolio", "ux portfolio", "product designer", "job application", "作品集", "案例"]
triggers:
  - "portfolio site"
  - "portfolio website"
  - "design portfolio"
  - "ux portfolio"
  - "case study page"
  - "case studies"
od:
  mode: prototype
  craft:
    requires:
      - typography
      - accessibility-baseline
      - anti-ai-slop
      - ux-writing
  surface: web
  platform: desktop
  scenario: personal
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
  example_prompt: "My product design portfolio from my work library: the checkout redesign, the bank onboarding and the design system, for senior product designer roles."
---

<!-- Kit skill (openspec add-portfolio-site-and-deck). -->
# Portfolio Site

A website for one designer, built from their work library (`get_open_design_library`): a home page, one case study per chosen project and an about/contact page, linked as one collection and published as one site with home as its `index.html`.

## Before the first page

1. **Read the library.** Call `get_open_design_library`. If there is none, or the projects lack facts, use the open-design-portfolio skill first: save the projects, import the work, confirm alt text. Never write a case study from facts the library doesn't hold.
2. **Ask once, at most three questions, together**, unless the conversation already answers them: the discipline (product, UX, visual, brand, motion…), who it's for (hiring managers for a role, clients, a school), and which projects to show (three to five; suggest the library's first ones). Accept "you pick".
3. **Style.** The library's style (its design system) is used unless the designer names another. If there is no style and the designer has a site, a Figma file, a Canva design or screenshots of their own work, offer to extract their own design system from it (`extract_open_design_design_system`) before building, so the portfolio looks like them and not like a template.
4. **Plan the site.** One `collectionId` (e.g. `portfolio-site`; not `portfolio`, which is the library's own folder) and a `flow` with `kind: "site"`:
   - screens: `index` (Home), one per case study with the project slug as its id, `about` (About and contact);
   - links: home → each case study ("Read the case study"), each case study → the next one and back home, every page → `about`;
   - `nav`: Work → `index`, About → `about` (add a résumé link in the nav only if the library has one).
5. **Build each page** with its own `prepare_open_design_brief` call: the same `collectionId`, `flow` and `portfolio: { projects: [<all chosen slugs>] }`, the page's id as `screenRole`. The brief lists each project's facts and the pictures you may use, with their markup. Register each page with the same `collectionId`, `screenRole`, `flow` and `portfolio`.
6. **Check** each page with `check_open_design_artifact`, then the collection with `collectionId`. Fix every error and the portfolio warnings (first screen, summary, length, alt text, weight, live links).
7. **Publish** with `publish_open_design_artifact` from any page: the site opens on home.

## Home page (`index`)

- The first screen, on a 390 × 844 phone and on a desktop, shows the designer's name, their role, a contact link (`mailto:` or one marked `data-od-contact`) and the top of the first project card. Nothing else has to fit; the check measures these four.
- One card per case study, in the library's order, each marked `data-od-project-card`: one picture, the title, the designer's role and one outcome line. The whole card links to the case study.
- No skills bars, no logo walls of tools, no "Hi, I'm" hero filling the screen.

## Case study (one per project)

Put `data-od-case-study="<project slug>"` on `<body>`. The body text (outside navigation and footer) runs 500 to 1,800 words; the check counts it. Sections, in this order, with headings in the designer's voice:

1. **Summary**, marked `data-od-summary`: role, team, dates, platforms and the main outcome (mark it `data-od-outcome`). A reviewer should get the project in ten seconds.
2. **Problem**: what was wrong and for whom, from the library.
3. **Constraints**: what limited the work.
4. **Decisions**: give these the most room. For each, the choice, the options rejected and why, and the trade-off, with the pictures that show it. A rejected option shown beside the chosen one is the strongest thing on the page.
5. **Outcome**: each outcome exactly as the brief writes it (a measured number as given, an estimate with "about", a qualitative one without a number). Never round, combine or invent.
6. **How I worked** (only when the brief lists records): the explorations, comparisons, edits, review rounds and before/after pages the kit has for the project, and the designer's own note. When the brief says there are none, leave the block out.
7. **Next steps or what I'd do differently**, only if the library or the designer says.
8. Links: the live product (`data-od-live`), prototypes, write-ups; then the next case study and a way home.

The outline is an order, not a layout: build the layout from the design system and the work itself, so two designers' sites don't look alike. Vary the picture rhythm (a full-width hero shot, a pair comparing chosen and rejected, a strip of phone screens) instead of repeating one block.

## Pictures

- Use only the pictures the brief lists, with the markup it gives: `src`, `srcset` with the 800/1400/2800 variants, `sizes`, `width` and `height`, the library's alt text and `data-od-asset`. The brief has already left out internal pictures and applied redaction.
- `loading="lazy"` on every picture below the first screen; the first card's picture loads eagerly.
- Alt text marked as a draft in the brief must be confirmed by the designer before publishing; the check reports drafts.
- A page and what it loads stays under 3 MB.

## About page (`about`)

The designer's own bio from the library, where they are, how to reach them (the same contact link), and their links. No invented testimonials, client logos or years of experience.

## A version for one job or client

With a target (`portfolio: { target }`), the brief gives its projects in order, its ceiling and its cover note. Build it as its own collection (the target slug as `collectionId`), open the home page with the cover note, mark each project's block `data-od-project="<slug>"`, and for an unlisted target put `<meta name="robots" content="noindex">` in every page's head and don't link it from the public site. A client target can add a "For you" section (`data-od-for-you`) linking the redesign concept of their site and its before/after page.

## Rules

- Only library facts. When a fact the outline needs is missing, ask, or leave that part out.
- An `unlisted` project stays off any public list or search page the designer adds later; say so if they ask to share the site widely.
- Tokens only: every colour, size, radius and shadow comes from the design system's `:root` variables.
- Real links: every page links to the others with `href="<id>.html"` and `data-od-goto="<id>"`, and uses the shared navigation the brief gives.
