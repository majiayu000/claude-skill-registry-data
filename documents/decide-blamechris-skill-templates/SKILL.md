---
description: "A decision protocol for an agent that thinks it is blocked."
---

# /decide

A decision protocol for an agent that thinks it is blocked. Most apparent blocks are not blocks: they are questions the repo already answers, or cheap reversible calls the agent is entitled to make and record. The few that are real deserve a structured question carrying options and a recommendation — not a paragraph of prose that hands the problem back and waits. This skill routes any pending decision down a fixed ladder, and dictates the shape of the ask when escalation is genuinely warranted.

Invoke it the moment you catch yourself about to write *"I need your input"*, *"how would you like me to proceed"*, or *"let me know and I'll continue"* — and any time you are about to stop work pending an answer or are about to write a seed with more than one next task. Cues like *"just decide"*, *"stop stalling"*, *"ask me properly"*, *"what are my options"* route here too. There are exactly two acceptable outcomes: a decision you made and recorded, or one `AskUserQuestion` call carrying 2-4 options with your recommendation first. A paragraph ending in a question mark is not one of them.

## Arguments

- `$ARGUMENTS` — all optional:
  - *(empty)* — run the decision currently in front of you down the ladder.
  - A question in quotes — run that one question down the ladder.
  - `batch` — sweep every question accumulated so far, drop the ones rungs 1-2 answer, and escalate the survivors together in a single round.

## The ladder

Run the rungs **in order**, and stop at the first one that resolves the question. A question reaches the user only by surviving rungs 1 and 2 — that ordering is the whole mechanism, and jumping straight to "ask" is the failure this skill exists to prevent.

### 1. Answer it yourself from the repo

Most questions that feel like they need the user are already answered by artifacts you can read. Search before you escalate:

- **The code around it** — how do the ten nearest files do this? Convention beats preference.
- **Git history** — `git log -S'<symbol>'`, `git log --oneline -- <path>`, `git blame`. The last person to touch this usually left their reasoning in a commit body.
- **The issue and its thread** — acceptance criteria settle scope questions; comments settle design ones.
- **Docs, ADRs, `CLAUDE.md`** — `CLAUDE.md`, `.claude/skill-profile.md`, `docs/doctrine/`, and the linked issue/PR.
- **The tests** — they encode intended behaviour more precisely than any doc.
- **This session** — was it already settled upstream, earlier in the run, or in the session log? Re-asking a settled question is worse than not asking.

Questions that look like user decisions and are not:

- *"Which naming convention?"* — the sibling files already chose it.
- *"New module, or extend the existing one?"* — the architecture doc and the way the siblings are split.
- *"Which error type / log level?"* — grep the neighbours.
- *"Should I write a test for this?"* — repo policy. Yes.
- *"Which library?"* — the one already in the dependency manifest.
- *"Keep backwards compatibility for X?"* — count X's callers first; zero callers is not a compatibility question.
- *"Is this in scope for the issue?"* — the acceptance criteria say.
- *"Should I fix the failing lint too?"* — CI has to be green. Not a choice.
- *"Which version number?"* — the versioning scheme and the changelog.

If reading gives you a defensible answer, that is your answer. Cite where you found it (file, commit, issue comment) so the reasoning survives you.

### 2. Decide and record

If the call is within existing authority, cheap and reversible, it is yours to make. The test: **could you undo it in a minute, with a follow-up commit, before anything outside this branch depends on it?** If yes, decide. A choice the owner explicitly reserves still goes to rung 3, even if it is easy to undo.

- **Pick** the option you would defend.
- **State the assumption** in plain words — "assumed X because Y".
- **Write it down** where the work carries it: the PR assumptions or the private session ledger.
- **Proceed.** Do not stop for confirmation on something you could undo in a minute.

Recording is not paperwork — it is what keeps the decision cheap to overturn. A recorded assumption costs the user one line to reverse; an unrecorded one costs them an archaeology session. And a decision nobody wrote down gets made again, differently, three files later.

Typically this rung: internal naming, file layout, test structure, error-message wording, how far a refactor spreads inside the diff you are already writing, which of two already-vendored helpers to use, a default behind a flag that ships off.

Silence is consent at this rung — that is precisely why it is this rung, and precisely why silence is never consent at rung 3.

### 3. Escalate only when it materially changes the work

Escalate only if at least one of these is true:

- **Divergent deliverable** — the answers lead to genuinely different work, and picking wrong wastes hours rather than minutes.
- **Irreversible** — deleted data, a force-push, a published release or package, a closed account, a sent message. You cannot take it back.
- **Outward-facing** — someone beyond this branch sees it: a public API, schema or CLI surface you would then have to deprecate; a message to a human; an issue or PR on a repo that is not yours; published docs.
- **Spends the user's money, quota or reputation** — paid API calls, provisioned infrastructure, anything published under their name.
- **Overrides something they already said** — you would be carving an exception out of a stated preference. Ask; do not assume the exception.
- **Legal, security or privacy weight** — credentials, licences, personal data.

