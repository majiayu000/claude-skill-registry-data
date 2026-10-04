---
name: adr
description: Create a new Architecture Decision Record (MADR) in docs/adr, or supersede an existing one, and update the ADR index. Use when a change introduces or alters an architectural decision, or when the user asks to record a decision.
argument-hint: "<decision title>"
---

# Create an ADR

1. Read `docs/adr/README.md` and the ADRs related to the topic. If an accepted ADR already covers it, decide with the user whether this is a clarification (no ADR needed) or a change (a new ADR that supersedes the old one).
   - Before the first stable release (1.0), a change may be made in place instead ([ADR-0001](../../../docs/adr/0001-record-architecture-decisions.md)): edit the accepted ADR, add a dated note under **More Information** saying what changed and why, and bump its `date`. From 1.0 on, always write a new ADR.
2. Take the next free number `NNNN` (4 digits; never reuse a number). File name: `docs/adr/NNNN-kebab-case-title.md`.
3. Copy `docs/adr/template.md`. Fill in:
   - front matter: `status: proposed`, today's date, `decision-makers: milten89`
   - context and problem statement (a question), decision drivers, at least two considered options, the outcome with honest consequences (good and bad), and a **Confirmation** section saying how compliance is checked (a test, an analyzer, a CI step or a review rule).
4. Don't invent the maintainer's preferences. If the decision isn't clear from the conversation, ask before writing the outcome.
5. If it supersedes an ADR: in the old file set `status: superseded by ADR-NNNN` and add a link. Don't change its content otherwise.
6. Add a row to the table in `docs/adr/README.md`.
7. If the decision changes rules summarized in `CLAUDE.md`, update `CLAUDE.md` in the same change, and add follow-up work to `docs/BACKLOG.md`.
8. Write it in English (ADR-0009).
