---
name: exegetical-notes
description: Use when producing structured exegetical analysis of a biblical passage. Use when user asks for exegetical notes, verse analysis, passage study, word study with morphology, or detailed interpretive framework for a text. Always English output. Saves to file.
---

# Exegetical Notes

## Purpose

Produce structured, context-neutral exegetical analysis of a biblical passage.
Data-grounded. Always English. Saved to file as a reusable reference document.

**Key constraint:** Every data claim must come from bundled data or web-verified scholarly sources.
Training knowledge supplements but never substitutes for data.

---

## Iron Rules

### Rule 1: Run Pericope Check First

Before generating notes, run a lightweight boundary check:

1. Identify passage boundaries
2. Check Levinsohn (NT) or Masoretic (OT) for boundary confirmation
3. **If boundaries are problematic:** Warn the user and recommend adjustment
4. **If user confirms problematic passage:** Proceed with note in Section 1

**Warning format:**
```
⚠️ Boundary check: [Book] [Range] may be a partial unit.
[Specific issue with discourse evidence]
Recommended passage: [better range]

Continue with [original range]? (notes will flag this in Section 1)
```

### Rule 2: Lexical Analysis Uses morphology_parser.py

Section 4 (Lexical Analysis) must:
- Call morphology_parser.py for parsing data
- Cite actual counts from vocabulary_parser.py
- Never say "appears frequently" — give exact count and verse references
- Format: `lemma (reference): morph description [morphology_parser.py]`

**Valid:** `ἐναρξάμενος (1:6): lemma ἐνάρχομαι, aorist middle participle, nom. sg. masc. [morphology_parser.py]`
**Invalid:** `ἐναρξάμενος is an aorist participle meaning "having begun"`

### Rule 3: Tier All Interpretive Claims

Section 6 must use exactly four tiers, each labeled:

- **Tier 1: Linguistic Evidence** — morphology/grammar directly contradicts the misreading
- **Tier 2: Discourse Evidence** — Levinsohn features or structure contradicts
- **Tier 3: Scholarly Consensus** — web-search-verified with real citations
- **Tier 4: Interpretive Notes** — agent assessment, labeled as such

Never mix tiers. If no Tier 3 source found after web search, state this explicitly.

### Rule 4: Tier 3 Source Quality

For web searches (Tier 3 guardrails):

**Prefer (Tier A):** NICNT, NIGTC, ICC, WBC, BECNT, Hermeneia, BNTC, AB, BDAG
**Accept (Tier B):** Study Bibles with scholarly notes, TDNT, ABD, NAC
**Use with caution (Tier C — always cite tier):** Popular commentaries (BST, TNTC), credentialed scholar blogs
**Reject (Tier D):** Devotional websites, AI content, uncredited blogs, forums

If only Tier C sources found, state: "[Tier C source, use with caution]"
If no verifiable source found, state: "No Tier A/B source located for this claim."

### Rule 5: Run verify_claims.py on Output

After generating the full notes:
1. Run verify_claims.py on the complete output
2. Report results in Section 10
3. If any FAIL results for data claims: correct the claim before saving

### Rule 6: Save to Correct Location

Output always saved to:
```
~/.claude/exegetical-notes/{book_name}/{YYYY-MM-DD}-{chapter-verse-to-chapter-verse}.md
```

Examples:
- `~/.claude/exegetical-notes/philippians/2026-02-18-1-1-11.md`
- `~/.claude/exegetical-notes/genesis/2026-02-18-37-2-11.md`

After saving, report the saved path to user.

---

## Workflow

```
1. Parse invocation
   → book, range, optional --context

2. Run pericope check (lightweight boundary assessment)
   → If problematic: warn user, await confirmation
   → If valid or confirmed: proceed

3. Gather data
   NT: morphology_parser.py for lexical data
       levinsohn_parser.py for discourse features
       vocabulary_parser.py for lemma frequencies
       semantic_groups.yaml for thematic connections
   OT: morphology_parser.py --testament ot for Hebrew morphology
       sefaria_paragraphs.py for Masoretic markers
       vocabulary_parser.py --testament ot for frequencies

4. Web search (for Tier 3)
   → Search for scholarly commentary on passage
   → Evaluate source quality (Tier A/B/C/D)
   → Note source, author, publication

5. Generate all 10 sections

6. Run verify_claims.py on output

7. Fix any FAIL results

8. Save to output location

9. Report saved path to user
```

