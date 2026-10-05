---
name: information-architecture
description: >
  Use when deciding how content and pages are ORGANIZED so the right message
  reaches the right audience — site maps and page inventories, what each page's
  job is, where a message/section/feature should live, navigation and funnel
  structure, heading-level scannability, and audits for buried or orphaned key
  messages. Applies to any structured content, not only websites: docs, books,
  curricula and long papers are the same discipline. Invoke on questions like
  "where should this content live", "does the home page need X", "users can't
  find Y", when defining an audience or a thesis, when outlining before
  writing, when adding/removing/reordering a page or section, and as a required
  lens on any content-page review. Scope is STRUCTURE and placement of content
  ONLY — visual/aesthetic judgment is design-guide; component/state/data
  structure is frontend; broad UI polish is impeccable; sentence-level voice and
  wording are academic-writing (scholarly) or plain-language (non-technical);
  and grant proposals take their structure from grant-writing, which owns
  funder-mandated section order. Those often co-apply; this skill decides what
  goes where and why.
---

# Information Architecture

Goal: make sure every message the owner cares about has a findable, first-class
home — and that each page does one clear job in a deliberate structure — for a
user who scans, not reads.

## Before structure: audience, then thesis

IA is medium-agnostic — a site, a book, a curriculum, a technical paper and a
legal argument are one discipline. Writing is another form of information
architecture, and it is the same skill that builds a website. That makes the
writing skills partners rather than rivals: IA settles what the sections are,
what order they run in and what each has to prove, then academic-writing or
plain-language decides how the sentences inside them sound. Reach for both on
any prose deliverable. Whatever the medium, two questions come before any
structural decision:

1. **Who is the audience, and what do they need from you?** Not who you want to
   talk about — who is on the other end, and what they came for. Everything
   below is downstream of this answer.
2. **What is the thesis — the whole project in one sentence?** One level above
   the per-page jobs. It stays high level and withholds the detail; its work is
   to point the reader at what's coming. A complicated subject earns a
   complicated sentence, but it still has to be one sentence.

**Audience expertise sets the shape.** Treat "knows nothing", "knows a little"
and "knows a lot" as three different audiences, because they need three
different structures. Serving all three at once forces an explicit choice:
pitch low-to-medium, or give advanced readers their own wing — and if it's a
wing, decide whether it belongs inside this property or is a separate one. The
more diverse the audience, the harder the job; don't let that decision stay
implicit.

**Audience is researched, not assumed.** On client work, interview the client
extensively about who they *actually* want to reach. Interview subject-matter
experts for the content itself. Being highly skilled at building the thing is
not the same as knowing its subject or its users — and when the subject is
outside your expertise, you still have to go deep into it before you can
structure it.

## Core principles

1. **Users scan headings, not paragraphs.** A message that exists only inside a
   paragraph is invisible at the IA level. Anything strategically important —
   a differentiator, an offer, a proof point — needs a first-class, scannable
   presence: its own section, heading, list item, or card. "It's mentioned in
   the bio" does not count as placed. Readers also move *non-linearly*: they
   read the opening, jump to the end, then dip back into whichever middle
   sections look relevant. Structure is what makes that possible — and when it's
   missing, the reader "just starts wandering around, because the author was
   wandering around." Your disorganization becomes theirs.
