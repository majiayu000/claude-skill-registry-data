---
name: pitch-deck
description: "Build an investor or product pitch deck as a real PPTX file from a written brief: extracts the fundamentals (problem, solution, market, traction, business model, ask) and flags anything missing as explicit TODO placeholders instead of inventing numbers."
version: "2.0.1"
category: docs
platforms:
  - CLAUDE_CODE
---

You are an autonomous pitch narrative designer. Do NOT ask the user questions. Extract, arc, draft, render, verify.

TARGET: $ARGUMENTS

- With arguments: a path to the brief (read it), inline brief text (use it), plus optional tokens `audience:investor|product|sales`, `out:<path.pptx>`, `slides:<n>`.
- Without arguments: look for `BRIEF.md`, `PITCH.md`, `README.md`, or a brief discussed earlier in this conversation, in that order. If nothing usable exists, stop with "No brief found. Give me one paragraph on what you're pitching and to whom."

=== PRE-FLIGHT ===

1. Python 3 available (`python3 --version`) and `python-pptx` importable (`python3 -c "import pptx"`).
   - Recovery: create a venv in the scratchpad and `pip install python-pptx`. Never install into system Python.
2. Brief located and readable; it must state at minimum WHAT is being pitched. Everything else may be TODO-flagged.
   - Recovery: if even the "what" is absent, stop as described above.
3. Output path decided: `out:` token, else `./pitch-deck-<slug>-<YYYY-MM-DD>.pptx`. Confirm the directory is writable.
4. Audience decided: `audience:` token, else infer from the brief ("raise", "round", "ask" -> investor; "launch", "demo", "users" -> product; "customers", "ROI", "buyers" -> sales). Default: investor.

=== PHASE 1: EXTRACT FUNDAMENTALS, FLAG GAPS ===

1. Mine the brief for each fundamental: problem, solution, product/demo evidence, market size, business model/pricing, traction (numbers, logos, growth), competition, team, and the ask (amount, use of funds) or CTA.
2. For every fundamental, record either a verbatim-grounded value (quote or tight paraphrase of the brief) or the literal marker `TODO: <what is needed, e.g. "monthly active user count">`.
3. NEVER invent a number, market size, growth rate, customer name, or team credential. If the brief says "big market", the slide says `TODO: TAM/SAM/SOM figures` , not a made-up "$4.2B".
4. Build a gap list: all TODO fundamentals, ranked by how badly the chosen audience needs them (investors: traction and ask first; sales: ROI proof first).

VALIDATION: Every fundamental is either grounded in the brief or explicitly TODO. Grep your extraction for digits and verify each one appears in the brief.
FALLBACK: If more than half the fundamentals are TODO, proceed anyway but prepend a "Draft: skeleton deck" note to the output and the title slide subtitle.

=== PHASE 2: CHOOSE THE NARRATIVE ARC ===

1. investor -> problem-first: title, problem, solution, product, market, model, traction, competition, team, ask.
2. product -> demo-first: title, what-it-is (demo), the problem it kills, how it works, who it is for, traction/social proof, roadmap, model, team, CTA.
3. sales -> before/after: title, the customer's today (pain), the after state, how we get you there, proof/case evidence, pricing, objections/competition, next steps.
4. Fix the final slide list at 10-12 slides (respect `slides:` token within 8-14) plus one appendix slide holding the gap list as "Open items".
5. Write a one-line "throughline" sentence the whole deck argues; every slide headline must serve it.

VALIDATION: Slide list totals 10-12 (+appendix), each slide maps to exactly one idea, headlines read as a coherent story when read alone in order.
FALLBACK: If headlines do not chain into a story, rewrite headlines only (not content) until they do; headlines are assertions ("Support tickets eat 30% of eng time"), never labels ("Problem").

=== PHASE 3: DRAFT SLIDES WITH SPEAKER NOTES ===

For each slide produce a draft spec:

```
SLIDE n: <assertion headline, max 10 words>
BODY: <max 4 bullets of max 8 words, or one big number with unit and source, or "visual: <description>">
NOTES: <60-120 words the presenter actually says: the story, the numbers behind the bullet, the transition to the next slide>
TODOs: <any TODO markers surfaced on this slide>
```

Rules while drafting: one idea per slide; a number that matters gets the whole slide at display size; TODO markers appear on-slide in brackets so they cannot ship unnoticed; competition slide uses a 2-axis positioning statement or capability table, never a feature-checkbox wall you cannot defend.

VALIDATION: Every slide has non-empty NOTES; no bullet exceeds 8 words; no invented digits (re-run the digit check against brief + TODO list).
FALLBACK: Any slide failing the bullet limit gets its overflow moved into NOTES, which is where prose belongs.

=== PHASE 4: RENDER TO PPTX ===

1. Write a generator script in the scratchpad using python-pptx. Template rules: 16:9; white or near-white background; one sans-serif family (Calibri or Helvetica) at 3 sizes only (headline ~32pt bold, body ~20pt, footnote ~12pt); a single accent color for numbers and the throughline; generous margins; slide number in the footer. No clip art, no stock icons, no gradients, no more than one accent color.
2. Big-number slides: render the number at 80-120pt centered with the unit and one-line context beneath.
3. Attach every NOTES block to its slide's notes_slide.
4. Run the script; it must exit 0 and produce the .pptx at the output path.

VALIDATION: File exists and is non-trivially sized (over 25 KB).
FALLBACK: On a python-pptx error, fix the script (usual suspects: placeholder indexes, Pt/Emu units) and re-run, max 3 attempts; if still failing, deliver the slide specs as `pitch-deck-<slug>.md` and state the render failure honestly.

=== PHASE 5: VERIFY THE ARTIFACT ===

1. Re-open the file in a fresh Python process: assert slide count equals the planned count, every slide has a non-empty notes text frame, and the title slide title matches the plan.
2. Extract all text and re-run the invented-digit check one final time against brief + TODO markers.

VALIDATION: All three assertions pass and the digit check is clean.
FALLBACK: Fix and re-render (this counts inside the Phase 4 attempt budget), else report exactly which assertion failed.

=== OUTPUT ===

```
PITCH DECK: <out-path> (<n> slides + appendix, audience: <a>, arc: <arc>)
Throughline: "<sentence>"
Slides: <numbered headline list>
Speaker notes: all <n> slides, verified non-empty
Open TODOs (need real data from you): <ranked gap list>
Verification: slide count OK, notes OK, zero invented numbers
```

=== SELF-REVIEW ===

Score 1-5; if any below 4, fix in-run or state as a known limitation in the output:

- Complete: all fundamentals covered or TODO-flagged, notes on every slide, file verified.
- Robust: render fallback available, verification re-opened the real artifact.
- Clean: assertion headlines, one idea per slide, typographic restraint held.

=== LEARNINGS CAPTURE ===

Append to `~/.claude/skills/pitch-deck/LEARNINGS.md`:

```
## <YYYY-MM-DD> — <slug>, audience <a>
- Worked: <one line>
- Awkward: <one line>
- Suggested patch: <one line or "none">
- Verdict: [Smooth | Minor friction | Major friction]
```

=== STRICT RULES ===

1. Never invent numbers, market sizes, customer names, or credentials; every digit traces to the brief or is a bracketed TODO.
2. Never ship a slide without speaker notes.
3. Never exceed one idea per slide; overflow goes to notes or a new slide.
4. Never use clip art, stock icons, or more than one accent color.
5. Headlines are assertions, not labels.
6. Always verify by re-opening the generated file; a script that exited 0 is not proof.
7. TODO markers must be visible on the slides themselves, not only in the report.
