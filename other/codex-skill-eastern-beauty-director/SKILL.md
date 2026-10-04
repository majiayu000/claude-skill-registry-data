---
name: eastern-beauty-director
description: Director-level AI art prompt creation for Eastern beauty series, including Eastern fantasy / gu feng Chinese beauty character art, classical Eastern beauty, realistic and modern Eastern beauty, Cosplay展会摄影 / official convention cosplay photography with AAA game character campaign and Vogue editorial quality, 古风闺蜜 / AncientFemaleCompanionship two-person ancient Chinese female companionship photography, 东方美学图鉴 / 小红书图鉴 cover and content systems for 四大美人、四大才女、十二花神、东方神女、敦煌飞天、朝代服饰、东方器物、东方神话, 甜系纯欲生活写真 / SweetHomeGirl lifestyle portraits built around realism, feminine charm, romantic feeling, story moment, and natural attraction, new-Chinese-style fashion editorials, magazine portraits, worldbuilding, mythic role design, costume/styling systems, cinematic composition, lighting, negative prompts, and model-specific prompt variants. Use when the user asks for 东方美人, 东方审美, 东方美学图鉴, 小红书图鉴, 图鉴封面, 图鉴正文, 四大美人, 四大才女, 十二花神, 东方神女, 敦煌飞天, 朝代服饰, 东方器物, 东方神话, Cosplay展会摄影, coser, Coser, 漫展摄影, 展会摄影, ChinaJoy, Bilibili World, Tokyo Game Show, 游戏展台, 官方展会摄影, AAA游戏角色Cosplay, 古风闺蜜, AncientFemaleCompanionship, Ancient Female Companionship, 闺阁夜话, 姐妹古风写真, 古代闺阁生活, 灯下梳发, 共读, 夏夜纳凉, 守夜, 江南同行, 湖亭共伞, 山寺同行, 灯会夜游, 柔美, 妩媚, 成熟, 优雅, 高贵, 清冷, 温婉, 英气, 神性, 慵懒, 东方幻想, 古风美女, 古典东方美人, 宋韵, 唐宫, 江南, 洛神, 青瓷, 昆曲, 国风人物, 汉服女子, 写实东方美人, 现代东方审美, 新中式, 东方高级感, SweetHomeGirl, 甜系纯欲生活写真, 甜系纯欲, 甜美女友感, 真实女生, 自然抓拍, 故事感, 女友视角, lifestyle girlfriend portrait, 仙侠/武侠/宫廷/江南/敦煌风 AI 绘画提示词, image prompt optimization, style word expansion, character series concepts, or prompt packs for Midjourney, Stable Diffusion, ComfyUI, DALL-E, Gemini, Seedream, or other image generation tools.
---

# Eastern Beauty Director

## Core Workflow

Act as an art director, worldbuilding designer, cinematographer, costume designer, layout designer, content system designer, and prompt engineer for Eastern beauty imagery. Current coverage is strongest for gu feng and Eastern fantasy; if the user asks for realistic or modern Eastern beauty, preserve that direction and adapt the framework without forcing hanfu, mythology, or fantasy spectacle. If the user asks for 东方美学图鉴, 四大美人, 四大才女, 十二花神, 东方神女, 敦煌飞天, 朝代服饰, 东方器物, 东方神话, or 小红书图鉴内容, treat it as a visual-content-system task, not only a single beauty prompt.
Produce prompts that feel directed, specific, and image-ready rather than a list of pretty adjectives.

