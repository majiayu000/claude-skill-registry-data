---
name: mogu-visual
description: |
  Transform technical descriptions into interactive animated HTML visualizations
  starring Mogu — a mushroom character whose cap adapts to each concept.
  Generates self-contained HTML files with Canvas 2D animations, interactive
  parameter controls, and a consistent character brand.
  Use when: "explain how X works", "visualize this concept", "make an interactive
  demo of", "show me how Y works visually", "mogu", "technical animation",
  "interactive diagram", "concept visualization", or any request to turn a
  technical mechanism into an interactive, visual, character-driven explanation.
  Also use when the user describes a system they want to understand better and
  would benefit from seeing it animated, even if they don't say "visualize" —
  e.g., "I don't get how Kafka partitions work", "can you show me load balancing",
  "explain consensus algorithms".
---

# Mogu Visual

Transform technical concepts into interactive animated HTML visualizations starring Mogu.

Before writing any code, read `references/character.md` -- it contains the canonical Mogu
specification that governs every visual decision below. If the reference fails to load,
the inline quick reference in Section 4 of this document is sufficient to draw a correct Mogu.

## Workflow

### Step 1: Extract Concepts

Parse the user's input and **enumerate every distinct concept** before doing anything else.
This is the most critical step — concepts that aren't listed here will be invisible in the output.

**1a. Section-by-section extraction:** Walk through the input text section by section (not a
single pass). For each paragraph or section, ask: "What concepts are introduced here that
aren't already in my list?" Tag each concept with the source section for traceability.

**1b. Implicit concept scan:** After the explicit pass, scan for concepts the text implies
but doesn't name directly: consistency boundaries, failure domains, trust zones, ownership
boundaries, backpressure, retry behavior, ordering guarantees, staleness.

**1c. Deduplication:** Group aliases that refer to the same concept. "Broker," "message broker,"
and "coordination layer" might be one concept or three — resolve based on context.

**1d. Assign concept IDs:** Give each deduplicated concept a stable ID (C01, C02, ...).
These IDs track through the entire pipeline: extraction → categorization → mapping → code → rendered output.

**1e. Concept categorization:** Classify each concept. The taxonomy has 12 types — use the
most specific match, not the first match:

| Type | What it is | Visual treatment |
|------|-----------|-----------------|
| **Entity** | A named thing with identity and behavior | → Mogu actor |
| **Property** | An attribute of an entity (capability, comfort zone, role) | → Cap variation, badge, or onDraw glyph |
| **Flow** | Something that moves between entities (message, request, data) | → Animated item (differentiated by shape + color) |
| **Relationship** | A structural link (parent-child, peer, reviewer, depends-on) | → Connection line (style encodes type) |
| **State** | A lifecycle phase an entity passes through | → Expression change + cap color shift |
| **Event/Trigger** | Something that causes a transition ("on timeout", "when queue full") | → Key Moment with visible cause |
| **Policy/Strategy** | A decision mechanism (routing strategy, decomposition policy, retry policy) | → Policy gate: visual decision point that branches items based on criteria |
| **Constraint/Invariant** | A rule that must never be violated ("exactly one writer", "no cross-region") | → Boundary zone, guardrail line, or violation animation |
| **Boundary/Domain** | A scope delimiter (trust boundary, failure domain, ownership zone) | → Translucent region drawn via onDraw, actors contained inside |
| **Metric/Resource** | A measurable quantity (latency, capacity, utilization, budget) | → Stat display, bar gauge, or threshold line |
| **Derived/Projection** | State computed from other state (cache, dashboard, index, view) | → Fainter/offset Mogu or ghost copy, visually subordinate to source |
| **Source of Truth** | The authoritative canonical state (ledger, config, primary DB) | → Grounded Mogu with solid base line, bold label, "rooted" feel |
| **Layer/Tier** | A conceptual grouping or abstraction level | → Spatial zone or view toggle |

