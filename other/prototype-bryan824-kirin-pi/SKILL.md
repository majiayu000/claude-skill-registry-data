---
name: prototype
description: "When a design question needs runnable evidence — choose a useful experimental surface, protect real data, and let observed behavior inform the decision."
---

# Prototype

Build the cheapest experiment that can answer the question for its recipient,
not a compulsory TUI, web page or production scaffold.

- State the question, useful observations and allowed scope before coding. A
  logic/state question usually needs [LOGIC.md](LOGIC.md); a visual/interaction
  comparison needs [UI.md](UI.md). Choose a script, terminal, offline artifact or
  native preview according to the question and recipient. Ask when that choice
  is consequential, rather than guessing from backend/frontend file location.
- Use existing language, tools and preview seams. Keep experimental code clearly
  disposable and isolated from production routing and mutations. Start with
  in-memory or approved fixture data; persistence experiments need an explicitly
  isolated data boundary and recovery path.
- Keep relevant state visible, scenarios resettable and results reproducible.
  Leave a small decision check for nontrivial logic. Throwaway status does not
  waive input validation, failure handling, accessibility or data protection.
- Present observed evidence separately from assumptions and unrun checks. A human
  preference remains the human's decision; if the recipient has not tried the
  artifact, do not invent their verdict.

Deliver: question, artifact/run instructions, scenarios, evidence and decision or
remaining uncertainty in the task's existing working notes. Absorb only validated logic
or the selected direction under production standards and authorization. Remove
owned throwaway work only within cleanup authority; preserve user edits and
records. No new decision diary.
