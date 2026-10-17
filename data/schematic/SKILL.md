---
name: schematic
description: Document a non-code system — disks, mounts, network, service graph, device wiring — as a diagram-first wiki doc backed by captured ground truth. Trigger on:- schematic, diagram this, draw the layout, document how this is wired, map my disks, picture of the setup, wiki diagram.
argument-hint: "the system to draw — e.g. 'disk and dataset layout on this box', 'erp service graph' [--excalidraw]"
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Edit, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_evaluate, mcp__plugin_playwright_playwright__browser_close
model: claude-sonnet-5
---

# Schematic

A structure explained in paragraphs is a diagram written the long way. This produces the
diagram, and the evidence that it is true.

The skill is not the mermaid block — you can already draw one. It is the discipline
around it: capture before drawing, check every node back to the capture, and land the
result where a future session will find it.

## When to use this

- A system was just set up, reorganized, or discovered, and the knowledge currently lives
  only in this session.
- Someone would otherwise have to read piles of prose — or re-run the discovery — to
  learn how it is put together.
- **Codebase → `/crawl`** (its output is `CODEBASE.md`, consumed by the pipeline). This
  skill is for everything else with structure: disks and datasets, mounts and backups,
  network segments, host/service graphs, a device's power and data path, one dataset's
  journey across machines.
- Skip when the structure is three boxes and one arrow — say it in a sentence.

## Procedure

1. **Read `.specify/memory/constitution.md`** — the Document shape section governs the
   output.

2. **Bound the subject.** One line: what is inside the picture, what is deliberately
   outside it. A schematic without a boundary grows until it explains nothing.

3. **Search the wiki first** (`wiki-local` `search`). If a doc for this system exists,
   this run updates it — do not open a second doc on the same subject.

4. **Capture ground truth by command, never from memory.** One Bash call, section
   headers, output to a scratch file. Pick the probes for the subject:

   | Subject | Probes |
   |---|---|
   | disks / datasets | `lsblk -f`, `findmnt -A`, `df -h`, `zpool status`, `btrfs fi show`, `blkid` |
   | mounts / backups | `findmnt`, `systemctl --user list-timers`, the backup tool's own config |
   | network | `ip -br a`, `ip r`, the dnsmasq/router config file itself |
   | services / hosts | `systemctl --user list-units --state=running`, unit `ExecStart` lines, listening sockets via `ss -ltnp` |

   Read a governing config rather than inferring it from an effect. If a probe is
   unavailable, say so — an unverified region of the diagram gets marked, not guessed.

5. **Pick the form from the structure, not from habit.**
   - containment (disk → partition → dataset → mountpoint) → `flowchart` with `subgraph`
   - movement (sync, backup, replication direction) → `flowchart LR`, edges labelled with
     what moves and how often
   - lifecycle / status → `stateDiagram-v2`
   - ordering over time → `sequenceDiagram`
   - more than topology per element → the constitution's escalation applies; this is the
     `--excalidraw` case, and `excalidraw.md` holds the gate in full.

6. **Render one mermaid block**, per the constitution's Document shape. Every node label
   carries its identifying fact — device path, size, filesystem, host, port — so the
   picture stands alone.

   **`--excalidraw`** — draw natively instead: emit an element skeleton on a declared
   grid and render it to `<slug>.excalidraw` plus `<slug>.svg`, per `excalidraw.md`. The
   SVG is what the doc embeds; the `.excalidraw` is the editable original. State the grid
   pitch in the doc so a later edit lands predictably. This mode needs network.

7. **Drift check.** Walk each node and each edge back to a specific line in the capture.
   Anything you cannot source is deleted, or drawn and labelled `?`. State the result in
   one line: how many nodes checked, how many marked.

   In `--excalidraw` mode the unit is not the node but **the claim**. Position, grouping
   and colour all assert things there — a zone drawn around two of five bays claims those
   two are a vdev, and an empty bay claims the slot is free. Walk every element that
   asserts something back to the capture, ornament included when it carries meaning.
   Anything that asserts nothing must be visibly inert: no label, no fill that reads as a
   grouping. If you cannot tell whether an element is a claim, it is one.

8. **Write the prose beneath it — only what the picture cannot carry:** why this layout,
   what breaks it, what is deliberately not redundant, what is planned but not built. If
   a paragraph restates the diagram, cut it.

9. **Close with the capture commands** under a `## Verify` heading, so the next reader
   can re-check the diagram against the box instead of trusting its date. With
   `--excalidraw`, name the `.excalidraw` file there too, and the grid pitch it uses.

10. **Propose the wiki write in one line** — title plus gist — and wait for an explicit
    yes, per the standing store rules. On yes: `write_doc` to `wiki-local`, and
    `create_entity` for a host, pool, or service that needs a stable identity. If
    `wiki-local` will not connect, report that and save the doc to a file — never let the
    knowledge land nowhere.

## Constraints

- Never draw before step 4. A diagram from memory is a plausible-looking fiction, and it
  is worse than no doc because it will be trusted.
- The diagram is the top of the doc. If the reader must read prose to understand the
  picture, the labels are wrong, not the reader.
- One subject per doc. A second system is a second run.
- `--excalidraw` is for subjects mermaid cannot express, not for subjects you would
  rather hand-arrange. A graph drawn natively is a graph a future session can no longer
  diff.
- In `--excalidraw` mode the `.excalidraw` file is the source of truth and the SVG is
  generated from it. Never hand-edit the SVG.
- Do not build a mermaid→excalidraw conversion step. It was tried and it fails on
  `subgraph`; see the verified note in `excalidraw.md`.
- Do not reorganize, mount, format, or otherwise change the system you are documenting —
  this skill observes. A defect found while drawing is a finding to report, and an erp
  task if it is deferred.
- Do not write to the wiki without the explicit yes from step 10.

## Done criteria

- One mermaid block, every node labelled with its identifying fact.
- Every node and edge sourced to the capture, or visibly marked `?`.
- Prose contains nothing the diagram already shows.
- A `## Verify` section holds the commands that regenerate the evidence.
- The doc is in the wiki, or its absence is reported with the file it was saved to.
- With `--excalidraw`: `.excalidraw` + `.svg` both written, every claim-bearing element
  sourced, the grid pitch stated, and the localhost server confirmed stopped.
