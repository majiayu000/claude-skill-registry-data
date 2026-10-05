---
name: ai-trust-builders
description: >-
  Use when designing AI product trust, privacy, or honesty UX — cloud
  disclosure, voice/mic consent, transcript retention, memory ownership, AI
  labeling, caveats, or audit footprints. Trigger on disclose cloud, recording
  consent, watermark, incognito, or data-ownership settings.
---

# AI Trust Builders — honesty & privacy UX

Trust builders make the system **legible**: what is AI, what left the machine,
what was retained, and how to refuse. Complementary to governors (control of
*actions*) and untrusted framing (control of *prompt injection*).

Pattern catalog: [references/patterns.md](references/patterns.md).
Adapted from tommyjepsen/awesome-ux-skills `ai-trust-builders`.

## When to use

- Cloud providers, voice enrollment, camera, transcript retention, memory,
  settings / privacy copy.
- Auditing whether a feature is honest about where data goes.
- **Not** for: scanner/framing implementation, cost metering polarity alone, or
  HITL confirm shapes (`ai-governors`).

## Seam → pattern map

| Seam | Prefer | Notes |
|---|---|---|
| Cloud model / failover | Disclosure + Caveat + Footprints | Say when persona/recall leaves the box |
| Transcript / dreaming to cloud | Disclosure + Consent + Ownership + Footprints | Privacy event, not a footnote |
| Voice mic / enroll | Consent (+ Disclosure) | Recording indicator; gate mode ≠ consent |
| Camera / vision | Consent + Disclosure + Caveat | No silent always-on claim |
| Memory / durable facts | Ownership + Footprints + Caveat | Owner can see/delete; sources labeled |
| Capability / help copy | Disclosure (honest cannot-do) | False capability = bug |
| Chat / history | Footprints + Caveat | Name model/provider when non-obvious |
| Generated media | Watermark / attribution | Don't pretend human-authored |

## Seven patterns (short)

1. **Caveat** — decision-time "may be wrong"; never the only safety net.
2. **Consent** — opt-in for record/enroll/train; separate those acts.
3. **Data Ownership** — retention vs training; default privacy-protective.
4. **Disclosure** — label AI actor and cloud vs local.
5. **Footprints** — inspectable trail of what was sent/stored/applied.
6. **Incognito / memory-off** — session without durable write when stakes are high.
7. **Watermark** — mark AI-generated media when mixed with human content.

## Honesty rules

- A **false capability line** is a bug — copy must match mechanism and flags.
- **Merged ≠ live** — disclosure about a path is inert until deployed.
- **Degrade path** must not drop disclosure.
- Caveats habituate; pair with Footprints/Citations for high-stakes acts.
- Consent buried in env comments is not consent UX.

## Design checklist

- [ ] Owner can answer: local or cloud? retained? used for training?
- [ ] Voice/camera active state is perceptible without reading logs.
- [ ] Cloud paths name the provider class (not only "AI").
- [ ] Unavailable/degraded search shows notice, not empty success.
- [ ] Settings expose ownership controls or an explicit "we don't train on you".

## Output format

1. **Trust risk** — what could be misunderstood.
2. **Patterns** — 1–3.
3. **Surface** — exact UI/copy/flag.
4. **Pair with** — governor if an irreversible act is involved.

## Cross-references

- `ai-governors` — oversight of acts
- `ai-wayfinders` — onboarding without over-claiming
- `ui-fix-observe-first` — measure disclosure UI for contrast/focus
