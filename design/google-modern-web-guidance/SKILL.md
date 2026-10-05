---
name: google-modern-web-guidance
description: "Trigger: frontend, React, TypeScript, CSS, HTML, accessibility, responsive UI, web performance. Fetch current Google Modern Web Guidance before client-side work."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Run this skill first for every HTML, CSS, React or browser JavaScript change.

# Hard Rules
- Do not implement client-side behavior from memory when current platform guidance is available.
- Search before writing code; retrieve the most relevant result before implementation.
- Use Google Modern Web Guidance through `npx`; it is not an MCP.
- Follow the documented fallback guidance for features that are not Baseline Widely Available.

# Execution Steps
1. Run `npx -y modern-web-guidance@latest search "<action-oriented task>" --skill-version 2026_05_16-c5e78707`.
2. Retrieve the selected guidance: `npx -y modern-web-guidance@latest retrieve "<guide-id>"`.
3. Apply it to the React/Vite implementation and test the relevant responsive/accessibility/performance behavior.
4. Cite the guide ID in the PR or Linear evidence when it materially changed the implementation.

# Output Contract
Return searched guide IDs, the applied decision, browser/fallback impact and validation evidence.
