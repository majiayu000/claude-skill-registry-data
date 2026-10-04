---
name: champion-plan
description: Build a champion, do not just hope you have one. It identifies who inside the account can sell for you, arms them with the internal-sell narrative and a one-pager they can forward, and plans the multi-thread so the deal does not rest on one person. Built for B2B sales teams, customizable to your CRM and your deal process. Trigger on "who is my champion", "build a champion", "arm my champion", "this deal is single-threaded", "help them sell internally", or any multi-thread or champion-development request.
---

# Champion Plan

## What this does
Takes an account and turns one interested contact into a champion who sells for you when you are not in the room. It scores who on the deal can actually be a champion, writes the narrative they use to make the case internally, builds the one-pager they can forward without editing, and maps the other threads you need so the whole deal does not hang on a single relationship. One champion is one point of failure; this removes it.

## What you'll need
You do not need to connect anything to get value today. Bring the account and the skill runs now. Connect the tools below and it pulls the context automatically and adds signals you cannot paste by hand.

- Works today with: what you paste about the account. Who you are talking to, their role, what they care about, who else is involved, and where the deal stands. A short list of contacts is enough to start.
- More powerful connected to a CRM: it reads the contact roles, titles, and engagement automatically, so the champion scoring and the thread map match the real account.
- Sharper with a meeting or email tool: pulls who is actually replying and who has gone quiet, so the multi-thread plan is based on real engagement, not the org chart.
- Sharper with an enrichment source: fills in titles, seniority, and reporting lines so you can see who your champion still needs to reach.

## How this runs at your connection level
This skill is never reliant on a connector. It runs on what you tell it today and gets more powerful as you connect tools. It never invents a contact or a relationship it cannot see. A gap is a question it asks you, not a name it makes up.

- **Bring your data**: paste the contacts and context. The skill builds the full champion plan today on your real account. No connection required.
- **Connect your tools**: the same skill pulls the roles, the engagement, and the org detail automatically. Same plan, less effort, grounded in who is really moving.
- **Just exploring**: no live account? Get the framework, the fields it reads, and a worked example on a sample account, so you can see the shape before you bring a real one.

Every run ends with the one thing that would sharpen the next: a role to confirm, a thread to open, a tool to connect.

## Customize this for yourself
This was built for a B2B SaaS org selling into a buying committee. Set these to your stack:

| Set this | What it is | Default / Example |
|---|---|---|
| CRM | your CRM connector | Salesforce, HubSpot, Pipedrive |
| CONTACT ROLES | how you see who is on a deal | OpportunityContactRole, buyer role field |
| CHAMPION traits | what makes a real champion for you | has power or access, feels the pain, will act |
| THREADS_TARGET | how many engaged contacts you want | 3 (re-tune to your deal size) |
| ENGAGEMENT source | where replies and touches live | Task, Event, email or meeting tool |
| ONE_PAGER format | how your champion forwards the case | your template, your brand |
| ENRICHMENT | source for titles and reporting lines | your enrichment connector |

Your definition of a champion is yours. The skill scores against the traits you set, not a generic profile.

## The method

### Identify the champion (score, do not assume)
Not every friendly contact is a champion. Score each contact on three things: do they have power or access to it, do they personally feel the pain you solve, and will they actually spend capital to act. A contact who likes you but cannot move anyone is a coach, not a champion. Name the difference.

### Arm them with the internal-sell narrative
Your champion has to sell this when you are not there, to people you may never meet. Write the case in their language: the problem in the organization's terms, why now, what it costs to do nothing, and what the win looks like for their team. Short enough to say in a hallway.

### Build the one-pager (forward without editing)
Give the champion something they can send up the chain untouched: the problem, the solution, the value, and the ask, on one page in their voice. If they have to rewrite it, they will not send it. Make it forwardable as-is.

### Map the multi-thread (do not rest on one person)
List every role the deal needs on side: the economic buyer, the technical evaluator, the blocker, the coach. Mark who is engaged and who is dark. Every single-threaded deal is one departure away from dead. Plan the next thread to open and who opens it.

### Test the champion (before you rely on them)
Give the champion a small ask that proves they will act: a meeting with their boss, an internal intro, a piece of information only an insider gets. If they deliver, they are real. If they stall, you have a coach, and you plan a second thread now, not later.

## Quality gates
- No contact is called a champion without evidence they have access and will act, not just interest.
- The thread map names the roles that are still dark, never only the ones already engaged.
- The one-pager is written to be forwarded unedited, in the champion's terms, not yours.
- Engagement claims are grounded in real touches where that data is available, and flagged as assumption where it is not.
- Any name or title carried from the account is shown as given or sourced, never invented.

## Output (example)
```
CHAMPION PLAN · Acme Corp (illustrative)

Champion scoring
  Dana (VP Ops)      power: yes   pain: high   will act: proven  -> CHAMPION
  Sam (Analyst)      power: no    pain: high   will act: yes     -> coach
  Priya (Finance)    power: yes   pain: low    will act: unknown -> reach

Thread map (target: 3 engaged)
  Economic buyer   CFO            DARK   <- open next, via Dana
  Technical eval   Sam            engaged
  Champion         Dana           engaged
  Blocker          Security lead  unknown

Next moves:
  1. Arm Dana with the one-pager for the CFO conversation.
  2. Ask Dana for the intro to Finance. That is the champion test.
  3. Open the security thread before it becomes a late surprise.
```

## Where the inputs come from
THREADS_TARGET (3) and the champion traits are defaults, not laws. They suited a mid-market committee sale. The names, roles, and scores above are examples, illustrative only, not real people. The method does not change when your account does. Set the traits and the target to your real buying process and the plan shapes itself around it.

## Example chat
**You:** I've got a good contact at Acme but I'm not sure if she's a real champion or just friendly. Here's who I've talked to. [pastes contacts]

**Claude:** Scored it.
```
Dana (VP Ops)      power: yes   pain: high   will act: proven  -> CHAMPION
Sam (Analyst)      power: no    pain: high   will act: yes     -> coach

Thread map (target: 3 engaged)
  Economic buyer   CFO            DARK   <- open next, via Dana
  Technical eval   Sam            engaged
```
The distinction that matters: Sam feels the pain just as much as Dana, but no power to move budget makes Sam a coach, not a champion. Calling Sam a champion is how deals stall on someone who can't actually say yes.

**You:** How do I know Dana will really carry this internally?

**Claude:** Give her a small test before you rely on her: ask for the intro to the CFO. If she delivers, she's real. If she stalls, you've got a coach and you open a second thread now, not after the deal's already single-threaded and stuck. One sharpener: connect your email tool so the thread map reflects who's actually replying, not just who's listed as a contact, that's usually where a "champion" turns out to have gone quiet.

## Go further
Scoring one account by hand catches the risk before it costs you the deal. Here's the version that watches every open deal at once.

- **Flag single-threaded deals automatically.** Connect Salesforce contact roles to a scheduled Claude task that scans open opportunities weekly and surfaces any deal with only one engaged contact.
- **Catch the champion going quiet.** Wire Gong or your email tool so a champion who stops replying triggers a Slack alert to the rep before the silence becomes a lost deal.
- **Generate the one-pager on demand.** Connect this to your business-case skill so the moment a champion is scored, the forwardable one-pager drafts itself in their voice, ready to send up the chain.

A champion tested once by hand is a habit once it runs on every deal automatically.

## Make it yours
Fork it. Change the traits, the thread target, the one-pager format. The point is not to run someone else's coverage model. It is to make sure your deal never rests on one person again. Built by an operator. Customize it, break it, make it better.
