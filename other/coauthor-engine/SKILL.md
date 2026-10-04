---
name: coauthor-engine
description: >
  Activate when the user needs to manage multi-author collaboration on a paper.
  Tracks author contributions using the CRediT taxonomy, manages responsibility
  assignments, documents the human-AI division of labor, and produces an author
  contribution statement ready for submission.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Co-Author Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (coauthor-engine)
> **Input:** [N] authors, task: [contribution tracking / responsibility assignment / CRediT statement]
> **Output:** author_contributions.md saved
> ```

# Co-Author Engine

## Core Principle

Modern academic publishing increasingly requires transparent documentation of who
did what. The CRediT (Contributor Roles Taxonomy) system standardizes this. For
AI-assisted papers, documenting the human-AI division of labor is not optional —
it's becoming a requirement at major venues.

## When to Activate

- User says "author contributions", "CRediT statement", "who did what"
- User says "add co-author", "assign responsibilities", "contribution tracking"
- Before submission (submission-engine may trigger this)
- When documenting AI involvement in the research process

---

## Step 1: DEFINE Author Roster

### Author Information Template

```markdown
## Authors

| # | Name | Affiliation | Role | ORCID | Corresponding |
|---|------|-------------|------|-------|--------------|
| 1 | [Name] | [University/Org] | [Senior/Junior/PI] | [ORCID] | [Yes/No] |
| 2 | [Name] | [University/Org] | [Senior/Junior] | [ORCID] | [No] |
| 3 | AI Agent (Claude) | Anthropic | AI Assistant | N/A | No |
```

### Author Order Conventions

- **IS/Business conventions:** First author did most work, last author is senior/PI
- **CS conventions:** First author did most work, alphabetical otherwise or by contribution
- **Note:** If AI is listed, typically in acknowledgments, not as author (venue-dependent)

---

## Step 2: ASSIGN CRediT Roles

### CRediT Taxonomy (14 Roles)

For each author (including AI), indicate contribution level:

| # | CRediT Role | Definition | Author 1 | Author 2 | AI Agent |
|---|-------------|-----------|----------|----------|----------|
| 1 | Conceptualization | Ideas, formulation of research goals | Lead | Supporting | — |
| 2 | Data curation | Managing, annotating, maintaining data | Lead | — | Supporting |
| 3 | Formal analysis | Statistical, mathematical, computational analysis | Supporting | — | Lead |
| 4 | Funding acquisition | Obtaining financial support | — | Lead | — |
| 5 | Investigation | Conducting the research, data collection | Lead | Supporting | Supporting |
| 6 | Methodology | Development or design of methodology | Lead | Supporting | Supporting |
| 7 | Project administration | Managing and coordinating the project | Lead | — | — |
| 8 | Resources | Provision of study materials, tools, computing | — | Lead | — |
| 9 | Software | Programming, implementation, code | — | — | Lead |
| 10 | Supervision | Oversight and leadership responsibility | — | Lead | — |
| 11 | Validation | Verification and replication of results | Lead | Supporting | Supporting |
| 12 | Visualization | Creating figures, diagrams, plots | Supporting | — | Lead |
| 13 | Writing — original draft | Creating the initial manuscript | Supporting | — | Lead |
| 14 | Writing — review & editing | Critical review, commentary, revision | Lead | Lead | Supporting |

**Levels:** Lead / Supporting / — (not involved)

### AI-Specific Contribution Documentation

For the AI agent, document specifically:

```markdown
## AI Contribution Statement

This paper was produced with the assistance of an AI writing system (Claude,
via the Open Academic Paper Machine). The AI system contributed to:

- **Literature search and synthesis:** Automated multi-database search, deduplication,
  and initial thematic clustering of [N] papers
- **First draft generation:** Initial drafts of all sections following academic
  writing templates, subsequently revised by human authors
- **Figure generation:** [N] figures generated via AI (PaperBanana)
- **Citation verification:** Automated verification of [N] citations against source abstracts
- **LaTeX compilation:** Automated conversion and PDF generation

**Human oversight and quality control:**
- All research questions, theoretical framing, and methodological decisions were
  made by human authors
- All AI-generated text was reviewed, revised, and approved by human authors
- Empirical data collection and analysis were conducted by human authors
- Final manuscript was reviewed and approved by all human co-authors

**AI disclosure:** [Statement per venue requirements, e.g., "In accordance with
[Venue]'s AI policy, we disclose that AI tools were used in the preparation of
this manuscript as described above. All authors take full responsibility for the
content."]
```

---

## Step 3: TRACK Responsibilities

### Task Assignment Matrix

For ongoing collaboration, track who is responsible for what:

```markdown
## Task Assignment

| Task | Responsible | Deadline | Status |
|------|------------|----------|--------|
| Finalize RQs | Author 1 | [date] | Done |
| Data collection | Author 1 | [date] | In progress |
| Method section review | Author 2 | [date] | Pending |
| Figure 3 redesign | AI Agent | [date] | Done |
| Discussion revision | Author 1 + Author 2 | [date] | Pending |
| Final proofread | Author 2 | [date] | Pending |
| Cover letter | Author 1 | [date] | Pending |
| Submission | Author 1 (corresponding) | [date] | Pending |
```

---

## Step 4: GENERATE Output

### Author Contribution Statement (for manuscript)

Generate venue-appropriate contribution statement:

**CRediT format (most journals):**
```
Author Contributions: [Author 1]: Conceptualization (lead), Investigation (lead),
Methodology (lead), Project administration (lead), Validation (lead), Writing —
review & editing (lead). [Author 2]: Conceptualization (supporting), Funding
acquisition (lead), Resources (lead), Supervision (lead), Writing — review &
editing (lead).
```

**Prose format (some journals):**
```
[Author 1] conceived the study, conducted the literature review, designed the
methodology, and wrote the initial manuscript. [Author 2] supervised the project,
provided critical feedback on theoretical framing, and co-edited the final
manuscript. Both authors approved the final version.
```

### Save

| File | Content |
|------|---------|
| `author_contributions.md` | Full CRediT matrix + AI statement + task tracker |
| Add to `paper.tex` | CRediT statement in Author Contributions section |
| Add to `submission/` | AI disclosure statement for venue requirements |

---

## Integration

| Scenario | Integration |
|----------|-------------|
| Submission-engine | Provides author contribution statement for submission |
| Orchestration log | Complements the AI audit trail |
| Review-engine | Tracks who addresses which reviewer comment |