1. Clarify only when a missing choice changes the image: subject age category, era/subgenre, mood, image model, aspect ratio, or use case. If unclear, choose a refined default and state it briefly.
2. Classify the request intent with `references/request-router.md` when the user gives a short Chinese phrase, a structured Chinese parameter block, asks for a rewrite, requests a prompt pack, asks for SweetHomeGirl, asks for realistic/modern Eastern beauty, or names a platform. Use `references/style-taxonomy.md` as the canonical family map before adding or selecting any new style direction.
3. Lock explicit parameters before expanding: subject, style route, mood, costume, scene, prop, palette, aspect ratio, model/platform, output mode, and any "must keep / must avoid" instructions. Preserve them; add inferred defaults only as labeled supplements.
4. Apply `references/character-subject-system.md` as the global character diversity engine before writing any final prompt. Every image should explicitly choose a face structure, eye/brow detail, hairstyle, expression, makeup direction, posture/body-language note, and gaze target that fit the route. For multi-image or daily batches, do not reuse the same face, hairstyle, expression, pose, and camera relationship across images; the same Eastern beauty aesthetic universe must not become the same woman in different clothes.
5. Select the route family first. For 东方美学图鉴 / 小红书图鉴 / 四大美人 / 四大才女 / 十二花神 / 东方神女 / 敦煌飞天 / 朝代服饰 / 东方器物 / 东方神话 requests, load `styles/东方美学图鉴.md` and decide whether the output is cover, overview page, character page, timeline page, compare page, or knowledge page. For Cosplay展会摄影 / coser / Coser / 漫展摄影 / 展会摄影 / ChinaJoy / Bilibili World / Tokyo Game Show / 游戏展台 / 官方展会摄影 requests, load `styles/Cosplay展会摄影.md` and treat the result as official convention photography with original AAA-game-character cosplay quality, not ordinary convention snapshots. For 古风闺蜜 / AncientFemaleCompanionship / 闺阁夜话 / 姐妹古风写真 / 灯下梳发 / 共读 / 夏夜纳凉 / 守夜 / 江南同行 / 湖亭共伞 requests, load `styles/古风闺蜜.md` and treat the result as realistic ancient Chinese female companionship photography, not xianxia fantasy. For gu feng or Eastern fantasy visual direction, select exactly one primary route from `styles/东方幻想古风.md`. Do not blend incompatible routes unless the user asks for a hybrid; if hybrid is requested, name the dominant route and the secondary accent. For classical non-fantasy Eastern beauty, load `styles/古典东方美人.md`. For SweetHomeGirl / 甜系纯欲生活写真 requests, load `styles/甜系纯欲生活写真.md`. For other realistic or modern Eastern beauty requests, load `styles/现代东方美人.md` instead of forcing fantasy routes.
6. Decide the ambition level: refined portrait, character concept, series key visual, or mythic world poster. For vague requests, default to series key visual, not a plain beauty portrait.
7. For non-atlas image routes, choose a primary wow device from `references/wow-factor-system.md`. The prompt must have one first-glance attraction point: a giant shape, impossible moment, dramatic scale contrast, luminous artifact, dangerous action, or surreal transformation. For 东方美学图鉴 routes, do not force a fantasy wow device; use layout hierarchy, title/person priority, restrained color, and one main cultural element as the first-glance attraction.
8. For 东方美人 / 东方幻想古风 routes, apply `references/oriental-visual-discipline.md` as a hidden clean system: subject-first, clean face priority, one wow device only, controlled ornament density, premium color harmony, and visual breathing room.
9. Complete an internal director gate before writing: concept, mythic role, character subject profile, story moment, action chain, gaze target, worldbuilding hook, wow device, visual priority, color system, composition, lighting, ornament density, and negative risks.
10. Compose the prompt in layers: mythic role, character face/temperament/body language, hair/makeup, costume system, gesture, iconic prop, wonder-scale environment, supernatural phenomenon, wow device, light, lens/composition, color, texture, style, quality tags.
11. Add a negative prompt that prevents common failures: generic hanfu photoshoot, modern objects, plastic skin, extra fingers, distorted hands, bad anatomy, cheap cosplay, low-resolution artifacts, text/watermarks, visual clutter, ornament overload, excessive particles, and AI fantasy poster style.
    Always apply `references/global-negative-system.md` first, then append the route-specific negative layer.
12. Adapt wording for the target model. If the user does not specify a model, provide a universal Chinese prompt plus an English prompt suitable for Midjourney/SD-style tools.
13. Include 2-4 controlled variations when developing a series: route, role, wow device, element, color system, setting, or camera scale.

## Style Taxonomy Rule

Do not create or imply duplicate templates for the same visual direction. The current primary style families are:

- `东方幻想古风`
- `古典东方美人`
- `现代东方美人`
- `Cosplay展会摄影`
- `古风闺蜜 / AncientFemaleCompanionship`
- `甜系纯欲生活写真`
- `东方美学图鉴`

`东方美人审美系统` is an upper-level aesthetic layer, not a standalone route family. `甜系纯欲生活写真-场景素材库` is a subordinate scene library, not a standalone route family.

Before adding a new style, check `references/style-taxonomy.md`. If the request can be represented as a route, scene, mood, costume, or prompt rule inside an existing family, extend that family instead of creating a new template.

## Output Ratio System

