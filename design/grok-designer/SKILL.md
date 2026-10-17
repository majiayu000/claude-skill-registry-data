---
name: grok-designer
description: Use Grok 4.5 as the required external design advisor when a task needs UI critique, UX critique, component-choice review, interaction-flow review, design imagery markdown, art direction, visual hierarchy judgment, design-system fit, color/type/layout suggestions, HTML mockups, SVG icons, handwritten SVG wordmarks, or file-based feedback on existing UI. Trigger on requests like "design a page", "generate design imagery", "give design advice", "optimize this UI", "improve UX", "optimize user flow", "review interaction", "check usability", "reduce friction", "choose the right component", "review this design", "create an icon", "suggest colors", "UI mockup", "visual direction", "lettering", "wordmark", "handwritten logo", or when another agent needs a second opinion on visual or interaction quality.
---


# Grok Designer — UI, UX, and Visual Design Advisor

Use Grok 4.5 as an external advisor for visual design, UI finish, UX task flow, interaction friction, art direction, and lightweight design artifacts.

## Critical rules

- ONLY interact with Grok through the global `grok-designer` CLI. Do not call the API or provider-specific scripts directly.
- When this skill is used, call `grok-designer` before giving UI advice, UX advice, design imagery, art direction, critique, visual advice, HTML, or SVG output. Do not write those deliverables from the agent's own judgment.
- Call `grok-designer` directly in the normal path. If the command is missing, install it silently with the bundled `scripts/install_cli` script, then retry.
- For visual/UI review of existing files, use `grok-designer ui`.
- For UX, task-model, component-choice, interaction-flow, friction, or state-behavior review, use `grok-designer ux`.
- For requests that need both UI and UX review, run `ui` and `ux` independently. You may use the CLI's comma-separated form, such as `grok-designer ui,ux ...`, or run separate commands in parallel.
- For broad art direction, use `grok-designer direction`. It may include files as background context.
- For design imagery markdown, use `grok-designer direction` and read the generated markdown before responding.
- For new standalone HTML/SVG design drafts, use `grok-designer html` or `grok-designer svg`.
- For a single handwritten SVG brand wordmark, lettering mark, signature mark, or logo-like text asset, use `grok-designer svg`.
- For a comparison sheet with multiple wordmark candidates, use `grok-designer html`.
- If the user provides screenshots, mockups, moodboards, or visual references, include relevant images with `-i / --image` when they help Grok judge visual style, layout, hierarchy, mood, fidelity, interaction sequence, or state transitions.
- Grok is stateless. It does not know the current project, prior conversation, screenshots, local files, design rules, or previous Grok outputs unless they are included in the current command.
- Do not ask Grok to review code quality, technical debt, CSS lint, engineering consistency, performance, or architecture unless the user explicitly asks. Keep Grok focused on what users can perceive and operate.
- Do not ask Grok to output code patches or diffs for existing files. Use its design advice, then make the actual edits yourself.
- After Grok returns UI advice, UX advice, design imagery markdown, visual direction, or an HTML mockup, show the output or a concise summary to the user and wait for confirmation before implementing it in project code, unless the user explicitly asked to implement immediately.
- Because UX changes often affect state logic, routing, form behavior, data loading, or validation, present a summary of structural/logic changes and wait for confirmation before refactoring component logic unless the user explicitly asked to implement immediately.
- After `html` or `svg` returns, do not start an extra AI review, visual critique, browser screenshot check, grep/tail completeness check, or refinement loop unless the user explicitly asked for checking or iteration. The CLI performs structural integrity checks before writing generated HTML/SVG. Read enough to know what Grok returned, then present it to the user.
- For ordinary HTML, SVG, or icon requests, run the script ONCE per task. Read the output file and proceed.
- Pass the user's stated requirements and concrete project context. Do not add the agent's own style labels, layout choices, color choices, metaphor choices, interaction concepts, or evaluation criteria unless the user explicitly said them.
- Do not pre-design for Grok. For creative generation, state the user goal, source material, output format, and hard constraints only. Do not name visual directions, metaphors, layouts, palettes, typography, materials, animations, or interaction models unless the user explicitly provided them.
- For multiple alternatives, ask Grok for independent, clearly different options. Do not assign the options names like "dashboard direction", "editorial direction", or "radar direction" unless the user gave those directions.
- The CLI manages its own configuration and authorization. Do not pre-check authorization. If a call fails with `error=not_authorized`, report that Grok Designer is not authorized.

