---
name: vietnamese-language
version: 1.0.0
description: >
  Vietnamese language reference layer — loaded on demand by other skills, pipelines,
  and agents. 17 reference files covering: platform-specific cultural dynamics
  (Facebook/TikTok/Instagram/LinkedIn/Zalo/YouTube/Twitter-X/Threads), formal document
  conventions, press release structure, viral content patterns, educational content norms,
  SEO/diacritic strategy, regional dialects, Gen Z slang taxonomy, advertising cultural
  frameworks, and email/messaging conventions. Does NOT duplicate content-creator/languages/vi.md
  (power words, hooks, CTAs, tone registers), marketing suite (funnel strategy, KPIs, ad
  templates), or proofreader/SKILL.md (grammar rules, tone mark errors). Load this when the
  task requires deep Vietnamese cultural/linguistic context beyond surface-level platform specs.
---

# Vietnamese Language Knowledge Base

Pure reference layer. No workflows, no agents, no presets — just knowledge files that other skills consume on demand.

## Boundaries

**Already covered — do NOT load these reference files if what you need is:**
- Power words, hook templates, CTAs, 4 tone registers, diacritic/Unicode rules, platform surface conventions → `content-creator/languages/vi.md`
- Ad copy structure (6 variants), TOFU/MOFU/BOFU templates, compliance checklist → `marketing/05-copy-quang-cao/`
- Email sequence strategy, automation, KPIs → `marketing/14-email-marketing/`
- Grammar rules, tone mark errors, code-switching → `proofreader/SKILL.md`
- Active VN editing (de-template prose, translationese cleanup, deep grammar check, style consistency) → `humanizer-vi`, `translationese-cleaner-vi`, `grammar-checker-vi`, `style-guide-vi`
- Platform format specs (character limits, aspect ratios, hashtag counts) → `content-creator/references/platforms.md`

**This skill fills the gap for:** deep platform cultural dynamics, formal/legal/press Vietnamese, viral pattern mechanics, SEO diacritic strategy, regional dialects, Gen Z slang formation patterns, advertising cultural values framework, and email/messaging register conventions.

---

## Routing Table

Read this table to decide which reference file to load. Load only the file(s) needed for your current task.

### Platform Files (`references/platforms/`)

| Task signal | Load |
|---|---|
| Facebook Groups, livestream sellers, Marketplace, age-segment register | `references/platforms/facebook.md` |
| TikTok challenge vocabulary, duet/stitch language, FYP hooks, trending audio | `references/platforms/tiktok.md` |
| Instagram VN aesthetic captions, carousel education, Story interaction, collabs | `references/platforms/instagram.md` |
| LinkedIn VN B2B register, hierarchy/deference, job posting language | `references/platforms/linkedin.md` |
| Zalo OA broadcast copy, mini app flows, customer service, boss/parent norms | `references/platforms/zalo.md` |
| YouTube VN title optimization, description, comment engagement, Shorts | `references/platforms/youtube.md` |
| Twitter/X VN short-form, real-time commentary, thread structure | `references/platforms/twitter-x.md` |
| Threads VN creator register, conversation threading | `references/platforms/threads.md` |

### Topic Files (`references/`)

| Task signal | Load |
|---|---|
| Government document (Nghị định, Thông tư, Quyết định) | `references/formal-documents.md` |
| Business correspondence, memo, proposal | `references/formal-documents.md` |
| Academic or legal writing in Vietnamese | `references/formal-documents.md` |
| Press release / thông cáo báo chí | `references/press-releases.md` |
| Viral content mechanics, 2024–2026 formats | `references/viral-content.md` |
| Challenge participation, meme culture | `references/viral-content.md` |
| Seasonal content (Tết, Mid-Autumn, national holidays) | `references/viral-content.md` |
| Educational content, EduTok, e-learning | `references/educational-content.md` |
| Ministry of Education language standards | `references/educational-content.md` |
| SEO Vietnamese keywords, diacritic strategy, CocCoc | `references/seo-content-marketing.md` |
| Content marketing structure, long-form blog | `references/seo-content-marketing.md` |
| Northern vs Southern vocabulary differences | `references/regional-dialects.md` |
| Brand targeting Hà Nội vs Hồ Chí Minh | `references/regional-dialects.md` |
| Diaspora Vietnamese (Việt kiều) | `references/regional-dialects.md` |
| Gen Z slang formation, internet language, teen code | `references/gen-z-slang.md` |
| Number substitution, English loanword integration | `references/gen-z-slang.md` |
| Advertising values framework, Confucian/Buddhist persuasion | `references/advertising-copywriting.md` |
| KOL/KOC integration patterns, celebrity endorsement language | `references/advertising-copywriting.md` |
| Seasonal campaign language (Tết copy, 8/3, 20/10) | `references/advertising-copywriting.md` |
| Regulatory language (Bộ Y Tế, health claims) | `references/advertising-copywriting.md` |
| Business email register, customer service scripts | `references/email-messaging.md` |
| Newsletter conventions, SMS marketing | `references/email-messaging.md` |
| Automated message templates, chatbot copy | `references/email-messaging.md` |

---

## Integration Points

These existing skills should cross-reference this skill:

- **`content-creator`** with `language=vi`: supplements `vi.md` with platform deep-dives when the brief specifies Zalo OA, LinkedIn VN, YouTube VN, or Twitter/X VN (platforms not covered in vi.md)
- **`marketing/05-copy-quang-cao`**: load `advertising-copywriting.md` for Tết campaign copy or health/beauty copy requiring Bộ Y Tế compliance language
- **`marketing/14-email-marketing`**: load `email-messaging.md` for Zalo OA broadcast conventions and Vietnamese newsletter register
- **`marketing/04-script-video`**: load `gen-z-slang.md` when target audience is under 25 and brief requires authentic slang
- **`proofreader`**: load `formal-documents.md` when proofreading government/legal documents; load `press-releases.md` when proofreading thông cáo báo chí

---

## Loading Protocol

1. Check the routing table above for your current task
2. Load only the matching reference file(s) — never load all 17
3. If your task spans multiple areas (e.g., Tết TikTok campaign for Gen Z), load the relevant files (tiktok.md + viral-content.md + gen-z-slang.md)
4. Cite which reference file(s) you loaded in your output so downstream agents know what was consulted