---
name: motion-brief
description: Use when starting any motion video, when a video request is a one-liner or vague, or before any film code is written.
---

# Motion brief

This skill writes the brief and stops for approval twice: after the shotlist, and after the stills.

## 1. Interview (one message, then wait)
Ask only what the request doesn't already answer:
1. What is it, in five lines? Who watches, and what should they believe and do after?
2. The pain, in the words a customer would use.
3. Three features, in order, and the payoff: one real result or number. Is everything on those screens public yet (unreleased features, customer names)?
4. Call to action and link.
5. Style (list `../motion-video/styles/`), length, formats (16:9, 1:1, 9:16), and where it will be posted (its safe areas).
6. References: 1-3 videos, a frame, or a folder of your own images. Name the style in words as well as linking it.
7. Voice: none, your recording, or TTS labelled as AI.
8. Facts: every number or claim you want on screen, with where it comes from.
9. Brand: the logo file, typefaces, colours and tone. Never invent a logo; with none supplied, the product name is set in type.
Default anything missing from the style card and say which. Never default the payoff or the call to action.

## 2. Write, in `<slug>/`
- `BRIEF.md`: the one-line message (what the viewer should believe at the end), audience, style, length, formats and where it's posted, brand (logo, type, colours), voice, references and what to take from each (grammar only), payoff, CTA.
- `facts.md`: `| claim as shown | source | date | kind |`, kind `fact` or `example`. A claim with no source is cut or becomes an `example`.
- `shotlist.md`: on the beat grid from the style's tempo. Per shot: beats, the real UI state (or "illustration" for non-product elements in story styles), camera, on-screen text, effect, and which fact it shows. The first frame states the pain or opens on the payoff; something new every 2-4 seconds.

## 3. Gate 1: shotlist
Show BRIEF.md and shotlist.md. Wait for OK. Notes are "problem + result wanted".

## 4. Gate 2: stills
After motion-capture (or straight after the shotlist when no product is on screen): `PY ENGINE/film.py frames <slug> <beat> ...` for 4-6 key beats (hook, first feature, payoff, end card). Show them. Wait for OK before any full render.

## Done when
Both gates are approved and `facts.md` covers every number in the shotlist. Hand over to motion-video (single film) or motion-director (long or multi-agent).
