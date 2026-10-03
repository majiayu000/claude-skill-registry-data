---
name: crun-action-camera-enhancer
description: Enhance character action prompts, dynamic poses, camera movement trajectories, and visual effects for Crun AI image and video generation models. Supports Text-to-Image, Image-to-Image (reference character action transform), Text-to-Video, and Image-to-Video (animating reference character images into dynamic action clips). Use whenever the user asks for character actions, combat scenes, jumping, martial arts, magic casting, acrobatics, dynamic pose pictures/videos, camera motion, animating an uploaded character, or performing action transforms on reference images.
---

# Crun Character Action & Camera Director

Use this skill to transform high-level user action requests into highly dynamic, cinematographically rich image and video generation prompts.

This skill operates as an **Upstream Director & Prompt Enhancer**. It decomposes user inputs (text prompts or uploaded reference character images) into camera movement trajectories, pose dynamics, secondary motion physics, and visual effects (VFX), then passes the optimized payload to Crun base skills (`crun-model-router`, `crun-account-credits`, and `crun-task-runner`) for final rendering.

---

## Execution Workflow

```text
[ User Input ] (Text Request or Reference Character Image)
    │
    ├── 1. Upload Source Media (If reference photo/image provided)
    │       └─ python <runtime>/crun_cli.py upload <local-file>
    │
    ├── 2. Action & Camera Breakdown
    │       ├─ Camera Trajectory (Low angle, Dutch tilt, Push-in tracking, Foreshortening)
    │       ├─ Pose Dynamics (Keyframe phase, muscle tension, center of gravity)
    │       └─ Physics & VFX (Billowing dress/hair, energy orb, shockwaves, debris)
    │
    ├── 3. Route Model & Construct Payload
    │       ├─ Text-to-Image / Image-to-Image (image-edit with uploaded file_url)
    │       └─ Text-to-Video / Image-to-Video (image-to-video with uploaded file_url)
    │
    ├── 4. Estimate & Button Confirmation Gate
    │       ├─ Estimate Credits (crun-account-credits)
    │       └─ Present Breakdown Details & Interactive Options (ask_question tool)
    │
    └── 5. Task Creation & Result Delivery (crun-task-runner)
            ├─ python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
            ├─ python <runtime>/crun_cli.py task wait --task-id <task_id>
            └─ Local Media Result & Preview Delivery
```

---

## Detailed Execution Steps

### Step 1: Upload Reference Media (If Provided)

When the user provides a local character photo, sketch, or reference image (for Image-to-Image or Image-to-Video action generation):

```bash
python <runtime>/crun_cli.py upload <local-file>
```

Use the returned `file_url` in the model payload. Never send raw local paths, Base64 strings, or data URIs to Crun model inputs.

---

### Step 2: Action & Camera Breakdown Matrix

Decompose the requested action scene across three key visual dimensions:

#### 1. Camera Motion & Framing
- **Camera Trajectory**:
  - *Tracking / Push-In*: Rapid push towards the point of impact to heighten dramatic tension.
  - *Low Angle / Worm's-Eye View*: Emphasize character height, power, or vertical leap.
  - *Dutch Angle (Tilt)*: Introduce instability, extreme speed, or kinetic energy.
  - *Orbit / Arc Pan*: Smooth circular sweep around the character during spell charging or stance transitions.
- **Framing**:
  - *Extreme Foreshortening*: Elements closest to the camera (e.g., outstretched palm, sword point) appear dramatically enlarged.

#### 2. Pose Dynamics & Anatomy Mechanics
- **Keyframe Progression**:
  - *Anticipation*: Coiled posture, bent knees, arms pulled back, muscle tension.
  - *Impact*: Maximum extension, rigid core, wide stance, foreshortened limbs thrusting forward.
  - *Follow-Through*: Slanted body angle, floating inertia, extended movement lines.
- **Weight & Gravity**: Center of gravity shifting, ground fractures or dust clouds from footing impact.

#### 3. Physics & Visual Effects (VFX) Injection
- **Secondary Motion Physics**:
  - Hair strands floating or swirling violently in wind backdrafts or air shockwaves.
  - Flowing fabric (skirt hem, cape, sash, jacket tails) billowing opposite to the movement direction.
- **VFX & Particle Dynamics**:
  - Energy & Magic: Glowing orbs, electric arcs, glowing rune circles, light beams.
  - Environmental Impact: Shattering glass, floating rocks/debris, radial shockwave rings, speed lines, dust plumes.

---

### Step 3: Route Model & Construct Enhanced Payload

