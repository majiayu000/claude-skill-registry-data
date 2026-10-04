---
name: remotion
description: "Use when creating programmatic videos, animated explainers, or visual compositions with Remotion."
---

# Remotion Video Creator

Create videos using Remotion — React components rendered as video frames. Orchestrates a multi-phase pipeline from concept to verified MP4.

## Prerequisites

**Node.js >= 18** and **npm >= 9** on PATH; headless Chromium is bundled with `@remotion/cli`.
For project structure and full reference index, see [project-layout.md](references/project-layout.md).

## Quick Start

```
User: Create a 30-second explainer video about how DNS works
```

The skill runs a 5-phase pipeline: storyboard the concept, generate voiceover audio, build React scenes in parallel, evaluate quality via stills, and verify against the storyboard. Each phase gates the next.

## Pipeline

Each phase has a reference with full instructions — read it when you reach that phase.

| Phase | Name | Reference | Gate |
|-------|------|-----------|------|
| 0 (opt) | Analyze | [analyze.md](references/analyze.md) | `.storyboard.md` exists |
| 1 | Storyboard | [storyboard.md](references/storyboard.md) | User approves `docs/STORYBOARD.md` |
| 2 | Audio | [audio.md](references/audio.md) | `public/vo-beat*.mp3` + `src/timing.ts` exist |
| 3 | Build | [build.md](references/build.md) | All scenes render and pass visual inspection |
| 4 | Eval | [eval.md](references/eval.md) | All scenes score >= 7.0 |
| 5 | Verify | [verify.md](references/verify.md) | User approves `docs/VERIFICATION_REPORT.md` |

## References

- **Pipeline:** [storyboard](references/storyboard.md) · [audio](references/audio.md) · [build](references/build.md) · [eval](references/eval.md) · [verify](references/verify.md) · [analyze](references/analyze.md)
- **Design:** [design system](references/design-system.md) · [color script](references/color-script-rules.md) · [motion rules](references/motion-design-rules.md) · [backgrounds](references/backgrounds.md) · [diagrams](references/diagrams.md)
- **Components:** [core](references/components.md) · [extended](references/components-extended.md) · [TerminalScene](references/components-terminal-scene.md) · [terminal_recording](references/terminal-recording-scene-type.md) · [scene templates](references/scene-templates.md) · [patterns](references/patterns.md)
- **Animation:** [vocabulary](references/animation-vocabulary.md) · [hooks](references/animation-hooks.md) · [transitions](references/transition-catalog.md) · [audio sync](references/audio-sync-patterns.md)
- **Content:** [audio/voiceover](references/audio-voiceover.md) · [narrative](references/narrative-structures.md) · [marketing](references/marketing-concepts.md) · [visualization](references/visualization-reasoning.md)
- **Templates:** [beat sheet](references/beat-sheet-template.md) · [storyboard](references/visual-storyboard-template.md) · [timing](references/timing-manifest-template.md) · [verification](references/verification-template.md) · [CLAUDE.md](references/claude-md-template.md)
- **Other:** [project layout](references/project-layout.md) · [error recovery](references/error-recovery.md) · [output format](references/output-format.md)