---

## Output Format (All 10 Sections Required)

```markdown
# Exegetical Notes: [Book] [Range]

**Generated:** [YYYY-MM-DD]
**Passage:** [Book Chapter:Verse-Chapter:Verse] (SBLGNT/NA28 for NT; MT/OSHB for OT)
**Genre:** [epistle | narrative | poetry | prophecy | wisdom | apocalyptic]
**Pericope Status:** [Valid unit | Extended from user input | Confirmed problematic — noted in Section 1]

---

## 1. Passage in Literary Context

[Where this unit sits in the book's argument or narrative arc]
[Connection to preceding unit — what it follows from]
[Connection to following unit — what leads into next section]
[If --context provided: reference the segmentation context]
[If pericope check found issues: note here]

## 2. Internal Structure

[Clause-level structure using discourse features]
[Table required:]

| Verses | Element | Function |
|--------|---------|----------|
| [range] | [label] | [discourse role] |

[Levinsohn feature names cited for internal divisions]
[Masoretic markers cited for OT internal structure]

## 3. Propositional Summary

[The passage's central proposition in 1-2 sentences]
[Secondary propositions if argument is complex]
[Keep strictly descriptive — no Tier 4 claims here]

## 4. Lexical Analysis

[For each key lemma:]
**[Greek/Hebrew] ([reference])**: lemma [lemma form], [full parsing] [morphology_parser.py]
Gloss: "[translation]"
[Semantic group from semantic_groups.yaml if applicable]
[Frequency in book from vocabulary_parser.py]
[Significance for passage interpretation]

[Flag hapax legomena or unusual forms]
[Note semantic range if relevant to interpretive decision]

## 5. Exegetical Conclusions

[Numbered list of defensible interpretive claims]
[Each grounded in sections 2-4]
[Example:]
1. [Claim grounded in morphology — cite the parsing]
2. [Claim grounded in discourse structure — cite the feature]
3. [Claim grounded in intertextual connection — cite the link]

## 6. Interpretive Guardrails

[For each common misreading:]

### [Misreading description]

**Tier 1: Linguistic Evidence**
[How morphology/grammar contradicts this reading]
[Cite: specific parsing, form, or grammatical construction]

**Tier 2: Discourse Evidence**
[How discourse structure contradicts this reading]
[Cite: specific Levinsohn feature or Masoretic marker]

**Tier 3: Scholarly Consensus** (web-verified)
[Citation: Author, Title, Publisher, Year, pp.]
[Tier level: A | B | C — state if C]

**Tier 4: Interpretive Notes** (Agent assessment)
[Clearly labeled as agent assessment, not established fact]

## 7. Open Questions

[Unresolved exegetical issues where data is insufficient]
[Areas of genuine scholarly debate]
[Questions this analysis cannot settle]
[What additional research would be needed]

## 8. Intertextual Links

[Cross-references with verse citations]
[Format: "Reference → Connection to current passage"]
[OT quotations or allusions (from OT_quotes.json for NT passages)]
[Semantic group connections across testaments]
[Parallel passages with significant differences noted]

## 9. Data Sources

- MorphGNT/SBLGNT (CC BY-SA 3.0) — morphological parsing via morphology_parser.py
- [OR] Open Scriptures Hebrew Bible morphhb (CC BY 4.0) — Hebrew morphology
- Levinsohn GNT Discourse Features (dataset 2016; book: Levinsohn 2000) — discourse analysis via levinsohn_parser.py
- [OR] Sefaria / OpenScriptures paragraph markers — Masoretic structure
- [Vocabulary source: vocabulary_parser.py with per-book JSON]
- [Semantic groups: semantic_groups.yaml]
- [Tier 3 sources: full citations as used in Section 6]

## 10. Verification

**verify_claims.py results:**
- Claims checked: [N]
- Claims verified (PASS): [N]
- Claims failed (FAIL): [N — should be 0 for data claims]
- Claims unverifiable: [N — Tier 3 citations expected here]
- Overall: [PASS | FAIL]

[If FAIL results: list each failure and correction made]
```

