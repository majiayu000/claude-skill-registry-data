---
name: ib-check-deck
description: Deck and report quality checker. Reviews a presentation or report for (1) number consistency across slides, (2) data-narrative alignment, (3) language polish and terminology, (4) visual and formatting QC. Use whenever the user asks to review, check, QC, proof, or do a final pass on a deck, report, or document — including requests like "check my numbers", "reconcile figures across slides", "is this ready to send", "what am I missing", "보고서 검수해줘", "PPT 확인해줘", "숫자 맞는지 확인", "보고서 QC", "덱 검토", "발표자료 QC", "오타 찾아줘".
---

# Deck Quality Checker

Perform comprehensive QC on a presentation or report across four dimensions. Read every slide, then report findings.

## Preflight: Dependency Check

Before starting (chat environment only — Office Add-in skips this), verify required libraries are installed and install any that are missing.

```bash
python3 -c "import pptx" 2>/dev/null || python3 -m pip install python-pptx
```

**Important**: Do not skip this step — `scripts/extract_numbers.py` and slide-text extraction both require `python-pptx`.

## Environment check

This skill works in both the PowerPoint add-in and chat. Identify which you're in before starting:

- **Add-in** — read from the live open deck.
- **Chat** — read from the uploaded `.pptx` file.

This is read-and-report only — no edits — so the workflow is identical in both.

## Workflow

### Read the deck

Pull text from every slide, keeping track of which slide each line came from. You'll need slide-level attribution for every finding ("$500M appears on slides 3 and 8, but slide 15 shows $485M"). A deck with 30 slides is too much to hold in working memory reliably — write the extracted text to a file so the number-checking script can process it.

The script expects markdown-ish input with slide markers. Format as:

## Slide 1
[slide 1 text content]

## Slide 2
[slide 2 text content]

### 1. Number consistency

Run the extraction script on what you collected:

python scripts/extract_numbers.py /tmp/deck_content.md --check

It normalizes units ($500M vs $500MM vs $500,000,000 → same number), categorizes values (revenue, margins, multiples, percentages), and flags when the same metric category shows conflicting values on different slides. This is the part most likely to catch something a human missed on the fifth read-through.

Beyond what the script flags, verify:
- Calculations are correct (totals sum, percentages add up, growth rates match the endpoints)
- Unit style is consistent — the deck should pick one of $M or $MM and stick with it
- Time periods are aligned — FY vs LTM vs quarterly, explicitly labeled

### 2. Data-narrative alignment

Map claims to the data that's supposed to support them. This is where decks go wrong quietly — someone edits the chart on slide 7 and forgets the narrative on slide 4.

- Trend statements ("declining margins") → does the chart actually go that direction?
- Market position claims ("#1 player") → revenue and share data support it?
- Plausibility — "#1 in a $100B market" with $200M revenue is 0.2% share; that's not #1

### 3. Language polish

Professional decks have a consistent register. Scan for anything that breaks it: casual phrasing ("pretty good", "a lot of"), contractions, exclamation points, vague quantifiers without numbers, inconsistent terminology for the same concept, typos.

### 4. Visual and formatting QC

Run standard visual verification checks on each slide. You're looking for: missing chart source citations, missing axis labels, typography inconsistencies, number formatting drift (1,000 vs 1K within the same deck), date format drift, footnote and disclaimer gaps.

Visual verification catches overlaps, overflow, and contrast issues that don't show up in text extraction. Don't skip it — a chart with no source citation looks the same as a properly sourced one in the text dump.

## Output

Categorize findings by severity:

- **Critical** — number mismatches, factual errors, data contradicting narrative. These block delivery.
- **Important** — language, missing sources, terminology drift. Should fix.
- **Minor** — font sizes, spacing, date formats. Polish.

Lead with criticals. If there aren't any, say so explicitly — "no number inconsistencies found" is a finding, not an absence of one.
