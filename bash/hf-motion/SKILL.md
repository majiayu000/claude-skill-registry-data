---
name: hf-motion
# Description is 399 chars, over check 16's 250-char WARN band, on purpose: the eight implemented recipe names (~110) are the per-recipe trigger surface (per-recipe phrases live in references/help.md), and the product-launch-video boundary keeps "site launch video" asks from misfiring on launch-film (trigger-eval, #26).
description: >-
  Render a HyperFrames motion graphic recipe: intro-kinetic, pixel-dissolve,
  circle-pop, screen-dive, text-sandwich, letter-flythrough, ui-morph,
  launch-film. Use for /video:hf-motion, "자기소개 모션그래픽 만들어줘",
  "make my kinetic intro video". Needs the official hyperframes plugin. Not
  for freeform video (hyperframes:motion-graphics), site launch videos
  (hyperframes:product-launch-video) or planned recipes.
license: MIT
allowed-tools: Bash, Read, Skill, AskUserQuestion
compatibility:
  network: required
metadata:
  model_recommendation:
    tier: sonnet
    reason: "recipe dispatcher: parse params, run scripted scaffold and verification gates, inspect snapshots"
    claude: prefer
    non_claude: advisory-only
---

# video:hf-motion — recipe → parameterized HyperFrames video

## Role

같은 뼈대, 내용만 교체. 레시피 템플릿(`templates/<recipe>/`)의 `CONFIG` 를 파라미터로 채우고
공식 `hyperframes` 플러그인 CLI 로 lint → check → snapshot → render → 검증. 엔진 규칙은
`hyperframes:hyperframes-core` / `hyperframes:motion-graphics` 소유 — 여기서 재서술하지 않는다.

## Prologue — every Bash block

Bash calls share no variables: start each block with these two lines, filling
`<skill-base-dir>` with the absolute directory you read this file from.

```sh
if [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then HFM="$CLAUDE_PLUGIN_ROOT/skills/hf-motion"; else case "<skill-base-dir>" in /*) HFM="<skill-base-dir>" ;; *) HFM="${HERMES_SKILL_DIR}" ;; esac; fi
[ -n "$HFM" ] && [ -f "$HFM/scripts/scaffold.mjs" ] || { printf '[FAIL] hf-motion: skill dir unresolved (%s); export CLAUDE_PLUGIN_ROOT=<plugin dir>\n' "${HFM:-unset}" >&2; false; }
```

## Step 1: Parse args

`$ARGUMENTS` = `<recipe> [key=value ...] [--out <dir>]` (table, examples, env: `references/help.md`).
- `-h` / `--help` / `help` → print `references/help.md` verbatim and stop.
- No recipe → run `node "$HFM/scripts/scaffold.mjs" --list`, add the planned list
  from `references/recipes/README.md` (marked not implemented), ask which one, stop.
- Planned / unknown recipe → say it is not implemented and stop; never approximate it.

## Step 2: Prerequisite — official hyperframes plugin

```sh
PLUGIN=$(bash "$HFM/scripts/find-hf-plugin.sh") || exit 1
```

On failure stop with its message. Then load `Skill(hyperframes:hyperframes-core)` and
`Skill(hyperframes:motion-graphics)` before touching anything beyond `CONFIG`.
Every CLI call goes through `node "$PLUGIN/skills/hyperframes/scripts/plugin-cli.mjs" <cmd>`
— never a bare `npx hyperframes`, never `skills update`.

## Step 3: Collect and confirm params

Read `references/recipes/<recipe>.md` (param table, limits, timeline) and
`references/constraints.md`. Every on-screen string and number comes from the
user — ask for any fact you do not have; never invent one. Show the full
param table (defaults marked) and get an explicit yes before Step 4.

## Step 4: Scaffold

```sh
node "$HFM/scripts/scaffold.mjs" <recipe> <out-dir> 'key=value' ...
```

Quote each pair; lists use `|`; Korean stays literal UTF-8. It validates limits and
writes `CONFIG`, the static timing attributes, the music bed and any user asset
(an unreadable one stops it, nothing written; `--update` re-applies).

## Step 5: Verification gates

Bind `PLUGIN` as in Step 2, then run lint, check, snapshot per `references/verification.md` and **look at every
snapshot** with Read (tofu, overflow, wrong text, palette). Any error → fix the cause
and re-run from Step 4. Only the warnings listed there are accepted.

## Step 6: Render and verify

Only after Step 5 is clean and the params are confirmed:

```sh
PLUGIN=$(bash "$HFM/scripts/find-hf-plugin.sh") || exit 1   # re-bind: new Bash call
cd <out-dir> && node "$PLUGIN/skills/hyperframes/scripts/plugin-cli.mjs" render . -q high -o ./renders/video.mp4
python3 "$HFM/scripts/verify-render.py" renders/video.mp4 <verify-args>
```
`<verify-args>`: copied verbatim from the scaffold's `verify-render args:` line.

## Step 7: Report

`[OK] video:hf-motion <recipe> -> <out-dir>/renders/video.mp4` + params table, inspected
snapshot paths, verify-render lines — or `[FAIL] video:hf-motion stopped at step <n>: <reason>`.
No success claim without the verify-render output.
