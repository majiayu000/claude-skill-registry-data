---
name: diy-works
description: Create dimensioned 2D drawings and editable Blender models from sketches, plans, or technical PDFs. Design and revise furnished interiors across CAD and Blender, compare layout variants, check clearances and moving parts, and render daylight or night views. Develop furniture models into shop drawings, bills of materials, edge-banding and drilling schedules, and panel-saw cutting plans. Use for a single stage or the full workflow, with an optional guided brief. Triggers also on Czech requests such as "návrh do výroby", "nářez", "výkres", "truhlář", "skříňka", "kuchyňská linka".
user-invocable: true
---

# From Design to Fabrication

Start with the user's existing material and deliver the stage they ask for. A sketch request can end with a 2D drawing. A request to model a product from a PDF calls for an editable model. For fabrication, continue through the files the workshop needs.

Answer in the user's language. Czech users get Czech text, and Czech workshop terms are fine (nářez, prořez, olepení, kusovník, DTD, LTD). File names, part IDs and JSON keys stay as they are.

## Before you start: check dependencies

The skill runs in Claude Code and in the OpenAI Codex agent. All paths below are relative to this skill's directory, wherever it is installed (for example `.claude/skills/diy-works` or `~/.codex/skills/diy-works`). Run the helper scripts with `python3` through the agent's shell tool.

The first time the skill is used in a session, and before any stage that needs an external tool, run:

```text
python3 scripts/check_env.py --stage <2d|3d|clearance|cutting|dwg|all>
```

If anything is reported as `MISSING`, **tell the user before doing the work**. Say what is missing, which deliverable it blocks, and give the exact install command the script printed. Offer to run that command. Never install anything without the user's consent. For the Python packages, `python3 scripts/check_env.py --install` creates `~/.venvs/diy-works` and installs `shapely` and `ezdxf` there (Homebrew and Debian Python refuse a global `pip install`). Run it only after the user agrees. Afterwards, run every helper script with the interpreter the check prints under "Run the helper scripts with". If the user declines, continue with the stages that don't need the missing item, and list the outputs that were skipped in the final summary.

| Need | Used for | Alternative |
| --- | --- | --- |
| Python 3.8+ | all helper scripts | none |
| `shapely` | `scripts/check_clearance.py` | measure clearances manually in CAD/Blender and say so |
| `ezdxf` | DXF drawings, DXF sheet layouts | a CAD MCP server; JSON/CSV/SVG cutting plans work without it |
| Blender MCP **or** local `blender` | editable 3D models, renders | a connected Blender MCP removes the need for a local binary, and vice versa |
| ODA File Converter / libredwg | `.dwg` delivery | deliver DXF and say so |

The script cannot see agent tools. Check for a connected Blender MCP yourself: in Claude Code, look for `mcp__blender__*` tools (load them via tool search if they are deferred); in Codex, look at the configured MCP servers. If none is connected, use headless Blender: `blender -b --python <script.py>`. The helpers in `scripts/blender/` work both ways (see [parts.json](references/parts-json.md)). Report which method you actually used. The optional `vykres-do-blenderu` skill helps with paired DXF/Blender scenes. If it is not installed, carry on without it.

## Optional guided brief

When someone asks for a guide, for example `/diy-works guide` in Claude Code or `$diy-works guide` in Codex, or “walk me through it,” lead a short conversation. For a direct brief, start work immediately. If the user wants to prepare or share a brief independently, link to the [browser guide](guide.html). It works offline once the package is extracted.

1. Use previous answers and attachments. If the goal is unclear, offer a dimensioned 2D drawing, a Blender model, fabrication documents, the complete workflow, or a room layout and revision. For the last option, establish whether the user wants a review, alternatives, a change to a particular file, or another view.
2. Ask one question at a time that affects the next decision. For 2D, establish a reference dimension and the views required. For 3D, confirm the product variant and what the model will be used for. For fabrication, establish which dimensions have been measured, which material and hardware have been chosen, and which cutting parameters the workshop uses. Consult the drawing or PDF first when it can answer the question.
3. Accept “I don't know,” “skip,” or “start with what you have.” Once work can proceed, briefly summarise the brief and create the requested deliverable. If the user only wants a brief, deliver it as text. Treat a brief from the offline guide as the starting point and ask only about gaps that matter at the current stage.

