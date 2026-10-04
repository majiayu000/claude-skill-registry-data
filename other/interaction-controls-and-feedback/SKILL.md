---
name: interaction-controls-and-feedback
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P013
  - P037
  - P043
  - P044
  - P045
  - P047
  - P050
  - P055
  - P057
  - P064
  - P068
  - P071
  - P075
  - P076
  - P077
  - P078
  - P090
  - P101
  - P108
  - P109
  claims:
  - C00806
  - C01403
  - C01236
  - C01237
  - C00539
  - C00541
  - C01248
  - C01249
  - C01387
  - C01388
  - C01411
  - C01412
  - C01558
  - C01559
  - C00210
  - C00211
  - C00578
  - C00579
  - C00602
  - C00603
  - C00871
  - C00872
  - C01113
  - C01114
  - C01231
  - C01573
  - C01406
  - C01407
  - C01454
  - C01455
  authored_from_digest: c5492aab5f8dff591e7e9ec24fed8df88c97b1e9ee50d5703f2284a359c19bdd
---

# Interaction, Controls, and Feedback

Make interaction considerate and low-excise: clear affordances, rich feedback, reversible actions, direct manipulation.

## When this applies

- A form has a destructive action like Reset (P010).
- Deciding whether to report an event or ask before acting (P013).
- Deciding how to present actions on a screen (P037).
- Finding and removing unnecessary user work (P043).

## Procedure

Apply these principles to the situation under review; for each, name the user goal at stake and the trade-off the choice carries.

