---
name: explain-code
description: Explains code with visual diagrams and analogies. Use when explaining unfamiliar code, onboarding a beginner, walking through a tricky function, or breaking down a system's flow. Triggers on phrases like "explain this code", "walk me through", "how does this work", "I don't understand this function".
---

# Explain Code

Make code understandable to a beginner without dumbing it down. Lead with intuition, follow with mechanics.

## When explaining code, always include:

1. **Start with an analogy.** Compare the code to something from everyday life — a queue at a coffee shop, a postal sorting room, a kitchen with multiple cooks. The reader should be able to picture what the code is *doing* before they understand *how*.

2. **Draw a diagram.** Use ASCII art to show the flow, structure, or relationships. Boxes for components, arrows for data, dashed lines for async or optional paths. A diagram beats three paragraphs of prose.

3. **Walk through the code.** Explain step-by-step what happens — line by line for tricky bits, block by block for routine bits. Cite line numbers (`file.py:42`) so the reader can follow along in their editor.

4. **Highlight a gotcha.** What's a common mistake or misconception? What did *you* misread the first time? What invariant looks obvious but isn't? One sharp warning is worth more than a generic "be careful."

Keep explanations conversational. For complex concepts, use multiple analogies — different mental models reveal different facets.

## Format template

When you invoke this skill, structure the response like this:

```
## The big picture
<one-sentence analogy>

## The diagram
<ASCII art>

## The walk-through
1. Line X: ...
2. Line Y: ...
   ...

## The gotcha
<the one thing people get wrong>
```

## Examples of good analogies

- **Async/await** → ordering at a coffee shop with a buzzer: you place the order (await), the barista works on it while you sit down (event loop runs other tasks), the buzzer goes off when ready (promise resolves).
- **Recursion** → Russian nesting dolls: each call opens a smaller version of the same problem until you hit the smallest doll (base case), then you assemble back up.
- **Closures** → a backpack the function carries everywhere: even when called somewhere else, it still has access to the variables that were in scope when it was defined.
- **Mutex / lock** → the bathroom key at a gas station: only one person at a time, you wait for the key, you give it back when done.
- **Pub/sub** → a newsletter: publishers send issues, subscribers receive them, neither knows who the other is.
- **Database transaction** → a Word doc with "track changes" — you can keep editing, but nothing's saved until you commit; one click of "discard" rolls everything back.

## Diagram patterns

**Sequential flow:**
```
[input] ──▶ [step 1] ──▶ [step 2] ──▶ [output]
```

**Branching:**
```
              ┌──▶ [path A]
[decision] ──┤
              └──▶ [path B]
```

**Async / event loop:**
```
caller ──await──▶ [task]            ┐
   │                                │ event loop runs
   │  ◀────── result ──────         ┘ other work meanwhile
```

**State machine:**
```
[idle] ──start──▶ [running] ──finish──▶ [done]
                     │
                  cancel
                     ▼
                 [cancelled]
```

## When NOT to use this skill

- One-line edits or trivial syntax fixes — the analogy overhead isn't worth it.
- The user explicitly asks for terse output ("just give me the diff", "what's the fix").
- Code review feedback — use the `requesting-code-review` skill instead; reviews need findings, not pedagogy.

## Calibration

Match the depth of explanation to the question:
- "What does this line do?" → walk-through only, skip the analogy.
- "How does this whole module work?" → full template (analogy + diagram + walk-through + gotcha).
- "I'm a beginner, help me understand X" → full template + a second analogy at the end.
