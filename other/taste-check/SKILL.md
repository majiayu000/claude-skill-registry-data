---
name: taste-check
description: >-
  Review content quality before anything is shown or sent (vault notes, outgoing drafts, dedup
  merges, service files) and return an explicit pass, fail or manual-review verdict. The
  counterpart of a post-build test gate: that one asks whether the build works, this one whether
  the writing is fit to show. Triggers: "/taste-check <path|text>", "/taste", "check this note".
license: MIT
---

# /taste-check — the taste gate for content

The gate is **a kill switch, not a checkbox**. Three outcomes, each with an owner and a consequence:

| Outcome | Criterion | Consequence |
|---|---|---|
| ❌ **FAIL** | at least one ⛔ principle is violated | the artifact is NOT shown as ready; return it to the author with the list of violations |
| ⚠️ **MANUAL** | the ⛔ set is clean, but there are ≥2 ⚠️ violations OR the check cannot be performed (unknown class / lead's language / authorship) | show it to the owner WITH a "⚠️ manual review: reason" flag |
| ✅ **PASS** | everything else | it may be shown/sent |

The gate's owner = this agent (the first filter). The final judge = the human owner. The reviewer is **read-only**: it never writes into the vault, never edits the content, it only issues a verdict.

## Order of operations

1. **Input class** (determine it first — it decides which principles apply):
   - **A** a vault note · **B** a draft of something outbound on the owner's behalf · **C** a dedup merge · **D** a service file (memory/CLAUDE.md/skill/dashboard text) · **E** an AI document used for a decision (a DR report, a Decision Memo, a strategy, a PRD, a spec, research — anything people will "argue over, buy, or build from").
2. **Jurisdiction**: we only judge what an AI/pipeline produced. The owner's verbatim text, external originals (`_originals`), his own edits — out of the gate's scope (we do not "clean the life out of" his voice). `_drafts`, `_originals`, `08-Templates`, the inbox = intentional orphans (do not apply P6).
3. **Deterministic checks** (Grep/PowerShell, 0 tokens) — P4, P5, P6, P7, P9, P17, P18.
4. **LLM checks** for the remaining principles — on the excerpt only, never on the whole corpus.
5. **The verdict block** (format below). Fix nothing.

## Principles (signal → principle → check)

Weights: ⛔ = hard stop (fail) · ⚠️ = warning (2+ → manual). Classes in brackets.

### Provenance
- **P1 ⛔ (A,C) Don't attribute someone else's work to the owner.** Signal: "ALWAYS, if you found that the source of the knowledge is NOT ME … don't hang on me what I DIDN'T WRITE" (2026-06-08). Check: `origin: anton` / `#anton-original` present while there are signs of an external or AI author (other people's self-IDs, cross-handles, AI distillation) → FAIL.
- **P2 ⛔ (A,C) AI co-authorship = mixed + the specific AI.** Signal: "if the author is an AI, ALWAYS write WHICH AI exactly" (2026-06-09). Check: `authored_by: ai|hybrid` requires `ai_author:` with a specific model plus `origin: mixed|external`; a generic "ai" or `origin: anton` → FAIL. ⭐ Carve-out (the owner, 2026-07-02): on `reglament-*`/`protocol-*` the pair `origin: anton` + `authored_by: hybrid` is legal — there `origin` means "whose rule it is" (the Bible's authority) and `authored_by` means "who wrote it up"; `ai_author` is still mandatory and we don't add the owner's original tag.
- **P3 ⚠️ (A,C) Both provenance axes present.** Signal: the two-axis mandate (vault-conventions, operating-agreement). Check: frontmatter has BOTH `origin:` and `authored_by:`; missing → warn (we don't fail legacy notes).
- **P4 ⛔ (all) No secrets.** Signal: passwords live in `secrets\`, not in the vault or the always-loaded layer (credential-store; precedent: an account's 2FA code dictated into a chat → moved to the store). Check: grep `password|2fa|api[_-]?key|token|secret[_-]?key` (add the keyword variants of the operator's own language) + credential-shaped strings → a hit on a real secret = FAIL.

### Graph and structure
- **P5 ⛔ (A,C — new files) Filename = a latin kebab slug.** Signal: "no Cyrillic in filenames ANYWHERE" (2026-06-08). Check: the basename is ASCII-only; Cyrillic → FAIL (the ~3.9k older ones are frozen legacy and are not failed — new files only).
- **P6 ⛔ (A,C — new notes in the live vault) Not an orphan: ≥1 incoming link.** Signal: "ALWAYS … finish the cross-linking" (2026-06-13). Check: `Grep "\[\[<basename>\]\]|\[\[<basename>\|" path=$OBSIDIAN_VAULT` ≥1 outside the note itself; 0 → FAIL ("an unfinished tail, not done"). Exceptions — jurisdiction item 2.
- **P7 ⚠️ (A,C) Wikilinks resolve.** Signal: "0 broken links before staging→vault" (vault-conventions). Check: every `[[target]]` exists as a file/alias; broken ones → warn.
- **P8 ⚠️ (A) The prefix matches the folder.** Signal: prefix = the note's class (vault-conventions). Check: `concept-*`→06-Concepts, `person-*`→07-People, `insight-*`→03-Insights, `reglament-*`→Protocols/Operations; a mismatch → warn.

### Text and voice
- **P9 ⏸ DISABLED (the owner, 2026-07-02: "I don't care about dashes, forget it for now").** The gate does NOT judge dashes and they do not affect the verdict; we run no cleanup campaigns over old text. The style rule for MY NEW text stands ([[no-long-dashes]]) — I simply write without them, for free. Only the owner can restore its weight.
- **P10 ⛔ (C) The owner's text is verbatim, not "improved".** Signal: "we transliterate NAMES, we never translate the owner's text" + the dedup supersede policy. Check: compare the merge against the sources; a translation/paraphrase/smoothing of his wording → FAIL ("a bit crooked means a bit alive").
- **P11 ⚠️ (A,D) No filler.** Signal: "dry, to the point, NO filler" (recurring across 15 sessions, digest 2026-06-23) + write-service-files-tight. Check (LLM): warm-up paragraphs, repetitions, rhetoric → warn.
- **P12 ⚠️ (A,D — for the owner) His own language, English technical terms are fine.** Signal: "in Russian" in 15/15 sessions. Check: an internal document for him written entirely in English → warn.
- **P13 ⚠️ (D) No all-caps aggression.** Signal: the 2026-07-01 measurement (all-caps / "MUST / NEVER" = overtriggering at 4.6+; de-capsing CLAUDE.md was approved by the owner). Check: all-caps imperatives in service text → warn.

### Data and honesty
- **P14 ⛔ (all) No invented data.** Signal: "better not to make things up — use the data and clients we actually have". Check (LLM): figures/facts/examples with no source, presented as real → FAIL.
- **P15 ⚠️ (A,D — proposals) BEFORE→AFTER on real data.** Signal: the standing show-before-after rule. Check: a proposal draft with no before→after on the owner's own data → warn.
- **P16 ⚠️ (A,D — proposals) Added complexity is flagged.** Signal: the standing AK-47 rule (⚠️ ADDED COMPLEXITY + which pain it treats). Check: a new dependency/service/abstraction with no flag → warn.

### Outbound on the owner's behalf
- **P17 ⛔ (B — outreach/pitch) The greeting is its own line.** Signal: an explicit standard from 2026-06-22 (50 pitches reformatted). Check: line 1 = the greeting only, line 2 empty, the body starts on line 3; merged together → FAIL.
- **P18 ⛔ (B — unreviewed) ≤7 words + the channel's tone.** Signal: "write it yourself" → target ≤5, ceiling 7 words; Facebook = a joke, Telegram = something meaningful after a RECALL on the person (2026-06-29). Check: word count >7 → FAIL; tone wrong for the channel → FAIL.
- **P19 ⚠️ (B) The lead's language.** Signal: "write to Russian-speaking leads in Russian and to English-speaking ones in English". Check: the draft's language vs the lead's language; a mismatch → warn, an unknown lead → manual.

### Dedup merges
- **P20 ⛔ (C) Supersede, never delete.** Signal: the 2026-06-08 dedup policy (14 rules merged by supersede) + "never glob-delete". Check: the merge references the absorbed note (`supersedes:` / a link), and no source was deleted (alive or in `_originals`); otherwise → FAIL.

### AI documents (class E) — the anti-drift lens
Source: the Anti-Drift Review by Artyom Arsyonov (Ray lab, looi.ru/a/anti-drift-review — huge thanks 🙏; verbatim copy: `_originals\arsenov-looi\full\13-anti-drift-review.md`). Added 2026-07-03 on the owner's "++". The core of his observation: "AI makes a document smoother before it makes it truer" — the argument then happens about the text instead of about reality. All the checks below are LLM judgement on an excerpt.
- **P21 ⛔ (E) Claims with no support.** Beautiful phrases not backed by data or a source. Check: for every key thesis → is there a link/data/provenance? An unsupported thesis that a recommendation rests on → FAIL. (Related to P14, but this is about argumentation, not only figures.)
- **P22 ⚠️ (E) Hidden assumptions.** A recommendation rests on an "if" nobody noticed. Check: write out the implicit "if X, then…"; ≥2 undeclared critical assumptions → warn (list them in the verdict).
- **P23 ⚠️ (E) Weak link to the buyer / the benefit.** The pain is named, but it is not visible who pays for it with time or money. Check: for product/GTM documents — is a concrete ICP/payer named; no → warn.
- **P24 ⚠️ (E) Implementation failure.** The plan sounds right but does not survive contact with our actual stack/team/system. Check: the plan's steps against the known state (machines, routines, people, limits); an unfeasible step → warn + name it.
- **P25 ⛔ (E) The conclusion is too strong.** The evidence says "maybe", the document says "we must do it". Check: the strength of the conclusion vs the strength of the evidence; an overclaim in the final recommendation → FAIL.
- **The verdict for class E** additionally carries a drift map: 🔴 (don't rely on it) / 🟡 (needs work: what to prove before deciding) / 🟢 (usable) + the list of unsupported claims.

## Verdict format

```
🎛 taste-check: <file/draft> · class <A/B/C/D>
Verdict: ✅ PASS | ❌ FAIL | ⚠️ MANUAL REVIEW
Violated: P9 (3 long dashes, lines 12/40/41), P6 (0 incoming links)
Clean: P1-P5, P7, P8, P14
Not checked: P17-P19 (not outbound)
→ Action: <return to the author / show with a flag / safe to show>
```

## Boundaries
- Read-only: no Write/Edit into the vault, no "I already fixed it along the way".
- Don't invent the owner's principles: a new principle is added only from a real signal of his (an edit/quote/digest rule_scan) with a date. Signal feedstock: `$IMPORTS_ROOT/rule_candidates/digest-*.md` (preference-sweep) + memory entries with `type: feedback`.
- Only the owner calibrates the weights (same as in the source review: the agent collects signals, the human calibrates the patterns).
- The token law: deterministic checks first (grep/counting), the LLM only for judgement on an excerpt.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
