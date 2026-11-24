---
name: after-action
description: "Use after repeated corrections or avoidable failures, after a hard bug, or before clearing a long session. Proposes only. Not after a clean run."
user-invocable: false
---
# After action
Job: Turn session failures into lasting changes to the agent's surroundings, not the product.
Takes: a session, default current, or worker reports.   Gives: ranked proposals tied to observed events.
Team moves: look back

The aim is to remove causes. A repeated warning isn't a fix. This block proposes only. Acting goes through the skill `repo-fitting` or the skill `agent-prose`.

## Steps

1. Use the skill `agent-prose`, since most proposals touch something an agent reads.
2. Read the actual session, not a memory of it. If the current session is gone or compressed, look back through the log. Also read what the team left: run outcomes, timeouts, lease clashes, check bounces and limit refusals. A brief that needed three steers is a finding about the brief.
3. Walk these lenses and collect candidates, each with the event that shows it.

   | Lens | Look for | Usual proposal |
   |---|---|---|
   | Lookups | Slow hunts for something a line could have pointed to, hidden dependencies | A pointer where the next agent will look |
   | Checks | Mistakes a check should have caught. Read scripts and CI first. A check that exists but never runs is the real find, and a repo with no gate of any kind is a finding too | Wire it up, or add one |
   | Review rules | Each violation of a rule | Mechanical (a code pattern, a forbidden call, how imports are written, where a file sits): an automated check, whichever way is cheapest. Judgement call: a written standard |
   | Steering files | Oversized instruction files, lines that changed nothing | Move content into standards or checks, delete the rest. Root instruction files should be mostly pointers |
   | Tool economy | Costly calls, token-heavy tools, repeated reads | A narrower tool or call |
   | Information access | Logs or services the agent lacked | Read-only access or a pointer |

4. Place standards with context pressure in mind. Builders are the most squeezed and reviewers the least, so standards are enforced at review. Keep the builder's always-loaded text small.
5. Rank by severity: what cost the most, and what will recur.
6. Write each proposal in this form: the event, the cause, the change, its route (`repo-fitting`, `agent-prose`, a standard), and the gate it would need. When the user corrected the same ask, channel or style twice, also propose a line for `~/.dami/prefs.md` in its form (`ok:`, `show:`, `taste:`, see the skill `house-rules`); their yes is the OK to write it.
7. Stop. Present the list and let the user choose.

## Done when

- The session or log was actually read, and the scope is stated: full, or which part.
- Every proposal is tied to an observed event, quoted or referenced.
- Proposals are ordered by severity.
- Every violation was classified as mechanical or judgement.
- Existing scripts and CI were read before any check was proposed.
- No file was changed.