When the user attaches a ZIP from the guide, read `project-brief.txt` and the relevant files in `attachments/`. Earlier versions used `zadani-pro-codex.txt` and `prilohy/`. The current chat request takes precedence. Treat original PDFs, drawings, and models as reference material. Look for an external path only if the corresponding item is missing from the bundle.

## 1. Establish geometry and scale

- Identify the subject, deliverable, current revision, and dimensions that determine the result. Carry forward confirmed decisions. For multiple variants, check the product code, handedness, and source file.
- Work in millimetres. Define a shared origin, axes, reference face, and orientation. Record whether each critical dimension comes from a manufacturer, a site measurement, a design decision, or an estimate. For PDF sources, record the page and view.
- Follow the relevant steps for [2D design, technical PDFs, and modelling](references/vykres-a-model.md). When updating a paired architectural DXF and Blender scene, the installed `vykres-do-blenderu` skill can also help.
- Preserve the source. Save changes as a clearly identified revision and use consistent product, assembly, and part IDs across deliverables. Update the shared dimensions and regenerate affected outputs from them.

## Work on an existing interior

Choose the instructions that match the request. A review can end with findings. A new camera view can use the approved model as it stands.

| When the user asks for… | Use this procedure |
| --- | --- |
| A change to a furnished plan, a missing wall, a new opening, or a CAD/Blender update | [Select the correct revision, edit the paired files, and check the result](references/project-revisions.md) |
| A fitted kitchen, bathroom, wardrobe, bedroom, study area, or open-plan living space | [Design the room around its users, products, services, and moving parts](references/room-design.md) |
| Alternatives, a room audit, a different camera, mood lighting, or a seasonal arrangement | [Compare layouts and present the approved geometry](references/views-and-variants.md) |
| A measured answer about a door swing, drawer, chair, or appliance clearance | [Check real footprints and operating positions](references/clearances.md) |
| Drawings for a built-in seen in a room rendering | [Extract the selected assembly and define its machining details](references/vyrobni-dokumentace.md) |

## 2. Resolve the construction for fabrication

Follow the [shop documentation workflow](references/vyrobni-dokumentace.md). Break the design into physical parts and purchased components, and record them in one [`parts.json`](references/parts-json.md). The [worked example](examples/skrinka/README.md) shows the whole chain on a small cabinet. Choose the joints, back-panel location, and mounting arrangement for the fronts. Derive blank dimensions and drilling positions from that construction. The model's outer envelope and visible gaps alone do not define them.

Consider fabrication during design. For a corner desk, compare a split top with a supported joint against a single L-shaped top. Check available sheet sizes, grain matching at the joint, visible edges, access for assembly, and whether the parts fit through the doorway. Check knee clearance, drawer travel, and cable grommet positions.

## 3. Plan cuts for the intended workshop

Generate the BOM, edge banding, drilling schedule, labels and the cutting job with `scripts/bom.py` from `parts.json`, then run the [sheet cutting planner](references/narez.md) on the generated `narez-job.json`. Show the user the SVG sheet preview (`--format svg`) and the yield per sheet. Verify the material, thickness, net build-up at each edge, permitted rotation, grain direction, measured saw kerf, trim allowances, and available sheet sizes. Each cut must run all the way across one existing workpiece. Document internal cut-outs, mitres, grain matching across adjacent parts, and subsequent machining separately.

Before releasing a plan for fabrication, verify the order of operations, including edge banding, and the capabilities of the actual saw or panel cutting centre. If a parameter is missing, continue with the parts that can be verified and identify the affected drawing or operation.

## 4. Verify and deliver

- **2D.** Reopen the saved DXF and check the units, critical dimensions, and at least one asymmetric feature. For a PDF, render the sheets and check legibility and print scale.
- **3D.** Reopen the saved model, measure its actual dimensions in world coordinates (`scripts/blender/measure.py` reports sizes, unapplied scale and overlapping panels), and compare the corresponding views against the source. Show a preview from an angle that reveals an important detail.
- **Fabrication.** Match part IDs across the model, drawings, bill of materials, and cutting plan. Check quantities, assembled dimensions, edges, orientation, and cut feasibility. Identify which items have been verified for the shop and which are still at the design stage. Link to the actual deliverables and list any outstanding inputs that affect fabrication.
