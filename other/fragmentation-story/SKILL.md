---
name: fragmentation-story
description: >
  Tell a named movement leader's actual story of informational and relational
  fragmentation. Inventories every place their content currently lives — books,
  PDFs, articles, blogs, websites, social media, their own head, notes/laptop,
  apps, podcasts, YouTube, sermons, talks — with specific titles and locations
  pulled from prior research. Use when asked to map fragmentation for a leader,
  audit where their content is scattered, or produce a "where does it all live"
  report. Reads from `docs/movement_leader_research/{slug}/` and writes
  `fragmentation-story.md` into that leader's folder.
disable-model-invocation: true
---

Produce a fragmentation story for: $ARGUMENTS

`$ARGUMENTS` is one or more movement leaders — either the folder slug
(`alan-hirsch`, `andy-crouch`) or a full name (`Alan Hirsch`). Multiple leaders
may be passed; handle each independently and write a separate story for each.

## What This Skill Produces

For each named leader, a single markdown file at
`docs/movement_leader_research/{slug}/fragmentation-story.md` containing:

1. **The narrative opening** — 2–4 paragraphs telling *their specific story* of
   informational and relational fragmentation. Not a template. Names, specific
   counts, specific places. The reader should feel the scatter.
2. **Informational fragmentation map** — an exhaustive inventory of every
   surface where their content lives, with **titles and locations filled in**
   to the level the research supports.
