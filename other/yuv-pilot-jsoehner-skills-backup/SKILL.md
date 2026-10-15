---

name: yuv-pilot

description: |

  Top-of-pyramid orchestrator for Yuval Avidani's YUV.AI brand work. Apply when the user wants YUV.AI output and the medium is ambiguous or multi-medium, or for strategic planning. Triggers: "for YUV.AI", "for my brand", "YUV.AI launch", "ship something for me", "orchestrate", "cross-channel", "multi-platform for me", "yuv-pilot", Hebrew השקה, מולטי-פלטפורמה ל-יובל. It routes intent to the correct downstream YUV.AI skills (decks, design-system, viral-video, etc.) and handles multi-artifact composition.



---



# yuv-pilot — the YUV.AI skills pyramid



> The flight director. Doesn't fly the plane — tells you which crew member should.



This skill is the **top of the YUV.AI skills pyramid**. Its job is to recognise a YUV.AI brand request, identify what's actually being asked for, pick the right combination of downstream YUV.AI skills, and hand off cleanly. It does not produce visual output, write code, or render assets. It is a router.



The metaphor maps to the brand: in flight ops, the pilot doesn't refuel the aircraft, doesn't load the cargo, doesn't run ATC. The pilot decides the mission and tells the right specialist when to act.



---



## §0. When to apply — strict YUV.AI gate



### ✅ Apply when



- The user mentions **YUV.AI**, **"my brand"**, **"my design system"**, **"for me"**, **"my launch"**, **"my channels"**, **"Let's Fly High"**, OR explicitly invokes `/yuv-pilot`.

- The deliverable spans **multiple media** — a launch needing a site + deck + reel + social cards is the canonical case.

- The user is asking *"what should I build for YUV.AI"* / *"how do I ship X for my brand"* — strategic, not yet a single artifact.

- The medium is ambiguous and clarification would help — e.g. "do something for me about MCP" (could be deck, blog, reel, social, site section).



### ❌ Do NOT apply when



- The request is clearly **single-medium** AND a specific downstream skill obviously owns it:

  - *"Make me a YUV.AI deck about X"* → `yuv-decks` wins directly. yuv-pilot stays out.

  - *"Edit this video into a viral short for me"* → `yuv-viral-video` wins. yuv-pilot stays out.

- The request is **non-YUV.AI** (generic game / app / client work / third-party brand). The whole pyramid stays out.

- The user has already named the specific tool / skill they want.



The principle: **yuv-pilot is the front door for ambiguity.** When the path is obvious, let the specific skill take the request.



---



## §1. The YUV.AI skills pyramid



```

                          ┌─────────────────────┐

                          │     yuv-pilot       │  ← you are here

                          │  (intent → route)   │

                          └──────────┬──────────┘

                                     │

            ┌────────────────────────┼────────────────────────┐

            ▼                        ▼                        ▼

       ┌─────────┐            ┌─────────────┐          ┌──────────────┐

       │yuv-decks│            │ yuv-design- │          │ yuv-viral-   │

       │         │            │   system    │          │   video      │

       │  talks  │            │             │          │              │

       │ slides  │            │ palette,    │          │ short MP4s,  │

       │ keynotes│            │ typography, │          │ Reels, Shorts│

       │ open-   │            │ assets,     │          │ video-use +  │

       │ slide   │            │ socials,    │          │ hyperframes  │

       │ Yuval   │            │ credentials │          │ MrBeast-pace │

       │ voice   │            │ 3 modes     │          │              │

       └────┬────┘            └──────┬──────┘          └──────┬───────┘

            │                        │                        │

            ▼                        ▼                        ▼

        open-slide          tokens / components       hyperframes

        slide-authoring     brand assets               video-use

        nano-banana-pro     social link set            gsap

        mermaid-diagrams    lessons-learned            nano-banana-pro

        gsap                                           gsap

                            ╲                          ╱

                             ╲                        ╱

                              ╲                      ╱

                               ▼                    ▼

                          ┌─────────────────────────────┐

                          │ Brand DNA (Universal Fly    │

                          │ High Throughline)           │

                          │ • flight metaphors          │

                          │ • HUD + dials               │

                          │ • phoenix mark + watermark  │

                          │ • Anton + JetBrains Mono    │

                          │ • "Let's Fly High"          │

                          └─────────────────────────────┘

```



### How to read the pyramid



- **Top tier (orchestrator):** `yuv-pilot`. Routes intent.

- **Middle tier (opinionated YUV.AI skills):** `yuv-decks`, `yuv-design-system`, `yuv-viral-video`. Each owns one mode of output. Each calls down to the bottom tier.

