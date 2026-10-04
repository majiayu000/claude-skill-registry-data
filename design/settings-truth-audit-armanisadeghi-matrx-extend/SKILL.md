---
name: settings-truth-audit
type: Skill
title: "settings-truth-audit — prove every setting is read, honest, previewable and reachable from where it acts"
description: "Audit-and-fix method for one user setting area across every repo. Use when a setting seems ignored, duplicated or confusing, on 'audit the X settings' or 'why doesn't my X setting apply', or as a lane of the settings sweep. NOT for adding a new setting (use build-sub-feature)."
tags: [settings, knobs, census, audit, doctrine]
timestamp: 2026-09-25T00:00:00Z
---

<!-- SYNCED COPY — do not edit here.
     Canonical: common-docs/skills/settings-truth-audit/SKILL.md
     This file is distributed to every consuming repo by
     common-docs/meta/scripts/sync_skills.py. Edit the canonical, run the
     sync, and commit each repo. Edits made here are overwritten and lost. -->

# settings-truth-audit

Arman, 2026-09-25, after two wrong answers about voice: *"The core problem is no one gives enough
fucks to go get the facts."* The voice area had five pickers in four stores; three of them were
read by nothing, one claimed to apply "everywhere", none played a sample, and the Chrome extension
used a hardcoded voice. Worked example — read it once:
for-Arman hand-over 2026-09-25 · voice-census.md (deleted in d0e885c98).

Every step ends on a check. The report is the census table plus the fixes, never prose.

## 1. Census the EXPERIENCES, not the settings screens

Start from where the capability actually happens, in every repo (`matrx-frontend`, `aidream`
incl. `mobile/`, `matrx-extend`, `matrx-local`, `matrx-sandbox`, packages). Grep the doers, not the
settings: for voice that was `speak(`, websockets, `speechSynthesis`, TTS endpoints, realtime
clients, TwiML. Group call sites into user-visible experiences. One row each:

**experience · route/surface · audience · engine/provider · vocabulary (the allowed values) ·
value comes from (file:line) · user can change it where · entry UI (has a menu?)**

Audience is **consumer** (the person using AI Matrx for themselves) or **builder** (a value chosen
for something they build that speaks to other people — a podcast host, an agent's voice, a
workflow step). Never let one control serve both.

Done when: two independent methods (grep of doers + enumerate routes/clients) add no new row.

## 2. Trace every control to a reader

For each settings control in the area: the key it writes → grep every reader of that key in every
repo. No reader that runs (a reader nothing renders counts as none) = **dead control**.

Done when: every control row says `read by <file:line>` or `DEAD`.

## 3. Trace every consumer to its source

For each experience: which store it reads, what it falls back to, whether that fallback is a
hardcoded constant, and **when** it resolves (a one-shot read before the organization loads
silently takes the fallback — make it reactive).

## 4. Check the vocabulary before promising "one"

Can one value mean the same thing to every consumer? If the engines' vocabularies differ, there
is no single setting — one row per real vocabulary, stated honestly ("each engine has its own
voices"). Faking one value across engines is the defect this skill exists to stop.

## 5. The defect classes — check every one

| Class | Looks like |
|---|---|
| Dead control | saves a value nothing reads |
| Duplicate control | two screens edit one key, one without the good UI |
| Rival store | two keys for one idea; consumers split between them |
| Ignored setting | a consumer (often another repo/client) reads a constant instead |
| Lying copy | "used everywhere", "app-wide", a label naming the wrong scope |
| Hidden default | an override screen that does not show what applies when unset |
| No preview | a sensory choice (voice, sound, theme, font) you cannot hear/see first |
| No door | the place the setting acts has no path to the row that governs it |
| Consumer/builder blend | a personal preference rewriting what a builder made, or vice versa |
| Timing race | resolved once before org/session loads, so the fallback wins |

## 6. Fix shape

- **One home per capability** listing every instance — including a fixed one as "a choice of one",
  shown and, where possible, playable.
- Each choosable instance is a row on the platform knob ladder (`platform.feature_knob`, organization
  → user → device), rendered by the ONE editor (`KnobFieldControl`); give it a preview when sensory.
- **Every place it acts gets a door** (`SettingDoor` → the exact row). A lone icon gets the door in
  its menu, never a second icon.
- Delete dead controls; point their old links at the home. Correct every lying sentence.
- Resolve reactively; never swap a live session's value mid-session.
- Another client on the same engine reads the same knob (`platform.knob_snapshot`).

## 7. Verify from the seat

As the test account in the browser: change the value, hear/see it at each consumer, reload, follow
each door and land on the highlighted row. A picker that renders but never plays is not verified.

## Report

The census table (step 1), the control table (step 2), the defects found by class, and what changed
with file paths — then commit per repo and add the area to the sweep register.