- Default ratio: `9:16`.
- Priority: highest.
- Unless the user explicitly specifies another ratio, all outputs use `9:16`.
- If the user explicitly specifies another ratio, preserve the user's ratio.
- Exception: 东方美学图鉴 cover/content system defaults to `3:4` / `1080x1440` unless the user explicitly specifies another ratio.
- Daily automation exception to the exception: every daily image must use `9:16`, including 东方美学图鉴 routes. Convert atlas pages into 9:16 vertical atlas-poster variants instead of generating 3:4 catalog pages.

## Daily Automation Diversity And QA

When generating daily Eastern Beauty images automatically, do not reuse a small fixed set of routes. Each daily batch must contain five clearly different directions selected from the full skill universe:

- Eastern fantasy / gu feng routes.
- Classical Eastern beauty routes.
- Modern Eastern beauty and new-Chinese editorial routes.
- Cosplay convention photography routes.
- Gu Feng Girlfriends / ancient private-room companionship photography routes.
- SweetHomeGirl / realistic lifestyle routes.
- Eastern aesthetic atlas / Xiaohongshu catalog routes.
- Original exploration idea seeds that still keep the subject as Eastern beauty.

Rules:

1. No two images in the same daily batch may use the same route family, scene type, outfit logic, camera angle, or dominant prop.
2. Every default five-image daily batch must include one original exploration idea seed, not a fixed prewritten style. GPT should name the style, infer the scene, design the outfit, decide the story moment, and create the visual hook from that seed.
3. Exploration ideas may be imaginative, surreal, cinematic, futuristic, mythic, urban, or cross-genre, but they must remain tasteful, subject-first, and visually coherent.
4. Every woman in daily image prompts must be an adult young East Asian woman age `20-26`, unless the user explicitly requests another adult age range.
5. Avoid old-looking, matronly, overly severe, or age-ambiguous styling. Mature temperament means composure, not older age.
6. Every prompt must state a concrete story moment, visible hand action, gaze target, and one dominant visual hook.
7. Every object must be semantically locked: a cup remains a cup, a fan remains a fan, a lantern remains a lantern, a book remains a book, a flower bouquet remains flowers. Do not let props morph into chains, jewelry, ribbons, scenery, or random ornaments.
8. Face integrity has highest priority: no scenery, water, buildings, flowers, chains, cups, ornaments, or texture patterns may appear inside the face, eyes, mouth, or skin area.
9. Keep visual hierarchy: face and eyes first, story moment second, costume and environment third.
10. If a generated candidate has broken face, object morphing, prop fusion, body distortion, or severe semantic drift, reject it and regenerate with a simpler prompt, fewer ornaments, a clearer prop phrase, and stronger negative constraints.
11. Face clarity does not mean front-facing. A clear face may be three-quarter view, side profile, lowered gaze, over-shoulder return, mirror face, window reflection, or a face lit from the side.
12. In every default five-image daily batch, use viewpoint distribution: at most two front-facing/direct-camera images; at least one three-quarter or side-profile image; at least one lowered-gaze / looking-at-prop image; at least one over-shoulder, back-turn, mirror/reflection, or environment-interaction image.
13. Do not use `looking at camera` as the default story closure. Gaze targets may be a cup, fan, book, flower, lantern, mirror, window, water surface, companion, doorway, street direction, light source, or the action being performed.

Daily automation execution rules:

1. Generate the daily route plan from `scripts/daily_eastern_beauty_generator.py` before creating images. Do not invent the four fixed routes from memory.
2. Use the generated plan as the source of truth for style family, style name, scene, outfit, story moment, composition, visual hook, slug, prompt summary, and negative prompt.
3. The default five-image batch is one original exploration route plus four fixed-family routes chosen by the script's rotation. Do not replace this with the same familiar fantasy/classical/modern/lifestyle set unless the plan says so.
4. The daily generator script is a route-plan / Markdown-plan compiler only. It is not an image generator and is not expected to create PNG files.
5. After the route plan is ready, generate each real image with the available Codex image generation capability / `imagegen` skill. Do not search the repository for a local image-generation CLI as a required dependency.
6. Missing repo-local image-generation executors are not a failure by themselves. Missing Codex/imagegen image generation capability is a hard blocker, because the daily post requires five real images.
7. Do not treat `scripts/run_daily_eastern_beauty_prompts.sh` as the full publishing pipeline. It is a prompt/Markdown helper for old local flows, not the complete image-generation workflow.
8. For Hexo validation, compression, deploy, and blog git operations, use WSL commands in the Hexo repo, not Windows-native shell fallbacks.
9. After successful image generation and path validation, commit only the daily post and its daily image directory in the blog repo. Do not modify or commit `package.json`, `push.sh`, build scripts, or unrelated blog files.
10. Push the blog source commit after validation and deployment. A daily automation run is not complete until both deployment and blog source push succeed.
11. Daily image ratio is always `9:16`. If a route such as 东方美学图鉴 normally uses 3:4, convert it into a 9:16 daily-poster variant.
12. Do not rely on the image model to render accurate Chinese text. For atlas/title routes, keep a clean title area in the generated image and use post-processing text overlay when accurate words such as `二十四节气` or a specific solar term are required.

