---
name: comfyui-anime
description: "Generate high-quality anime, manga, and Danbooru-style illustrations using the local ComfyUI instance and Illustrious SDXL (waiIllustriousSDXL_v170)."
version: 1.1.0
author: kuroko
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags:
      - anime
      - comfyui
      - danbooru
      - illustrious-xl
      - sdxl
      - illust
      - image-generation
    category: creative
---

# Illustrious-XL & Wai-Illustrious Prompting Guide & Skill

Use this skill whenever the user asks to draw, generate, or create anime artwork, manga characters, illustrations, or portraits (including drawing Kobeni herself).

## Backend Setup & Models
* **Engine**: Local ComfyUI on `http://127.0.0.1:8188`
* **Models Available in `generate_anime_image`**:
  * `anima` (Default): Optimized workflow, cinematic warm lighting, rich gradient shading, and expressive dynamic poses.
  * `wai_illustriousxl`: `waiIllustriousSDXL_v170.safetensors`, crisp 2D digital anime line art, strong tag fidelity.
* **Default Sampler**: Euler Ancestral / Karras, 25-28 steps, CFG 5.5 - 6.5
* **Clip Skip**: 2

---

## 🎨 Illustrious-XL & Anima Prompting Standards

Illustrious XL and Anima are heavily optimized on Danbooru-style datasets. Follow this tag order for best quality and composition:

### 1. Structure Order (Golden Order):
1. **Core Subject & Count**: `1girl, solo` / `1boy, solo` / `2girls`
2. **Character & Series Name**: `kobeni higashiyama, chainsaw man` / `zhu yuan (zenless zone zero), zenless zone zero` / `d.va (overwatch), overwatch`
3. **Artist & Style Tags**: `@ratatatat74`, `aleeria_v`, or artist combos for style mixing (preserve `@` when required by tag syntax).
4. **Quality & Aesthetic Boosters**: `masterpiece, best quality, very aesthetic, absurdres, newest`
5. **Facial Features & Hair**: `short black hair, two hair clips, brown eyes, mole under eye`
6. **Clothing & Accessories**: `bodysuit, plugsuit, meka suit` / `maid outfit, white apron`
7. **Pose, Camera & Expression**: `shy, blushing, looking at viewer, dutch angle, holding game controller, selfie pose, front view across desk`
8. **Environment & Lighting**: `cozy bedroom, glowing monitors, neon rgb lighting, night, cinematic lighting, depth of field`

### 2. Standard Negative Prompt for Illustrious-XL:
```
lowres, worst quality, low quality, bad anatomy, bad hands, missing fingers, extra digits, signature, watermark, username, blurry, jpeg artifacts, artist name, mutated, disfigured, text, ugly, bad proportions, bad eyes, poorly drawn hands
```

### 3. Prompting Rules & DO NOTs:
* ✅ **DO**: Use comma-separated Danbooru tags.
* ✅ **DO**: Use SDXL weighting if needed: `(maid outfit:1.1)`, `(blushing:1.15)`.
* ❌ **DO NOT USE PONY TAGS**: Never use `score_9, score_8_up, score_7_up, source_anime`. Illustrious XL does NOT use Pony scores; using them degrades output quality.
* ❌ **DO NOT USE LOCALHOST URLS**: Always use local file paths and `MEDIA:<path>`.

---

## 📐 Optimal Resolutions (SDXL Standard)

| Format | Resolution | Best Use Case |
| :--- | :--- | :--- |
| **Portrait (Default)** | `832 x 1216` | Character solo portrait, maid outfit, full/half body |
| **Landscape** | `1216 x 832` | Scenery, multiple characters, cinematic wide shots |
| **Square** | `1024 x 1024` | Icons, profile pictures, close-up portraits |

---

## ⚡ How to Execute

### Via Native Tool:
Call the tool `generate_anime_image(prompt="...", aspect_ratio="portrait")`.

### Via Python Script:
```bash
python3 /home/kuroko/.hermes/skills/comfyui-anime/scripts/generate_anime.py "<danbooru_tags>" --aspect_ratio portrait
```

### Example: Drawing Kobeni Maid (Optimized Illustrious XL Prompt):
```bash
python3 /home/kuroko/.hermes/skills/comfyui-anime/scripts/generate_anime.py "1girl, solo, kobeni higashiyama, chainsaw man, masterpiece, best quality, very aesthetic, absurdres, newest, short black hair, two hair clips, brown eyes, mole under eye, maid outfit, black maid dress, white apron, frilled headband, shy, blushing, looking at viewer, indoor, cafe interior, soft lighting" --width 832 --height 1216
```

---

## 🔬 Related Local Labs & References
* **Computational Biology Mini-Lab**: See [references/computational_biology_mini_lab.md](references/computational_biology_mini_lab.md) for Boltz-1/Boltz-2 complex prediction, RDKit/Biopython pipelines, and the local 3Dmol viewer service on port `9188`.
