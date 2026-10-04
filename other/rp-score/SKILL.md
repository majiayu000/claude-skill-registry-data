---
name: rp-score
model: sonnet
argument-hint: "<candidate> against <job>"
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - WebSearch
  - Glob
---

# /rp-score — Candidate-Job Fit Scorer

Score a candidate against a job requirement using 9 weighted dimensions extracted from the RIP matching engine. Produces a per-dimension breakdown with specific reasoning, a weighted overall score, and positioning guidance.

Zero API cost. Uses only Claude's reasoning plus optional WebSearch for company research.

---

## Input

Parse the user's argument to identify:

- **Candidate:** one of —
  - Name + LinkedIn URL (e.g., "Jane Smith linkedin.com/in/janesmith")
  - Pasted resume text
  - Absolute file path to a candidate YAML (e.g., `~/.recruiter-skills/data/candidates/jane-smith.yaml`)
  - Candidate slug (e.g., `jane-smith` — will look up the YAML automatically)

- **Job:** one of —
  - Pasted JD text
  - URL to a job posting (fetch it)
  - Absolute file path to a JD text file

If either side is ambiguous, ask one clarifying question before proceeding.

---

## Step 1: Load Config

Check if `~/.recruiter-skills/config.yaml` exists. If it does, read it. The `icp` block (required_skills, preferred_skills, min_years, max_years, target_industries) contextualizes what "good" looks like for this recruiter's practice. Use it to calibrate scoring — especially for `skills_match` and `industry_fit`.

---

## Step 2: Load Candidate Data

Determine candidate data source:

1. **If a candidate YAML path or slug is provided:** Read the file from `~/.recruiter-skills/data/candidates/{slug}.yaml`. Use all fields as the candidate profile.
2. **If a LinkedIn URL is provided:** Use WebSearch to find publicly visible information about the candidate (title, company, tenure, skills). Note that data will be limited.
3. **If resume text is provided:** Extract: name, current title, current company, location, years of experience (calculated from work history), skills list, company history, education, and any notable accomplishments.

Build a working candidate profile with whatever is available. Note any fields that are missing or low-confidence.

---

## Step 3: Load Job Data

Determine job data source:

1. **If a URL:** Fetch the page, extract the job posting text (strip nav, footer, forms). Parse out: job title, company name, location/remote policy, required experience, required skills, preferred skills, responsibilities, and any stated compensation.
2. **If a file path:** Read the file.
3. **If pasted text:** Use directly.

Extract the key scoring inputs: required skills list, preferred skills list, years of experience required, seniority level, location requirements, industry context, and company tier signals (startup, mid-market, enterprise, FAANG-tier).

---

## Step 4: Score Each Dimension

Score each dimension on a 0-10 scale. Apply the weight multiplier. Be specific — reference actual evidence from the candidate profile and JD, not generic reasoning.

### The 9 Dimensions

**1. semantic_fit (weight: 1.8)**
Overall role alignment. Does this candidate's career arc, functional focus, and specialization map directly to what this role requires? A DevOps engineer with 8 years of platform work is a 9 for a Senior DevOps role. A DevOps engineer applying to a Product Manager role is a 2.

Scoring guide:
- 9-10: Direct match, primary function aligns exactly
- 7-8: Strong overlap, minor gaps in focus area
- 5-6: Adjacent role, substantial transferable experience
- 3-4: Tangential, requires significant role shift
- 0-2: Wrong function entirely

**2. title_fit (weight: 1.4)**
Title progression logic. Does the candidate's title history make sense for this role's seniority level? Penalize: title inflation (VP at a 5-person startup for a VP role at 500-person company), large step-ups without evidence of scope, or step-downs that need explaining.

Scoring guide:
- 9-10: Same title or logical next step with demonstrated scope
- 7-8: One level off but evidence supports the move
- 5-6: Meaningful gap, candidate would need to be sold as "leveling up"
- 3-4: Two levels off or significant title mismatch
- 0-2: Wrong level entirely (IC for exec, or over-qualified to the point of mismatch)

