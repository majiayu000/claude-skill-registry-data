---
name: dzmm-builder
description: Comprehensive skill for building, debugging, and optimizing DZMM.AI applications. Use this skill when users request creating interactive web apps on the DZMM platform, need guidance on DZMM API usage, or require help with existing DZMM applications. Covers AI-driven chatbots, visual novels, dating sims, content generators, RPG games, content platforms, and visual effect systems. Includes state management games, message management (reroll/edit/delete), multi-opening systems, rich text rendering, modular prompt engineering, resource reuse strategies, React/Vue to DZMM migration, and responsive mobile design.
---

# DZMM Builder

## Overview

Build AI-driven interactive web applications on the DZMM.AI platform using specialized knowledge, complete examples, and reusable code patterns. This skill provides comprehensive support for creating single-file HTML applications that leverage streaming AI conversations, cloud key-value storage, and browser effect systems.

## When to Use This Skill

Invoke this skill when users:
- Request creating a new DZMM application ("Build me a DZMM chatbot", "Create an AI story generator", "Make a dating sim game", "Build a social media content generator", "Create a visual novel", "Build an interactive fiction game")
- Ask questions about DZMM API usage ("How do I use dzmm.completions?", "How does KV storage work?", "How to parse structured AI output?", "How to use chat API for branching stories?", "How to implement streaming AI responses?")
- Need help debugging DZMM applications ("My DZMM app returns 400 error", "AI responses are not displaying", "State not persisting", "DZMM API not initializing")
- Want to optimize existing DZMM apps (performance, user experience, architecture improvements, mobile responsiveness, reduce token usage)
- Ask about "fourth wall breaking" effects or browser control from AI
- Need guidance on state management in games (stats, mood, relationships, dynamic UI)
- Want to integrate Markdown rendering or rich text formatting (nested structures, dialogue quotes, options buttons)
- Request configuration/setup UI for applications
- Need branching narrative systems (Galgame save/load, multi-route stories, choice history tracking)
- Ask about available models and their performance characteristics
- **Request message management features** ("How to add reroll/regenerate?", "How to let users edit messages?", "How to delete conversation branches?")
- **Want multi-opening/multi-scenario systems** ("How to add multiple starting scenes?", "How to switch between different story routes?")
- **Need help migrating from React/Vue to DZMM** ("How to migrate my app to DZMM?", "What's the DZMM equivalent of useState?", "Can I use React/TypeScript with DZMM?", "How to build DZMM apps with modern frameworks?", "vite-plugin-singlefile for DZMM", "My DZMM app has sandbox errors", "Form submission blocked in DZMM", "localStorage not working in DZMM", "HTTP 400 error with DZMM API", "maxTokens limit exceeded")
- **Ask about resource management** ("How to load images/audio in DZMM?", "Should I use URLs or embed resources?")

## Core Capabilities

### 1. Application Generation

Generate complete, single-file HTML applications for the DZMM platform based on user requirements.

**Approach:**
1. Clarify the application type and core features
2. Select an appropriate architecture pattern (stateless generator, stateful dialogue, or layered cache platform)
3. Use example templates from `assets/examples/` as foundation
4. Customize for specific requirements
5. Test the complete flow (initialization → AI call → display)

**Architecture Patterns:**

**Stateless Generator** - For one-shot content generation:
- Example: Translator, text summarizer, content creator, social media post generator
- No conversation history or state persistence
- Simplest architecture, fastest development
- Optional: Integrate marked.js for Markdown rendering
- Reference: See `assets/examples/小红书文案.html` for minimal implementation
- Code snippets: `references/code-snippets.md` section 2