## Grok CLI

Use `grok-designer` for every Grok task.

Normal path: call `grok-designer` directly. Do not run install or auth checks before every use.

If the shell reports `command not found`, resolve `/path/to/this-skill` to the directory containing this `SKILL.md`, run `/path/to/this-skill/scripts/install_cli` silently, then retry the original `grok-designer` command. If the installer reports a `path_warning`, use the printed `installed_path` for this turn and tell the user that the CLI directory is not on PATH.

If the CLI returns `error=not_authorized`, stop and tell the user Grok Designer is not authorized. Do not read, copy, print, or manage API keys.

Each command has its own built-in prompt. Choose the right command and pass the user's task plainly; do not add a cross-command prompt framework, design direction, UX solution, or extra output rules unless the user explicitly gave them.

Commands:

- `grok-designer ui` — Use for visual/UI review: layout, hierarchy, density, typography, color, spacing, surfaces, shadows, component appearance, visual consistency, and UI finish. It may include `-f` and `-i` as reference context, and requires a readable markdown file name with `-o`.
- `grok-designer ux` — Use for UX and interaction review: task model, component choice, flow, friction, control structure, affordance, recoverability, validation, navigation clarity, accessibility when it affects usability, and loading/error/empty/success/disabled/hover/focus/active states. It may include `-f` and `-i` as reference context, and requires a readable markdown file name with `-o`.
- `grok-designer ui,ux` — Use when the user wants both visual/UI and UX review. The CLI runs independent markdown review commands and writes one output per command.
- `grok-designer direction` — Use before implementation when the task needs a stronger idea, art direction, visual metaphor, design imagery markdown, or high-level design direction. Files are optional. Always provide a readable markdown file name with `-o`.
- `grok-designer html` — Use for a new standalone HTML mockup or concept page. It may include `-f` and `-i` as reference context, but do not use it to directly revise an existing project file.
- `grok-designer svg` — Use for a new SVG icon, simple illustration, or single handwritten SVG wordmark. It may include `-f` and `-i` as reference context.

When `ui` or `ux` needs to judge existing UI, pass complete relevant files by default. Do not summarize, slice, or annotate the file unless the file is too large for the CLI limit or the user asks for a scoped review. Prompt-only `ui` or `ux` is fine for general design questions.

For `ui`, `ux`, and `direction`, always name the markdown file at call time with `-o`. Prefer a bare readable filename, such as `accounts-filter-ui.md`, `tag-editor-ux.md`, `museon-home-art-direction.md`, or `pricing-page-design-imagery.md`; the CLI saves bare names under `.grok-designer/`. Use an explicit path only when a specific directory is required.

For multi-command markdown review, pass a single readable `-o` name. The CLI suffixes it per command:

```bash
grok-designer ui,ux "评审这个标签编辑组件" \
  -f ./TagEditor.tsx \
  -f ./tag-editor.css \
  -o tag-editor-review.md
```

This writes separate outputs such as `tag-editor-review-ui.md` and `tag-editor-review-ux.md`.

For `html` and `svg`, pass files with `-f` when Grok should reference existing content, design rules, previous mockups, theme tokens, example components, or brand references. Treat those files as context for a new design draft, not as files Grok will patch in place.

For `html`, describe the design goal only. Do not ask Grok to save a file, return a `file://` URL, provide a download link, or explain where the file is. The CLI writes the output file; Grok must return raw complete HTML source only.

For `html`, do not mention asset or dependency policy by default. Let Grok decide whether images, fonts, scripts, stylesheets, icon libraries, audio, or video help the design. Only add asset constraints when the user explicitly asks for them, such as fully self-contained, offline-safe, no external resources, or use realistic public images.

For handwritten wordmarks, use `svg` when the user wants one asset, and use `html` when the user wants several candidates to compare. Describe the word or words, mood, and any explicit material preference from the user. Do not prescribe neon, metal, sci-fi, or other effect-heavy styles unless the user asked for them. The default direction is readable paper-and-ink SVG lettering with subtle writing animation and tasteful finishing marks when useful.

The built-in `direction`, `html`, and `svg` prompts lightly remind Grok to avoid generic AI templates and default category stereotypes, keep the subject immediately recognizable through concrete sensory anchors, ground design choices in the product subject and real content, use purposeful contrast when it improves visual communication, spend visual boldness in one important place, and keep surrounding UI quiet.

## Context Rules

Grok receives only the command text, files passed with `-f`, and images passed with `-i`. It has no memory across calls.

