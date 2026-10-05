---
name: structure-flow-checker
description: "Analyses a draft for logical sequence, narrative coherence, and transitions, then reports exactly where the structure breaks down and why."
status: stable
category: editing
subcategory: editing
version: 1.0
eval_score: 4.2
tags: [structure, narrative-flow, editing, logic, organisation]
---
# Structure Flow Checker

## What This Skill Does
Analyses a draft for logical sequence, narrative coherence, and transitions, then reports exactly where the structure breaks down and why.

## When To Use This Skill
- After a first draft is complete and you suspect the argument or story is losing the reader somewhere, but you are not sure where
- When a long piece — feature article, documentary commentary, in-depth report — has been assembled from separate research blocks and the joins feel rough
- Before sending a draft to a senior editor, when you want to catch structural problems yourself first
- When you have restructured a piece mid-draft and need to confirm the new order holds together

## What You Need To Provide
**Required:** The full draft text — article, script, commentary, or report.

**Optional:** The intended format (print feature, broadcast package, online explainer), the intended audience (general public, specialist, regional), and the structural logic you were aiming for (e.g. "inverted pyramid," "problem–solution–outcome," "chronological," "scene-setting then argument").

## How the Assistant Approaches This
1. Reads the entire draft once to understand the intended argument or story arc — what the piece is trying to establish from opening to close.
2. Maps the actual sequence of information: what appears in each section, in what order, and what each section assumes the reader already knows from previous sections.
3. Checks the map against sound structural logic — does each section follow necessarily from the one before? Are there gaps where the reader must make an unexplained leap? Are there moments where the same information appears twice, or where a key piece of context arrives too late to be useful?
4. Reports the findings by location, with a plain-language explanation of the structural problem at each point and the effect it has on a reader moving through the piece in sequence.

## Output Format
A structured diagnostic report in two parts:

**Part 1 — Overall structure assessment (one paragraph)**
A plain-language summary of how the draft is organised, whether the overall logic holds, and the single most significant structural weakness.

**Part 2 — Flagged issues (list)**
Each issue presented as:
- **Location:** paragraph or section reference (first few words of the paragraph for easy finding)
- **Problem:** what the structural issue is, described in plain terms
- **Effect on reader:** what a reader experiences at this point — confusion, loss of momentum, repeated information, missing context
- **Suggested fix:** a brief, actionable recommendation (not a full rewrite — just enough to point the way)

Issues are listed in order of appearance in the draft, not by severity. This makes it easier to work through corrections in sequence.

Length: typically 400–700 words for a 1,000-word draft. Scales proportionally. Tone is direct and collegial — the kind of notes a trusted editor would give.

## Quality Criteria
- [ ] The overall assessment accurately describes the piece's actual structure, not a generic template
- [ ] Every flagged issue is tied to a specific location in the text
- [ ] Effect-on-reader descriptions reflect real reading experience, not abstract editorial theory
- [ ] Suggested fixes are actionable with a single structural decision, not a full redraft
- [ ] No issues are flagged that are matters of style or word choice rather than structure

## Example

### Input
**Format:** Print feature article, general interest magazine
**Intended structure:** Profile of a person's career arc — chronological, with a thematic argument running through it
**Draft:**

---

When Carla Reyes walks onto a building site now, the workers stop what they are doing. Not because she is the project director. Because she is the only woman in sight, and they still aren't used to it.

Reyes grew up in a small coastal town with no engineering tradition. Her father ran a fishing supply business; her mother taught primary school. She won a scholarship to study civil engineering at twenty-two and graduated near the top of her class.

The construction industry has been slow to change. Studies consistently show that women make up fewer than fifteen percent of the engineering workforce globally, and that the figure has barely shifted in a decade. Retention is a bigger problem than recruitment — many women who enter the field leave within five years.

She got her first job at a regional infrastructure firm, working on a bridge reconstruction project. She describes the first months as "learning to exist in rooms where no one expected you." She was promoted to lead engineer within three years, faster than anyone at her level in the firm's recent history.