**State Management Game** - For interactive games with dynamic variables:
- Example: Dating sims, RPG games, decision-based narratives
- Multiple state variables (stats, mood, time, relationships)
- Structured AI output parsing (###STATE/###END format)
- Configuration UI for game initialization
- State-driven UI updates (progress bars, backgrounds, effects)
- Auto-save with KV storage
- Reference: See `assets/examples/恋爱游戏.html` for complete implementation

**Stateful Dialogue System** - For multi-turn conversations:
- Example: Chatbots, interactive stories, Q&A systems
- Maintains conversation history
- Uses Alpine.store for state management
- Persists state with KV storage
- Reference: See `assets/examples/dungeon-adventure.html` and `assets/examples/horror-story.html`

**Layered Cache Platform** - For content communities:
- Example: Forums, story libraries, content platforms
- Two-tier caching (list cache + detail cache)
- On-demand content generation
- Concurrent request locking
- Reference: See `assets/examples/贴吧.html` for full implementation

**Visual Novel / Galgame System** - For narrative-driven interactive fiction:
- Example: Visual novels, interactive stories, AI-driven narrative games
- Multi-opening scene system with dynamic switching
- Rich text rendering with placeholder technique (handles nested structures)
- Message management (reroll, edit, delete with context preservation)
- Multi-slot save/load system with preview
- Modular prompt system (main prompt + character + guidance + emphasis)
- Responsive mobile design with compressed UI
- Reference: See yoshiwara-chronicles project for complete implementation
- Key features: XML-structured prompts, <last_input> emphasis, streaming AI responses

### 2. API Integration Guidance

Provide detailed guidance on using DZMM's specialized APIs.

**Core APIs:**

**window.dzmm.completions()** - Streaming AI generation:
```javascript
await window.dzmm.completions(
  {
    model: 'nalang-turbo-0826' | 'nalang-medium-0826' |
           'nalang-max-0826' | 'nalang-xl-0826' |
           'nalang-max-0826-16k' | 'nalang-xl-0826-16k',
    messages: [{ role: 'user' | 'assistant', content: string }],
    maxTokens: number  // Optional, 200-3000, default 1000
  },
  (newContent, done) => {
    // newContent is cumulative, not incremental
    // done is true when generation completes
  }
);
```

**window.dzmm.chat** - Tree-structured conversation storage (⭐ NEW):
```javascript
// Insert messages into conversation tree (supports branching storylines)
const result = await window.dzmm.chat.insert(parentId, [
  { role: 'user', content: 'Player choice' },
  { role: 'assistant', content: 'Story response' }
]);
const newMessageIds = result.ids; // Array of new message IDs

// Get message details (with parent/children relationships)
const messages = await window.dzmm.chat.list(['msg-123', 'msg-124']);
// Returns: [{ id, role, content, timestamp, parent, children }, ...]

// Get complete conversation timeline
const timeline = await window.dzmm.chat.timeline(messageId);
const fullHistory = await window.dzmm.chat.list(timeline);
```
**Use cases:** Galgame save/load systems, branching narratives, multi-route stories, interactive fiction with choice history.

**window.dzmm.kv** - Cloud key-value storage:
```javascript
// Save (auto-serializes objects)
await window.dzmm.kv.put(key, value);

// Load
const result = await window.dzmm.kv.get(key);
if (result.value) {
  const data = result.value;
}

// Delete
await window.dzmm.kv.delete(key);
```
**Limits:** Keys ≤256 chars, values ≤1MB recommended. Development mode: data lost on refresh. Production: persistent.

**Critical Requirements:**
- Must wait for `dzmm:ready` event before any API calls
- Only `user` and `assistant` roles supported (no `system`)
- Limit conversation history to ≤20 messages to avoid token overflow
- maxTokens range: 200-3000, default 1000
- Concurrent requests: ≤3 recommended
- Use versioned keys for KV storage (e.g., `app_state_v1`)

**Reference:** Consult `references/developer-guide.md` sections 2-3 for complete API documentation and `references/code-snippets.md` sections 1-3 for ready-to-use code patterns.

### 3. Effect System Implementation

Implement "fourth wall breaking" effects where AI can control the user's browser environment.

**Effect Categories:**

**Visual Effects:**
- Light control (dimming, darkness, flickering)
- Screen shake (low/medium/high intensity)
- Glitch effects
- Color filters (blood, blur, etc.)

**Audio Effects:**
- Programmatic sound generation (beeps, drones, heartbeats)
- Web Audio API without external files
- Ambient and tension-building sounds

**Dynamic Elements:**
- Particle systems (dust, blood, explosions)
- Jumpscare popups
- Element manipulation

**Implementation Pattern:**

```javascript
// 1. AI outputs special instructions
const aiPrompt = `When the user says "turn off lights", output:
###EFFECT
{"action":"lights","params":{"state":"off"}}
###END`;

// 2. Parse and execute
const effectMatch = content.match(/###EFFECT\s*({[\s\S]*?})\s*###END/);
if (effectMatch) {
  const effect = JSON.parse(effectMatch[1]);
  executeEffect(effect);
  // Remove instruction from display
  content = content.replace(/###EFFECT[\s\S]*?###END/, '').trim();
}

// 3. Effect executor
function executeEffect(effect) {
  switch(effect.action) {
    case 'lights':
      document.body.classList.add(`lights-${effect.params.state}`);
      break;
    // ... more effects
  }
}
```

**Reference:** See `assets/examples/horror-story.html` for complete effect system with CSS animations, Web Audio, and Canvas particles.

### 4. Debugging and Optimization

Diagnose and fix common DZMM application issues.

**Common Issues:**

**HTTP 400 Errors:**
- Cause: Using `role: 'system'` in messages (not supported)
- Fix: Convert system prompts to first `user` message or maintain in frontend variables
- Cause: Messages array contains undefined/null values
- Fix: Validate and sanitize messages before sending

**No Response from AI:**
- Cause: API not ready yet
- Fix: Ensure `dzmm:ready` event is awaited before any API calls

**Context Overflow:**
- Cause: Too many messages or overly long content
- Fix: Slice messages array to last 10-20 items, truncate individual messages to 2000 chars

**State Not Persisting:**
- Cause: KV key naming conflicts or version mismatch
- Fix: Use versioned keys with unique identifiers

**Form Submission Blocked (Public Release Only):**
- Cause: DZMM public release uses iframe sandbox without `allow-forms` permission
- Error: `Blocked form submission to '' because the form's frame is sandboxed`
- Fix: Replace `<form>` with `<div>`, use `@click` instead of `@submit.prevent`
- Example:
  ```html
  <!-- ❌ WRONG: Will fail in public release -->
  <form @submit.prevent="handleSubmit()">
    <button type="submit">Submit</button>
  </form>

  <!-- ✅ CORRECT: Works in all environments -->
  <div>
    <button type="button" @click="handleSubmit()">Submit</button>
  </div>
  ```
- Note: This only affects public release, not development mode or workshop preview

**Performance Optimization:**
- Debounce user input to reduce API calls
- Implement two-tier caching for content-heavy apps
- Use concurrent request locks to prevent duplicate API calls
- Limit conversation history proactively

**Reference:** Consult `references/developer-guide.md` section "常见问题" for comprehensive troubleshooting guide.

### 5. Code Patterns and Snippets

Provide reusable, production-ready code patterns for common DZMM tasks.

**Available Patterns:**
1. Initialization and API readiness (dual detection with timeout)
2. AI completions (basic, multi-turn, streaming with real-time display)
3. KV storage operations (save, load, delete, multi-slot, batch operations)
4. Chat API operations (branching narratives, save/load, timeline retrieval)
5. Instruction parsing systems (JSON, XML, ###STATE format)
6. Alpine.js state management (local and global stores)
7. Visual effect systems (CSS animations, particles, audio)
8. Error handling and structured logging (retry with exponential backoff)
9. Utility functions (debounce, sanitize, scroll control)
10. Prompt templates (structured output, XML hierarchy, emphasis sections)
11. Complete application templates
12. **Rich text rendering** (placeholder technique for nested structures)
13. **Message management** (reroll, edit, delete with context preservation)
14. **Multi-opening system** (scene switching with state management)
15. **Resource management** (URL-based asset loading, preloading)
16. **Modular prompt system** (main + character + guidance + emphasis)
17. **Responsive layout patterns** (mobile-first with Tailwind breakpoints)

**Usage:** Reference `references/code-snippets.md` for copy-paste ready code snippets organized by category. All snippets are tested and can be used directly or with minimal modifications.

**New Visual Novel Patterns (from yoshiwara-chronicles):**
- Rich text parser with placeholder technique
- Message reroll/edit/delete functions
- Opening scene switcher with confirmation
- Multi-slot save system with preview extraction
- Streaming AI response with auto-scroll
- XML-structured prompt builder
- Resource manager for external assets

## Workflow Guide

### For New Applications

1. **Clarify Requirements**
   - Determine application type (chatbot, game, content platform, etc.)
   - Identify core features and interactions
   - Choose architecture pattern

2. **Select Template**
   - Browse `assets/examples/` for similar applications:
     - `小红书文案.html` - Simple content generator, Markdown rendering
     - `恋爱游戏.html` - Dating sim, multi-variable state management
     - `horror-story.html` - Effect system, immersive experience
     - `dungeon-adventure.html` - Turn-based game, state management
     - `neon-gomoku.html` - AI opponent, game logic
     - `贴吧.html` - Content platform, two-tier caching

3. **Build Application**
   - Start with HTML structure and Alpine.js integration
   - Implement DZMM API initialization (wait for `dzmm:ready`)
   - Add AI completions with appropriate model selection
   - Implement state management and KV storage if needed
   - Add visual effects or advanced features as required

4. **Test and Refine**
   - Test initialization and API readiness
   - Verify AI responses and parsing
   - Check state persistence across page reloads
   - Optimize performance (history limits, debouncing)

### For Debugging Existing Applications

1. **Identify the Issue**
   - Review error messages and console logs
   - Check network requests in browser DevTools
   - Verify API readiness timing

2. **Diagnose Root Cause**
   - Cross-reference with common issues in `references/developer-guide.md`
   - Check message format compliance (only `user`/`assistant`)
   - Validate conversation history length

3. **Apply Fix**
   - Use code patterns from `references/code-snippets.md`
   - Add error handling if missing
   - Implement validation for user inputs and API responses

4. **Optimize**
   - Add performance improvements (caching, debouncing)
   - Improve user experience (loading states, error messages)
   - Enhance code maintainability (structured logging, modularity)

### For Migrating React/Vue Applications to DZMM

**Two Approaches Available:**

#### Approach A: Keep React/Vue Framework (Recommended for Large Projects)

Use modern build tools to maintain component-based development, then bundle to single HTML.

**Tech Stack**: React + TypeScript + Vite + vite-plugin-singlefile

**Workflow**:
1. **Setup**: `npm create vite@latest my-app -- --template react-ts`
2. **Install Plugin**: `npm install -D vite-plugin-singlefile`
3. **Configure Vite**: Add plugin for single-file build mode
4. **Develop**: Keep existing React components structure
5. **Build**: `npm run build:single` → generates standalone HTML
6. **Deploy**: Upload to DZMM platform

**Key Considerations**:
- ✅ Keep TypeScript type safety and component modularity
- ✅ Hot reload during development
- ✅ Rich ecosystem (shadcn/ui, React Router, etc.)
- ⚠️ Handle sandbox restrictions (localStorage, form submission)
- ⚠️ Enforce maxTokens limits (200-3000)
- ⚠️ Prevent consecutive same-role messages in API calls

**Critical Fixes**:
- **localStorage**: Implement fallback to memory storage
- **Forms**: Replace `<form>` with `<div>` + button onClick
- **maxTokens**: Never exceed 3000 (API returns HTTP 400)
- **Messages**: Merge emphasis into last user message to avoid consecutive roles

**See**: Q11 in `references/developer-guide.md` for complete implementation guide

#### Approach B: Rewrite to Alpine.js (Lightweight Alternative)

Convert component hierarchy to single HTML with Alpine.js reactive sections.

1. **Assessment**
   - Identify existing resources (images, audio, fonts) - **these will be reused via URLs**
   - Map React/Vue components to Alpine.js x-show pages
   - List state variables (useState/Vuex → Alpine data)
   - Inventory API calls (fetch → dzmm.completions/kv)

2. **Resource Strategy (Critical)**
   - **DO NOT recreate visual assets with CSS** - use GitHub Raw URLs
   - Collect all image/audio file URLs from original project
   - Create resource manager object with base URL
   - Use Google Fonts or existing font CDN links
   - **Goal**: 100% visual fidelity, not approximate simulation

3. **Structure Migration**
   - Convert component hierarchy to single HTML with x-show sections
   - Convert state management:
     - `useState` → Alpine reactive data properties
     - `useEffect` → Alpine `x-init` or watchers
     - `props` → Alpine function parameters or computed properties
   - Convert event handlers: `onClick={fn}` → `@click="fn"`

4. **API Migration**
   - Replace `fetch('/api/chat')` with `dzmm.completions()`
   - Convert localStorage to `dzmm.kv` operations (or safe storage wrapper)
   - Add `dzmm:ready` event waiting
   - Implement streaming callbacks if needed

5. **Feature Additions (from yoshiwara-chronicles patterns)**
   - Add message management (reroll, edit, delete)
   - Implement rich text rendering with placeholder technique
   - Add multi-opening system if applicable
   - Implement modular prompt system
   - Add responsive mobile optimizations

6. **Testing and Refinement**
   - Verify all resources load correctly (images, audio)
   - Test DZMM API initialization
   - Check mobile responsiveness (375px, 768px, 1920px)
   - Validate state persistence with KV storage
   - Test on actual DZMM platform (dev and production modes)

**Comparison**:
| Factor | React + Vite | Alpine.js |
|--------|--------------|-----------|
| Type Safety | ✅ TypeScript | ❌ Plain JS |
| Dev Experience | ✅ Hot reload | ⚠️ Manual refresh |
| Ecosystem | ✅ Rich (shadcn/ui, etc.) | ⚠️ Limited |
| File Size | ⚠️ Larger (900KB+) | ✅ Smaller (<100KB) |
| Maintenance | ✅ Component-based | ⚠️ Single file can get messy |
| Learning Curve | ⚠️ Steeper for beginners | ✅ Easier to learn |

## Model Selection Guide

Choose the appropriate DZMM AI model based on task complexity:

**Standard Models (32K context):**
- **nalang-turbo-0826**: Fastest, most economical. Best for simple tasks, quick responses (maxTokens: 1000-1500)
- **nalang-medium-0826**: Balanced performance. Good for moderate complexity tasks (maxTokens: 1500-2000)
- **nalang-max-0826**: Enhanced reasoning and strategy. Best for game AI, complex rules, stable output (maxTokens: 2000-3000)
- **nalang-xl-0826**: Largest model, strongest comprehension. For complex dialogues, long-form content (maxTokens: 2000-3000)

**16K Models (faster, shorter context):**
- **nalang-max-0826-16k**: Fast version of max model with 16K context window
- **nalang-xl-0826-16k**: Fast version of XL model with 16K context window

**Legacy Model Names (may still work in some examples):**
- `nalang-xl` → likely maps to `nalang-xl-0826`
- `nalang-xl-10` → likely maps to `nalang-xl-0826`

**Selection Tips:**
- For prototyping: Start with `nalang-turbo-0826` for speed
- For production games: Use `nalang-max-0826` or `nalang-xl-0826` for quality
- For short conversations: Try 16K variants for faster response
- All models support maxTokens range: 200-3000 (default 1000)

## Resources

### references/developer-guide.md
Complete DZMM platform developer guide covering:
- Platform introduction and tech stack
- Core API documentation with examples
- Three architecture patterns with full implementations
- Best practices for prompts, error handling, performance
- Comprehensive FAQ and troubleshooting
- Design philosophy and logging strategies

Load this reference when users need in-depth understanding of DZMM concepts, detailed API specifications, or comprehensive architecture guidance.

### references/code-snippets.md
Organized library of reusable code patterns:
- 10 categories covering all common DZMM tasks
- Copy-paste ready snippets
- Complete with comments and usage examples
- Tested and production-ready

Load this reference when implementing specific features or need quick access to proven code patterns.

### assets/examples/
Seven complete, working DZMM applications:

1. **小红书文案.html** (~15KB) - Stateless Generator
   - Minimal architecture for quick prototyping
   - Markdown rendering with marked.js integration
   - Input validation with character count
   - Modern gradient UI design
   - Single-purpose content generation
   - Best for: Quick tools, text generators, one-shot tasks

2. **恋爱游戏.html** (~35KB) - State Management Game
   - Multi-variable state system (affection, mood, time, relationship)
   - Structured AI output with ###STATE/###END parsing
   - Configuration UI for game initialization
   - Dynamic UI updates (progress bars, backgrounds)
   - Complete save/load system with state filtering
   - Responsive mobile design with extensive @media queries
   - Best for: Dating sims, stat-based games, visual novels

3. **horror-story.html** (29KB) - Effect System
   - Comprehensive effect system (lights, sounds, particles, visual effects)
   - AI-controlled browser environment
   - "Fourth wall breaking" implementation
   - Web Audio API sound generation
   - Canvas particle system
   - Best for: Immersive experiences, atmospheric games

4. **dungeon-adventure.html** (41KB) - Turn-based Game
   - Turn-based game with state management
   - Character stats and inventory system
   - Multi-turn AI dialogue with context
   - JSON parsing for game state updates
   - Best for: RPG games, adventure games

5. **neon-gomoku.html** (24KB) - Board Game
   - AI opponent for board games
   - Game logic and win detection
   - Structured AI instruction parsing
   - Visual game board rendering
   - Best for: Strategy games, puzzle games

6. **贴吧.html** (26KB) - Content Platform
   - Two-tier caching architecture
   - List + detail content loading
   - Concurrent request locking
   - XML parsing for content structure
   - Best for: Forums, content communities, social platforms

7. **yoshiwara-chronicles-dzmm.html** (84KB) - Complete Visual Novel System (Alpine.js) ⭐
   - **Multi-opening system** with dynamic scene switching (Night Chapter, Day Chapter)
   - **Rich text rendering** with placeholder technique (handles nested options, dialogue quotes, italics)
   - **Message management** (reroll/regenerate, edit, delete with context preservation)
   - **Multi-slot save system** (3 slots with preview extraction)
   - **Modular prompt engineering** (XML-structured with main + character + guidance + emphasis sections)
   - **Advanced prompt techniques** (`<last_input>` emphasis, token optimization, format rules at bottom)
   - **Streaming AI responses** with real-time display and auto-scroll
   - **Responsive mobile design** (compressed navigation, flex-wrap buttons, adaptive spacing)
   - **Resource reuse pattern** (GitHub Raw URLs for background images)
   - Complete implementation of all visual novel patterns documented in this skill
   - Best for: Visual novels, interactive fiction, narrative-driven games, Galgames
   - **Reference project**: Based on 54-commit development of yoshiwara-chronicles

8. **yoshiwara-chronicles-react** (893KB, gzip: 473KB) - React Multi-Component Version 🚀
   - **Same project as #7**, but built with **React + TypeScript + Vite**
   - **Component-based architecture**: 30+ modular TypeScript/TSX files
   - **Professional codebase structure**: services/lib/contexts/types layered design
   - **Complete DZMM API encapsulation** with TypeScript type safety
   - **Sandbox compatibility layer**: localStorage fallback, form submission handling
   - **Automatic API parameter validation**: maxTokens range checking, consecutive role detection
   - **Production-ready error handling**: Detailed logging, validation, graceful degradation
   - **Modern build pipeline**: Vite + vite-plugin-singlefile (hot reload → single HTML)
   - **All features from Alpine.js version** plus improved maintainability
   - Best for: Large projects (>5000 lines), team collaboration, TypeScript projects
   - **Full source code**: https://github.com/waylon256yhw/yoshiwara-chronicles/tree/dzmm-version
   - **Documentation**: `assets/react-examples/yoshiwara-chronicles-react.md`
   - **Key learning**: Q11 (React/Vue migration guide), Q12 (backend integration templates)

Use these as starting templates or reference implementations for specific features.

## Best Practices

1. **Always Initialize Properly**
   - Wait for `dzmm:ready` event before any API call
   - Initialize AudioContext on first user interaction (browser requirement)
   - Show loading state during initialization
   - Use dual detection: check `window.dzmm` directly + event listener + timeout recheck
   - Example pattern:
   ```javascript
   if (window.dzmm) {
     this.dzmmReady = true;
   } else {
     window.addEventListener('dzmm:ready', () => { this.dzmmReady = true; });
     setTimeout(() => {
       if (!this.dzmmReady && window.dzmm) this.dzmmReady = true;
     }, 2000);
   }
   ```

1.5. **⚠️ Resource Reuse Strategy (Critical for Migrations)**
   - **Golden Rule**: If resources already exist, ALWAYS reference them by URL instead of recreating with code
   - **Use GitHub Raw URLs** for images, audio, fonts from existing projects
   - **Never simulate textures** with CSS gradients/shadows - use real image files
   - **100% visual fidelity** vs ≤60% with code simulation
   - Benefits: Perfect restoration, time savings, smaller file size, easier maintenance
   - Example:
   ```html
   <!-- ✅ CORRECT: Direct URL reference -->
   <div style="background-image: url('https://raw.githubusercontent.com/user/repo/main/public/image.jpg')">

   <!-- ❌ WRONG: CSS simulation of textures -->
   <div style="background: linear-gradient(...); box-shadow: inset ...">
   ```
   - **Resource Manager Pattern**:
   ```javascript
   const ASSET_BASE = 'https://raw.githubusercontent.com/user/repo/main/public';
   const assets = {
     backgrounds: { welcome: `${ASSET_BASE}/bg1.jpg` },
     music: [{ src: `${ASSET_BASE}/music/track1.mp3` }]
   };
   ```
   - **Migration Checklist**: All images referenced? All audio referenced? Fonts from CDN? Any simulated textures replaceable?

2. **Manage Conversation History**
   - Keep only last 10-20 messages to prevent token overflow
   - Truncate individual messages to reasonable lengths (≤2000 chars)
   - Use system prompts as first user message, not `role: 'system'`

3. **Handle Errors Gracefully**
   - Wrap all API calls in try-catch blocks
   - Provide user-friendly error messages
   - Log structured context for debugging (model, message count, error)

4. **Optimize Performance**
   - Implement debouncing for user input
   - Use two-tier caching for content-heavy apps
   - Add concurrent request locks to prevent duplicate calls
   - Clean up resources (audio nodes, animation frames, particles)

5. **Design Clear Prompts with Format Control**
   - Use structured output formats (###STATE/###END, XML, or JSON)
   - **Provide both correct AND incorrect examples in prompts**
   - Explicitly warn AI what NOT to do (e.g., "❌ Don't put dialogue before STATE")
   - Use clear delimiters and validate parsing
   - Example from 恋爱游戏.html:
   ```javascript
   【正确示例】
   用户:早上好
   回复:
   ###STATE
   {"affection":52,"mood":"高兴"}
   ###END
   早上好呀!

   【错误示例 - 绝对不要这样】
   ❌ 把对话写在STATE前面
   ❌ 不写STATE
   ```

6. **Smart State Persistence**
   - **Exclude temporary state** from saves (disabled, loading, input)
   - Only save game-critical data
   - Use Object.assign() for clean state restoration
   - Example pattern:
   ```javascript
   const excludeKeys = ['disabled', 'loading', 'input'];
   const saveData = {};
   Object.keys(this).forEach(key => {
     if (!excludeKeys.includes(key) && typeof this[key] !== 'function') {
       saveData[key] = this[key];
     }
   });
   ```

7. **Responsive Design for Mobile**
   - Design for touch interactions first
   - Use extensive @media queries for layout adjustments
   - Test text readability on small screens (14-16px minimum)
   - Ensure buttons are finger-friendly (min 44px touch targets)
   - Hide non-essential labels on mobile to save space

8. **Configuration UI Pattern**
   - Provide initial setup screen for user customization
   - Include game/app instructions in setup
   - Validate inputs before allowing start
   - Example: name input, difficulty selection, initial parameters

9. **Markdown Integration (for content generators)**
   - Load marked.js before Alpine.js
   - Configure marked options once: `marked.setOptions({ breaks: true, gfm: true })`
   - Render with `x-html="renderMarkdown(content)"`
   - Style rendered HTML with specific CSS selectors (`.post-body h1`, `.post-body p`, etc.)

10. **Version Your Data**
    - Use versioned keys for KV storage (e.g., `app_state_v1`)
    - Include timestamps for cache expiry checks
    - Document data schema changes

11. **Use Chat API for Branching Narratives**
    - Perfect for Galgame save/load systems with multiple routes
    - Store each player choice and story branch as separate messages
    - Use `parentId` to create branching storylines at decision points
    - Track current position with last message ID
    - Load history with `timeline()` for save/load functionality
    - Example pattern:
    ```javascript
    // Save choice and branch
    const result = await dzmm.chat.insert(currentNodeId, [
      { role: 'user', content: playerChoice },
      { role: 'assistant', content: storyResponse }
    ]);
    currentNodeId = result.ids[result.ids.length - 1];
    localStorage.setItem('savePoint', currentNodeId);

    // Load save
    const timeline = await dzmm.chat.timeline(savedNodeId);
    const history = await dzmm.chat.list(timeline);
    ```

12. **Respect API Limits**
    - **Concurrent requests**: Keep ≤3 simultaneous API calls
    - **Call frequency**: Add debouncing to avoid rapid-fire requests
    - **Message size**: Limit individual messages to reasonable lengths
    - **Development vs Production**: Remember data persistence differs between modes
    - Use loading states to prevent duplicate requests during processing

13. **Rich Text Rendering with Placeholder Technique**
    - **Problem**: Nested structures (like `<options>` inside AI responses) conflict with regex replacements
    - **Solution**: Extract complex structures → process simple text → restore structures
    - **Pattern**:
    ```javascript
    renderRichText(text) {
      // 1. Extract options blocks with placeholders
      const optionsMap = [];
      let result = text.replace(/<options>([\s\S]*?)<\/options>/g, (match, content) => {
        const placeholder = '___OPTIONS_' + optionsMap.length + '___';
        optionsMap.push(content);
        return placeholder;
      });

      // 2. Process regular text (italics, quotes, line breaks)
      result = result
        .replace(/\*([^*]+)\*/g, '<em>$1</em>')
        .replace(/「([^」]+)」/g, '<span class="dialogue">「$1」</span>')
        .replace(/\n/g, '<br>');

      // 3. Restore options as HTML buttons
      optionsMap.forEach((content, i) => {
        const buttons = /* generate buttons from content */;
        result = result.replace('___OPTIONS_' + i + '___', buttons);
      });
      return result;
    }
    ```
    - **Use data attributes** to avoid HTML quote conflicts: `<button data-option="${escaped}">`
    - **Event delegation** for dynamic buttons: Single click handler with `event.target.closest('[data-option]')`

14. **Message Management Features**
    - **Reroll (Regenerate)**: Preserve context before target message, call API with same history
    - **Edit**: Update user message, delete all subsequent messages, auto-trigger AI response
    - **Delete**: Slice array to remove message and everything after it
    - **Key implementation details**:
    ```javascript
    // Reroll: preserve context
    const contextMessages = this.messages.slice(0, messageIndex);
    // Edit: delete subsequent + auto-respond
    this.messages = this.messages.slice(0, index + 1);
    await this.getAIResponse(editedContent, false);
    // Delete: with confirmation
    if (confirm('Delete this and all following messages?')) {
      this.messages = this.messages.slice(0, index);
    }
    ```
    - Use `editingIndex` and `rerollingIndex` for UI state tracking
    - Always clean `<options>` tags from history to prevent AI format inertia

15. **Multi-Opening Scene System**
    - **Configuration**: Array of opening objects `[{ id: 'night', label: '夜之章' }]`
    - **Content library**: Object mapping `{ night: 'content...', day: 'content...' }`
    - **State management**: Track `selectedOpening` and `previousOpening` for cancel support
    - **Pattern**:
    ```javascript
    changeOpening() {
      if (this.messages.length > 1) {
        if (!confirm('Switch will clear conversation. Continue?')) {
          this.selectedOpening = this.previousOpening; // Revert
          return;
        }
      }
      this.previousOpening = this.selectedOpening;
      this.messages = [];
      this.messages.push({ role: 'assistant', content: this.getOpeningGreeting() });
    }
    ```
    - Extensible design: Easy to add new openings to array and content object

16. **Responsive Mobile Design**
    - **Top navigation**: Use `flex-col md:flex-row` for vertical (mobile) → horizontal (desktop)
    - **Button overflow**: Add `flex-wrap` and `gap-1.5` to allow wrapping
    - **Text scaling**: `text-xs md:text-sm` for responsive font sizes
    - **Decorative elements**: Hide on mobile with `hidden md:block`
    - **Compressed spacing**: Reduce padding/margin on mobile (e.g., `py-4 → py-1.5`)
    - **Fixed layout**: Use `h-screen` + `flex-1` + `flex-shrink-0` for header/content/footer
    - **Touch targets**: Minimum 44px for buttons on mobile
    - **Whitespace control**: `whitespace-nowrap` to prevent button text wrapping
    - Test at: 375px (iPhone SE), 768px (iPad), 1920px (Desktop)

17. **Advanced Prompt Engineering**
    - **XML Structure**: Use tags like `<时代背景>`, `<创作美学>`, `<回复规范>` for clear hierarchy
    - **Emphasis section**: Put critical format rules at BOTTOM of message array (AI remembers recent content better)
    - **Message construction**:
    ```javascript
    const messages = [
      { role: 'user', content: systemPrompt },     // Top: World/character setting
      ...cleanedHistory,                           // Middle: Conversation
      { role: 'user', content: getEmphasis() }     // Bottom: Format rules (strongest)
    ];
    ```
    - **<last_input> wrapper**: Emphasize most recent user input
    ```javascript
    for (let i = cleanedMessages.length - 1; i >= 0; i--) {
      if (cleanedMessages[i].role === 'user') {
        cleanedMessages[i].content = `<last_input>\n${cleanedMessages[i].content}\n</last_input>`;
        break;
      }
    }
    ```
    - **Token optimization**: Simplify repeated tags (`<option>` → `<op>` saves ~12 chars × 3)
    - **Clean history**: Remove `<options>` blocks from history to prevent AI format inertia

18. **KV Storage Advanced Patterns**
    - **Multi-slot saves with preview**:
    ```javascript
    // Save: Full game state
    await dzmm.kv.put(`game_slot_${slotNumber}`, JSON.stringify({
      character, messages, timestamp, ...gameState
    }));

    // Preview: Extract metadata only (don't load full messages)
    const data = JSON.parse(result.value);
    return {
      characterName: data.character.name,
      messageCount: data.messages.length,
      lastMessage: data.messages[messages.length-1].content.slice(0, 50),
      timestamp: new Date(data.timestamp).toLocaleString()
    };
    ```
    - **Batch operations**: Use `Promise.all()` for parallel KV operations
    - **Versioning**: Use keys like `${appName}_v2_${dataKey}` for schema upgrades
    - **Chunking**: Split large data if hitting size limits
    - **Caching with expiry**: Store `{ value, expiresAt }` and check timestamp on load

19. **Streaming AI Response Optimization**
    - **Real-time display**: Update UI in callback with `done === false`
    - **Placeholder message**: Add empty message to array, update content in callback
    - **Auto-scroll**: Use `$nextTick()` to ensure DOM updated before scrolling
    - **Error recovery**: Remove placeholder message if API fails
    - **Retry logic**: Implement exponential backoff (1s, 2s, 4s) for failed requests
    - **Pattern**:
    ```javascript
    this.messages.push({ role: 'assistant', content: '' });
    const idx = this.messages.length - 1;
    await dzmm.completions({ /* ... */ }, (content, done) => {
      this.messages[idx].content = content;
      if (done) {
        this.$nextTick(() => scrollToBottom());
      }
    });
    ```

## Writing Style Note

Follow DZMM conventions:
- Use imperative/infinitive verb forms in instructions
- Maintain objective, instructional tone
- Provide concrete examples with actual code
- Reference bundled resources explicitly
- Keep explanations concise and actionable
