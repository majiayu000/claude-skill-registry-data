---
name: hmi-design-light
description: ISA-101 design rules for Human Machine Interfaces in process automation, covering display hierarchy, color standards, alarm integration, navigation, and situation awareness. Use when designing, building, reviewing, or generating code for HMIs, control system displays, SCADA screens, operator dashboards, or industrial control panels. Use when asked about ISA-101, alarm design, operator display hierarchy, or HMI color standards.
---

# HMI Design for AI Agents

ISA-101 design rules for Human Machine Interfaces in process automation. Apply these rules strictly when designing HMI displays, screens, dashboards, or control interfaces.

## Core Design Philosophy

1. **The HMI is a safety tool first.** Every design decision must support safe, effective process monitoring and control.
2. **Support situation awareness.** The operator must always know: what is happening now, why it's happening, and what will happen next.
3. **Minimize cognitive load.** Operators should detect, diagnose, and respond — not search, decode, or remember.
4. **Consistency is mandatory.** All displays must share a unified look, feel, and interaction model.
5. **Failure must be visible.** If a display element, data source, or communication path fails, the operator must know immediately.

## Display Hierarchy

Design displays generally in a 4-level hierarchy.

### Level 1 — Overview (Entire Span of Control)
- Shows the operator's ENTIRE scope of responsibility on ONE screen
- Key parameters, calculated conditions, alarm status, deviation indicators
- Embedded sparkline trends for critical variables
- NO control actions — monitoring only
- Abnormal states must be immediately visible via color/shape changes
- Should be continuously visible (dedicated monitor if possible)
- Include: deviation direction, severity indicators, alarm counts by area

### Level 2 — Unit/Area Operating Displays (Primary Working Displays)
- Operator's PRIMARY working displays during normal operations
- Show one major system or subsystem per display
- Include all controllers, setpoints, and indicators needed for routine operations
- Display all high and medium priority alarms for the area
- Task-based layout: operator should handle most routine work from these displays with minimal navigation
- Include start-up/shutdown task-specific information

### Level 3 — Detail Displays (Troubleshooting)
- Detailed P&ID-style or schematic views of specific equipment
- All control loops, indicators, and interlock status for depicted equipment
- Display ALL alarm priorities
- Used for non-routine operations: lineup changes, equipment switching, diagnostics
- Task-based: minimize navigation within troubleshooting workflows

### Level 4 — Diagnostic / Reference Displays
- Point details, operating procedures, help information
- Safety shutdown details, interlock/permissive logic
- Can be popups or faceplates (not always full-screen)
- Not primarily for process control, but control access may exist (e.g., point detail faceplates)

## Color Rules

### Background
- Use UNSATURATED or NEUTRAL backgrounds (light gray recommended)
- NEVER use black backgrounds (causes excessive contrast and eye strain)
- NEVER use saturated/bright backgrounds
- Test all color schemes in grayscale to verify sufficient contrast for color-blind users

### Color Usage Principles
- Color directs attention and adds meaning — use it SPARINGLY and CONSISTENTLY
- Reserve alarm colors EXCLUSIVELY for alarms — never use alarm colors for other purposes
- The most noticeable/saturated colors = most important information
- Color must NEVER be the sole indicator — always pair with shape, text, brightness, size, or texture
- Use no more colors than users can reliably distinguish (typically 6-8 max for coding)
- No color gradients on static elements; gradients may be used on dynamic elements only
- Maintain consistent color meanings across ALL displays

### Color-Blindness Accommodation
- Common deficiencies: red-green (~8% males), green-yellow, white-cyan
- Use brightness/contrast differences alongside color
- Test with grayscale rendering
- Consider age-related lens yellowing (blues/purples appear gray to older users)

## Visual Design Rules

### Animation and Visual Dynamics
- Blinking: ONLY for unacknowledged alarms or items requiring immediate action
- Flashing (color alternation): ONLY for abnormal situations requiring attention
- NEVER blink or animate text/numbers (makes them unreadable)
- Always provide a way to stop/acknowledge blinking
- **If nothing requires operator action, NOTHING on the display should be moving, blinking, or flashing.**

### Text and Numbers
- Use mixed/title case (NOT ALL CAPS — harder to read)
- Underlines = hyperlinks ONLY
- Font must be readable from normal operator position
- Clear character definition (distinguish 1/I/L, 0/O)
- Horizontal text orientation (vertical only if unavoidable)
- Abbreviations only if part of standard operator vocabulary
- Numbers: suppress leading zeros on whole numbers, show leading zero for values between -1 and 1
- Show engineering units near values
- Match decimal precision to measurement accuracy and operator need
- Present numbers in directly usable form (operator should never need to convert units)

### Information Density
- Match density to the display's PURPOSE (overview = lower density; detail = higher density)
- If a display is too dense:
  - Consolidate data into summarized indicators
  - Choose a more effective display style (trend vs. table vs. bar)
  - Provide some information on-demand only (popups/faceplates)
  - Split into multiple displays

