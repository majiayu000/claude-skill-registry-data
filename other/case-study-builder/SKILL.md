---
name: case-study-builder
description: Build client case studies through a low-overwhelm, multiple-choice interview plus whatever files the user can dig up — producing web-ready case study copy with a media plan (what images/videos to provide, find, or generate). Use this whenever the user wants a case study, client success story, portfolio write-up, results page, testimonial feature, or says "write up what we did for [client]". Also trigger when the user mentions having clients but no case studies, wants to turn a finished project into marketing proof, or casually says "I should really do a case study for X" — even without the word "case study" (e.g. "I want to show off the work we did for that gym").
---

# Case Study Builder

## Why this skill works the way it does

The person using this skill has plenty of successful client work and zero (or few) written case studies. That gap almost never exists because writing is hard — it exists because *starting* is hard: the facts are scattered across emails, memory, and old files, and a blank page plus twenty open-ended questions is overwhelming. Your entire job is to extract a publishable case study while spending as little of the user's energy as possible. Their attention is the scarcest resource in this process. Every choice below follows from that.

A shipped case study with two clearly-marked placeholders beats a perfect one that never gets finished. Bias hard toward momentum.

## The flow

1. **Figure out where you are.** New case study? Resuming one (look for an existing `*-intake.md` notes file or prior conversation context)? Or a "I have 30 clients and no case studies" cold start? Cold starts go to Batch mode (below) — do not start interviewing about a client that hasn't been picked yet.
2. **Mine what already exists.** Before asking a single question, extract everything you can from files the user provided, things they said in conversation, the client's live website, and any connected tools. Turn findings into pre-filled answers.
3. **Interview** — multiple choice, in short rounds, only about gaps. Rules below.
4. **Draft** the case study using `references/template.md`.
5. **Media plan** — what visuals the page needs, with a provide → find/create → generate fallback for each (also in the template).
6. **Deliver** the case study file plus the intake notes file, and offer the next client while momentum exists.

You don't have to run these strictly in order. If the user brain-dumps enough in their first message, skip straight to drafting and ask only what's missing afterward.

## Interview rules

The user chose multiple-choice questioning on purpose — clicking an answer costs almost nothing; composing a paragraph costs a lot.

- **Use the AskUserQuestion tool** (or your environment's equivalent structured-question tool) whenever it's available. Each question gets 2-4 concrete candidate answers plus the built-in "other" for free-text.
- **Pre-fill the options with your best guesses.** If their notes say calls went up after launch, offer "Roughly doubled", "Up 20-50%", "Not sure — I'd have to check". A good option set means the user mostly confirms rather than recalls. Guessing wrong is fine; making them type is the failure mode.
- **Small rounds.** At most 4 questions per round, then stop. Between rounds, show a one-line progress marker like "That's the hard part done — one more round on results, or say 'write it now' and I'll draft with what we have."
- **The escape hatch is always open.** "Skip", "idk", or "just write it" are all valid answers to everything. When the user says write it now — write it now, with placeholders. Do not sneak in "just one more question."
- **Never re-ask what you already know.** If a file or earlier message answered it, treat it as answered. Re-asking is the fastest way to make this feel like homework.
- **Read `references/question-bank.md`** before the first round. It has the five phases, the priority order (results and challenge matter most), and example option sets. Don't run all five phases if the material is already there.
- **Running unattended** (subagent, scheduled run, or no question tool available): don't stall and don't invent answers. Mine everything available, write the best draft you can with `[NEED: ...]` placeholders, and end with a short list of multiple-choice questions the user can answer whenever they return.

## Files, whenever they show up

The user may hand over files at any point — before, during, or after the interview: email threads, proposal docs, analytics exports, screenshots, invoices, chat logs. When they do, mine them immediately and update the intake notes before asking anything else. In the intake notes, record where each fact came from (e.g. "traffic numbers: GA export client sent 3/12") so claims can be traced later.

## Truth rules

Case studies are marketing, but they're marketing that prospects fact-check. Never invent metrics, quotes, timelines, or client names. Everything in the draft is either (a) from the user, their files, or verifiable sources, or (b) a visible placeholder.

- Distinguish verified numbers from recollection. "Calls roughly doubled" from memory gets written as "roughly doubled" — not "104% increase."
- Quotes must be real. If there's no quote, put a `[QUOTE]` placeholder in the draft and include a ready-to-send quote-request message (template has one) so getting a testimonial takes the user one forward.
- Confirm the client is OK being named before the final version uses their name. If unknown, draft with the name but flag it, and offer the anonymized variant ("a family-owned plumbing company in Houston").

## Who the case study is for

It's written for a prospect standing in the same shoes the client stood in — not for the user's ego. That means: open with a situation the prospect will recognize as their own, use the client's industry language rather than agency jargon, make results concrete enough to covet, and let the story carry the numbers. The reader's takeaway should be "this could be me," not "this company is impressive." Both the hard numbers *and* the narrative matter — numbers make it credible, story makes it feel possible.

## Drafting and output

Read `references/template.md` before writing the draft. Deliver two files, and actually send them to the user (SendUserFile or equivalent) rather than just describing them:

- `<client-slug>-case-study.md` — the web-ready copy, including the media plan section.
- `<client-slug>-intake.md` — the accumulated facts, sources, unanswered questions, and permissions status. This is the resume point: if the session ends mid-way, this file is how the next session picks up without re-asking anything.

## Batch mode ("I have a ton of clients")

When the user has a backlog and doesn't know where to start, the enemy is trying to do all of them. Run a quick triage instead: ask for a rough client list (or pull one from connected tools), then for each ask two things at most — how good is the story, and how reachable are the facts. Present a short ranked table and recommend ONE to start with: the best story-to-effort ratio, not necessarily the biggest client. Then run the normal flow on that one. When it ships, offer the next. One published case study creates the momentum thirty planned ones never will.
