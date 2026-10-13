---
name: drafting-multi-format-content
description: Draft production-ready templates for three formats — video/audio scripts (explainers, tutorials, shorts, voiceovers, podcast outlines, Lyria prompts), threaded long-form social (LinkedIn threads, X threads, IG carousels, Threads), and FlashFusion Customization Service customer lifecycle comms (intake, quote, design brief, proof, production, shipping, post-sale). Use whenever the user asks to script a video or podcast, draft a thread, build a carousel, or generate customer-facing templates for custom orders. Also triggers on proof approval, rush order, bulk inquiry, order amendment, rejection letter, testimonial request, case study, reorder template, voiceover script, explainer video, tutorial video, Reels script, TikTok script, Shorts script. When the user says "LinkedIn post" or "X post" without specifying length, default to the threaded-social library unless they clearly want a single short caption. Do NOT use for short captions, blog essays, KB articles, SOPs, or newsletter editions.
metadata:
  version: "1.1.0"
---

## Routing

Handles threads, carousels, video/audio scripts, and customer comms. For a single short social post in Kyle's voice: use generating-social-posts.

# Drafting multi-format content

Three template libraries in one skill. Each library has a different voice, structure, and acceptance criteria.

## When each library applies

| Format family | Use when | File |
|---|---|---|
| Video/audio scripts | The deliverable is spoken, narrated, or audio-first | `templates/video-audio.md` |
| Threaded long-form social | The deliverable is a multi-post thread on LinkedIn, X, Threads, or an IG carousel — longer than a caption, shorter and more episodic than a blog | `templates/threaded-social.md` |
| FlashFusion Customization Service | The deliverable is a customer-facing comm or form for a custom-order workflow (intake, quote, proof, production, shipping, post-sale) | `templates/ff-customization.md` |
| **NOT covered by this skill** | Short social captions, blog long-form essays, KB articles, SOPs, runbooks, The Prompt newsletter editions, persona-specific product listings, chaosclub lyric/liner entries | Use the matching lane-specific skill instead |

## Scope gates before drafting

Before writing any template body, confirm three things:

1. **Lane.** Which of Kyle's lanes does this serve? (FlashFusion, chaosclub, The Prompt, Loxihart, or a new lane.) Lane drives voice.
2. **Surface.** Where does this publish? (LinkedIn, X, Substack, Wix, internal.) Surface drives constraints.
3. **Persona.** Who reads it? (One of the 7 FF personas, a chaosclub subscriber, an Loxihart client, a mixed public audience.) Persona drives density and jargon level.

If any of the three is missing, ask before drafting. Do not guess the lane from topic alone — a thread about AI agents could be FlashFusion (persona drop), The Prompt (ecosystem take), or chaosclub (never — wrong lane).

## Default guardrails (apply to every template in this skill)

Pulled from Kyle's established anti-sycophancy and anti-slop defaults. These are non-negotiable across all three libraries.

- **No hype adjectives.** No "game-changer," "revolutionary," "unlock," "leverage," "power of." If the claim needs a hype adjective to land, the claim isn't strong enough.
- **One claim per line in short-form, one argument per beat in long-form.** Stacked claims dilute each other.
- **Evidence before adjective.** If you want to call something fast, give the number.
- **No AI tells.** No "in today's fast-paced world," no "in conclusion," no "it's important to note," no triple-parallel structure ("it empowers, enables, and elevates"), no rhetorical "but here's the thing." These are AI-generation fingerprints.
- **Sentence case in titles and headings.** Never Title Case.
- **No emoji unless the platform demands it** (IG carousels, sometimes TikTok captions — see per-template notes). Never in Loxihart or chaosclub. Sparingly in FF / The Prompt.
- **CLAIMS / GAPS footer on anything making testable claims.** Applies to opinion threads, case studies, post-mortems, and The Prompt Loxihart tier. Skip on pure narrative (chaosclub voice notes) and procedural (FF forms).
- **[SOURCED] vs [GENERATED] labels on any piece citing data or claiming facts.**

See `references/voice-guardrails.md` for the full anti-slop checklist.

## How to use this skill

1. User describes what they want to template or draft.
2. Identify format family → open the matching template file. Each template file has a TOC at the top — scan the TOC to locate the right template by number, then jump to that section rather than loading the entire file.
3. Run the scope gates (lane, surface, persona).
4. Select the closest template by use-case match, not by name fit.
5. Fill slots. Apply default guardrails. Add lane-specific voice overrides from the template's voice notes.
6. Run the acceptance criteria listed on the template before returning.
7. Append CLAIMS / GAPS footer if the template makes claims.

## What this skill does NOT cover

- Short-form social captions (single post, <=280 chars on X, <=3 lines on LinkedIn) — these live in the lane-specific short templates from the main content template system.
- Blog long-form (single-author essay, single-URL, >800 words) — different beat structure, different platform constraints.
- KB articles, SOPs, runbooks — Loxihart-only, covered separately.
- The Prompt newsletter editions — three-tier structure covered by the newsletter skill.
- Persona-specific product listings — Wix catalog templates live in the FlashFusion short-format library.
- Chaosclub lyric + liner note entries — different skill.

## Related references

- `references/voice-guardrails.md` — full anti-slop checklist


---

## Negative Evals — should NOT trigger this skill

1. "Write a quick LinkedIn post about what I learned today" — single short post in Kyle's voice, routes to generating-social-posts.

---

## CLAIMS
<!-- [SOURCED] or [GENERATED] labels for assertions in this skill. None yet — footer added by audit fix pass. -->

## COUNTEREXAMPLE
<!-- Known cases where this skill should NOT activate or may produce wrong output -->

## CONTRADICTIONS
<!-- ! Conflicts with other skills or system prompts -->
