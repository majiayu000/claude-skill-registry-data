---
name: use-zello
description: "Zello Work push-to-talk (PTT) SDK integration for the EnforcementMAPS Expo React Native application. Covers installation, Android native config, authentication lifecycle, voice PTT, rich messaging, channels/contacts, background services, FCM coexistence, emergency dispatch, and troubleshooting. Use this skill whenever the user mentions Zello, push-to-talk, PTT, walkie-talkie, radio, voice messaging, officer communications, dispatch radio, emergency voice, or any work involving the src/features/zello/ module — even if they don't explicitly say 'Zello'."
version: 1.0.0
license: MIT
---

# Zello PTT Skills

You now have access to the full suite of Zello Work SDK integration skills for EnforcementMAPS. Read `./zello-skills-orchestrator.md` to determine which sub-skills apply to the current task, then load and apply them accordingly.

## Quick Reference

| Goal | Skill |
|------|-------|
| Install SDK, configure Android, set up Firebase | zello-setup |
| Wire Zello auth into AuthContext, ZelloProvider | zello-auth |
| Build PTT button, voice send/receive, playback | zello-voice |
| Send/receive text, image, location, alert messages | zello-messaging |
| Manage channels, contacts, groups, presence | zello-channels |
| Background service, FCM push, battery optimisation | zello-background |
| Emergency mode, Code21 dual-trigger, dispatch calls | zello-emergency |
| Fix build errors, debug runtime issues | zello-troubleshooting |

## Reference Material (load on demand)

| Reference | When to load |
|-----------|-------------|
| `references/api-reference.md` | Looking up specific SDK methods or signatures |
| `references/events-catalog.md` | Wiring event listeners or debugging event flow |
| `references/security-networking.md` | Firewall rules, encryption details, credential storage |

## Assets

| Asset | Purpose |
|-------|---------|
| `assets/feature-scaffold.md` | Template for `src/features/zello/` directory structure |

## Project Context

- **App:** EnforcementMAPS (CIVIC MAPS patrol officer platform)
- **Stack:** Expo 54, React Native 0.81, pnpm, TypeScript 5.9
- **SDK:** `@zelloptt/react-native-zello-sdk@2.0.1`
- **Build:** EAS managed workflow (no manual android/ edits)
- **Docs:** Full integration documentation at `docs/dev/zello/`

Consult `./zello-skills-orchestrator.md` for routing rules and multi-skill combinations.
