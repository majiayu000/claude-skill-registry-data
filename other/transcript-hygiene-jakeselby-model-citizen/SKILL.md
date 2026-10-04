---
name: transcript-hygiene
description: Bound what subagents return and what tool output enters the transcript; load when briefing a subagent or reading large output.
---

# Transcript hygiene

The resident rule `primitives/rules/transcript-hygiene.md` is provenance for the full harness,
not a standalone installation requirement. Apply the reading and return limits below directly.

The user reads the transcript, not just the final message. **Thinking summaries are wanted and
stay** — they are collapsed and opened deliberately. Everything else in the scroll is cost they
did not ask for, and the worst offenders are tool output and relayed subagent reports, not prose.

## Read narrowly

- **Never `cat` a whole file to answer a narrow question.** `sed -n '40,80p'`, `head -40`, or
  `grep -n` with the pattern. Read the whole file only when you will actually use the whole file.
- **Never chain `cat A && cat B && cat C`** to orient. Orient with `grep -n '^#'` for headings,
  `wc -l` for size, then read the part that matters.
- **Filter every `find` and `ls`.** A repo with a `renders/`, `data/` or `target/` directory will
  print hundreds of generated filenames. Scope the glob or pipe to `head`.
- **A command printing more than ~100 lines needs a reason** you could state out loud.

## Bound what a subagent hands back

`delegation.md` says to cap the return. These are the numbers.

- **Gathering agent: 400 words.** Research digest: **600**. Adversarial review: findings only,
  no restatement of what it read.
- **Detail goes to a file, not into the return.** Brief it to write the long version into the
  scratchpad and return the verdict, the findings that change a decision, and the path.
  Same split as a plan: card in the message, addendum on disk.
- **A word cap is not a budget to spend.** Ask for what changes the answer, and nothing else.

## Never reprint a subagent's output

- **Synthesize, never relay.** A finding that matters belongs in your own answer, in your own
  words, carrying the source. A finding that does not matter does not appear at all.
- **Never paste the report** — not as a quote, not as a "here is what the research agent found"
  block, not lightly edited. The harness already renders the agent's own row.
- **Never echo the brief you sent.** The user has no reason to read a prompt they did not write.
- **No arrival narration.** Not "both research threads are back", not "the agents have
  returned". Shape the reply by the `voice` stance; the reader does not need the machinery.

## The tool description is the action log

In a focus view, tool calls, results and thinking collapse into one-line expandable rows, and
the line the user sees is the `description` you passed. It is the log, not a label for your own
benefit.

- **Write it for a reader who never opens the row.** "Check whether the plan card fits the cap",
  not "run awk on the plan file".
- **No flags, no paths, no command text.** They are not reading the command; that is what
  expanding is for.
- **One clear action in plain words**, five to ten for routine commands, longer only when a
  glance would not tell them what it does.

Text you write between tool calls stays visible in a focus view. A one-line note before a batch
is welcome; narrating each call is not.

## The one exception

Verbatim relay is correct when the exact text *is* the finding: an error message, a licence
clause, a quoted decision row, a failing assertion. Quote the line, not the report around it.
