---
name: personal-athlete-81-grid
description: Create a personal athlete 81-cell MandalArt grid from an Ohtani Shohei-style 64+8+1 model. Use when the user asks for 大谷翔平 81 宮格, 個人運動員81宮格, sports skill maps, athlete training Mandala charts, badminton 81 grids, or editable JSON/SVG/PNG-ready athlete development templates with Ohtani-style colors.
---

# Personal Athlete 81 Grid

## Purpose

Turn an athlete's core goal into a square 9x9 MandalArt grid:

- `1` center goal: the athlete's north star.
- `8` domains: the center 3x3 ring around the goal.
- `64` extension cells: each domain expands into eight concrete actions.

Default visual style is the Ohtani Shohei reference: thick black 3x3 section lines, short bold text, red center, pink domain centers/core layer, white hard skills, cyan mental/social/recovery/long-term layer.

## Workflow

1. Identify the athlete, sport, and center goal.
2. Choose eight domains. Prefer `5` hard or sport-skill domains and `3` long-term domains.
3. Expand each domain into eight short, editable action cells.
4. Save as JSON first. JSON is the source of truth; SVG/PNG are outputs.
5. Render a square 81-cell visual if requested.

For badminton, a good default domain set is:

```text
後場攻防、切吊變化、網前手感、重心步法、發接前三、恢復保養、球友情場、長壽榜樣
```

## JSON Schema

Use this compact shape:

```json
{
  "title": "永錫羽毛球81宮格",
  "center": "越老越健康\n越久越快樂\n重心強",
  "visual_style": "ohtani",
  "domains": [
    {
      "name": "後場攻防",
      "type": "hard_skill",
      "items": ["側身準備", "高遠拉開", "殺球角度", "一殺一抽", "抽球拍面", "殺後銜接", "切吊變化", "教練回饋"]
    }
  ]
}
```

Rules:

- Exactly eight `domains`.
- Each domain has exactly eight `items`.
- Keep each label short enough for a square cell, usually 2-6 Chinese characters.
- Do not duplicate the domain name in `items`; the renderer places it in each outer 3x3 center.
- Use line breaks in `center` only when needed.

## Ohtani Visual Color Rules

Use these colors unless the user asks for another palette:

| Layer | Default color | Meaning |
|---|---|---|
| Center goal | red `#ff260f` | final target, identity-level athletic goal |
| Domain cells | pink `#fb8aa0` | the eight main domains and outer domain centers |
| Hard skills | white `#ffffff` | sport technique, body mechanics, concrete drills |
| Mental/social/long-term | cyan `#65eadb` | psychology, character, recovery, relationships, longevity |
| Section lines | black `#050505` | 3x3 blocks |
| Cell lines | gray `#b9b9b9` | individual cells |

Map domain types:

- `hard_skill`: white outer cells, pink domain center.
- `body`: white outer cells, pink domain center.
- `recovery`: cyan outer cells, pink domain center.
- `mental`: cyan outer cells, pink domain center.
- `social`: cyan outer cells, pink domain center.
- `longevity`: cyan outer cells, pink domain center.

## Rendering

Use the bundled script when a deterministic SVG is useful:

```bash
python3 scripts/render_ohtani_81_grid.py assets/yongxi-badminton.json output.svg
```

Then convert SVG to PNG with a local tool if available, such as:

```bash
qlmanage -t -s 2400 -o . output.svg
```

The script expects the JSON schema above and outputs a square 2400x2400 SVG.

## Prompt Pattern

When the user gives only a sport and goal, use this pattern internally:

```text
Create an Ohtani-style personal athlete 81 grid for SPORT.
Center goal: GOAL.
Return 8 domains, each with 8 short action cells.
Use 5 sport-skill/body domains and 3 recovery/mental/social/longevity domains.
Keep labels concise enough for a square 9x9 grid.
Use JSON as the editable source.
```
