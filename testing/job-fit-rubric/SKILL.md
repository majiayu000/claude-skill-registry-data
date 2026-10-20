---
name: "job-fit-rubric"
description: "Shared scoring rubric for the job-search skills, not run on its own: job-lead-intake-scan, job-lead-tier2-scoring and job-lead-manual-jd-lookup load it whenever they set a Fit Score. Defines the evidence table the model fills in and runs score.py to turn it into a deterministic 1-10 score with a readable breakdown."
---

# Job Fit Rubric (v1.1)

The single source of truth for how a Fit Score is produced. Scoring is split in two:

1. **Judgment (the model):** read the job and the user's full resume, and classify each item into a small evidence table. This part is still a model's reading, but every classification is written down and can be checked.
2. **Arithmetic (`score.py`):** turn that table into a 1-10 score. Same table in, same score out, every time. The weights are constants at the top of `score.py`, and this file explains them.

Never pick a Fit Score by feel, and never adjust the number `score.py` returns. If the score looks wrong, the evidence table is wrong: fix the classification, re-run, and say what you changed.

## Files in this skill
- `score.py`: the scoring function. Run `python3 <this skill's directory>/score.py evidence.json` (or pipe JSON on stdin). It prints `score`, `raw`, `caps_applied`, `breakdown` and `rubric_version`, or exits 2 with the reason if the table is invalid.
- `test_score.py`: checks that the rules below hold (`python3 -m pytest -q` in this directory).

## Step 1: build the evidence table

Write a JSON object:

```json
{
  "mode": "tier2",
  "title_seniority": "strong | partial | weak",
  "work_arrangement": "remote | commutable_onsite | commutable_hybrid | relocation_acceptable | relocation_required | unknown",
  "requirements": [
    {"text": "<quoted from the JD>", "type": "required | preferred", "evidence": "strong | partial | none", "resume_evidence": "<short quote or pointer from the full resume, empty if none>"}
  ]
}
```

Use `"mode": "tier1"` and omit `requirements` when no job description has been read (title, company and location from an alert email only).

**`requirements` (Tier 2 only).** One entry per distinct qualification in the JD.
- `text`: the JD's own words, trimmed. Don't paraphrase.
- `type`: `required` for anything under "Requirements", "Qualifications", "Must have", "You have", or stated as required, or as a minimum years figure. `preferred` for "Preferred", "Nice to have", "Bonus", "A plus", "Ideally". If the JD doesn't separate them, treat its main qualifications list as required and anything hedged ("familiarity with", "exposure to") as preferred.
- `evidence`, judged against the full resume only, never against what the user might know but hasn't written down:
  - `strong`: the full resume directly shows it (same tool, method, certification, or responsibility, and at least the years asked for).
  - `partial`: related or adjacent evidence (a comparable tool, fewer years, done but long ago, or only certification without hands-on delivery).
  - `none`: nothing in the full resume supports it.
- Combine near-duplicates (the same ask in two bullets is one entry). Leave out boilerplate that isn't a qualification (benefits, EEO, "passion for our mission"). A JD normally yields 6-20 entries.
- **Rescoring the same JD:** keep the previous run's `requirements` entries exactly (same text, same type) and judge only `evidence` and `resume_evidence` again. Don't merge, split or reword entries on a rescore, so a changed score reflects a changed resume.

**`title_seniority`.** Compare the role's title and level with the **Target roles** in the user's job-search profile (Role families, Seniority, Adjacent roles).
- `strong`: same kind of role at the same level.
- `partial`: right family but a level off (e.g. a junior or a VP role), or one of the profile's Adjacent roles.
- `weak`: a different discipline or a big level mismatch.

