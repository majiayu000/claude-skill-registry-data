---
name: stakeholder-adapter
description: "Adapts any working document (PRD, status update, proposal, meeting notes)
  into audience-specific versions: Leadership/Executives, Engineering/Team, and
  Client/External partner. Applies audience-specific framing rules — business impact
  for executives, technical depth for engineers, outcome language for clients. Use
  when the same document needs to reach multiple audiences without manual rewriting.
  Triggers RU: «адаптируй документ», «сделай версию для руководства», «разные версии
  документа». Triggers EN: 'adapt document', 'stakeholder adapter', 'create executive
  version', 'make a client version', 'rewrite for audience'."
version: 1.0.0
---

# Skill: stakeholder-adapter

Adapts any working document into audience-specific versions for Leadership, Engineering/Team, and Client — applying the right framing, length, and vocabulary for each reader without rewriting from scratch.

Target audience: product managers, team leads, project managers, business analysts.

---

## Triggers

**English:** "adapt document", "stakeholder adapter", "create executive version", "make a client version", "rewrite for audience", "tailor this for", "I need different versions of this document", "adapt for leadership", "create team version", "prepare versions for different audiences"

**Russian:** «адаптируй документ», «перепиши для аудитории», «сделай версию для руководства», «сделай версию для команды», «сделай версию для клиента», «адаптируй для стейкхолдеров», «разные версии документа», «подготовь версии для разных аудиторий»

---

## Language Detection

Detect the language of the **source document** — produce adapted versions in that language.
If the user explicitly requests a different language, use it.
If the source document language is unclear, use the language of the user's request.

---

## Input

**Required:** source document — pasted as text in the conversation, or provided as a local file path (.md or .txt).

**Optional:**
- Target audience selection (if not provided, ask via AskUserQuestion)
- Document type (status update, PRD, proposal, meeting notes, other)
- Key message that must appear in every adapted version

---

## Output

One clearly labeled section per selected audience, presented in chat.

Optionally, files saved to the working directory on user request:
`stakeholder-adapter-[audience]-YYYY-MM-DD.md`

---

## Instructions

### Step 0 — Extract context from the trigger

Before asking questions, check what the user already provided in their message:
- Document text included → extract it
- Target audiences mentioned (e.g., "for leadership and the client") → extract them
- Document type mentioned → extract it

Proceed to Step 1 with only the **missing** information.

### Step 1 — Collect missing inputs

If the source document was **not** provided in the trigger, ask the user to paste it. Do not proceed without source content.

If target audience, document type, or key message are unknown, use a **single AskUserQuestion call** to collect them:

**Q1 — Which audience versions do you need?** *(multiSelect: true)*
- "Leadership / Executives"
- "Engineering / Team"
- "Client / External partner"
- "All three"

**Q2 — What type of document is this?** *(multiSelect: false)*
- "Status update / progress report"
- "Feature spec / PRD"
- "Proposal / business case"
- "Meeting notes / summary"
- "Other"

**Q3 — Is there a key message that must appear in every version?** *(multiSelect: false)*
- "No specific requirement"
- "Yes — I'll type it below"

### Step 2 — Validate the document

| Condition | Action |
|-----------|--------|
| Document ≤ 3 sentences | Proceed; note: "Short input — adapted versions will be brief" |
| Document in a language different from the UI language | Detect language; produce versions in source language; note this at the top |
| File path provided but file not found | Stop: "File not found at [path]. Paste the document text directly." |
| Unsupported file format (.docx, .pdf, .xlsx) | Stop: "Unsupported format. Paste the document text or use a .md / .txt file." |
| No document provided after prompting | Stop: "No source document provided. Paste the text to proceed." |

### Step 3 — Generate adapted versions

Produce one labeled section per selected audience. Apply these rules:

---

#### Leadership / Executives

**Goal:** Enable a quick decision or provide clear business context in minimal reading time.

- **Lead with:** business impact, decision needed, or key metric
- **Length:** 25–35% of the original
- **Include:** risks and mitigations (high level), timeline (milestones only), resource/budget implications if present, one clear "Action required:" or "For information:" line at the top
- **Remove:** implementation details, technical terms, internal process steps, task-level specifics
- **Format:** short paragraphs; up to 5 bullet points for key data points; close with an explicit next action or status

---

#### Engineering / Team

**Goal:** Give the team everything they need to act without hunting for information.

- **Lead with:** what needs to be done and by when
- **Length:** equal to or longer than the original if technical context was thin
- **Include:** technical details, dependencies, blockers, acceptance criteria, task-level timeline with concrete dates
- **Remove:** business justification that has no bearing on implementation; stakeholder-facing language
- **Format:** structured; use tables for task/owner/status where useful; use concrete deadlines, not ranges

---

#### Client / External partner

**Goal:** Communicate outcomes and value without exposing internal workings.

- **Lead with:** what was delivered or what will be delivered
- **Length:** 30–40% of the original
- **Include:** outcomes and value, timeline (delivery dates, not internal milestones), clear next steps or ask
- **Remove:** internal metrics, cost/margin data, team names, process details, technical implementation
- **Flag (don't remove automatically):** if a section appears to contain sensitive internal data, add: `⚠ Review before sending: this section may contain internal information`
- **Tone:** professional, positive, confident; no jargon or acronyms
- **Format:** clean prose; close with "**Next steps:**" section

---

### Step 4 — Apply key message check

If the user provided a key message in Q3: verify it is reflected (verbatim or semantically equivalent) in each generated version. If it was omitted from a version, reinsert it in the most natural position.

### Step 5 — Present output

Output all versions sequentially, separated by `---`. Each version is headed with `## Version for [Audience]`.

After presenting versions, ask:
> "Would you like me to save these as separate files?"

If yes: write one `.md` file per version to the current working directory:
`stakeholder-adapter-leadership-YYYY-MM-DD.md`, `stakeholder-adapter-team-YYYY-MM-DD.md`, `stakeholder-adapter-client-YYYY-MM-DD.md`

---

## Edge Cases

| Condition | Behavior |
|-----------|----------|
| Only one audience selected | Generate one version; same quality and structure |
| Original document already targets one specific audience | Note which; adapt accordingly for the others |
| Very long document (2000+ words) | Process fully; if the leadership version exceeds 300 words, offer a condensed version (max 150 words) |
| User requests an unlisted audience (e.g., "investors") | Map to nearest category (investors → Leadership); note: "Adapting for investors using Leadership/Executive framing" |
| Mixed-language document (EN + RU sections) | Process in full; produce adapted versions in the dominant language; note the mix |

---

## Constraints

- Does not rewrite from scratch — adapts and reframes existing content only
- Does not add invented facts, metrics, or commitments not present in the original
- Does not automatically remove sections from the client version — flags sensitive data instead
- Does not replace stakeholder review — the user is responsible for approving before sending
