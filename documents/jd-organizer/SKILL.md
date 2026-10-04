---
name: jd-organizer
description: "Reorganize files in the current directory using the Johnny Decimal system. Scans all files recursively, inspects images and PDFs when unclear, then guides the user through defining scope, discovering categories, and building a numbered JD structure — one confirmed step at a time. Use when the user wants to organize, restructure, or apply Johnny Decimal to a folder."
---

# Johnny Decimal Organizer

Guide the user through building a Johnny Decimal system for their current directory. Scan first, think second, propose third, move last — and confirm at every gate.

<HARD-GATE>
Do NOT move, rename, or delete any files until the user has reviewed and approved the full reorganization plan. Every phase ends with an explicit user confirmation before proceeding to the next. This applies no matter how obvious a change seems.
</HARD-GATE>

## What Is Johnny Decimal?

Johnny Decimal (JD) is a file organization system built on three levels:

```
10-19 Area name          ← broad life/work domain (max 10 areas, numbered in tens)
  11 Category name       ← specific type of work within the area (max 10 per area)
    11.01 ID name        ← the individual thing (folder where files actually live)
      file.pdf           ← files live ONLY inside ID folders, never in areas/categories
```

**Rules that cannot be broken:**
- Files live only in ID folders (e.g. `11.01 Singapore trip`), never directly in area or category folders
- IDs increment: `11.01`, `11.02`, `11.03` — no semantic meaning, just creation order
- Max 1 level of subfolders inside an ID folder
- 00-09 is reserved for the system index
- Areas are broad ("areas of life"), categories are specific ("type of work within that area")
- Prefer fewer, broader categories — every category is a future decision to make

