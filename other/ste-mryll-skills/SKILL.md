---
name: ste
version: 1.4.0
description: "Write, rewrite, translate, or check content in Simplified Technical English (ASD-STE100), with four compliance levels (verified / marked / clean / raw) backed by the official dictionary and a checker script. Explicit invocation only: run this skill ONLY when the user types /ste or explicitly asks for the ste skill by name. NEVER auto-invoke it on mentions of STE, STE100, ASD-STE100, Simplified Technical English, or controlled language, and NEVER on a request to answer or write in ASD-STE100 - that is a request about tone, not a request to run this skill."
disable-model-invocation: true
---

# STE — Simplified Technical English (ASD-STE100)

STE is a controlled language: ~53 writing rules plus a dictionary of 875
approved words where each word has exactly one meaning per part of speech.
Dictionary compliance CANNOT come from memory — words you would swear are
approved ("qualified", "ensure", "should") are not. Only the Verified level
below claims compliance, and every claim in it comes from the checker script,
not from intuition.

STE is defined for English only. The STE text is always written in English
first. If the user asked in another language or asks for a translation, you
translate FROM the STE English as a second pass — never draft directly in the
other language.

The source can be anything: a document, a merge-request description, a
procedure — or something just discussed in the conversation that the user
wants again in STE. The workflow is the same; for conversational
re-explanations the cheap levels (Marked, Clean) are usually the right
default to offer first.

## Step 1 — Choose the compliance level and output language (before anything else)

Ask both in ONE interaction (AskUserQuestion where the harness has it, a
plain question otherwise) — but ask only what the request leaves open:

- **Level**: if the request names one, use it silently. A request that
  semantically asks for compliance ("does this comply with ASD-STE100?",
  "quiero STE estricto") selects Verified automatically.
- **Output language**: if the request names a language, asks for a
  translation, or was written in a non-English language (which implies
  English + that language), use that silently. The choice is "English only"
  or "English + <language>" — never translation-only: the STE English IS the
  deliverable, and the target language never changes Step 3 (drafting is
  always English; translation is always the second pass).

The levels:

- **Verified STE** — full dictionary compliance. Costs the most tokens:
  replacements, TN/TV judgment, fix passes, and the manual checklist.
- **Marked draft** — STE-style draft with every unresolved word tagged so the
  reader sees what a verified pass would resolve. Not verified.
- **Clean draft** — STE-style draft, no marks. The TN/TV annotation work
  primes richer domain detail (measured: ~15% more content than Raw, at the
  price of slightly weaker general vocabulary and ~40% more tokens).
  Annotations are validated and stripped by `--clean`. Not verified.
- **Raw draft** — STE style from model training only. No annotations, no
  dictionary, no checker, no marks, zero tool calls. The cheapest and
  fastest level; also the shortest, least detailed output.

Clean skips Step 2 (the `--clean` mode reads no dictionary). Raw skips
Steps 2 through 5 entirely — write and deliver. If the dictionary cannot be
downloaded, only Clean or Raw are possible: say so, and the note must say
"not verified (dictionary unavailable)" with no flagged-word count.

## Step 2 — Get the official dictionary (cached; Verified and Marked only)

```bash
C="${XDG_CACHE_HOME:-$HOME/.cache}/asd-ste100"
if [ ! -s "$C/ste100.txt" ]; then
  mkdir -p "$C"
  curl -sL --fail -o "$C/spec.pdf" "https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf"
  pdftotext -layout "$C/spec.pdf" "$C/ste100.txt"
fi
```

`-layout` is required — the checker parses the dictionary columns and
validates the cache structurally (Issue 9 marker, dictionary boundary,
exactly 875 approved entries). A wrong cache is a controlled error with
regeneration instructions, never silent misclassification. `pdftotext` comes
with poppler; the checker requires `gawk`.

## Step 3 — Draft in STE English, annotating TN/TV as you write

Draft from what you already know of the STE rules — do not read
`references/rules.md` first; read it only when you are not sure about a
specific rule. Shapes by text type: procedural — max 20 words per sentence,
imperative; descriptive — max 25 words, no imperative, max 6 sentences per
paragraph; safety instruction — WARNING (injury) or CAUTION (damage), then
command or condition, then consequence.

While drafting (all levels except Raw), annotate every word you use as a
technical noun or technical verb (rules 1.5 / 1.12) the moment you write it:

- Single word: `webhook~tn` or with its category `webhook~tn19`
- Technical verb: `reboot~tv2`
- Multi-word: `[[tn6: pressure relief valve]]`

The annotation moves the TN/TV judgment to the moment it is free and feeds
the compliance-note inventory. The checker validates syntax, category code,
and dictionary relationship; the semantic category membership is your
judgment. Categories can be omitted while drafting (`~tn`) — the checker
prints the numbered category list when any are missing, and the Verified
label is forbidden while any declared word lacks a category.