**`work_arrangement`.** Judged against the **Location** section of the user's job-search profile (Home area, Home ZIP, Max commute (miles), Commutable to, Remote, Relocation).
- `remote`: fully remote in the user's country, including occasional travel. If the profile says Remote: no, use `unknown` and say why in the Score Breakdown.
- `commutable_onsite` / `commutable_hybrid`: the office is within the profile's **Max commute (miles)** of the **Home ZIP** (of the Home area's center if there's no ZIP), by road, or in a place listed under **Commutable to**. Estimate the distance from the office's address or city, using web search to place it if needed. If you can't place the office, or it's within about 10% of the limit either way, use `unknown` and say so in the Score Breakdown.
- `relocation_acceptable`: on-site or hybrid somewhere that needs a move the profile allows (Relocation: yes, or a place listed after "only to").
- `relocation_required`: on-site or hybrid somewhere that needs a move the profile doesn't allow, or "remote" but requiring residence somewhere the user won't move to.
- `unknown`: the posting or email doesn't say. Prefer finding out over guessing.

Rubric v1.0 named the commutable categories `colorado_onsite` and `colorado_hybrid`; `score.py` still reads those names, so evidence tables saved under v1.0 can be rescored.

## Step 2: run the script

Write the table to a scratch file and run `score.py`. If it exits 2, fix the table and run it again. Copy `score` into the Fit Score column and the `breakdown` string into the Score Breakdown column, exactly as returned (the `job-tracker` skill says what goes in front of it).

## The rules `score.py` applies (v1.1)

| Component | Weight | How it's measured |
|---|---|---|
| Requirements coverage | 70% | Each requirement earns 1 (strong), 0.5 (partial) or 0 (none). **Required items count 3×, preferred items 1×.** Coverage = weighted earned ÷ weighted possible. |
| Title / seniority | 20% | strong 1, partial 0.5, weak 0 |
| Work arrangement | 10% | remote, commutable on-site and commutable hybrid 1; unknown and acceptable relocation 0.5; relocation the user won't make 0 |

`raw = 10 × (0.7 × coverage + 0.2 × title + 0.1 × arrangement)`, rounded half-up to a whole number between 1 and 10. Then these ceilings apply:

- **Relocation required → at most 3.** The user won't make that move, so no other strength can lift it. An acceptable relocation has no cap.
- **Fewer than half of the required items met (counting partials as half) → at most 5.**
- **Tier 1 (no JD read) → at most 8.** Requirements coverage is assumed to be 60%, since nothing has been checked yet.

The resulting colour bands on the tracker are unchanged: 8-10 strong, 6-7 workable with gaps, 1-5 stretch.

**Example breakdown:** `Rubric v1.1 | Req 1.5/3 · Pref 1/2 · coverage 50% · Title strong · Remote | raw 6.5 → 7`

## The Gaps cell
The tracker has one **Gaps** column, right next to Fit Score, so the user can see the gaps without scrolling. Every skill writes it the same way:
- Up to 3 gaps, biggest first, one per line, each starting with `• ` (bullet and space), lines separated by a line break inside the cell.
- Each gap is a short phrase, about 2-8 words, naming what the job asks for that the full resume doesn't show. No full sentences, no quotes from the JD, no explanation.
- Examples: `• No PMP`, `• Workday HCM not shown`, `• 3 of 10 yrs people mgmt`, `• Relocation required (TX)`.
- Tier 1 rows (no JD read): `• JD not read yet`, plus any gap the alert email itself makes obvious (e.g. relocation).

## Changing the rubric
Weights and caps live only in `score.py`. Change them there and in the table above in the same PR, bump `RUBRIC_VERSION`, and run the tests. Scores already in the tracker keep the version they were scored under (it's in their Score Breakdown); rescoring old rows is a separate, explicit request.

## Known constraints
- Scores against the full resume only. Experience that isn't in the full resume isn't evidence until the user adds it there.
- The full resume and the Target roles and Location settings come from the user's job-search profile (see `job-tracker`, **The job-search profile**).
- This skill never touches the tracker; the calling skill does.
- Which gaps to list is each calling skill's call; only the format of the Gaps cell is fixed here.
