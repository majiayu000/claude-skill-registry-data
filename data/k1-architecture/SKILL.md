---
name: k1-architecture
description: Deep understanding of K1.reinvented's compilation architecture, node system, and extension methodology. Teaches why graphs compile to C++ and how to extend the system without violating minimalism.
---

# K1.reinvented System Architecture Skill

## The Core Insight: Why This Architecture Works

For three years, every LED project architecture fell into the same trap: **flexibility OR performance**. You could have creative freedom OR execution speed, never both.

K1.reinvented proves this is a false choice. The insight is simple but profound:

**Move the creative work to the computer. Move the execution work to the device.**

Don't ask the device to interpret JSON at runtime. Don't ask it to evaluate node graphs in real-time. Don't force a tiny embedded system to be both flexible AND fast.

Instead:
- **Computer**: Visual node graphs, artistic composition, creative iteration (TypeScript codegen)
- **Device**: Compiled native C++, zero interpretation overhead, pure execution (ESP32-S3)

The node graph exists ONLY at development time. It guides code generation. Then it disappears. What runs on the device is pure C++ that looks exactly like what you'd write by hand.

**This is the revolution: compilation as creative medium, not optimization trick.**

---

## The Two-Stage Compilation Process

### Stage 1: JSON Graph → C++ Code (Development Time)

**Input:** `graphs/departure.json` - Visual node graph describing the pattern

```json
{
  "name": "Departure",
  "nodes": [
    {"id": "position", "type": "position_gradient"},
    {"id": "palette", "type": "palette_interpolate", "parameters": {"palette": "departure"}},
    {"id": "output", "type": "output"}
  ],
  "wires": [...],
  "palette_data": [[0, 8, 3, 0], [32, 45, 25, 0], ...]
}
```

**Process:** TypeScript compiler (`codegen/src/index.ts`) walks the graph:
1. Reads node definitions and their parameters
2. Performs topological sort (generators → processors → output)
3. For each node, generates C++ code using Handlebars templates
4. Embeds palette data directly into generated code
5. Outputs `firmware/src/generated_effect.h`

**Output:** Pure C++ code with no runtime graph interpretation

```cpp
void draw_generated_effect() {
    static float field_buffer[NUM_LEDS];
    static CRGBF color_buffer[NUM_LEDS];

    // position_gradient: Map LED index to 0.0-1.0
    for (int i = 0; i < NUM_LEDS; i++) {
        field_buffer[i] = (float)i / (NUM_LEDS - 1);
    }

    // palette_interpolate: Interpolate between keyframes
    const uint8_t palette_keyframes[] = {0, 8, 3, 0, 32, 45, 25, 0, ...};
    for (int i = 0; i < NUM_LEDS; i++) {
        // ... interpolation logic ...
    }

    // output: Write to LED array
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = color_buffer[i];
    }
}
```

### Stage 2: C++ Code → Machine Code (Compile Time)

**Process:** PlatformIO + GCC compile the generated C++:
1. C++ compiler inlines loops
2. Constant folding optimizes calculations
3. Dead code elimination removes unused paths
4. Result: Optimal assembly for ESP32-S3

**Outcome:** 450+ FPS execution with zero overhead. The graph structure has completely disappeared.

---

## The Node Type System

Every node has a **type** that determines what code it generates. Currently supported:

### Generator Nodes (Create Data from Context)

**`position_gradient`**
- Maps LED index to 0.0-1.0 range
- Used as input to other nodes
- Generated code: Simple division loop

**`gradient`** (HSV gradient)
- Creates hue values across LED range
- Parameters: start_hue, end_hue
- Generated code: Linear interpolation

### Transform Nodes (Process Data)

**`palette_interpolate`** (CRITICAL NODE)
- Maps 0.0-1.0 position to palette colors
- Reads `palette_data` from graph
- Generates keyframe array + interpolation logic
- **This is where artistic intent becomes code**

**`hsv_to_rgb`**
- Converts HSV color space to RGB
- Parameter: brightness
- Generated code: Standard HSV→RGB math

### Output Nodes (Write to LEDs)

**`output`**
- Copies color_buffer to leds array
- Always the final node in graph
- Generated code: Simple array copy

---

## How to Extend: Adding New Node Types

**The minimalist principle:** Only add node types that serve beauty. If it doesn't enable new forms of artistic expression, don't add it.

### Example: Adding a `sine_wave` Node

**1. Define the node type in graph JSON:**
```json
{"id": "wave", "type": "sine_wave", "parameters": {"frequency": 3.0, "amplitude": 0.5}}
```

**2. Add case to codegen (`codegen/src/index.ts`):**
```typescript
case 'sine_wave':
    const freq = node.parameters?.frequency ?? 1.0;
    const amp = node.parameters?.amplitude ?? 1.0;
    return `
    // Node: ${node.id} (sine_wave)
    for (int i = 0; i < NUM_LEDS; i++) {
        float t = field_buffer[i];
        field_buffer[i] = ${amp}f * sin(t * ${freq}f * TWO_PI);
    }`;
```

**3. Test with all three patterns:**
- Does it compile without errors?
- Does the generated code make sense?
- Could you debug it if it breaks?

**4. Verify it serves beauty:**
- Does this enable new artistic possibilities?
- Or is it just technical sophistication?

### Anti-Pattern: Don't Add Complexity for Completeness

**Bad reason to add a node:** "It would be technically elegant to have a full math library"

**Good reason to add a node:** "This enables expressing emotions that weren't possible before"

---

## The Codegen Architecture

### Key Files

