---
name: icaire-deckify
description: Build or improve ICAIRE presentation decks for leadership, partners, workshops, reports, internal working sessions, and public events. Use when the user asks for a slide outline, slide copy, speaker notes, visual structure, deck cleanup, or executive polish pass.
---

# ICAIRE Deckify

Create or improve a presentation deck that makes ICAIRE's message clear,
credible, and appropriate for the audience.

## Contract

- Start from the deck purpose, audience, format, deadline, and desired action.
- Use BigBrain or the ICAIRE MCP connector for ICAIRE facts, people, meetings,
  initiatives, partner context, prior language, and sensitivities when the user
  has not supplied enough source material.
- Match the deck to the setting: leadership update, partner briefing, workshop,
  report presentation, public event, or internal working session.
- Separate confirmed facts from proposed narrative, placeholders, and items that
  need approval.
- Keep slide copy concise and make speaker notes carry nuance where needed.
- Preserve the intended message when fixing slide layout. Do not weaken,
  delete, or shorten content just to mask a formatting problem when the slide
  has room for the content to fit.
- Include a polish pass for narrative flow, executive clarity, and stakeholder
  sensitivity.
- Before submission, render the deck visually, review every slide, iterate on
  weak slides, and only then report the deck as ready.
- Treat spacing and layout as first-order review criteria: look for cramped
  copy, weak whitespace, near-overlaps, misaligned elements, and text sitting
  too close to other text or page chrome.
- Ensure elements have sufficient padding and breathing room so the slide does
  not feel cramped, while avoiding unnecessary whitespace and keeping the
  composition balanced.
- Treat awkward line breaks as visual defects when they split a short phrase,
  leave a dangling word, or make a point look accidentally broken across lines.
- Use ICAIRE's primary brand color `#4A9549` as the main visual accent for
  deck themes, section dividers, charts, callouts, and other designed elements
  unless the user supplies a different approved design system.
- Use light variants of the primary brand color for card backgrounds, content
  panels, and subtle slide surfaces instead of default grey when the deck needs
  a branded but still quiet executive look. Use full-strength green sparingly
  for slim banners, rules, or emphasis, and keep title-slide gradients soft
  enough that all text remains high contrast.
- When available as local untracked assets, use the report-ready ICAIRE and
  UNESCO lockups from `../../assets/brand/report/` on title slides. Place them as restrained
  co-branding near the top of the title slide, commonly above the main title,
  preserve aspect ratio, and keep them clear of headers, banners, and title
  text. On colored, gradient, or image backgrounds, the deck builder must
  prepare logo/image assets explicitly: use alpha-enabled PNGs, generate
  transparent working copies, or place images on an intentional background
  color/panel that matches the slide design. Never rely on accidental white
  pixels from the source image. Do not commit deck assets, lockups, generated
  images, or other binary media to the skills repo.

## Workflow

1. Define the deck assignment.
   - Identify audience, purpose, meeting or event, target length, language,
     delivery format, and whether the deck is internal or external.
   - If the user gives raw material, preserve the intended message before
     restructuring it.
2. Gather context.
   - Read provided notes, outlines, old decks, reports, meeting notes, or source
     documents.
   - Query BigBrain or ICAIRE MCP for current ICAIRE context when names,
     initiatives, partner history, or claims are unclear.
3. Shape the story.
   - Create a slide sequence with a clear opening, evidence, implications,
     asks, and closing.
   - Choose the level of detail appropriate to the audience.
4. Draft slide content.
   - Write slide titles as claims or useful signposts.
   - Keep body copy short, specific, and scannable.
   - Add speaker notes for context, caveats, transitions, and talking points.
5. Add visual direction.
   - Suggest charts, diagrams, photos, logos, maps, timelines, or comparison
     tables only when they make the point clearer.
   - Identify missing assets or data needed to complete the deck.
