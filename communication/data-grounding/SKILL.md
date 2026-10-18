---
name: data-grounding
description: Ground-truth checks that run BEFORE any conclusion is drawn from a dataset — a message export, mail archive, chat.db, review window, or log trawl. Use when analyzing, summarizing, or reviewing such data; enumerate channels, state scope and denominators, verify corpus retrieval, and treat conversation text as speech acts, not events.
---

# Data Grounding

Moved verbatim from the root `CLAUDE.md` (2026-10-16) so it loads only when a dataset is being analyzed. Case histories behind every rule: [`docs/data-grounding-precedents.md`](../../../docs/data-grounding-precedents.md).

Before drawing ANY conclusion from a dataset — a message export, a mail archive, a review window,
a log trawl — establish the ground truth of the *input* first (case histories behind every rule
here: [`docs/data-grounding-precedents.md`](docs/data-grounding-precedents.md)):

- **Enumerate the CHANNELS before analyzing any one of them.** A missing channel does not widen
  the error bars — it **inverts the conclusion's sign**. Before concluding anything about an
  interaction, a relationship, or a sequence of events, list every channel that could carry it
  (text messages, voice/video calls, a second messaging app, email, transfers, in-person) and
  state in the output which you queried and which you did not (precedent P1). **No scope,
  window, or count check catches this**, because every count *within* the queried channel was
  correct — which is why channel enumeration precedes all of them.
- **State the scope up front, in the output**: the exact date/window boundaries, the direction of
  the records (sent AND received? one side only?), any export filters, and the **total record
  count** — before the first conclusion, so a scope error surfaces immediately.
- **Window = the last human review point, never the last automated run.** An automation's
  timestamp is not evidence a human saw anything.
- **Suspicious-count self-check**: if a count looks too low or too high against the requester's
  stated expectation or the surrounding evidence, treat that as a data-scope bug in YOUR input
  until proven otherwise — re-derive it by a second independent method before presenting.
- **When a file could be a queue or a record, assume RECORD** — verify live sent-state/channel
  state before acting on a file's title or presence.
- **A conversation corpus records SPEECH ACTS, not EVENTS.** "I sent you $150" is evidence that a
  sentence was typed. Ideas floated, contracts drafted, plans proposed, dates agreed and amounts
  negotiated are *conversation* — most are never executed. A claim of the form "X happened"
  sourced only from message text is **asserted-in-conversation**, never **occurred**, unless a
  NON-conversational channel corroborates it: commits, transactions, calendar, filesystem
  artifacts, or the operator. Mark the distinction in the output (precedent P2).
- **A window is not the corpus — never state a sample's finding in the corpus's language.** Report
  the denominator you actually read, next to the denominator that exists, every time. The failure
  is silent and it scales (precedent P3). If the
  full extent is unknown, that is itself the first finding — establish it before analyzing.
- **Corpus retrieval fails silently and looks like absence.** Before concluding a corpus holds
  nothing about a subject, verify the resolver reached a real store: `python3
  scripts/corpus_resolve.py` must name a populated home. The estate has now twice reported "no
  populated corpus" with hundreds of MB on disk (registry header, and again 2026-07-31 from a
  relocated store) — "I found nothing" and "I read nothing" are indistinguishable in the output.
- **On a "since we last reviewed" ask, the PRIOR SESSIONS are one of the channels — and their
  findings live in the assistant's prose, not in their tool results.** Reconstructing the watermark
  from the earlier session's *user prompts* is under-reading it. (2026-08-07: a Charles review did
  exactly that, then reported "Instagram was never read — no export on disk." It had been read, live
  via the Chrome bridge, in that same prior session; the four-phase relationship arc, the lifetime
  money total, and a decisive verbatim exchange were all already established there and had to be
  recovered from the transcript after the operator said "a lot happened in the previous sessions.")
  Browser-read evidence leaves **no artifact on disk** — it survives as screenshots, so grep the
  assistant `text` blocks. Absence of a file is not absence of a reading. Locate the prior work
  (`grep -rli <subject> .agent-runtime/*/projects/*/*.jsonl`), inherit its findings **with
  provenance**, then state only what is new — and write the result to a durable artifact so the next
  session never pays this cost again.
- **A binary or attachment-backed event is invisible to a text dump, and reads as "it didn't
  happen."** Rendering a thread by its text column silently drops every non-text event. (2026-08-07,
  same review: two Apple Cash transfers rendered as `[media]` placeholders and were reported as "no
  money moved in this window" — they had moved, mid-call, six days after the operator said "dont ask
  me for money ever again," which was the single most load-bearing fact in the window.) In
  `chat.db`, payments are `message.balloon_bundle_id LIKE '%PeerPayment%'` with the amount inside
  `payload_data`; enumerate the distinct `balloon_bundle_id` values before trusting any dump, and
  never conclude "no X occurred" from a channel rendered in one modality.
