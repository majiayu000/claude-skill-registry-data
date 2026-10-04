---
name: qa
description: Audits a feature that has shipped to a dev or staging server against the plan of record — spec entries and the Figma design. One mode stops once the checklist is drawn; the other clicks through the browser and files a defect report. Defects are written as reproduction steps, expected, actual, and evidence (request results, screens) so they can be handed to engineering as they are. Triggers - "/fig:qa", "QA this", "check what is on the dev server", "file the defects", "QA 해줘", "개발서버 확인해줘", "결함 정리해줘".
allowed-tools: AskUserQuestion, mcp__claude_ai_Notion__notion-fetch, mcp__claude_ai_Notion__notion-search, mcp__claude_ai_Notion__notion-query-data-sources, mcp__claude_ai_Slack__slack_read_thread, mcp__claude_ai_Slack__slack_read_channel, mcp__plugin_figma_figma__get_screenshot, mcp__plugin_figma_figma__get_metadata, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__browser_batch, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__find, mcp__claude-in-chrome__read_page, mcp__claude-in-chrome__get_page_text, mcp__claude-in-chrome__read_console_messages, mcp__claude-in-chrome__read_network_requests
---

# qa — baseline-referenced QA (checklist → verification → defect report)

Once a feature is on a server, **compares it against the plan of record**, finds what diverged, and hands it over in a shape engineering can act on directly.

**The premise**: no verdict without a baseline. Not "this looks wrong" but **"this breaks rule X in document Y"**. An item with no baseline is not a defect — it is `needs confirmation`.

## When to invoke

- A dev or staging deploy has been announced and the behaviour needs looking at
- A reported defect needs reproducing and confirming
- A pre-release sweep for anything the plan called for and the build is missing
- **A checklist only**, with no verification (`baseline` mode)

## When NOT to invoke

- Auditing the design's own structure and naming → `/fig:lint`
- Carrying design-versus-code differences back into the file → `/fig:code`
- Reviewing a document or a message → not this skill
- Filing defects as tickets → whatever ticket tool you use. This skill stops at the report

## Inputs

- `source` (required): where the request came from — a thread link, a page, or the request as spoken
- `target` (required): the screen or feature under verification
- `mode` (optional): `baseline` (stop at the checklist) / `full` (verify and report). Omitted, it asks
- `env` (optional): the address, the account scope, the data scope to test against (branch, org, and so on). Given a name alone, the address is looked up in `qa.environments`

## Modes

    baseline  Steps 1–3 only. Emits the checklist and stops — for when someone else will run it,
              or when the scope needs agreeing before verification starts
    full      Steps 1–7. Verifies through the browser and files the defect report

Even in `full`, the step-3 checklist is **shown before verification begins**. Start clicking without agreeing on what will be looked at and the scope drifts.

---

## 1. Settle the target (reading, no confirmation needed)

Read the source and pull out the following. Do not guess.

- What shipped / where this round's scope ends
- **Defects already reported** — if there are any, they reproduce first
- Anything the requester specifically asked to have checked
- Exclusions (scope they said not to look at)

Whatever the source does not say, leave as `TBD`, and only ask about the parts that would change the verification result.

## 2. Collect the baseline (reading)

Gather the documents the verdicts will rest on. **Internal assets first.** Where to look is set by `qa.baseline`, and any entry that is `null` is skipped.

| Source | What to pull |
|---|---|
| Spec feature and policy entries | Detailed behaviour (Given/When/Then), states and cases, rules and exceptions |
| The design | Screen composition, state variants, copy |
| Existing tickets | Past decisions and reversals, undecided items |
| The request itself | What is newly asked for in this round |

- Pull features and policies **exhaustively, by domain**. Look at only a handful and verification items leak out.
- Read `archived` and `deprecated` entries too — **a deprecated feature still present on screen** is a common defect.
- An entry whose status is not `confirmed` may still serve as a baseline, but the report marks it `baseline unconfirmed`.

## 3. Build the checklist

Group by screen and by feature, and write each item as **a sentence that clicking will prove true or false**.

    ① [screen name]
       □ [behaviour] — baseline: spec detailed behaviour
       □ [state] — empty / loading / error / permission
       □ [rule] — value constraints, inheritance, linkage rules
       ← mark reported defects in place so it is visible that they are reproduction targets

Do not let any screen miss these four kinds.

- **Happy path** — exactly as the behaviour table has it
- **States and cases** — empty, loading, error, permission, pagination
- **Rules and exceptions** — inheritance, pinning, linkage: the "where does this value come from" rules
- **Round trip** — after saving or editing, does it land correctly in the list and on other screens

Items that cannot be seen for lack of an account or data are separated out here in advance as `will not verify`.

**`baseline` mode ends here.**

## 4. Prepare access

- Confirm the address and the data scope. Do not touch scope they said to leave alone.
- **Never enter login or authentication details on the user's behalf.** Ask for the screen to be brought up, then take over.
- Before verification starts, record the current state (total counts, the values of the target items) — it is the reference for before-and-after comparison and for restoring.

## 5. Run the verification

Work down the checklist in order. Batch clicks, input, waits, and captures together to cut round trips.

