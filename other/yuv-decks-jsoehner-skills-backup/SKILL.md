---

name: yuv-decks

description: |

  Build cinematic, narrative-driven presentation decks in Yuval Avidani's signature style using @open-slide/core. The user describes a topic and audience; this skill scaffolds an open-slide project, drafts the 4-act narrative arc (Boarding → Ascent → Cruise → Descent), writes every slide in the Yuval voice (plain-language, no jargon, story-driven), applies the brand visual language from yuv-design-system, and orchestrates companion skills for hero images and video moments. Triggers on "make a deck", "create slides", "build a presentation", "build a deck", "new deck", "presentation about", "talk deck", "hackathon deck", "open-slide deck", "yuv-decks", "yuv deck", "deck like Yuval", "מצגת", "שקפים", "דק", "מצגת על", "להכין מצגת". Use proactively whenever the user asks for ANY slide-based talk; the skill self-selects the right scope.



---



# yuv-decks — Build Yuval Avidani-style cinematic decks



The opinionated playbook for **talk decks** built on open-slide. Defines:



- **The Yuval voice** — plain-language, no jargon, story-driven

- **The 4-act narrative arc** — Boarding → Ascent → Cruise → Descent

- **The JourneyBar** — the single unifying visual on every slide

- **Companion-skill orchestration** — yuv-design-system, slide-authoring, nano-banana-pro, hyperframes, mermaid



**Visual palette is pulled from `yuv-design-system` in Decks mode** — Fly High purple/yellow/grey (the dedicated palette for slide-based output). For talks whose central metaphor IS literal flight, this skill's own **cinematic-flight** opt-in mode (sky-blue + hot pink) — see Step 5 — overrides the design system's Decks tokens. Never use Neon mode for slides; Decks mode is exclusive to presentations.



This skill is the distillation of building "Build Agents That Ship" for the NICE pre-hackathon (May 2026). Read it end-to-end before drafting any slides.



## Where this skill sits in the YUV.AI pyramid



`yuv-decks` is in the **middle tier** of the YUV.AI skills pyramid. The top-tier orchestrator `yuv-pilot` routes here when the user wants a slide deck. You can also be invoked directly when the user says "make me a deck" without going through yuv-pilot first.



When this skill calls `yuv-design-system`, it **MUST lock the mode to "Decks"** — never let it fall through to Neon (web/app palette) or Warm Editorial. Decks mode is the only palette mode for slides.



See `yuv-pilot/SKILL.md` for the full pyramid map and routing table.



**Reference implementation**: <https://github.com/hoodini/build-agents-that-ship> (private — clone if you have access; the entire pattern this skill describes is implemented there).



---



## What this skill builds on



`yuv-decks` is the **opinionated layer**. It explicitly delegates to:



| Skill | Owns | When to consult |

|---|---|---|

| **`yuv-design-system`** | Palette, typography, animation library, brand assets, signature components (`PurpleBar`, `YellowUnderline`, `FlightHUD`, `CompassDial`, `CounterUp`, `HeroBg`), canonical social links, Hyperframes patterns | Always. Step 5, Step 6, and any time you touch palette/type/components. |

| **`slide-authoring`** | Open-slide file contract, 1920×1080 canvas, type scale defaults, vertical budget math, asset paths, hard framework rules | When writing the JSX for each page (Step 6 onward). |

| **`create-slide`** | Generic open-slide author (asks scoping questions and picks a theme) | For non-Yuval-voice decks (other people, generic content). `yuv-decks` supersedes it for Yuval's signature talk style. |



The yuv-decks rules **add on top** of yuv-design-system and slide-authoring; they never override them.



---



## When to invoke this skill



The user wants a *talk* or *presentation* deck. Triggers:



- "Make me a deck about X"

- "Create slides for a talk on Y"

- "Build a presentation for the [company] hackathon"

- "I'm presenting about Z — help me build the deck"

- "מצגת על..." / "שקפים על..." / "דק על..."



Do NOT invoke for: a single landing page, a video, a document, a Google Slide PowerPoint export. This skill is for **open-slide React decks** rendered at 1920×1080 with cinematic motion.



---



## Step 0 — Bootstrap the project



