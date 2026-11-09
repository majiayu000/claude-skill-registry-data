---
name: browser-relay-verification
description: >
  Apply before calling WebFetch or WebSearch for any claim that needs an
  external source - legal, compliance, technical/API, library, market, or
  pricing facts alike. In this project, external verification is done by
  the user's browser, not by Claude directly. Follow the steps below in
  order for every case; there is no subject-matter carve-out.
---

# Browser Relay Verification

Follow these steps in order. Branch only on documented precedent, never on
confidence in a source.

## Step 1 - Citation already in hand?

- Yes: open it directly. Confirming a quote from an already-cited,
  official-docs URL is not primary research. No hand-off.
- No: continue to Step 2.

## Step 2 - Documented precedent?

Precedent = written down in this repo already: a prior research doc,
status note, or session finding recording that this exact domain fetched
cleanly from this environment.

- No precedent: skip to Step 4. Never attempt the fetch to test it.
- Precedent exists: continue to Step 3.

## Step 3 - One attempt

Make one direct WebFetch/WebSearch call against that source.

- Succeeds: use it. Done.
- Fails: stop. Never retry with a different URL, mirror, secondary source,
  or search engine. Go to Step 4.

## Step 4 - Hand off

Hand off to the user, not a subagent. Write a self-contained prompt. Include:

1. Background: the project, the decision or constraint at stake, why the
   question matters.
2. The specific question(s), narrow enough to answer with sources.
3. A hard requirement, worded as an instruction: open every source
   yourself and confirm it says what you're citing before citing it.
   Never cite a search snippet or a page you have not personally opened.
   Anything not opened and confirmed goes in the unverified section, not
   the claims section.
4. The required response shape: per claim, the source name/URL/date and
   the exact quote it supports. A separate section for everything
   rejected or left unverified.

## Step 5 - Accept or re-chase

- Reply shows the source was opened and the quote matches: keep it.
- Reply cites without showing it was opened: reject it - the instruction
  was explicit. Return to Step 4 for that claim alone.

## Step 6 - "Not verified" flags

Triage each item the reply's own unverified section listed (Step 4):

- Material (changes the conclusion): return to Step 4 for that gap only.
- Non-material, concrete (a specific, chaseable claim): log as an open gap.
- Non-material, vague ("couldn't verify," nothing to chase): drop it.
