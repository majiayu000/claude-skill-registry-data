---
name: srs-generator
description: >
  Generate IEEE 830 SRS from raw requirements. Use when the user says
  "write SRS", "generate requirements doc", "analyze requirements",
  "I have raw requirements from a client", or pastes a client email/chat/PRD.
---

# srs-generator — IEEE 830 SRS from Raw Requirements

Pipeline: **Brainstorm** → Receive → Extract → Gap Scan → Clarify (P1 → P2 → P3) → Generate → Review Gate → Save

Reference files (load before starting):
- `.codex/skills/srs-generator/references/srs-template.md`
- `.codex/skills/srs-generator/references/gap-detection-guide.md`

**Context files (load if present — created by `.codex/scripts/init_project.py`):**
- `projects/{name}/_context/vision.md` → pre-fills §1.2 Scope and §2.1
- `projects/{name}/_context/features.md` → pre-fills §2.2 and IN/OUT table
- `projects/{name}/_context/tech_stack.md` → pre-fills §3.5 Design Constraints
- `projects/{name}/_context/glossary.md` → pre-fills Appendix A
- `projects/{name}/_context/quality_standards.md` → pre-fills §3.3–§3.6 NFR

If context files exist: skip Brainstorm Gate questions already answered there.

---

### Brainstorm Gate — Understand Context First

Do NOT ask for raw requirements yet. First understand project context.

Ask these 3 questions in one batch:

1. **System type:** Web app / Mobile app / API / Internal tool / SaaS / Desktop / Other?
2. **Primary users:** Who will use this system? (end customers, internal staff, admins, B2B clients…)
3. **Core problem:** What problem does this system solve? (1–2 sentences)

Wait for answers. Use responses to seed §2.1 Product Perspective, §2.3 User Characteristics, and §1.2 Scope.

After receiving answers, prompt:
```
Context noted. Now paste your raw requirements — any format works:
client email, bullet list, chat transcript, PRD draft.
```

Wait for raw input, then proceed to Step 0.

---

### Step 0 — Receive Input

Read full input silently. Emit:
```
Input received: ~{N} words | type: [email prose | bullet list | partial PRD | mixed]
```

---

### Step 1 — Extract & Classify

Output structured block:
- **Actors** — named and implied stakeholders. Tag undefined: `[GLOSSARY-GAP: {actor}]`
- **Features** — FR-01, FR-02… in "Subject can do X" form. Note strategy: prose / bullets / PRD
- **Constraints** — verbatim fragments only (tech stack, deadline, compliance, budget)
- **Out-of-Scope signals** — explicit exclusions. If absent: `[CONTEXT-GAP: no out-of-scope boundary stated]`

Append `[Source: {location}]` to every item.

---

### Step 2 — Gap Scan

Load `.codex/skills/srs-generator/references/gap-detection-guide.md`. Run all 7 patterns. Output:

| # | Priority | Pattern | Verbatim fragment / missing element |
|---|----------|---------|-------------------------------------|

Zero gaps → state explicitly, jump to **SRS Generation**.

---

### Step 3 — Round 1 Clarification (P1 — Blockers)

If P1 gaps exist, ask the user with ≤7 questions. Label:
```
Round 1 of 3 — Scope & Actors (P1 — must resolve before writing SRS)
```

On receipt: integrate, mark resolved gaps. Unanswered P1 → `[CONTEXT-GAP: {desc}]` → Appendix B.
Block only if zero actors AND zero scope remain. Then proceed to Round 2.

---

### Step 4 — Round 2 Clarification (P2 — Functional Details)

If P2 gaps remain, ask the user with ≤7 questions. Label:
```
Round 2 of 3 — Functional Details (P2)
```

Unanswered → log assumed default in SRS and Appendix B. Then proceed to Round 3.

---

### Step 5 — Round 3 Clarification (P3 — Optional)

Ask the user with ≤7 questions. Label:
```
Round 3 of 3 — Non-Functional & Secondary Details (P3 — optional)
Reply 'skip' to use [TBD] placeholders.
```

On "skip": mark all P3 gaps `[TBD: {condition} | owner: {role} | resolve-by: sprint planning]`.
Proceed to **SRS Generation**.

---

### SRS Generation

Populate `.codex/skills/srs-generator/references/srs-template.md` with all gathered information.

**§1.2 Scope** — mandatory IN / OUT table for every feature area.

**§3.2 Functional Requirements** — each FR block:
```
FR-NN [Essential|Conditional|Optional]
Requirement:  The system shall {verb} {object} when {condition}.
Actor:        {role}
Precondition: {state}
Given:        {context}
When:         {trigger — exactly one}
Then:         {externally observable outcome}
Source:       [{location}]
```
Non-observable "Then" → `[VERIFIABILITY-FAIL: FR-NN]` → Appendix B

**§3.3–§3.6 NFR** — Quality Attribute Scenario (ISO/IEC 25023):
```
NFR-NN [{ISO/IEC 25010 characteristic}]
Source / Stimulus / Environment / Artifact / Response / Response Measure: {numeric}
```

After populating, run IEEE 830 quality checklist from `gap-detection-guide.md`. Output verdict:
- `COMPLIANT` — all sections present, Appendix B empty
- `PARTIALLY COMPLIANT` — sections present, Appendix B has open items
- `NON-COMPLIANT` — required sections missing

---

### Human Review Gate

```
Review complete. SRS is {verdict}.
Open issues: {count} (see Appendix B).
Proceed to save? [Y / n]
```

Wait for explicit confirmation before writing any file.

---

### Save & Report

1. Derive slug from §1.2 product name (lowercase, hyphenated). Fallback: ask user.
2. Path: `docs/srs-{slug}-{YYYYMMDD}.md`
3. Echo absolute path, wait for confirmation.
4. Create `docs/` if absent, write file, confirm: `"Saved ✓ {absolute_path}"`
