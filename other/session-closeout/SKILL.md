---
name: session-closeout
description: Close out a work session safely. Verifies every change is committed, pushed, and green, confirms the work is live and verified, updates the notes for next time, and hands back a summary with links and a rollback path. Trigger on "close out the session", "wrap up", "lock it up", "are we good to close", "session QA", "end of session", or any moment before you stop or hand off.
---

# Session Closeout

## What this does

Runs the safety pass at the end of a work session so you never leave the work half-shipped. It checks that everything is committed and pushed, the build or deploy is green, the change is actually live and verified, and the notes are updated so the next session starts warm. Then it hands you a short summary with live links, open items, and how to roll back. It is the lock-up, not the learning pass. Pair it with a handoff note and a reflect pass.

## What you'll need

You do not need to connect anything. Point it at what you did this session and it walks the checklist. It gets sharper when it can see your repo, your CI, and your deploy.

- Works today with: a plain list of what you changed and where it should be live. Paste it.
- More powerful with a git repo: it reads status, the branch, and whether local matches the remote.
- Sharper with CI or a deploy target: it confirms the build is green on the right commit before it calls it done.

## How this runs at your connection level

Never reliant on a connector. It runs on what you tell it and gets more certain as it can see more. It never reports "shipped" for something it cannot confirm. An unverifiable claim is flagged, not assumed.

## Customize this for yourself

| Set this | What it is | Example |
|---|---|---|
| Your definition of done | What "shipped" means for you | committed, pushed to main, deploy green, verified live |
| Your verify step | How you confirm it is live | load the URL, run the test, check the dashboard |
| Your notes location | Where the next-session brief lives | a context doc, an issue, a channel message |
| Your rollback | How you undo the last change | the previous good commit or release |

## The method

### 1. Inventory what changed
List every change this session and where each is supposed to show up. Anything not on the list does not get verified, so the list has to be honest.

### 2. Commit and push
Confirm the working tree is clean, everything is committed with a real message, and local matches the remote. Uncommitted work is the most common way a session is lost.

### 3. Confirm green
If there is a build, CI, or deploy, confirm it is passing on the exact commit you pushed. Not a previous one.

### 4. Verify live
Actually load the thing. Check the change is present in production, not just in the diff. For anything visual, look at it.

### 5. Update the notes
Write the next-session brief: current state, open items, where things live. Convert any "today" to a real date.

### 6. Hand back the summary
Report what shipped with live links, what is still open, and the one command or commit to roll back if needed.

## Quality gates

- Nothing is reported as done unless it was confirmed live. Unverifiable items are flagged.
- Local must match the remote before closeout passes.
- The summary always includes a rollback path.
- Closeout is the safety pass only. It does not rewrite the work or the skills; that is the reflect pass.

## Output (example)

```
CLOSEOUT: green
Shipped:
- New pricing page, live at /pricing (verified)
- Fixed the signup redirect (verified, tested)
Committed + pushed: main @ a1b2c3d, matches origin
Deploy: READY on a1b2c3d
Open items: mobile spacing on the hero (not blocking)
Rollback: revert to 9f8e7d6
```

## Where the inputs come from

The change list is yours. Git status, the deploy state, and the live check are read from your repo, your CI, and the running site when those are connected. Everything else is confirmed by loading it, not assumed.

## Example chat

**You:** Close out this session. I shipped the new pricing page and fixed the signup redirect.

**Claude:** Ran the checklist. Both are actually live, not just committed.
```
CLOSEOUT: green
Shipped:
- New pricing page, live at /pricing (verified)
- Fixed the signup redirect (verified, tested)
Committed + pushed: main @ a1b2c3d, matches origin
Deploy: READY on a1b2c3d
Open items: mobile spacing on the hero (not blocking)
Rollback: revert to 9f8e7d6
```
Worth naming: I didn't mark either item done until I actually loaded the page and checked it was there. A diff that's committed isn't the same as a change that's live, and this pass only counts the second one.

**You:** What if the deploy had still been building when I asked to close out?

**Claude:** Then this comes back "not green," not "probably fine." It confirms the build passed on the exact commit you pushed, not a previous one, before it calls anything shipped. Sharpener: connect your CI so I can confirm the deploy state directly instead of you telling me it finished.

## Go further
The checklist catches what memory would have missed. Here is the version that runs it without being asked.

- **Run it automatically at the end of every session.** Wire this as the last step of a scheduled Claude task or a git hook so nothing gets left half-shipped by accident.
- **Confirm live status without manual checking.** Connect your deploy target, Vercel for example, so the verify-live step checks production directly instead of you loading the page.
- **Post the summary where the team sees it.** Send the closeout report to Slack automatically so a teammate picking up next session starts warm without asking you what happened.

The lock-up happens the same way every time, whether you remember to run it carefully or not.

## Make it yours

Set your own definition of done and your verify step in the table above. Run this at the end of every session, or before any risky handoff. Follow it with a handoff note for continuity and a reflect pass so the system learns.
