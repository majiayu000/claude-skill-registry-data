---
name: fingerprint-optimizer
description: Automatically evaluates and optimizes engine configurations to minimize Fingerprint JS suspect scores and eliminate bot flags.
---

# Fingerprint Optimizer Skill

This skill empowers Hermes to automatically heal fingerprint decay. If anti-bot mechanisms evolve and the Golden Template begins failing, Hermes can trigger this skill to empirically determine a new optimal configuration.

## How it works

When invoked, the Fingerprint Optimizer:
1. Iterates over a matrix of configuration settings (e.g., `useHttpCloak: [true, false]`, `injectStealthJS: [true, false]`, differing Chrome versions).
2. Executes `npx tsx dump-fp.ts zendriver` or `npx tsx dump-fp.ts stealth --allow-trackers` for each permutation.
3. Parses the output in `fp-dump.json`, prioritizing:
   - Lowest `suspect_score`
   - Absence of `bot_type: browser_automation_studio` or any tampering flags.
4. Updates `app-config.json` with the optimal configuration values.

## Triggering

Run `/goal Optimize fingerprint configuration to achieve a suspect score of 0 on Zendriver`.
Or Hermes can autonomously decide to run this when success rates drop.

## Constraints
- **Golden Template Priority**: Stealth (Camoufox) is the primary baseline. Do not degrade Camoufox's strict tracking block (`block_webrtc: true`) in production just to satisfy a demo script.
- **A/B Testing**: Run multiple configurations iteratively. Do not execute parallel `dump-fp.ts` processes to avoid IP rate-limiting.
