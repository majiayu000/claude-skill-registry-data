---
name: design-interview
description: Deep Socratic interview for interior design projects — gathers crystal-clear design requirements with ambiguity scoring before executing the design workflow. Use when starting a new design project, when requirements are vague, or when the user says "interview", "hỏi kỹ", "tư vấn chi tiết", "phỏng vấn thiết kế".
---

# Design Interview — Socratic Requirements Gathering for Interior Design

Adapts the deep-interview methodology (Socratic questioning + mathematical ambiguity gating) specifically for interior design projects. Instead of generic software dimensions, scores clarity across **6 design-specific dimensions**. Instead of bridging to code execution, bridges to the pandaConcept design workflow (`/design-consult` → `/mood-board` → `/generate-prompt` → `/render`).

## Why This Exists

Jumping straight to `/generate-prompt` or `/render` with vague requirements ("làm phòng khách đẹp") produces wasted renders and prompt iterations. This skill ensures crystal-clear design intent BEFORE spending API credits on rendering.

## Use When

- User has a vague design idea ("tôi muốn thiết kế phòng ngủ", "redesign my living room")
- User says "interview", "hỏi kỹ", "tư vấn chi tiết", "phỏng vấn thiết kế", "don't assume"
- Starting a new project and `brief.md` is empty
- Requirements span multiple rooms or styles
- Client feedback history in `notes.md` shows repeated mismatches

## Do Not Use When

- User already has a detailed brief with style, colors, materials specified → use `/design-consult` or `/generate-prompt` directly
- User has a reference image and wants edits → use `/edit-design`
- User just wants to look up a style → use `/style-guide`
- User says "just render it" → respect their intent

## Execution Policy

- Ask **ONE question** at a time — never batch multiple questions
- Target the **WEAKEST clarity dimension** with each question
- Reference `/style-guide` internally when asking style-related questions — offer specific style options, not open-ended "what style?"
- Score ambiguity after every answer — display transparently
- Do not proceed to design workflow until ambiguity ≤ threshold (default 0.2)
- Persist interview state for resume across sessions

---

## Phase 1: Initialize

1. **Parse the user's idea** from `$ARGUMENTS`
2. **Detect project context** — run these checks to know what exists:

```
!ls projects/${PROJECT_NAME}/brief.md 2>/dev/null && echo "HAS_BRIEF=true" || echo "HAS_BRIEF=false"
```

```
!ls projects/${PROJECT_NAME}/rooms.md 2>/dev/null && echo "HAS_ROOMS=true" || echo "HAS_ROOMS=false"
```

```
!ls projects/${PROJECT_NAME}/style-config.yaml 2>/dev/null && echo "HAS_STYLE_CONFIG=true" || echo "HAS_STYLE_CONFIG=false"
```

```
!ls projects/${PROJECT_NAME}/notes.md 2>/dev/null && echo "HAS_NOTES=true" || echo "HAS_NOTES=false"
```

```
!ls projects/${PROJECT_NAME}/references/*.{jpg,jpeg,png,webp} 2>/dev/null && echo "HAS_REFERENCE=true" || echo "HAS_REFERENCE=false"
```

```
!ls projects/${PROJECT_NAME}/references/preprocessed/semantic_analysis.json 2>/dev/null && echo "HAS_SEMANTIC=true" || echo "HAS_SEMANTIC=false"
```

### Project Detection Logic

```
No PROJECT_NAME specified?
└── Ask which project, or create new one from .template/

HAS_BRIEF=true AND brief has content?
└── EXISTING PROJECT — read all files, pre-fill known dimensions, skip clear questions.

HAS_SEMANTIC=true?
└── Read semantic_analysis.json — pre-score Space, Style, Material dimensions from Gemini data.
    This can jump ambiguity from 100% to ~40% instantly.

HAS_REFERENCE=true AND HAS_SEMANTIC=false?
└── Suggest running /preprocess-room first — Gemini Vision analysis dramatically reduces interview rounds.
```

3. **Read existing project files** (based on check results):
   - `brief.md` (if exists) — pre-fill known answers, skip already-clear dimensions
   - `rooms.md` (if exists) — know which rooms are defined
   - `style-config.yaml` (if exists) — know if style/colors/materials are already set
   - `notes.md` (if exists) — know previous feedback to avoid repeating mistakes
   - `semantic_analysis.json` (if exists) — pre-fill Space, Style, Material dimensions from Gemini data
