---
name: b-roll-shot-list
description: "Generates a detailed, numbered B-roll shot list from a video script or outline, organized by section, with shot type, subject, and purpose for each shot."
status: stable
category: youtube
subcategory: scripting
version: 1.0
eval_score: 4.4
tags: [youtube, scripting, b-roll, production, shot-list, video-production]
---
# B-Roll Shot List

## What This Skill Does
Generates a detailed, numbered B-roll shot list from a video script or outline, organized by section, with shot type, subject, and purpose for each shot.

## When To Use This Skill
- You have a finished or near-finished script and need to plan your B-roll filming session
- You're preparing for a shoot day and need to know exactly what footage to capture
- You want to avoid the common mistake of finishing an edit and discovering you're missing coverage for key moments
- You're working with a videographer or camera operator and need a shared reference document

## What You Need To Provide
**Required:** The full video script or a detailed section-by-section outline; the video's main subject or topic; shooting environment (e.g., home studio, outdoor location, office, on-the-go).
**Optional:** Gear available (e.g., gimbal, drone, macro lens); visual style or reference channels; anything you definitely cannot film (licensed locations, private settings, faces of specific people); screen recording or graphics sections that will replace B-roll.

## How the Assistant Approaches This
1. Reads through the script section by section, identifying every moment where a visual is needed to cover narration, demonstrate a concept, establish a location, or add texture to a talking-head shot.
2. For each moment, determines the most effective shot type (wide establishing, close-up detail, over-the-shoulder, cutaway, insert, time-lapse suggestion) and writes a specific, filmable description — not "show cooking" but "close-up of hands pressing dough into a bowl, flour cloud visible."
3. Organizes shots by script section, flags any shots that require special preparation (permits, props, second person, specific time of day), and adds a brief shooting notes section at the end with logistical groupings to make the shoot day efficient.
4. After the shot list, provides a "Next Step" note: which group of shots to film first on the shoot day (typically setup shots before process shots), what to prepare before arriving on location, and whether chapter-timestamps should be run after the edit to generate the video's description chapters

## Output Format
Numbered shot list organized under bold section headers matching the script. Each entry: shot number, shot type in brackets, specific subject description, one-line purpose note. Ends with a "Shoot Day Notes" section that groups shots by location or setup for efficient filming. Total length: proportional to script complexity — a 10-minute script typically generates 20–35 B-roll shots. Output ends with a "Next Step" note: which group to film first, what to prepare before the shoot, and whether to run chapter-timestamps after the edit is done.

## Quality Criteria
- [ ] Every major script section has at least one B-roll shot assigned to it
- [ ] Shot descriptions are specific enough to film without interpretation — no vague subjects
- [ ] Shot types are varied — not every shot listed as a close-up or a wide
- [ ] Purpose notes explain why each shot serves the edit, not just what it shows
- [ ] Shoot Day Notes group shots logically to minimize setup time
- [ ] No shots listed that require unavailable resources (unless flagged as optional)
- [ ] Output includes at least one concrete next action the user can take immediately (start filming the first group, prepare props or location, or run chapter-timestamps after the edit)

## Example

### Input
**Script sections:**
1. Hook (VO): "Most home cooks have never actually tasted aged butter. Today that changes."
2. What is cultured and aged butter — brief explanation with on-camera host demo
3. The process: sourcing cream, culturing with live cultures, aging in the fridge for 3–14 days
4. Taste test: comparing fresh butter, store-bought cultured butter, and home-aged butter
5. Practical tips: what can go wrong, how to store it, what to use it on
6. Outro with final product on camera

**Topic:** Making and aging cultured butter at home
**Environment:** Home kitchen, standard consumer gear (no drone, no macro lens)
**Style:** Clean, natural light, artisan food video aesthetic

### Output

**B-Roll Shot List — Aged Cultured Butter**
*Total shots: 28 | Estimated filming time: 3–4 hours*

---

**SECTION 1 — HOOK**

1. [CLOSE-UP] Fresh butter block on a wooden board, knife resting against it — hook visual, holds while VO plays
2. [WIDE] Refrigerator door opening to reveal jars of cream at various stages — establishes the project, creates intrigue
3. [INSERT] Hand placing a dated label on a sealed jar — establishes time element before VO mentions it

---

**SECTION 2 — WHAT IS CULTURED BUTTER**

