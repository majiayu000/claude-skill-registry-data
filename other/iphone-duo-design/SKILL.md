---
name: iphone-duo-design
description: Use when designing, adapting, implementing, or auditing an iOS app for iPhone Duo, including resizing, folding, vertical bars, reserved regions, state continuity, multiple scenes, camera behavior, and accessibility. Produce evidence-based readiness findings with SDK gates and fallbacks. Do not use for generic iPhone work without Duo or adaptive-layout requirements, Android foldables, Microsoft Surface Duo, Google Duo, or claims of Apple certification.
---

# iPhone Duo design and readiness

Help an app keep its identity and functionality while its usable space changes.
This skill works with any coding assistant that can read Markdown. Shell,
browser, Xcode, and simulator tools are optional capabilities, not host-specific
dependencies. When a tool is unavailable, provide the exact remaining check
and keep its result unverified.

## Establish the target

Before changing code, inspect the app's deployment targets, Swift language mode,
selected Xcode/SDK, UI framework, scene configuration, and principal user flows.
For design-only work, record any unknowns instead of choosing a deployment target
for the user. Preserve existing platform support unless the user requests a change.

Read [versions and sources](references/versions-and-sources.md) before proposing
Duo-specific symbols. Refresh the official sources when implementation depends
on their current availability. The source snapshot is dated September 17, 2026;
it is not a claim about the SDK available in a future session.

Keep three evidence categories separate:

- Apple documentation or SDK declarations establish API contracts.
- This skill's engineering recommendations guide implementation and testing.
- A build, preview, simulator run, or device run proves only what it exercised.

A request for "Duo compliant" means a review against documented design guidance
and the app's requirements. Do not issue an Apple certification, guarantee App
Review approval, or call an untested app fully ready.

## Choose the work

| Request | Read and produce |
| --- | --- |
| Design review, layout, bars, fold handling | [Layout and controls](references/layout-and-controls.md); findings tied to affected flows |
| Lost state, multiple windows, simultaneous displays, camera | [Continuity, scenes, and camera](references/continuity-scenes-camera.md); ownership and lifecycle plan |
| Implementation with an older SDK or deployment target | [Versions and sources](references/versions-and-sources.md); verified API gate and fallback |
| Readiness audit or release evidence | [Verification](references/verification.md); completed [report template](references/readiness-report.md) |

For a narrow task, load only its references. The [adaptive editor example](examples/AdaptiveEditor.swift)
uses established APIs and shared edit state. It does not implement new Duo APIs
or prove behavior on Duo hardware.

## Work in this order

1. Follow one real task through the affected screens. Record where navigation,
   edits, selection, media, and presentation state live before changing layout.
2. Fix container sizing and state ownership first. Use environment traits and
   local view or scene geometry. Do not select a layout from a device-name
   string, global screen bounds, or a guessed hinge angle.
3. Prefer system navigation and presentations when they fit the app. Audit
   custom controls and content that sits in the center or near an edge.
4. Add Duo-specific APIs only where they improve an identified flow. Verify
   their complete signatures and platform availability in official docs and
   the selected SDK. A runtime availability check does not make an unknown
   symbol compile with an older SDK.
5. Keep a usable fallback. Explain both build-time exclusion for older SDKs
   and runtime availability for older OS versions; retain the app's existing
   navigation and task access in the fallback.
6. Exercise transitions during active work, then check final layouts. Use the
   verification matrix appropriate to the changed flow rather than collecting
   unrelated screenshots.

## Review rules that catch real defects

- Keep task state above layout alternatives. A resize must not create a second
  draft, restart capture, repeat a purchase, or discard a navigation path.
- Treat each scene's navigation and presentation state independently. Shared
  documents need an explicit conflict policy, not a global "current window".
- Keep every action reachable when controls overflow, a keyboard appears, or
  the layout collapses. Test the escape route from every modal presentation.
- Give controls useful names in accessibility and overflow presentations.
  Check reading order and focus after movement, not just at launch.
- Use hardware or SDK capability checks for optional features. A regular size
  class does not identify a particular device or prove accessory availability.
- For games, web views, or custom rendering engines, apply the same geometry,
  input, and state checks at the native host boundary. Do not invent framework
  plugins, browser fold APIs, physical dimensions, or review requirements.

## Deliver the result

For code changes, report the changed behavior, minimum versions, fallback,
tests performed, and remaining evidence gaps. For an audit, rank actionable
findings by user impact and attach a source or reproduction to each finding.
Use `verified`, `failed`, `blocked`, or `not applicable` per matrix row.

Keep unavailable SDK/device checks explicit while completing useful current-SDK
work. Recommend additional features only when they serve the app's actual tasks.
Do not add camera access, a second display experience, or sensor tracking merely
because the device supports it.
