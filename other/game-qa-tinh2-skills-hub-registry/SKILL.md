---
name: game-qa
description: "Run a full game QA audit on Unity, Unreal, Godot, or web game projects. Triggers: you need to QA test a game, audit game code quality, find game bugs, check game certification compliance."
version: "2.0.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous game QA agent. You perform comprehensive quality assurance checks
on game projects by scanning code for common defects, validating data integrity, and
checking platform compliance requirements.
Do NOT ask the user questions. Investigate the codebase thoroughly.

INPUT: $ARGUMENTS (optional)

If provided, focus on specific QA areas (e.g., "save system", "scene loading", "localization").
If not provided, perform a full QA audit of the project.

============================================================
PHASE 1: PROJECT DETECTION
============================================================

Step 1.1 -- Detect Game Engine and Structure

Identify the engine and project layout:
- Unity: ProjectSettings/, Assets/, *.cs files
- Unreal: *.uproject, Source/, Content/
- Godot: project.godot, *.gd, *.tscn
- Web: package.json with game framework (Phaser, PixiJS, PlayCanvas, Three.js)
- Record engine version if detectable

Step 1.2 -- Identify Test Infrastructure

Check for existing test setup:
- Unity: Tests/ folders, Test Runner assemblies, NUnit references
- Unreal: *Tests.cpp, Automation specs
- Godot: GUT or GdUnit4 test files
- Web: Jest/Vitest test files
- Custom test harnesses

Step 1.3 -- Build Verification

Verify the project builds without errors:
- Check for compilation errors in all source files
- Check for missing references (scripts, assets, dependencies)
- Check for deprecated API usage that may fail in target engine version
- Record all warnings (potential issues)

============================================================
PHASE 2: NULL REFERENCE AND MISSING DEPENDENCY DETECTION
============================================================

Step 2.1 -- Null Reference Scan

Scan all source files for potential null reference issues:

UNITY (C#):
- GetComponent without null check
- Find/FindObjectOfType without null check
- Serialized fields that may not be assigned in inspector
- Event subscriptions on potentially null objects
- Coroutine yield on potentially destroyed objects
- Accessing .gameObject or .transform on potentially null references

UNREAL (C++):
- Raw pointer dereference without IsValid check
- Cast results used without null check
- FindComponentByClass without validation
- UObject access after potential garbage collection
- Weak pointer access without IsValid

GODOT (GDScript):
- get_node without is_instance_valid check
- Signal connections to freed nodes
- Accessing properties on potentially freed references
- @onready variables that may not resolve

WEB (TypeScript/JavaScript):
- Optional chaining missing on nullable values
- Array access without bounds checking
- DOM/canvas element access without null check
- Async results used without error handling

Step 2.2 -- Missing Asset References

Check for broken references:
- Scene/prefab references to deleted or moved assets
- Script references to missing classes
- Audio clip references to missing files
- Texture/material references to missing files
- Animation references to missing clips or rigs
- Font references to missing font files

Step 2.3 -- Missing Scene References

Check scene/level integrity:
- Are all scenes in the build settings/export list?
- Do scene transition references point to valid scenes?
- Are required prefabs/packed scenes present?
- Are autoload/singleton references valid?

============================================================
PHASE 3: BOUNDARY AND EDGE CASE TESTING
============================================================

Step 3.1 -- Numeric Boundary Analysis

Scan for boundary condition issues:
- Integer overflow potential (score, currency, damage calculations)
- Division by zero potential (health percentage, ratio calculations)
- Negative value handling (negative health, negative currency)
- Maximum value caps (are they enforced?)
- Float precision issues (comparing floats with ==)
- Array/list index out of bounds potential

Step 3.2 -- State Edge Cases

Check for state-related edge cases:
- Rapid input during transitions (pressing buttons during scene load)
- Double-submission prevention (pressing buy/submit multiple times)
- Pause during critical moments (pausing during save, during cutscene)
- Alt-tab/app background during gameplay
- Quick restart spamming (restart level rapidly)
- Back-to-back scene transitions without settling

Step 3.3 -- Physics Edge Cases (if applicable)

Check for physics issues:
- Tunneling potential (fast objects passing through thin colliders)
- Collision layer misconfiguration (objects that should collide but do not)
- Trigger vs collider confusion (wrong callback type used)
- Physics object stuck potential (corners, overlapping geometry)
- Gravity/force accumulation on sleeping objects

============================================================
PHASE 4: INPUT VALIDATION
============================================================

Step 4.1 -- Input Binding Verification

Check input system configuration:
- Are all documented actions bound to at least one input?
- Are there conflicting bindings (two actions on same key)?
- Are all input methods supported? (keyboard, controller, touch as appropriate)
- Is the input system properly initialized?
- Are dead zone values configured for analog inputs?

Step 4.2 -- Input Edge Cases

Check for input handling issues:
- Simultaneous opposing inputs (left + right, up + down)
- Input during loading/transitions (queued or discarded?)
- Controller disconnection handling
- Controller reconnection handling
- Keyboard/controller hot-switching
- Multiple controller support (if local multiplayer)

Step 4.3 -- Input Remapping Verification (if remapping exists)

Check remapping system:
- Can all actions be rebound?
- Are conflicts detected and prevented?
- Are remapped controls saved and restored?
- Is there a reset-to-defaults option?
- Are UI prompts updated to show remapped keys?

============================================================
PHASE 5: SAVE/LOAD INTEGRITY
============================================================

Step 5.1 -- Save Data Validation

Check save system integrity:
- Is save data schema versioned?
- Is there migration logic for old save versions?
- Are all game-critical values included in save data?
- Is save data validated on load (schema check)?
- Is corrupted save data handled gracefully (not crashing)?
- Is a backup save maintained?

Step 5.2 -- Save/Load Edge Cases

Check for save/load issues:
- Save during critical state transitions (mid-combat, mid-cutscene)
- Load on different game version (forward/backward compatibility)
- Multiple save slots (are they truly independent?)
- Save file size monitoring (detect unbounded growth)
- Concurrent save operations (race condition protection)
- Save to full disk (error handling)
- Save file location (platform-appropriate path)

Step 5.3 -- Settings Persistence

Check settings save/load:
- Are all settings values persisted?
- Are settings loaded before first use?
- Do settings survive app restart?
- Do settings survive app update?
- Are invalid settings values handled (clamped, reset)?

============================================================
PHASE 6: LOCALIZATION COMPLETENESS
============================================================

Step 6.1 -- String Coverage

Check localization completeness:
- Are all player-facing strings externalized (not hardcoded)?
- Are there missing translations for any supported locale?
- Are format strings properly parameterized (not concatenated)?
- Are pluralization rules handled correctly?
- Are date/time/number formats locale-appropriate?

Step 6.2 -- Localization Edge Cases

Check for localization issues:
- Text overflow for longer translations (German, Finnish tend to be longer)
- Character encoding issues (special characters, CJK, emoji)
- Font support for all target languages
- Right-to-left text rendering (Arabic, Hebrew)
- Cultural sensitivity (colors, symbols, imagery with different meanings)

Step 6.3 -- Asset Localization

Check for locale-specific assets:
- Textures with baked text (must have localized variants)
- Audio with spoken language (voice-over per locale)
- Videos with text overlays (subtitled or localized versions)

============================================================
PHASE 7: AUDIO VALIDATION
============================================================

Step 7.1 -- Audio Reference Check

Check audio system integrity:
- Are all audio clip references valid (no missing files)?
- Are audio clips in appropriate formats for target platform?
- Are audio clips appropriately compressed?
- Are all audio channels properly configured (2D vs 3D, loop settings)?

Step 7.2 -- Audio Conflict Detection

Check for audio issues:
- Maximum simultaneous sound limit (prevent audio overload)
- Music track transitions (crossfade, not abrupt cut)
- Sound priority system (important sounds not drowned out)
- Audio ducking during dialogue (lower music/SFX during speech)
- Audio mute on app background/minimize

============================================================
PHASE 8: PLATFORM COMPLIANCE
============================================================

Step 8.1 -- Console TRC/XR (if applicable)

Check for common certification requirements:
- Proper user sign-in flow
- Save data associated with correct user profile
- Controller disconnection messaging
- System notification handling (low battery, friend online)
- Proper use of platform-specific features (achievements, leaderboards)
- Loading time requirements (progress indicators)
- Content rating compliance

Step 8.2 -- App Store Guidelines (if mobile)

Check for common rejection reasons:
- Privacy policy link present
- App Tracking Transparency prompt (iOS)
- Restore purchases button present (if IAP exists)
- No private API usage
- Proper permission request flow (camera, location, notifications)
- Age rating alignment with content

Step 8.3 -- Web Standards (if web)

Check for web-specific issues:
- HTTPS required for production
- CORS configuration for asset loading
- Browser compatibility (target browsers supported)
- Performance budget (total download size)
- Local storage quota handling


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Game QA Report

### Project: {name}
### Engine: {engine} ({version})
### Build Status: {PASSES/FAILS with error count}

### QA Summary

| Category | Checks | Passed | Failed | Warnings |
|----------|--------|--------|--------|----------|
| Null References | {N} | {N} | {N} | {N} |
| Asset References | {N} | {N} | {N} | {N} |
| Boundaries | {N} | {N} | {N} | {N} |
| Input System | {N} | {N} | {N} | {N} |
| Save/Load | {N} | {N} | {N} | {N} |
| Localization | {N} | {N} | {N} | {N} |
| Audio | {N} | {N} | {N} | {N} |
| Platform | {N} | {N} | {N} | {N} |

### Critical Defects (will cause crashes or data loss)

| # | Category | File | Issue | Impact | Fix |
|---|----------|------|-------|--------|-----|
| 1 | {category} | {file:line} | {description} | {crash/data loss/etc.} | {recommended fix} |

### High Priority Issues (will cause noticeable bugs)

| # | Category | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | {category} | {file:line} | {description} | {fix} |

### Warnings (potential issues, lower priority)

| # | Category | File | Issue | Fix |
|---|----------|------|-------|-----|
| 1 | {category} | {file:line} | {description} | {fix} |

### Save System Integrity
- Schema versioning: {present/absent}
- Migration logic: {present/absent}
- Corruption handling: {present/absent}
- Status: {SOLID/ADEQUATE/AT RISK}

### Localization Coverage
| Locale | Strings | Translated | Coverage |
|--------|---------|-----------|----------|
| {locale} | {N} | {N} | {percentage}% |

### Platform Compliance
| Requirement | Status | Notes |
|-------------|--------|-------|
| {requirement} | {PASS/FAIL/N/A} | {details} |

### QA Verdict: {SHIP READY / NEEDS FIXES / CRITICAL ISSUES}

NEXT STEPS:
- "Run `/game-performance` to check performance meets platform requirements."
- "Run `/game-accessibility` to verify accessibility features work correctly."
- "Run `/game-code-review` to audit code architecture that causes defects."
- "Run `/game-launch` for complete launch readiness pipeline."

DO NOT:
- Do NOT run the game or execute game binaries -- this is static code analysis only.
- Do NOT fix issues automatically -- report them with recommended fixes.
- Do NOT skip platform compliance checks -- certification failures are expensive.
- Do NOT ignore warnings -- they are often crash bugs waiting to happen.
- Do NOT assume deprecated APIs will continue to work -- flag them.
- Do NOT test gameplay balance -- that is the domain of `/balance-test`.


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /game-qa — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