**Default save location:** `~/Documents/yuv-projects/decks/<deck-slug>/` — always save decks here so you can find them again later. The skill creates the parent directory if it doesn't exist. Override only if the user explicitly asks for a different location.



```bash

# Pick a slug. Lowercase, hyphenated, descriptive.

mkdir -p ~/Documents/yuv-projects/decks

cd ~/Documents/yuv-projects/decks

npx @open-slide/cli init <deck-slug>

cd <deck-slug>

npm install

npm run dev   # starts the preview at http://localhost:5173

```



Final path: `~/Documents/yuv-projects/decks/<deck-slug>/`. Tell the user where the deck lives at the end of every session.



The scaffold creates `slides/getting-started/` (a demo). You will create your own slide under `slides/<deck-id>/index.tsx` and delete or ignore the demo.



---



## Step 1 — Scope the deck (ASK BEFORE WRITING)



Before drafting, lock in these four decisions via a single `AskUserQuestion` (multi-question form):



1. **Topic & audience** — what is the deck *for*, and *who* will be in the room? Get the customer's actual agenda if possible (literal bullets they expect to hear) — match 1:1.

2. **Page count** — Short (5–6), Standard (8–10), Deep dive (12–24).

3. **Language** — English / Hebrew / Bilingual. Yuval is bilingual; pick based on audience.

4. **Speaker context** — Is Yuval the presenter? Is this for a specific company (NICE, etc.)? Knowing the host lets you craft callback moments ("…yes, the company you're sitting in…").