**3. industry_fit (weight: 1.2)**
Industry relevance. Does the candidate's experience in specific industries map to what the hiring company operates in, or values? Some roles are industry-agnostic; others (fintech compliance, healthcare data, defense) require specific domain knowledge.

Scoring guide:
- 9-10: Same industry, relevant domain knowledge demonstrated
- 7-8: Adjacent industry, skills and context transfer directly
- 5-6: Different industry but role is generally transferable
- 3-4: Industry switch requires explanation, some domain ramp-up needed
- 0-2: High-domain-specificity role, candidate has none of the required domain experience

**4. skills_match (weight: 1.5)**
Technical and functional skills alignment. Compare the candidate's demonstrated skills against the JD's required and preferred skills lists.

Calculate:
- Required skills covered: X of Y (count matches)
- Preferred skills covered: X of Y
- Critical gaps: skills listed as required that are absent

Scoring guide:
- 9-10: All required skills present, most preferred skills present
- 7-8: All required skills present, some preferred gaps
- 5-6: Most required skills present, 1-2 gaps in required
- 3-4: Multiple gaps in required skills, candidate would need training
- 0-2: Fundamental skill mismatch (e.g., Python role, candidate is Java-only)

**5. experience_level (weight: 1.3)**
Years and depth of relevant experience. Not just years of total experience, but years in the relevant function/technology/scope level.

Scoring guide:
- 9-10: Meets or slightly exceeds the stated years requirement with directly relevant experience
- 7-8: Within 1-2 years of requirement, or more years but some spent in adjacent areas
- 5-6: Meaningful gap (under-experienced by 2-3 years, or over-experienced with stale skills)
- 3-4: Significantly under or over the mark
- 0-2: Experience level is fundamentally mismatched

**6. location_fit (weight: 1.0)**
Geographic match or remote policy alignment.

Scoring guide:
- 10: Candidate is in the exact city required (or role is fully remote and candidate is remote)
- 8: Candidate is in the metro area, or willing to relocate (stated on resume/profile)
- 6: Different metro but same region, role is hybrid-flexible
- 4: Long-distance, relocation would be required, no stated willingness
- 0-2: International, visa sponsorship likely needed, or candidate has stated no relocation

**7. company_tier (weight: 0.8)**
Company caliber alignment. Does the candidate's company history match the caliber and complexity of the hiring company? Assess both directions: a candidate from a Fortune 100 may struggle in an early-stage startup, and a candidate from a 3-person startup may not have the process/scale experience a 1,000-person company needs.

Scoring guide:
- 9-10: Company caliber is an excellent match (similar scale, stage, growth phase)
- 7-8: One tier off but skills are clearly transferable
- 5-6: Meaningful caliber gap, candidate would need an adjustment period
- 3-4: Large gap in either direction (e.g., startup founder → Big 4 corporate role)
- 0-2: Fundamental mismatch in scale/complexity of environment

**8. education_fit (weight: 0.5)**
Education relevance. Note: weight is lowest of all dimensions because most technical/functional roles are skill-over-degree. Only penalize heavily if the JD explicitly requires a specific degree.

Scoring guide:
- 9-10: Exact degree match, prestigious institution if that's a factor
- 7-8: Relevant degree, or strong equivalent (bootcamp + 5+ years, relevant certifications)
- 5-6: Unrelated degree but strong practical experience compensates
- 3-4: No degree and JD implies preference, limited certifications
- 0-2: Role explicitly requires credential the candidate does not have (e.g., MD, Bar admission, CPA)

**9. trajectory (weight: 1.0)**
Career arc momentum. Is the candidate's recent trajectory pointing toward this role, or away from it? A candidate who was a Senior Engineer → Staff Engineer → Principal Engineer → Architect has clear upward arc. A candidate who was VP → Director → Manager is trending the wrong direction.

Scoring guide:
- 9-10: Clear upward arc with increasing scope, recent wins, logical next step
- 7-8: Mostly upward, one lateral or one step-down with clear reason
- 5-6: Flat trajectory or unclear direction, this role fits but arc doesn't point to it strongly
- 3-4: Descending arc or repeated lateral moves, candidate may be coasting
- 0-2: Visible stalls, gaps, or pattern that suggests declining performance or disengagement

