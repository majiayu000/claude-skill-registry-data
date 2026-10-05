---
name: brain-ingest
version: 1.0.0
description: "Pull facts from company sources (email, Google Drive, SharePoint, PDFs, decks, docs, meeting notes) into brain files, with a source on every fact and approval before anything is written. Trigger with /brain-ingest or when the user mentions 'ingest,' 'import this into the brain,' 'pull from Drive,' 'pull from SharePoint,' 'pull from my email,' 'update the brain from this doc,' 'mine these files,' or drops documents in incoming/ after setup."
---

# Brain Ingest

Turn scattered company material into brain-file updates. Works with any source the agent can read: files in `incoming/`, a knowledge-source folder, or whatever connectors this runtime has (email, Google Drive, SharePoint, OneDrive, Slack, Granola, and so on). Run it as often as you like. The brain grows a batch at a time.

---

## Workflow

### Step 1: Pick the sources

Ask what to pull from, if the user hasn't said:

> What should I pull from? A file or folder, a Drive or SharePoint location, an email search, or "everything in incoming/"?

- **Connector sources:** use the connectors available in this session. If the user names a source with no connector, say so and suggest exporting the files to `incoming/` instead. Don't guess at APIs.
- **Searches:** narrow before reading. Search by topic, sender, folder, or date range, list the hits (title, owner or sender, date), and let the user confirm which to read. Never bulk-read a whole mailbox or drive.
- **Files:** read PDFs, decks, docs, spreadsheets, and images with whatever file-reading ability the runtime has. If one can't be read, say which and move on.

Keep a list of what you read, with a locator for each: a file path, document URL, or email subject + sender + date. That locator becomes the source citation.

### Step 2: Extract

For each source, pull out only what a brain file can use:

- Product facts, numbers, customer names, funding, team → `truth.md`
- Positioning, pillars, value props, ICP → `positioning-and-messaging.md`
- Competitors, win/loss reasons → `competitive.md`
- Buyer roles, pains, priorities → `personas.md`
- Features and technical detail → `capabilities.md`
- Customer scenarios and outcomes → `use-cases.md`
- Verbatim buyer phrasing → `audience-language.md`
- Sales motion, objections, stall points → `customer-journey.md`
- Discovery questions → `qualifying-questions.md`
- Industry trends and news → `market-signals.md`
- Boilerplate, bios, pitches → `tactical-assets.md`
- Colors, fonts, logo rules → `brand-guide/brand-guide.md`

Skip anything that fits nowhere. Leave out personal, HR, legal, and financial-detail content even when it's in the source.

### Step 3: Compare against the brain

Read each target brain file before proposing changes. Sort every extracted item into one of:

- **New:** fills a `[FILL IN]` or adds something absent
- **Confirms:** matches what's there (just report the count)
- **Conflicts:** disagrees with the brain or with another source
- **Stale?:** the source is older than what the brain says, or looks superseded (old deck, draft, pre-rebrand)

### Step 4: Propose, then write on approval

Show the proposal grouped by brain file:

```
truth.md
  + Team size: 140 employees
      source: Drive › Board deck Q3 (2026-08-12)
  ! Funding: brain says "$18M Series A", source says "$30M Series B"
      source: email "Series B close" from CFO (2026-09-02)

personas.md
  + New persona: IT Director — owns vendor consolidation
      source: SharePoint › Sales › Discovery guide.docx
```

Ask the user to approve, edit, or reject each item, or approve a file's items together. Ask them to resolve every conflict. Never resolve one yourself.

Then write only the approved items:

- Replace the matching `[FILL IN]`, or add to the right section in the file's existing format.
- Put the source right after the fact as an HTML comment: `<!-- source: Drive › Board deck Q3, 2026-08-12 -->`. It stays out of rendered output and lets a later reader trace where the fact came from.
- Mark anything the user approved but wasn't sure about with `[VERIFY]`.

### Step 5: Wrap up

Report what changed, file by file, and what was skipped. Then run `/brain-health` to show what's still empty, and suggest sources likely to fill it ("personas.md is still thin. Sales call recordings or a discovery guide would help").

---

## Rules

- **Approval before every write.** Same rule as the rest of `/brain/`. Sources are raw input, not verified claims.
- **Every fact gets a source.** No source, no write.
- **Read-only on sources.** Never edit, move, label, reply to, or delete anything in email, Drive, SharePoint, or a knowledge source.
- **Most recent and most authoritative wins, but the user decides.** A signed-off deck beats a draft; a recent email beats an old one. Flag it, don't pick.
- **Don't copy sources wholesale.** Extract facts and short phrases. Never paste whole documents or email threads into brain files.
- **Keep it private.** Don't quote names or internal discussion from email in a proposal unless it's the fact itself.

## Related Skills

- **brain-health**: Shows which brain files need filling and what to gather for them
- **product-marketing**: Builds positioning, personas, and competitive files once raw facts are in
- **tone-mapping**: Use instead for voice-and-tone and voice-samples, which need writing samples, not facts
- **design-extract**: Use instead for the brand guide when you have a live website
- **granola**: Pulls meeting notes into `incoming/` for ingest

## Learnings

<!-- Updated by /reflect in your instance. Promote stable patterns to the main skill body. Ships empty. -->
