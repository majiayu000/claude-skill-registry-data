---
name: debate
description: Have the Claude and GPT partners critique each other's answers across a configurable number of rounds (default 1) before converging on a synthesis. Use when the user wants the two perspectives stress-tested against each other, not just shown side by side.
---

# debate — make the two partners argue it out

Normally Debby fans a question out to both partners and shows the two
answers side by side. **debate** goes further: it relays each partner's
answer to the *other* partner for criticism, loops that for a configurable
number of rounds, and then converges on a synthesis.

## Rounds

The user picks how many rounds of back-and-forth to run. **Default: 1
round.** A "round" is one full cross-critique exchange (each partner sees
and criticizes the other's latest answer). Honor an explicit count from the
user ("debate this for 3 rounds"); otherwise run 1.

## Procedure

1. **Round 0 — collect the opening answers.** If you do not already have a
   fresh answer from each partner for this question, dispatch it to both
   `claude` and `gpt` in parallel via `sys_session_send` (ANSWER mode), give
   each call a stable per-partner `title` — the topic with the partner's name
   attached (e.g. `debate-pricing-claude` / `debate-pricing-gpt`), end your
   turn, and collect both with `sys_read_inbox`. If you already showed the
   user both answers this turn, reuse those as round 0.

2. **For each debate round (default 1):**
   - Send `claude` the OTHER partner's latest answer (GPT's) and ask it to
     critique that answer and then give its own updated answer (CRITIQUE
     mode). Reuse that partner's own `title` so it continues its thread.
   - Send `gpt` the OTHER partner's latest answer (Claude's) and ask the
     same. Dispatch both in the same turn so they run concurrently.
   - End your turn; collect both updated answers with `sys_read_inbox`.
   - Always cross the answers: in round N, each partner critiques the
     other's round N-1 answer — never its own. Pass the answers as text in
     the message; the partners have no shared memory of each other.

3. **Converge.** After the final round, write the synthesis yourself:

       ## 🟠 Claude — final
       <Claude's last answer, lightly trimmed>

       ## 🔵 GPT — final
       <GPT's last answer, lightly trimmed>

       ## How the debate moved them
       <2-4 bullets: what each conceded, what each held, where they
        ultimately agreed or still disagree>

       ## Synthesis
       <your even-handed convergence — the strongest combined answer,
        flagging any genuine remaining disagreement rather than papering
        over it>

## Notes

- Keep it even-handed. You are the moderator, not a third debater — your own
  opinion enters only in the Synthesis, and even there it is a synthesis of
  the two, not a new position.
- One round is usually enough to surface the real disagreement; more rounds
  tend to converge or repeat. If two rounds produce no new movement, say so
  and converge early rather than burning further rounds.
- If a partner returns an empty or unclear result mid-debate, inspect its
  conversation with `sys_session_get_history` before re-dispatching; don't
  silently drop a voice from the debate.
