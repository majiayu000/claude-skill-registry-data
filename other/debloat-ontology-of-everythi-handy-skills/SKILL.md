---
name: debloat
description: >-
  Restate the last message by cleaning it up only: make it more logical and
  more concise, and remove filler and empty talk, without polishing.
disable-model-invocation: true
license: Apache-2.0
metadata:
  language: en
  translation_of: debloat-cn
  version: "0.1.1"
---

# Debloat

Restate the user's last message. Clean it up only. Do not polish it.

## Scope

Work on the latest user message in this conversation. Leave earlier messages, instructions, and your own drafts untouched. If that message is already one clean statement, return it unchanged and say that nothing needed removal.

## Cleanup

1. Keep the claims, requests, names, numbers, and constraints that are already there.
2. Drop filler, hedges that add no condition, repeated points, and sentences that do not change the request.
3. Put the remaining points in the order the work needs: goal, then constraints, then the ask.
4. Use the author's words. Shorten a sentence by cutting words. Do not swap in a smoother phrase.

## Leave out

- New facts, examples, or advice.
- A warmer tone, a stronger voice, or a more formal register.
- Headings, bullets, or emphasis the original did not need in order to be followed.
- A comment on how the message was written, unless the user asked for that.

## Done

The reply is the restatement and nothing else. It is no longer than the source. Every kept claim can be pointed to in the source. No sentence exists only to sound better.