---

## Invocation Format

```
/exegetical-notes Phil 1:1-11
/exegetical-notes Genesis 37:2-11
/exegetical-notes Romans 3:21-26
/exegetical-notes Genesis 37:2-11 --context "segmentation: Joseph narrative, 8 sessions"
```

- `--context`: Optional. Provides segmentation context for Section 1.
- Book names accept abbreviations (Phil, Gen, Rom, etc.) or full names.
- Testament auto-detected from book name.

---

## Reference Data Access

### NT Morphological Data

```
python3 scripts/morphology_parser.py [Book] --range [range] --output yaml
```

### OT Morphological Data

```
python3 scripts/morphology_parser.py [Book] --testament ot --range [range] --output yaml
```

### Vocabulary Frequencies

```
python3 scripts/vocabulary_parser.py [Book] [--testament ot]
```

### Levinsohn Discourse Features (NT)

```
python3 scripts/levinsohn_parser.py [Book]
```

### Masoretic Markers (OT)

```
python3 scripts/sefaria_paragraphs.py [Book]
```

### Claim Verification

```
python3 scripts/verify_claims.py output.md
```

### Semantic Groups

Located at: `skills/biblical-segmentation/reference/vocabulary/semantic_groups.yaml`

---

## Semantic Groups Reference

Key semantic families from `semantic_groups.yaml` (for Section 4 connections):

| Group | NT lemmas | OT Strong's |
|-------|-----------|-------------|
| Joy | χαίρω, χαρά | H8057, H8056 |
| Faith | πίστις, πιστεύω | H0539 |
| Love | ἀγάπη, ἀγαπάω | H0157, H2617 |
| Righteousness | δικαιοσύνη, δίκαιος | H6663, H6664 |
| Covenant | — | H1285 (בְּרִית) |
| Holy | — | H6918, H6944 |

---

## Common Failure Patterns (Red Flags)

| Failure | Prevention |
|---------|-----------|
| "χαρά appears frequently" | Use vocabulary_parser.py: χαρά (5x) at 1:4, 1:25, 2:2, 2:29, 4:1 |
| Wrong voice in morphology | Always verify via morphology_parser.py |
| "Scholars agree..." without citation | Web search required; cite author/title/year |
| Mixing Tier 1 and Tier 4 | Label every tier claim explicitly |
| Skipping verify_claims.py | Section 10 is required |
| Not saving to output location | Check path, save, report path to user |
| Proceeding past problematic pericope without warning | Pericope check is mandatory Step 1 |

---

## Example Output Fragment: Section 4 (Lexical Analysis)

```markdown
## 4. Lexical Analysis

**ἐναρξάμενος (1:6)**: lemma ἐνάρχομαι, aorist middle participle,
nominative singular masculine [morphology_parser.py]
Gloss: "having begun"
Semantic note: Middle voice is significant — "begun in/among themselves" or
reflexive causative. Contrast with active voice ἐναρχόμενος (not attested here).
Frequency in Philippians: 1x (this passage) [vocabulary_parser.py]

**ἐπιτελέσει (1:6)**: lemma ἐπιτελέω, future active indicative,
3rd person singular [morphology_parser.py]
Gloss: "will complete/finish"
Temporal referent: ἄχρι ἡμέρας Χριστοῦ Ἰησοῦ — eschatological frame.
Frequency in Philippians: 1x [vocabulary_parser.py]

**χαρά (1:4)**: lemma χαρά (noun), [not a verb form — check pos in morphology data]
Frequency in Philippians: 5x (1:4, 1:25, 2:2, 2:29, 4:1) [vocabulary_parser.py]
Semantic group: Joy family — see also χαίρω (9x in Philippians) [semantic_groups.yaml]
```
