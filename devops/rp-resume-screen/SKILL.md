---
name: rp-resume-screen
model: sonnet
argument-hint: "<resume path or paste> against <JD path or paste or URL>"
user_invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# /rp-resume-screen — Resume vs Job Screen

Analyze a candidate's resume against a specific job description. Simulates a hiring manager's 6-second scan, then runs a full evidence-quality audit, surfaces likely objections, and delivers the top 5 positioning fixes a recruiter can act on.

Zero API cost. Uses only Claude's reasoning.

---

## Input

The user provides two things (in any order, any format):

- **Resume:** file path (absolute), pasted text, or "uploaded as context"
- **Job description:** file path, pasted text, or a URL

Parse the user's argument to identify which is which. If a URL is provided for the JD, use WebFetch to retrieve the page and extract the posting text. If either input is ambiguous, ask one clarifying question before proceeding.

---

## Step 1: Load Config and Resume/JD

1. Check if `~/.recruiter-skills/config.yaml` exists. If it does, read it. Extract `recruiter.specialties` and `icp` fields if present — use them as context for the analysis.
2. If the resume is a file path, read it. If it's pasted text, use it directly.
3. If the JD is a file path, read it. If it's a URL, fetch it and extract the job posting content (strip nav, footer, boilerplate). If it's pasted text, use it directly.
4. Extract the candidate's name from the resume. Generate a slug: lowercase, spaces to hyphens, no special characters (e.g., "Jane Smith" → `jane-smith`).

---

## Step 2: The 6-Second Scan

Simulate what a hiring manager sees in the first 6 seconds. This is the visual/headline layer before deep reading.

Output this section as:

```
THE 6-SECOND SCAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
First impression: [one sentence — what the resume signals instantly]
Role match visible? YES / PARTIALLY / NO
Title alignment:   [current title vs target title — obvious match or not]
Company caliber:   [does the company list signal the right tier]
Tenure concern:    YES (flag) / NO (clean)
Format/clarity:    CLEAR / CLUTTERED / SPARSE
```

---

## Step 3: Evidence Quality Audit

Extract every major claim in the resume (skills, accomplishments, scope, leadership, tools). For each meaningful claim, rate the evidence quality:

- **STRONG** — specific, quantified, verifiable (e.g., "Reduced deploy time from 4h to 12min by rewriting CI pipeline")
- **MODERATE** — contextual but not quantified (e.g., "Led migration to Kubernetes cluster")
- **WEAK** — vague and could apply to anyone (e.g., "Strong communication skills")
- **ABSENT** — the JD requires it, but the resume doesn't address it at all

Format as a table:

```
EVIDENCE AUDIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Claim                                    Rating      Notes
──────────────────────────────────────── ─────────── ────────────────────────────
[claim]                                  STRONG      [brief rationale]
[claim]                                  MODERATE    [brief rationale]
[claim]                                  WEAK        [brief rationale]
[JD requirement not in resume]           ABSENT      Required: [what JD says]
```

Include at minimum: all technical skills the JD mentions, all leadership/scope claims, and all quantified impact statements (or absence thereof).

---

## Step 4: Narrative Strength Assessment

Evaluate the resume's overall story as a recruiter would when presenting to a hiring manager.

Answer these questions in a brief paragraph for each:

1. **Career arc clarity** — Does the progression make obvious sense for this role? Or does the recruiter need to explain a non-obvious path?
2. **Scope alignment** — Does the scale of past work (team size, company size, budget, system complexity) match what the JD implies?
3. **Recency** — Are the most relevant experiences recent, or are they buried in older roles?
4. **Differentiation** — What makes this candidate specifically memorable vs. 20 other resumes for the same role?

---

## Step 5: Likely Hiring Manager Objections

List 3-5 objections a hiring manager is likely to raise when reviewing this resume for this specific role. Be honest, not polished. These are the friction points a recruiter must preemptively address.

Format:

```
LIKELY OBJECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Objection] — [Why it arises from the resume/JD gap]
2. [Objection] — [Why it arises]
...
```

---

## Step 6: Top 5 Positioning Fixes

Concrete, actionable edits or talking points — things the recruiter can bring back to the candidate or use when presenting the candidate to the client.

Format:

```
TOP 5 POSITIONING FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. [Fix title] — [What to change/add/reframe, and why it addresses the gap]
2. ...
```

Fixes should be specific. "Add metrics to bullet 3 in the Acme Corp role" is better than "Add more quantification."

---

## Step 7: Overall Fit Rating

```
OVERALL FIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fit:         STRONG / MODERATE / WEAK / NO FIT
Screen:      ADVANCE / ADVANCE WITH COACHING / HOLD / PASS
Confidence:  HIGH / MEDIUM / LOW (based on resume completeness)

Summary: [2-3 sentences the recruiter can use verbally with the hiring manager]
```

---

## Step 8: Save to Candidate File

Build the candidate YAML using data extracted from the resume and this analysis.

Target path: `~/.recruiter-skills/data/candidates/{name-slug}.yaml`

If the file already exists, read it first, then update only `fit_score` and `fit_reasoning`. Do not overwrite fields that are already populated unless you have better data from the resume.

If the file does not exist, create it with this schema:

```yaml
name: ""                    # full name from resume
linkedin_url: ""            # extract if present in resume, else ""
current_title: ""           # most recent title
current_company: ""         # most recent company
location: ""                # location from resume header
years_experience: 0         # calculated from work history
skills: []                  # technical skills extracted from resume
email: ""                   # extract from resume header if present, else ""
fit_score: 0                # 0-10, derived from overall fit rating (STRONG=8-10, MODERATE=5-7, WEAK=2-4, NO FIT=0-1)
fit_reasoning: ""           # one-sentence summary of fit
source: "screened"
status: "screened"
found_at: "2026-03-24"      # today's date
```

Use Bash to ensure the directory exists:
```bash
mkdir -p ~/.recruiter-skills/data/candidates
```

Write the file. Confirm the path in your output.

---

## Step 9: Suggest Next Step

After the analysis, suggest ONE logical next action based on the fit rating:

- **STRONG fit** → "Run `/rp-score {name-slug}` to get the full 9-dimension weighted score before submitting."
- **MODERATE fit** → "Run `/rp-score {name-slug}` to identify which dimensions are dragging the score, then decide if coaching closes the gap."
- **WEAK fit** → "Consider running `/rp-market-map {role} in {location}` to find better-matched candidates in this market."
- **NO FIT** → "This candidate doesn't fit this role. Run `/rp-market-map` to map who does fit, or check other open roles."

---

## Output Format Rules

- Use plain text with the separator lines shown above. No markdown headers (no `##`).
- Tables use plain ASCII alignment (not markdown pipes for visual display).
- Lead with the 6-second scan. Do not bury the headline.
- Be direct. This analysis is for a recruiter, not the candidate. No softening language.
- Total output should be readable in under 3 minutes.
