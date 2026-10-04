---
name: filemaker-xml
description: >
  Use this skill whenever the user wants to work with FileMaker script XML or custom function XML.
  This includes: generating FileMaker XML from a description, pseudocode, or
  script steps; analysing or reviewing existing FileMaker XML for errors or
  silent-failure risks; converting scripts between formats; or any task where
  the output must be paste-ready XML for the FileMaker Script Workspace or Manage Custom Functions dialog.
  Trigger any time the user mentions FileMaker scripts, fmxmlsnippet, Set
  Variable XML, script step XML, custom function XML, or asks to produce XML that can be pasted
  into FileMaker. Always use this skill — do not attempt FileMaker XML tasks
  from memory alone, as the format has undocumented paste-handler rules that
  cause silent failures without this reference.
---

# FileMaker Script & Custom Function XML Skill

## Overview

This skill enables Claude to correctly **analyse** and **generate** FileMaker
Script Workspace XML — the `fmxmlsnippet type="FMObjectList"` format that
FileMaker accepts via clipboard paste.

The format has a lenient XML parser but a strict paste handler. Structural
deviations that look fine as XML can cause steps to paste with silently missing
data (e.g. Set Variable pastes with no variable name). The reference files in
this skill are the authoritative reverse-engineered spec for what the paste
handler actually accepts.

---

## Mandatory reading — progressive loading

The specification (v2.0) is split so a task loads only the sections it
needs. The rules are:

1. **Always read `references/core.md` first.** Not optional. It contains
   the paste format requirements, common conventions, the Set Variable
   canonical structure, and the silent-failure modes that apply to every
   step. Skipping it reintroduces the from-memory failure mode this
   skill exists to prevent.
2. **Always read `references/steps-control.md`.** Control steps (If,
   Loop, Perform Script, Exit Script, Comment, transactions) appear in
   virtually every script.
3. **Then read only the step category files containing the steps the
   task needs**, using the routing index below. When reviewing XML someone else
   produced, route by the `name` attributes on the `<Step>` elements
   in the snippet.
4. Custom function tasks: read `references/custom-functions.md`
   (plus core.md — the wrapper differs but the conventions apply).
5. MBS or other plugin steps: read `references/steps-plugin.md`.
6. `references/worked-example.md` is optional background, not required
   for any task.

When reviewing XML someone else produced, route by the step `id`
attributes present in the snippet.

Do not rely on training data for FileMaker XML structure — always consult
the reference files. The format contains non-obvious quirks (e.g. a
trailing space in the `Configure RAG Account ` step name) that only
appear in the spec.

---

## Routing index

Set Variable (141) is documented in `core.md` §3 (its canonical
structure is a silent-failure trap, so it lives with the core rules).

**`steps-control.md`** — Allow User Abort, Comment, Commit Transaction, Else, Else If, End If, End Loop, Exit Loop If, Exit Script, Halt Script, If, Install OnTimer Script, Loop, Open Transaction, Pause/Resume Script, Perform Script, Perform Script on Server, Perform Script on Server with Callback, Revert Transaction, Set Error Capture, Set Error Logging, Set Layout Object Animation, Set Revert Transaction on Error, Set Script Triggers, Set Variable, Set Variable by Name, Trigger Claris Connect Flow

**`steps-navigation-editing.md`** — Clear, Close Popover, Copy, Cut, Enter Browse Mode, Enter Find Mode, Enter Preview Mode, Go to Field, Go to Layout, Go to List of Records, Go to Next Field, Go to Object, Go to Portal Row, Go to Previous Field, Go to Record/Request/Page, Go to Related Record, Paste, Perform Find/Replace, Select All, Set Selection, Undo/Redo

**`steps-fields-records.md`** — Commit Records/Requests, Constrain Found Set, Copy All Records/Requests, Copy Record/Request, Delete All Records, Delete Portal Row, Delete Record/Request, Duplicate Record/Request, Export Field Contents, Export Records, Extend Found Set, Find Matching Records, Import Records, Insert Audio/Video, Insert Calculated Result, Insert Current Date, Insert Current Time, Insert Current User Name, Insert File, Insert from Device, Insert from Index, Insert from Last Visited, Insert from URL, Insert PDF, Insert Picture, Insert Text, Modify Last Find, New Record/Request, Omit Multiple Records, Omit Record, Open Record/Request, Perform Find, Perform Quick Find, Relookup Field Contents, Replace Field Contents, Replace Field Contents by Name, Revert Record/Request, Save Records as Excel, Save Records as JSONL, Save Records as PDF, Save Records as Snapshot Link, Set Field, Set Field By Name, Set Next Serial Value, Show All Records, Show Omitted Only, Sort Records, Sort Records by Field, Truncate Table, Unsort Records

**`steps-windows-files.md`** — Adjust Window, Arrange All Windows, Close Data File, Close File, Close Window, Convert File, Create Data File, Delete File, Freeze Window, Get Data File Position, Get File Exists, Get File Size, Move/Resize Window, New File, New Window, Open Data File, Open File, Print, Print Setup, Read from Data File, Recover File, Refresh Window, Rename File, Save a Copy as, Save a Copy as XML, Scroll Window, Select Window, Set Data File Position, Set Multi-User, Set Use System Formats, Set Window Title, Set Zoom Level, Show/Hide Menubar, Show/Hide Text Ruler, Show/Hide Toolbars, View As, Write to Data File

