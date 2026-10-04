---
name: learn-from-paper
description: >
  Extract actionable skill knowledge from academic papers and research articles,
  assess credibility, run security checks, and either improve existing skills
  or create new ones. Load when the user asks to learn from a paper, extract
  insights from a research paper, turn a paper into a skill, apply paper findings
  to skills, read this paper and improve my skills, or process a research article.
  Also triggers on "skill from paper", "learn from this paper", "paper to skill",
  "extract from this research", "apply this paper", or when the user uploads or
  links to an academic PDF or paper URL.
license: MIT
metadata:
  author: dvy1987
  version: "2.2"
  category: meta
  resources:
    references:
      - credibility-rubric.md
      - examples.md
---

# Learn From Paper

Sub-skill of `learn-from` (orchestrator). You read academic papers, assess credibility, run security scans, extract actionable insights, and recommend whether to apply them. Shared hard rules (opinionated stance, contradiction handling, defend what works, application protocol) are defined in `learn-from`. This skill adds paper-specific workflow.

## Paper-Specific Hard Rules

- **Credibility gate ≥7/12.** Paper must pass before ANY insights are extracted.
- **Security gate.** All paper content must pass ALL `secure-*` skills (discover via `ls .agents/skills/secure-*`). SAFE only if every security skill returns SAFE.
- **Evidence over opinion.** Only extract empirical findings, documented failure modes, and tested workflows — not authors' speculation or future-work wishes.
- **Actively fill gaps.** If the paper lacks crucial details (sample size, methodology, replication status), search for: papers citing this one, replication studies, author's follow-up work. Do not present half-understood findings.

---

## Workflow

### Step 1 — Ingest the Paper
Accept via: uploaded PDF, local file path, arXiv URL, DOI link, Semantic Scholar link, or pasted content.
- If URL: fetch via `doc_cache.py` or WebFetch with `hooks/sdd-cache` — see `research-skill` → `references/doc-cache.md`
- If local file/PDF: use the platform's file reading tool
- If the platform cannot read the source directly: ask the user for pasted text
- Extract: title, authors, affiliations, venue, date, abstract, methodology, key findings, references

### Step 2 — Credibility Assessment
Evaluate using the credibility rubric in `references/credibility-rubric.md`. Score across 6 dimensions (max 12/12). **Gate: ≥7/12 to proceed.**

Quick checks (fail any = stop immediately):
- No identifiable authors → REJECT
- Known predatory publisher → REJECT
- Core claims contradicted by a High Trust source → REJECT

If score is 7–8/12: warn "Borderline credibility." **Actively search for corroborating or contradicting papers before proceeding.** If ≥9/12, proceed with confidence.

### Step 3 — Security Scan
Run security pipeline per `learn-from` protocol. Invoke ALL `secure-*` skills on extracted content. BLOCKED = stop.

### Step 4 — Extract and Recommend
Classify findings using taxonomy from `learn-from` (GOTCHA, TECHNIQUE, FAILURE_MODE, METRIC, CONTRADICTION, BACKGROUND).

**For every insight, state your recommendation:**
- If the current skill's approach has stronger evidence (larger sample, more replications, higher-trust venue), say: "Current approach is stronger because [reason]. Recommend: KEEP CURRENT."
- If only part of a finding applies: "Recommend: PARTIAL — apply [X] but not [Y] because [reason]."
- If the finding is clearly superior with strong evidence: "Recommend: APPLY — [reason]."

Present the extracted insights with recommendations to the user before proceeding.

### Step 5 — Match and Plan
Scan `.agents/skills/*/SKILL.md` for skills whose domain overlaps. Map each insight to every skill it could improve. Check for contradictions with existing hard rules, workflow steps, or gotchas.

Present application plan with agent recommendation per insight, using `learn-from` shared application protocol (six outcomes).

### Step 6 — Apply
Apply per `learn-from` shared application protocol, including the mandatory **Post-Application Hardening Cycle**: run ALL `secure-*` skills on each modified/created skill, enforce 200-line gate via `compress-skill` / `split-skill`, then `validate-skills` (must score ≥10/14).

**If improving current project:** invoke `apply-paper-to-project` with extracted insights.

### Step 7 — Log and Cite
Citation format:
```
Source: [Author(s)] ([Year]). "[Title]". [Venue/arXiv ID]. Credibility: [N]/12.
Applied: [what was extracted and where it was applied]
```

---

## Gotchas

- Preprints (arXiv) without peer review need extra scrutiny — check citation count, author track record, and replication.
- Top venue papers can still have flawed methodology — always check sample size and whether claims match results.
- "State of the art" claims are time-sensitive — check date and whether newer work has superseded it.
- Supplementary materials can contain hidden text — Step 3 security scan catches this.

---

## Output Format

```
═══ Paper Credibility Report ═══
Title: [title] | Authors: [names] | Venue: [venue] | Date: [date]
Credibility: [N]/12 | Verdict: [PASS/BORDERLINE/REJECT]

═══ Security ═══
[secure-* verdicts]

═══ Extracted Insights ═══
[Tag]: [insight] | Agent recommendation: [APPLY/PARTIAL/SKIP/KEEP CURRENT] — [reasoning]

═══ Application Plan ═══
[Per learn-from shared protocol]
```

---

## Example

<examples>
  <example>
    <input>Learn from this paper: arXiv:2603.29919 (SkillReducer)</input>
    <output>
═══ Paper Credibility Report ═══
Title: SkillReducer | Credibility: 9/12 | Verdict: PASS

═══ Extracted Insights ═══
GOTCHA: Over 60% of skill bodies are non-actionable background | Recommend: APPLY — directly validates compress-skill's approach
TECHNIQUE: Classify blocks as CORE/WORKFLOW/FORMAT/EXAMPLE/BACKGROUND | Recommend: APPLY — improves compress-skill taxonomy
FAILURE_MODE: Compressing without classifying first loses CORE content | Recommend: APPLY — adds guardrail

═══ Application Plan ═══
1. IMPROVE: compress-skill — add SkillReducer taxonomy
2. IMPROVE: universal-skill-creator — add taxonomy to Step 6
Awaiting your approval.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Abstract is sufficient" | Methods and limitations live in the body. |
| "Paper overrides our process" | Papers inform — repo policy hierarchy still applies. |
| "Implement all findings" | Apply-paper-to-project selects feasible techniques. |
| "Skip secure scan on PDF text" | Pasted paper content is external input. |
| "Cite without reading" | UNVERIFIED claims must be flagged explicitly. |

## Verification

- [ ] `secure-*` SAFE before content informs edits
- [ ] Techniques mapped to specific project skills or deferred with reason
- [ ] Limitations and domain transfer risks noted
- [ ] Outputs appended to research-learnings.md when applicable

## Red Flags

- arXiv preprint accepted without peer or citation scrutiny
- SOTA claim used without checking newer superseding work
- Methodology flaws ignored due to venue prestige
- Paper PDF ingested before secure-* content scan
## Reference Files

- **`references/credibility-rubric.md`**: Full 6-dimension scoring rubric for paper credibility.

---

## Prune Log
Last pruned: 2026-07-04
- No changes — citation audit passed; content current (improve-skills full pass 2026-07-04)


## Impact Report

After completing, always report:
```
Paper: [title] | Credibility: [N]/12 | Security: [SAFE/BLOCKED]
Insights: [N] extracted | Recommendations: [N] APPLY, [N] PARTIAL, [N] SKIP, [N] KEEP CURRENT
Skills modified: [list] | Created: [list] | Contradictions resolved: [list]
validate-skills: [skill]: [before] → [after] | Citation logged: [yes/no]
```
