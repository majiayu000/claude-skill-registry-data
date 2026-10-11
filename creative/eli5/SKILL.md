---
name: eli5
description: Explain work, a system or a situation to Sergio in plain words with real names, so he understands it on one read. Use when he asks to explain like a 5yo, says eli5, or says he does not understand what was done or where things stand.
---

# eli5

Sergio reads this when he has lost the thread. He wants to understand, not to be impressed. Simplify the telling, never the claims: every sentence stays true to the code, the calls and the messages, and the words get shorter, not the facts.

## The shape of the answer

Two layers, in this order.

1. **The short version, under 200 words.** The whole story: who is involved, what the goal is, what was done, where it stands, what is open. Written so that it stands alone if he reads nothing else.
2. **The detailed version.** The same story told fully, in the sections below, each under its own heading so he can stop at any point and still have a complete picture up to there.

Close with a `Summary` of three or four bullets: the state, the open decisions, and what is his to do.

## The sections of the detailed version

Write them in this order. Each section answers one question a person asks when they come back to work they half remember.

**Who does what.** Name every person and every program in the story, one line each, with the thing each one owns. A program is named by its real name and by what it does for the person using it. The reader must be able to point at each name later in a pull request or a message and know which one it is.

**What each thing is.** For every program, repo, service or file that carries the story, say what it is in concrete terms: what the person sees, where it runs, what it holds, what it talks to. Check this against the code before writing it, because a one-word label from memory is the most common error and it breaks the whole explanation. When a thing has several parts, list the parts by their real paths and say what each part does.

**The problem, in one sentence.** The problem as the person who raised it said it, then one sentence on why the old behaviour produced it.

**What was done, as numbered steps.** One step per change that landed, in time order, each with its date and its version, tag, pull request or commit. Each step says what changed for the person using the program and what changed in the code, in that order.

**One scenario, start to end.** Pick the one scenario the work exists for. Walk it from the triggering event to the last visible effect: who acts, what each program does, what the person sees at each point, and where each piece of data goes. Write it as the sequence it really is. When the order or the timing is the point, write the sequence as a short numbered list of conditions and effects rather than prose, so the reader can see what happens on the second call as well as the first.

**What it does not do yet.** Every known gap, each with the reason it is open and whose decision it waits on.

**Where we are now.** One line per open thread: its state, who holds the next move, and what that move is.

## Rules for every sentence

- Plain words, short sentences, one idea per sentence. Define each term the first time it appears, in the same sentence.
- Real names only. Use the exact identifier, path, route, flag, version and error text, and explain around it. A description of a thing stands in for its name only when the name has not been said yet.
- Concrete over abstract. Say what the person sees, what the program reads, where the bytes go. When an abstract word appears (layer, surface, mechanism, flow), replace it with the thing it stands for.
- Explain with real technical examples: the actual request, the actual file, the actual message. Figurative language is excluded in full: no analogies, no metaphors, no comparisons to everyday objects or other products as a way of explaining. If a comparison to another product is a fact of the design, state it as a fact of the design and move on.
- Prose and numbered lists only. The answer is text in the conversation, never a page, a diagram file or an artifact.
- Cite where it matters: a `file:line`, a pull request number, a call or message anchor, so he can check the claim.
- Minimizers are out: simply, just, obviously, basically, of course, as you know.
- Separate what exists today from what is proposed, and what was observed from what is inferred. Say which is which.

## Before sending

Read the answer once as someone who was away for a week. Every name must have been introduced before it is used. Every claim must be one he could check. If a sentence needs the reader to already know the code, it is not finished.