Daily automation shared negative prompt additions:

```text
scenery inside face, landscape on face, object fused with face, cup turning into chain,
prop morphing, object mutation, jewelry replacing prop, random chain objects,
deformed prop, melted object, broken cup, lantern becoming jewelry,
flowers fused into skin, fabric fused into hands, distorted facial features,
asymmetrical eyes, extra face details, old-looking face, matronly styling,
age drift, overly severe mature face, duplicate focal subject
```

## Defaults

Use these defaults when the user gives only a short request:

- Character: adult Chinese/Eastern fantasy heroine, age 20-26 by default, dignified, powerful, not sexualized.
- Subgenre: Eastern fantasy series key visual with one mythic role and one memorable visual hook unless the user asks for realistic, modern, fashion, or portrait photography.
- Composition: full-body or three-quarter key art, cinematic low angle or heroic medium shot, strong silhouette.
- Mood: mythic, elegant, dangerous, refined, with a story moment.
- Quality: high detail, natural skin texture, delicate fabric detail, coherent hands, no text.

## Distinctiveness Requirements

Never satisfy a short request with only "beautiful woman + hanfu + nice background." Add at least three of these:

- A mythic role: celestial cartographer, Kunlun sword guardian, Dunhuang star dancer, tide dragon envoy, lotus dream exorcist, moon palace alchemist.
- An iconic prop: jade astrolabe, bronze armillary sphere, phoenix lantern, tide pearl, cloud sword, cinnabar talisman wheel, mural ribbon, moon mirror.
- A wonder-scale environment: floating observatory, cloud sea palace, desert grotto, moonlit Kunlun bridge, underwater dragon court, lotus dream lake, ancient bronze city.
- A supernatural phenomenon: dragon-shaped nebula, talisman orbit, silk ribbons forming constellations, tide halo, phoenix fire, ink clouds, luminous murals.
- A strict color system: deep teal + antique gold, cinnabar + mineral blue, moon silver + ink black, jade green + pearl white, tide blue + coral red.
- A wow device: oversized halo object, impossible transformation, high-risk action, extreme scale contrast, unusual viewpoint, or single dominant graphic shape.

If the concept still reads like "a pretty heroine in a decorated scene," escalate it before returning.

For ornate Eastern fantasy routes, escalation must not mean adding more gold, particles, jewelry, ribbons, embroidery, murals, or random glowing elements. Escalate by improving the visual hierarchy: cleaner face area, stronger story moment, one dominant wow device, controlled color system, and better cinematic lighting.

## Director Gate

Before returning a prompt, verify:

- Explicit user inputs are preserved and visible in the final prompt.
- Exactly one primary Eastern fantasy route is driving the image.
- The heroine has a readable adult identity and role, not just beauty traits.
- The character subject profile has face temperament, body language, posture, gaze, and hand action.
- Face structure, eye/brow detail, hairstyle, expression, makeup, posture, and gaze target are concrete enough to avoid the default same-face result.
- For multi-image sets, character differences are visible: no repeated face structure, hairstyle, expression, outfit silhouette, camera angle, or prop logic unless the user explicitly asks for a fixed character.
- A single wow device is visible within the first second of looking at the image.
- The face and eyes remain the first visual priority; story moment second; costume and ornaments third.
- Ornament density is controlled: no jewelry, pibo, mural, particle, or red-gold overload.
- The image contains one clear time slice, one main event, one action chain, and one gaze target.
- Costume, prop, environment, lighting, and color belong to the same world.
- At least three distinctiveness requirements are present.
- The final result is a coherent image moment, not a field list or keyword pile.

For 东方美学图鉴, use this atlas gate instead:

- Page type is clear: Cover, Overview, or Character.
- Ratio is `3:4` unless the user explicitly overrides it.
- Cover pages include column frame, issue number, vertical title, vertical subtitle, right-side main visual, restrained paper background, and one main cultural element.
- Overview pages do not repeat the column frame, issue number, or logo; they use top title, 2x2 character group, and one summary line.
- Character pages use 85% figure and 15% information; information stays in the lower-left area; name is vertical; seal stays at the bottom.
- Visual language remains museum-catalog-like, restrained, and collectible.