---

## Step 5: Calculate Weighted Score

```
For each dimension:
  weighted_contribution = (score / 10) × weight

Sum all weighted contributions.
Divide by sum of all weights (= 10.5).
Multiply by 10 to get a 0-10 final score.
```

Sum of weights: 1.8 + 1.4 + 1.2 + 1.5 + 1.3 + 1.0 + 0.8 + 0.5 + 1.0 = 10.5

Label the overall score:
- 8.5 - 10.0 → STRONG FIT
- 7.0 - 8.4 → GOOD FIT
- 5.5 - 6.9 → MODERATE FIT
- 3.5 - 5.4 → WEAK FIT
- 0.0 - 3.4 → NO FIT

---

## Step 6: Format Output

```
CANDIDATE FIT: {Candidate Name} → {Job Title} @ {Company Name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall: {score}/10 ({label})

  semantic_fit:     {score}/10 (1.8x) — {one line of specific reasoning}
  title_fit:        {score}/10 (1.4x) — {one line}
  industry_fit:     {score}/10 (1.2x) — {one line}
  skills_match:     {score}/10 (1.5x) — {one line, include count if possible}
  experience_level: {score}/10 (1.3x) — {one line}
  location_fit:     {score}/10 (1.0x) — {one line}
  company_tier:     {score}/10 (0.8x) — {one line}
  education_fit:    {score}/10 (0.5x) — {one line}
  trajectory:       {score}/10 (1.0x) — {one line}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRENGTHS (top 3 reasons this works):
  - {specific strength}
  - {specific strength}
  - {specific strength}

GAPS (what a hiring manager will push back on):
  - {specific gap}
  - {specific gap}
  [- optional third if meaningful]

POSITIONING ADVICE (what the recruiter should lead with):
  {2-4 sentences: how to present this candidate to maximize acceptance.
  What narrative to use. What to address proactively. What to never lead with.}

RECRUITER VERDICT: {SUBMIT / SUBMIT WITH COACHING / HOLD / PASS}
Rationale: {one sentence}
```

---

## Step 7: Save to Candidate File

Find or create the candidate YAML at `~/.recruiter-skills/data/candidates/{name-slug}.yaml`.

Ensure directory exists:
```bash
mkdir -p ~/.recruiter-skills/data/candidates
```

If the file exists, read it first, then update only these fields:
- `fit_score` — set to the calculated overall score (round to 1 decimal)
- `fit_reasoning` — set to a single sentence summarizing the score

If the file does not exist, create it with this schema:

```yaml
name: ""                    # from candidate data
linkedin_url: ""            # from candidate data if available
current_title: ""           # from candidate data
current_company: ""         # from candidate data
location: ""                # from candidate data
years_experience: 0         # from candidate data
skills: []                  # from candidate data
email: ""                   # from candidate data if available
fit_score: 0                # set to calculated score
fit_reasoning: ""           # set to one-sentence summary
source: "screened"
status: "screened"
found_at: "2026-03-24"      # today's date
```

Confirm the saved path at the end of your output.

---

## Step 8: Suggest Next Step

Based on the verdict, suggest one action:

- **SUBMIT or SUBMIT WITH COACHING:** "Ready to draft outreach to the client? Run `/rp-outreach` to write the submission message, or `/rp-candidate-msg` to draft the candidate prep message."
- **HOLD:** "The score is borderline. Run `/rp-resume-screen {candidate-slug} against {JD}` for a full evidence audit to identify whether coaching would move the needle."
- **PASS:** "This candidate doesn't fit this role. Run `/rp-market-map {role} in {location}` to map where better-fit candidates are concentrated."

---

## Output Format Rules

- Lead with the score table. No preamble.
- Every dimension must have a specific, evidence-based rationale — never generic statements like "strong background."
- If candidate data is incomplete (e.g., only a LinkedIn URL with limited info), flag which dimensions were scored with low confidence.
- Do not inflate scores. A 6/10 is a real result. Recruiters need accurate signals, not feel-good numbers.
- Total output should fit in one screen. Keep dimension notes to one tight line each.
