---
name: play-test
description: Set up realistic test conditions and guide the user through hands-on checks of a code change or reported bug. Use when asked to play-test changes or walk through manual verification together.
metadata:
  website: "https://photostructure.com/coding/play-test/"
---

# Play-test changes with the user

Handle the setup and diagnosis so the user can inspect the behavior and judge
whether it makes sense. Keep the walkthrough short and interactive.

1. Read the relevant diff, code, and project instructions. For a reported bug,
   ask whether the user wants to reproduce it, verify the proposed fix, or do
   both, unless they have already specified. Offer only relevant checks;
   reproduction is optional and may not be a priority. For changes with no bug
   to reproduce, test the intended behavior. Choose a few concrete scenarios
   for the agreed scope.

2. Prepare the environment yourself: start the app, create test data, and put
   files or records into the required state. Identify the build being tested.
   Use disposable copies when setup would alter user data. If a prerequisite
   is unavailable, explain what is missing before asking the user to supply it.

3. Give the user the exact URL, screen, or command to open. Describe the starting
   state and have them confirm it matches the scenario they intend to test.

   For mobile browser testing, generate and display a QR code with a local QR
   encoder, alongside a clickable link to the same full test URL. Use the
   development machine's LAN address with the phone on the same network and
   the server listening on that interface, or an existing reachable preview URL.
   Do not encode `localhost`, a loopback address, or `0.0.0.0`. Preserve the
   URL's path, query, and fragment. Have the user confirm that scanning the code
   opens the intended build on their phone before continuing.

4. Give one action, or a small group of closely related actions, with the
   expected visible result and what to report back. Show any script you ask the
   user to run and explain what it changes so they can read it first.

5. Wait for the user's observations before the next dependent step. Compare
   them with the expected result. When they differ, investigate and explain
   the finding; fix it only if fixes are already in scope, then repeat the
   affected checks.

When both checks are requested, use a separate build or checkout for the
original version, preserving the uncommitted fix and other work. Reproduce the
issue there first and have the user confirm that it matches their report. Then
repeat the same scenario with comparable starting state on the proposed fix.
Report an inconclusive reproduction separately from successful checks of the fix.

End with a short record of what passed, failed, or remains untested, plus any
test processes or temporary data left behind. Distinguish checks you ran from
observations the user confirmed. A passing automated test does not establish
that the user completed the walkthrough.