### Graphic Symbols
- Navigation targets: distinct, consistent visual coding
- Selectable items: distinct, consistent visual coding (different from navigation targets)
- Process-action buttons: visually distinct from navigation buttons
- Unavailable buttons: remain visible but visually coded as unavailable (grayed)
- Dynamic elements should change appearance to reflect process state

## Navigation Rules

### Performance Targets
| Action | Target |
|--------|--------|
| Critical displays | 1-2 clicks |
| Non-critical displays | 3 clicks max |
| Alarm summary | 1 click (always) |
| System diagnostics | 1-2 clicks |
| Display call-up time | < 3-5 seconds |
| Operator switching | < 5 seconds |

### Navigation Design
- Primary pattern: HIERARCHICAL (drill-down from overview to detail)
- Support lateral (side-to-side) navigation between related systems
- Provide multiple navigation methods (menus, hyperlinks, keyboard shortcuts, context menus)
- Yoking: link related displays so one click updates multiple screens/panels
- Operator should NEVER need to type a display name — clickable access for everything
- Navigation should support both normal AND abnormal operation workflows

## Interaction Design

### Data Entry
- Consistent presentation across all displays
- Inset entry fields, clear current selection, grayed unavailable items
- Visual format clues for expected input format
- Reject wrong-format entries with clear error explanation
- Process-affecting commands require MULTIPLE input actions (never single-click for critical actions)
- Multi-step commands: show confirmation of ALL actions before execution
- Always provide cancel/undo during change process
- Enforce acceptable limits on critical entries

### Faceplates and Popups
- Include configurable timeout (auto-close after inactivity)
- Operator must be able to override timeout
- Must not obscure important display information (or be moveable)
- If multiple popups: clearly indicate which has keyboard focus
- Consistent presentation with rest of HMI

## Alarm Integration

- Alarm colors are RESERVED — never used for non-alarm purposes
- Unacknowledged alarms: blinking indicator
- Acknowledged alarms: steady (non-blinking) indicator
- Alarm priority must have both audible AND visual indication
- Alarm summary accessible in 1 click from ANY display
- Auditory signals: audible from operator position, not so loud as to distract other operators
- Provide method to silence acknowledged audible alarms
- On Level 1: show all top-priority alarms positioned near associated equipment
- On Level 2: show top and middle priority alarms
- On Level 3: show all priorities

## Situation Awareness

Three levels the HMI must actively support:

1. **Perception** — What is happening in the process right now?
2. **Comprehension** — What does the current state mean?
3. **Projection** — What will happen next if no action is taken?

**Dark screen philosophy:** Normal = visually quiet (muted colors, no animation). Abnormal = visually loud. As deviation increases, visual/audible signals increase proportionally.

**Preventing tunnel vision:** Level 1 overview must remain visible at all times. Display context around alarming values — neighboring values, trends, upstream/downstream status.

## Display Styles Reference

| Style | Use When |
|-------|----------|
| **Process** (P&ID/PFD) | Showing equipment, piping, instrumentation relationships |
| **Functional Overview / Dashboard** | KPIs, cross-area performance, executive summary |
| **Schematic Overview** | Operator's full span of control |
| **List/Table** | Tabular data, equipment lists, strapping tables |
| **Trend/Graph** | Real-time or historical data over time |
| **Group (Faceplate array)** | Side-by-side controller monitoring (e.g., all flow valves) |
| **Topology/Location** | Physical/network layout, fire detection zones |
| **Logic Monitor** | Boolean/function block/ladder logic visualization |
| **Procedural** | Step-by-step sequential operations |
| **Health/Diagnostic** | Network, server, controller status |
| **Alarm List** | Alarm summaries, shelved/suppressed lists |
| **Video** | Live CCTV/process cameras |

## Performance Requirements

- Display call-up: fully populated with live data in 3-5 seconds
- Display refresh: 1-5 seconds (match process dynamics, never sub-second — causes jittery numbers)
- Faceplate refresh: 2-3 seconds
- Write-to-controller acknowledgment: provide immediate visual feedback
- If display load is slow (trends, remote), show graphic first and populate data progressively

## Common Mistakes

1. Using black backgrounds with bright colored elements (causes eye strain, chromatic distortion)
2. Using alarm colors (red, yellow) for non-alarm decoration
3. Creating displays with no clear visual hierarchy — everything looks equally important
4. Over-animating — excessive blinking, flashing, and movement
5. Requiring more than 3 clicks to reach any display
6. Designing for normal operations only — forgetting abnormal/upset scenarios
7. Putting too much information on Level 1 (overview should be scannable in seconds)
8. Using inconsistent color meanings across displays
9. Requiring operators to convert units or perform mental arithmetic
10. Not providing cancel/undo for control actions