5. **Initialize state** via `state_write(mode="design-interview")`:

```json
{
  "active": true,
  "current_phase": "design-interview",
  "state": {
    "interview_id": "<uuid>",
    "project_name": "<name or null>",
    "initial_idea": "<user input>",
    "has_existing_brief": false,
    "rounds": [],
    "current_ambiguity": 1.0,
    "threshold": 0.2,
    "dimension_scores": {
      "space": 0.0,
      "style": 0.0,
      "material_color": 0.0,
      "function": 0.0,
      "mood_lighting": 0.0,
      "provider": 0.0
    },
    "design_entities": [],
    "challenge_modes_used": [],
    "pre_filled_from_brief": []
  }
}
```

6. **Announce the interview**:

> Bắt đầu phỏng vấn thiết kế. Tôi sẽ hỏi từng câu để hiểu rõ ý tưởng trước khi tạo prompt hay render. Sau mỗi câu trả lời, bạn sẽ thấy điểm clarity. Chúng ta sẽ bắt đầu workflow khi ambiguity giảm xuống dưới 20%.
>
> **Ý tưởng:** "{initial_idea}"
> **Project:** {project_name or "chưa có — sẽ tạo mới"}
> **Ambiguity:** 100%

**Pre-fill optimization:** If existing project files already answer some dimensions (e.g., `style-config.yaml` has `primary_style: "japandi"`), pre-score those dimensions and skip questions about them. Announce what was pre-filled:

> Đã đọc từ project files: style = Japandi, colors = earth tones. Sẽ tập trung hỏi những phần chưa rõ.

---

## Phase 2: Interview Loop

Repeat until `ambiguity ≤ threshold` OR user exits early.

### 6 Design Clarity Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| **Space Clarity** | 20% | Room type, dimensions, layout, architectural features (windows, ceiling, columns) |
| **Style Clarity** | 25% | Design style, era, fusion preferences, style-specific vocabulary |
| **Material & Color Clarity** | 20% | Color palette (primary/secondary/accent), materials, textures, finishes |
| **Functional Clarity** | 15% | Purpose, occupants, lifestyle, budget range, furniture to keep/add |
| **Mood & Lighting Clarity** | 10% | Atmosphere, lighting (natural/artificial), time of day, sensory experience |
| **Provider & Output Clarity** | 10% | Which AI providers, quality expectations, camera angles, render count |

### Ambiguity Formula

```
ambiguity = 1 - (space × 0.20 + style × 0.25 + material_color × 0.20 + function × 0.15 + mood_lighting × 0.10 + provider × 0.10)
```

### Step 2a: Generate Next Question

Target the dimension with the **LOWEST clarity score**. Question styles per dimension:

| Dimension | Question Style | Example |
|-----------|---------------|---------|
| Space | "Mô tả không gian..." | "Phòng khách khoảng bao nhiêu m²? Có cửa sổ lớn không? Trần cao hay thấp?" |
| Style | "Về phong cách..." (offer specific options from `/style-guide`) | "Bạn thích sự ấm cúng của Scandinavian, sự tinh tế của Japandi, hay vẻ sang trọng của Art Deco? Tôi có thể show đặc điểm từng style." |
| Material & Color | "Về chất liệu và màu sắc..." | "Bạn muốn tông màu ấm (gỗ, be, terracotta) hay lạnh (xám, trắng, xanh)? Có chất liệu nào bạn đặc biệt thích hoặc muốn tránh?" |
| Function | "Về công năng..." | "Ai sống trong nhà? Có trẻ nhỏ, thú cưng không? Cần khu vực làm việc trong phòng không?" |
| Mood & Lighting | "Về không khí..." | "Bạn muốn cảm giác gì khi bước vào phòng? Ấm cúng như quán café, thoáng đãng như resort, hay tối giản yên tĩnh?" |
| Provider | "Về output..." | "Bạn muốn render với provider nào? Cần bao nhiêu góc chụp? Budget cho API calls?" |

**Important:** When asking about style, always reference `/style-guide` internally and present specific options with brief descriptions — never ask open-ended "bạn muốn style gì?"

### Step 2b: Ask the Question

Use `AskUserQuestion`:

```
Round {n} | Focusing: {weakest_dimension_vi} | Ambiguity: {score}%

{question}
```

Provide contextually relevant clickable options + free-text.

