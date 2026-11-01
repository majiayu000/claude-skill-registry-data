---
name: stakeholder-map
description: "This skill should be used when the user wants to map the stakeholders, decision rights, and communication structure of an AEC project. Trigger on 'stakeholder map', 'who decides what', 'project stakeholder analysis', 'RACI matrix for this project', 'map the stakeholders', 'governance plan', or pasted project context where governance, sign-off authority, or communication cadence is the question. Generates a structured stakeholder map markdown in `docs/stakeholders/` and appends to the project stakeholder index."
license: MIT
metadata:
  title: "Stakeholder Map"
  summary: "Map who decides what, and who talks to whom"
  discipline: "practice-contracts"
  tags: "Pre-Design"
---


# Stakeholder Map


## Overview


Build a stakeholder map for a North American AEC project — identify all stakeholders across six categories, assign RACI roles per AIA project phase, document decision rights and communication cadence, and place stakeholders on an influence/interest grid. Output lives in `docs/stakeholders/`.


Aligned with North American AEC practice: AIA B101 / C401 phase definitions, PMI PMBOK stakeholder management, ICRA + ICRA 2.0 for healthcare, and the typical AHJ structure for US/Canadian municipalities.


## Scope and limits — read first


**What this does.** Lists everyone the project has to deal with across six
categories, assigns RACI by phase, records who signs off when and inside what
response time, and places each party on an influence and interest grid. Output
lands in `docs/stakeholders/`.

**What this does not do.**

- **It does not know your project's people.** Names, organisations, and contacts
  come from you. Where a role is required but nobody has been named, the map
  carries the role with the name blank, and that blank is the useful part.
- **It does not settle who decides.** Two parties both claiming sign-off is
  recorded as a finding for the owner to resolve, not resolved here by picking
  one.
- It does not read the contract. Decision rights, review periods, and approval
  gates are whatever your agreement says; the map records what you tell it the
  agreement says.
- It does not know every authority in your jurisdiction. It prompts for named
  departments, and one it cannot name stays an open question rather than
  becoming "the building department".
- It does not manage the project. This is a map made once and revised
  deliberately, not a live directory.

**What you need before starting.** Project type, delivery method, owner type,
and jurisdiction, plus whoever is already known by name. If the agreement sets
review periods or approval gates, have it in front of you.

## When to use


Trigger on:

- Pasted project context with a governance, sign-off, or communication question.
- Explicit asks: "stakeholder map", "RACI matrix", "who decides what", "who needs to be in the room", "map stakeholders for this project".
- Hand-off from `brief-review` when the brief flagged decision-rights gaps.
- Pre-kickoff prep before SD launches.

Do NOT trigger for:

- Brief / RFP review (use `brief-review`).
- Meeting notes structuring (use `meeting-notes-cleaner`).
- Drawing-set review (use `drawing-checklist`).
- Client-facing language translation (use `client-translator`).

## Workflow


### Step 1 — Bootstrap if needed


Check that `docs/stakeholders/index.md` exists. If not:


```bash
python scripts/init_stakeholders_workspace.py
```


### Step 2 — Establish project context


Read `docs/project.md` if it exists for project type, delivery method, jurisdiction, owner type. If missing, ask once for:

- **Project type** — commercial / civic / healthcare / education / residential / mixed-use / industrial. Drives which authorities and consultants are required.
- **Delivery method** — Design-Bid-Build / Design-Build / CM at Risk / IPD / Progressive Design-Build. Drives the Construction-side stakeholders and timing of GC entry.
- **Owner type** — private / public-municipal / public-state / public-federal / institutional (university, hospital system) / nonprofit. Drives governance gates and public engagement.
- **Jurisdiction** — city + state. Drives AHJ list (some jurisdictions have unique authorities — NYC DOB/FDNY, CA HCAI for hospitals, DSA for K-12, NYC SCA, GSA for federal).

### Step 3 — Identify stakeholders across six categories


Load `references/stakeholder_categories.md` for the full taxonomy. Quick reference:

1. **Owner-side** — owner, owner's rep / PM, end users, finance, board / trustees, legal, IT/security, facilities ops.
2. **Design team** — architect of record (AOR), design architect (if separate), structural, MEP (mechanical / electrical / plumbing / fire protection), civil, landscape, lighting, acoustics, AV/IT, security, code consultant, sustainability/LEED, accessibility, signage/wayfinding, FF&E, kitchen, lab planner, healthcare planner — only the disciplines the project type requires.
3. **Construction** — GC / CMAR / DB lead, key subs (concrete, steel, glazing, MEP), suppliers (long-lead equipment), commissioning agent (if owner-engaged).
4. **Authority Having Jurisdiction (AHJ)** — building department, fire marshal, planning / zoning, ADA / accessibility office, DOT (if curb cut / row impact), utility companies (electric / gas / water / sewer / telecom), environmental (state EPA, EPA region), public health (food service, pools, healthcare), historic preservation (if applicable), school district facilities (if K-12), state agencies (HCAI, DSA, OSHPD-equivalent if healthcare/education in regulated state).
5. **Public / community** — neighbors, community board / neighborhood council, advocacy groups, business improvement district, tribal consultation (if applicable).
6. **Operations / post-occupancy** — facility manager, IT / network, security operations, custodial / cleaning, food service, parking, building engineer.