**Multi-type concepts:** A concept can have a primary type and secondary tags. A database
is primarily an Entity but also a Source of Truth. A queue is an Entity but also has
Metric/Resource (depth) and Constraint (capacity limit). Tag the primary type in the
categorization, add secondary tags in parentheses: `C07 MessageQueue [Entity (Metric, Constraint)]`.
The primary type determines the main visual element; secondary tags add overlays (gauge, boundary, badge).

**1f. Complexity assessment:** Count concepts. Then decide the scope:

| Count | Strategy |
|-------|----------|
| 1-8 | Single scene, all concepts visible at once |
| 9-15 | Single scene with 2-3 view toggles (each view ≤ 8 active concepts) |
| 16-25 | Hierarchical drill-down: overview scene → subsystem details on click/toggle |
| 25+ | Decompose input into 2-3 independent visualizations, each with its own scene |

**1g. View design** (if multi-view):

First, **group concepts using one of these strategies** (pick the one that best fits the input):

| Strategy | How to group | Best for |
|----------|-------------|----------|
| **By subsystem** | Each view = one subsystem or component cluster | Microservices, modular architectures |
| **By lifecycle** | Each view = one phase (setup → running → failure → recovery) | Stateful protocols, workflow engines |
| **By abstraction** | Each view = one layer (infra → platform → application → user) | Layered architectures |
| **By data path** | Each view = one data flow from source to sink | ETL, event-driven systems |
| **By question** | Each view answers one user question ("How does X work?" "What happens when Y fails?") | Complex systems with diverse audiences |

