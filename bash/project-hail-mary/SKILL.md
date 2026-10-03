---
name: project-hail-mary
description: Build, scaffold, troubleshoot, or product-shape a macOS rescue launcher, focus ritual, or last-minute shipping workflow that can start a hype song, open critical apps and docs, start a countdown, and copy a heads-down status update. Use when Codex needs to turn "Project Hail Mary", "panic mode", or "play Sign of the Times and open everything I need" into a realistic menu bar app, shortcut, script, or launch sequence without inventing unsupported music or messaging APIs.
---

# Project Hail Mary

Use this skill when the user wants a rescue button for crunch mode, deep focus, or a deadline save.

Default product shape: a lightweight macOS launcher that opens the user's music and work surfaces fast, keeps the countdown visible, and leaves a clear next-step checklist instead of vague motivation.

## Quick Start

1. Choose the lane: `menu-bar-app`, `shortcut-pack`, `one-shot-script`, `dashboard`, or `support-only`.
2. Run `python3 scripts/hail_mary_brief.py --goal "<user request>" --anthem "Sign of the Times"` to normalize the request.
3. If the user wants something runnable right away, use `python3 scripts/hail_mary_launch.py --anthem "Sign of the Times" --service spotify --app "Visual Studio Code" --url "https://github.com"`.
4. Default Hail Mary sequence:
   - open a hype track or playlist in a real music surface
   - open the repo, docs, notes, call, or dashboard tabs the user actually needs
   - start a visible countdown or show the finish time
   - copy a heads-down status update into the clipboard instead of auto-sending it
   - make the next action obvious
5. Be explicit about capability boundaries:
   - do not promise silent playback control of paid music services unless the local app or browser flow supports it
   - keep sign-in inside Apple Music, Spotify, YouTube, GitHub, Slack, Notion, or the user's browser
   - prefer launchers, timers, and copied communication drafts over hidden background control
6. If a real app scaffold is requested, prefer a SwiftUI menu bar app first and add richer flows only if the user asks.

## Workflow

### Choose The Lane

- `menu-bar-app`: build a persistent Mac rescue button with an anthem, checklist, countdown, and links into work surfaces.
- `shortcut-pack`: use Shortcuts, shell scripts, AppleScript, or browser launchers when the user wants something quick without a full app.
- `one-shot-script`: fire off the anthem, open the right tools, copy the status line, and print a finish time in one local command.
- `dashboard`: build a single-window launch board with sections like music, comms, critical links, and blockers.
- `support-only`: explain the fastest realistic path without building anything.

### Build The Brief

Run the brief script first. Useful commands:

```bash
python3 scripts/hail_mary_brief.py --goal "make a panic-mode Mac menu bar app that opens my repo, Linear, and docs"
python3 scripts/hail_mary_brief.py --goal "play Sign of the Times and open everything I need for a launch push" --anthem "Sign of the Times"
python3 scripts/hail_mary_brief.py --goal "give me a one-shot rescue script for a 45 minute deadline" --lane one-shot-script --focus shipping
```

The brief should capture:

- anthem or soundtrack preference
- launch lane and shell
- core work surfaces: repo, ticket board, docs, notes, call, dashboard
- timebox length or target finish time
- whether the user wants a copied status update or a visible checklist
- fallback path if direct service control is not realistic

### Music Kickoff Guidance

- Default to real user-owned music surfaces:
  - Apple Music search or playlist handoff
  - Spotify search or playlist handoff
  - YouTube search or video handoff
- If the user explicitly wants a track like `Sign of the Times`, open the search or canonical result page unless the exact deep link is already available.
- Do not bundle copyrighted audio into the repo.
- If direct playback requires a signed-in app or browser session, say so and optimize time-to-music instead of pretending playback is guaranteed.
- If the user wants a custom ritual sound, let them swap the anthem with a local file, playlist URL, or app deeplink.

### Countdown And Focus Guidance

- For quick flows, a printed finish time or in-app timer is often enough.
- If the user wants a system notification, use a local notification or reminder, not a fake background scheduler.
- Treat Focus or Do Not Disturb changes as opt-in. Do not silently promise system-wide mode changes unless the chosen path actually supports them on that Mac.

### Communication Guidance

- Copy a short status line to the clipboard rather than auto-posting into chat by default.
- Good copied messages:
  - `Heads down for 45 minutes. Shipping the last blocker now.`
  - `Running a Hail Mary pass. I will post status by 6:30 PM.`
- If the user wants Slack, Telegram, or another chat action, open the surface or prefill text only when that path is clearly supported.

### Security And Privacy

- Keep logins and tokens in the user's own apps or signed-in browser profile.
- Never frame messaging or music-service automation as acceptable on accounts the user does not control.
- Prefer visible user-owned surfaces over hidden automation when secrets or account state are involved.

### Implementation Preferences

- Start with the smallest reliable flow that gets the ritual live.
- Prefer:
  - browser or app handoff
  - local launch script
  - menu bar wrapper
  - deeper automation last
- If a browser flow matters, pair this skill with [$playwright](/Users/arnav/.codex/skills/playwright/SKILL.md).
- If the user wants spoken prompts or countdown audio, pair this skill with [$speech](/Users/arnav/.codex/skills/speech/SKILL.md).

## Required Deliverables

- A short implementation brief with the chosen lane.
- Clear statement of what is directly automatable versus what hands off into the user's signed-in tools.
- A concrete Mac surface:
  - menu bar app
  - one-shot script
  - shortcut pack
  - dashboard
  - support steps
- The fastest path to a real Hail Mary ritual the user can trigger again.

## Resources

- `scripts/hail_mary_brief.py`: normalizes the user's request into a build brief.
- `scripts/hail_mary_launch.py`: small local launcher for music, work surfaces, countdown text, clipboard status, and a notification.
- `references/supported-surfaces.md`: guardrails for music handoff, timers, and communication flows on macOS.
