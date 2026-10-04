---
name: quality-check
description: Run pre-publish quality assurance checks on a clip including visual quality, audio quality, platform compliance, and content completeness.
---

# Quality Check

Run automated quality assurance checks on a ProAnimate clip before publishing. Scores visual quality, audio quality, content completeness, and platform compliance, then provides actionable improvement suggestions and auto-fix capabilities.

## Purpose

Ensure a clip meets minimum quality standards before export or publishing. The QA system grades clips from A+ to F, identifies specific issues (text readability, audio clipping, missing elements), and can automatically fix common problems.

## Steps

1. **Gather QA input** from stores using `extractQAInputFromStores()`:
   - Visual input: canvas element bounds (position, size, type, opacity, frame range), background color, text colors/sizes.
   - Audio input: dialogue segments (amplitude, peak levels), music volume, total duration.
   - Content input: planned vs. actual counts for characters, dialogue lines, text overlays, templates, SVG objects, media items. Error frame list.
   - Platform target (optional): tiktok, instagram, youtube, etc.

2. **Generate the QA report** by calling `generateQAReport(input, threshold)`:
   - Runs all category scorers in sequence:
     - `scoreVisualQuality()` -- element overlap detection, text readability (WCAG contrast), visual balance, empty space ratio.
     - `scoreAudioQuality()` -- dialogue audibility (amplitude levels), music vs. dialogue balance, awkward silence detection, audio coverage, clipping detection.
     - `scoreContentCompleteness()` -- character count match, dialogue audio completeness, text overlay rendering, template loading, SVG object presence, frame integrity.
     - `checkPlatformCompliance()` -- aspect ratio, duration limits, safe zone verification, resolution, caption requirements, CTA recommendations, text coverage limits.
   - Each check produces a `QACheckResult` with: id, name, category, status (pass/fail/warning/skipped), severity (critical/warning/info), score (0-100), suggestion, autoFixable flag.

3. **Interpret the report**:
   - `overallScore` -- weighted average across all categories (0-100).
   - `grade` -- letter grade: A+ (95+), A (85+), B+ (78+), B (70+), C+ (63+), C (55+), D (40+), F (<40).
   - `passed` -- whether the score meets the threshold (default 60).
   - `categoryScores` -- per-category breakdown (visual, audio, content, platform). Critical checks are weighted 3x, warnings 2x.
   - `improvements` -- sorted list of actionable fixes with estimated impact scores.

4. **Apply auto-fixes** (if available):
   - `runAutoFixLoop(maxIterations)` iterates: fix issues, re-check, repeat until passing or max iterations reached.
   - Supported auto-fix actions:
     - `add-text-background` -- adds semi-transparent background to low-contrast text overlays.
     - `adjust-music-volume` -- lowers music volume to 25% when it overpowers dialogue.
     - `enable-captions` -- turns on word-by-word captions.
     - `set-aspect-ratio` -- switches to platform-preferred aspect ratio.
     - `set-resolution` -- adjusts canvas resolution to meet platform minimums.

5. **Run pre-publish checklist** for manual verification:
   - `generatePrePublishChecklist()` returns a checklist of required and recommended items:
     - Required: content present, audio generated, background set, valid duration, adequate resolution.
     - Recommended: captions enabled, background music, CTA present, optimal aspect ratio, brand compliance.
   - Items are auto-checked based on current project state.

## Key Files

| Purpose | Path |
|---------|------|
| Quality gate orchestrator | `src/services/qualityAssurance/qualityGate.ts` |
| Visual quality scorer | `src/services/qualityAssurance/visualQuality.ts` |
| Audio quality scorer | `src/services/qualityAssurance/audioQuality.ts` |
| Content completeness | `src/services/qualityAssurance/contentCompleteness.ts` |
| Platform compliance | `src/services/qualityAssurance/platformCompliance.ts` |
| Auto-fix loop | `src/services/qualityAssurance/autoFix.ts` |
| Pre-publish checklist | `src/services/qualityAssurance/prePublishChecklist.ts` |
| A/B variant generator | `src/services/qualityAssurance/variantGenerator.ts` |
| QA types | `src/types/qualityAssurance.ts` |
| QA store | `src/stores/useQualityAssuranceStore.ts` |
| Pre-publish score UI | `src/components/panels/PrePublishScore.tsx` |

## Common Issues

- **Low visual score from overlap**: Text overlays placed on top of characters or media. Check `CanvasElementBounds` for frame-range collisions. Overlaps involving text are penalized more heavily.
- **Audio dialogue audibility fail**: Dialogue segments with `avgAmplitude < 0.15` are flagged as too quiet. Check ElevenLabs TTS volume settings.
- **Audio clipping**: Dialogue segments with `peakAmplitude > 0.95` clip. Reduce TTS volume or apply compression.
- **Content completeness mismatch**: Planned element count differs from actual. Usually caused by failed asset loading (broken image URLs, template errors). Check `errorFrames` array.
- **Platform safe zone violations**: Elements placed in platform-reserved areas (TikTok bottom 20%, right 12%). Use `compositionEngine.ts` safe zone functions.
- **Auto-fix changes not visible**: Auto-fix mutates Zustand stores directly (e.g., `useTextOverlayStore`). The UI should re-render automatically, but force a re-render if the canvas does not update.

## Examples

Run full QA report:
```ts
import { generateQAReport, extractQAInputFromStores } from '@/services/qualityAssurance/qualityGate'
const input = extractQAInputFromStores()
const report = generateQAReport(input, 60)
console.log(report.grade, report.overallScore, report.passed)
```

Run auto-fix loop:
```ts
import { runAutoFixLoop } from '@/services/qualityAssurance/autoFix'
const { finalReport, appliedFixes, iterations } = await runAutoFixLoop(3)
console.log(`Fixed ${appliedFixes.length} issues in ${iterations} iterations`)
```

Generate pre-publish checklist:
```ts
import { generatePrePublishChecklist } from '@/services/qualityAssurance/prePublishChecklist'
const checklist = generatePrePublishChecklist({
  hasDialogue: true, hasCaptions: true, hasBackground: true,
  durationSeconds: 30, canvasWidth: 1080, canvasHeight: 1920,
  // ... other fields
})
console.log(checklist.items.filter(i => !i.checked))
```