## Step 4 — Run the checker (one call per pass)

```bash
scripts/ste-check.sh --annotated --verified draft.md
scripts/ste-check.sh --annotated --marked draft.md
scripts/ste-check.sh --clean draft.md      # implies --annotated
scripts/ste-check.sh --entry <word>        # full dictionary entry lookup
```

Always pass `--annotated` for drafts you wrote (your drafts carry TN/TV
annotations); never pass it when checking third-party text.

Exit codes: 0 automated checks clean, 1 findings remain, 2 invocation/cache
failure. One run classifies every word (NOT APPROVED with extracted
alternatives per part of speech, NO ENTRY, DECLARED TN/TV inventory,
CATEGORY REQUIRED, REVIEW, CONTRACTIONS, IDENTIFIER REVIEW) and runs the
mechanical checks (semicolons, sentence and paragraph limits with line
numbers, "-ing" warnings, parenthetical sentences). `--marked` also emits
`<draft>.marked.md` with every unresolved word tagged. `--verified` prints
the manual rule checklist.

## Step 5 — Resolve (Verified only; max 3 total checker passes)

- NOT APPROVED → replace with the extracted alternative. The extraction is
  mechanical: when it does not fit your meaning or part of speech, read the
  entry first with `--entry <word>`. A lowercase word CAN stay if the context
  makes it a technical noun or technical verb (rules 1.6 / 1.12) — annotate
  it and justify it in the note; replacement is the default, TN/TV the
  documented exception.
- NO ENTRY → annotate as TN/TV with a category, or rewrite without the word.
- REVIEW / CATEGORY REQUIRED / CONTRACTIONS / IDENTIFIER REVIEW / mechanical
  findings → resolve each one.
- Rerun the checker after fixing. "Automated checks clean" is not the end:
  complete the printed MANUAL CHECKLIST before applying the Verified label.
- If findings remain after the third checker pass, the deliverable is NOT
  Verified: deliver the marked artifact with a "verification incomplete"
  note.

## Step 6 — Deliver

1. The STE English text (verified, marked, or clean).
2. The translation, if the user asked in another language or requested one:
   sentence by sentence from the STE English, same source term → same target
   term everywhere, conditions before commands, warnings keep the risk word →
   command → consequence shape. Formal STE compliance exists only for the
   English text — say so.
3. The compliance note.

## Compliance note (required)

Verified deliverables end with exactly these three items:

- **TN/TV**: every declared technical noun/verb with its category number and
  name — taken from the checker's DECLARED inventory plus any justified
  REVIEW words (e.g., "residual current device — TN, category 6, systems and
  components").
- **Replaced**: unapproved words from the source or draft and what replaced
  each one (e.g., "qualified → APPROVED").
- **Unverified**: words that could not be checked — or "none".

The other levels end with one line instead:

- Marked: the level and the checker's flagged count (e.g., "Draft level:
  marked — 7 words flagged by ste-check; not dictionary-verified STE").
- Clean: "Draft level: clean — annotations validated and stripped; the
  dictionary was not read." (`--clean` classifies nothing, so there is no
  flagged count to report.)
- Raw: "Draft level: raw — model training only; nothing was checked."

A marked, clean, or raw draft must never present itself as STE-compliant,
and "all vocabulary is approved" without a checker run behind it is never
written.

## Economy mode (optional)

If the harness supports delegating to a subagent with a cheaper model tier —
or an `ste-writer` agent type is available — you MAY delegate Steps 3–5 to
it and only relay its deliverable and compliance note. The checker keeps the
quality floor deterministic, so a cheaper drafting model is safe: its
vocabulary errors are caught mechanically, and its judgment calls surface in
the compliance note. Never delegate the level choice (Step 1).

## Common mistakes

- Asserting compliance from memory. "qualified" is not approved (use
  APPROVED); "display" is approved as a noun but not as a verb; "should" is
  not approved (MUST, or IF for conditions). Run the checker first, claim
  after.
- Trusting an extracted alternative blindly when it does not fit the
  sentence — the columns are parsed mechanically; `--entry` shows the full
  entry with meanings and examples.
- Treating a Marked, Clean, or Raw draft as STE. Only Verified — automated checks
  clean AND manual checklist completed — may claim compliance.
- Keeping a 4+ word noun cluster. Rule 2.2: write it in full once, then
  hyphenate the unit ("pressure-relief valve") or give a shorter form.
- Using Issue 8 terminology: "technical name" no longer exists — Issue 9
  says technical noun / technical verb.
- Drafting directly in Spanish (or any non-English language). The dictionary
  only exists for English — draft in STE English, verify, then translate.