4. [MEDIUM] Host at counter explaining to camera — primary talking-head coverage
5. [CLOSE-UP] Side-by-side: pale commercial butter on left, deep yellow aged butter on right — visual comparison supporting explanation
6. [INSERT] Hand pressing thumb into each butter sample showing texture difference — tactile comparison detail
7. [OVER-THE-SHOULDER] Host reading from a handwritten recipe card — adds authenticity, covers transition moment

---

**SECTION 3 — THE PROCESS**

8. [WIDE] Full counter setup: cream in pouring jug, cultures in small bowl, clean jars — establishes workspace before process begins
9. [CLOSE-UP] Cream being poured into mason jar, visible consistency — step 1 visual
10. [INSERT] Spoon dropping starter culture into cream, slow pour — step 2 visual
11. [CLOSE-UP] Jar lid being sealed, hand shaking jar to mix — step 3 visual
12. [TIME-LAPSE SUGGESTION] Jar sitting on counter over 24 hours (can simulate with three still shots at intervals with edit jump cuts) — time passing visual
13. [CLOSE-UP] Thickened cream in jar being lifted and tilted — shows cultured consistency before churning
14. [MEDIUM] Churning process in stand mixer or food processor — covers narration about the churning stage
15. [CLOSE-UP] Buttermilk separating and being poured off — process detail
16. [INSERT] Hands kneading butter under cold water in bowl — washing process
17. [CLOSE-UP] Finished butter being formed into a log on parchment paper — satisfying close before aging section
18. [WIDE] Butter log placed on labeled shelf in refrigerator — establishes the aging wait

---

**SECTION 4 — TASTE TEST**

19. [WIDE] Three butter samples labeled on a board: Fresh / Store-Bought Cultured / Home-Aged — establishes the test
20. [CLOSE-UP] Knife spreading each butter on bread in sequence — action shot repeated three times, cut together
21. [INSERT] Host hand holding bread piece up to natural light — texture and color visible
22. [MEDIUM] Host tasting each sample, reacting — primary reaction coverage (3 separate takes, one per butter)
23. [CLOSE-UP] Deep yellow aged butter melting onto warm toast — hero shot, most appetizing moment

---

**SECTION 5 — PRACTICAL TIPS**

24. [CLOSE-UP] Butter with visible mold on edge — cautionary visual (can use food coloring on a test batch if needed, or source a reference photo for on-screen graphic)
25. [INSERT] Butter wrapped in wax paper and stored in airtight container — storage method visual
26. [CLOSE-UP] Aged butter melting in cast-iron pan with herbs — use-case visual

---

**SECTION 6 — OUTRO**

27. [MEDIUM] Host at counter with finished butter and a loaded slice of bread — final product hero moment
28. [CLOSE-UP] Finished butter log on board, knife for scale — clean closing product shot

---

**SHOOT DAY NOTES**

**Group 1 — Setup shots (film first, before anything is used):** Shots 1, 5, 8, 19
**Group 2 — Process sequence (film in recipe order):** Shots 9–18
**Group 3 — Taste test (film after aging is complete):** Shots 19–23
**Group 4 — Talking-head and reaction (film after setup is dressed):** Shots 4, 7, 22
**Group 5 — Hero and closing shots (film last with the best-looking final product):** Shots 23, 27, 28

**Flags:** Shot 24 (mold visual) may require a prop or graphic substitution — do not use actual spoiled food on camera without controlled lighting and a clear framing that avoids misrepresentation.

## Known Limitations
- Shot suggestions assume standard consumer camera access. If you're shooting on a smartphone only, some shot types (slow motion, time-lapse) may need to be flagged as device-dependent.
- This skill cannot account for shots that are genuinely impossible without location access — if a script mentions a specific landmark or commercial location, those shots will be listed but flagged. You'll need to decide whether to substitute or seek access.
- For highly abstract or non-visual topics (philosophy, personal finance concepts, mental health), B-roll options are inherently limited. The assistant will suggest illustrative and metaphorical shots, but some sections may need graphics, text overlays, or screen recordings instead.

## Related Skills
- [full-script-writer](../full-script-writer/SKILL.md)
- [chapter-timestamps](../../post-production/chapter-timestamps/SKILL.md)
- [thumbnail-concept-brief](../../pre-production/thumbnail-concept-brief/SKILL.md)