**`steps-accounts-ai-misc.md`** — Add Account, Allow Formatting Bar, AVPlayer Play, AVPlayer Set Options, AVPlayer Set Playback State, Beep, Change Password, Check Found Set, Check Record, Check Selection, Configure AI Account, Configure Local Notification, Configure Machine Learning Model, Configure NFC Reading, Configure Persistent Data, Configure Prompt Template, Configure RAG Account, Configure Region Monitor Script, Configure Regression Model, Correct Word, Delete Account, Dial Phone, Edit User Dictionary, Enable Account, Enable Touch Keyboard, Execute FileMaker Data API, Execute SQL, Execute URL, Exit Application, Fine-Tune Model, Flush Cache to Disk, Flush Web Viewer Cookies, Generate Response from Model, Get Folder Path, Insert Embedding, Insert Embedding in Found Set, Insert Image Caption, Insert Image Captions in Found Set, Install Menu Set, Install Plug-In File, Open URL, Perform AppleScript, Perform Find by Natural Language, Perform JavaScript in Web Viewer, Perform RAG Action, Perform Semantic Find, Perform SQL Query by Natural Language, Re-Login, Refresh Object, Refresh Portal, Reset Account Password, Save a Copy as Add-on Package, Select Dictionaries, Send DDE Execute, Send Event, Send Mail, Set AI Call Logging, Set Dictionary, Set Session Identifier, Set Web Viewer, Show Custom Dialog, Speak, Spelling Options, Validate Scripts

**`steps-pdf.md`** — Append PDF, Cancel PDF, Close PDF, Create PDF, Open PDF, Print PDF

**`steps-plugin.md`** — all MBS and other plugin steps (External step structure, §9)

**`custom-functions.md`** — custom function definitions (§11): skeleton, attributes, parameters, recursion

---

## Task: Analysing existing XML

When the user provides FileMaker XML to review:

1. Read `core.md`, then the category files for the step ids present.
2. Check against the silent-failure modes (core.md §7):
   - **7.1** — `Name` element emitted as single-letter tag (Set Variable loses variable name)
   - **7.2** — compact/single-line form instead of expanded child form
   - **7.3** — Install OnTimer Script interval bound to wrong slot (interval emitted as bare `<Calculation>` instead of wrapped in `<Interval>`)
   - **7.4** — rendering layer strips the canonical `Name` tag to a single letter before generation
   - **7.5** — cross-file Perform Script missing `<FileReference>` (pastes as `<unknown>`)
3. Check wrapper: must be `<?xml version="1.0" encoding="UTF-8"?>` + `<fmxmlsnippet type="FMObjectList">`.
4. Check indentation: two spaces, no tabs.
5. Check CDATA: all calculation content must be in `<Calculation><![CDATA[...]]></Calculation>`.
6. For each step, verify the canonical skeleton matches the spec for that step ID/name.
7. Report issues clearly, quoting the offending XML fragment and explaining the paste-time consequence.
8. Offer a corrected version.

---

## Task: Generating XML

When the user wants to generate FileMaker XML from a description or pseudocode:

1. Read `core.md` and `steps-control.md`, then the category files for
   the steps the task needs (routing index above).
2. Look up each step's canonical skeleton in its category file.
3. Apply the core.md §1 paste format requirements throughout:
   - Wrap in `<?xml version="1.0" encoding="UTF-8"?>\n<fmxmlsnippet type="FMObjectList">...\n</fmxmlsnippet>`
   - Two-space indent, no tabs
   - CDATA for all calculations
   - Expanded (not compact) child forms
   - Correct element order per spec
4. For schema references (table names, field names, layout names, script names):
   - If the user has provided a DDR or explicit IDs, use those.
   - Otherwise use the **placeholder-ID pattern**: `id="1"` everywhere, with `name` attributes matching the user's names. FileMaker will resolve real IDs on paste. (core.md §5)
5. Emit the variable-name element for Set Variable and any other step that requires it using the correct four-letter form `Name` (capital N, lowercase a-m-e) as documented in core.md §3 and §5. Be aware of the rendering trap described in §7.4 — the tag must be the full word, not a single letter.
6. Use ASCII comparison operators (`<>`, `<=`, `>=`) rather than Unicode equivalents — safer for transport (core.md §5).
7. Output the complete XML inside a code block with `xml` syntax highlighting.
8. After the XML, briefly note any assumptions made (e.g. placeholder IDs used, repetition defaulted to 1).

---

## Key conventions (quick reference — always verify against core.md)

| Convention | Rule |
|---|---|
| Wrapper | `fmxmlsnippet type="FMObjectList"` |
| Indent | 2 spaces, never tabs |
| Calculations | `<Calculation><![CDATA[expr]]></Calculation>` |
| Variable name tag | four-letter `Name` element, capital N (core.md §3) |
| Schema IDs without DDR | `id="1"` + matching `name` attribute (placeholder-ID pattern) |
| Comparison operators | ASCII: `<>` not `≠`, `<=` not `≤`, `>=` not `≥` |
| Disabled steps | `enable="False"` on the `<Step>` element |
| Comment divider (blank) | Self-closing `<Step enable="True" id="89" name="Comment"/>` |