**Naming conventions:**
- Sentence case, spaces as word separators
- Dates: `YYYY-MM-DD - Title` or `YYYY-MM - Title`
- Versions: `v1 - Title`, `v2 - Title`
- Separator between date/version and title: ` - ` (space-dash-space)
- No `&` or apostrophes in folder names (break shell commands)
- No JD ID in filenames (it's already in the folder)
- `z`-prefix marks unused/retired folders — they sort to the bottom and signal "don't touch"

---

## Checklist

Complete these phases in order. **Do not skip or combine phases.**

1. **Scan the directory** — build a mental map of what exists
2. **Define scope** — ask what's in and what's out (one question at a time)
3. **Discovery** — present discovered "things" as a flat list for the user to react to
4. **Areas** — propose broad groupings, confirm before naming
5. **Categories** — propose specific types within each area, confirm
6. **Numbering** — assign JD numbers to agreed structure, show full tree
7. **ID assignment** — map each existing file/folder to a JD ID
8. **Plan review** — write the plan to a file, ask user to read it
9. **Execute** — move files only after explicit go-ahead

---

## Phase 1: Scan

Recursively list all files and folders in the current directory. Use `find` or `ls -R` or the Glob/Read tools as appropriate. Skip:
- `node_modules/`, `.venv/`, `.next/`, `dist/`, `.git/`
- `.DS_Store`, `.stversions/`
- Anything already explicitly marked `OUT OF SCOPE` by the user

If you encounter an image or PDF whose purpose is unclear from its filename, read/view it to determine what it is before moving on. Announce when you're doing this:
> "I'm going to look inside `[filename]` to understand what it is."

Build an internal understanding of:
- What broad life/work domains are represented?
- What are the rough "types of things" present?
- Anything already numbered (might be an existing JD system to preserve)?
- Any folders deeper than 3 levels (potential over-nesting to collapse)?
- Any files sitting loose at the top level (orphans)?

---

## Phase 2: Scope

**One question at a time.** Start with:

> "Before we design any structure, I want to make sure we agree on what belongs in this system. Looking at what I found, I'll walk you through a few quick questions.
>
> First: are there any folders or files I should leave completely untouched — even if they look disorganized? For example, archived projects, things managed by another tool, or anything you'd rather not move."

Wait for their answer. Then ask:

> "Is this system meant to cover [list the broad domains you observed], or is there anything here that should live somewhere else entirely and just needs to be moved out?"

If they confirm scope, summarize it:
> "Got it. **In scope:** [list]. **Out of scope:** [list]. I'll build the JD system only around what's in scope."

Do not proceed until scope is confirmed.

---

## Phase 3: Discovery

Present a flat "sticky note" list — every distinct *thing* you found, one per line, stripped of implementation detail. This is NOT a proposed structure, just an inventory.

Format:
```
Things I found in [directory]:

• Tax returns (2022–2024)
• Health insurance documents
• Passport scan
• YouTube channel assets — thumbnails, scripts, channel art
• OrganizedTiger project — wireframes, pitchdeck, contracts
• Software receipts / license emails
• Bank statements
• Resume and portfolio pieces
• Travel itineraries and hotel confirmations
• Personal photos (various years)
• ...
```

Then ask:
> "Does this list feel complete? Anything I missed, or anything here that surprises you?"

Incorporate any corrections, then move to Phase 4.

---

## Phase 4: Areas

**Areas are broad.** Think "areas of your life." A typical personal system has 3–6.

Propose 2–3 possible area structures. Present them as options:

```
Option A — by life domain
  10-19 Projects
  20-29 Finance
  30-39 Personal records
  40-49 Media and creative

Option B — by frequency of use
  10-19 Active work
  20-29 Reference and records
  30-39 Archive

Option C — [third variant based on what you observed]
```

Then ask:
> "Which of these feels most natural to you, or would you like to mix and match? You don't have to pick one wholesale — tell me what resonates."

Iterate until the user is satisfied. Do not assign numbers yet.

**Guidance to give the user:**
- "Think big. Narrow areas run out fast. You only get ten."
- "You can always split an area later, but merging two you regret is harder."
- "Ask yourself: 'Where would a stranger look for my health insurance?'"

---

## Phase 5: Categories

Take each confirmed area and propose 3–6 categories within it. Work through one area at a time.

```
For "20-29 Finance", I'm thinking:

  • Tax
  • Banking and accounts
  • Expenses and receipts
  • Contracts and agreements
  • Investments
  • Insurance

Does that cover it, or would you merge/split anything?
```

Key reminders to apply:
- If a category has only one item right now, ask: "Can you imagine the next thing that would go here?" If not, consider merging it.
- Avoid categories so specific they force impossible decisions later ("Home insurance" vs "Car insurance" vs "Insurance" — just use "Insurance").
- Duplicate category names across areas are fine as long as the area provides context.

Confirm each area's categories before moving to the next.

---

## Phase 6: Numbering

Once all areas and categories are confirmed, assign numbers. Present the full numbered tree:

```
10-19 Projects
  11 Software development
  12 YouTube channel
  13 E-commerce and reselling

20-29 Finance
  21 Tax
  22 Banking
  23 Expenses and receipts
  24 Contracts

30-39 Personal records
  31 Identity documents
  32 Health
  33 Career

40-49 Media and creative
  41 Photography
  42 Design assets
```

Rules for number assignment:
- 00-09 reserved for index (create `00 Index` category here)
- Assign numbers in a logical reading order if a natural sequence exists, otherwise just increment
- Leave gaps is fine (skip 14, go to 15) if you anticipate expansion
- Don't over-think it — numbers carry no semantic weight

Ask:
> "Does this numbering feel right? Any areas or categories you'd like to renumber, rename, or reorganize before I map files to IDs?"

Do not proceed until the full tree is approved.

---

## Phase 7: ID Assignment

Now map every file and folder you found to a JD ID. For each item:

1. Determine which category it belongs to
2. Assign the next available ID number within that category (start at `.01`)
3. Propose a name for the ID folder following naming conventions

Present this as a table or structured list:

```
Proposed ID assignments:

  21.01 2024 tax return
    ← currently: "Taxes/2024 tax return.pdf"

  21.02 2023 tax return
    ← currently: "Old stuff/taxes 2023.pdf"

  22.01 Chase checking account
    ← currently: "bank/chase statements/"

  31.01 Passport
    ← currently: "Documents/passport scan.jpg", "Desktop/passport-old.pdf"
```

Flag anything ambiguous:
> "I'm not sure whether `contracts - freelance.pdf` belongs in `24 Contracts` or `13 E-commerce`. Which feels right to you?"

Ask one ambiguity question at a time. When resolved, continue.

When all items are mapped, ask:
> "Does this assignment look right? Anything you'd rename, re-categorize, or skip?"

---

## Phase 8: Plan Review

Write the complete reorganization plan to a markdown file in the current directory:

**Filename:** `jd-reorganization-plan.md`

The file should contain:
1. The full numbered JD tree (areas → categories)
2. Every proposed `mv` operation in the form:
   ```
   FROM: path/to/current/file.pdf
   TO:   21-29 Finance/21 Tax/21.01 2024 tax return/2024 tax return.pdf
   ```
3. Any files that will be left in place (out of scope, already correct, unclear)
4. Any files proposed for deletion (duplicates, `.DS_Store`, etc.) — list separately and do NOT delete until user confirms

Then say:
> "I've written the full plan to `jd-reorganization-plan.md`. Please read through it carefully. When you're ready, tell me:
>
> - Approve — and I'll start moving files
> - Change [X] — and I'll update the plan
> - Cancel — and I'll leave everything as-is"

**Do not touch any files until the user explicitly says to proceed.**

---

## Phase 9: Execute

Once the user approves, execute moves one area at a time. After each area:

> "Finished moving files into `10-19 Projects`. Moving on to `20-29 Finance` next — okay?"

This gives the user a chance to pause if something looks wrong.

After all moves:
1. Create `00-09 Index/00.00 Index.md` with the full JD tree as a plain-text index
2. Clean up any now-empty folders (ask first: "These folders are now empty: [list]. Delete them?")
3. Delete `jd-reorganization-plan.md` only if user wants it gone (offer to keep it as a reference)

---

## Key Principles

- **One question per message** — never stack multiple questions
- **Multiple choice preferred** — easier to answer than open-ended
- **The system serves the user** — if they want to break a rule, explain the trade-off, then do what they want
- **Scope creep is the enemy** — if something is out of scope, say so and don't include it
- **Fewer, broader categories always wins** — resist the urge to create a category for every edge case
- **Confirm before acting** — even after approval, announce each step as you do it
- **Ambiguity is normal** — when a file could fit two places, ask. Don't guess silently.
- **Never delete without explicit permission** — always list proposed deletions separately

## Handling Special Cases

**Already has a JD system:**
> "I can see there's already a JD structure here. Do you want me to audit and improve the existing system, or start fresh?"

**Existing structure conflicts with JD rules:**
> "I noticed files saved directly in the `11 Software` category folder (not inside an ID). JD requires everything to be inside a numbered ID like `11.01 Project name`. I'll fix these as part of the plan."

**Enormous number of files (100+):**
Work area by area. Don't try to present 200 items at once — present one area's inventory, confirm it, then move on.

**User wants to skip a phase:**
> "Happy to move faster — but I want to make sure we don't design a system around incomplete information. Can we do a quick [phase]? It should take less than two minutes."

**User is unsure about a naming decision:**
> "There's no wrong answer. Pick whatever feels natural to your brain, because you're the one who has to remember it. You can always rename later without breaking the system."