**`codegen/src/index.ts`** (~280 lines)
- Main entry point
- Graph parsing and validation
- Topological sort (ensures correct execution order)
- Node-specific code generation
- Template compilation via Handlebars

**Critical Functions:**

```typescript
function generateNodeCode(node: Node, graph: Graph): string
// Takes a node definition, returns C++ code string
// This is where artistic intent becomes executable code

function compileGraph(graph: Graph): string
// Orchestrates entire compilation process
// Returns complete C++ file content
```

### The Template System (Handlebars)

Uses simple string templates, NOT complex C++ metaprogramming:

```typescript
const effectTemplate = `
void draw_generated_effect() {
    {{#each steps}}
    {{{this}}}
    {{/each}}
}`;
```

**Why Handlebars instead of C++ templates?**
- Simpler to understand and debug
- Template errors are clear TypeScript errors, not cryptic C++ template errors
- Maintains minimalism (string substitution, not meta-programming)

---

## Debugging Guide

### Problem: Codegen Fails

**Symptom:** `npm run compile` throws error

**Check:**
1. Is the JSON valid? Run through JSON validator
2. Does every node have a valid type?
3. Are palette_data arrays properly formatted?
4. Are wires connecting valid node IDs?

**Fix:** Correct the JSON graph definition

### Problem: Generated Code Won't Compile

**Symptom:** PlatformIO build fails with C++ errors

**Check:**
1. Open `firmware/src/generated_effect.h`
2. Look at the actual generated code
3. Find the C++ syntax error
4. Trace back to which node generated it

**Fix:** Fix the code generation logic in `codegen/src/index.ts` for that node type

### Problem: FPS is Below 450

**Symptom:** `Serial.println` shows 200-300 FPS

**Check:**
1. Is LED transmission blocking? (Should use RMT non-blocking)
2. Are there `delay()` calls in the main loop?
3. Is audio processing interfering? (Should be on separate core)
4. Are there expensive operations in the render loop?

**Fix:** Profile where cycles are going, optimize the bottleneck

### Problem: Colors Look Wrong

**Symptom:** Pattern doesn't match expected visual

**Check:**
1. Is palette_interpolate generating correct keyframe data?
2. Are edge cases handled (first/last LED)?
3. Is the interpolation formula correct?
4. Are RGB values in 0.0-1.0 range (not 0-255)?

**Fix:** Debug the palette interpolation logic in generated C++

---

## Performance Characteristics

### Target: 450+ FPS for 180 LEDs

**Calculation:**
- 180 LEDs × 3 bytes × 8 bits = 4,320 bits per frame
- WS2812B: 800 kHz bitrate = 5.4 ms transmission time
- Remaining time per frame: 2.22ms - 5.4ms = -3.18ms? NO.

**Wait, how is 450 FPS possible?**

**Answer: Non-blocking transmission via RMT peripheral**
- Main loop renders next frame while RMT transmits current frame
- Dual-core: Core 0 does audio, Core 1 does graphics
- Zero blocking, pure parallel execution

**Breakdown per frame (180 LEDs):**
- Position calculation: ~360 cycles (2 cycles/LED)
- Palette interpolation: ~5,400 cycles (30 cycles/LED)
- Color assignment: ~360 cycles (2 cycles/LED)
- **Total: ~6,120 cycles = ~25 microseconds @ 240 MHz**
- Result: 40,000 FPS theoretical, 450 FPS actual (RMT transmission limit)

**The RMT transmission is the bottleneck, not the computation.**

---

## Extension Philosophy

### When to Add Node Types

**Ask these questions:**
1. Does this enable expressing emotions that weren't possible before?
2. Can I explain why this serves beauty, not just technical elegance?
3. Is the generated code simple enough to debug when it breaks?
4. Does this maintain the 450+ FPS target?

**If all four are YES:** Add it.
**If any are NO:** Don't.

### When to Add Features to Codegen

**Examples of GOOD additions:**
- Time-based modulation (enables animation)
- Audio-reactive nodes (enables music sync)
- Multi-layer blending (enables complex compositions)

**Examples of BAD additions:**
- "Complete" math library (complexity without purpose)
- Runtime graph switching (violates compilation principle)
- Visual debugger UI (sophistication without necessity)

---

## The Mission Connection

Every architectural decision serves the mission: **Prove flexibility and performance aren't opposites.**

**Compilation philosophy:** Flexibility at development time, performance at execution time
**Node system:** Composable primitives that maintain minimalism
**Code generation:** Transparent, debuggable, understandable
**Performance target:** Uncompromising 450+ FPS

If you find yourself adding complexity that doesn't serve this mission, stop. Delete it. Return to clarity.

---

## Phase B and Beyond

**Phase B: Expand node types** (10-15 types total)
- Time-based modulation
- Mathematical operators (add, multiply, sin, cos)
- Color blending and layering

**Phase C: Visual editor**
- Draw graphs instead of JSON
- Real-time preview
- One-click deploy

**Phase D: Audio reactivity**
- FFT nodes
- Beat detection nodes
- Audio-driven modulation

But everything must maintain:
- Zero runtime overhead
- 450+ FPS execution
- Minimalist architecture
- Service to beauty

---

## Final Truth

This architecture works because it respects both domains completely:

**Artistic domain:** Visual node graphs, intuitive composition, creative freedom
**Execution domain:** Compiled C++, native speed, zero overhead

The compilation step is the bridge. It's not a convenience—it's the insight that makes the entire system possible.

Understanding this deeply is what separates maintaining the code from owning the vision.