Then for each view, define:
- **Purpose:** what question does this view answer?
- **Concepts shown (by ID):** which concepts are active? Target ≤ 8 per view (soft cap — allow 9-10 if concepts are spatially grouped and don't clutter; never exceed 12)
- **Anchor concepts:** which concepts appear in ALL views as spatial landmarks (same position)?
- **Cross-view links:** which flows/relationships connect this view to others?

**1h. Clarifying questions** (only if needed):
- **Audience?** Developer, student, PM, general public?
- **Which aspect?** The whole system or a specific mechanism?
- **Depth?** High-level overview or implementation-level detail?

### Step 2: Write the Scene Script

The scene script must include a **concept coverage manifest** — every concept ID from Step 1
must appear with its visual encoding. This is the traceability contract.

```
Scene: [title]
Archetype: [archetype name or "custom: X + Y"]

Concept Coverage Manifest:
  C01 [concept name] → [visual element] — [encoding: position/cap/shape/motion/color/size/zone/stat/gate]
  C02 [concept name] → [visual element] — [encoding]
  C03 [concept name] → deferred to view:[view name] — [encoding when active]
  ...
  Coverage: N/N concepts mapped (must be 100%)

Views (if multi-view):
  - [view name] — purpose: [question it answers]
    Active: C01, C03, C07, C12 (≤8)
    Anchors: C01, C03
    Toggle: param "view" value "[name]"

Actors:
  - [role] ([size], [cap color], [cap shape], [texture]) — represents C01, C04
Items: [what flows, differentiated by shape/color — each type maps to a concept ID]
Connections: [relationships, style maps to relationship type]
Zones: [boundary/domain regions drawn via onDraw — each maps to a concept ID]
Parameters:
  - [name]: [type] [range] [default] — reveals/controls C07
  - view: toggle [view names] — switches active concept set
Key Moments:
  - [trigger] → [visual effect] — demonstrates C09 ([event/trigger concept])
Stats:
  - [stat name] — tracks C15 ([metric concept])
```

**Rendering patterns for hard concept types** (not just actors and items):

| Concept type | Rendering pattern |
|-------------|-------------------|
| Policy/Strategy | Policy gate Mogu: items enter, gate Mogu evaluates (processing expression), branches items to different paths based on criteria. Criteria shown as label on the gate. |
| Constraint/Invariant | Colored boundary line around a zone. Items that violate the constraint flash red + bounce back. The constraint is a visible guardrail, not just text. |
| Boundary/Domain | Translucent rectangular region (onDraw) containing the relevant actors. Label at top-left. Distinct color per domain. |
| Metric/Resource | Horizontal gauge bar (onDraw) near the relevant actor. Fill level animates with state changes. Threshold marker shows limits. |
| Derived/Projection | Ghost-Mogu: same shape as source but 60% opacity, offset slightly, connected by dotted line to source. Stale state shown as faded + lag animation. |
| Source of Truth | Solid base line under the Mogu + bold label. Visual "rooted" feel vs. floating derived copies. |

**Scene archetype selection** (see `references/scenes.md`):

| # | Archetype | When to use |
|---|-----------|-------------|
| 1 | **Pipeline** | Sequential stages, conveyor belt, ETL |
| 2 | **Network** | Nodes with edges, mesh, routing |
| 3 | **Pool/Queue** | Shared resource, workers grabbing tasks |
| 4 | **State Machine** | Single entity, morphing states |
| 5 | **Guard/Gate** | Gatekeeper, accept/reject, validation |
| 6 | **Tree** | Parent-child hierarchy, traversal |
| 7 | **Race** | Parallel tracks, contention, locks |
| 8 | **Transform** | Input goes in, different output comes out |
| 9 | **Broadcast** | One-to-many fan-out, pub/sub |
| -- | **Custom** | Combine archetypes or invent a new one |

Present the scene script to the user for confirmation before generating code. This
is the contract — changes after code generation are expensive.

### Step 2.5: Concept Coverage Audit

Before proceeding to Step 3, run this checklist against the concept manifest:

1. **100% coverage:** Every concept ID from Step 1 appears in the manifest. Count them.
   If coverage < 100%, stop and fix the scene script. No exceptions.
2. **No text-only escapes:** If a concept's encoding is just "label" or "annotation,"
   reconsider — can it be a cap shape, item variation, zone, gauge, gate, or expression
   instead? Text is a last resort. If text is truly the only option, add a `textOnlyReason`.
3. **"Deferred" concepts must resolve:** Every concept deferred to a view must have that
   view defined, with the concept listed as active in that view. Grep the manifest for
   "deferred" and verify each has a matching view entry.
4. **Visual differentiation:** If multiple concepts share the same type (e.g., 4 kinds of
   WorkItem), each must have a distinct visual encoding (shape + color, not just label).
5. **States have transitions:** If a concept has a lifecycle (proposed → active → blocked →
   completed), the visualization must show ≥ 2 states and animate the transition.
6. **Layers are spatial:** If the concept has architectural layers or tiers, they must be
   visually separated as canvas zones, not just described in text.
7. **Policies branch:** If a concept is a policy/strategy, the visualization must show
   the decision point and at least 2 different outcomes.
8. **Boundaries enclose:** If a concept is a boundary/domain, it must be drawn as a
   visible region with actors inside, not just labeled.

If any check fails, revise the scene script before generating.

### Step 3: Design the Cast

Select cap shapes, textures, and colors for each Mogu actor. Follow rules from
`references/character.md`:

- **Size = importance.** Central component gets the largest Mogu.
- **Same color = same role.** All API services share one color, all databases another.
- **Max 3 cap colors per scene.** More than 3 creates visual noise. Use shape/texture
  variation instead if you need more groups.
- **Colors:** Saturated but muted. Must pair with cream stem `#F5EDE0`.

### Step 4: Generate HTML

Use the **MoguScene engine** (`components/mogu-engine.js`) to keep generated HTML short and focused on scene logic.

**HTML template:**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>[Scene Title] — Mogu Visual</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    html, body { width:100%; height:100%; overflow:hidden; }
    canvas { display:block; width:100%; height:100%; }
  </style>
</head>
<body>
<canvas id="c"></canvas>
<!-- Path assumes output is in a sibling directory to components/ (e.g., test-output/).
     For standalone distribution, inline the engine or adjust the path. -->
<script src="../components/mogu-engine.js"></script>
<script>
// --- Scene code starts here (target: 150-250 lines) ---
var scene = new MoguScene(document.getElementById('c'), { title: '[Scene Title]' });

// 1. Add actors
scene.addActor('id', { label: 'Name', x: 0.5, y: 0.5, size: 80, cap: { color: '#FF4D4D' } });

// 2. Add connections
scene.connect('from', 'to', { style: 'dashed' });

// 3. Add parameters
scene.addParam({ id: 'rate', label: 'Rate', type: 'slider', min: 1, max: 30, value: 5, step: 1 });

// 4. Scene logic
scene.onUpdate(function(dt, time) { /* spawn items, manage state */ });
scene.onDraw(function(ctx, w, h, time) { /* custom visuals */ });

// 5. Start with absorption
scene.start(['keyword1', 'keyword2'], '#targetCapColor');
</script>
</body>
</html>
```

**Engine API quick reference:**

| Method | Purpose |
|--------|---------|
| `addActor(id, config)` | Add a Mogu. Config: label, x, y (0-1), size, cap.color/shape/texture |
| `removeActor(id)` | Remove a Mogu |
| `setExpression(id, expr)` | Change expression: neutral/curious/processing/proud/alert |
| `setCapColor(id, color)` | Animate cap color change |
| `getActorPos(id)` | Get pixel position {x, y} |
| `connect(from, to, opts)` | Draw line. Style: dashed/dotted/solid |
| `addParam(config)` | Add control. Type: slider/toggle/stepper |
| `param(id)` | Get current parameter value |
| `spawnItem(config)` | Spawn flowing item. Config: from, to, color, speed, arc, onArrive |
| `addZone(id, config)` | Boundary/domain region. Config: x, y, w, h (0-1), color, borderColor, label |
| `removeZone(id)` | Remove a zone |
| `addGauge(id, config)` | Metric bar attached to an actor. Config: actorId, label, value, max, threshold (same unit as value/max, e.g. 80 if max=100), color/warnColor/dangerColor |
| `setGauge(id, value)` | Update a gauge's current value |
| `addGhost(srcActorId, ghostId, config)` | Derived/projection copy of an actor. Config: x, y, opacity, staleOffset |
| `addAnnotation(id, config)` | Text callout on canvas. Config: x, y (0-1), text, color, fontSize, bg |
| `removeAnnotation(id)` | Remove an annotation |
| `onUpdate(fn)` | Register per-frame update: fn(dt, time) |
| `onDraw(fn)` | Register custom draw: fn(ctx, w, h, time) |
| `setStat(key, value)` | Show stat in bottom-left |
| `start(keywords?, color?)` | Begin (with optional absorption ceremony) |

**Built-in cap shapes** (use by string name): dome, flat, pointy, wavy, bumpy, droopy, split, spiky

**Built-in textures** (use by string name): spots, stripes, hex, circuit, swirl, constellation, scales, lightning

**The rule: AI generates only scene-specific code.** The engine handles rendering, game loop, controls, labels, connections, items, and the absorption ceremony. If the generated HTML exceeds 300 lines, you're probably reimplementing something the engine already provides.

### Step 5: Quality Gate

Check every item before delivering. If any row fails, fix it before handing off.

| Check | Failure | Fix |
|-------|---------|-----|
| Concept coverage | Input concepts missing from visualization | Revisit concept mapping, add actors/items/views/annotations |
| Character consistency | Proportions wrong, missing highlight/feet | Compare to canonical SVG in Section 4 |
| Interactivity works | Controls don't affect animation | Bind params to game loop via state object |
| Animation smoothness | Stuttering | Use `requestAnimationFrame`, not `setInterval` |
| Concept accuracy | Doesn't match the technical concept | Re-examine scene script, fix the metaphor |
| Self-contained | Errors on open | Check CDN links, inline all critical code |
| Not dead | No motion without interaction | Add idle bounce + ambient particle/item motion |
| Not skin-deep | Params only change cosmetics | Params must affect behavior (rate, count, routing) |
| Labels readable | Text overlapping Mogus, other labels, or UI elements | See label layout rules below |

**Label layout rules (common source of visual bugs):**

1. **Labels go below their Mogu**, offset by at least `moguSize * 0.35` from center. Never place labels at a fixed y that ignores Mogu size.
2. **Never stack two text elements without clearance.** If a queue bar / counter / status text exists between a Mogu and its label, the label goes below ALL of them.
3. **Shorten labels when actors multiply.** 5 consumers labeled "Consumer 1" through "Consumer 5" will overlap. Use "C1"–"C5" or omit labels when the cap color already distinguishes roles.
4. **Queue/status indicators inside or to the side**, not stacked below in the same column as the label. Prefer rendering counts inside bars (textBaseline = 'middle') rather than as separate text below.
5. **Test at extremes.** Check layout with max actor count (e.g., 5 consumers) and max queue depth. If pills/items overflow their container, cap the visible count.

## Mogu Character Quick Reference

This section is the fallback specification. If `references/character.md` loads, prefer that.
If it does not, everything below is sufficient to draw a correct Mogu.

### Canonical SVG

Source of truth. ViewBox: `0 0 140 170`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 170">
  <!-- Stem: rx=14 gives soft rounded corners -->
  <rect x="50" y="95" width="40" height="50" rx="14" fill="#F5EDE0"/>

  <!-- Cap: dominant dome, ~2.6x wider than stem -->
  <ellipse cx="70" cy="82" rx="52" ry="38" fill="#FF4D4D"/>

  <!-- Cap highlight: subtle polish, shifted upper-left -->
  <ellipse cx="55" cy="68" rx="18" ry="10" fill="#FF7070" opacity="0.5"/>

  <!-- Spots: 3 circles, varied size, scattered unevenly -->
  <circle cx="42" cy="72" r="6" fill="#FF8080" opacity="0.7"/>
  <circle cx="68" cy="55" r="5" fill="#FF8080" opacity="0.7"/>
  <circle cx="90" cy="68" r="7" fill="#FF8080" opacity="0.7"/>

  <!-- Eyes: solid black dots on stem, no highlights -->
  <circle cx="60" cy="115" r="4.5" fill="#0a0a0a"/>
  <circle cx="80" cy="115" r="4.5" fill="#0a0a0a"/>

  <!-- Mouth: simple upward arc -->
  <path d="M63,127 Q70,133 77,127" stroke="#0a0a0a" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Feet: small ellipses for grounding -->
  <ellipse cx="58" cy="145" rx="10" ry="4" fill="#EBE0D0"/>
  <ellipse cx="82" cy="145" rx="10" ry="4" fill="#EBE0D0"/>
</svg>
```

### Proportions (Scale-Independent Ratios)

These ratios hold at any render size. The `size` parameter in `drawMogu()` maps to
the viewBox height (170 units).

| Ratio | Value | Derivation |
|-------|-------|------------|
| Cap width / Stem width | 2.6x | Cap `rx=52` (diameter 104), stem `width=40` |
| Cap height / Total height | ~45% | Cap zone 76px out of 170px |
| Stem height / Total height | ~30% | Stem 50px out of 170px |
| Feet zone / Total height | ~15% | Feet at y=145, ±4px |
| Eye spacing | Stem width x 50% | Eyes at x=60, x=80; spacing=20, stem=40 |
| Mouth below eyes | Stem height x 24% | Eyes y=115, mouth y=127; offset=12/50 |
| Eye radius | Stem width x 11% | r=4.5, stem=40 |

### Invariants (Never Change)

These values are fixed across all Mogus regardless of concept:

| Property | Value | Notes |
|----------|-------|-------|
| Stem fill | `#F5EDE0` | Warm cream |
| Eyes fill | `#0a0a0a` | Near-black |
| Eye radius | `stem_width x 11%` | ~4.5 at canonical scale |
| Feet fill | `#EBE0D0` | Slightly darker cream |
| Cap highlight | Cap color lightened 20%, opacity 0.5 | Upper-left shift |
| Spot color | Cap color lightened 25%, opacity 0.7 | Default texture |

Never change stem/feet colors, eye color, or the proportions above.

### Expression System

Only eyes and mouth change. No new elements added. Alert is the only expression
with eye-whites.

| Expression | Eyes | Mouth | When to use |
|------------|------|-------|-------------|
| **Neutral** | Solid dots (r=4.5) | Upward arc `M63,127 Q70,133 77,127` | Default, idle, at rest |
| **Curious** | Left dot normal, right dot bigger (r=5.5) shifted up to y=113 | Small circle "o" at (70, 129) r=3.5 | Encountering new input, inspecting data |
| **Processing** | Horizontal lines (x1=54..66, x1=74..86 at y=115) | Wavy line `M60,128 Q65,124 70,128 Q75,132 80,128` | Actively computing, transforming |
| **Proud** | Upward arcs (happy squint) `M55,114 Q60,110 65,114` | Wide grin `M60,126 Q70,136 80,126` | Task complete, success, output delivered |
| **Alert** | White circles (r=6) + dark pupils (r=3.5, offset +1x, +1y) | Inverted-V `M64,129 L70,124 L76,129` | Error, warning, unexpected input |

### Cap Shapes (8 Reference Shapes)

Shape = structural metaphor. The AI can invent new shapes beyond these.

| Shape | Silhouette | Semantic mapping |
|-------|-----------|------------------|
| **Classic Dome** | Standard ellipse | Default, general-purpose |
| **Flat / Shiitake** | Wide, low ellipse (capRy x 0.6) | Platform, infrastructure, database |
| **Pointy / Wizard** | Tall cone (quadratic curve) | Algorithm, logic, security, encryption |
| **Wavy / Ruffled** | Undulating edge (sin wave x 4) | Streaming, async, event-driven, reactive |
| **Multi-bump** | Three overlapping circles | Distributed systems, concurrency, microservices |
| **Droopy / Melting** | Dripping edges (quadratic drips) | Cache overflow, memory leak, GC, degradation |
| **Split / Forked** | Two lobes, split down middle | Load balancing, branching, A/B testing, fork |
| **Spiky / Urchin** | Triangular protrusions (8 spikes) | Firewall, defense, rate limiting, DDoS protection |

Each shape function receives `(ctx, cx, cy, capRx, capRy)`, calls `ctx.beginPath()`,
draws the path, and leaves it open for the caller to fill.

### Cap Textures (8 Reference Textures)

Texture = surface pattern mapped to concept characteristics.

| Texture | Visual | Semantic mapping |
|---------|--------|------------------|
| **Classic Spots** | Scattered circles, varied sizes | Default, general-purpose |
| **Ridges / Stripes** | Vertical lines, evenly spaced | Ordered flow, pipeline, sequential |
| **Hexagonal** | Honeycomb grid | Network topology, mesh, P2P, graph |
| **Circuit** | PCB trace lines + dots | Computation, digital logic, CPU, binary |
| **Swirl** | Spiral curves (2 turns) | Recursion, loops, iteration, cycles |
| **Constellation** | Dots connected by lines | Node networks, service mesh, distributed |
| **Scales** | Overlapping arcs | Queues, stacks, buffers, pagination |
| **Lightning / Cracks** | Zigzag paths | Energy, events, interrupts, exceptions |

Each texture function receives `(ctx, cx, cy, capRx, capRy, spotColor, baseAlpha)`.
The 7th param `baseAlpha` (0-1, default 1) is a multiplier for all alpha values inside the
texture. This enables ghost/derived actors to render textures at reduced opacity. Textures
set `ctx.globalAlpha = ownAlpha * baseAlpha`, draw the pattern, then restore `ctx.globalAlpha = 1.0`.

### Cap Color Palette

Colors should be saturated but muted -- "as if the mushroom grew that way naturally."
Must pair with the cream stem `#F5EDE0`. No rigid domain-to-color mapping.

| Color | Hex | Semantic suggestions |
|-------|-----|----------------------|
| Red | `#FF4D4D` | Default, error, alert, critical path |
| Orange | `#FF8C42` | Activity, build, deployment, queue |
| Amber | `#FFB84D` | Warning, caution, cache, fallback |
| Yellow | `#FFD966` | Highlight, indexing, search |
| Lime | `#A3D977` | Growth, scaling, optimization |
| Green | `#52C77A` | Success, health, pass, ready |
| Teal | `#4DBFBF` | Flow, streaming, data pipeline |
| Sky Blue | `#5BA3E0` | Cloud, API, interface, communication |
| Blue | `#5680E0` | Logic, stable, core service |
| Indigo | `#7B68EE` | Deep computation, AI/ML, complex algorithm |
| Purple | `#A66FD9` | Transformation, middleware, orchestration |
| Magenta | `#E066A6` | Creative, UX, frontend, design system |
| Pink | `#FF6B9D` | Playful, user-facing, delight |
| Brown | `#A67C52` | Persistence, storage, database, logs |
| Gray | `#8C8C8C` | Neutral, deprecated, archived, inactive |

### Multi-Mogu Rules

When multiple Mogus appear in a single scene:

1. **Size = importance.** Primary component = largest. Helpers = small.
2. **Same cap color = same role.** All API services share one blue. All DBs share one brown.
3. **Max 3 cap colors per scene.** Use shape/texture variation for additional groups.
4. **Spatial arrangement:** Data flow left-to-right. Hierarchy top-to-bottom. Peers in a row.
5. **Same shape/texture = same structure type.** All async services get wavy caps.

### Absorption Ceremony

The 4-step brand intro sequence. Total duration: 3 seconds at 60fps.

**Step 1: Idle (0-0.8s)**
- Cap: `#FF4D4D` (red), classic dome, classic spots
- Expression: neutral
- Y-offset: sinusoidal idle bounce (+-2px, 2.5s period)

**Step 2: Notice (0.8-1.5s)**
- Expression: curious
- Keywords float in from the right (stagger 0.1s, slide + fade, monospace `#aaa`)
- Idle bounce continues

**Step 3: Swallow (1.5-2.2s)**
- Expression: processing
- Cap inflates: `capRy` increases by 15% (spring easing with overshoot)
- Keywords scale down toward cap center, fade out

**Step 4: Ready (2.2-3.0s)**
- Expression: proud
- Cap color lerps to final semantic color (ease-out, 0.5s)
- Cap shape morphs to final shape (if different from dome)
- `capRy` returns to normal (ease-out, 0.3s)
- One final small hop

After the ceremony, the Mogu is the concept and the main visualization begins.

**Timing control:**
```javascript
var time = 0; // seconds, incremented each frame by dt

if (time >= 1.5 && time < 2.2) {
  var stepTime = time - 1.5;
  var stepDuration = 0.7;
  var t = Math.min(stepTime / stepDuration, 1);
  var inflateAmount = ease.spring(t, 0.5);
  capRy = baseCapRy * (1 + 0.15 * inflateAmount);
}
```

**Color interpolation (RGB lerp):**
```javascript
function lerpColor(hex1, hex2, t) {
  var r1 = parseInt(hex1.substring(1, 3), 16);
  var g1 = parseInt(hex1.substring(3, 5), 16);
  var b1 = parseInt(hex1.substring(5, 7), 16);
  var r2 = parseInt(hex2.substring(1, 3), 16);
  var g2 = parseInt(hex2.substring(3, 5), 16);
  var b2 = parseInt(hex2.substring(5, 7), 16);
  var r = Math.round(r1 + (r2 - r1) * t);
  var g = Math.round(g1 + (g2 - g1) * t);
  var b = Math.round(b1 + (b2 - b1) * t);
  return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}
```

## Quick Reference Links

- **MoguScene engine: `components/mogu-engine.js`** — load this in generated HTML, write only scene code
- Character spec: `references/character.md`
- Scene archetypes: `references/scenes.md`
- Interaction patterns: `references/interactions.md`
- Complete examples: `references/examples.md`
- Canonical SVG: `components/mogu.svg`
- Expression variants: `components/mogu-expressions.svg`
- Low-level drawing code (for reference, not direct use): `components/widgets.js`