She now runs a mid-sized construction company she co-founded eight years ago. The firm specialises in public-sector infrastructure — schools, hospitals, water treatment facilities. Last year it completed twelve projects across four regions.

The moment that changed everything came in her third year at the regional firm. A senior colleague dismissed her calculation in a site meeting in front of the full team. She rechecked it that evening. She had been right. She decided then that she would not wait to be given authority — she would build it herself.

Her company now employs forty engineers, a third of them women. She runs a paid internship programme that explicitly targets candidates from underrepresented backgrounds.

Why does any of this matter beyond one person's story? Because the infrastructure built in the next thirty years will shape where people live, how they move, and whether cities can survive climate pressure. The people who design it will determine what gets prioritised. Reyes argues that a homogeneous profession will produce homogeneous answers to problems that are anything but.

---

### Output

**Structure Flow Check — Print Feature Profile**

---

**Overall assessment**

The draft has the right instinct — open with a striking scene, build a biographical arc, layer in the industry context, close with the wider stakes. The biographical thread is clear and the closing argument is strong. The main structural problem is sequencing: the most dramatically significant moment in the subject's life — the site meeting that changed her direction — arrives in paragraph six, buried after two paragraphs of industry statistics and a description of her current company. The reader has already been told where she ends up before they understand the moment that drove her there. This deflates the career arc and weakens the payoff of the closing argument.

---

**Flagged issues**

1. **Location:** "The construction industry has been slow to change…" (paragraph 3)
   **Problem:** This block of industry statistics arrives immediately after the subject's education, before the reader has followed her into the workplace at all.
   **Effect on reader:** The reader's momentum into the biographical story stalls. The statistics feel like a detour rather than context, because there is no specific moment in her story yet to attach them to.
   **Suggested fix:** Hold this statistics block until after the site meeting scene. It will read as explanation rather than interruption once the reader has seen what she faced personally.

2. **Location:** "She now runs a mid-sized construction company…" (paragraph 5)
   **Problem:** The current state of her career is described before the pivotal moment that led to it (paragraph 6).
   **Effect on reader:** The career arc's dramatic logic collapses. The reader is told the outcome before the cause. When the site meeting scene arrives, it feels like backstory rather than turning point.
   **Suggested fix:** Move the description of her current company and its work to after the site meeting scene. The sequence should be: early career → the moment → what she built because of it.

3. **Location:** "Her company now employs forty engineers…" (paragraph 7)
   **Problem:** This paragraph repeats information already given in paragraph 5 (description of the company) without adding a new dimension.
   **Effect on reader:** Slight feeling of having read this before. The two company-description paragraphs should be one, placed after the turning-point scene.
   **Suggested fix:** Merge paragraphs 5 and 7 into a single post-turning-point section describing the company she built and the deliberate choices she made in building it.

---

**No issues found in:** opening scene (strong), biographical origins (well placed), turning-point scene itself (vivid and specific), closing argument (earns its weight).

## Known Limitations
- The skill analyses the structure of the text as written — it cannot judge whether the events described are true or the facts are accurate. A structurally coherent piece can still contain errors.
- For very short pieces (under 300 words), structural analysis is limited — there is simply not enough material to map a complex arc. Use the proofreader skill instead for short-form content.
- The skill works from the text alone. If the intended structure differs significantly from what appears on the page, providing your intended structure in the Optional input field produces more useful diagnostics.
- Highly experimental or non-linear structures (e.g. deliberate fragmentation, collage journalism) may be flagged as problems when they are intentional choices. Note your structural intention in the Optional field if your piece uses a non-conventional approach.

## Related Skills
- [structure-improvement-advisor](../structure-improvement-advisor/SKILL.md)
- [copy-editor](../copy-editor/SKILL.md)
- [redundancy-checker](../redundancy-checker/SKILL.md)
- [tone-consistency-checker](../tone-consistency-checker/SKILL.md)
