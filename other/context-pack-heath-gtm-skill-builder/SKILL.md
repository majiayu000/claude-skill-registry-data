---
name: context-pack
description: Turn a cold start into a warm one. Build a single orientation document for a project, account, or workspace, what it is, where things live, the decisions made so far, the open items, and the next move, so a new session or a new teammate is productive in minutes instead of days. Trigger on "get me up to speed", "onboard someone to this", "what's the context here", "brief a new session", "orient me on this account", or any cold-start on work already in motion.
---

# Context Pack

## What this does
Builds one document that orients whoever picks up the work next, a new AI session, a new teammate, or you in three weeks. It answers the five questions a cold start always asks: what is this, where does everything live, what has already been decided, what is still open, and what happens next. The result is a single pack you can paste into a new session or hand to a person, so nobody re-derives context that already exists.

## What you'll need
You do not need to connect anything to get value today. Point it at the work and it runs now. Connect the tools below and it pulls the scattered pieces together for you.

- Works today with: whatever you can describe or paste, a project brief, a thread, a folder listing, your own notes on where things stand.
- More powerful connected to a repo or file store: it reads the folder structure and the README so "where things live" is real, not remembered.
- Sharper with a notes or wiki tool: it pulls prior decisions and open items instead of asking you to recall them.
- Sharper with a task tool: it lists the open items with owners and due dates, not just your best guess.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you can describe today and gets more complete as you connect sources. It never invents a decision or a location it cannot see. A gap becomes a question, not a fabricated answer.

- **Bring your data**: paste the brief, the thread, the folder listing. The skill assembles the pack today on what you actually know. No connection required.
- **Connect your tools**: the same skill reads the repo, the notes, the task list, and fills the sections it had to ask about. Same pack, less recall, fewer blanks.
- **Just exploring**: no project yet? Get the five-section template and a worked example, so you can see the shape before you fill it.

Every run ends with the one thing that would make the next pack sharper, a source to connect or a section you keep leaving blank.

## Customize this for yourself
This was built for an operator juggling several projects or accounts at once. Set these to your world:

| Set this | What it is | Default / Example |
|---|---|---|
| SUBJECT | the thing being packed | a project, an account, a workspace |
| CODE_HOME | where the build lives | a git repo, a shared drive |
| NOTES_HOME | where decisions and notes live | a notes/wiki tool, a doc folder |
| TASK_HOME | where open items live | a task tool, a checklist |
| DECISION_WINDOW | how far back "decisions so far" reaches | last 90 days (re-tune) |
| STALE_FLAG | when the pack itself needs a refresh | 14 days since last update |

Point it at your sources. The five questions do not change. Where the answers live is yours.

## The method

### The five questions (fixed order)
Every pack answers these, in this order, no exceptions.
1. **What is this** one paragraph a newcomer could repeat back correctly.
2. **Where things live** the map: build, docs, data, credentials-by-reference (never the secret itself).
3. **Decisions so far** the calls already made, each with the one-line why, most recent first.
4. **Open items** what is unresolved, who owns it, what it is waiting on.
5. **Next move** the single most important thing to do next, named plainly.

### Where-things-live map
List the real locations, not "the usual place." A path, a link, a tool name. If a location is a guess, mark it a guess. Point to where a credential is stored, never paste the credential.

### Decisions-so-far digest
Pull the decisions that shaped the current state and give each a one-line reason. If a decision log exists, cite it. If not, this section is the seed of one, and the skill will say so.

### Open-items pass
Every open item gets an owner and a blocker if it has one. "Someone should" is not an owner. An item with no owner is itself flagged.

### Next-move call
End on one move, not a menu. The pack is useless if the reader still has to decide where to start.

## Quality gates
- Nothing is written or saved anywhere without your explicit approval. The pack is drafted for you to place; it does not touch a repo, a wiki, or a task tool on its own.
- No invented locations. A guessed path is labelled a guess, not stated as fact.
- No secret in the pack. Credentials are referenced by where they live, never pasted.
- The next move is exactly one item, named, not a list to triage.

## Output (example)
```
CONTEXT PACK · Northwind onboarding automation · updated today

WHAT THIS IS
  A workflow that enriches new signups and routes them to the right owner.
  Runs nightly. Feeds the account list the AE team works each morning.

WHERE THINGS LIVE
  Build      a git repo, /automations/onboarding
  Docs       a notes tool, "Northwind onboarding" space
  Data       a shared sheet, "signups-raw" tab
  Secrets    stored in the team vault (referenced, not pasted)

DECISIONS SO FAR
  - Route by company size, not persona. Personas were too noisy. (last week)
  - Nightly, not real-time. Real-time tripled the API cost for no lift.

OPEN ITEMS
  - Dedupe on domain still manual. Owner: you. Waiting on: a rule spec.
  - Owner for EU signups undecided. Owner: unassigned (flagged).

NEXT MOVE
  Write the dedupe rule spec so the last manual step can be automated.
```

## Where the inputs come from
DECISION_WINDOW (90 days) and STALE_FLAG (14 days) are defaults, not laws. A slow-moving account can reach back further; a fast build should refresh sooner. The five questions are fixed. The windows are yours.

## Example chat
Here is the skill running on a real cold start.

**You:** I'm handing the Northwind onboarding automation off to a teammate. Build the context pack.

**Claude:** Pack's built, and it surfaced one unassigned item before your teammate would have found it the hard way.
```
DECISIONS SO FAR
  - Route by company size, not persona. Personas were too noisy.
  - Nightly, not real-time. Real-time tripled the API cost for no lift.

OPEN ITEMS
  - Owner for EU signups undecided. Owner: unassigned (flagged).
```
That EU signups gap would have sat silent until someone asked "wait, who owns this," probably at a worse time than now. Naming it unassigned up front means your teammate inherits a known gap, not a hidden one. One sharpener: connect your notes tool so decisions get pulled straight from the record instead of from what you can recall today.

**You:** Good catch. What's the single next move you'd put at the top?

**Claude:** One move, not a list.
```
NEXT MOVE
  Write the dedupe rule spec so the last manual step can be
  automated.
```
That's the one thing blocking the automation from running fully hands-off, everything else on the open-items list can wait a week. One sharpener: connect your task tool so open items carry a real owner and due date instead of "you" by default.

## Go further
The read is step one. Here's where an operator takes it once the manual version proves out.

- **Keep the pack alive, not a snapshot.** Point a scheduled Claude task at your repo and notes tool weekly and regenerate the pack so it never goes stale past the flag window.
- **Make it the standard hand-off ritual.** Require a fresh pack before any account or project changes owners, posted to Slack so the new owner starts oriented on day one.
- **Chain it into onboarding.** Feed the pack straight into your new-hire or new-teammate onboarding flow so context transfer stops depending on a meeting that may not happen.

You built the read once; now it runs itself.


## Make it yours
Fork it. Add a "risks" section, a "who to ask" section, a glossary. Cut what you never read. The point is not a template someone else loves. It is the pack that gets your next session productive in one paste. Built by an operator. Customize it, break it, make it better.