5. **Visual mode** — Fly High (default purple) or cinematic-flight (sky-blue + hot pink, only when the talk's central metaphor IS literal flight). When in doubt: Fly High.



Do NOT skip this step. Every redirect later in the build traces back to a wrong assumption here.



---



## Step 2 — The Yuval Voice (non-negotiable rules)



All copy follows these three rules:



### Rule 1 — Plain language, never jargon

Replace every term that isn't a household word:



| Don't say | Say instead |

|---|---|

| EBIT | real profit |

| PoC | the prototype / the demo phase |

| BYOC | your own cloud |

| service-account-as-god | admin-token-for-everything |

| RAG | lookup before answering |

| fine-tuning | training the model on your data |

| vLLM | local LLM runner |



If a *name* must stay (LiteLLM, Bedrock, Anthropic, Cognigy) — keep it, but **define it in 3 words on first mention** ("LiteLLM — an AI gateway library").



### Rule 2 — Short sentences. Punchy fragments. Like this.

Maximum **8–12 words per bullet**. Cut all "thus / therefore / however." If a sentence wraps to 3 lines, split or shorten.



**Calibration test** — transform this BEFORE writing any draft:



> ❌ "When Watson got a recommendation wrong, nothing learned from it. Same mistakes, repeated for years. The system never improved with use."

>

> ✅ "Watson made a mistake. Watson kept making it. For years."



### Rule 3 — Define every name on first mention

"Watson is IBM's AI. Won Jeopardy in 2011. Then aimed at hospitals."

"Klarna is Sweden's biggest fintech — Buy Now Pay Later, 150M customers."



Never assume the audience knows who/what.



---



## Step 3 — The Narrative Arc (4 acts)



The structure that survives audiences:



```

ACT I · BOARDING — The Stakes              (slides 1–4)

  Cover · Hook stat · Sources agree · Failure patterns



ACT II · ASCENT — The Stories              (slides 5–9)

  Failure case story · Why it failed (4 bullets) ·

  Success case story · Why it worked (4 bullets) ·

  Reference example (real product the audience knows)



ACT III · CRUISE — The Build               (slides 10–22)

  Anatomy · Agent types · MCP · Multi-agent · Where to apply ·

  Client stack · Server infra · Gateway · Routing · Tracking ·

  Optimization · Evals · MVP → Production



ACT IV · DESCENT — The Action              (slides 23–24)

  How to start tomorrow · Closing

```



**Structural laws:**

- Case studies CLUSTER together (slides 5–9). Don't interleave with considerations.

- Each case study is **TWO slides**: the *story* + the *lessons* (4 specific failure points or success moves). The lessons slide is where "aha tokens drop."

- Stories BEFORE considerations. The audience needs *why it matters* before *how to do it*.

- Cut anything not in the customer's agenda — even if you love it. (Examples cut in the NICE deck: ROI math, Mgmt Pitch, Skill-vs-Agent-vs-Feature-vs-Product, Obsolescence Check.)



---



## Step 4 — Case Study Triplet (failure + success + reference)



Always anchor with three **real, public, verifiable** stories:



| Role | What it is | Example used in the NICE deck |

|---|---|---|

| **Failure** | The most-funded, most-public AI/enterprise project that crashed. Name the *specific* failure points. | IBM Watson Health ($4B over 11 years, 0 patients helped) |

| **Success-with-caveat** | A real success that had to course-correct. Shows wins need humility. | Klarna AI Assistant (replaced 700 FTEs, then partly rehired) |

| **Reference** | A current production example the audience *already knows or owns*. **Bonus**: the company hosting the talk. | NICE Cognigy (NICE acquired it 2024) |



**Verifiable stats for the stakes act** (memorize these — they're real and citable):



- **MIT NANDA** "State of AI in Business 2025" (Aug 2025): **95% of GenAI pilots fail** to deliver measurable P&L impact.

- **Gartner** (mid-2024 forecast): **30%** of GenAI projects abandoned after PoC by end of 2025.

- **BCG** "Build for the Future 2024": **26%** of companies actually generate value from AI.

- **McKinsey** State of AI 2024–2025: **1 in 4** organizations see real profit from generative AI.

- **STAT News** + **University of Texas System Audit** (2017) for IBM Watson Health.

- **Klarna press release** (Feb 27, 2024) + Bloomberg/Fortune coverage (May 2025).



**Never fabricate a stat.** If you don't have a citation, use a *rule of thumb*, not a number with a fake source.



---



## Step 5 — Visual Language



The deck inherits **all** of its palette, typography, signature components, and animation defaults from **`yuv-design-system`**. Read those sections first:



- `yuv-design-system` **§1** — Palette modes (Fly High default; Warm Editorial for the brand family)

- `yuv-design-system` **§2** — Typography (Anton + Inter for English, Rubik + Assistant for Hebrew, letter-spacing 0 default)

- `yuv-design-system` **§6** — Signature components (`PurpleBar`, `YellowUnderline`, `FlightHUD`, `CompassDial`, `CounterUp`, `HeroBg`)

- `yuv-design-system` **§7** — Animation defaults + Hyperframes compatibility

- `yuv-design-system` **§3** — Brand assets (logo wordmark for watermarks, profile photo for about slides)



This skill is **opinionated only about what's unique to talk decks** — the narrative arc, the journey indicator, the cinematic-flight optional mode, the deck-specific entrance animation. Everything else: read the design system.



### Default mode: Fly High (purple)



Fly High is the default for all decks. Pulled from `yuv-design-system` §1:



```css

:root {

  --yuv-purple:      #5E17EB;   /* act-slide backgrounds, vertical accent bars, journey trail */

  --yuv-purple-dark: #3D0DA8;

  --yuv-yellow:      #FFEC00;   /* loud accent only — never a background */

  --yuv-grey:        #F1F2F2;   /* content-slide background */

  --yuv-white:       #FFFFFF;

  --yuv-black:       #000000;

}

```



**The two-background rule** (non-negotiable, from yuv-design-system):



- **Act slides** (cover, section dividers, hero stats, closer) — **purple background**, white headline, large Anton type.

- **Content slides** (everything else — info, evidence, lists) — **light-grey `#F1F2F2` background**, black headline.



No third background colour. Ever. Yellow is an accent, never a background.



The `<PurpleBar>`, `<YellowUnderline>`, `<FlightHUD>` components from `yuv-design-system` §6 ARE the deck's signature visual elements — use them.



### Optional mode: cinematic-flight (sky-blue + hot pink)



Only use when the talk's central metaphor IS literal flight (i.e., the "Build Agents That Ship" NICE deck where every slide leans into the flight arc). Most talks should stay on Fly High.



```ts

const cinematicFlight = {

  bg: '#dceaf6',        // sky-blue base

  text: '#1a1814',      // charcoal

  accent: '#ff3b8a',    // hot pink — the trail color

  yellow: '#ffd76e',    // soft sun

  cloudWhite: '#ffffff',

  skyDeep: '#7ab0d4',

  warmGray: '#6b7a8a',

  red: '#c8403d',       // failure indicators

  green: '#2f7d4f',     // success indicators

  shadow: 'rgba(80, 120, 180, 0.20)',

  hairline: 'rgba(26, 60, 100, 0.18)',

};

```



In cinematic-flight mode, swap the JourneyBar trail to `--accent` (hot pink) and use sky-blue as the act-slide background instead of purple. Everything else (Anton + Inter typography, JourneyBar structure, narrative arc, voice rules, reusable templates) is identical.



### The JourneyBar — the signature unifying element



This is **yuv-decks' single most powerful unifying element**, on every slide at the top edge.



Thin dashed flight-route line from `DEPART · [host company]` to `ARRIVE · [outcome]`. Solid trail fills as you progress through the deck (uses active palette's accent: purple in Fly High, hot pink in cinematic-flight). A small ✈ airplane icon sits at the current position with **dynamic pitch**:



- Act I Boarding → 90° (level, taxiing)

- Act II Ascent → 58° (nose up, climbing)

- Act III Cruise → 90° (level, cruise)

- Act IV Descent → 115° (nose down, descending)



Three terminal-dots mark the act boundaries. Phase label below the bar: `II · ASCENT 2/4`.



### Cinematic backgrounds (full-bleed nano-banana)



Every non-video slide gets a **full-bleed nano-banana image at 100% opacity** with:



- Ken Burns pan animation (`yuv-cinematic-pan`, 22s, `scale 1.04 → 1.06`, `translateX ±12px`)

- A directional bone-wash gradient (`textZone: 'left' | 'right' | 'bottom'`) keeping the text readable where it lives

- White content cards floating on top of the cinematic image



### Page entrance animation



```css

@keyframes yuv-page-enter {

  0%   { opacity: 0; transform: scale(1.06); filter: blur(10px); }

  60%  { opacity: 1; }

  100% { opacity: 1; transform: scale(1); filter: blur(0); }

}

```



Every slide enters with a 0.65s scale-and-defocus. Feels like a film cut.



---



## Step 6 — Companion skills (when to invoke which)



This skill orchestrates others. Invoke them at the right moment:



| Skill | When to invoke | What it does |

|---|---|---|

| **`yuv-design-system`** | Always — Step 5 and any palette/type/component decision | Visual brand source of truth. Pull palette tokens, type rules, signature components, brand assets, social link footer from here. |

| **`slide-authoring`** | Step 6 onward — when writing JSX | Open-slide hard rules: file contract, 1920×1080 canvas, vertical budget math, asset paths. |

| **`nano-banana-pro`** (or `anthropic-skills:nano-banana-2`) | After Step 5 — to generate cinematic hero/atmospheric images for every major slide. **Requires `GEMINI_API_KEY`.** | Image generation. Use the prompt template below. |

| **`hyperframes`** | For 4–5 high-impact video moments (cover intro, big-number reveal, case-study timelines, closing flourish). | HTML/CSS/GSAP video composition → renders to MP4 embedded as `<video>` in the slide. |

| **`mermaid-diagrams`** | For technical architecture diagrams when SVG is heavier than needed. | Clean flowcharts/sequence diagrams. |

| **Excalidraw MCP** (`create_view`) | For live-in-chat hand-drawn workflow diagrams you can show the user during design discussion. | Interactive Excalidraw rendering. |

| **`video-edit`** / **`yuv-viral-video`** | If the talk includes pre-recorded selfie footage that needs to be embedded. | Video editing pipeline. |



### nano-banana prompt template



Two flavours — match the active visual mode.



**For Fly High mode (default):**



```

[Scene description — 1–2 sentences, 16:9 cinematic frame, single focal subject]



STYLE: Cinematic editorial poster, electric-optimism dev-keynote aesthetic.

Vibrant. Luminous. Deep purple (#5E17EB) primary tones, electric yellow (#FFEC00)

warm accent lighting, near-black (#000000) shadows, soft grey (#F1F2F2) negative

space. Sharp lighting contrast. Generous space for typography overlay.

Movie poster, not infographic. NO TEXT. NO LOGOS. NO READABLE LETTERS.

```



**For cinematic-flight mode:**



```

[Scene description — 1–2 sentences, 16:9 cinematic frame, single focal subject]



STYLE: Cinematic editorial poster meets aviation-noir aesthetic. Vibrant. Luminous.

Dark moody background with neon-glow accents. Hot pink (#ff3b8a) as primary luminous

accent, soft sun yellow (#ffe066) as warm glow, sky blue (#7ab0d4) deep tones,

charcoal (#1a1814) shadows. Sharp lighting contrast. Generous space for typography

overlay. Movie poster, not infographic. NO TEXT. NO LOGOS. NO READABLE LETTERS.

```



Always: single focal subject (not a montage), one third of the frame as quiet sky for typography, explicit NO-TEXT instruction.



---



## Step 7 — open-slide framework rules



All open-slide framework rules live in **`slide-authoring`**:



- File contract (`export default [Page, …] satisfies Page[]`)

- 1920×1080 canvas, absolute px values only

- Single `index.tsx` per deck, assets under `slides/<id>/assets/`

- No new dependencies (`react` + standard web APIs only)

- Vertical budget math (every page must fit 1080px — bullets must NOT wrap)

- No `overflow: auto`



Read `slide-authoring` end-to-end before writing any page JSX. The yuv-decks rules ADD on top of these framework rules; they never override them.



---



## Step 8 — Reusable templates (copy these patterns)



The build-agents-that-ship deck has 4 reusable component templates. Copy them into your new deck:



### `UseCase` — consideration slide with pill, headline, bullets, metric card

Used for the Act III consideration slides (10–22). Two-column grid: text left, offset-shadow metric card right. Supports optional `bgImage` + `cinematicBg` for the cinematic look.



### `CaseStudy` — story-arc slide for failure/success/reference

Used for the three case studies. Top: status pill + period. Big company name. Tagline below ("Klarna is Sweden's biggest fintech…"). 4 fact-rows on left, image/video on right, pivotal moment box, lesson card, citation strip.



### `LessonsGrid` — 4-card "Why it failed/worked" pattern

Used right after each case study. Headline + 4 numbered cards in a 2×2 grid + colored takeaway strip ("Take this with you · …").



### `JourneyBar` — flight-path indicator at the top of every slide

The unifying element. Renders the dashed full route, the solid trail filled to current % (purple in Fly High, hot pink in cinematic-flight), three terminal dots, and the airplane icon with phase-dependent angle.



### `AtmosphericBg` — backdrop with `cinematic` mode

```tsx

<AtmosphericBg src={img} cinematic textZone="left" />

```



The full source for these templates is in `slides/claude-cowork-enterprise/index.tsx` in the reference repo. Copy verbatim, then adapt.



---



## Step 9 — The 12-step build workflow



```

1.  Get the customer's agenda (literal bullets). Map slides 1:1.

2.  Bootstrap: npx @open-slide/cli init <slug> && cd <slug> && npm install && npm run dev

3.  Ask the 5 scoping questions (Step 1). Lock in answers — including visual mode.

4.  Draft the 4-act outline (Step 3). Confirm with user before writing JSX.

5.  Write all slide components in a single index.tsx under slides/<deck-id>/.

    Use the reusable templates (UseCase, CaseStudy, LessonsGrid).

    Pull palette tokens + signature components from yuv-design-system.

6.  Add JourneyBar with PHASES matching your 4 acts.

7.  Invoke nano-banana-pro: generate ~10 cinematic atmospheric images

    (one per major slide, using the mode-appropriate prompt template).

    Save to slides/<deck-id>/assets/.

8.  Invoke hyperframes for 4–5 video moments (cover intro, hook reveal,

    case-study timelines, closing). Render to MP4, drop into assets/.

9.  Wire images and videos into slides. Use AtmosphericBg cinematic for

    images, full <video> for the dramatic moments.

10. Verify in browser: walk every slide. Check vertical budget. Check

    that no bullet wraps. Check that fonts loaded.

11. Iterate with the customer. EXPECT 5+ redirects. Don't fight them —

    each one improves the deck.

12. Push to a private GitHub repo BEFORE the talk so it survives a

    laptop failure. Include a README with clone-and-run instructions.

```



---



## Step 10 — Anti-patterns (things that look good but fail)



- ❌ **ROI math with division formulas** → use plain English ("Did it pay for itself? = What you got back ÷ What you spent.")

- ❌ **"Should you build it?" as 4 bullet points** → use a 2×2 quadrant matrix (high/low volume × repetitive/creative). Visual matrix is 10× clearer than prose.

- ❌ **Mgmt-pitch slides** in a hackathon deck → cut. Wrong audience.

- ❌ **Using cinematic-flight for a non-flight-metaphor talk** → default to Fly High purple. cinematic-flight is reserved for talks where literal flight IS the arc.

- ❌ **Same template for every slide** → looks uniform but boring. Add cinematic backgrounds per slide for unity-with-variety.

- ❌ **Citing fabricated stats** to a developer audience → use rules of thumb instead, or cut the number entirely.

- ❌ **EBIT, PoC, RAG, BYOC** dumped without definition → audience tunes out within 30 seconds.

- ❌ **"Watson failed because of misalignment"** → too abstract. Be specific: "Trained on textbook cases. Real patients aren't in the textbook."

- ❌ **Layouts that wrap text on bullets** → shorten or split.

- ❌ **`overflow: auto`** to hide overflowing content → the canvas doesn't scroll. Cropped content is gone.

- ❌ **Stacking multiple Anton elements on one slide** → see yuv-design-system §6 "One Anton element per slide / section."



---



## Step 11 — The DECK-PLAYBOOK.md file



After scaffolding, drop a `DECK-PLAYBOOK.md` at the project root for the speaker to add their personal notes. Section 10 of the playbook is intentionally a `TODO` checklist for the speaker to fill in after the talk:



> - [ ] _What worked in the room?_

> - [ ] _What would I do differently next time?_

> - [ ] _What surprised me?_



Each deck becomes feedback for the next deck. After 10 sessions, the playbook will be more accurate than the speaker's conscious memory.



---



## Step 12 — Repository structure (the deliverable)



```

<deck-slug>/

├── package.json               # @open-slide/core ^1.1.0

├── package-lock.json          # locks exact versions (commit this)

├── README.md                  # clone-and-run instructions

├── DECK-PLAYBOOK.md           # this skill, distilled for the speaker

├── AGENTS.md / CLAUDE.md      # symlinked open-slide rules + playbook link

├── open-slide.config.ts

├── slides/

│   └── <deck-id>/

│       ├── index.tsx          # ALL slides in one file (typically 22–24)

│       └── assets/            # *.mp4 (videos) + *.png (nano-banana images)

└── .gitignore                 # node_modules, .env*, .DS_Store

```



Push to a **private** GitHub repo before the talk:

```bash

gh repo create <user>/<deck-slug> --private --source=. --remote=origin --push \

  --description "..."

```



---



## Reference implementation



The exact pattern this skill describes was implemented at:



**<https://github.com/hoodini/build-agents-that-ship>** (private — clone if you have access)



## References & Loading Triggers



**MANDATORY - LOADING TRIGGERS**:

- Before locking visual palettes in Step 5, you **MUST** read [yuv-design-system](../yuv-design-system/SKILL.md) fully.

- Before constructing react JSX layouts in Step 7, you **MUST** read `slide-authoring`.

- **Do NOT load** design system references during Step 1 project bootstrapping steps.



### Dev Server Cache Issues & Package Dependencies

1. **Server cache warnings**: If newly added local image or video assets fail to load in the browser preview, restart the open-slide dev server (`npm run dev`) to refresh its build cache.

2. **Dependencies check**: Verify that `@open-slide/core` dependencies versions in `package.json` are compatible prior to editing slide contents.





That repo includes:

- 24 production slides in one `index.tsx` (~3000 lines)

- 5 HyperFrames-rendered MP4 videos

- 14 nano-banana cinematic backgrounds

- Reusable templates (UseCase, CaseStudy, LessonsGrid, JourneyBar, AtmosphericBg)

- The DECK-PLAYBOOK.md this skill is derived from



When unsure how to implement a pattern described in this skill, **read the corresponding file in that repo**.



---



## Closing principle



**The deck is for the audience, not for the speaker.**



Every layer of polish — voice, story, visual, motion — exists to make the audience feel they're on a journey, that the lessons are theirs to take, and that the speaker respects their time and intelligence.



If a slide doesn't pass the "would this drop an aha-token in the audience's mind" test, cut or rewrite it. Hollywood, not corporate. Story, not summary. Flight, not boxes.


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
