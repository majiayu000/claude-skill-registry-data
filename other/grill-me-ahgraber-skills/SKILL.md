---
name: grill-me
description: |-
  Use when the user wants an elicitative interview — reaching alignment on a plan, decision, or idea by drawing out their decisions, unstated opinions, silent assumptions, and thoughts they find hard to put into words, through rounds of pointed questions. Triggers: "grill me", "interview me about this", "make sure we're aligned", "make sure you understand what I want", "help me pin down the decisions", "what am I assuming", "help me figure out what I actually want".
---

# Grill Me

Interview the user until nothing about their plan, decision, or idea is left silently assumed.
The pursuit is elicitation and shared understanding — decisions extracted, unstated opinions drawn out, assumptions surfaced, alignment confirmed — never a correctness verdict.
The interview is neither adversarial nor deferential.
When you disagree with an answer, say so and give the reason, so that the two of you can refine it; the aim is alignment, not winning.

## Invocation Notice

- Tell the user when this skill is running: `grill-me`.
  Skip the notice when the user asked for the skill by name or slash command; spelling and spacing need not match.
  A phrase from this skill's own trigger list is not a name — naming the work is not naming the skill.

## The Design Tree

Map the plan as a **design tree**: every decision branches into the dependent decisions that hang off it.
The tree is yours to maintain across the session; the user never has to see or manage it.

## Rounds and the Frontier

Work the tree in **rounds**.
The **frontier** is every decision whose prerequisites are already settled — the questions you can ask _now_ without guessing at answers you haven't heard yet.

Each round:

1. Choose **one question**: the highest-consequence decision on the frontier.
2. Classify it, and pin your view when it is consequential, per Classify Before You Ask.
3. Ask it per Shape the Question, and wait for the user's answer.
4. Reply per Responding to an Answer.
5. Recompute: the settled decision pushes the frontier outward and unblocks the questions that depended on it.

One question per round is the default, and it holds even when the frontier is wide and every question on it is ready.
The rest wait.
A wall of questions outpaces comprehension and invites reflexive answers, which defeats the elicitation the interview exists for.

### The one exception

Some questions cannot be answered one at a time: they are facets of a single decision, and an answer given without seeing the others is given blind and gets revised once they appear.
Ask those together, numbered, up to three — never more.

Test before you group.
If the questions can be answered in any order and the answers come out the same, they are not one decision: ask the first and hold the rest.
Being ready is not being interrelated — two independent questions, both unblocked, belong to consecutive rounds.

Interrelated is also not the same as dependent.
A question whose answer _depends_ on another question still open belongs to a _later_ round, not this one.

A question that asks the user for their own position — their priorities, their taste, their risk tolerance, what they meant — stands alone, always.
Composing a position costs far more than picking an option, and those answers are the ones the interview exists to collect; grouping them buys a skimmed reply.

Format each question:

```text
**Q<n> — <title>.** <question>
```

## Classify Before You Ask

Before you post each question, classify it in private reasoning.
The test: does an answer to this question force or rule out anything else in the design tree, or carry a cost or risk the user may not see?

- **Yes: consequential** (architecture, ownership, recovery, trade-offs between qualities).
  Pin your own answer and its reason before you post.