6. Polish and verify.
   - Check narrative continuity, terminology, stakeholder sensitivity, and
     unsupported claims.
   - Mark placeholders and approvals needed before external use.
   - For actual deck files, render every slide or a full contact sheet before
     submission. Inspect the visual output, not just source text or file
     existence.
   - Iterate on any slide with awkward wrapping, clipped text, tiny unreadable
     copy, duplicate numbering, weak hierarchy, bad spacing, overcrowding, poor
     alignment, near-overlaps, or leftover placeholders.
   - Inspect inherited or unused template objects as well as visible text. If a
     placeholder, bar, or text area has no visible purpose, remove it or make
     its role explicit instead of leaving a hidden or empty object on the slide.
   - Inspect slides with dense text at full size, not only in a montage. A
     montage can hide spacing problems such as one line sitting too close to
     another block of text.
   - Check both sides of the spacing problem: too little padding around text,
     bullets, cards, charts, and footers; and too much empty space that makes
     the slide feel unbalanced or unfinished.
   - Check vertical rhythm between major elements. A large dead band below a
     paragraph, heading, chart, or card is a layout problem even when nothing
     overlaps.
   - Check whether text wraps at natural phrase boundaries. If a short point
     breaks mid-phrase and the slide has available space, fix the formatting
     first: widen the text box, adjust the object position or size, remove
     unnecessary manual line breaks, tune line spacing, or use natural phrase
     breaks. Shorten copy or move nuance to speaker notes only when the
     intended message is genuinely too long for the slide.
   - Check that branded treatments are systematic: repeated cards and panels
     should use the same light brand-surface treatment, while banners or
     gradients should support hierarchy without overpowering the content.
   - Check slide object order in the rendered output. Decorative meshes,
     gradients, color washes, and background shapes must sit behind titles,
     text, logos, charts, cards, and other content.
   - Re-render after edits and repeat the visual check until the deck is
     presentable for the stated audience.

## Output

Default to this structure unless the user requested another format:

- `Deck Purpose`: audience, setting, and desired outcome.
- `Slide Outline`: ordered slide titles with one-line intent.
- `Slide Copy`: title and concise body copy for each slide.
- `Speaker Notes`: optional notes for delivery and nuance.
- `Visual Structure`: recommended charts, diagrams, images, or layout cues.
- `Polish Notes`: tone, flow, and stakeholder-sensitivity improvements.
- `Missing Inputs`: facts, assets, approvals, or data still needed.
- For generated deck files, include `Visual QA`: what was rendered, what issues
  were fixed, and whether any residual visual risks remain.

## Guardrails

- Do not invent ICAIRE facts, metrics, partner positions, approvals, or event
  details.
- Do not overload slides with report-length paragraphs.
- Do not use public-facing claims that rely on internal-only context unless the
  user has approved that use.
- Do not make visual suggestions that require unavailable data without marking
  the dependency.
- Do not claim the deck is final when source material, design assets, or
  approvals are missing.
- Do not submit a generated deck after only checking that the file exists.
- Do not ignore rendered-slide problems because the text outline is correct.
- Do not leave empty inherited text boxes, bars, or placeholders in the final
  deck when they can confuse visual review or artifact annotations.
- Do not rely on a montage alone when it reveals possible clipping, wrapping,
  unreadable text, or weak hierarchy; inspect the affected full-size slides and
  revise them.
- Do not accept text that technically does not overlap but visually crowds
  another line, bullet block, footer, chart, or card. Fix the spacing, shorten
  the copy, move the note into speaker notes, or split the content.
- Do not solve cramped slides by blindly adding whitespace everywhere. Keep
  layouts balanced: trim copy, redistribute content, adjust placement, or move
  nuance to speaker notes so the slide has enough padding without feeling
  sparse.
- Do not accept unnecessary manual line breaks or accidental wrapping that makes
  concise points look split, especially on title slides, metrics, short bullets,
  and closing lists.
- Do not solve a formatting defect by deleting or weakening content when a
  layout adjustment would let the original message fit cleanly.
- Do not accept a slide merely because each object is individually readable;
  the relationships between objects must also feel intentional and balanced.
- Do not leave default grey cards or panels in a deck that is otherwise using
  ICAIRE brand color, unless the grey has a deliberate hierarchy role.
- Do not place decorative gradients, meshes, or background shapes above text,
  logos, or content. A background treatment that obscures or dulls content is a
  z-order defect, even if the source object list looks plausible.
- Do not use checkerboard-preview or rough source logo files in final decks
  when clean report-ready lockups are available.
- Do not assume a PNG has transparency because the saved source preview looks
  transparent. Check the alpha channel or rendered slide; if a logo shows a
  white box on a non-white background, fix the asset or add an intentional
  matching image background treatment in the deck builder before delivery.
