---
name: visual-evidence-review
description:
  Capture and inspect concise before/after evidence for significant UI or design changes, store up to three WebP
  comparisons in Backlog tasks, and document truthful text-only or visually unchanged exemptions. Use during UI
  implementation and review across web, native apps, and games.
---

# Visual evidence review

Make agent-authored UI changes easy to review in their task. This skill applies in assisted and unattended work; it does
not change commit permissions or make every design adjustment a new human approval gate. Follow the project's ordinary
review policy. A separate unresolved design choice still needs human input.

This skill supports workspace schema 1/runtime schema 1. Inspect a versioned project's
`.agents/agent-workspace/install-manifest.json` compatibility and use its installed helper scripts. Unsupported
compatibility requires an explicit tooling/skill migration; globally updating this skill does not replace project
tooling.

## Decide what needs evidence

- Capture every significant user-facing change and every design change. Choose representative surfaces, states, and
  viewports covering the task, with at most **three combined before/after images per task**. Several related regions can
  share one capture when they remain legible; keep each region at its original scale.
- Skip screenshots for pure text changes. Record `text-only` with a concrete reason; typography, spacing, wrapping
  behavior, component placement, colors, or other design changes do not qualify merely because text is involved. For
  work with no UI effect, record `no-ui`.
- For potentially visual changes, compare matched captures using a 50/50 onion overlay and inspect it at native
  resolution. If no noticeable difference remains, record `no-visible-change` with the inspected overlay and reason.
  Numeric pixel differences support inspection; they never decide perceptual significance alone.
- Missing capture access, an unavailable baseline, unequal states, or a blank/error image are **blockers**, not
  exemptions. Record the limitation and defer through the normal task workflow when it cannot be resolved within scope.
  An after-only image may help diagnosis but does not satisfy a before/after review.

## Capture a trustworthy pair

Plan the views before editing and capture the actual baseline. Record baseline/current revisions or deployments, route
or scene, viewport and pixel scale, theme, locale, fixtures, and interaction state. Keep originals, capture metadata,
and intermediate files under `.local/visual-evidence/<task-id>/`. Use realistic safe fixtures; inspect for private
information before retaining an artifact.

Capture matching geometry and state with the project's existing tools. Do not stretch, align, redraw, generate, or
retouch screenshot content to make a pair agree. Wait for real readiness, loaded assets/fonts, and stable animations.
Use the same explicit crop on both images when a detail needs focus, keeping enough context to reveal displacement or
overflow. Missing baselines can use an isolated existing revision/worktree with separate outputs and ports; preserve the
active checkout and index.

Read only the relevant part of [capture guidance](references/capture.md):

- **Web:** use the installed `webcraft:ui-screenshots` skill when available. This task's `backlog/assets` destination
  and three-image cap override its default local-only delivery. If unavailable, adapt the project's Playwright setup
  into a reusable capture script/spec; the reference gives the minimal pattern.
- **Native macOS:** use an actual app render/test screenshot or capture the intended window. OS screen capture may
  require the capturing app's Screen & System Audio Recording permission. Accessibility permission for driving UI is
  separate; follow the reference when access is missing.
- **Godot or other games:** capture the actual rendered scene/viewport or a permission-approved game window. A
  successful headless test, import, or scene file is not a rendered screenshot.

## Inspect, combine, and record

Use the workspace's `.agents/agent-workspace/scripts/compare-ui.py` with a Python environment containing Pillow 10.1+
and WebP support. Prefer an existing project/bundled environment; no global dependency install is needed for the
coordination CLI. Run `--help` for supported options. The helper preserves pixels, labels the pair, calculates source
hashes/dimensions/differences, and leaves perceptual judgement to the reviewer.

```sh
python3 .agents/agent-workspace/scripts/compare-ui.py --root . --task TASK-42 --name menu-mobile \
  --before .local/visual-evidence/task-42/menu-before.png \
  --after .local/visual-evidence/task-42/menu-after.png
```

The first command writes only a local onion overlay and emits JSON. Open that overlay at native size and inspect the
originals for actual colors and contrast. For a noticeable change, rerun with `--publish` to create
`backlog/assets/task-42/menu-mobile.webp`. **Claim that task's asset directory before publishing.** Open every final
comparison and confirm its labels, framing, readable context, and coverage. `--replace` allows an intentional update at
the same exact slug; the helper never deletes unrelated evidence or chooses images to discard. Curate redundant evidence
explicitly within owned scope when reaching the three-image cap.

Use `node .agents/agent-workspace/scripts/agents.mjs --help` for the current `visual` command. Register one
classification per task with an inspection note; comparisons pass each final WebP using `--file`, and
`no-visible-change` passes its local overlay using `--onion`. A comparison note identifies the revisions/settings,
significant surfaces covered, and what the reviewer should inspect. The command maintains relative Markdown image embeds
in the task:

```markdown
![Before and after: mobile menu](../assets/task-42/menu-mobile.webp)
```

Register evidence after the final implementation snapshots, before verification/review, when using the guarded snapshot
workflow. Changed implementation or evidence requires fresh registration and review. The images are scoped
implementation artifacts; task embeds belong to the task's serialized Backlog record. Never edit task Markdown by hand
or stage somebody else's changes. Final task bookkeeping follows the shared commit workflow.

## Review result

The reviewer inspects the final pair and the claimed behavior, recording whether changes match the intended design and
whether there are regressions. Screenshots supplement functional checks; a visible button does not prove its action
works. Keep the inspection outcome and any limitation in the task. Retain at most three final WebP comparisons under
`backlog/assets/<task-id>/`; originals, overlays, and processing metadata stay ignored under `.local/`.
