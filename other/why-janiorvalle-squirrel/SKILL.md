---
name: why
description: "Use for \"why does X work this way\", \"why did we pick Y\", design rationale, regressions, postmortems, and \"where did this number come from\". Finds every evidence source available (git, tickets, docs, chat, observability, error tracking, product analytics), searches them all in parallel, and returns a cited answer that separates what's known from what's guessed. For what the code does, use how."
---

# Why

Find out why code is the way it is: what problem it solved, what constraints shaped it, what was tried and rejected. Companion to `how`, which tells you what the code does. `why` tells you what pushed it into that shape.

## The idea

The reason for a piece of code is almost never in the code. It's in a PR discussion, a ticket, a design doc, a Slack thread, a monitor threshold, an error spike, or a usage chart, and the question doesn't tell you which. So find every source you have access to, search them all at once, and report what each one said, including the ones that said nothing. An empty result from the ticket tracker is a fact: nobody ticketed this.

Default to searching everything. An investigator coming back empty costs one subagent. Missing the design doc that exists costs a wrong answer.

## How to think

You're a careful investigator working from partial records. Commit messages lie. Tickets go stale. The author may have left. Be honest about what you know versus what you're guessing.

- **Evidence first, story second.** Collect, then see what the pieces support. Never pick a story and go looking for evidence that fits.
- **Quote and cite.** Every claim about intent points at a commit, PR, ticket, doc, message, or code comment a reader can reach in under a minute. No citation means it's an inference and gets labeled as one.
- **Hedge on purpose.** "Appears to", "likely", "suggests" when the evidence is indirect. "Because" only when someone wrote the reason down.
- **Show contradictions.** If the ticket says one thing and the PR says another, show both. Don't pick the tidier one.
- **Name the gaps.** "We searched the tracker for A and B and found nothing" is an answer. A confident guess in its place is worse, because the reader will act on it.
- **Don't read intent off the code.** "It checks for null so the author must have wanted to handle null" is mechanics, not motivation.
- **The user's guess is a hypothesis, not a conclusion.** "I assume this is for performance?" gets checked like any other candidate.

`references/epistemics.md` has the confidence tiers and phrasing. The synthesizer must follow it.

## Step 1. Pin the target and the question

The target is a chunk of code, a pattern, a feature, or a named decision. The question is usually one of:

- Why was X designed this way. Rationale.
- Why X instead of Y. Tradeoff.
- What edge cases forced this. Defensive reasoning.
- What business or product constraint led here. External forcing function.
- Why does this still exist. Dead-code territory.
- What's the history of X. Broad sweep.

If the target is vague, take your best guess from context, say what you took it to mean, and go. Don't ask; the human can redirect.

## Step 2. Anchor in the code

Build the anchor yourself before spawning anyone. It's cheap, and every investigator needs it.

- File paths and line ranges.
- Key symbols.
- The last several commits touching the target.
- PR numbers from merge commits, usually `(#1234)` in the subject.
- Ticket ids mentioned in those commits or PR bodies.

```bash
git blame -L <start>,<end> <file>
git log --oneline -20 -- <file>
git log --follow -p -- <file>
git log -1 --format=%B <commit>
gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews
```

## Step 3. Find your sources and spawn investigators

List the MCPs and tools available in this session. Map each to one evidence category:

1. Source control. Git and the PR host. Always available.
2. Issue tracker. Linear, GitHub Issues, Monday, whatever the team uses.
3. Long-form docs. Confluence, Notion, Google Docs.
4. Team chat. Slack, Teams, Discord.
5. Observability. Datadog, Grafana, New Relic.
6. Error tracking. Sentry, Rollbar, PostHog error tracking.
7. Product analytics. PostHog, a warehouse like Databricks or Snowflake, experiment and flag tables.

If an MCP could fit two categories, pick the one it's mainly for and note it. Write the coverage map down. It goes in the final output.

Spawn one investigator per category that has a source, all at once. One investigator per source. Don't give one agent three MCPs: each source has its own query vocabulary and result shape.

Investigators need tool access, so don't use a read-only mode that strips MCPs. They still shouldn't write anything. That's an instruction, not a sandbox.

Each investigator gets:

1. `references/investigator-prompt.md`, filled in.
2. Its category's section from `references/sources.md`, adapted to the actual tool.
3. The incident angle from the end of `sources.md`, if the target looks defensive. Null checks, retries, timeouts, rate limits, feature flags, size clamps.
4. The code anchor from step 2.
5. The original question.

### When to skip a source

Only with a written reason that goes in the final output. Two valid ones:

- No tool for that category in this session. That's a gap, not a choice. Say so.
- The source can't apply. A build-time script has no runtime errors. High bar. "Probably nothing there" doesn't clear it.

If the target is a single trivial commit and the PR description already answers the question, you can answer inline, only after confirming every available source would be redundant, and say you did. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer with `references/synthesizer-prompt.md`, every investigator's findings including the empty ones, the skipped sources with reasons, the anchor, the question, and `references/epistemics.md`. It needs tool access too, to spot-check citations. It writes the final answer: claims sorted by how well the evidence supports them, gaps named, sources listed.

## Step 5. Present

Show the synthesizer's output. Light edits for clarity are fine. Do not touch the confidence language; dropping the hedges is the failure this skill exists to prevent.

Lead with the plain version: what we found and how sure we are, in words someone outside the project can follow. Detail below.

## Output

The format is in `references/synthesizer-prompt.md`, from the plain-version lead through the sources and confidence summary, plus the block for a reader about to change the code. Keep the sections that apply.

## Ways this goes wrong

- A plausible story built on thin evidence. Uncited claims go in inferred or hypotheses, not in found.
- Citing the code as evidence for its own intent.
- Assuming the latest commit is the whole story. Trace back.
- Confirming the user's guess instead of checking it.
- Skipping the gaps section. An investigation with no gaps is hiding something.
- Deciding up front a source won't have anything. Search it. Let the empty result speak.
- One agent covering several sources.

## Reference files

- `references/epistemics.md`. Confidence tiers and phrasing. The synthesizer follows it.
- `references/investigator-prompt.md`. The brief each investigator gets.
- `references/sources.md`. One section per evidence category: what it holds, how to search it, what good evidence looks like, pitfalls. Plus the incident angle.
- `references/synthesizer-prompt.md`. The brief for the synthesizer, including the output format.