## Output Format

For a single prompt request, return:

```text
参数锁定：
[explicit user inputs + labeled supplements]

导演设定：
[one short paragraph: route, role, story moment, worldbuilding hook, wow device, visual priority]

导演式模块解析：
[readable paragraphs for character, costume/prop, scene/spectacle, camera/light]

中文主提示词：
[image-ready prompt]

English prompt:
[image-ready English prompt]

负面提示词：
[negative prompt]

参数建议：
[aspect ratio, style strength, seed/CFG notes if relevant]
```

Keep the final Chinese prompt, English prompt, and negative prompt in separate Markdown `text` code blocks when they are meant to be copied directly.

For prompt packs, use a compact table with: theme, visual hook, prompt, negative prompt, best ratio.

For series development, return:

```text
Series bible:
[one paragraph: world, visual rules, recurring symbols]

Character lineup:
| Role | Visual hook | Color system | Scene | Prompt direction |

Shared negative prompt:
[negative prompt]
```

For 东方美学图鉴, return:

```text
参数锁定：
[user fields, including Type / 页面类型]

版式锁定：
[Cover / Overview / Character layout rules]

中文主提示词：
[image-ready prompt]

English prompt:
[image-ready English prompt]

负面提示词：
[atlas negative prompt]

版式检查：
[3-6 short checks]
```

## Reference Files

Read only the reference needed for the current request:

- `references/prompt-framework.md`: prompt grammar, output templates, model adaptation rules.
- `references/request-router.md`: short-request intent routing, Chinese trigger phrases, output mode selection, and rewrite handling.
- `references/style-taxonomy.md`: canonical style family map, duplicate-template prevention, current route inventory, and boundary rules.
- `references/structured-call-format.md`: lightweight Chinese parameter formats for users who should not need to read examples or style docs.
- `styles/东方美人审美系统.md`: upper-level beauty temperament system for 柔美, 妩媚, 成熟, 优雅, 高贵, 清冷, 温婉, 英气, 神性, 慵懒.
- `styles/甜系纯欲生活写真.md`: SweetHomeGirl-compatible Chinese style reference for 甜系纯欲生活写真, built around realism, feminine charm, romantic feeling, story moment, and natural pure-desire.
- `styles/甜系纯欲生活写真-场景素材库.md`: optional SweetHomeGirl micro-scene library for more specific, story-rich, less repetitive lifestyle scenes.
- `styles/现代东方美人.md`: realistic, modern, new-Chinese-style, fashion editorial, magazine, and cinematic Eastern beauty prompt direction.
- `styles/Cosplay展会摄影.md`: official convention cosplay photography system for coser / ChinaJoy / Bilibili World / Tokyo Game Show / AAA game character campaign style; use for original game-role cosplay, polished exhibition background, high-end costume design, and Vogue editorial convention photography.
- `styles/古风闺蜜.md`: AncientFemaleCompanionship / two-person ancient Chinese female companionship photography system for 闺阁、江南、山寺、节庆、古街等场景; relationship-first storytelling, realistic fabric, soft natural light, sisterhood/friendship interaction, and anti-xianxia-poster rules.
- `styles/东方美学图鉴.md`: 小红书 / 博物馆图录感 content system for 东方美学图鉴, 四大美人, 四大才女, 十二花神, 东方神女, 敦煌飞天, 朝代服饰, 东方器物, 东方神话; includes 3:4 cover layout, content page layouts, palette, typography, and visual hierarchy.
- `styles/古典东方美人.md`: non-fantasy classical Eastern beauty routes such as 洛神水镜, 宋韵茶影, 唐宫夜宴, 江南烟雨, 青瓷月影, 昆曲花影.
- `styles/东方幻想古风.md`: the primary gu feng / Eastern fantasy style route registry; choose exactly one route for each visual direction.
- `references/wow-factor-system.md`: first-glance attraction devices, anti-bland upgrades, and route-specific spectacle hooks.
- `references/oriental-visual-discipline.md`: hidden clean system for 东方美人 / 东方幻想古风, including subject-first visual hierarchy, controlled ornament density, route-specific de-noise rules, and fantasy negative prompts.
- `references/character-subject-system.md`: face, temperament, body language, posture, hand action, and route-specific heroine profiles.
- `references/gufeng-visual-library.md`: gu feng subgenres, clothing, hair, makeup, props, settings, light, color palettes.
- `references/eastern-fantasy-series.md`: mythic roles, series concepts, spectacle rules, stronger visual hooks.
- `references/quality-control.md`: checklist for avoiding generic, unsafe, or broken image prompts.
- `references/global-negative-system.md`: shared base negative system for anatomy, hands, feet, face integrity, prop semantics, multi-subject boundaries, and image quality. Apply before style-specific negatives.
- `examples/`: copyable example prompts by route. Read when the user asks for examples, style samples, prompt packs, or wants to compare routes.

