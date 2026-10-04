---
name: write-best-practice-skill
description: Use when authoring a new SKILL.md to contribute to the official grimoire-core package, or when writing skills for a user package that has chosen to follow STANDARD.md.
source: Wikipedia Manual of Style, MDN Web Docs Contributor Guide
tags: [skill-authoring, structured-authoring, contributor, domain-expert, quality-contribution]
---

# Write Best Practice Skill

Author a new grimoire SKILL.md that encodes a domain best practice and passes `review-best-practice-skill`.

## Why This Is Best Practice

**Adopted by:** Structured authoring guides are standard in high-quality OSS knowledge
projects — Wikipedia's Manual of Style, MDN Web Docs contributor guide, and all major
package registries provide explicit authoring templates to maintain quality at scale.
**Impact:** Defects caught at authoring time cost 5–10× less to fix than those caught at
review — a principle established in software engineering (Boehm, Software Engineering
Economics, 1981) that applies equally to knowledge contributions. Wikipedia's Manual of
Style, applied at authoring time, contributes to Featured Articles achieving measurably
higher quality benchmarks (citation density, edit stability) than non-featured articles —
a direct effect of structured authoring criteria applied before submission.
**Why best:** An explicit authoring guide — vs. ad-hoc contribution where authors
discover requirements through reviewer rejection — eliminates the most common failure
modes (vague "Adopted by", missing impact numbers, over-scoped skills) before a reviewer
ever sees the file.

Sources: Wikipedia Manual of Style, MDN Web Docs Contributor Guide, Boehm (Software
Engineering Economics, 1981)

## Steps

### 1. Verify the practice qualifies

> **Package scope.** This skill authors skills for the official **grimoire-core** package, where STANDARD.md compliance is required. User package authors may also use it if they've chosen to follow the standard — it's optional but enables `review-best-practice-skill` interoperability. Writing simpler user package skills? See [docs/user-package.md](../../../docs/user-package.md) for a minimal template.

Before writing a single line, confirm all four gates:

- **Majority adoption**: adopted by MOST top-tier companies or credentialed professionals
  — not just a few notable ones, not your team's approach
- **Measurable impact**: strong demonstrated outcome (%, time saved, defect reduction,
  risk reduction) — "helps" or "improves" without numbers fails this gate
- **No duplicate**: run `suggest-best-practice` with your topic first — if a skill already
  covers it, extend that skill instead of creating a duplicate
- **No genuine controversy**: if credible top-tier professionals are split ~50/50,
  there is no consensus and therefore no best practice — skip it

If any gate fails, stop. Writing a skill that doesn't qualify wastes reviewer time.

### 2. Pick the name

Follow the full naming standard in `STANDARD.md`. Key rules:

- Pattern: `<verb>-<subject>[-<qualifier>]`
- Verb must be imperative and specific — use the approved verb table; reject `handle-`, `manage-`, `improve-`, `get-`, `use-`, `help-`
- Subject must be specific — if "which kind?" is a valid follow-up, it's too generic
- Qualifier only when `verb-subject` collides across domains
- Kebab-case, ≤50 characters, no `skill-`/`guide-` prefix
- One concept only — if you need "and" in the name, it's two skills

```
❌ handle-deployment        → rejected verb
✅ diagnose-deployment-failure

❌ improve-code             → rejected verb + generic subject
✅ optimize-query-latency

❌ code-review              → noun-first
✅ review-pull-request
```

### 3. Find credible sources

The `source` field must be verifiable. Match source type to domain:

| Domain | Qualifying sources |
|--------|-------------------|
| Engineering | Google Engineering Practices, Netflix/Stripe/AWS engineering blogs |
| Health | WHO guidelines, Mayo Clinic, NIH, ACSM, NSCA position stands |
| Finance | CFA Institute, Bridgewater, Goldman Sachs frameworks |
| Law | ABA Model Rules, BigLaw practice standards, ISDA/NVCA model agreements |
| Business | McKinsey/BCG/Bain frameworks, HBS/INSEAD curriculum |
| Design | Apple HIG, Material Design, Nielsen Norman Group |
| Sports | NSCA CSCS, USA Weightlifting, Olympic coaching methodology |

If you're not certain a source is still current, credible, or holds this position — or the topic is new or fast-moving — search the internet to verify before citing it. Don't rely solely on training-data recall for facts that can change (adoption status, current tool/API names, recent institutional guidance). If no internet-access tool is available in this environment (e.g. network disabled, sandboxed, or no search tool configured), say so explicitly and proceed on best available knowledge — flag the claim as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result.

Failing source examples: "industry standard", "widely known", "common practice".

### 4. Write the frontmatter

```yaml
---
name: write-best-practice-skill
description: Use when <triggering conditions — NOT a summary of the steps>.
source: <institution, standard body, or top-tier company list>
tags: [problem-keyword-1, problem-keyword-2, problem-keyword-3]
---
```

