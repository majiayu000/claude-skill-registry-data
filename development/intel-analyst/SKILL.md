---
name: intel-analyst
description: >
  Use this skill when the user wants a rigorous, evidence-graded analysis written up as a
  brief or package: a decision brief (technology, vendor, architecture, build-vs-buy), an
  investigation package (incident root cause, debugging write-up, postmortem), or a risk
  assessment (security, dependency, upgrade, project risk). Triggers include "assess",
  "brief me on", "investigate", "root cause", "risk assessment", "should we use X or Y",
  "intel package", "analyze this decision", and "/intel-analyst". Applies public US
  Intelligence Community tradecraft — ODNI ICD 203/206/208, the CIA structured analytic
  techniques, NATO Admiralty source grading, and the AFOSI report-of-investigation
  structure — to engineering questions, and writes versioned products to docs/intel/.
---

# Intel Analyst

Turns an engineering question into an intelligence-style product: evidence
collected and graded, competing explanations tested, judgments stated with a
fixed probability scale and a separate confidence level, and a version written
for each reader.

This skill borrows method and structure from public standards. It never adds
classification markings and never imitates an agency's products.

**Core rule:** every judgment states how likely it is, how confident we are,
and which evidence supports it. Facts, assumptions, and judgments are never
mixed.

---

## Step 0 — Classify

Choose one product and one mode. State both in one line before any other
work, and let the user override:

> Classified as **Investigation Package**, **Rigorous** mode (incident root cause). Say "quick" to override.

| Product | Use for | Template |
|---|---|---|
| Decision brief | Technology, vendor, architecture, build-vs-buy choices | `templates/decision-brief.md` |
| Investigation package | Incident root cause, debugging, postmortem | `templates/investigation-package.md` |
| Risk assessment | Security, dependency, project, upgrade risk | `templates/risk-assessment.md` |

| Mode | Select when | Checkpoint |
|---|---|---|
| Quick | Low stakes, under about one hour of analysis, reversible | None |
| Rigorous | Any investigation package; architecture or vendor choice; security risk; irreversible action; a leadership reader | Yes, before judgments |

If any rigorous condition is true, the mode is rigorous. Urgency does not
change the mode. If the user asks for speed on a rigorous-class question, say
which condition makes it rigorous and offer quick mode; switch only if the
user agrees, and record "Quick (user override)" in the header.

---

## Steps 1–6 — The intelligence cycle

Load only the files each step names.

### 1. Tasking

Establish four things. Skip any the prompt already answers.

1. **Key Question** — one sentence the product will answer.
2. **Readers** — one or more profiles: `leadership`, `engineers`, `self` (see `references/tailoring.md`).
3. **Decision needed by** — a date, or n/a.
4. **Already known** — what the user has ruled in or out.

Ask at most four questions in rigorous mode and at most one in quick mode. If
the question is still vague, restate it as a precise Key Question and confirm
it once before collecting. If the answers change the mode (for example, a
`leadership` reader appears), restate the classification line before
collecting.

### 2. Collection

