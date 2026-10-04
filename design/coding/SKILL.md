---
name: coding
description: Coding patterns, architectural best practices, and runtime failure modes
---

# Skill: Software Coding Agent

You are an expert developer agent. You write, inspect, and execute clean, production-grade code.

## ⚠️ CRITICAL INVARIANTS (Apply immediately)

1. **CSS HEIGHTS IN `%` AND height=0 = VISUAL FAILURE MODE #1** (visualizers, bars, charts):
   - **NEVER set `bar.style.height = '0px'` upon creation**:
     - ❌ `const bar = document.createElement('div'); bar.style.height = '0px'; container.appendChild(bar);`
     - ✅ `const bar = document.createElement('div'); bar.style.height = (value * 3) + 'px'; container.appendChild(bar);` (Visible on load)
   - `height: 80%` ONLY works if direct parent has an EXPLICIT `height` (not just `min-height`).
   - Vertical bars container MUST be `display: flex; flex-direction: row; align-items: flex-end;` with explicit inline pixel heights. NEVER use `flex-direction: column; flex: 1;` on vertical bars.

2. **PURE VANILLA JAVASCRIPT inside `<script>`**: No TypeScript syntax (`: type`, `as`, `interface`, `: void`, `?` parameter markers) -> causes SyntaxError and blank page.

3. **PYTHON CALL TERMINATION `)` NOT `}`**: When tool call arguments contain `{}` (JS/CSS code), close the Python call with `)`, never `}`.

4. **CANONICAL ANIMATION LOOP — RENDER & REFRESH STATE AT EACH STEP**:
   - Canvas OR DOM div, NEVER mixed.
   - Re-render state and UI text within the async loop:
     ```js
     async function bubbleSort() {
         for (let i = 0; i < data.length - 1; i++) {
             if (data[i] > data[i + 1]) { [data[i], data[i+1]] = [data[i+1], data[i]]; }
             comparisons++;
             counterEl.textContent = comparisons;   // Update UI counter in loop
             draw();                                 // Redraw state in loop
             await sleep(delay);                     // await sleep delay (50-300ms)
         }
     }
     ```

5. **DYNAMIC CONTROLS & EVENT WIRING**:
   - Every interactive button (`#startBtn`, `#pauseBtn`, `#resetBtn`, `#stepBtn`) MUST have an active `addEventListener('click', ...)` attached.
   - Every slider (`#speedRange`, `#sizeRange`) MUST have an `addEventListener('input', ...)` attached that updates the runtime parameters and UI label dynamically.

6. **ROBUST SCRIPT INITIALIZATION (NEVER BARE DOMContentLoaded)**:
   - When scripts are placed at the bottom of the `<body>` or evaluated dynamically, `DOMContentLoaded` may have ALREADY fired (`document.readyState === 'complete'`), causing a bare `document.addEventListener('DOMContentLoaded', ...)` listener to NEVER trigger and leaving the board blank.
   - ALWAYS initialize using the robust readyState pattern:
     ```js
     function init() { generateArray(); }
     if (document.readyState === 'loading') {
         document.addEventListener('DOMContentLoaded', init);
     } else {
         init();
     }
     ```

## Dynamic Resources (Progressive Disclosure)

- **[resources/quand_utiliser_quels_outils.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/coding/resources/quand_utiliser_quels_outils.md)**: Tool selection matrix.
- **[resources/r_gles_d_or.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/coding/resources/r_gles_d_or.md)**: Golden development rules.
- **[resources/format_de_r_ponse_final.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/coding/resources/format_de_r_ponse_final.md)**: Final response format.
