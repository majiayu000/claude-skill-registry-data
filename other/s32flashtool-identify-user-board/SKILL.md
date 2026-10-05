---
name: s32flashtool-identify-user-board
description: Identify an S32 Flash Tool user board by exact name, partial name, image, or other hardware clues, and route to the correct support-details workflow.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32flashtool
  depends_on: '["s32flashtool-agent-rules-minimal", "s32flashtool-workflow-index", "s32flashtool-supported-devices-per-platform"]'
  tags: '["s32flashtool", "identification", "board", "hardware", "read-only"]'
---

# S32FlashTool - Identify User Board

Identify the most likely S32 Flash Tool board from whatever clues the user
provides - exact or partial name, board image, silkscreen text, connector
labels, processor markings, or installed S32 Flash Tool examples and PDFs -
and hand off cleanly to the support-details workflow once identity is known.

## When to use

Use this skill when the user wants to establish **what board they have**,
before any support or operation question can be answered concretely.

Typical triggers:
- the user says *"I have this board"*, *"which board is this?"*, or *"can
  you tell me what board this is?"*
- the user provides a board photo, silkscreen text, or connector labels and
  asks to identify it
- the user gives a partial or approximate board name (*"S32N EVB"*,
  *"the S32G reference design"*) that needs to be resolved to a canonical name
- the user gives an exact board name and asks for confirmation or context
- a sibling skill (e.g. `s32flashtool-supported-devices-per-platform`) needs
  a board identity before it can produce a support-matrix answer
- the session has no established board yet and the next request would need one

## When not to use

