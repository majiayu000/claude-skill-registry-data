---
name: explainer-graphic
description: Build one self-contained HTML page that explains a complex thing as a drawn mechanism with labeled parts, not decorated text. Trigger on "explainer graphic", "explain this visually", "make an infographic", "draw how this works", "one diagram that explains it", "visual breakdown of", or when someone is stuck on how a system works and a picture would do the job faster than prose.
---

# Explainer Graphic

Most infographics are decorated text: a paragraph with an icon glued to it. This skill makes the opposite thing. Find the mechanism inside a topic, draw the mechanism, and let the words caption the drawing.

## Inputs

- The topic, in whatever shape the user has it: a question, a pasted doc, a link, a file.
- The reader. Who is looking at this, and what do they already know? Ask once if it is not obvious from the conversation. Default to a sharp adult who is new to this field, not to a child.
- Optional: brand colors, a section ceiling, an output folder.

Do not ask a second round of questions. One clarifier, then build.

## Step 1: find the spine before you draw anything

Write one sentence, for yourself, that answers this: what does the thing actually do, mechanically? Not what it is for, what it does. If you cannot write that sentence, you do not understand the topic well enough to draw it. Go read first.

That sentence is the spine. Now cut it into 4 to 7 beats. A beat is a state change: something enters, something transforms, something leaves. Two beats that change nothing between them are one beat.

Then stress test the spine. Delete beat 3 on paper. Could the reader still explain the thing to a colleague? If yes, beat 3 is trivia. Cut it and find the real one.

## Step 2: give every beat a drawing that carries weight

Each beat gets four parts, in this order:

1. **A claim line.** Six to twelve words, active voice, states what happens. Not a label like "Authentication". A claim like "The server signs the token so nobody can forge it."
2. **A drawing.** Inline SVG. Every shape stands for a noun in the claim. Every arrow carries a verb label. A shape that means nothing gets deleted, no matter how good it looks.
3. **An anchor.** One concrete thing from the reader's world that behaves the same way. Anchors are load bearing, not cute. "Like a wax seal on a letter" earns its place. "Like magic" does not. Use the anchor once, then drop it: a metaphor stretched across the whole page starts lying.
4. **Two or three sentences** in plain language. Jargon is allowed only after the drawing has shown what the word points at.

If a beat resists drawing, that is information. Usually it means the beat is really two beats, or that you are still describing purpose instead of mechanism.

## Step 3: build the page

One HTML file, no network requests. No CDN scripts, no web fonts, no remote images, nothing that breaks when the reader opens it on a plane. System font stack is fine and loads instantly.

Page order:

- Title, then the spine sentence in one line, large. A reader who bounces after four seconds should still leave with the spine.
- The beats, one per full section, in order.
- A close titled for the payoff, not for the format. State the one thing to remember and the nearest place the reader will actually run into this.

Constraints, all of them non negotiable:

- Readable at 375px wide. Nothing overflows, the page body never scrolls sideways. Wide diagrams scroll inside their own container.
- Light and dark, via `prefers-color-scheme`. Strokes and labels stay readable in both.
- Body text at least 4.5:1 against its background, in both themes.
- SVG text stays real `<text>`, never converted to paths. Every SVG gets a `<title>` and a `<desc>` so a screen reader gets the same explanation.
- Motion reveals content, it never gates it. Use an IntersectionObserver for fade and rise, no libraries, and honor `prefers-reduced-motion` by showing everything at once. With JavaScript disabled, every beat is still visible.
- One accent color that means exactly one thing on every beat. If red means danger in beat 2, it cannot mean the database in beat 5.

## Where output goes

Save to `explainers/<topic-slug>.html` under the current project, or into the folder the user names. Print the absolute path when you are done, and open the file if you can.

## Ship check

Run all six before you hand it over. Fix, do not explain away.

1. **Cover the text.** Can a stranger trace the mechanism from the drawings alone? If not, the drawings are decoration and the page has failed at its one job.
2. **Read the claim lines on their own,** top to bottom. They should already form a paragraph that explains the thing.
3. **Resize to 375px.** No horizontal scroll on the body, no clipped labels.
4. **Toggle dark mode.** Every stroke, fill, and label survives.
5. **Disable JavaScript.** Every beat still shows.
6. **Count unlabeled shapes.** The answer is zero.

## When to reach for something else

- Comparing quantities: that is a chart, not an explainer.
- Choosing between options: that is a table.
- Steps the reader will perform with their hands: that is a checklist.

This skill is for one situation only, and it is a good one: "I do not understand how this works."

## Attribution

Adapted from [SV Academy's explainer-graphic skill](https://github.com/sva-admin/explainer-graphic) (commit [`7e6bc02`](https://github.com/sva-admin/explainer-graphic/tree/7e6bc02c7fa6fa87e37a216537d37351c16cbfc8)), copyright © 2026 Silicon Valley Academy, under the MIT License. See [LICENSE](LICENSE).