2. **Every page has one job.** State it in one sentence ("Home: convert a
   cold visitor into someone who explores Solutions or Process"). Content that
   doesn't serve the page's job belongs on another page — linked, not copied.
3. **Key messages follow the visitor's path, not the author's files.** Ask
   "what does a first-time visitor see in their first 30 seconds, in order?"
   The most differentiating message must appear on the entry pages (home,
   landing), not only on the deep page that explains it fully.
4. **Summary → detail, linked.** The full story lives on exactly one page; the
   other pages carry a short, scannable teaser that funnels to it with an
   explicit CTA. Duplicated full explanations drift apart; orphaned detail
   pages never get visited.
5. **Funnels are explicit.** Each page names its next step (a CTA, not just
   nav). If you can't say where a page sends its reader next, the page is a
   dead end.
6. **Navigation mirrors the mental model.** Labels use the visitor's words,
   not internal jargon; groupings match how visitors think about the problem,
   not how the codebase is organized.
7. **Structure changes are content decisions first.** Decide placement and
   hierarchy in prose (what, where, why) before touching markup; then let the
   design/frontend skills own how it looks and how it's built.
8. **Outline before prose.** Never start writing — or building pages — and let
   the structure emerge behind you. Put the whole structure in place first:
   thesis → the discrete chunks that support it → conclusion. The reliable shape
   is an argument: state the claim, then the first piece of evidence, the
   second, the third, and then show that all of them arrive at the same
   conclusion. Every project supports its thesis differently; the outline is
   where you work out how this one does.
9. **The opening and the closing carry the most weight.** An entry page *is* the
   introduction: after reading it a first-time visitor should know exactly what
   this is about, and be able to either go deeper or stop there satisfied. Size
   it to the medium — the first page of a site, the first chapter of a book, the
   first two pages of a twenty-page paper.
10. **Keywords carry through.** Fix the handful of terms the project owns and use
    them consistently from the entry page down into every subsection, in one
    writing voice. Consistent vocabulary is what makes a set of pages read as a
    single argument rather than several separate ones.

## IA review checklist

Run this on any content page addition/change, and as a periodic audit:

- **Audience check:** can you name the audience and what they need? Where it
  spans expertise levels, has the pitch-low-to-medium vs. separate-wing decision
  actually been made and written down — and if it's a wing, same-property or
  separate?
- **Thesis check:** is there one sentence for the whole project, above the
  per-page jobs? Does each top-level section visibly support it?
- **Page-job check:** can you state each affected page's job in one sentence?
  Does every section on it serve that job?
- **Buried-message scan:** list the owner's top 3–5 messages (differentiators,
  proof, offer). For each: on which pages does it appear *at heading/section
  level*? A key message living only in body prose on entry pages = gap.
- **Heading-only read:** read just the headings of the page top to bottom. Does
  the story still make sense? Would a scanner know the key message exists?
- **Funnel check:** does each page have an explicit next-step CTA? Does the
  entry-page teaser link to the detail page that carries the full story?
- **Orphan check:** is any page/section unreachable except by URL, or reachable
  only from one buried link?
- **Duplication check:** is any full explanation living on two pages? Collapse
  to summary→detail.
- **Opening check:** after only the entry page or introduction, could a
  first-time visitor say what this is and decide whether to go deeper?
- **Vocabulary check:** do the project's key terms recur consistently across
  sections in one voice, or does each page invent its own words?
- **Nav check:** do labels match visitor vocabulary? Is anything important
  missing from nav, or anything in nav that no longer earns the slot?

## Working method

- Write the outline first and treat it as the thing to agree on: thesis, section
  order, and what each section is there to prove. Structure gets reviewed before
  prose or markup exists — that is the cheapest moment to move a section.
- Research the audience instead of assuming it. Interview the client about who
  they actually want to reach; interview subject-matter experts for the content.
  Record the answers, because every later placement argument appeals to them.
- Resist the narrative hook outside narrative work. Opening on a compelling
  out-of-sequence moment is a fiction device (a memoir can open on an event that
  happens much later, then jump back); for sites, docs and technical writing, go
  straight — the overall first, then the first point, the second, the third.
- Before proposing changes, build (or update) a one-screen page inventory:
  page → job → sections (heading level) → CTAs → what links here. Diff the
  owner's key-message list against it; the gaps are the work.
- Propose placement as: message → page → position (between which sections) →
  treatment (section/list/card/CTA) → why there. Get the placement decision
  locked before implementation starts.
- Prefer the smallest structural change that makes the message scannable —
  a new section with an existing visual idiom beats a redesign.
- Record project-specific IA decisions (page jobs, section order rationale,
  key-message map) in the project's own docs so later sessions don't re-derive
  or accidentally undo them.

Per-lesson history lives in `LEARNINGS.md` beside this skill, when your copy keeps one.

## Related skills

- [planning](../planning/SKILL.md): a placement decision is a plan-time decision; it belongs in the plan's single question round.
- [research-methods](../research-methods/SKILL.md): long papers and institutional documents (definitions up front, a roles-and-responsibilities spine) take their structure from here.
- [data-analytics](../data-analytics/SKILL.md): that skill decides which metrics a dashboard shows; this one decides where the dashboard and each figure sit.
