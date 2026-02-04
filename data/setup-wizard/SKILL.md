---
name: setup-wizard
description: >
  Guided onboarding for new users. Collects reference documents, builds
  CANDIDATE-PROFILE.md from them, configures agents. Use for: "set up",
  "initialize", "get started", "configure my profile".
---

# Setup Wizard

Guide users through first-time repository configuration.

<philosophy>

## More Input = Better Output

The system's quality is directly proportional to the reference materials provided. Your job is to extract EVERYTHING the user has. Old CVs, cover letters, LinkedIn, project docs, performance reviews. All of it.

The user does NOT fill in CANDIDATE-PROFILE.md manually. You build it from their materials.

</philosophy>

<workflow>

## Phase 0: Install Playwriter Extension

**This enables browser automation for filling lengthy, multi-page application forms.**

Many companies use applicant tracking systems (Workday, Greenhouse, Lever) that require filling the same information across 5-10 pages. Playwriter lets the agent do this for you.

1. Direct user to install:
   - URL: https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe

2. Instruct them to:
   - Pin the extension to Chrome toolbar (click puzzle icon, then pin)
   - Gray icon = not connected
   - Green icon = connected and ready

3. Explain the use case:
   - "When you find a job with a long application form, click the Playwriter icon on that tab."
   - "I can then fill in the form using your profile data."
   - "You review before submitting. I never submit without your approval."

4. Confirm: "Is Playwriter installed and pinned?"

## Phase 1: Collect Reference Materials

**Be greedy. Ask for everything.**

### Required
1. "Paste your current CV here, or give me a file path."
   - Save to `01-Core-Materials/CVs/[Name]-CV-Current.md`

2. "Do you have older CV versions? Different formats for different roles?"
   - Save each to `01-Core-Materials/CVs/[Name]-CV-[Version].md`

3. "Copy and paste your LinkedIn profile. The whole thing: headline, about, experience, skills, recommendations."
   - Save to `01-Core-Materials/Portfolio/[Name]-LinkedIn-Profile.md`

### Highly Valuable
4. "Any cover letters you're proud of?"
   - Save to `01-Core-Materials/Cover-Letters/[Name]-CL-[Company].md`

5. "Portfolio pieces, case studies, or project write-ups?"
   - Save to `01-Core-Materials/Portfolio/[Name]-[Project].md`

### Nice to Have
6. "Performance reviews, recommendation letters, award citations?"
   - Save to `01-Core-Materials/Portfolio/[Name]-[Type].md`

7. "Old job descriptions from roles you've held?"
   - Save to `01-Core-Materials/Portfolio/[Name]-JD-[Role].md`

<examples>

<example type="good">
- "What else do you have? Old CVs, cover letters, anything. The more I have, the better your applications will be."
- "Even rough drafts help. I can extract the good parts."
- "Got a LinkedIn? Paste the whole profile. I need the About section, experience, skills, everything."
</example>

<example type="bad">
- Stopping after getting one CV
- Not asking about LinkedIn
- Accepting "that's all" without probing
</example>

</examples>

## Phase 2: Build CANDIDATE-PROFILE.md

**You build this. The user verifies.**

Read ALL collected materials in `01-Core-Materials/`. Then populate `CANDIDATE-PROFILE.md`:

| Section | Build From |
|---------|------------|
| Contact Info | CV header, LinkedIn |
| Core Identity | LinkedIn headline, CV summary, cover letter intros |
| Career History | CV experience, LinkedIn experience, JDs |
| Signature Project | Portfolio pieces, CV highlights |
| Skills | CV skills, LinkedIn skills, project descriptions |
| Education | CV, LinkedIn |
| Writing Style | Cover letters, LinkedIn About (capture their voice) |
| Application Strategy | Analyze what role types their materials target |

**For each section:**
1. Show what you synthesized: "From your materials, I built this: [section]"
2. Ask: "Anything to change or add?"
3. Save after confirmation

**For gaps:**
1. Point out what's missing: "I don't have [X]. Can you tell me?"
2. Ask directly, offer to draft from bullet points

## Phase 3: Capture Voice and Preferences

1. "Looking at your cover letters, I notice you use phrases like [examples]. Is that your natural voice?"
2. "Any words or phrases I should NEVER use?"
3. Save to Writing Style section

## Phase 4: Configure Agents

### job-application-automator.md
- "Any style rules or pet peeves for your documents?"
- Update `<user_preferences>` block

### researcher.md
- "What are your job search parameters? (remote/hybrid, industries, salary range, location)"
- Update `<user_context>` block

## Phase 5: Verify and Handoff

1. Summarize:
   - Files collected in `01-Core-Materials/`
   - CANDIDATE-PROFILE.md status
   - Agent configurations

2. Offer: "Want me to scan for any gaps in your profile?"

3. Explain next steps:
   - `job-application-automator` for CVs and cover letters
   - `researcher` for company research
   - `/setup` to return here anytime

</workflow>

<file_destinations>

| Material | Save To |
|----------|--------|
| Current CV | `01-Core-Materials/CVs/[Name]-CV-Current.md` |
| Old/variant CVs | `01-Core-Materials/CVs/[Name]-CV-[Version].md` |
| LinkedIn profile | `01-Core-Materials/Portfolio/[Name]-LinkedIn-Profile.md` |
| Cover letters | `01-Core-Materials/Cover-Letters/[Name]-CL-[Company].md` |
| Portfolio/projects | `01-Core-Materials/Portfolio/[Name]-[Project].md` |
| Performance reviews | `01-Core-Materials/Portfolio/[Name]-Review-[Year].md` |
| Recommendations | `01-Core-Materials/Portfolio/[Name]-Recommendation-[From].md` |
| Job descriptions | `01-Core-Materials/Portfolio/[Name]-JD-[Role].md` |

</file_destinations>

<validation>

Before completing setup, verify:

- [ ] At least one CV saved
- [ ] LinkedIn profile saved (strongly encourage)
- [ ] CANDIDATE-PROFILE.md fully populated (no `[brackets]` in key sections)
- [ ] Contact info complete
- [ ] At least 2 work experiences documented
- [ ] Skills populated with real skills from materials
- [ ] Writing Style section captures user's actual voice
- [ ] Agent preferences configured

</validation>