None of those? Go back down to rung 2 and decide. Asking is not free: it costs the user a context switch and it costs the run its momentum. Weigh that against the cost of being wrong — and remember that a wrong rung-2 call is usually a one-commit fix.

Use existing delegated authority for routine choices. Irreversible actions, new spending and overriding owner preferences remain reserved unless explicitly authorized.

### 4. When you escalate, escalate well

Use the **`AskUserQuestion` tool. Never prose.** A question buried in a paragraph makes the user reconstruct your context, compose an answer, and remember what they already told you; a structured question is answered with a click.

- **2-4 concrete options.** Each names an actual course of action ("ship the SQLite backend now, add Postgres behind an adapter later"), not a category ("the simple approach").
- **Lead with your recommendation.** The first option is the one you would take, and it is labelled as the recommendation. You built the context; carrying that judgment back with the question is the deliverable, not an overstep.
- **Real pros and cons on every option — including the recommended one.** Name what your recommendation costs. An option with no downside listed reads as unconsidered, and a judgment whose price is hidden cannot be audited.
- **Plain language.** Write for someone who has not read the diff: expand the internal names, drop the acronyms you coined this session, describe consequences in terms of the product rather than the code.
- **One round, not five.** Batch every open question. Drip-feeding one per turn turns a five-minute conversation into a day of latency.
- **Say what happens if they do not answer** — record the recommended plan as the default and continue independent authorized work. For an owner-reserved choice, the dependent task stays blocked until answered; the default never grants permission to execute it. Keep the choice in DECISION with `recommend:` and `default:` in every status block. If the choice is already authorized and reversible, resolve it at rung 2 instead of asking.
- **Never ask a bare "what would you like to do?"** If you cannot draft two concrete options, you do not understand the problem well enough to escalate it. Go back to rung 1.

Use the host question UI equivalent. If unavailable, present numbered options with recommendation, trade-offs and a no-answer default; reserved execution stays blocked until authorized.

### 5. Never idle

**A block on one thread is not a block on the work.** Before you ask anything:

- **Split the work** into what actually depends on the answer and what does not. The dependent slice is almost always smaller than it feels.
- **Keep going on everything else** — the other items in the queue, the tests, the docs, the parts of this change that both answers share. Select independent work from the current authorized package and review queue.
- **If everything truly depends on the answer**, build the recommendation, marked provisional, while the question stays open. A provisional implementation is far easier to redirect than a blank branch.
- **Report progress alongside the question.** Never send a message whose entire content is a question. *"Asked about X; meanwhile Y and Z landed and CI is green"* is a report. *"I'm blocked on X"* is not.

## Anti-patterns

Every one of these has shipped. Name it when you catch yourself doing it.

- **The prose block** — *"I wasn't sure whether to use X or Y, so I stopped."* A block delivered as a paragraph, with no options and nothing to click, leaves the user guessing what you even want from them.
- **Full stop on a partial block** — one thread waiting, the whole run parked, while four other items were ready to go.
- **The drip-feed** — one question this turn, another the next, a third after that. Five interruptions for what was one conversation.
- **Re-litigating settled ground** — asking about something already decided earlier in this session, in the issue thread, or in an ADR. Read the log before you ask.
- **Optionless options** — a list of choices with no steer, so the user has to rebuild the context you already have before they can pick. If you cannot recommend, you have not finished thinking.
- **Escalating what the repo answers** — the most common failure of all, and the cheapest to avoid: the convention was sitting in the sibling file the whole time.
- **Manufactured urgency** — dressing a one-commit reversible choice as a fork in the road, and buying an interrupt with it.
- **Silence as approval** — proceeding with an irreversible or outward-facing action because nobody replied. No answer means not yet.

## Is this actually blocked?

Run this before every escalation. Items 3 and 4 are an **or** — either one alone justifies escalating, matching rung 3's "at least one". The rest must be yes; the first **no** names where to go back to. Read them in order and stop at the first that sends you to rung 4.

1. I searched the code, the git history, the issue thread and the docs, and the answer is not there. *(No → rung 1.)*
2. It was not already decided earlier in this session, or in a previous one. *(No → rung 1.)*
3. The answers lead to genuinely different work — not just a different name, order, or internal shape. *(No → check item 4; a small-diff change can still be irreversible.)*
4. I cannot cheaply undo the wrong choice; or the action is irreversible, outward-facing, or spends the user's money or reputation. *(No → rung 2.)*
5. I can state 2-4 concrete options, and I know which one I would pick and why. *(No → rung 1 — you do not understand it well enough to ask yet.)*
6. I know what continues regardless of the answer, and it is already continuing. *(No → rung 5.)*

## Reporting

The question itself goes through the tool; the message around it still ends with the house `**Status:**` line — what is done, what is in flight, and what is waiting on the answer, naming the question. One to three lines, no padding. A status line whose whole content is "blocked" is the failure this skill exists to prevent. Use the fleet root’s four-slot Status block and one-task Next line, retaining pending choices with recommendation and default.
