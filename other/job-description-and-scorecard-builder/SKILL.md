---
name: job-description-and-scorecard-builder
description: "Generate a job description and a matched interview scorecard from role notes. Paired hiring documents for managers who hire without an HR team. Use when opening a new role. Triggers: 'write a job description', 'job description and scorecard', 'вакансия и скоркард', 'напиши вакансию'."
version: 1.0.0
---

# Job Description and Scorecard Builder

This skill generates a job description (JD) and a matched interview scorecard from your role input notes in a single pass. Designed for hiring managers, team leads, and department heads who run interviews without a dedicated recruiter. No recruiting SaaS required.

**Input:**
- Role notes (free-form text): title, level, must-have requirements, nice-to-have, compensation range, work format, optional team context

**Output:**
- Single markdown response with two paired documents: Job Description + Interview Scorecard, ready to copy-paste

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse Role Input

1. Read the user's role notes (free-form text, bullet list, or structured).
2. Extract structured fields:
   - **Title:** role name (required)
   - **Level:** Junior / Middle / Senior / Lead / Director / VP / C-level
   - **Must-have requirements:** list of non-negotiable skills or qualifications
   - **Nice-to-have requirements:** list of preferred but optional skills
   - **Compensation:** range or "not specified"
   - **Work format:** Remote / Hybrid / Onsite
   - **Team context:** team size, reporting line, or department (optional)
   - **Interview format preference:** competency-based / case-based / behavioral (optional)
3. If Title is present but other fields are missing: proceed with available data; flag gaps at the top of the output.
4. If input is only a job title with no other context (e.g., "Engineer"):
   - Generate 4–5 clarifying questions (level, must-haves, team context, compensation, work format)
   - Do not produce an empty template
   - Respond: "Роль пока не описана — нужно больше деталей. / The role is underspecified. Please answer these questions:"
   - Stop. Do not proceed to document generation.

### Step 2: Generate Job Description (Format A)

1. Create the JD with these sections in order:
   - **About the Role:** 1–2 sentences on what the person does and team context; include why the role exists if known
   - **Responsibilities:** 4–7 bullet points, each starting with an action verb (Build, Lead, Drive, Analyze, etc.)
   - **Requirements > Must Have:** derived from must-have input; one requirement per bullet
   - **Requirements > Nice to Have:** derived from nice-to-have input; omit section entirely if none provided
   - **Compensation & Work Format:** compensation range + work format on separate bullets
   - **About the Team:** 1 sentence on team size, structure, or reporting line; omit if no team context provided
2. Adjust language register:
   - Standard roles (Junior through Lead): professional, specific, results-oriented
   - Leadership roles (Director / VP / C-level): strategic language, focus on organizational impact

**Edge Case — Leadership Role:**
If level is VP, Director, or C-level: add leadership, strategic thinking, and organizational impact to the Responsibilities list; these same dimensions become criteria in the Scorecard (Step 3).

**Edge Case — Update Mode:**
If user pastes an existing JD with a request to update it: apply new inputs as changes only; prefix output: "Updated: [list of changed sections]. Unchanged sections kept as-is." Do not regenerate the full JD from scratch.

**Edge Case — Mixed Language Input:**
If notes are in mixed EN + RU: detect dominant language; generate both documents in that language; translate all requirements consistently.

### Step 3: Generate Interview Scorecard (Format B)

1. Map each must-have requirement from the JD to a scored criterion in the scorecard. Criterion names must match the JD requirement phrasing exactly (preserves the paired linkage).
2. Assign weights:
   - Must-have requirements → **High**
   - Nice-to-have requirements → **Medium** (add at the end of the criteria table; omit if none provided)
3. For each criterion, write behavioral anchors:
   - **1 — Not demonstrated:** no evidence observed in the interview
   - **2 — Below bar:** partial or inconsistent evidence; lacks depth or breadth required for the role
   - **3 — Meets bar:** clear evidence meeting the stated JD requirement
   - **4 — Exceeds:** significantly stronger; demonstrates expertise beyond what the role requires
4. Add **Overall Recommendation** with four options: Strong Hire / Hire / No Hire / Strong No Hire
5. Add **Notes / Observations** free-text field at the end

**Edge Case — Interview Format Specified:**
If user specified a format (case / behavioral / technical): align anchor language to that format; add a note at the top of the scorecard: "Scorecard designed for [format] interview."

### Step 4: Format and Output

1. Output both documents in a single markdown response:
   - Format A (JD) first, labeled `## Job Description — [Title] ([Level])`
   - Horizontal rule (`---`) as separator
   - Format B (Scorecard) second, labeled `## Interview Scorecard — [Title] ([Level])`
2. No meta-commentary between or after the two documents
3. Output language matches detected user language
4. All section headers translate to Russian when responding in Russian:
   - "About the Role" → "О роли"
   - "Responsibilities" → "Обязанности"
   - "Must Have" → "Обязательно"
   - "Nice to Have" → "Желательно"
   - "Compensation & Work Format" → "Компенсация и формат работы"
   - "About the Team" → "О команде"
   - "Interview Scorecard" → "Оценочный лист"
   - "Overall Recommendation" → "Итоговая рекомендация"
   - "Notes / Observations" → "Заметки / Наблюдения"

---

## Negative Cases

- **Empty input or whitespace only:** Respond: "Опиши роль: название, уровень, ключевые требования. / Describe the role: title, level, must-have requirements."
- **Request to find or search candidates:** Respond: "Этот скилл создаёт документы — вакансию и скоркард. Поиск кандидатов не поддерживается. / This skill creates documents — a job description and scorecard. Candidate search is not supported."
- **Title only, no other context:** Ask clarifying questions (see Step 1.4). Do not produce an empty template.

---

## Output Format

Single markdown response with two paired, labeled sections:

```markdown
## Job Description — [Role Title] ([Level])

### About the Role
[1–2 sentences: what the person does, team context, why the role exists]

### Responsibilities
- [Action-verb-first responsibility]
- [Action-verb-first responsibility]
- [Action-verb-first responsibility]
- [Action-verb-first responsibility]

### Requirements

**Must Have:**
- [Must-have requirement 1]
- [Must-have requirement 2]

**Nice to Have:**
- [Optional requirement 1]

### Compensation & Work Format
- **Compensation:** [range or "not specified"]
- **Work format:** [Remote / Hybrid / Onsite]

### About the Team
[1 sentence: team size, structure, or reporting line]

---

## Interview Scorecard — [Role Title] ([Level])

**Instructions:** Rate each criterion 1–4 using the behavioral anchors.

| Criterion | Weight | 1 — Not demonstrated | 2 — Below bar | 3 — Meets bar | 4 — Exceeds |
|-----------|--------|----------------------|---------------|---------------|-------------|
| [Must-have 1 — exact JD phrasing] | High | No evidence observed | Partial or inconsistent | Meets stated JD requirement | Significantly beyond requirements |
| [Must-have 2 — exact JD phrasing] | High | No evidence observed | Partial or inconsistent | Meets stated JD requirement | Significantly beyond requirements |
| [Nice-to-have 1] | Medium | No evidence | Mentioned, not demonstrated | Demonstrated | Deep expertise shown |

**Overall Recommendation:**
☐ Strong Hire  ☐ Hire  ☐ No Hire  ☐ Strong No Hire

**Notes / Observations:**
[Free text]
```

**Field rules:**
- Criterion names in the scorecard match JD must-have requirement phrasing exactly
- Each behavioral anchor is one sentence or phrase
- "Meets bar" (score 3) aligns directly with the stated JD requirement language
- Nice-to-have criteria row omitted if no nice-to-haves were provided