`description` check: does it start with "Use when"? Does it describe WHEN to use it,
not WHAT it does? Could you answer "I have this problem, should I use this skill?" by
reading it? If yes, it's correct.

`tags` check: cover all 4 axes — problem keyword (`injury-prevention`), tool/method
(`progressive-overload`), role/context (`athlete`), outcome (`strength-gain`). Not domain
names (`health`, `engineering`). 3–8 tags, lowercase kebab-case.

### 5. Write `## Why This Is Best Practice`

This is the most scrutinized section. All four sub-fields are required:

```markdown
## Why This Is Best Practice

**Adopted by:** [Specific companies or institutions — not "many companies"]
**Impact:** [Measurable outcome with cited evidence — not "significantly better"]
**Why best:** [Why this over alternatives — name the alternatives]

Sources: [Verifiable citation — institution, study, engineering blog]
```

**Adopted by** checklist:
- Names at least 2 specific companies or 1 named institution
- Claims majority adoption, not just notable adoption
- A domain expert would agree this is the majority position

**Impact** checklist:
- Contains a number (%, ratio, time) OR cites a named study
- The outcome is causal, not just correlated
- Not "significantly better" or "much faster" without data

**Why best** checklist:
- Names at least one alternative approach
- Explains why this approach wins over that alternative
- Not just "this is good" — argues why

### 6. Write `## Steps`

Steps must be immediately executable — the reader can follow them right now.

- **Concrete**: "Run `git diff --cached`" not "check your changes"
- **Commandable**: every step is an action, not a description
- **Complete**: includes what to do when something fails or is ambiguous
- **Specific**: names the actual tool, shows the actual command or output

Size check: 50–300 lines total. Under 50 = too shallow. Over 300 = split into two skills.

### 7. Add domain safety footer (if applicable)

| Domain | Required footer |
|--------|----------------|
| Health / Medicine | `> For personal health decisions, consult a qualified healthcare provider.` |
| Law | `> This is educational content, not legal advice. Consult qualified legal counsel for your situation.` |
| Finance / Investing | `> This is educational content, not financial advice. Consult a licensed financial advisor for personal decisions.` |
| Psychology / Mental Health | `> For mental health concerns, consult a qualified mental health professional.` |

### 8. Run `review-best-practice-skill`

Invoke `review-best-practice-skill` on your draft file.

**Revision gate before PR:** Before creating a PR or outputting the final SKILL.md, run `review-best-practice-skill` against the draft. If the review produces REJECT or NEEDS-REVISION findings, fix them before proceeding. Do not submit a skill that fails its own quality gate.

Fix every REJECT and NEEDS-REVISION finding until the verdict is PASS.

Common first-draft failures:
- "Adopted by" says "many companies" → name them
- "Impact" says "significantly improves" → cite the study or the number
- Steps describe concepts instead of actions → rewrite as commands
- Skill covers two separable concepts → split into two skills

### 9. Register in `SKILLS.md`

Add a one-line entry to `SKILLS.md` in the correct domain section and subsection,
in alphabetical order among peers:

```markdown
- [`skill-name`](./skills/<domain>/<subdomain>/skills/<skill-name>/) — <description field verbatim>
```

**SKILLS.md entry format:** When adding the skill to SKILLS.md, use this format:
```
| skill-name | domain/subdomain | One sentence: what problem it solves | [source-author, year] |
```
The description column must complete the sentence 'Use this when...' and reference the triggering situation, not the skill's method.

Then increment the domain count in the section header:

```markdown
## Domain (N) → ## Domain (N+1)
```

If the subdomain does not yet exist in `SKILLS.md`, add a `### subdomain` header in
alphabetical order within the domain section before the entry.

## Rules

- Run `suggest-best-practice` first — never create a duplicate
- Verify majority top-tier adoption before writing anything
- Search the internet to verify sources and adoption claims when uncertain or the topic is recent — don't rely solely on training-data recall; if no internet-access tool is available, say so and flag the claim as unverified
- `description` field describes triggering conditions ONLY — no workflow summary
- Must pass `review-best-practice-skill` before opening a PR
- If contested 50/50 among top-tier, do not write the skill

## Common Mistakes

**Over-scoping**: "nutrition and training program" — two separable concepts, two skills.

**Vague adoption**: "Used by top companies and professionals in the field" — this fails
the Adopted by check. Name Google, Netflix, Mayo Clinic, CFA Institute — specific names.

**Missing impact number**: "Code review reduces defects" — passes. "Code review helps
code quality" — fails. Always find the study or internal data with a number.

**Description summarizes workflow**: "Use when writing a skill — checks frontmatter,
writes steps, runs review." — WRONG. Correct: "Use when authoring a new SKILL.md to
contribute to grimoire."

**Skill for one team's approach**: your company uses Terraform — that's not a grimoire
skill unless it's majority adoption across the industry.