The CLI places the final user goal after reference files and image manifests so Grok sees the concrete task last. Agents should keep the task text close to the user's wording instead of repeating constraints in several places.

When asking about an existing UI, pass the smallest complete set of files needed for the judgment:

- The target file or component being judged
- The project design guide or style reference, if one exists in the workspace
- Related CSS/theme/token files when they materially affect the visual result
- Nearby component files only when they define visible structure, visible states, or reused UI patterns
- State, hook, form, validation, routing, or context files when they materially affect UX behavior
- Screenshots, mockups, moodboards, reference images, exported previews, or sequential state screenshots when the user's question depends on what the UI looks like or how it changes

For `ui`, prioritize visible/rendered context:

- Target component or page files
- CSS/theme/token files
- Design-system or style-reference files
- Screenshots, rendered previews, mockups, or visual references

For `ux`, visual files are not enough. Include context that defines the user's task and state transitions:

- Component files that define controls, states, validation, and visible behavior
- Existing component-library files or nearby examples when the question depends on choosing the right control pattern
- Hooks, context, route, form, schema, or data-loading files that control the flow
- Copy/config files that affect labels, errors, confirmations, empty states, or success states
- Sequential images such as `-i step1.png -i step2.png` when the experience spans multiple states
- The intended user task, if it is not obvious from the files

Prefer complete files over excerpts. Use multiple `-f` flags:

```bash
grok-designer ui "判断这个页面是否符合项目现有视觉风格，并给出具体优化建议" \
  -f ./design.html \
  -f ./src/styles/tokens.css \
  -f ./src/components/Button.tsx \
  -o design-page-ui.md
```

```bash
grok-designer ux "评审这个标签编辑组件的任务模型和交互状态" \
  -f ./src/components/TagEditor.tsx \
  -f ./src/hooks/useTags.ts \
  -i ./screenshots/tag-editor-open.png \
  -o tag-editor-ux.md
```

Use `-i` for image context:

```bash
grok-designer ui "结合截图给这个页面提视觉设计建议" \
  -f ./design.html \
  -i ./screenshots/current.png \
  -o current-page-ui.md

grok-designer direction "参考这张图，生成设计意象 markdown" \
  -i ./references/moodboard.png \
  -o product-design-imagery.md
```

When images are passed with `-i`, the CLI may internally send an optimized WebP version to Grok to reduce request size while preserving readable UI detail. Agents should still pass the original screenshot or reference image path.

Do not pass unrelated source files, build output, dependency folders, logs, or implementation details that do not affect the visual result or user-visible interaction. If the needed context is too large, choose representative design-system files and say in the task text what is missing.

If Grok's `ui` or `ux` output says it needs more context, do not treat that as final advice. Gather the requested files or information when available, then rerun the same command once with the added `-f` or `-i` inputs. If the requested context cannot be found, tell the user exactly what is missing and ask for it.

The built-in `ui` prompt asks Grok to:

- focus on visual effect, information hierarchy, reading rhythm, typography, color, spacing, surfaces, component appearance, UI finish, and emotional tone
- avoid code review, CSS hygiene critique, technical debt, architecture, business logic, and new feature suggestions
- explain exactly where to change, how to change it, and why the visual result improves
- include pseudo-code, CSS, or JSX snippets when useful, with enough length to explain the change, without outputting a full file
- remind the implementing agent to prefer existing components, selectors, classes, tokens, variables, layout patterns, and interaction patterns
- name reusable components or tokens only when they are visible in the provided files; otherwise do not invent project-specific names
- include a short "do not change" section when there are concrete areas, tokens, components, visual traits, copy, or states that should be preserved
- ask for missing context instead of guessing when a reliable UI judgment is not possible

The built-in `ux` prompt asks Grok to:

- focus on natural task model, component choice, cognitive load, interaction friction, control structure, affordance, recoverability, validation, navigation clarity, accessibility when it affects usability, and visible state feedback
- judge whether the chosen component or control pattern matches the task, such as using an editable tag/chip editor for tag editing instead of separate add and delete inputs
- evaluate loading, error, empty, success, disabled, hover, focus, and active states when relevant
- avoid pure visual polish unless it directly harms usability
- avoid product strategy, feature bloat, gamification, broad repositioning, code review, CSS hygiene, technical architecture, and file-structure critique
- work within the existing product scope and user goal
- provide concrete structural, component-pattern, interaction, copy, state, or layout changes
- ask for missing state logic, routing, component code, component-library examples, form validation, or sequential screenshots instead of guessing when reliable UX judgment is not possible