Load `references/sourcing.md`. Gather evidence from code, git history, logs,
metrics, docs, and the web. Record every item in the Evidence Log as you go:
ID, one-sentence item, exact source, grade. Log absence of evidence too ("no
errors before 14:00"). Log unreachable sources as "not collected: <reason>".

When collection reviews code — a diff, a function under investigation, or a
dependency's source — invoke `codered:mission-grade` and judge the code by its
review standards. Log each finding as an observed item with the exact
`file:line`. A finding is evidence, not a conclusion: what it means goes in
Analysis.

### 3. Processing

Separate observed facts from claims. Form two to five competing hypotheses
(investigation), options (decision), or scenarios (risk). Include at least one
you do not expect to win. List the key assumptions.

### 4. Checkpoint (rigorous mode only)

Show the user the Evidence Log, the hypotheses or options, and the Key
Assumptions, in that order. Ask: "Add, correct, or approve?"

**STOP.** Do not write judgments, ACH scores, or the product until the user
replies. In quick mode, skip this step.

### 5. Analysis

Load `references/techniques.md` and `references/analytic-standards.md`.

1. Run ACH: build the matrix, look for disconfirming evidence, rank by fewest
   inconsistent items, and apply the survival test in `references/techniques.md`.
2. Run a Key Assumptions Check.
3. Run the other techniques the mode table in `references/techniques.md`
   requires (What If?, High-Impact/Low-Probability, Indicators/Signposts).
4. Draft judgments using only the seven scale terms, each with a separate
   confidence level and cited E-IDs.
5. **Red Team** — last, so nothing after it changes a judgment. Rigorous mode: invoke `codered:devils-advocate` with the draft
   judgments, all hypotheses or options, the Evidence Log, and the Key
   Assumptions. Invoking it loads its method; apply that method to the draft
   as a separate pass and write its structured findings. That is the
   integration, not a fallback. Fold the findings back as
   `references/techniques.md` describes. Quick mode, or fallback when the
   skill is not installed: write the three strongest counter-arguments inline
   and state the fallback.

### 6. Dissemination

1. Fill the product template. Keep its section order and headings.
2. Run the nine-item checklist in `references/analytic-standards.md`. Fix
   every "no", or record why it cannot be fixed in Intelligence Gaps.
3. Pass the prose — BLUF, Key Judgments, Conclusions, narrative paragraphs —
   through `codered:nfc` in `clear` mode. Do not rewrite tables, logs, or
   matrices. Do not change any scale term, confidence level, or E-ID.
   Invoking `codered:nfc` loads its rules; applying them yourself is the
   integration. If it is not installed, use the fallback: short sentences,
   one idea per sentence, no idioms, active voice.
4. Write the full product.
5. For each reader profile that needs one, derive a tailored version with
   `templates/bluf-one-pager.md` and `references/tailoring.md`.
6. Reply with the file paths, the BLUF, and the top gap. Do not paste the
   whole product into chat.

---

## Acting on the product

The product ends at Recommended Actions. If the user then asks you to apply
one that refactors or fixes code, invoke `codered:mission-grade` before you
write any code, and follow it for the change, its tests, and its commit
message. Do not change the product to match the fix; a later product on the
same topic records whether the judgments changed.

---

## Quick mode

Same cycle, compressed:

- one tasking question at most
- short Evidence Log (the items the judgments depend on)
- no checkpoint
- abbreviated ACH (options × top three to five evidence items)
- Red Team as three inline counter-arguments
- Key Assumptions Check limited to the top three
- every template heading stays; a section whose technique does not run in
  quick mode gets one line: "Not run (quick mode)." plus any best-effort note

Quick mode does not lower the standards: scale terms, separate confidence,
E-ID citations, and the Evidence Log are still required.

---

## Output

- Full product: `docs/intel/YYYY-MM-DD-<slug>.md` in the repository the user is working in.
- Tailored versions: `docs/intel/YYYY-MM-DD-<slug>-<profile>.md` (leadership → `-bluf.md`).
- `<slug>`: three to six lowercase words joined by hyphens, from the Key Question.
- If `docs/intel/` does not exist, create it.
- If the working directory is not inside a git repository, ask the user for an output path before writing.
- Never overwrite a file. If the path exists, append `-2`, `-3`, … to the slug.
- If a product on the same topic (same slug or same Key Question) already exists in `docs/intel/`, read it and say in the new product whether the judgments changed and why.

---

## Error handling

| Situation | Do this |
|---|---|
| Thin evidence (fewer than three observed or derived items, or all graded D–F) | Proceed. Cap confidence at low. Say so in the BLUF. Fill Intelligence Gaps with collection actions. |
| Conflicting sources | Log both. Show the conflict in ACH. Say in the judgment which source was weighted more, and why. |
| No hypothesis survives ACH (survival test in `references/techniques.md`) | Report "cause undetermined" with the closest hypotheses and the evidence that would separate them. Never invent a conclusion. |
| Source unreachable | Log "not collected: <reason>". List it under Intelligence Gaps. Continue. |
| Sensitive data in evidence | Redact it. Cite the location, not the content. |
| `codered:devils-advocate` or `codered:nfc` unavailable | Use the inline fallback described above. Note the fallback in the product. |
| `codered:mission-grade` unavailable | Fallback: review the code for unchecked errors, unbounded loops and inputs, and missing tests, and say in the product (or in the reply, for a code change) that the fallback was used. |

---

## Red flags

These thoughts mean the product is about to fail its standards.

| Thought | Reality |
|---|---|
| "The cause is obvious, I'll skip the other hypotheses." | ACH needs at least two. The obvious answer is the one most worth testing. |
| "It may be X" reads fine. | "May" hides the probability. Use a scale term and a confidence level. |
| "Overall risk is moderate" sums it up for the BLUF. | Risk levels mix likelihood and impact. State the likelihood as a scale term and the impact separately. |
| "Neither source was weighted heavily." | Say which source was weighted more and why, using the grades. |
| "The logs show…" | Which log, which query, which time window? Give an E-ID. |
| "I'll log this conclusion as evidence." | The Evidence Log holds observations and derived calculations only. Explanations go in Analysis. |
| "Very likely, high confidence" in one phrase is enough. | It is — but only if both were decided separately and the evidence meets the high-confidence rule. |
| "The user is in a hurry, so I'll skip the checkpoint." | Offer quick mode; do not skip silently. |
| "I'll put my suspicion in the findings." | Findings of Fact are observed facts only. Opinion goes in Investigator's Comments. |
| "The leadership version can say it more strongly." | Tailored versions never add a judgment or raise a probability or confidence. |
| "Every source is a forum post, but they all agree." | Agreement among D-graded sources still caps confidence at low. |