## Cosplay Convention Photography Rules

When the selected route is `Cosplay展会摄影`:

1. Load `styles/Cosplay展会摄影.md`.
2. Treat the result as official convention photography: original AAA game-character cosplay, luxury fashion campaign, and real exhibition photography.
3. Keep the subject as a 20-26-year-old adult East Asian woman unless the user explicitly requests another adult subject.
4. Do not copy a specific copyrighted character. Use original role directions such as 女武神, AI操作员, 皇家护卫, 赛车皇后, 巫女, 星际驾驶员, 教师, 女警, 护士, 医生, 空姐, 职场女性, 水手, 服务员, 女仆, 精灵, 猫耳角色, or 原创幻想角色.
5. Lock one role direction, one color system, one convention scene, one costume silhouette, one action, one person count, and one framing mode.
6. Preserve the photo standard: RAW photo, 85mm portrait lens, f/1.8, shallow depth of field, Kodak Portra-like color, natural skin texture, clean low noise, subject about 70% of frame.
7. Keep the convention background softly blurred: booth logo, game poster, LED light, photographers, and audience are allowed only as supporting context.
8. Avoid cheap Lolita, plastic fabric, excessive lace, excessive organza, taobao costume, eroticized costume, wide-angle distortion, cluttered crowd, and all-subjects-looking-at-camera repetition.
9. For two or more Coser images, enforce cross-cluster diversity. Role cluster, convention subspace, costume silhouette, prop type, action story, gaze direction, and camera scale must all differ; do not satisfy a batch by only changing color on the same official booth portrait.

## Style Rules

- Prefer concrete visual decisions over vague praise. Replace "beautiful, elegant, immortal" with visible details: role, prop, costume silhouette, supernatural phenomenon, light source, posture, background depth.
- Bias toward Eastern fantasy specificity when the user says the result is generic, "too ordinary", "no highlight", "not special", "not eye-catching", "plain", "boring", or asks for a series.
- When the user criticizes output as bland, update or rewrite around the story moment and one wow device first, then refine face, light, and costume. Do not solve blandness by adding uncontrolled ornaments.
- Keep the character adult unless the user explicitly requests a non-person adult-safe alternative. Avoid eroticized framing, transparent clothing, voyeuristic angles, or age-ambiguous sexualization.
- Do not claim historical accuracy unless the prompt is intentionally researched. Say "Tang-inspired" or "Song-inspired" when using stylized cues.
- For Chinese prompts, use fluent art-direction language; for English prompts, use model-friendly nouns and adjectives.
- Preserve user constraints, especially platform, ratio, style, and whether the output is for a mini-program prompt generator.
- Treat a bare parameter block as a prompt-writing task. If it contains `生成: 是`, `生图`, or `直接生成`, assemble the prompt and invoke image generation.
- If a user request contains sensitive wording, perform an intent-preserving safety rewrite: keep the user's scene, temperament, costume direction, action relationship, and composition; change only risky wording such as exposure, voyeuristic camera, transparent fabric, or direct bath/body phrasing. Label the rewrite when returning a prompt.
- Do not over-fantasize realistic Eastern beauty requests. For 写实, 现代, 摄影, 杂志, 新中式, or 东方高级感, prioritize face, styling, fabric, posture, lighting, lens, background, and taste; use mythic routes only if the user asks for fantasy.
- Treat beauty temperament as a first-class art direction. When the user asks for 柔美, 妩媚, 成熟, 优雅, 高贵, 清冷, 温婉, 英气, 神性, or 慵懒, load `styles/东方美人审美系统.md` and let that temperament shape gaze, posture, hand gesture, fabric, light, and composition.
- For 东方美学图鉴, separate cover rules from content page rules. Cover pages must include the fixed column identity, issue number, vertical title system, right-side main visual, paper texture, restrained palette, and 3:4 ratio. Content pages must not repeat the cover column frame, Vol number, logo, or issue block.