## Parallel Review

When the user asks for multiple review dimensions, run each relevant command independently. Do not collapse UI, UX, art direction, HTML, or SVG work into one broad prompt.

For UI + UX review:

1. Run `grok-designer ui` and `grok-designer ux` separately, or run `grok-designer ui,ux` so the CLI writes independent outputs.
2. Pass the same user goal to both commands without adding agent-authored visual styles, interaction metaphors, palettes, layouts, or UX solutions.
3. Give `ui` screenshots, rendered previews, style tokens, theme files, and visible component files.
4. Give `ux` component logic, state files, routing files, component-library examples, form/validation logic, and sequential screenshots when available.
5. After both outputs return, synthesize them for the user:
   - Present UX first: task model, component choice, flow, state feedback, friction, and recoverability.
   - Present UI second: hierarchy, typography, spacing, polish, and visual consistency.
   - If UX and UI advice conflict, prioritize the UX structural decision first and explicitly note which UI advice only applies if the affected element remains.

Useful commands:

```bash
grok-designer ui "给这个页面提视觉/UI设计建议" -f ./design.html -o design-page-ui.md
grok-designer ux "评审这个页面的任务流、交互摩擦和状态反馈" -f ./design.html -o design-page-ux.md
grok-designer ui,ux "同时从 UI 和 UX 角度评审这个标签编辑组件" -f ./TagEditor.tsx -o tag-editor-review.md
grok-designer ui "结合截图给这个页面提视觉/UI设计建议" -f ./design.html -i ./screenshots/current.png -o page-screenshot-ui.md
grok-designer direction "给这个产品生成设计意象 markdown" -o product-design-imagery.md
grok-designer direction "基于这个页面生成设计意象 markdown" -f ./design.html -o page-design-imagery.md
grok-designer html "基于这个页面生成一个完整、全新的落地页方案。保留产品信息，由你独立判断视觉方向，不要复刻原稿。" -f ./design.html -o ./designs/page.html
grok-designer html "基于这个页面生成第 1 个完整落地页方案。保留产品信息，由你独立判断视觉方向。后续方案需要彼此明显不同。" -f ./design.html -o ./designs/page-option-1.html
grok-designer svg "为 Museon 生成一个手写 SVG 字标，气质像策展笔记标题" -o museon-wordmark.svg
grok-designer html "展示 Museon、Mel、Signal 三个手写 SVG 字标候选，默认偏纸面墨迹和真实笔触" -o wordmark-candidates.html
grok-designer svg "生成一个设置图标" -f ./brand.md -o ./icons/settings.svg
```

Read every output file before acting. Apply only the suggestions that fit the project.

`ui`, `ux`, and `direction` outputs include a final `原始提示词` section. It records the task text and readable paths for referenced files or images, without copying the full file contents into the appendix.

For advisory outputs (`ui`, `ux`, and `direction`) and HTML mockups from Grok, do not immediately edit project files. Present Grok's output or a concise summary, ask the user to choose or confirm the direction, then implement only the confirmed parts. SVG icon output can be saved directly when the user's request is only to create the asset. Do not run a self-review pass just because an HTML or SVG file was created.

The script prints on success:

```text
output_path=<path to output file>
```

For multi-command review, it prints one path per command:

```text
output_path[ui]=<path to UI output file>
output_path[ux]=<path to UX output file>
```

For `html` and `svg`, the script also prints:

```text
integrity=passed
```

Read the file at `output_path` to get Grok's response.

On failure, the CLI prints stable fields:

```text
error=<code>
message=<short explanation>
hint=<next step>
```

Follow the `hint` when it is actionable. If `error=not_authorized`, stop and tell the user Grok Designer is not authorized.

For generated HTML/SVG, treat `output_path` plus `integrity=passed` as the normal completeness signal. Do not duplicate CLI checks in the agent unless the user asks for additional browser or visual verification.

## Output types

- `grok-designer ui` — Markdown UI review output.
- `grok-designer ux` — Markdown UX review output.
- `grok-designer direction` — Markdown design direction output.
- `grok-designer html` — Self-contained complete HTML source with inline CSS. Ready to open in browser. The CLI rejects incomplete HTML, missing head/body, file URLs, markdown fences, lorem ipsum, and non-HTML wrapper output.
- `grok-designer svg` — Clean SVG code for icons, simple illustrations, or single handwritten wordmarks. The CLI rejects invalid XML, wrapper text, markdown fences, and local file URLs. Can be saved directly or embedded in HTML/React.

