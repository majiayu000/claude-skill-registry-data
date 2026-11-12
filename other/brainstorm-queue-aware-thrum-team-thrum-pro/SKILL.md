---
name: brainstorm-queue-aware
description: "Use when running as a brainstormer that a Brainstorm Steward is managing — redirect every Q-by-Q question to the Steward as a NEED message and block for the ANSWER instead of asking the human directly. Fires when your briefing names a steward."
---

# Brainstorm: Queue-Aware Mode

## When this fires

You are a brainstormer running the normal `brainstorming` skill, and your
briefing names a `steward: @<name>` (or otherwise tells you a Brainstorm
Steward is managing your slot in a queue of parallel brainstorms). That one
fact is the whole trigger. If no steward was named, ignore this skill
entirely and run `brainstorming` exactly as documented — ask the human
directly, the ordinary way.

Every `@<steward>` placeholder below stands for that same name from your
briefing — substitute the real agent name, not the literal text
`<steward>`.

This is a **thin overlay, not a replacement**. Everything about how you
research, propose options, and converge to a locked design is still owned by
the `brainstorming` skill. The only thing this skill changes is **where a
question goes when you would otherwise have asked the human.**

## The redirect

Wherever `brainstorming` says "ask the user" or "pause for the human's
answer," do this instead:

1. Compose the question exactly as you would have asked the human — one
   clear question, plus 2-3 concrete options (A/B/C) so the Steward has
   something to decide between, not an open-ended essay prompt.
2. Send it as a `NEED` to your steward, per the NEED/ANSWER convention
   (first line `NEED [<topic>]:`; the steward replies with an `ANSWER`):

   ```bash
   thrum send --to @<steward> --stdin <<'EOF'
   NEED [<topic>]: <one clear question>
   A) <option>
   B) <option>
   C) <option>
   EOF
   ```

3. Block on `thrum wait` rather than polling or continuing speculatively:

   ```bash
   thrum wait
   ```

4. When `thrum wait` returns, read the reply from your inbox the normal way.
   The Steward answers by replying directly to your NEED message (threaded,
   automatic), with a body starting `ANSWER:`. Treat that `ANSWER:` line
   exactly as if the human had just said it to you — fold it into the design
   and continue the brainstorm from there.

Nothing about the NEED/ANSWER convention is a new subcommand or a structured
payload — it's plain `thrum send` / `thrum reply` / `thrum wait` with a
one-line prose convention on top. Don't invent a schema, a JSON body, or a
`thrum need` command; none exists.

## One question at a time, still

The `brainstorming` skill's Q-by-Q discipline doesn't change: send **one**
NEED, block, get the **one** ANSWER, then decide whether the next question is
needed before sending it. Do not queue up three NEEDs in a row hoping to
save a round trip — the Steward may be juggling several brainstormers at
once, and batching on your end doesn't help it; it just makes your own
inbox harder to reason about when replies come back out of order. Batching
NEEDs across brainstormers so the human sees fewer round trips is the
**Steward's** job, not yours — that's the whole point of putting a Steward
in the loop.

## If the Steward doesn't answer

`thrum wait` blocking indefinitely is normal and expected — the Steward may
be waiting on the human, or working through other brainstormers first. Don't
treat a long wait as a signal to guess.

If the wait genuinely exceeds a reasonable bound for your situation (you've
been blocked far longer than the Steward's other visible turnarounds, or
you have independent reason to think the NEED never arrived):

1. **Re-send the NEED once** — a fresh `thrum send` with the same question,
   not a new phrasing, so the Steward isn't left reconciling two versions of
   the same ask. Note in the resend that this is a repeat:

   ```bash
   thrum send --to @<steward> --stdin <<'EOF'
   NEED [<topic>]: <one clear question> (resend — no answer yet)
   A) <option>
   B) <option>
   C) <option>
   EOF
   ```

2. If that still doesn't produce an ANSWER, **escalate to your `parent`**
   (the Steward, or whichever agent your briefing names as parent) with a
   plain status message — do not decide the content yourself:

   ```bash
   thrum send --to @<parent> --stdin <<'EOF'
   Blocked on NEED [<topic>] — resent once, still no ANSWER. Need a decision
   to keep moving; not proceeding on a guess.
   EOF
   ```

Never fill in the owner's decision from your own judgment because the
Steward is slow. A wrong guess here isn't a small correction later — it's a
design-lock built on a decision the owner never actually made.

## Design-lock discipline still belongs to you

The Steward is a **relay**, not a decider. It exists to keep your questions
moving through a queue when the human is juggling several brainstormers —
it is not delegated authority to choose between your options on the owner's
behalf, and an `ANSWER:` it relays is the owner's answer passed through, not
the Steward's own opinion. Nothing about a Steward being in the loop loosens
the standing brainstorm discipline: you still hold the RESOLVED-CHOICES
record for the owner (per the `interactive-brainstorm` role rule / the
standing brainstorm design-lock convention), and every locked decision still
needs to trace back to a real `ANSWER:` line, not to an inference you made
because the Steward's presence made the human feel one step further away.
If an `ANSWER:` is ambiguous or doesn't actually resolve the question you
asked, send a follow-up NEED rather than picking the reading that's
convenient.

## Announce handoffs, so the Steward can keep things moving

When you send finished work to another agent and then sit waiting on them —
for example, a brainstorm or plan sent to a coordinator for dual review —
send the Steward a brief, plain-prose heads-up so it can notice if you stall
and prompt a nudge. This is **not** a new convention; it's the same
unstructured-message style as NEED, just without the `NEED:` prefix (the
Steward isn't being asked to decide anything, only to keep an eye out):

```bash
thrum send --to @<steward> --stdin <<'EOF'
WAITING [<topic>]: sent the brainstorm to @<coordinator> for dual review.
EOF
```

You are **not** expected to poll for a response yourself while in this
state — that's the Steward's job, the same way batching NEEDs is. When the
response you were waiting on actually arrives, send a short close-out so the
Steward's picture of the queue stays current:

```bash
thrum send --to @<steward> --stdin <<'EOF'
UNBLOCKED [<topic>]: review came back, resuming.
EOF
```

Keep both messages short — one line of status, not a narrative. The Steward
reads these the same way it reads a NEED: as a judgment agent scanning its
inbox, not a parser expecting a fixed shape.

## Why this is safe to layer on

Nothing here adds a new delivery mechanism, a new command, or a schema —
every example above is `thrum send --stdin <<'EOF' ... EOF`, `thrum reply`,
or `thrum wait`, exactly as documented in the NEED/ANSWER convention. Using
a **quoted** heredoc delimiter (`<<'EOF'`, never bare `<<EOF`) is
deliberate: an unquoted heredoc runs command substitution on backticks and
`$()` inside your message body before it's ever sent, which can silently
execute something you only meant as text. Always quote the delimiter.