1. Prevent data-loss interruptions by replacing destructive confirmation or Save Changes dialogs with timely validation and Undo, so users can recover changes in the context where they made them. (P010)
2. Avoid stopping the proceedings for normalcy, confirmations, or high-excise reports; let software take a good-enough action, keep users informed with modeless feedback, and make actions adjustable or reversible with Undo. (P013)
3. Choose the right action affordance for the job: buttons and button groups for always-visible related actions, links for low-emphasis actions, hover tools for per-item mouse actions, and an Action Panel for discoverable, richly organized commands; keep pop-up menus short and never use drop-downs for actions. (P037)
4. Eliminate excise, the extra cognitive and physical work that serves the tools or outside agents rather than the user's goal: remove pure excise, do not weld on training wheels, judge visual excise from over-reliance on metaphor and ornament, and determine whether a function is excise by comparing it to persona goals, while neither removing excise merely for power users nor forcing them to pay the price of beginners' help. (P043)
5. Model Undo the least like its implementation and the most like the user's mental model, because Undo exists exclusively for humans, who make mistakes: treat everything the user does as valid and reasonable rather than as error, recognize that Undo's primary purpose is to support exploration (reassuring users and encouraging experimentation), and understand that it serves the necessary condition of trustworthiness rather than directly advancing a goal. (P044)
6. Implement document handling to match the unified model: save automatically on close without a confirmation dialog and at intervals or in the background during a session (keeping an optional manual save), provide an explicit Create a Copy that quietly makes an independently named copy in the same directory, let users rename in place by clicking the title-bar name and put new files somewhere findable like the Desktop, treat storage format as a document property accessed through Document Properties or Export rather than bundled into Save, provide an explicit Abandon Changes or Revert rather than using the file system as a surrogate for Undo, and drop the implementation-model File menu name in favor of the document type or Document. (P045)
7. Eliminate error messages where possible by making software immune to bad input, accepting and reconciling imperfect entries with modeless feedback, using bounded controls, and supplying known values automatically. (P047)
8. Support streamlined repetition by reducing repeated operations to as few actions as possible and offering mechanisms such as command history, macros, shortcuts, scripting, copy-paste, or find-and-replace where appropriate. (P050)
9. Provide Multilevel Undo in highly interactive apps by modeling actions as reversible operations on a 10-12+ item stack, making reversible anything that could be permanent while leaving transient/view states untracked, defining operations in the user's terms, and exposing them with Smart Menu Items. (P055)
10. Let users sort, rearrange, filter, and query data interactively (fast, iterative, contextual, and supporting nuanced conditions), because placing points next to each other reveals relationships and highlighting a subset keeps it in context. (P057)
11. Use overlays to surface many options only when needed: give them useful capacity, signal them and don't cover the field, auto-display only when clearly useful to most, and use a modal overlay when inputs need isolated attention—showing the results back on the form. (P064)
12. Make every functional and data element a concrete representation that responds to a specific earlier requirement, so that each aspect of the product traces back to a usage scenario or business goal; comprehensively catalog the data objects, expect one requirement to need several interface elements, and ground the design in realistic business, brand, technical, and customer requirements. (P068)
13. Keep users constantly informed with rich visual modeless feedback — information about the status and attributes of processes and objects that is rich, visual, and always displayed without a mode shift, the way a car dashboard is — to help users avoid mistakes and all but eliminate dialogs; recognize that such feedback is not for beginners because it takes work to discover and decode, so keep menus and dialogs as support and make any feedback used to warn of serious trouble extraordinarily clear; and prefer positive audible feedback (a success sound whose absence signals a problem) over negative beeps that act as insulting public alarms. (P071)
14. Present storage according to the user's single-document mental model rather than the file system's implementation model of two copies (one in memory, one on disk) that both belong to the application: hide the file system's existence, use a unified file model that treats the document as one thing and leaves disk/memory writing to the file system, and avoid the Save As trap that conflates naming and placing a file, cannot rename or relocate the current document, and can silently discard recent changes. (P075)
15. Give drag-and-drop precise, positive feedback: have each drop candidate visually indicate its receptivity while the drag cursor identifies the source object (never confusing the two by using the cursor to show drop candidacy), avoid negative feedback like the Not-Permitted symbol that is easily misread as a warning against releasing, drag a transparent outline or thumbnail so the object does not obscure a small target and the cursor hotspot stays visible, show an insertion target such as a caret bar when an object can drop between others, and give clear completion feedback so it is obvious the drop occurred. (P076)
16. Support precise object positioning and manipulation: dedicate a specific area such as a title bar to repositioning so the object's drag idiom stays free for other functions (with explicit pliancy hinting), offer a meta-key constrained drag that locks movement to a single axis, assist alignment with guides and dynamic smart guides and snapping, and use resize handles that double as selection indicators (vertex handles for polylines, Bezier handles for curves) — remembering that handles obscure the object they mark, making them poor permanent controls best replaced by frame or corner resizers for windows. (P077)
17. Make list controls efficient and manipulable: distinguish important items with graphic icons so users find them faster than scanning text, use earmarking (a check box per item) rather than disabling mutual exclusion for multiple selection in a scrollable list, support drag-and-drop from and within lists with auto-scroll, make items editable in place with a discoverable way to add a new entry (a perpetual Click to Add Entry row), and never scroll text horizontally because it hides the first letters of every line and destroys readability. (P078)
18. Avoid secondary actions where possible; when they must stay, reduce their prominence and visually distinguish them, and in wizards make forward a primary Continue and Back a secondary action. (P090)
19. Give controls clear affordance so an element looks or behaves like what it does, keep the visual language consistent (same icon or word means the same thing), and keep elements and text alignment stable from screen to screen. (P101)
20. Give every transaction a prominent, button-like final control at the end of the eye's travel near the last field, labeled with a specific verb, because a clear last step gives closure and a misplaced one causes hunting or abandonment. (P108)
21. Show a spinner or loading indicator whenever a response exceeds about one second (below 0.1s feels instant, 0.1-1s is tolerated), telling the user what is happening, how far along, and how to stop, without locking the rest of the UI. (P109)

## Principles applied

- **P010** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P013** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P037** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P043** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P044** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P045** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P047** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P050** (medium) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P055** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P057** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P064** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P068** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P071** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P075** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P076** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P077** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P078** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P090** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P101** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P108** (high) — grounded in claims/evidence and chunk anchors in `sources/`.
- **P109** (high) — grounded in claims/evidence and chunk anchors in `sources/`.

## Provenance

Grounded in principles P010, P013, P037, P043, P044, P045, P047, P050, P055, P057, P064, P068, P071, P075, P076, P077, P078, P090, P101, P108, P109, their backing claims and evidence records, and paragraph-level source anchors under `sources/anchors/`. Every cited id resolves into this package's distilled spine; see `provenance-ledger.md` and `reports/faithfulness-report.yaml`.
