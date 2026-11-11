---
name: business-starter
description: "Sets up the four files that make Claude know a business: a CLAUDE.md about the business (what you do, who you sell to, offers, voice, rules), a context/ folder (pricing, offers, customers) Claude looks things up in instead of guessing, a memory/ file where every correction is saved so mistakes are not repeated, and a skills/ folder for jobs you walk it through once. Interviews the owner, fills the templates, never invents a price or fact. Use when an owner says Claude does not know their business, keeps getting details wrong, or says \"set up my business\", \"business starter\", \"remember this\" or \"don't do this anymore\"."
---

# Business Starter

Four parts that turn Claude from a general chatbot into something that knows your business:

| Part | What it holds | When Claude reads it |
|---|---|---|
| `CLAUDE.md` | What you do, who you sell to, your offers in one line each, your voice, your rules | Every session, automatically (Claude Code reads it on start) |
| `context/` | The details: `pricing.md`, `offers.md`, `customers.md` | When a task needs them. CLAUDE.md tells it where to look |
| `memory/memory.md` | Every correction you give: "don't do this anymore", "do it this way" | Every session (imported from CLAUDE.md), and appended to after each correction |
| `skills/` | Jobs you walk it through once, saved as steps it repeats | When a request matches a skill's description |

Templates are in `templates/`. This skill copies them into your business folder and fills them in with you.

Not the same as the root [`CLAUDE.md`](../../CLAUDE.md) in this repo: that one is my orchestrator setup (subagents, workstreams, focus list). This one is about your business. You can use both: put this one in your business folder, and copy the orchestrator rules in underneath if you want them.

## What you need

- **Claude Code** (best): a folder for your business, e.g. `~/Business`. You start Claude there with `cd ~/Business && claude`.
- **Claude.ai** (fallback): a Project. Paste the filled CLAUDE.md into the Project instructions, upload the `context/` files to Project knowledge. Claude.ai cannot write to Project files, so for memory it prints the new line and you paste it into `memory.md` and re-upload.

## Setup (`start`)

1. Ask where the business folder is. If it already has a CLAUDE.md, read it and offer to merge, never overwrite.
2. Copy `templates/` into the folder: `CLAUDE.md`, `context/`, `memory/`, and create an empty `skills/` folder (in Claude Code the working folder is `.claude/skills/`; see "Skills" below).
3. Interview in two rounds. Accept "skip" and leave `<TODO: ...>` in place of anything skipped.

   Round 1
   1. What does the business do, in one sentence a customer would say?
   2. Who buys from you? (type of person or company, size, where they find you)
   3. What do you sell? Name, price, what is included, for each offer.
   4. What do you never do or never sell?

   Round 2
   5. How do you talk to customers? Paste 2 or 3 messages or posts you wrote yourself.
   6. Words, claims or topics Claude must never use.
   7. Tools you use (email, payments, booking, CRM) and which ones Claude may read.
   8. Who else works in the business and what they own.

4. Write the answers into the templates. Prices and offer details go in `context/`, not in CLAUDE.md. CLAUDE.md stays under about 80 lines.
5. Show every file back. Owner confirms or corrects. Corrections go straight into the files.
6. Print the test: "Start a new session in this folder and ask: what do we sell, to whom, and what does the main offer cost? It should answer from the files and name the file."

## Commands

| Command | Does |
|---|---|
| `start` | Setup above |
| `remember <feedback>` | Appends one line to `memory/memory.md` (format below), shows the line |
| `update <pricing / offers / customers>` | Edits that context file, shows the diff, adds a dated line to its "Changes" list |
| `check setup` | Reads all four parts and lists gaps: `<TODO>`s left, prices in CLAUDE.md instead of context/, memory lines that contradict each other, CLAUDE.md over 80 lines |

## Memory rules

- Any correction from the owner ("no, not like that", "stop doing X", "always do Y") becomes one line in `memory/memory.md` in the same reply, without being asked. Say "Saved to memory: ..." so the owner sees it.
- Format: `YYYY-MM-DD | rule | why (owner's words, short)`. One rule per line, written as an instruction.
- Before adding, check for an older line that says the opposite. Replace it and say so; never keep both.
- Keep it short. Over about 60 lines, offer to group duplicates. Facts about the business (a new price, a new offer) go in `context/`, not memory.

## Skills

A skill is a folder with a `SKILL.md`: a name, a one-line description of when to use it, and the steps. Claude Code finds skills in `.claude/skills/` in the folder you start it in, or `~/.claude/skills/` for every folder.

- Ready-made ones: copy any folder from this repo's `skills/` (for example `monday-numbers`, `warm-lead`, `happy-customer`).
- Your own: walk Claude through a job once, then say "turn what we just did into a skill". The `hand-it-off` skill in this repo does this step by step.
- A skill should read `context/` for facts instead of copying prices into itself, so one price change updates every skill.

## Safety rules

- Never invent a price, offer, customer fact or rule. Unknown = `<TODO: ...>` and a question.
- Never put passwords, API keys, bank details or customer personal data in any of these files. Customer files describe types of customer, not named people.
- Merge, never overwrite, an existing CLAUDE.md or memory file.

## End of every run

1. Files created or changed, with paths.
2. `<TODO>`s still open.
3. The test question from step 6.
