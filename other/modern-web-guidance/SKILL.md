---
name: modern-web-guidance
description: "Modern HTML/CSS/Web APIs, Baseline compatibility, progressive enhancement, accessibility and performance. Modern web, tarayıcı uyumluluğu, bu CSS destekleniyor mu."
license: Apache-2.0
---

# Modern web guidance

Consult the bundled Google Chrome guides when choosing a modern browser API, CSS capability, accessibility pattern or performance technique. Routine text edits and already-established patterns do not require this workflow.

Search the local `guides/` directory by the actual feature. Open only the relevant one or two guides. The offline snapshot is pinned in [SOURCE.md](SOURCE.md); check current primary documentation if compatibility or API behavior is decisive. Do not run a package manager or install a CLI merely to read these bundled files.

Use the project's explicit browser targets. Without targets, prefer broadly supported behavior and progressive enhancement. Check Baseline, feature availability, accessibility and fallbacks for the actual target browsers; a guide's existence is not evidence of universal support.

Adapt framework-agnostic guidance to the existing project. Check rendered behavior and an appropriate fallback when materially relevant. Do not add dependencies, rewrite unrelated components or persist project-wide policies unless the task warrants it.
