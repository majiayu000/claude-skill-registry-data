---
name: job-batch
description: Process a batch of job applications - discover roles, prepare materials, pre-fill forms. Use when ready to apply to multiple positions.
---

# Job Application Batch Processor

*Slash command: `/job-batch`*

## Purpose

Process a batch of job applications using the relationship-focused methodology. This is NOT mass-applying - each role gets proper research.

---

## CRITICAL: This is Phase 6

Per the `/apply` skill methodology, formal applications are the LAST step, not the first.

**For each role in the batch, we do:**
1. Company intel (challenges, pain points, recent news)
2. People mapping (hiring manager + champions)
3. Email pattern detection
4. Outreach draft (user sends)
5. THEN formal application (user submits)

Batch processing doesn't skip steps - it parallelizes them.

---

## Workflow

### Phase 1: Discovery
1. Search for roles matching CLAUDE.md criteria
2. Verify each role is still open via Playwright
3. Check `applications/history.json` for duplicates
4. Create batch of 10 candidates

### Phase 2: User Selection
1. Present batch with compensation, location, fit assessment
2. User selects which to proceed with (typically 3-5, not all 10)
3. Create folders in `applications/pending/{company}_{role}_{date}/`

### Phase 3: Company Intel (NEW - REQUIRED)
For each selected role:
1. Research recent news, funding, product launches
2. Identify challenges and pain points
3. Find engineering blog, tech stack info
4. Document in `notes.md`:
   - 3-5 bullets on what they care about RIGHT NOW
   - Why this role exists (growth? backfill? new initiative?)

### Phase 4: People Mapping (NEW - REQUIRED)
For each selected role:
1. **Hiring Manager**: Who owns this headcount? LinkedIn search
2. **Champions**: 2-3 employees with aligned interests (publications, talks, GitHub)
3. **Mutual Connections**: Does user know anyone who knows them?
4. Document in `notes.md`:
   - Names, titles, backgrounds, LinkedIn URLs
   - Email patterns (use `email_finder.py`)

### Phase 5: Outreach Drafts (NEW - REQUIRED)
For each selected role, draft in `outreach_draft.md`:
1. **Informational email** to a champion (if genuine interest exists)
2. **Or hiring manager email** (after application)
3. Follow `/apply` skill templates - specific, about THEM, easy yes/no

**User sends these - Claude NEVER sends.**

### Phase 6: Materials Preparation
1. Navigate to each job posting via Playwright
2. Extract full job description to `notes.md`
3. Generate cover letter following `/anti-ai-writing` guidelines
4. Fill any application-specific questions in `responses.md`

### Phase 7: Form Pre-fill
1. Open each application in separate Playwright tab
2. Fill standard fields:
   - Name, email, phone, location
   - LinkedIn, GitHub URLs
   - Resume upload (CV PDF)
   - Cover letter (paste or upload)
3. Leave tabs open for user review
4. **DO NOT submit - wait for user**

### Phase 8: Report
Generate summary with:
- Tab index for each application
- Company, role, compensation
- **Hiring manager identified**: Yes/No
- **Outreach draft ready**: Yes/No
- Cover letter preview
- Any fields that couldn't be auto-filled

---

## Output Per Role

Each `applications/pending/{company}_{role}_{date}/` folder contains:

```
├── notes.md           # JD + company intel + people mapping
├── cover_letter.md    # Generated cover letter
├── outreach_draft.md  # Email to champion or hiring manager
└── responses.md       # Application-specific questions (if any)
```

---

## The Test

Before proceeding with any role, ask:

> "Could I email someone at this company even if they had no job openings?"

If the answer is "no" - the research isn't done yet.

---

## Job Board Handling

### Greenhouse (AI2, many others)
- Standard form structure
- Resume upload, cover letter text area
- May have custom questions

### Ashby (Genesis, Insitro)
- Clean modern forms
- Often has "How did you hear about us?"
- Resume upload supported

### Workday (Flatiron/Simons, PacBio)
- Complex multi-step forms
- May require account creation
- Often has duplicate entry issues

### Lever
- Simple single-page forms
- Resume + cover letter + optional fields

### Interfolio (Academic)
- Academic-specific
- May require separate documents (CV, research statement)

---

## Standard Field Values

Read from user's `.claude/CLAUDE.md` and `profile.json`:
- Name, email, phone, location
- LinkedIn, GitHub URLs
- Resume path (typically `documents/*.pdf`)

Users must configure these files before using batch processing. See `GETTING_STARTED.md`.

---

## Anti-AI Writing Checklist

Before finalizing any cover letter, verify:
- [ ] No "delve," "tapestry," "multifaceted," "pivotal"
- [ ] Em dashes < 2
- [ ] Contains at least one contraction
- [ ] Varied paragraph lengths
- [ ] Specific technical details
- [ ] No generic company praise

See: `/anti-ai-writing` skill

---

## Final Report Format

```
## Applications Ready for Review

| Tab | Company | Role | Comp | HM Found | Outreach Ready |
|-----|---------|------|------|----------|----------------|
| 1 | Flatiron | Sr SWE Lead | $190-235K | ✓ | ✓ |
| 2 | Genesis | ML Scientist | Competitive | ✓ | ✓ |
...

### Tab 1: Flatiron Institute
- URL: [link]
- Hiring Manager: [Name, Title]
- Champion for outreach: [Name] - [why interesting]
- Cover letter preview: [first 200 chars]
- Outreach email preview: [first 100 chars]
- Unfilled fields: None

[etc for each tab]

### Next Steps
1. Review outreach drafts - send if genuine interest
2. Review each application tab
3. Edit any fields as needed
4. Submit when ready
5. Follow up per `/apply` timing guidelines
```
