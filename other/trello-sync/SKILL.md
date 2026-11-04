---
name: trello-sync
description: Align the Trello board of EasyTask with finished work - comment with the version, tick checklists, move cards to the right list, add new bugs and ideas. Use after a release is published, when the user says "allinea Trello" / "segna su Trello", or to record a bug or idea found while working.
---

# Trello sync (EasyTask)

The user writes in Italian: answer and write the cards in Italian. Board: **EasyTask**. Load the Trello tools first (`ToolSearch` with `select:mcp__Trello__trelloSearch,mcp__Trello__trelloReadCard,mcp__Trello__trelloReadList,mcp__Trello__trelloWriteCard`; add `trelloWriteChecklist` to tick items). Card ids are ARIs: get them from a search or a read, never from the URL. `trelloReadCard` with `action: "get"` takes `cardIdOrUrl` (not `cardId`); the write tools take `cardId`.

## Lists
- **To do**: decided work, not started.
- **Idee / rimandate**: ideas and postponed work (the cards of a feature wait here until it ships).
- **Bugs**: open bugs.
- **Done**: finished features and work.
- **Fixed bugs**: bugs that were fixed and released.
- **Questions**: open questions for the user.
Read the lists with `trelloReadList` (`list_by_board`) if a name looks different: do not guess ids.

## Rules
- Writing to Trello is outward-facing: confirm with the user before changing cards, unless they asked for it in this very message ("segna su Trello", "allinea le card").
- Move a card to **Done** / **Fixed bugs** only when the release that ships it is **published** and verified, never when the PR merges. Say the version in the comment.
- Do not touch cards you were not asked about. Read a card (`trelloReadCard`) before editing: its description can hold decisions of the user that must stay.
- Keep decisions: when a card says "DECISO DALL'UTENTE (data): ...", leave it as it is and add below.

## Close a feature after a release
1. Find the cards (`trelloSearch`, `search_cards`, with words of the feature) and read each one.
2. Comment on each: `Rilasciata nella X.Y.Z (data): <cosa è stato fatto, in una o due frasi>`. Mention what was left out on purpose.
3. Tick the checklist items that are done.
4. Move the card: features to **Done**, bugs to **Fixed bugs**.
5. Re-read the umbrella cards that point to the feature (for example the UI review card "Revisione UI ...") and update the references that are now old.
6. Report in a short list: card, old list, new list.

## Record a new bug or idea
- Bug: create the card in **Bugs**. Title = the symptom in the user's words. Description: where it was found (date, version, OS), the steps or the failing test, what it should do, whether it also happens on `master`, and what to check first.
- Idea or postponed work: **Idee / rimandate**, with the reason it was postponed and a rough estimate if known.
- Link related cards by number in the description (for example "vedi card 119").