3. **Relational fragmentation map** — where their relationships, networks, and
   collaborations live (and don't live).
4. **The synthesis** — a short closing that makes the picture legible: what
   fraction of their work is retrievable, what is trapped, what is invisible.

This is not generic. Blank fields must be labeled **UNKNOWN — needs research**
so the gaps are as honest as the findings.

## Step 1 — Resolve the leader

1. Normalize the argument. If a full name was passed, slugify it
   (`Alan Hirsch` → `alan-hirsch`). If passed a slug, use it directly.
2. Check `docs/movement_leader_research/{slug}/` exists. If not, also check
   `docs/movement_leader_research/profiles/{slug}/`. If neither exists, stop
   and tell the user no research folder was found — point them at
   `/author-research` to create one.
3. Note the folder path you resolved for the rest of the run.

## Step 2 — Inventory the available research

Read, in order of priority, whichever of these exist inside the resolved folder:

- `sources.md` — raw source list, often with URLs
- `profile/` — `identity.md`, `biography.md`, `theology.md`,
  `voice-analysis.md`, `calling-profile.md`
- `content/books.md`, `content/articles.md`, `content/academic.md`,
  `content/audio.md`, `content/videos.md`, `content/courses.md`,
  `content/frameworks.md`, `content/content-audit.md`
- `digital-presence/websites.md`, `digital-presence/social-media.md`,
  `digital-presence/newsletters.md`, `digital-presence/platforms.md`
- `summary.md`, `network/organizations.md`, `analysis/audience-analysis.md`
- `_misc/` helpers — `content-analysis-root.md`,
  `digital-presence-discovery.md`, `network/` (collaborators, endorsements,
  events), `media/` (citations, press-coverage, reviews)
- `_staff/` helpers — `gap-analysis.md`, plus the older `legacy/` ALL-CAPS
  profiles (`{NAME}_CONTENT_AUDIT.md`, `{NAME}_AUTHOR_PROFILE.md`,
  `{NAME}_ORGS.md`, `{NAME}_TIMELINE.md`) only if present — a freshly
  researched leader has the categorized files above instead
- For Alan Hirsch specifically, also read
  `docs/movement_leader_research/alan-hirsch-baseline-report.md` — it has
  high-confidence counts and constraint analysis.

Use Glob (`docs/movement_leader_research/{slug}/**/*.md`) to see the full tree,
then Read each relevant file. Do not guess at content that is not in the
research. Mark gaps honestly.

## Step 3 — Build the informational inventory

For every category below, list **specific titles with specific locations**
(URL, filesystem path, publisher, platform name). If a category has no
evidence in the research, write `UNKNOWN — needs research` rather than
omitting it.

Required categories (include all, even when empty):

1. **Books** — title, publisher, year, co-authors, where it's actually
   sold/distributed (Amazon, IVP, publisher site), audiobook status
2. **Academic / peer-reviewed work** — dissertations, chapters, journal
   articles, with the journal/publisher name
3. **PDFs & downloadable documents** — whitepapers, Lausanne papers, study
   guides; where they're hosted (if known)
4. **Articles / essays** — platform + title + year; note any that exist only
   as links that may be dead
5. **Blogs / personal writing** — every blog surface they've used
   (Substack, Medium, personal site, guest posts on Forge/Saturate/etc.)
6. **Websites they control or co-own** — personal domain, org sites, legacy
   project sites
7. **Social media** — each account with the handle, platform, approximate
   follower count if known, posting frequency if known
8. **Newsletters / email** — platform (Substack, Mailchimp, ConvertKit), list
   size if known, cadence
9. **Podcasts (hosted)** — shows they own/host, where they publish
10. **Podcasts (guest appearances)** — every named episode/show from the
    research
11. **YouTube / video** — own channel (or absence of one), videos on other
    channels by name
12. **Sermons / teaching audio** — church archives, conference recordings,
    specific series if named
13. **Talks / conference presentations** — conference name, year, topic if
    known
14. **Courses** — seminary, online platform, self-hosted; platform name and
    institution
15. **Assessments / tools** — APEST, diagnostic instruments, apps they've
    built; where they live
16. **Apps / software platforms** — any digital products
17. **Notes / laptop / unpublished** — explicitly label this
    `UNKNOWN — likely substantial, not yet catalogued` unless the research
    says otherwise
18. **Their own head / embodied knowledge** — frameworks that exist primarily
    through speaking, consulting, coaching; 1-on-1 wisdom not yet externalized

For each item where a URL exists in the research, include the URL. For each
that is hinted at but unverified, add `(unverified)`.

## Step 4 — Build the relational inventory

1. **Organizations** — founded, board roles, advisory relationships (with
   org names)
2. **Co-authors and frequent collaborators** — names, which works they
   co-created
3. **Networks / movements** — the communities they are nodes in
   (Forge, Exponential, Lausanne, 100M, etc.)
4. **Seminary / academic affiliations** — institutions, role titles
5. **Mentors and protégés** — if the research names them
6. **Where relationships are stored** — CRM? Personal address book? Mental
   rolodex? Email history? Mark honestly — usually this is the most
   fragmented layer.

## Step 5 — Write the narrative

The file must open with prose that tells *this person's* story, not a
template. Use the specific numbers the research supplies. Good opens look
like:

> Alan Hirsch has written 20 books across 7 publishers over 21 years. More
> than 150,000 people have taken his APEST assessment. And if you try to
> follow his thinking from first book to current frame, you cannot — because
> there is no path. The books live on Amazon. The assessment lives on
> 5qcentral.com with no onward journey. His articles are scattered across
> Saturate, Verge, Exponential, and a static Squarespace at alanhirsch.org.
> His 38+ videos live on 20+ third-party YouTube channels. He does not have
> his own...

Bad opens look like: "Leader X has a significant body of work spread across
multiple channels." Do not write that.

Follow the opening with the informational map, the relational map, and a
one-paragraph synthesis that states explicitly: how retrievable their
knowledge is, what fraction is embodied vs. externalized, what the single
largest pool of "trapped" value is.

## Step 6 — Output

Write the file to
`docs/movement_leader_research/{slug}/fragmentation-story.md`.

Use this heading structure exactly:

```markdown
# {Full Name}: The Fragmentation Story

> Generated {YYYY-MM-DD} by the `fragmentation-story` skill from existing
> research in `docs/movement_leader_research/{slug}/`.

## The Story

{2–4 paragraphs of specific narrative}

## Informational Fragmentation

### Books
### Academic Work
### PDFs & Documents
### Articles
### Blogs & Personal Writing
### Websites
### Social Media
### Newsletters / Email
### Podcasts (Hosted)
### Podcasts (Guest)
### YouTube & Video
### Sermons / Teaching Audio
### Talks / Conferences
### Courses
### Assessments & Tools
### Apps / Software
### Notes, Laptop, Unpublished
### Embodied / In Their Head

## Relational Fragmentation

### Organizations
### Co-authors & Collaborators
### Networks & Movements
### Academic Affiliations
### Mentors, Protégés, Key Relationships
### Where Relationships Are Actually Stored

## Synthesis

{one paragraph}

## Research Provenance

- Source folder: `docs/movement_leader_research/{slug}/`
- Files read: {list the files you actually read}
- Confidence: {one sentence — what's well-evidenced vs. what's thin}
- Gaps requiring further research: {bullet list of the biggest UNKNOWNs}
```

If the user passed multiple leaders, repeat Step 2 through Step 6 for each,
then print a short summary to the user listing each file you wrote.

## Quality Bar

- **Specific, not generic.** Titles, URLs, platforms, handles. If the research
  has them, the story has them.
- **Honest gaps.** `UNKNOWN — needs research` beats a plausible invention.
- **No downstream recommendations.** This skill diagnoses fragmentation; it
  does not prescribe the Movemental platform response. That's a different
  document.
- **Do not recompute from scratch.** The point is to *organize* what's
  already been researched, not to re-scrape. If a category is genuinely
  empty after reading everything, say so.