## Configuration

- The global CLI reads `~/.config/grok-designer/config.toml`.
- Image optimization defaults to WebP when supported by the local CLI environment.
- Agents should not read, copy, or manage API keys.
- Do not check authorization in the normal path. Use `grok-designer auth status` only when explicitly debugging authorization.

## When to use

- Need Grok to inspect existing HTML/CSS/TSX and give visual UI advice
- Need Grok to inspect existing UI and give UX, interaction, task-flow, or state-feedback advice
- Need a concise visual or UX optimization plan based on one or more local files
- Need a visual reference or HTML mockup for a UI component or page
- Need handwritten SVG wordmark, lettering, signature mark, or logo-like text candidates
- Need SVG icons or simple illustrations
- Need color palette, typography, or layout suggestions
- Need design feedback or critique on an existing design
- Want a quick single-page HTML prototype to show a concept

## Workflow

1. Choose the smallest useful Grok task: `ui`, `ux`, `direction`, `html`, or `svg`.
2. Run `grok-designer` with a readable `-o` path and get an `output_path` before writing the final answer or file.
3. Use the user's wording as the task text whenever possible. Add only factual context needed to identify files, product scope, or constraints the user actually gave.
4. For visual/UI review, call `grok-designer ui`.
5. For UX, task-model, component-choice, interaction-flow, friction, or state-feedback review, call `grok-designer ux`.
6. For combined UI + UX review, run `grok-designer ui,ux` or run both commands independently and synthesize the outputs.
7. For design imagery markdown or visual direction, call `grok-designer direction`.
8. For new HTML/SVG design drafts, call `grok-designer html` or `grok-designer svg`; include `-f` or `-i` when reference context matters.
9. For a single handwritten SVG wordmark, call `grok-designer svg`; for several wordmark candidates in one comparison sheet, call `grok-designer html`.
10. Read Grok's output.
11. If `ui` or `ux` says more context is needed, gather the requested context and rerun the same command once before presenting advice to the user. If the context is unavailable, ask the user for it.
12. When implementing `ui` or `ux` output, first look for existing project components, selectors, classes, tokens, variables, and layout patterns to reuse. If Grok suggests replacing a broad system or inventing unrelated UI, narrow it to existing patterns before editing.
13. If Grok drifts into code review when the task is design review, rerun with a scoped goal such as: "只从 UI/UX 角度判断，不要评论代码规范或工程债。"
14. Present advisory outputs or HTML mockups to the user for confirmation before editing project code, unless the user explicitly asked to implement immediately.
15. Base the final response on Grok's output. You may summarize, select, or implement useful parts, but do not replace Grok's design judgment with your own generated design direction.

## Tips

- Keep the task prompt close to the user's request.
- If the user did not specify a style, color, font, layout, metaphor, visual direction, or interaction model, do not invent one in the prompt.
- Do not split multiple Grok generations by agent-authored themes. Use neutral wording such as "第 1 个独立方案 / 第 2 个独立方案 / 第 3 个独立方案" and ask Grok to make them clearly different through its own judgment.
- When passing a reference design, say whether Grok may preserve or should avoid copying it. Do not replace that with your own alternate concepts.
- For HTML mockups, do not mention asset or dependency rules unless the user asks. Unnecessary constraints can weaken Grok's design judgment.
- Only pass explicit user preferences, such as "dark mode" or "use blue", when the user actually said so.
- When the task asks for design insight, direction, or an HTML mockup, do not ask Grok for long explanatory copy. Let Grok express ideas through visible UI structure, states, examples, hierarchy, and interaction when possible.
- Do not translate "more designed" into visual noise. Strong visual treatment should support key actions, brand memory, and key content entry points; supporting areas should stay quiet, stable, and easy to scan.
- Let Grok decide how to avoid cliches. Do not add your own list of banned styles, but pass explicit user constraints such as "避免俗套科技感、赛博朋克感" when the user says them.
- Let Grok actively consider motion, inline SVG, material, and micro-interaction opportunities, but do not prescribe a specific animation or material style unless the user asked for it.
- Do not add your own anti-template checklist to the task prompt. The CLI already gives Grok light reminders about generic AI aesthetics, memorable visual ideas, restraint, real content, and UI copy.
- Chinese prompts work well — Grok responds in the same language.