### Step 2c: Score Ambiguity

After each answer, score all 6 dimensions (0.0-1.0):

**Scoring criteria per dimension:**

1. **Space Clarity** (0.0-1.0): Can you describe the room precisely? Do you know type, approximate size, key architectural features?
2. **Style Clarity** (0.0-1.0): Can you name the style and its key characteristics without ambiguity? Can you pull the right keywords from `/style-guide`?
3. **Material & Color Clarity** (0.0-1.0): Can you specify a 3-color palette with hex codes? Are key materials identified?
4. **Functional Clarity** (0.0-1.0): Do you know who uses the space, what furniture is needed, and budget constraints?
5. **Mood & Lighting Clarity** (0.0-1.0): Can you describe the atmosphere, lighting type, and time-of-day feel?
6. **Provider & Output Clarity** (0.0-1.0): Do you know which providers to use, how many renders, what quality level?

### Step 2d: Design Entity Tracking

Track design entities across rounds (analogous to ontology in deep-interview):

**Entity types for interior design:**
- `furniture`: sofa, dining table, bookshelf, bed...
- `material`: marble, oak wood, linen, brass...
- `color`: specific colors with hex codes
- `style-element`: specific style keywords (e.g., "tatami", "shiplap", "arches")
- `spatial-feature`: window, column, ceiling beam, alcove...

Track stability across rounds — converging entities = the design vision is solidifying.

### Step 2e: Report Progress

```
Round {n} complete.

| Dimension | Score | Weight | Weighted | Gap |
|-----------|-------|--------|----------|-----|
| Space | {s} | 20% | {w} | {gap or "Clear"} |
| Style | {s} | 25% | {w} | {gap or "Clear"} |
| Material & Color | {s} | 20% | {w} | {gap or "Clear"} |
| Function | {s} | 15% | {w} | {gap or "Clear"} |
| Mood & Lighting | {s} | 10% | {w} | {gap or "Clear"} |
| Provider & Output | {s} | 10% | {w} | {gap or "Clear"} |
| **Ambiguity** | | | **{score}%** | |

**Design palette:** {entity_count} elements | Stability: {ratio}%

{score <= threshold ? "Clarity đạt! Sẵn sàng bắt đầu design workflow." : "Câu tiếp sẽ hỏi về: {weakest_vi}"}
```

### Step 2f: Soft Limits

- **Round 3+**: Allow early exit with warning
- **Round 8**: Soft warning: "Đã 8 round. Ambiguity: {score}%. Tiếp tục hay bắt đầu?"
- **Round 15**: Hard cap (design interviews are naturally shorter than software ones)

---

## Phase 3: Design Challenge Agents

### Round 4+: Style Challenger
> Bạn nói thích {style}, nhưng mô tả của bạn nghe giống {alternative_style} hơn. Hãy xem sự khác biệt: {style} có {characteristics_A}, còn {alternative} có {characteristics_B}. Bạn nghiêng về bên nào?

Uses `/style-guide` data to challenge — not random, but evidence-based from the style catalog.

### Round 6+: Budget Simplifier
> Nếu giảm budget một nửa, phần nào bạn sẽ giữ nguyên và phần nào sẵn sàng thay đổi? Điều này giúp tôi hiểu đâu là yếu tố quan trọng nhất.

### Round 8+: Essence Finder (if ambiguity > 0.3)
> Chúng ta đã nói về nhiều chi tiết. Nhưng nếu chỉ chọn MỘT từ để mô tả căn phòng lý tưởng, từ đó là gì? (ấm cúng? sang trọng? tự nhiên? thoáng đãng?)

---

## Phase 4: Crystallize — Write to Project Files

When ambiguity ≤ threshold:

### Step 4a: Create/Update Project

If no project exists, create from template:
```bash
cp -r projects/.template/ projects/<project-name>/
```

### Step 4b: Write `brief.md`

Fill the brief template with interview findings:
- Client info, project overview
- Style direction, color preferences, material preferences
- Target audience, lifestyle notes
- Constraints (must keep, must avoid)
- Reference images (if provided during interview)

### Step 4c: Write `rooms.md`

For each room discussed:
- Room type, dimensions, style override
- Key furniture, lighting preferences
- Camera angles for rendering
- Priority level

### Step 4d: Write `style-config.yaml`

