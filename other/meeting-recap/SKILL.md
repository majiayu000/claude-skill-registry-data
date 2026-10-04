---
name: meeting-recap
description: Turn a call or meeting into a clean recap and a ready-to-send follow-up. The decisions, the action items with owners and dates, the open questions, and a follow-up note you can send as is. Built for B2B revenue teams, customizable to your notes and your process. Trigger on "recap this call", "meeting notes", "write the follow-up", "what did we agree", "action items from this", or any post-meeting summary request.
---

# Meeting Recap

## What this does
Takes the mess of a call, notes, transcript, or your own scribbles, and turns it into four clean things: what was decided, who owns what by when, what is still open, and a follow-up note ready to send. It is the difference between a meeting that moves and a meeting that evaporates.

## What you'll need
You do not need to connect anything to get value today. Bring your notes and the skill runs now. Connect the tools below and it pulls them automatically and adds context you cannot paste by hand.

- Works today with: your raw notes or a transcript of the call. Paste it or upload a file.
- More powerful connected to a meeting tool: it reads the transcript automatically, no copy-paste.
- Sharper connected to a CRM: pulls the account and deal context so the recap knows who is who.
- Sharper with an email tool: drops the follow-up straight into a draft addressed to the room.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on the notes you give it today and gets more powerful as you connect tools. It never invents a decision or an owner it cannot see. A gap is a prompt, not a guess.

- **Bring your data**: paste or upload your notes or transcript. The skill writes the full recap and follow-up today on your real call. No connection required.
- **Connect your tools**: the same skill reads the transcript automatically and adds context you cannot paste by hand (account history, prior action items, attendees). Same output, less effort, sharper.
- **Just exploring**: no call yet? Get the framework, the exact structure it produces, and a worked example on a sample call, so you can see the shape before you feed it.

Every run ends with the one thing that would make the next recap sharper, a note to capture or a tool to connect.

## Customize this for yourself
This was built for a B2B revenue team running customer and prospect calls. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| MEETING source | where the call lives | a meeting tool, a transcript, your notes |
| CRM | where the recap is logged | Salesforce, HubSpot, a CS platform |
| EMAIL tool | where the follow-up is drafted | your mail client, a sequencing tool |
| OWNER format | how you name owners | first name, email, @handle |
| DUE default | when an undated action is due | before the next meeting (re-tune) |
| TONE | the voice of the follow-up | warm-professional, brief, formal |
| LOG target | where the summary is saved | the account or deal record |

Run any meeting type you like. The skill pulls decisions, owners, and open questions out of your own notes, so point it at your call, not anyone else's.

## The method

### Decisions
What the room actually agreed, stated plainly. A decision is a settled thing, not a topic that came up. If it was discussed but not decided, it belongs in open questions, not here. Do not manufacture agreement the notes do not show.

### Action items with owners
Every action gets an owner and a date. An action item with no owner is a wish, and one with no date never happens. If the notes name neither, flag it as unassigned rather than guessing who or when.

### Open questions
What is still unresolved, and what it is waiting on. This is the list that drives the next meeting. Naming an open question is how a deal or a project keeps moving between calls.

### The follow-up note
A note ready to send to the room: thanks, the decisions, the action items with owners, the open questions, and the next step. In your tone, short enough that people read it. This is the artifact that makes the meeting count.

## Quality gates
- No decision that the notes do not support. A discussed topic is not a decision.
- Every action item has an owner and a date, or is clearly flagged unassigned.
- Owners are named, never "the team." An action everyone owns, no one owns.
- The follow-up is send-ready, not a rough draft the sender has to rebuild.

## Output (example)
```
MEETING RECAP · Acme Corp · discovery call

Decisions
  - Move to a 2-week trial on the two priority use cases.
  - Security review runs in parallel, not as a blocker.

Action items
  - Send trial plan and success criteria        owner: you        by Wed
  - Loop in security for the review              owner: Acme (Priya) by Fri
  - Book the mid-trial check-in                  owner: you        by Thu

Open questions
  - Who signs off on procurement? (waiting on Priya)
  - Budget confirmed for this quarter or next?

Follow-up note (ready to send)
  Hi Priya, thanks for the time today. To recap: we agreed to a
  two-week trial on [use cases], with the security review running
  alongside. I will send the trial plan and success criteria by
  Wednesday and get a check-in on the calendar. Open on my side:
  who owns procurement sign-off. Talk soon.
```
(Names and details illustrative.)

## Where the numbers come from
The due default (before the next meeting) and the follow-up tone are defaults, not laws. They suited a fast B2B sales cycle. If your process runs on hard dates, set them explicitly. If your tone is more formal, change it. The logic does not change. The defaults are yours.

## Example chat
Here is the skill running on a real call, start to finish.

**You:** Recap this discovery call and give me a follow-up I can send now. [pastes transcript]

**Claude:** Decisions, owners, and a send-ready note.
```
Decisions
  - Move to a 2-week trial on the two priority use cases.

Action items
  - Send trial plan and success criteria   owner: you   by Wed
  - Loop in security for the review        owner: Acme (Priya)  by Fri

Open questions
  - Who signs off on procurement? (waiting on Priya)
```
The catch worth naming: "security review runs in parallel" got discussed but I didn't log it as a separate decision, it's folded into the trial decision because that's what the notes actually show was agreed, not two settled things. Manufacturing an extra decision would make the recap look more settled than the room actually was. One sharpener: connect a meeting tool so the transcript comes in automatically and nothing gets lost in the copy-paste.

## Go further
The recap is step one. Here is where an operator takes it once the manual version proves out.

- **Draft the follow-up the second the call ends.** Wire a scheduled Claude task to a meeting tool so the recap and send-ready email generate automatically within minutes of the call finishing.
- **Log action items where they get worked.** Push owners and due dates into Salesforce or a task tool tied to the deal, so "send trial plan by Wed" shows up as a real task, not just a line in a doc.
- **Chase the open questions automatically.** Have a scheduled Claude task check unresolved open questions against the next meeting's notes and flag anything still open after two calls.

You built the recap once, now the follow-through gets tracked too.


## Make it yours
Fork it. Change the structure, the tone, the fields it logs. The point is not to run someone else's recap. It is to run yours, faster. Built by an operator. Customize it, break it, make it better.
