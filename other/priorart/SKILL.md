---
name: priorart
description: >-
  Prior-art check before you build — does this idea already exist? Takes a
  project/tool/library idea, reframes it in the vocabularies different
  communities would use, searches where builders publish (code registries,
  Show HN, arXiv), traces each match one dependency-layer down to the real
  incumbent, and returns a locator-backed landscape plus exactly one
  verdict: Build / Fork X / Contribute to Y / Use Z / Investigate first.
  Checked ideas persist in out/priorart/checked.md, so re-checking one opens
  with what changed. Keyless. Use for "does something like X already
  exist", "has anyone built this", "am I reinventing the wheel", "check
  prior art before I build" — e.g. "/priorart <idea>". For your existing
  project vs its peers use scout; for choosing between named options use
  verdict.
---

# priorart — who built this before me?

`/priorart <idea>` — check whether the idea already exists
`/priorart` — list ideas already checked (from `out/priorart/checked.md`)

Answer one question: **has someone already built this — and what does that
mean for whether you should?** The deliverable is one honest verdict with
the landscape as its evidence, not a survey. Advisory throughout: it
recommends; the human decides what, if anything, gets built.

## Step 0 — Check the memory

Read `out/priorart/checked.md` if it exists. If this idea (or a close
variant) was checked before, open with **"Since last check"**: re-verify
the previous brief's findings (status changes, new arrivals since that
date) instead of redoing the whole search. The pipeline below is for ideas
not yet in the log.

## Step 1 — Restate before searching

Restate the idea in one sentence — what it does, who it's for, and the
constraint that makes it distinctive — and confirm it with the user. Too
vague to restate → ask exactly **one** clarifying question, offering at
most 3 example dimensions (it's a question, not a questionnaire).

## Step 2 — Vocabulary before queries

Before any search, write 6–10 framings of the idea from distinct vantage
points: the builder's terms, the end-user's terms, the academic field's
terms, the infrastructure/implementation terms, and the adjacent
discipline that likely solved this first. Map each planned query to a
framing — this is what prevents five queries landing in the same semantic
neighborhood and calling it coverage. Most "novel" ideas are existing
ideas under a different name; the framings are where that name gets found.

## Step 3 — Search where builders publish

Budget: **≤10 queries for the whole check, with 1–2 held back for Step 4's
lead-tracing.** Fan out 2–3 sub-agents grouped by venue class, each briefed
with 2–3 framings and an explicit share of the rest (say the numbers; agents
without a stated allowance keep searching). Together the briefs cover every
vantage point from Step 2 — framings left out of every brief defeat the
point of writing them:

- **Registries & code** — GitHub/GitLab search, PyPI, npm, crates.io,
  Hugging Face for ML.
- **Products & launches** — Show HN, Product Hunt, the subreddits where the
  target users live. Product venues matter because the incumbent may be
  closed-source; this stays a builder's check — market sizing and
  business-model analysis are a different job and out of scope.
- **Writing** — arXiv/Scholar for academic framings, engineering blogs.
  When the domain has a high-signal venue where serious players cite the
  incumbent (model cards, RFCs, regulator guidance), check it over generic
  search.

Every finding returns with a **locator**: the URL plus a fetched signal —
last-commit/push date, downloads, release date. A signal that couldn't be
fetched is reported as "unknown", never asserted; one repo with real usage
beats any listicle.

## Step 4 — Trace one layer down

Read what each direct match is built on: "wraps X", "built on top of W",
"official harness for Z" are leads, not background — follow each with a
dedicated query. This check fails most often not at finding projects but at
stopping one layer too early and crowning a thin wrapper the incumbent.
Stop early only when the landscape is clear after 3–4 queries AND at least
one of them followed such a lead; at the cap without confidence, say so
plainly and report what was found.

## Step 5 — The landscape

Cluster findings into four buckets, **max 3 rows each** — curation, not a
dump: **direct matches** · **adjacent solutions** · **partial solutions** ·
**abandoned attempts** (note when each died and, where findable, why). Each
row: Name | Link | Status | Relevance, where the Status cell quotes its
fetched locator ("last commit 2026-05", "1.2k dl/mo") or says "unknown" —
liveness is looked up, never assumed. Found nothing for a bucket? Leave it
empty and say so; **never invent a competitor** — "no direct prior art
found, searched: <where>" is a valid, useful result. But treat a clean
landscape from same-neighborhood queries as a local minimum, not a green
light: three queries returning the same project means a semantic cluster
was searched, not the space — vary the framing before believing the blank.

Then extract the **standard patterns** across matches (common architecture,
libraries, naming, pricing): the default playbook the user would be
competing with or building on. Close with one honest **differentiator
paragraph**: name the real differentiator, or say plainly there isn't one —
manufactured novelty costs the user their next quarter.

## Step 6 — One verdict, then the record

State exactly one of these in the verdict section's heading itself —
`## Verdict: <one of the five>` — no hedging (nuance goes after the
verdict, not instead of it):

- **Build it** — genuine gap, and the differentiator is real.
- **Fork X** — the right base exists but has diverged from the need.
- **Contribute to Y** — the delta is a feature, not a project.
- **Use Z** — it exists; wanting to have built it isn't a reason to build it.
- **Investigate first** — prior art is dead or ambiguous: name exactly what
  to read (usually the corpse's issue tracker) before writing a line of code.

Follow with the one concrete next step. Render the brief in chat per
`references/brief-template.md` (read it at this step), save it to
`out/priorart/<idea-slug>-<YYYY-MM-DD>.md` (date via `date +%F`, never
guessed; create the folder if needed), and append one line to
`out/priorart/checked.md` — the memory Step 0 reads. Committing either is
the user's call.