### Data handling

- **Do not create or delete.** Go as far as the modal appearing, the required-field guard, and cancel. Even where `qa.allow_write` is true, do it only when genuinely necessary, and only after confirming.
- If a value was changed, **restore it before saving**. For verification that must go through a save, confirm there is a path back first.
- Any change that could not be restored is recorded on the spot and carried into the report.

### Ways of catching what gets missed

These have caught things repeatedly in practice. Run them whether or not they are on the checklist.

| Check | How | What it catches |
|---|---|---|
| **First action after entry** | Refresh → switch tab, filter, or search immediately, with no other interaction | The class of bug where the first click is swallowed whole. It behaves from the second onward, so manual QA keeps missing it |
| **Cross-path comparison** | Look at the same data through a different route (filter vs search vs detail) | Values or images going blank on one retrieval path only |
| **Count comparison** | Compare totals before and after a save or a toggle | Items lost or duplicated in the list |
| **Round-trip reflection** | Change it in the detail view, come back to the list, check | The class where the save works but the list never picks it up |
| **Failure evidence** | When an error appears, capture the network request and the console alongside | Which request failed with which code — the ground for handing it to engineering |
| **Cross-list consistency** | Compare the lists of two screens that handle the same items | Items present on one side only; values selectable elsewhere that the managing list does not have |
| **Input guards** | Actually type into a value that is supposed to be fixed | A no-edit rule that the screen does not enforce |

### Reproduction and verdicts

- **One failure is not a confirmed defect.** Reproduce at least twice, varying the conditions.
- If it does not reproduce, write it up as `intermittent` with the conditions it was observed under. Do not delete it.
- For anything that might be the data's fault (an unregistered value and the like), check the same item through another path to **separate an implementation problem from a data problem**.
- A difference with no baseline behind it is not a defect — it is `needs confirmation`. When it disagrees with the design or the document, ask which of them is current first.
- Watch for false positives: state-dependent checks are confirmed **only after actually producing that state** (an unsaved-changes warning, for instance, is verified by leaving with the value changed).

### Capture every issue as it happens

Every defect and every `needs confirmation` item gets screenshots **taken at the moment it is observed**, saved to disk — not reconstructed afterwards. Going back to re-capture means touching the data and the environment a second time, and some states (a locked operating mode, a value that has since been restored) cannot be produced again without asking.

- **One capture per reproduction step that shows something** — the starting screen, the input, the result. A before-and-after pair is the minimum for anything that changes a value.
- **Crop to the part that matters** (zoom on the region) and keep one wider shot so the reader can tell where on the page it is.
- Name the files `{item number}-{step}-{what it shows}` so the report can point at them and they sort in reading order.
- Where the evidence is a request result rather than something visible, capture the screen it came from anyway, and put the request on the evidence line.
- Items verified good get one capture each at most — enough to show the state was reached, not a gallery.

## 6. The defect report

Keep **what was reported and what was newly found apart**. The requester looks first at what became of the item they raised.

    [reported]  reproduced or not, plus what was observed, for each
    [new]       by severity

Severity is cut by the size of the consequence. Labels come from `qa.severity` — every org calls these something different, so follow the wording in their bug tracker exactly.

    Level 1   data loss, unrecoverable state, work stopped
    Level 2   core behaviour impossible, baseline violated
    Level 3   some information missing, lists disagreeing
    Level 4   copy, icons, legibility

### Match the fields to the issue template

Defects end up filed as issues. **Write them into the issue template's fields one-to-one from the start**, so moving them across fills the body as it is. The fields come from `qa.report_fields`; with no setting, use the ones below.

Whatever is common to the whole round goes at the head of the report **once** — not repeated per defect.

    project / version, build
    environment — server (dev, staging, production) · account permissions · data scope
    baseline documents — feature and policy entries · design · spec

One defect:

    {number} · {summary — one line, a noun phrase}
    · Severity: one of `qa.severity`
    · Frequency: one of `qa.frequency`
    · Reproduce: 1) … 2) … 3) …
    · Expected: … (baseline: which document, which part)
    · Actual: …
    · Evidence: captures (file names, in step order) · request results · count changes

Do not drop frequency — leaving an intermittent defect to read as "always" burns engineering time on reproduction. Write the verdict in plan language, and keep engineering detail such as request results and code **on the evidence line only**.

## 7. What the closing must always carry

- **Verified good** — listing what turned out fine is what makes coverage visible
- **Not verified**, with the reason (no account, out of scope, no data)
- **Changes left behind** — data that could not be restored, and how it happened

Without these three the report reads as "I looked at everything". Writing down what was not looked at is half of a report.

---

## Delivering the report

Where the report goes is **asked and settled** (in the response only / recorded on the ticket / drafted as a reply). External writes happen only after preview → "go".

**The person reading the report sees the captures, not a list of file names.** Walk each issue step by step — what was done, the capture, what it shows — in plain language before any engineering detail, and send the images themselves (attach them, or use whatever file-sending tool the session has). Where the report is going onto a ticket, say which captures go with which item; trackers that cannot take an image by API need them attached by hand, so say so rather than leaving a broken link.