#### 1. Operation Selection & Model Routing (`crun-model-router`)
Read `skills/crun-model-router/SKILL.md` to select modality, operation, and candidate models:

- **Text-to-Image** (`modality: "image"`, `operation: "text-to-image"`):
  - Used when generating a new action picture from pure text.
  - Preferred models: `openai/gpt-image-2`, `bytedance/seedream-5-pro`, `google/nano-banana-pro`.

- **Image-to-Image / Image Edit** (`modality: "image"`, `operation: "image-edit"`):
  - Used when modifying or creating an action scene based on an uploaded reference character image.
  - Preferred models: `bytedance/seedream-5-pro`, `openai/gpt-image-2`, `google/nano-banana-pro`.
  - Include uploaded `file_url` in model `img_url` / `image_url` field.

- **Text-to-Video** (`modality: "video"`, `operation: "text-to-video"`):
  - Used when generating a new action video clip from pure text.
  - Preferred models: `bytedance/seedance2-0-fast-t2v`, `vidu/q3-turbo-t2v`, `kling/v3-turbo`.

- **Image-to-Video / Character Animation** (`modality: "video"`, `operation: "image-to-video"`):
  - Used when animating an uploaded reference character image into a dynamic action video.
  - Preferred models: `bytedance/seedance2-0-fast-i2v`, `bytedance/seedance2-0-i2v`, `kling/v3-i2v`, `vidu/q3-turbo-i2v`.
  - Include uploaded `file_url` as the input image field (e.g., `image_url` or `img_url`).

#### 2. Universal Prompt Construction Formula
Translate visual descriptions into detailed English prompts for optimal Crun model rendering quality:

```text
[Character & Costume] + [Keyframe Pose & Foreshortening] + [Camera Trajectory & Framing] + [Secondary Clothing & Hair Physics] + [VFX & Energy Particles] + [Lighting & Environment] + [Cinematic Quality Keywords]
```

---

### Step 4: Estimate Affordability & Interactive Confirmation Gate

Read `skills/crun-account-credits/SKILL.md`:

```bash
python <runtime>/crun_cli.py task estimate --model <model> --input-file <input.json>
```

Verify `affordable: true`. Before task creation, **always present an interactive confirmation modal** using the `ask_question` tool so the user can review the breakdown.

#### Mandatory Confirmation Content Specification:
- **Scene Type & Target Output**: Text-to-Image / Image-to-Image / Text-to-Video / Image-to-Video
- **🖼️ Reference Image**: Uploaded Crun file URL (if provided)
- **🎬 Camera Motion**: Shot angle and trajectory (e.g., Low-angle Dutch tilt tracking push-in)
- **🤸 Pose Dynamics**: Keyframe posture (e.g., Foreshortened palm thrust, crouched impact stance)
- **✨ Physics & VFX**: Dynamic physics & particle effects (e.g., Billowing skirt, cyan energy orb, electric arcs)
- **🤖 Target Model & Estimated Credits**: e.g., `bytedance/seedance2-0-fast-i2v` (4.0 Credits)

#### Interactive Button Options:
Use interactive single-select buttons for confirmation:
- Options: `["Confirm & Generate", "Modify Camera/VFX", "Cancel"]`

---

### Step 5: Create Task & Monitor Execution

Read `skills/crun-task-runner/SKILL.md`:

```bash
python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
python <runtime>/crun_cli.py task wait --task-id <task_id> --timeout-seconds 300
```

---

### Step 6: Result Delivery & Preview

Deliver a localized status response featuring the normalized task ID, credit usage, local file path, and an inline media preview:

```text
✅ Action & Camera Generation Complete!
- Task ID: <task_id>
- Operation: <operation_type>
- Camera Trajectory: <camera_motion>
- Keyframe Pose: <pose_dynamics>
- Visual Effects: <vfx_details>
- Credits Used: <credits>

![Result Preview](/absolute/path/to/result.png_or_mp4)
```

---

## Canonical User Scenarios & Prompt Breakdown Reference

### Scenario 1: Anime Girl Energy Blast Video (Text-to-Video)

- **Input Intent**: Anime girl casting an energy blast (text-to-video).
- **Director Breakdown**:
  - **Camera Motion**: Low-angle push-in tracking shot with a slight Dutch angle tilt.
  - **Pose Dynamics**: Crouched charging stance transitioning into an aggressive forward palm thrust, extreme hand foreshortening.
  - **Physics**: Twin-tail hair and pleated skirt violently blowing backward from energy backdraft.
  - **VFX**: Glowing cyan and purple energy orb between palms, crackling electric arcs, floating ground debris, radial air shockwaves.