- **Bottom tier (generic tools):** `open-slide`, `hyperframes`, `gsap`, `nano-banana-pro`, `video-use`, `mermaid-diagrams`, `slide-authoring`. Not YUV.AI-specific; the middle tier uses them.

- **The Brand DNA layer** runs across the entire pyramid — every YUV.AI output, regardless of medium, carries the flight throughline. The palette is the chapter; the motifs are the brand.



---



## §2. Routing table — medium → composition



When the deliverable is clear, route directly. When it's ambiguous, ask once and then route.



| User wants… | Lead skill | Compose with | Notes |

|---|---|---|---|

| **Slide deck / keynote / talk / hackathon presentation** for YUV.AI | `yuv-decks` | `yuv-design-system` (**Decks mode** — Fly High purple/yellow/grey) · `slide-authoring` · `open-slide` · optionally `nano-banana-pro` for hero imagery · optionally `mermaid-diagrams` for architecture diagrams | yuv-decks scaffolds via `./scripts/new-deck.sh`. Drops AGENTS.md / CLAUDE.md / .github/copilot-instructions.md into the new deck root. |

| **Website / landing page / portfolio / About page** for YUV.AI | `yuv-design-system` (**Neon mode** — pink/cyan/white or rich black) | `gsap` for non-trivial animation · `hyperframes` if the hero needs an MP4-renderable composition | New project: run `install-agent-instructions.sh /path/to/project` to drop in the cross-tool instructions. |

| **Cinematic scroll-scrub landing from a short video** (the github/lion/hope showcase pattern — 5–15s clip becomes a single-screen hero where scrolling scrubs the video frame-by-frame and 5 text overlays crossfade) | `parallax-landing-page` | Brings its OWN type stack (Anton + Caveat + Inter) and accent palette (gold/amber/accent/cream). Does NOT call `yuv-design-system` — they coexist. For YUV.AI parallax landings, optionally add the phoenix watermark + Linktree URL as throughline. | Saves to `~/Documents/yuv-projects/landings/<slug>/`. Reference implementations live at `examples/parasites/`. |

| **Apple-style video-scrub landing with normal sections below** (sticky hero scrubs N frames as you scroll, then content sections continue) | `video-to-landing-page` | `yuv-design-system` in **Neon mode** for YUV.AI projects; no design system at all for generic / third-party work | The shorter, more conventional sibling to `parallax-landing-page`. Use when the hero is a teaser and the rest of the page carries copy + CTA. |

| **Web app / dashboard / interactive tool** for YUV.AI | `yuv-design-system` (**Neon mode**) | `gsap` · framework of choice (React, Svelte, plain) · `mermaid-diagrams` if there's an architecture diagram | One-Anton-per-screen rule applies. Use `<CounterUp>` for big stats. Glow on hero / primary CTA only. |

| **Game / interactive 3D experience** for YUV.AI | `yuv-design-system` (**Neon mode**) | Three.js · `gsap` for tweening · `hyperframes` if the game is capture-destined for a reel | Faceted brand-colored geometry. Pink/cyan accents on rich-black canvas is the strongest look. |

| **Promo video / reel / short / TikTok / Shorts** featuring Yuval | `yuv-viral-video` | `video-use` (cuts) · `hyperframes` (composition layer) · `gsap` (motion graphics) · `yuv-design-system` for type/palette overlay decisions · optionally `nano-banana-pro` for cutaway imagery | Always renders BOTH 9:16 AND 16:9. Saves with `_V<N>` suffix. Opinionated YUV.AI editorial style — MrBeast pacing, signature glass cards. |

| **Captioned video / tutorial / talking-head with subtitles** (Hebrew, English, or any Whisper-supported language) | `video-edit` | `hyperframes` · `hyperframes-cli` · `yuv-design-system` for type/palette decisions if YUV.AI-branded · Whisper (large-v3 default) for transcription | More general than `yuv-viral-video` — transcript-review-before-render workflow, dual aspect (16:9 + 9:16 from same source), liquid-glass caption pills. Use when the user wants a captioned showcase rather than a viral MrBeast-paced short. |

| **Cinematic / cinematic AI-generated video / 3D virtual cinematography** for YUV.AI | `cinematic-ai-video` (if available) | `hyperframes` · `yuv-design-system` for any overlay typography · `nano-banana-pro` | When the source is fully AI-generated rather than edited footage. |