For each stakeholder, capture: name (or role if person unknown), organization, role, primary contact channel.


### Step 4 — Assign RACI per AIA phase


Load `references/raci_guide.md` for guidance on applying RACI to AEC phases (Pre-design, SD, DD, CD, Bidding/Procurement, CA, Closeout).


For each stakeholder × phase cell:

- **R (Responsible)** — does the work
- **A (Accountable)** — single owner of the decision (only one A per decision)
- **C (Consulted)** — two-way input before decision
- **I (Informed)** — one-way notification after decision

Common pitfalls (from `references/raci_guide.md`): assigning multiple A's to one decision, confusing R with A, omitting AHJ from C in jurisdictions where pre-application consultation is standard.


### Step 5 — Document decision rights & communication cadence


Beyond RACI, capture:

- **Sign-off authority** — who signs off at end of SD, DD, CD, IFC. Single person or committee vote.
- **Decision SLA** — owner response time commitment (typical: 5 business days for routine, 10 for board-level).
- **Meeting cadence** — weekly OAC, biweekly user group, monthly executive review, quarterly board.
- **Escalation path** — when to escalate, to whom.

### Step 6 — Place stakeholders on influence/interest grid


Classic 2x2:

- **High influence + high interest** → manage closely (frequent touchpoints, deep engagement)
- **High influence + low interest** → keep satisfied (periodic high-level updates)
- **Low influence + high interest** → keep informed (regular updates, encourage feedback)
- **Low influence + low interest** → monitor (minimal effort)

The grid drives communication strategy, not necessarily project authority.


### Step 7 — Write the stakeholder map


Read `assets/stakeholder-map-template.md`, fill placeholders. Filename:


`docs/stakeholders/<YYYY-MM-DD>-<slug>.md`


Slug rule: lowercase, `[^a-z0-9-]` removed, max 40 chars, derived from project name (`acme-hq-stakeholders`, `westside-school`). If a map with the same date+slug already exists, suffix `-<n>`.


Use the Write tool. English only.


### Step 8 — Update the stakeholder index


```bash
python scripts/append_to_index.py \
  --date 2026-05-07 \
  --slug acme-hq-stakeholders \
  --project-type commercial \
  --delivery-method dbb \
  --owner-type private
```


The script appends a row to `docs/stakeholders/index.md`. Do NOT edit the index manually.


### Step 9 — Report


Tell the user:

- Path to the stakeholder map.
- Top 3 high-influence-high-interest stakeholders to engage first.
- Any decision rights gaps (cells where Accountable is missing).
- Any AHJ that should receive a pre-application consultation before SD launches.

## Rules

- Every decision has exactly one A. If two parties claim sign-off, that is a finding, not a fact — record it and recommend resolution.
- AHJs are stakeholders. They are not just "constraints" — they need consultation, RFI cycles, plan review submissions on a schedule.
- Jurisdiction-specific authorities must be named (e.g., "California HCAI" not "state hospital authority"; "NYC DOB" not "building department").
- For public-sector owners, identify the procurement officer and the elected/appointed sign-off body separately. They are different stakeholders with different decision rights.
- When the owner is a corporation, name the legal entity (the contracting party) separately from the operational owner (the day-to-day client). They may diverge on decisions.

## Anti-patterns

- Generic "city" or "the AHJ" entries — name the department.
- RACI matrix where every cell is filled with R / A / C / I letters in pretty patterns. Most stakeholders are not C or I on most decisions; leave cells blank when there is no role.
- Treating subs as undifferentiated. Identify the trade leads that drive long-lead procurement (mechanical, electrical, glazing, elevator, switchgear).
- Missing post-occupancy stakeholders. The facility manager has decision rights on FF&E and operational systems that affect CD.
- Editing `index.md` manually instead of using `append_to_index.py`.

## Resources

- `scripts/init_stakeholders_workspace.py` — bootstrap `docs/stakeholders/` and the stakeholder index
- `scripts/append_to_index.py` — append a row to `docs/stakeholders/index.md`
- `references/stakeholder_categories.md` — North American AEC stakeholder taxonomy by project type, with jurisdiction-specific AHJ names
- `references/raci_guide.md` — how to apply RACI by AIA project phase, common pitfalls, decision-type examples
- `assets/stakeholder-map-template.md` — stakeholder map markdown template