Do **not** use this skill for:
- support-matrix questions (*"which processors / flashes / interfaces are
  supported on this board?"*) - use `s32flashtool-supported-devices-per-platform`
- hardware setup / connection details (interface, port, boot mode) -
  use `s32flashtool-discover-hardware-setup`
- live processor identification from the connected target -
  use `s32flashtool-read-mcuid`
- routing a general user request - use `s32flashtool-workflow-index`
- any operation on the target (read, program, erase, verify) - use the
  matching operation skill

This skill is **read-only inference from clues**. It never invokes tools that
touch the target and never claims hardware verification.

## Shared references
- Apply shared rules from `s32flashtool-agent-rules-minimal/SKILL.md`.
- Use `s32flashtool-workflow-index/SKILL.md` to select the correct workflow.
- Hand off support-matrix questions to `s32flashtool-supported-devices-per-platform`.
- For claim labeling and evidence discipline, apply
  `s32flashtool-evidence-disciplined-technical-validation`.

## Quickstart

Follow this 5-step sequence. Skip forward when the user's clues already
answer an earlier step.

### Step 1 - Gather user clues

Extract any of:
- exact board name
- partial board name
- processor name or family
- platform (e.g. S32N5, S32G3)
- visible silkscreen text
- connector labels
- processor package marking
- whether the user provided an image or only text

If the user refers to *"this board"* and a board was identified earlier in
the session, reuse that identity unless new evidence contradicts it.

### Step 2 - Choose the identification path

**Path A - exact or near-exact board name given.** Use the name as the
primary clue. Refine or confirm with `nxp_knowledge_kb_search`. If
`s32flashtool_folder` is available, verify against installed examples/PDFs.
Return an identification with confidence. Do not block on requesting the
installation folder before giving a provisional answer.

**Path B - image only.** If `board_image_*` tools are available, use them
to shortlist candidates. Otherwise, use visible clues from the image
description together with `nxp_knowledge_kb_search`. With
`s32flashtool_folder` available and user permission, inspect `examples/`
and matching PDFs.

**Path C - no board name and no usable image.** Do not guess. Ask for the
smallest missing identifying detail (board name, processor family, or a
photo).

### Step 3 - Use installed S32FlashTool evidence when available

With `s32flashtool_folder`:
1. inspect `s32flashtool_folder/examples`
2. look for board/example names matching the user's clues
3. inspect matching board PDFs in `examples` (ask permission first for
   arbitrary local file reads)
4. treat an exact example or PDF hit as stronger evidence than inference
5. report installed-example evidence separately from knowledge-base evidence

Without `s32flashtool_folder`:
1. provide a provisional identification from user clues plus
   `nxp_knowledge_kb_search`
2. explicitly state that installed-example verification is still pending
3. ask for the folder only if the user wants authoritative verification

### Step 4 - Handle ambiguity

If multiple boards remain plausible:
1. list the top candidates
2. assign a confidence level to each (see below)
3. explain the discriminator for each candidate
4. ask the smallest follow-up question that would eliminate the ambiguity

Confidence levels:
- **high** - exact board-name match from the user, or exact installed
  example/PDF match
- **medium** - strong family/platform and knowledge-base match, no exact
  installed verification yet
- **low** - partial name match, approximate image similarity, or otherwise
  incomplete clues

### Step 5 - Hand off to support-details when needed

If the user asks *"what is supported on this board?"* after identification:
1. state the likely board/platform
2. hand off to `s32flashtool-supported-devices-per-platform`
3. keep identification evidence separate from support evidence

## Evidence sources

Use these in decreasing order of authority. Every claim in the response
labels which source it came from.

| Source | Label | Justifies | Does NOT justify |
|---|---|---|---|
| Exact board name from the user | `user-supplied` | *"Likely identified as X (user-supplied)"* | hardware verification, support conclusions |
| Installed example folder / PDF match under `s32flashtool_folder/examples` | `installed-example` | *"Matched against installed example `X-EVB.pdf`"* | that the board is physically present or working |
| `board_image_*` tool result with clear confidence | `image-match` | *"Board image analysis matched X with high confidence"* | anything the image can't show (populated flash, boot-mode jumpers) |
| `nxp_knowledge_kb_search` result | `kb-search` | *"Consistent with knowledge-base entry for X"* | authoritative installed-package answers when the folder is available |
| Live tool output from a connected target | `hardware-verified` | *"Verified by `read_mcuid` output"* | any board-level fact the tool didn't return |

Prefer higher-authority sources when they are available. Never merge sources
in a single claim - split into labeled statements.

## Preferred wording

Prefer *"likely identified from the user-provided board name"*, *"matched
against installed S32FlashTool examples"*, *"supported by knowledge-base
evidence"*, *"not yet verified against the local installation"*, *"not
hardware-verified"*.

Avoid *"this is definitely the board"* without exact evidence, *"supported
on the physical board"* without verified support and applicability, or
*"confirmed"* without documentation or live verification.

## Output format

Respond in this structure. Omit sub-sections that have no content rather
than leaving them empty.

### Hardware setup assessment
- **Likely board:** ...
- **Likely platform / family:** ...
- **Identification status:** exact match / likely match / ambiguous / insufficient information
- **Confidence:** high / medium / low

### Candidate boards
- **Candidate 1:** ... - reason
- **Candidate 2:** ... - reason
- **Candidate 3:** ... - reason
- If only one strong match exists: *"No significant alternative candidates identified."*

### Evidence
List the exact evidence used, one line per item, labeled with a source from
the Evidence sources table (`user-supplied`, `installed-example`,
`image-match`, `kb-search`, `hardware-verified`). Include the pointer
(example path, PDF filename, kb query, tool output reference).

### Recommended next step
State the single safest next action. Typical patterns:
- Provisional answer, `s32flashtool_folder` missing -> ask for the folder to
  verify against installed examples/PDFs.
- Ambiguous -> ask for the smallest missing discriminator.
- Identified, user wants support details -> hand off to
  `s32flashtool-supported-devices-per-platform`.

### Command or tool suggestion
Name the exact next tool/skill to use, e.g.:
- `nxp_knowledge_kb_search` with the identified board/platform clue
- inspect `s32flashtool_folder/examples`
- apply `s32flashtool-supported-devices-per-platform`

### If more information is required
Ask only the minimal follow-up question(s). Examples:
- *"What is the exact board name printed on the PCB or box?"*
- *"Can you share the processor family or device marking?"*
- *"Do you want me to verify this against your local S32FlashTool installation?"*
- *"What is your S32FlashTool installation folder?"*

## Worked examples

**User gives only a picture.** Try `board_image_*` first. Fall back to
visible-clue reasoning plus `nxp_knowledge_kb_search`. Return the top
candidates with confidence. Ask for the smallest discriminator if
ambiguity remains.

**User gives only a board name.** Use the name as the primary clue. Refine
with `nxp_knowledge_kb_search`. Do not block on requesting
`s32flashtool_folder`. Ask for the folder only if the user wants
installed-file verification.

**User gives no hardware details.** Do not guess. Ask for the smallest
missing identifying detail. Do not jump to programming or support
conclusions.

**User says "I have this board <name>. Tell me what you know about it."**
Identify the board and platform first. Label the result as exact, likely,
or provisional. If the user then asks about supported processors, flashes,
interfaces, or limitations, hand off to
`s32flashtool-supported-devices-per-platform`.

## Guardrails

**Scope**
- Only identify the most likely S32 Flash Tool board from clues (name,
  image, silkscreen, connector labels, installed examples). Route
  support-matrix questions to `s32flashtool-supported-devices-per-platform`.
- Recovery on scope mismatch: name the correct sibling skill and stop.

**Destructive actions**
- Identification is read-only. Do not trigger writes, erases, or flash
  operations from this skill.

**Refuse-and-escalate**
- Do not force a single-board match when several remain plausible.
  Recovery: return all candidates with evidence labels and confidence.
- Do not claim installed-example evidence unless `s32flashtool_folder` was
  provided and inspected. Recovery: label the answer as provisional and
  ask for the folder if the user wants stronger evidence.
- Do not claim hardware verification unless a live tool call confirmed it.
  Recovery: label the answer as *"not hardware-verified"* and name the
  live tool that would verify it (usually `s32flashtool-read-mcuid`).
- Do not fabricate hardware-specific defaults. Recovery: ask for the
  missing detail.

**Output contract**
- The identification status is exactly one of `exact | likely | ambiguous | unknown`.
- Every claim carries an evidence label from the Evidence sources table
  and a pointer (filename, kb query, image field, silkscreen text).
- Board identification is reported separately from support-matrix
  conclusions.

## Validation loop

1. The response classifies the match as one of
   `exact | likely | ambiguous | unknown`. Fail if the category is absent
   or invented.
2. Every claim (board name, platform, family, installed-example hit)
   carries an evidence label and pointer. Fail on any unsourced claim.
3. Support-matrix questions are deferred to
   `s32flashtool-supported-devices-per-platform`. Fail if this skill
   answers them directly.
4. No hardware-verification claim (*"board confirmed"*, *"connectivity
   verified"*) is made without a corresponding live tool call. Fail on
   any such claim.
5. No MCP tool that writes to a target is invoked. Fail on any destructive
   tool call.

## Out of scope

- Answering support-matrix questions (which processors / flashes /
  interfaces are supported on the board). Route to
  `s32flashtool-supported-devices-per-platform`.
- Live hardware verification. Use the connectivity/operation skills
  (`s32flashtool-read-mcuid`, `s32flashtool-get-flash-id`,
  `s32flashtool-list-available-serial-communication-interfaces`).
- Forcing a single-board match when multiple candidates remain plausible.
- Making installed-example claims without inspecting `s32flashtool_folder`.