| **Signature video banner** (the cinematic looping iframe at the top of a YUV.AI landing page) | `yuv-design-system` (Neon site + Hyperframes-compatible composition) | `hyperframes` (renders the banner) · `gsap` (animation) | Pattern documented in `yuv-design-system/references/presentations.md` § Signature video banner. |

| **Social card / OG image / Instagram square / poster** for YUV.AI | `yuv-design-system` (**Neon mode** — or **Warm Editorial** for Hope/practical) | `nano-banana-pro` for in-brand imagery · `mermaid-diagrams` if technical diagram | Watermark bottom-right, canonical socials if there's a footer. |

| **Speaker bio / About card / "meet the host"** | `yuv-design-system` (**Neon mode**) | The canonical credentials block (2× GitHub Star, AWS Gen AI Superstar, Channel 12 News, AI Builder & Speaker, Founder YUV.AI) + canonical socials | Always uses `assets/profile-yuval-studio.png` for the photo. |

| **Hope / Marcus / bigcats.ai / practical.yuv.ai (course landing)** | `yuv-design-system` (**Warm Editorial mode**) | `hope-born-to-run` (if it's a Hope/Marcus campaign) · `cinematic-ai-video` for any wildlife clips · `nano-banana-pro` for editorial imagery | This is the only mode that bans pure `#FFFFFF`. Paper-grain texture mandatory. |

| **Cross-channel launch** (site + deck + reel + social cards + email) | **yuv-pilot stays loaded** | Calls each of the above in sequence. Recommend a build order: design system + brand assets in place → deck (for the talk) → site (for the landing) → reel (for distribution) → social cards (for amplification) → email (for list). | This is the canonical multi-medium case. Build the design system surface first; the rest borrows from it. |



---



## §3. Worked examples



### Example A — *"Build me something for my next AI talk"*



**Read:** YUV.AI signal ✓ (it's *his* talk), medium = deck. Single-medium → route directly to `yuv-decks`, no need for yuv-pilot to stay involved.



**Hand-off response:**

> Loading `yuv-decks` — it'll scaffold an open-slide project with the 4-act narrative arc (Boarding → Ascent → Cruise → Descent), use `yuv-design-system` in **Decks mode** (purple/yellow/grey, FlightHUD, PurpleBar, Anton headlines), and optionally pull in `nano-banana-pro` for hero imagery. What's the talk about, and who's the audience?



### Example B — *"I want to launch my new course. Need a website, a hype video, and Instagram posts."*



**Read:** YUV.AI signal ✓, multi-medium (site + video + social). Stay in yuv-pilot and orchestrate.



**Hand-off response:**

> Orchestrating a 3-artifact YUV.AI launch. The course is `practical.yuv.ai` → **Warm Editorial mode** across all artifacts. Build order I'd recommend:

>

> 1. **Site** → `yuv-design-system` (Warm Editorial) + Hyperframes-compatible signature video banner at the top.

> 2. **Hype video** → `yuv-viral-video` (or `cinematic-ai-video` if you want AI-generated footage) + `hyperframes` for composition.

> 3. **Instagram posts** → `yuv-design-system` (Warm Editorial) + `nano-banana-pro` for the editorial imagery.

>

> Same design tokens flow through all three so the launch reads as one piece. Confirm the build order and I'll start with #1.



### Example C — *"Build me a snake game"*



**Read:** No YUV.AI signal. Generic request. **Whole pyramid stays out.**



**Hand-off response (or just: don't apply):**

> Generic snake game — picking an appropriate aesthetic for the game, not the YUV.AI brand. If you'd like this to be YUV.AI-branded (Neon palette, phoenix watermark), say "for YUV.AI" and I'll route through the design system.



### Example D — *"Build me a YUV.AI snake game"*



**Read:** YUV.AI signal ✓, single-medium = game. Skip yuv-pilot, route directly to `yuv-design-system` (Neon mode) + Three.js or Canvas.



**Hand-off response:**

> Loading `yuv-design-system` in **Neon mode** — pink player, cyan food on rich-black canvas, Anton uppercase score, phoenix watermark in the corner. Building now.



### Example E — *"What should I build to announce I hit 50K subscribers?"*



**Read:** YUV.AI signal ✓ (it's his channel), strategic question — no medium picked. Stay in yuv-pilot.



**Hand-off response:**

> A 50K announcement is canonically a 4-artifact micro-launch:

>

> 1. **Instagram square infographic** with a 0→50K growth chart — `yuv-design-system` (Neon mode) + `nano-banana-pro` (or inline SVG).

> 2. **Short reel celebrating it** — `yuv-viral-video` over a candid selfie or screen-share of the channel hitting 50K.

> 3. **A slide in your next talk** thanking the community — `yuv-decks` will fold it into the Boarding act.

> 4. **A pinned X post + LinkedIn post** with the infographic + a thank-you.

>

> Which one first? I'd start with the infographic — it's the artifact every other piece will reference.



---



## §4. When to ask the user vs. just route



**Just route** (no question) when:

- The medium is named in the prompt ("a deck", "a reel", "a landing page", "a tweet image").

- The brand-family is named ("for my course" → Warm Editorial, "for Hope" → Warm Editorial).

- The user has been here recently and the convention is clear.



**Ask once** when:

- Multi-medium and the build order matters.

- "Something for my brand" without a deliverable named.

- An ambiguous mode hint ("kind of editorial?" — could mean Warm Editorial or could mean Neon with editorial spacing).



**Never ask twice for the same question.** Pick a default, commit, build, let the user redirect after seeing output.



---



## §5. The hand-off protocol



When yuv-pilot routes, it should:



1. **Name the composition** explicitly. *"Loading yuv-design-system in Neon mode + gsap for the animation."*

2. **Lock the mode** for any downstream call to `yuv-design-system`. Decks mode for slides; Neon for everything else web/app/game/dashboard/social; Warm Editorial for Hope / practical.yuv.ai family.

3. **Confirm the build order** for multi-artifact requests.

4. **Hand off** — let the specific skill take over. Don't keep narrating.



Example hand-off line:



> *"Routing to `yuv-decks` (lead) + `yuv-design-system` in Decks mode + `slide-authoring` for the open-slide contract. Starting the 4-act narrative now."*



---



## §6. Companion / external skills (not YUV.AI-prefixed)



These are the generic tools the middle tier calls down to. yuv-pilot doesn't load them directly, but should know they exist:



| Skill | Owns |

|---|---|

| `open-slide` | The slide framework — not a skill, a project template that `yuv-decks` scaffolds via its `new-deck.sh` script. |

| `slide-authoring` | Open-slide file contract, 1920×1080 canvas, type-scale defaults, vertical budget math. |

| `hyperframes` | HTML→MP4 video rendering. The pillar for any YUV.AI video output. |

| `hyperframes-cli` | The `hyperframes init / lint / preview / render` commands. |

| `video-use` | Transcription (ElevenLabs Scribe), word-snapped cuts, base.mp4 extraction. The cuts layer that `yuv-viral-video` uses. |

| `video-edit` | Sibling to `yuv-viral-video` — general captioned-video editor with transcript-review-before-render workflow, dual 16:9 + 9:16 output, liquid-glass caption pills, Hebrew + English + any Whisper language. Pairs with `yuv-design-system` for type/palette decisions. Use when the goal is a captioned showcase rather than a viral short. |

| `gsap` | Primary animation library across all YUV.AI work. |

| `nano-banana-pro` | Image generation. Use the active mode's palette in prompts. |

| `mermaid-diagrams` | Architecture / flow / sequence diagrams in markdown. |

| `parallax-landing-page` | Cinematic scroll-scrub landing from a short video — the github/lion/hope showcase pattern. Has its own visual language; sits beside yuv-design-system rather than under it. |

| `video-to-landing-page` | Apple-style video-scrub hero with normal-scroll sections below. Calls into yuv-design-system (Neon mode) for YUV.AI projects. |

| `cinematic-ai-video` | AI-generated cinematography (Sora / Veo / Runway). |

| `hope-born-to-run` | Hope (cheetah) + Marcus (white lion) campaign content. Pairs with Warm Editorial. |



---



## §7. When NOT to load yuv-pilot



- **Generic requests** — no YUV.AI signal. Step back.

- **Third-party brand work** — client X, friend's project, etc. Step back.

- **Single-medium with an obvious downstream skill match** — let that skill take it directly. yuv-pilot only adds value when there's ambiguity or multi-medium composition.

- **The user has already named the specific tool** — honor the explicit choice.



---



## §8. Self-check before handing off



- [ ] YUV.AI signal confirmed.

- [ ] Medium identified (or clarified with one question).

- [ ] Right downstream skills named in the composition.

- [ ] Mode locked for `yuv-design-system` (Neon / Decks / Warm Editorial).

- [ ] Build order proposed if multi-artifact.

- [ ] Hand-off line spoken, then yuv-pilot stops narrating and lets the specific skill work.



---



Maintained by [@hoodini](https://github.com/hoodini) · [yuv.ai](https://yuv.ai) · [@yuvalav](https://x.com/yuvalav)


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).
