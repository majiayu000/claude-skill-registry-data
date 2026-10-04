---
name: factcheck
description: >-
  Adversarial citation and claim audit for any document — "do these sources
  actually say what the text claims?" Takes a markdown file, URL, or pasted
  draft (including this repo's own pulse/verdict briefs), extracts every
  checkable claim, then fans out verifier sub-agents instructed to refute,
  not confirm: does the cited link resolve AND assert the claim as stated,
  is the source primary or a laundered secondary write-up, has the claim
  gone stale. Emits a graded audit table — VERIFIED / MISATTRIBUTED /
  UNSUPPORTED / STALE / UNCHECKABLE — with a quoted passage as evidence for
  every grade, saved to out/factcheck/. Advisory: it grades, the human
  edits. Use when the user wants to check citations, verify sources, or
  audit a report, post, or brief — e.g. "/factcheck <doc>", "verify the
  sources in this", "are these citations real?", "is this actually true?".
  For researching a fresh topic use pulse; for judging code changes use
  done.
---

# factcheck — do the sources say that?

`/factcheck <path | URL>` — audit a document's claims against its sources
`/factcheck <path> focus <section/topic>` — audit only part of a long document

Answer one question: **for each claim this document makes, is there a source
that actually asserts it?** The documented failure mode of cited writing —
human and agent alike — is not missing links; it's links that resolve to
pages that *don't say that*. A working URL is the weakest form of evidence
there is. This audit replaces "it has citations" with "here is the passage."

## Step 0 — Scope the audit

Read the document (WebFetch if a URL; ask for a paste if it's paywalled).
Then size the job and say which tier you picked:

- **Small** (≤ ~10 checkable claims): verify inline, no sub-agents — the
  fan-out below would cost more than it saves.
- **Standard**: fan out, batching ~5–8 claims per verifier.
- **Focused**: the user named a section or topic → extract only there, note
  in the audit header that the rest was not examined.

If the document has **no citations at all**, say so up front — the audit's
question shifts from "does the cited source say this" to "does support for
this exist anywhere", and UNSUPPORTED becomes the default grade to beat.

## Step 1 — Extract the checkable claims

Walk the document and number every **checkable claim**: factual, specific,
and in principle verifiable — statistics, quotes, "X said/announced Y",
version numbers, benchmark results, historical facts, "studies show".

For each claim record: a short restatement, its **locator** (section
heading or line), the **cited source** if any, and whether it's
**date-sensitive** (anything with "currently", "latest", a version, or a
number that drifts).

Skip pure opinion and analysis — but flag **opinion dressed as fact**
("it is widely known that...") as a finding in its own right, ungraded.

## Step 2 — Adversarial verification (fan out)

Spawn verifier sub-agents (`subagent_type: "Explore"`), each with a batch
of claims and the same standing instruction: **try to refute each claim,
not confirm it** — a verifier hunting for agreement finds it whether it
exists or not. Per claim:

1. **Fetch the cited source.** Find the exact passage that supports or
   contradicts the claim — and **quote it verbatim**. No passage, no
   verification, regardless of how relevant the page looks.
2. **Trace laundered sources.** If the citation is a secondary write-up (a
   blog post about a paper, a news story about an announcement), follow it
   to the source that *owns* the claim — the paper, the changelog, the
   transcript. Grade against the owner; note the laundering.
3. **Check the date.** For date-sensitive claims, one search pass for
   newer, superseding evidence — a claim can be faithfully cited and still
   be wrong today.
4. **Uncited claims:** one honest search for a supporting primary source.
   Found → grade normally and record the found source. Not found →
   UNSUPPORTED, with the search noted.

**Grades** (exactly one per claim):

| Grade | Meaning |
|---|---|
| **VERIFIED** | The source asserts the claim as stated — passage quoted. |
| **MISATTRIBUTED** | The source is real but says something materially different — both versions quoted. |
| **UNSUPPORTED** | Link dead, source nonexistent, or no source found that asserts it. |
| **STALE** | Was true when written; superseded — the newer evidence quoted and dated. |
| **UNCHECKABLE** | Paywalled, offline, or genuinely unverifiable — stated, never guessed around. |

**Lossless hand-off:** each verifier writes full findings (quotes, URLs,
search trails) to `out/factcheck/.work/<batch>.md` and returns a compact
summary; build the audit from the files, not the summaries — a quote
flattened by a relay is no longer evidence.

## Step 3 — The audit

Render in chat, then save. Findings first, worst first:

```markdown
# Factcheck: <document title> — <YYYY-MM-DD>

**Document:** <path/URL> · **Claims examined:** N (of M total; scope note if focused)
**Score:** X VERIFIED · X MISATTRIBUTED · X UNSUPPORTED · X STALE · X UNCHECKABLE

## Findings that matter most
1–3 sentences: the riskiest problems (misattributions and unsupported
central claims outrank stale trivia), any laundering pattern, any cluster.

## Claim-by-claim
| # | Claim | Locator | Cited source | Grade | Evidence |
|---|---|---|---|---|---|
(evidence column = the quoted passage or the reason, always)

## Laundered sources
citation → owning source, per case (omit section if none)

## Date-sensitive claims
what to re-check and when (omit if none)
```

Save to `out/factcheck/<slug>-<YYYY-MM-DD>.md` (`<slug>` from the document
title; date via `date +%F` — never guessed). Create the folder if needed;
committing the audit is the user's call. Then **offer** — never do unasked —
the follow-ups:
annotate the original with inline flags, or draft corrected text for the
failing claims.

## Guardrails

- **A resolving link proves nothing.** Verification is a quoted passage or
  it didn't happen.
- **Refute-first.** Every verifier hunts for the disconfirming reading;
  when a grade is genuinely arguable, take the lower one and say why.
- **Primary sources own claims.** A write-up of a paper is not the paper;
  grade against the owner.
- **Unknowns stay UNCHECKABLE.** Never guessed, averaged, or rounded up to
  VERIFIED — an honest "couldn't check" is a finding, not a failure.
- **Advisory, not editorial.** The audit grades; the human decides what to
  do about it. Never edit the audited document without being asked.
- **This repo's outputs are fair game.** Auditing a pulse or verdict brief
  with fresh-context verifiers is the intended use, not an insult — the
  writer of a claim is the worst-placed agent to check it.
