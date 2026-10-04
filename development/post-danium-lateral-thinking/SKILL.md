---
name: post
description: Use when writing a social post on a topic or a reply to someone's post — X/Twitter, LinkedIn, Bluesky, Threads — and the obvious take is not good enough. Triggers include "reply to this post", "write a post about", "quote this", "tweet about", "my replies all sound the same", "what's a non-obvious take on", "build in public post", a pasted post with "what would you say to this", or a post URL. Do NOT use for analytical work like debugging, code review, or implementation tasks.
---

# Post

## What this does

Applies the lateral thinking toolkit to one specific creative target: a post or a reply. It is an applied layer over the `lateral` router, not a technique of its own — it acquires the target, routes it, runs the chosen technique, and shapes the result into drafts you can send.

The reason it exists: asked for a reply, an agent produces three phrasings of the take everyone else already posted. The existing replies under a post are the definition of "predictable" for that post; the drafts have to beat them.

## Procedure

### Step 1: Declare the mode and acquire the target

The input decides the mode. Name it in the diagnosis line; the drafts rule in Step 5 depends on it.

**Reply mode** — the input is someone else's post.
- **A URL** — read the post *and the visible replies* with whatever browser tool is available. Plain HTTP fetch fails on X (login wall). If no browser tool exists, ask for the post text and two or three replies pasted in; do not guess at the content.
- **Pasted text** — use it as given. Ask for the existing replies if none were included.

**Post mode** — the input is a topic, a claim, or a phrase to write about.
- Write the post anyone would write, in one draft, and label it `baseline`. It is the target for this mode. Nothing is routed from a blank topic.
- If the topic string carries two readings, pick the one the technique gets traction on and say which reading the baseline took.

Note the platform and its length limit. Default is X, 280 characters per draft.

### Step 2: Register check

Read the post for what it is. If it is a small, sincere post that is not asking for anything — a thank-you, a milestone, a personal note — say so before drafting: a clever reply from a stranger can underperform a plain "congrats" from someone who then engages with the work. Draft anyway; the user decides whether to send.

### Step 3: Route

Read `../lateral/SKILL.md` and follow its routing procedure. Diagnose from what the thread or baseline shows — every reply is the same encouragement, the post rests on an unquestioned premise, the announcement is a solution presented as an answer — and pick exactly one technique. If the user names a technique, skip diagnosis and use it.

### Step 4: Run the technique

Read the technique's `SKILL.md` and execute it inline, honesty mechanics included. One addition: a draft that says what an existing reply or the baseline already says is dead under that technique's redundancy rule, however well it is phrased.

If the technique's own failed-batch rule triggers, hand off as it says. Do not draw more in the hope of filling the drafts section.

### Step 5: Output

The output has these parts, in this order:

1. **Diagnosis** — one line: the mode, the symptom seen, and the technique chosen.
2. **Register note** — only when Step 2 applies.
3. **Drafts** — three to five, plain prose. Each ends with its character count in parentheses and stays within the platform limit. The technique label, if shown, goes after the count in one clause. What a draft may contain depends on the mode:

   **In reply mode**, a draft is written from the *idea* the technique produced, in the words of someone who never saw the stimulus, flip, or branch behind it. The stimulus stays in the transcript. Test before keeping a draft: cover the technique's label — does the draft still read as a plain statement to the poster, with no object being explained to them? If a sentence exists to explain the object, rewrite from the idea.

   Stimulus-shaped, fails: *"You didn't chase those 500, you kept the beam rotating. Ships find lighthouses, not the other way around."*
   Idea-shaped, passes: *"You didn't chase the 500. You posted every day whether anyone was watching, and that is what made you findable."*

   **In post mode**, the image may carry the draft when the post's job is to explain. Test before keeping one: delete the image and read what is left. If what is left already makes the point on its own, the image was decoration — cut it and keep the plain version. If what is left says nothing, the image is the explanation — keep it, and check that it is true in the way the draft uses it.

   Decoration, fails: *"LLMs reason step by step, like lightning feeling its way down. There's a fixed amount of thinking per word."* (delete the lightning; the point survives)
   Explanation, passes: *"Lightning can't cross the gap in one jump either. It feels its way down in short steps until the path connects — then the flash fires. An LLM works the same way."* (delete the lightning; nothing is left)
4. **Meta-pattern** — the technique's cross-result finding, including what the abandonments had in common.
5. **Weaknesses** — one line per draft where it is weak and why, which one the agent would actually send, and an origin flag on any draft that came from reading the post rather than from the technique.
6. **Offer** — the full transcript on request; fresh batch, go deeper on one draft, switch technique, or stop.

The technique transcript is not shown by default. It is available, and the meta-pattern and weaknesses sections are what make the drafts credible without it.

## Honesty mechanics

Inherited from the technique that ran. Two of its own:

- **Origin flag.** A good line that came from reading the post carefully is still a good line, but the technique does not get credit for it. Mark it.
- **Baseline test in post mode.** Every draft is compared to the `baseline`. A draft the baseline could have been is dead, and the output says which ones died that way.

## What NOT to do

- **Don't route the topic itself.** Write the baseline first; the techniques need something to climb from, flip, or force-fit against.
- **Don't hardcode a technique.** Four posts in one afternoon routed to three different techniques. The diagnosis is the work.
- **Don't ship the transcript by default.** The drafts, meta-pattern, and weaknesses are the deliverable. Offer the rest.
- **Don't prescribe on a saturated target.** Under a milestone or thank-you post, advice-shaped drafts die into standard advice; drafts that describe the poster's situation back to them survive. Weight accordingly.
- **Don't pick for the user.** Name which draft you would send and why. Sending is their move.
