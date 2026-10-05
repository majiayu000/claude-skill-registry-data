---
name: script-style-guide-checker
description: "Checks a script against a specified style guide and returns a prioritised list of violations with corrections."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [style-guide, script, broadcast, editing, consistency]
---
# Script Style Guide Checker

## What This Skill Does
Checks a script against a specified style guide and returns a prioritised list of violations with corrections.

## When To Use This Skill
- Before a script goes to the studio or is handed to a presenter, and you need to confirm it follows your outlet's house style
- When multiple writers have contributed to a single script and consistency has drifted
- When a script written for one outlet is being adapted for another with a different style guide
- When a junior writer's first broadcast script needs a structured style review before an editor sees it

## What You Need To Provide
**Required:** The complete script text, and the name or rules of the style guide to check against (e.g. AP Stylebook, BBC News style, your outlet's own in-house rules provided as a list).

**Optional:** The intended platform (TV bulletin, radio package, online video), the target audience (general public, specialist, regional), and any specific style rules you want prioritised over others.

## How the Assistant Approaches This
1. Reads the style guide rules you provide — either a named standard (AP, Reuters, BBC) or a custom ruleset you paste in — and builds a mental checklist of the most common violation categories: numerals, titles, abbreviations, punctuation, attribution format, time references, and tone register.
2. Reads through the script systematically, flagging every passage that deviates from the specified rules. Each flag is tied to a specific rule, not a general impression.
3. Returns a prioritised violation report — critical issues (meaning or legality affected) first, then consistency issues, then minor style preferences — with the original text, the rule it breaks, and a corrected version for each flag.

## Output Format
A structured report divided into three priority tiers:

**Critical** — violations that could cause factual confusion, legal risk, or on-air embarrassment (e.g. wrong title for a named role, incorrect date format that changes meaning).

**Consistency** — violations that contradict the style guide but do not affect meaning (e.g. figures written as words in some places, numerals in others).

**Minor** — matters of preference where the guide has a stated preference but the deviation is unlikely to cause problems (e.g. serial comma usage, hyphenation variants).

Each flagged item is presented as:
- **Location:** line or paragraph reference
- **Original text:** exact quote
- **Rule broken:** the specific style rule, cited precisely
- **Suggested correction:** a ready-to-paste replacement

Length scales with script length. A five-minute bulletin script typically produces a report of 300–600 words. Tone is direct and professional — written for an editor, not a student.

## Quality Criteria
- [ ] Every flag cites a specific rule, not a general style preference
- [ ] Corrections are ready to use verbatim without further editing
- [ ] Priority tiers are correctly assigned — nothing minor is labelled critical
- [ ] No false positives: the skill does not flag passages that actually comply with the guide
- [ ] The report covers the entire script, not just the opening sections

## Example

### Input
**Style guide:** AP Stylebook
**Platform:** TV evening news, general audience
**Script:**

```
PRESENTER INTRO

Good evening. 3 people are dead and more than 20 are injured after an explosion tore through a chemicals plant in the eastern outskirts of the city at 9 in the morning today.

Firefighters — who arrived on the scene at approximately nine fifteen — say the blaze is now under control. The plant's owner, Marcus Elliot, chairman and CEO of Elliot Industrial Holdings, confirmed in a statement that an investigation is underway. He says he is "co-operating fully with authorities."

Rescue teams are still searching the site. Reporter Anna Velez has more.

PACKAGE OPEN — ANNA VELEZ STANDUP

Three people lost their lives in what officials are calling one of the worst industrial accidents in the region in recent years. 22 people remain in hospital, six of them in critical condition.
```

### Output

**Script Style Check — AP Stylebook**

---

**CRITICAL**

None identified.

---

**CONSISTENCY**

1. **Location:** Presenter intro, sentence 1
   **Original:** "3 people are dead"
   **Rule broken:** AP style spells out numbers one through nine. Numerals are used for 10 and above.
   **Suggested correction:** "Three people are dead"

2. **Location:** Presenter intro, sentence 1
   **Original:** "at 9 in the morning today"
   **Rule broken:** AP style uses figures for times and omits "in the morning" when "a.m." is used instead.
   **Suggested correction:** "at 9 a.m. today"

3. **Location:** Presenter intro, sentence 2
   **Original:** "at approximately nine fifteen"
   **Rule broken:** Times should be figures with a.m./p.m. "Approximately" is acceptable but the time format is inconsistent with AP style.
   **Suggested correction:** "at approximately 9:15 a.m."

4. **Location:** Presenter intro, sentence 3
   **Original:** "chairman and CEO"
   **Rule broken:** AP capitalises formal titles only when they appear directly before a name. Here the title follows the name, so it should be lowercase.
   **Suggested correction:** "Marcus Elliot, chairman and chief executive of Elliot Industrial Holdings"
   *Note: AP also spells out "chief executive officer" as "chief executive" in running text rather than using the abbreviation CEO.*

5. **Location:** Package open, sentence 2
   **Original:** "22 people remain in hospital"
   **Rule broken:** AP style uses "in the hospital" (with article) in US English. Also, 22 follows the rule for numerals above nine — this instance is correct.
   **Suggested correction:** "22 people remain in the hospital"

---

**MINOR**

6. **Location:** Presenter intro, sentence 3
   **Original:** "He says he is 'co-operating fully with authorities.'"
   **Rule broken:** AP uses "cooperate" (no hyphen). British spelling "co-operating" is non-standard for AP.
   **Suggested correction:** "He says he is 'cooperating fully with authorities.'"

---

**Summary:** 5 consistency issues, 1 minor. No critical violations. Script is close to AP standard — the main pattern is time and numeral formatting. Corrections above can be applied directly.

## Known Limitations
- Named style guides (AP, Reuters, BBC) are checked against the assistant's training knowledge of those guides, which may not reflect the most recent edition. Always verify flagged rules against the current published version, especially for evolving areas like gender-neutral language or digital-first terminology.
- Custom in-house style guides must be pasted in full — the assistant cannot infer rules from a guide name it does not recognise.
- The skill checks written style, not whether the script reads aloud naturally. Broadcast rhythm and breath phrasing require a separate read-aloud pass.
- Very long scripts (over 2,000 words) may be checked more thoroughly if submitted in sections.

## Related Skills
- [copy-editor](../copy-editor/SKILL.md)
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md)
- [terminology-consistency-checker](../terminology-consistency-checker/SKILL.md)
- [proofreader](../proofreader/SKILL.md)
