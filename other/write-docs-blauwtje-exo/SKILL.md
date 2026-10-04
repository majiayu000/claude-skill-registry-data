---
name: write-docs
description: "Use when writing or editing prose read later: a README or doc page, a PR, issue or commit body, a changelog line, a brief or spec. Not for chat replies (the output style), code comments (the code standard), or fields ship, file-issues and spec set."
argument-hint: <the document or text to write or edit>
---

# Technical writing

Prose for a reader who was not in the session says who does what, by which mechanism, in the plain word. The enemy is text that sounds finished and says little: a benefit where the fact belongs, a borrowed phrase, a paragraph that welcomes, teaches and lists at once. The overcorrection is telegraphic text stripped of articles and verbs, which the reader has to decode.

## The loop

1. **Pick one mode per document.**
   - A tutorial teaches by doing, a how-to gets a known task done, a reference lists what exists, an explanation says why.
   - A Usage section opens on the command, never on a welcome.
2. **State the fact, not the benefit.**
   - Give the number, the behavior or the error that changed, because "ensuring stability" or "more robust" asks the reader to trust what the text could have shown.
   - A request to show off, sell or impress still gets only the facts the input states, because an effect nobody measured is invented.
3. **Name the actor and the mechanism.**
   - Say who does what, because a passive verb or an abstract noun hides the part the reader has to find.
4. **Use the codebase's names.**
   - Use the real file, option, flag and command name.
   - Use one name per thing, because a synonym reads as a second thing.
5. **Write whole sentences in plain words.**
   - Keep the articles and verbs.
   - Prefer the period to the dash or semicolon.
   - Write one thought per sentence and split past 25 words.
   - Let a one-sentence slot, such as a Highlights line or a summary, hold only the change that matters most, because two joined with "and" bury both.
6. **Scan the draft against `references/ai-tics.md` and rewrite every hit before handing it over.**
   - In a review of someone else's text, cite each hit by its id.

## References

| File | Read it when |
|---|---|
| `references/ai-tics.md` | Step 6, on every draft, and when reviewing a text for machine-written tone. |

## Judgment

- The codebase's name outranks the plain word: `maxBytes` stays `maxBytes`.
- The fields ship, file-issues or spec set outrank this skill's layout; only the wording inside them follows it.
- A reader's ease outranks a rule: if following one hurts a sentence, mend it differently or keep it as written.
- Product interface strings follow the product's copy rules, not this skill.