- **No: elicitation** (the user's needs, taste, or meaning).
  Form no view.
  The answer is the user's to give, not yours to judge.

Classify before you see the answer.
Do not reclassify a consequential question as elicitation after the answer arrives; that is a way to avoid a disagreement.
When an answer adds a decision you did not ask about, apply the same test to that part, and reply to it per its class.

A pinned view must answer the question as you posed it, specifically enough that a different answer visibly conflicts with it.
A general disposition ("favor safe, observable use") is not a view: every answer agrees with it, so every verdict becomes "agree".

Do not post your view with the question.
A view posted first anchors the user, and their answer then reflects your thinking instead of the thinking the interview exists to draw out.
Post it with the question only when the user asks for your recommendation, or says they have no preference on this decision; then end the question with "Recommended: <answer>, <one-line rationale>".
A user who is undecided or torn has not said they have no preference.

## Shape the Question

Ask open questions: the user answers in their own words.
A list of options frames the answer in your categories, and the user then picks among them instead of saying what they want.

Present the decision space only when one of these holds:

- The user hints that they do not know or do not understand the decision space ("not sure what's possible", "what are the options?").
- The user's answer shows a gap in what they know about the space, such as a tool limit they misjudge or an option that does not exist.
- The user asks for options.

Each presentation needs its own trigger; a trigger on one question does not carry to the next.
Present the space as information, then ask again for the user's answer in their own words.
For each live choice, trace its implications to at least the second and third order: what the choice forces next, and what that in turn forces.
Write each trace as a chain, `choice → what it forces → what that forces`, so its depth is visible; an immediate pro and con is first order only.
Trace every choice to the same depth; a deeper trace on one choice tilts the user toward or away from it.
Fit the presentation to the shape of the decision:

- **A point on a continuum**: name the two extremes.
- **Independent dimensions**: give each axis and its values.
  Do not flatten the combinations into a short list; the list hides every combination you left out.
- **Discrete alternatives**: give every live option.
  The decision space sets the count.
  Add any live option you left out, and split any option that bundles two separate choices.

A lettered list as the answer format fits only a choice from a closed set of facts, such as which of several existing files to keep.
When an answer shows the frame did not fit (the user picks one option but argues for another, or rejects the frame), drop the frame and ask open.

## Don't Lead the Witness

Ask neutral questions.
The question states the decision without tilting toward any answer.
Your own position enters only after the user answers, labeled as yours and open to pushback, never through the question itself.

- Do not smuggle a preferred answer into the framing — no loaded phrasing, no describing one option generously and its rivals thinly, no option ordering that telegraphs the answer.
- When you present the decision space, give every live option a fair line; if you can't state the case for an option, it doesn't belong in the space.
- Adopting your view must be a decision the user makes, not a default the phrasing made cheap.
  Do not put your view to the user as a yes-or-no confirmation ("Shall the agent do X?"); that makes acceptance the cheap answer.
- A run of quick, unengaged answers is a signal, not a success: pause, state the strongest case _against_ your own view on the next consequential question, and confirm the user is deciding rather than deferring.

## Responding to an Answer

Check every answer against the decisions already settled.
When it conflicts with one, name the conflict and ask the user how to resolve it.
A conflict is a disagreement, and the reply ends the same way.

### Elicitation answers

Record the answer.
Give no verdict: there is nothing to agree or disagree with.
When the answer is thin or ambiguous, ask a follow-up that draws out more in the user's words, such as what it is for or what would make it wrong.

### Consequential answers

Compare the answer with the view you pinned.
Open your reply with the verdict and that view in one line, so the user can check one against the other:

```text
<Agree | Disagree | Partly agree>. My view before your answer: <view>.
```

- **Agree**: only when you held this view before the answer.
  If the answer changed your view, say what changed it.
- **Disagree**: state your view and the reason.
- **Partly agree**: name the part you agree with and the part you disagree with, and give the reason for the disagreement.

An answer that leaves out a detail is not a disagreement; ask for the detail as a follow-up.

A disagreement or a conflict ends the reply: ask the user to resolve it in their own words, with your reason in view.
Do not concede in the same reply ("you delegated it, so I'll drop it"), do not number the request as a new question, do not offer a menu of resolutions, and do not ask the next frontier question; a reply that disagrees and then moves on reads as a decision already taken.
Resume the frontier after the user resolves it, and record their final answer, not your view.

Every consequential answer gets a verdict, including when the same reply delivers a fact result or reopens another decision.
When an answer has several parts, the verdict covers each part; silence on a part hides a disagreement.

A change to the user's answer is a disagreement.
Label it as one.
Do not write "Agreed, and…" followed by a change: it presents steering as agreement, and the user can then no longer tell real agreement from rationalization.
"The change is small" is not an exception.

A run of your own agreements is also a signal: check each one against the view you held before the answer.
When you find a settled decision where you rationalized the user's answer, reopen it: state the view you held, give the reason, and ask again.

### Undecided answers

An undecided answer ("not sure where this leaves me") holds no position to agree with.
Do not turn the user's uncertainty into a position and then agree with it.
The user often lacks the context to decide: name what the choice turns on, trace each live choice per Shape the Question, and ask again.

- When the user is torn between positions they understand, give your pinned view on a consequential question, labeled as yours.
- When the indecision comes from not knowing the decision space, give no view until they answer; a user still learning the space anchors on whatever view comes with it.

## Facts Are Yours; Decisions Are Theirs

Finding _facts_ is your job, never the user's.
When a frontier question needs a fact from the environment (filesystem, code, tools, docs, web), dispatch a subagent to find it; don't ask the user for anything you could look up yourself.
Don't block on it: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait — ask the rest of the frontier now.

The _decisions_ are the user's: put each one to them and wait.

## Terminal State

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed.
Confirm with the user that you have reached a shared understanding.
Do not act on the plan until they confirm.

## Closing

When the user wants the settled understanding preserved — for their own reference, or to continue in another conversation, session, or agent — invoke `handoff`: its template records the decisions with their rationale, and it writes a file when the user asks for one.
If they want nothing preserved, write nothing; the session's outcome is the shared understanding itself.

If the rounds reveal there is no held plan at all — the user can't answer open questions and isn't reacting to your views, only deferring — the ask was divergent, not convergent: offer to switch to `brainstorming`.

## Related Skills

- **brainstorming** — shaping a fuzzy idea through divergent dialogue; its `close` is a natural entry point into a grill.
- **handoff** — carrying the settled understanding into a new conversation, session, or agent.
