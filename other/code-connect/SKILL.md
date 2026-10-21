---
name: code-connect
description: Use when Figma components should point at the project's blocks and Blade components through Code Connect - reading the existing map, proposing new mappings from the block catalog, flagging components with no code counterpart, and sending mappings with send_code_connect_mappings only after the person approves the exact list. For reading a frame into specs use figma-ingest.
license: MIT
compatibility: Main session only, with the official Figma MCP server. Node 20+. Writes to Figma only after explicit approval.
---

# Code Connect

Mapped components make matching deterministic: a section whose Figma component is mapped to a block is filled without judgment. This skill creates those mappings, carefully, because they change a shared Figma file.

## When to use

- "Connect our Figma components to the code", "set up Code Connect".
- `figma-ingest` reported components without mappings that keep appearing.
- Not for ingesting a page (`figma-ingest`).

## Inputs required

1. A Figma file or frame URL.
2. The Figma MCP tools in this session (names ending in `get_metadata`, `get_code_connect_map`, `send_code_connect_mappings`).
3. The target project root and the kivo-creator plugin root (two levels above this skill's folder).

## Procedure

1. If the Figma tools are missing, stop with the connection steps from `figma-ingest`.
2. Call `get_metadata` for the frame and save it (for example `.creator/figma-metadata.xml`); call `get_code_connect_map` and save it (`.creator/figma-code-connect.json`).
3. Propose:

   ```bash
   node <kivo-creator>/scripts/code-connect.mjs --metadata=.creator/figma-metadata.xml --map=.creator/figma-code-connect.json --project=. --out=.creator/code-connect.json
   ```

4. Show three lists: already mapped (component and code), proposed (component, block or Blade component, score) and without a code counterpart. For each proposal, read the target's source file and drop proposals whose purpose does not match.
5. Ask the person to approve the exact list to send. Change nothing in Figma before that answer: end the turn with the question.
6. After approval (a later message), call `send_code_connect_mappings` once with the approved mappings, built from the tool's own input schema (node id, component name, source path, label). Do not send rejected or unreviewed items.
7. Call `get_code_connect_map` again and report what changed. List the unmatched components as candidates for new blocks or Blade components; do not create them here.

## Verification

- The map read after sending contains every approved mapping and nothing else new.
- No `send_code_connect_mappings` call happened before the approval message.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Send fails with a permission error | The account cannot edit the file or has no Code Connect access | Report it; the proposal file stays for someone with access |
| A proposal maps a card to a whole section block | Name similarity is not purpose | Drop it in step 4; map cards to Blade components instead |
| Everything is unmatched | Component names share no words with the code | Propose by hand from the catalog, still with approval |
| Mapped source path does not exist | The map points at a moved or deleted file | Flag it; propose the new path for approval |

## Escalation

Every send needs the person's explicit approval of the list. Ask before overwriting a mapping someone else created.
