---
name: testimonial-film
description: "Customer testimonial editor for Claude: turns a real customer interview into a 60-150 s case-study film (result hook, problem, solution, numbers, recommendation) plus a 30 s cut and vertical clips, with the best soundbite first and every jump cut covered. Use when the user says 'edit this customer testimonial', 'make a case study video', 'client review video', 'success story', 'social proof video', 'cut the interview with our customer', or hands over a customer interview and product B-roll. Real customers, real words, real order only. Runs on video-studio-core (transcribe, selects, story, B-roll, mix, deliver, QC)."
license: MIT
---

# Testimonial Film

A real customer, in their own words, saying what changed: credible first, polished second.

- **Best for:** customer case studies, client reviews, agency results, B2B social proof, course student stories
- **Inputs:** customer interview (one or two angles), B-roll of the customer using the product, result screenshots, logo
- **Default skin:** `testimonial-card` · alternatives `split-proof`, `quote-card-reel`, `frame-studio`
- **Formats:** 16:9 master, 9:16 and 4:5 cutdowns
- **Durations:** film 60-150 s, cutdown 30 s, Shorts 15-45 s
- **Genre preset:** `--genre testimonial-film`

## Before you start

- Needs **video-studio-core** in the same skills folder. `CORE` = that folder, `SKILLS` = the skills folder.
- First run: `python CORE/scripts/check_env.py`.
- **Ethics (non-negotiable):** the speaker is a real customer, the words are theirs, and their meaning is unchanged.
  No actors presented as customers, no invented numbers, no `stars` rating unless the user supplies the real review.
  If the customer was paid, got a discount or free product, add a disclosure card (FTC / ASCI). Get the customer's
  sign-off on the final cut.
- Ask for: name, job title, company (spelled exactly), the result numbers and where they come from, logo permission.

## How a pro cuts this

**Structure (% of length)**

| beat | % | what goes here |
| --- | --- | --- |
| result hook | 10 | the single best soundbite: the outcome in their words |
| problem before | 25 | what life was like, the cost of the problem |
| solution | 30 | how they found and used the product, specific moments |
| result / numbers | 25 | concrete results, shown with counters or screenshots |
| recommendation + CTA | 10 | "I'd tell anyone who..." then logo and CTA |

**Pacing.** ASL 3-6 s, visual change at least every 5 s. Hold the face on emotional or credibility lines; B-roll the
explanations.

**Cut rules.**
- Paper edit from the transcript; the hook may move up from later in the interview (log it), but every sentence stays
  whole. `story.py reorder` flags partial splices (HIGH) and back-references (MED): resolve every flag.
- Cover every join: B-roll >= 0.5 s each side, second angle, or a >= 1.2x punch-in (`speaker.zooms`).
- Light filler removal; keep natural hesitations that make them sound real. Keep the breath before the key line.
- Never use a reaction or B-roll that changes the meaning (Kuleshov).

**Transition grammar.** Cuts and J/L cuts; one dissolve at most into the CTA. No flashy transitions.

**Music and sound.** Bed ~-24 dB under speech, ducked (`duck: "speech-aware"`), lifted at the recommendation.
Room tone on every join. SFX low (4/min): a soft tick on a counter.

**Colour.** Natural and trustworthy: `documentary-natural` or `portra` at 0.5. Brief says "punchy": `clean-commercial` 0.6.

**Captions.** Two-line sentence-case subtitles low in frame (`"preset": "clean"`), <= 17 cps; burned captions on verticals.

**What the client judges.** Credibility, the customer sounding natural, a concrete result.

**Common mistakes.** Starting with "Hi, my name is"; numbers nobody can verify; over-polished audio; obvious jump
cuts; music louder than the customer; a quote stitched from two answers.

## Make the edit

```bash
python CORE/scripts/run.py customer.mp4 --style SKILLS/testimonial-card --genre testimonial-film --format 16:9 --smart-cuts --retakes --logo logo.png --work tf --stop-after plan
python CORE/scripts/story.py outline --work tf --genre testimonial-film
# result hook first, then the story in order; read tf/story_flags.md
python CORE/scripts/story.py reorder --work tf --order "s14,s2-s13,s15-s18" --genre testimonial-film --format 16:9 --out tf/order.json
python CORE/scripts/run.py - --timeline tf/order.json --style SKILLS/testimonial-card --genre testimonial-film --format 16:9 --broll broll/ --music bed.wav --work tf2 --stop-after broll
python CORE/scripts/render.py tf2/plan.json --frames 1,10,30,60,85
python CORE/scripts/render.py tf2/plan.json
python CORE/scripts/finish.py tf2/plan.json --platform youtube
```

Long interview with many retakes: `selects.py --work sel --input customer.mp4`, edit `sel/paper_edit.md`,
`selects.py --work sel --apply --format 16:9`, then `run.py - --timeline sel/selects_spec.json ...`.
Vertical cut: same order spec with `--format 9:16 --duration 30` in a new work folder, or
`track.py reframe customer.mp4 --out cust_916.mp4 --format 9:16` first.

## Refine the plan

- **Hook text (muted viewers):** a `text` element in the first 2.5 s with the result in their words, quoted exactly.
- **Lower third** at their first line: `{"type": "lowerthird", "name": "Ravi Kumar", "role": "Ops Lead, Acme Foods", "start": 2.8, "end": 7}`.
- **Result numbers:** `{"type": "counter", "from": 0, "to": 38, "suffix": "%", "label": "fewer late orders", "start": 52.1, "end": 56}`
  only for numbers the customer says or the client documents. Check make_plan's auto counters against what is said.
- **Quote card:** `{"type": "quote", "text": "We got our weekends back.", "author": "Ravi Kumar", "role": "Acme Foods"}`, word for word.
- **Disclosure** (when compensated): `{"type": "chip", "text": "Paid partnership", "start": 0, "end": 4}` or an end card line.
- **Captions:** `{"type": "captions", "preset": "clean"}`; fix names and product terms in `words` (keep times).
- **Colour/audio:** `"color": {"look": "documentary-natural", "intensity": 0.5}`,
  `"music": {"src": "bed.wav", "under": 22, "duck": "speech-aware", "fitTo": "beats"}`, `"roomTone": true`.
- `python CORE/scripts/editor.py review tf2/plan.json --genre testimonial-film`; fix uncovered jump cuts it lists.
- B-roll videos (`cutaways`) show in the `--frames` stills; check each lands on the right line.

## Deliver

```bash
python CORE/scripts/deliver.py tf2/plan.json --to youtube,linkedin --out-dir tf2/deliver
python CORE/scripts/deliver.py tf30/plan.json --to reels,shorts --out-dir tf30/deliver
python CORE/scripts/qc.py tf2/deliver/final_youtube.mp4 --plan tf2/plan.json --platform youtube --strict
```

Hand over the film, the 30 s cut, verticals, `captions.srt`, 3 thumbnails (`thumb_*.png`) and the change log of any
reordered sentences for the customer's approval.

## Check before delivering

- Every sentence is whole and in context; `story_flags.md` has no unresolved HIGH flags.
- Name, title, company and numbers match the customer's approval; disclosure present if they were compensated.
- No visible jump cut; voice clean but natural; `qc.py` passes loudness and caption checks.
- The customer (or the client on their behalf) has approved the final cut.

## Example requests

- "Make a 90-second case study from this interview with our client, best line first."
- "Cut a 30-second vertical testimonial for Instagram with captions."
- "Add their results as numbers on screen: 38% fewer late orders, 6 hours saved a week."
