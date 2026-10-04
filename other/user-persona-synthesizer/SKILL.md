---
name: user-persona-synthesizer
description: "Extract recurring profiles from real CustDev transcripts and generate evidence-backed persona cards. Use when synthesizing interviews into personas for product docs or roadmap. Triggers: 'synthesize personas', 'create user personas', 'extract personas from transcripts', 'синтезируй персоны', 'создай персоны из интервью', 'извлеки персоны из транскриптов'."
version: 1.0.0
---

# User Persona Synthesizer

This skill extracts recurring user profiles from real CustDev interview transcripts and generates structured, evidence-backed persona cards. It works from any free-form text or markdown files — no integrations, no special format required.

**Input:**
- Interview transcripts or notes: pasted text, markdown files, or plain text (any format accepted)
- Optional: focus attributes (e.g., "focus on goals and frustrations only") or persona count preference

**Output:**
- Markdown document with a summary table, per-persona cards (with verbatim quotes), and synthesis notes

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate and Parse Input

1. Check that interview content is provided (pasted text or file reference)
   - If input is empty or whitespace only: Stop. Return: "No transcripts provided. Paste interview notes or reference files to begin persona synthesis."

2. Detect input format
   - If input resembles structured data (CSV column headers, spreadsheet rows): flag it — "Structured data detected — extracting patterns from columns. For richer personas, raw interview text works better." Proceed.
   - If input is clearly not interview content (product spec, article, meeting minutes with no respondent voices): Stop and report — "This doesn't look like interview transcripts. Persona synthesis requires user interview content — notes, quotes, or dialogue with respondents."
   - If user explicitly requests synthetic/hypothetical personas (not from real data): Stop and report — "This skill synthesizes personas from real interview data only. For synthetic personas, ask Claude directly without this skill."

3. Count the number of distinct interviews or respondents
   - Use explicit separators ("Interview 1:", "Respondent:", "---", numbered sections) or infer from context
   - Report count: "Found N interview(s). Proceeding with synthesis."
   - If only 1–2 interviews detected: flag low sample — "Low sample size (N interviews) — patterns may not be representative. Consider adding more interviews before sharing with stakeholders." Continue.

### Step 2: Extract Attributes per Respondent

1. Check if the user specified a focus attribute list (e.g., "focus on goals and frustrations only")
   - If yes: extract only the specified attributes; skip others
   - If no: extract all attributes listed below

2. For each interview, extract the following attributes where present:
   - **Role / context:** job title, industry, company size, usage environment
   - **Goals:** what they're trying to achieve; motivations
   - **Frustrations:** pain points, complaints, blockers
   - **Behaviours & workarounds:** how they currently solve the problem; tools used
   - **Vocabulary:** recurring words or phrases they use to describe the domain
   - **Key quotes:** verbatim sentences that capture their perspective (capture at least 1–2 per respondent)

3. Build a per-respondent attribute map (internal working structure; not shown to user)

### Step 3: Cluster Respondents into Persona Candidates

1. Compare attribute maps across all respondents
2. Group respondents who share ≥2 significant attributes (role pattern, shared goal, or shared frustration)
   - Each group with ≥2 respondents becomes a persona candidate
   - Solo respondents (no matches) are noted as outliers in Synthesis Notes

3. If no clusters form (all respondents unique): Report — "No clear clusters found across N interviews. Possible reasons: small sample, very diverse audience, or inconsistent interview questions." Offer to generate individual profiles instead.

4. If a persona count preference was provided: adjust clustering to aim for that count (merge close clusters or split divergent ones)

### Step 4: Name and Describe Each Persona

1. For each cluster, generate a descriptive label that captures the dominant pattern
   - Format: "The [Adjective] [Role or Archetype]" (e.g., "The Overwhelmed Manager", "The Data-Driven Analyst")
   - Label should be memorable and based on dominant attributes, not invented arbitrarily

2. Write a 2–3 sentence profile description covering: who they are, what they do, and what they need

### Step 5: Build Persona Cards

For each persona, generate a structured card with:
- Name (descriptive label from Step 4)
- Respondent count (N of M)
- Profile description
- Goals (bullet list)
- Frustrations (bullet list)
- Key quotes (verbatim, sourced from transcripts)
- Behaviours & workarounds (bullet list)

### Step 6: Write Synthesis Notes

1. Identify overlaps — attributes shared across multiple personas
2. Identify tensions — contradictory needs between personas (e.g., Persona A wants automation, Persona B wants manual control)
3. Identify gaps — underrepresented segments if detectable from transcript context
4. Note any outlier respondents who didn't fit any cluster

### Step 7: Assemble and Output Document

1. Generate markdown document following the Output Format below
2. Ensure summary table appears first, followed by individual persona cards, then synthesis notes
3. Validate: no persona card is missing a verbatim quote; all respondents are accounted for in either a cluster or the outliers note

---

## Negative Cases

- **Empty input:** Stop before processing. Return: "No transcripts provided."
- **Non-interview input detected:** Stop. Return explanation and what type of content is needed.
- **Request for synthetic personas:** Stop. Redirect user to ask Claude directly without this skill.

---

## Output Format

Markdown document with the following structure:

```markdown
## User Persona Synthesis — [Date]

**Source:** [N] interview transcripts / notes
**Personas found:** [count]
**Total respondents mapped:** [N of M]

---

### Summary Table

| Persona | Respondents | Top Attributes |
|---------|-------------|----------------|
| [Name]  | N of M      | attr1, attr2, attr3 |

---

### Persona 1: [Name]

**Respondents:** N of M
**Profile:** [2–3 sentence description]

**Goals:**
- [Goal 1]
- [Goal 2]

**Frustrations:**
- [Frustration 1]
- [Frustration 2]

**Key quotes:**
> "[Verbatim quote from transcript]"

**Behaviours & workarounds:**
- [Behaviour or workaround]

**Vocabulary patterns:**
- [Recurring terms or phrases] *(omit section if no distinct vocabulary detected)*

---

### Synthesis Notes

- **Overlaps:** [shared attributes across personas]
- **Tensions:** [contradictory needs between personas]
- **Gaps:** [underrepresented segments, if detectable]
- **Outliers:** [respondents who didn't fit any cluster]
```

**Field rules:**
- Key quotes must be verbatim (no paraphrasing)
- Persona names should be descriptive labels, not generic identifiers ("Persona A")
- Summary table must list all personas; respondent counts must sum to ≤ total N
- Synthesis Notes section always present, even if only gaps or outliers noted
