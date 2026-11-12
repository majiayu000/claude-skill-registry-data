---
name: resume
description: Pick up the forms that wait for the user and settle the ones that were clicked but not confirmed. Use when the user says /resume, "I typed the code", "I passed the check", "I signed in", "continue", or after a run that said forms are waiting.
argument-hint: "[job id ...]"
model: claude-sonnet-5-5
effort: low
---

# /resume

A form waits for the user when only they can do the next thing: type a
code the board emailed, pass a robot check, finish a sign-in. It stays
open in the tool's own Chrome window. They do that one thing there; this
skill does the rest.

1. Run `npx jev status`. If nothing waits and nothing is unconfirmed, say
   so and stop.

2. For forms that wait at a human check (a code, a robot check), run:

   ```
   npx jev resume
   ```

   It watches each form while they finish it and records the application
   when the confirmation shows. Tell them which form it is on.

3. For forms whose Submit was clicked with no confirmation seen, run
   `npx jev reconcile`. If it cannot tell, ask them to look for the
   employer's confirmation email, then mark it with
   `npx jev mark <id> --status applied`, or `--status queued` to try again.

4. A form that waits at a **sign-in** (the reason mentions a sign-in, a
   password, account terms or a verification link) is different: carrying
   on means the tool signs in at that employer. You do not start that.
   Show the command, which has a Run button:

   ```bash
   npx jev resume --submit
   ```

5. Say what was sent, what still waits and why.

## What you never do

- Never read or type a code, never pass a check, never sign in. The user
  does that in the tool's window; you only watch and record.
- Never use `mark --status applied` unless the user saw the confirmation.