Fill with concrete values:
- `primary_style`, `secondary_style`
- `color_palette` with hex codes
- `materials` list
- `lighting` mood and time of day
- `photography` settings
- `providers` preferences

### Step 4e: Write Interview Spec

Save full interview record to `.omc/specs/design-interview-{slug}.md`:

```markdown
# Design Interview Spec: {project_name}

## Metadata
- Interview ID: {uuid}
- Rounds: {count}
- Final Ambiguity: {score}%
- Generated: {timestamp}

## Clarity Breakdown
| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| Space | {s} | 20% | {w} |
| Style | {s} | 25% | {w} |
| Material & Color | {s} | 20% | {w} |
| Function | {s} | 15% | {w} |
| Mood & Lighting | {s} | 10% | {w} |
| Provider & Output | {s} | 10% | {w} |
| **Ambiguity** | | | **{score}%** |

## Design Vision
{crystal-clear summary of the design intent}

## Design Palette (Entities)
| Element | Type | Details | Source Round |
|---------|------|---------|-------------|
| {name} | {type} | {description} | Round {n} |

## Assumptions Exposed
| Assumption | Challenge | Resolution |
|------------|-----------|------------|
| {assumption} | {how challenged} | {what decided} |

## Interview Transcript
<details>
<summary>Full Q&A ({n} rounds)</summary>
...
</details>
```

---

## Phase 5: Design Execution Bridge

Present execution options via `AskUserQuestion`:

> Spec hoàn tất (ambiguity: {score}%). Project files đã được cập nhật. Bạn muốn tiếp tục thế nào?

### Option 1: Full Design Flow (Recommended)
**`/design-consult` → `/mood-board` → `/generate-prompt` → `/render`**

Action: Invoke `/design-consult` with the project name. The brief, rooms, and style-config are already filled — design-consult will use them to produce a comprehensive design brief, then chain to mood-board and prompt generation.

Best for: First-time renders, complex multi-room projects.

### Option 2: Direct to Prompts (Skip consult + mood board)
**`/generate-prompt` → `/render`**

Action: Invoke `/generate-prompt` with style + room + provider from the interview spec.

Best for: When interview already covered everything in detail, single-room projects.

### Option 3: Mood Board First
**`/mood-board` → `/generate-prompt` → `/render`**

Action: Invoke `/mood-board` with style + room from interview.

Best for: When client wants to "feel" the space before committing to renders.

### Option 4: Edit Existing Design
**`/edit-design` → `/render`**

Action: Invoke `/edit-design` with reference images from `projects/<name>/references/`.

Best for: When interview was about modifying an existing design (reference images provided).

### Option 5: Continue Interviewing
Go back to Phase 2 for more clarity.

### Option 6: Just Save (No Render)
Save the project files only. User will return later to render.

**IMPORTANT:** On execution selection, invoke the chosen skill via `Skill()`. The design-interview is a requirements agent, not a rendering agent.

---

## Session Relevant Skills

- `/design-consult` — the natural next step after interview. Takes the filled `brief.md` and produces a comprehensive design brief.
- `/mood-board` — when the client wants atmospheric visualization before rendering.
- `/generate-prompt` — skip straight to prompts when all details are crystal clear.
- `/render` — final execution step, sends prompts to AI providers.
- `/style-guide` — referenced internally during style questions. Essential for offering informed style options.
- `/edit-design` — if the interview reveals this is an edit (reference image + changes), redirect here.
- `/refine` — after first renders, if results need iteration.
- `/compare-models` — after multi-provider renders, compare outputs.

## Gotchas

- **Don't ask what the code already shows**: If `style-config.yaml` already has `primary_style: "japandi"`, don't ask about style. Pre-fill and move on.
- **Style questions must be specific**: Never ask "bạn muốn style gì?" — always offer 2-3 options with descriptions from `/style-guide`.
- **Budget affects everything**: A "luxury" interview produces very different materials than "budget". Clarify early.
- **Multi-room projects need per-room clarity**: Don't assume all rooms share the same style. Ask about each room's overrides.
- **Provider question can be deferred**: If the user doesn't care about providers, default to the project's preferred providers or suggest 2-3 based on the style (e.g., Stability for textured styles, DALL-E for clean modern).
- **Climate/location matters**: Tropical location = no wool rugs, no heavy curtains. Ask if not obvious.
- **Camera angle is a design decision**: Wide-angle for spacious feel, eye-level for realistic. Include in interview if the user cares about composition.