- **Constructed Payload**:
  ```json
  {
    "prompt": "High-speed dynamic anime action video, a beautiful anime girl casting a powerful energy beam blast, low-angle tracking shot pushing forward quickly, extreme foreshortening on her outstretched palms, glowing cyan energy orb forming between her hands with crackling purple electric arcs, her long twin-tail hair and pleated skirt violently fluttering backward from the shockwave, floating ground debris and air distortion rings, dramatic cinematic lighting, intense anime combat scene, 4k resolution.",
    "duration": 5,
    "aspect_ratio": "16:9"
  }
  ```

---

### Scenario 2: Hooded Assassin Roof Leap Image (Text-to-Image)

- **Input Intent**: Hooded assassin jumping from a roof (text-to-image).
- **Director Breakdown**:
  - **Camera Motion**: Worm's-eye view looking straight up from the ground, wide-angle framing.
  - **Pose Dynamics**: Mid-air downward plunge keyframe, knees bent, dual daggers held in reverse grip, strong diagonal perspective axis.
  - **Physics**: Hooded cloak, scarf, and leather straps billowing dramatically upward against gravity.
  - **VFX**: Shattered roof tiles floating in air, moonlight rim light tracing body contours, silver blade glints, night mist.
- **Constructed Payload**:
  ```json
  {
    "prompt": "Dynamic cinematic action photography, a hooded assassin diving off an ancient rooftop downward toward the viewer, extreme low-angle worm's-eye view looking straight up into the night sky, mid-air leap pose with knees bent and dual daggers held in reverse grip, long black cloak and scarf billowing dramatically upward in the wind, shattered roof tiles suspended in mid-air, full moonlight rim light casting sharp highlights on leather armor and metallic blades, dramatic shadows, 8k hyper-detailed.",
    "aspect_ratio": "9:16"
  }
  ```

---

### Scenario 3: Animate Character Photo into Action Video (Image-to-Video / I2V)

- **Input Intent**: User uploads `character_portrait.png` and asks: "Animate this character doing a martial arts sword slash".
- **Execution Flow**:
  1. Upload image: `python <runtime>/crun_cli.py upload character_portrait.png` -> Returns `https://files.crun.ai/resources/abc123.png`
  2. Route model: `bytedance/seedance2-0-fast-i2v` (`operation: "image-to-video"`)
  3. Director Breakdown:
     - **Camera Motion**: Orbital tracking pan around the character during the slash.
     - **Pose Dynamics**: Full rotation body turn, extended arm holding sword, low center of gravity.
     - **Physics**: Clothing sleeves and hair whipping around in a circular arc.
     - **VFX**: Glowing sword aura wave, spark particles, motion blur trail.
- **Constructed Payload**:
  ```json
  {
    "image_url": "https://files.crun.ai/resources/abc123.png",
    "prompt": "High-speed action video animating the character in the reference image, performing a dynamic martial arts sword slash, orbital camera tracking shot panning around the character, sleeve and hair whipping violently in wind momentum, glowing silver sword arc light trail, spark particles, cinematic motion blur, 5 seconds.",
    "duration": 5,
    "aspect_ratio": "16:9"
  }
  ```

---

### Scenario 4: Character Action Transform (Image-to-Image / I2I)

- **Input Intent**: User uploads `hero_sketch.jpg` and asks: "Draw this character plunging from a roof with fire aura".
- **Execution Flow**:
  1. Upload image: `python <runtime>/crun_cli.py upload hero_sketch.jpg` -> Returns `https://files.crun.ai/resources/xyz789.jpg`
  2. Route model: `bytedance/seedream-5-pro` (`operation: "image-edit"`)
  3. Director Breakdown:
     - **Camera Motion**: Low angle looking upward at the falling hero.
     - **Pose Dynamics**: Mid-air plunge pose with fist aimed downward.
     - **Physics**: Jacket billowing upward from wind resistance.
     - **VFX**: Flaming aura around fist, fiery ember sparks, air shockwave rings.
- **Constructed Payload**:
  ```json
  {
    "img_urls": ["https://files.crun.ai/resources/xyz789.jpg"],
    "prompt": "Dynamic action concept art based on the character in reference image, plunging downward from a high building, low-angle view looking upward, fist extended downward with dramatic foreshortening, jacket fluttering upward in the air draft, roaring fire aura engulfing fists with floating embers, radial air shockwaves, dramatic lighting, 8k resolution.",
    "aspect_ratio": "9:16"
  }
  ```
