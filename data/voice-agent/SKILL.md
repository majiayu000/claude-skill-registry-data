---
name: voice-agent
description: Add OpenAI Realtime API voice agent to a Next.js presentation. Use when adding voice interactivity, realtime audio, AI presenter, or voice navigation to slides. Triggers on "voice agent", "realtime API", "audio presentation", "AI presenter", "voice navigation".
---

# Voice Agent for Presentations

Add an OpenAI Realtime API voice agent that presents slides, interacts with users, answers questions, and navigates via tool calls.

## Prerequisites

- Existing Next.js presentation with slide components
- `OPENAI_API_KEY` in `.env.local`

## Effort Distribution

| Phase | Effort | Description |
|-------|--------|-------------|
| 1. Infrastructure | 10% | Copy core files, wire up providers |
| 2. Customize Framework | 10% | Set presentation metadata, tweak personas |
| 3. Design Voice Engagement | 80% | Six passes: narrative, content, engagement, hints, progression, pacing |

**The creative work is Phase 3.** Phases 1-2 are mechanical setup.

Phase 3 breaks down into six passes:
- **Pass 1:** Extract narrative from existing docs (10%)
- **Pass 2:** Content foundation for each slide (20%)
- **Pass 3:** Engagement design for each slide (25%)
- **Pass 4:** UI interactivity hints (10%)
- **Pass 5:** Progression design for each slide (15%)
- **Pass 6:** Pacing and over-engagement signals (10%)

---

## Phase 1: Infrastructure Setup

This phase is mechanical file copying and integration. Use sub-agents to create files in parallel.

### Step 1.1: Copy Core Files

Read each source file from [files/](files/) and write it to the target path. These are complete, working files - no modification needed.

| Target Path | Source |
|-------------|--------|
| `lib/realtime/types.ts` | [files/types.ts](files/types.ts) |
| `lib/realtime/tools.ts` | [files/tools.ts](files/tools.ts) |
| `app/api/realtime-token/route.ts` | [files/realtime-token-route.ts](files/realtime-token-route.ts) |
| `hooks/useRealtimeConnection.ts` | [files/useRealtimeConnection.ts](files/useRealtimeConnection.ts) |
| `hooks/useAuditionSession.ts` | [files/useAuditionSession.ts](files/useAuditionSession.ts) |
| `components/voice-agent/VoiceAgentContext.tsx` | [files/VoiceAgentContext.tsx](files/VoiceAgentContext.tsx) |
| `components/voice-agent/VoiceAgentButton.tsx` | [files/VoiceAgentButton.tsx](files/VoiceAgentButton.tsx) |
| `components/voice-agent/index.ts` | [files/voice-agent-index.ts](files/voice-agent-index.ts) |

### Step 1.2: Copy Template File

Copy this file - it has `// TODO:` markers that you'll customize in Phase 2:

| Target Path | Source |
|-------------|--------|
| `lib/realtime/instructions.ts` | [files/instructions-template.ts](files/instructions-template.ts) |

### Step 1.3: Integrate with Existing App

Modify these **existing files** to wire up the voice agent. Don't replace the files - add to them.

**app/layout.tsx** - Add provider wrapper and button:
- Import `VoiceAgentProvider` and `VoiceAgentButton` from `@/components/voice-agent`
- Wrap `{children}` with `<VoiceAgentProvider>`
- Add `<VoiceAgentButton />` inside the provider, after children

```tsx
// Add these imports
import { VoiceAgentProvider, VoiceAgentButton } from '@/components/voice-agent';

// In the return, wrap children:
<VoiceAgentProvider>
  {children}
  <VoiceAgentButton />
</VoiceAgentProvider>
```

**Presentation component** (e.g., `components/slides/Presentation.tsx`) - Register navigation:
- Import `useVoiceAgent` hook
- Call `registerNavigationCallbacks` with your navigation functions
- Call `setSlideOverview` with slide metadata
- Call `setCurrentSlide` when the current slide changes

```tsx
import { useVoiceAgent } from '@/components/voice-agent';

// Inside the component:
const { registerNavigationCallbacks, setCurrentSlide, setSlideOverview } = useVoiceAgent();

// On mount - register how the agent can navigate
useEffect(() => {
  registerNavigationCallbacks({
    goToNext: () => /* your next slide logic */,
    goToPrevious: () => /* your prev slide logic */,
    goToSlide: (index) => /* your go-to-slide logic */,
    getCurrentSlide: () => currentSlide,
    getTotalSlides: () => slides.length,
  });
  setSlideOverview(slides.map(s => ({ id: s.id, title: s.title })));
}, []);

// When slide changes - keep agent informed
useEffect(() => {
  setCurrentSlide({
    id: slides[currentSlide].id,
    title: slides[currentSlide].title,
    slideNumber: currentSlide + 1,
    totalSlides: slides.length,
  });
}, [currentSlide]);
```

Adapt the callback implementations to match how your presentation handles navigation.

---

## Phase 2: Customize Framework

Open `lib/realtime/instructions.ts` and customize the `// TODO:` sections:

### Required: Presentation Metadata

```typescript
// TODO: Set your presentation details
const PRESENTATION = {
  title: 'Your Presentation Title',
  topic: 'What your presentation is about...',
  runningExample: 'Description of your main example or demo...',
  targetAudience: 'Who this is for and their background...',
  coreFramework: `
    1. **First Concept** - Brief description
    2. **Second Concept** - Brief description
    3. **Third Concept** - Brief description
  `,
};
```

### Optional: Persona Customization

The default personas work well for most presentations:
- **Sophie (guide)** - Warm, encouraging, patient
- **Marcus (coach)** - Direct, challenging, high-energy
- **Claire (expert)** - Clear, precise, structured
- **Sam (peer)** - Casual, exploratory, collaborative

To customize persona names or add presentation-specific phrases, edit the `personas` object.

### Optional: Audition Instructions

If using persona auditions, update `buildAuditionInstructions()` to reference your presentation's content.

### Optional: Landing Page

A landing page lets users configure their experience before starting. It should include:

- **Voice toggle** - Enable/disable the voice agent
- **Mode selection** - Choose interaction style (presenter, dialogue, assistant)
- **Persona selection** - Choose guide personality, optionally with "audition" preview
- **Start handler** - Set mode/persona and auto-start the session

When auto-starting the session from a `useEffect`, wrap `startSession` in `useEffectEvent` to prevent double-starts during the connection handshake.

See [files/LandingPage-example.tsx](files/LandingPage-example.tsx) for a complete reference implementation.

---

## Phase 3: Design Voice Engagement

**This is where you spend most of your effort.** Work through four focused passes, each building on the last. Don't try to do everything at once.

### Pass 1: Extract Narrative

Your presentation already has narrative documentation (NARRATIVE.md, SLIDES.md, or similar). Extract and codify it for the voice agent.

Create `lib/slide-contexts/overview.ts`:

```typescript
// Extracted from NARRATIVE.md and SLIDES.md
// This is reference material for writing consistent slide contexts

export const PRESENTATION_OVERVIEW = `
# [Your Presentation Title] - Overview

## The Story Arc

[Extract from NARRATIVE.md - the journey you're taking users on]

### Introduction (Slides X-Y): [Section purpose]
- [What happens in this section]
- [Key moments]

### [Section Name] (Slides X-Y)
- [What this section covers]
- [How it connects to the previous section]

[Continue for each major section...]

## Key Narrative Principles

- [Principles from your narrative - e.g., "progressive revelation"]
- [What themes to reinforce throughout]
- [How concepts connect to each other]
`;

export const RUNNING_EXAMPLE = `
## Running Example: [Your Example Name]

[Extract details about your main example/demo that threads through the presentation]

- What it is
- How it's used throughout
- What can go wrong (if relevant)
`;
```

**Focus:** Codify what already exists. Pull from NARRATIVE.md and SLIDES.md - don't invent new narrative.

**Why this matters:** When writing individual slide contexts, you'll reference this to ensure consistency. Every slide context should align with the overall story arc.

---

### Pass 2: Content Foundation

For each slide, create `lib/slide-contexts/slides/slide-XX-name.ts` with just the **factual content**:

```typescript
import { SlideContext } from '@/lib/realtime/instructions';

export const slideContext: SlideContext = {
  // PASS 2: What's here and what matters
  visualDescription: `
    Describe what the user sees on screen.
    Include layout, UI elements, interactive controls.
    Note current state if the slide is stateful.
  `,
  keyPoints: [
    'First key concept (2-4 total)',
    'Second key concept',
  ],
  backgroundKnowledge: `
    Deeper context for answering questions.
    Technical details, common misconceptions.
    Related concepts the user might ask about.
  `,

  // PASS 3: Leave empty for now
  engagementApproach: '',
  openingHook: '',
  interactionPrompts: [],
  transitionToNext: '',
};
```

**Focus:** Accuracy and completeness. What does the user see? What should they learn? What might they ask?

Use sub-agents to create multiple slides in parallel. Then create the index file:

```typescript
// lib/slide-contexts/index.ts
import { setSlideContext } from '@/lib/realtime/instructions';
import { slideContext as slide01 } from './slides/slide-01-title';
// ... more imports

export const slideContexts = { 'title': slide01, /* ... */ };

export function initializeSlideContexts(): void {
  for (const [id, ctx] of Object.entries(slideContexts)) {
    setSlideContext(id, ctx);
  }
}

// Re-export overview for reference
export { PRESENTATION_OVERVIEW, RUNNING_EXAMPLE } from './overview';
```

---

### Pass 3: Engagement Design

Now go back through each slide and fill in the **engagement strategy**. Reference your overview to ensure each slide fits the narrative arc.

```typescript
  // PASS 3: How to engage
  engagementApproach: `
    What's the unique strategy for THIS slide?
    e.g., "guided discovery", "pose question first", "create tension"
  `,
  openingHook: `
    The first thing to say when arriving on this slide.
    Should feel natural spoken aloud.
  `,
  interactionPrompts: [
    'Try clicking [element] to see what happens',
    'What do you think will happen if...?',
    'Have you encountered this in your own work?',
  ],
  transitionToNext: `
    How to naturally lead into the next slide.
    Creates continuity in the narrative.
  `,
```

**Vary your approach.** Don't use the same pattern on every slide:

| Slide Type | Pattern |
|------------|---------|
| Title/Intro | Build anticipation, establish rapport |
| Running example | Guided discovery - "try clicking X" |
| Concept reveal | Pose problem first, then reveal |
| Interactive demo | Encourage experimentation |
| Limitation/problem | Create cognitive tension |
| New section | "Level unlocked" excitement |
| Skeptic/objection | Address concerns conversationally |
| Recap | Reinforce key points, call to action |

**Focus:** Personality and flow. Read the opening hooks aloud - do they sound natural? Does each slide feel different? Do transitions connect to the narrative arc from your overview?

See [SLIDE-CONTEXT-PATTERN.md](SLIDE-CONTEXT-PATTERN.md) for detailed examples by slide type.

---

### Pass 4: UI Interactivity

For slides with interactive elements, add `sendHint()` calls to the slide components. This keeps the agent informed about user actions.

```typescript
import { useVoiceAgent } from '@/components/voice-agent';

export default function SlideXX({ isActive }: SlideProps) {
  const { sendHint } = useVoiceAgent();

  const handleButtonClick = () => {
    sendHint('User clicked Process. The AI is evaluating...');
    // ... do the action
    sendHint('Processing complete. Result: score 4/5 with reasoning about...');
  };
}
```

**Add hints for:**
- Button clicks (before and after async operations)
- Toggle/tab changes
- Accordion expansions
- Quiz answers
- Any state change the agent should know about

**Focus:** Context richness. Include what happened, not just what was clicked.

See [SEND-HINT-PATTERN.md](SEND-HINT-PATTERN.md) for patterns and examples.

---

### Pass 5: Progression Design

Review each slide context as if building from scratch for voice. Define clear exit conditions and progression signals.

For each slide, add:

```typescript
  // PASS 5: When is this slide "done"?
  slideGoal: `
    What should the user understand or experience before leaving?
    Be specific - this is the exit condition.
  `,
  progressionTrigger: `
    What signals it's time to move on?
    - User completed a specific action
    - User demonstrated understanding
    - User asked about what's next
    - For static slides: agent covered key points and user had chance to ask questions
  `,
```

**Questions to ask for each slide:**

1. What's the ONE thing the user must take away?
2. What interaction or acknowledgment signals they got it?
3. For static slides with no clicks: what content must the agent deliver before moving on?

**Progression trigger types:**

| Slide Type | Typical Trigger |
|------------|-----------------|
| Interactive demo | User completed the interaction AND acknowledged the insight |
| Concept reveal | User engaged with revealed content or asked clarifying question |
| Synthesis/static | Agent delivered both sides of comparison, user had chance to respond |
| Problem setup | User expressed concern or asked about solutions |
| Recap | User identified next action or explored summary content |

**Avoid:**
- Time-based triggers (agent can't track time)
- Vague triggers like "user seems ready"
- Triggers that require mind-reading

**Focus:** Clear, observable exit conditions. If you can't tell whether the trigger happened, it's too vague.

---

### Pass 6: Pacing and Over-Engagement

The agent should follow user interest, but not keep introducing new threads on its own. Define limits on agent-initiated engagement.

For each slide, add:

```typescript
  // PASS 6: Agent pacing
  agentPacing: {
    maxAgentQuestions: 2,  // How many questions before offering to move on
    ifUserPassive: `
      What to do if user gives brief responses or doesn't engage.
      Usually: give a concise overview, offer to explore or move on.
    `,
  },
  overEngagementSignals: [
    'Specific signs the agent is lingering too long',
    'E.g., user giving one-word responses',
    'Agent has asked multiple questions without substantive engagement',
  ],
```

**The key principle:** Agent-initiated exploration has a budget. User-initiated exploration is unlimited.

- If user wants to go deep on something → follow their lead
- If user is passive or brief → don't keep probing, offer value and move forward

**Typical budgets by slide type:**

| Slide Type | Agent Questions | If User Passive |
|------------|-----------------|-----------------|
| Intro/Title | 1-2 | Give overview, show example |
| Interactive demo | 1-2 | Walk through one path, offer more |
| Concept reveal | 1 check | Summarize key point, transition |
| Static synthesis | 0-1 | Deliver insight, check for questions |
| Skeptic/objection | 1 | Give key defense, acknowledge validity |
| Recap | 1 | Highlight most common starting point |

**Over-engagement signals to watch for:**

- User giving one-word or minimal responses to multiple questions
- User not clicking suggested interactions after prompting
- Agent has asked 3+ questions without substantive user engagement
- Conversation circling same points without new insight
- User explicitly asking to move on or see something else

**Focus:** Respect user attention. The agent's job is to be helpful, not to fill airtime.

---

## Interaction Modes

The voice agent supports three interaction modes:

| Mode | Who Drives | Best For |
|------|-----------|----------|
| **presenter** | Agent leads | Structured walkthroughs, demos |
| **dialogue** | Shared turn-taking | Learning, exploration, engagement |
| **assistant** | User leads | Self-paced study, reference |

Set via `setMode('dialogue')` on the voice agent context. Default is `'dialogue'`.

---

## Testing Checklist

- [ ] Microphone permission works
- [ ] Connection establishes (check console for "session created")
- [ ] Navigation tools work (agent says "next" -> slide advances)
- [ ] Hints flow through on interactions
- [ ] Slide context updates when navigating
- [ ] Persona voice sounds correct

---

## Architecture

For technical decisions and WebRTC flow, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Troubleshooting

**Agent doesn't start talking:**
- Ensure `response.create` is sent after connection (this happens automatically in useRealtimeConnection)
- Check that instructions are being passed to the token endpoint

**Navigation doesn't work:**
- Verify `registerNavigationCallbacks` is called with correct functions
- Check console for function call events

**Hints not reaching agent:**
- Verify `status === 'connected'` before sending
- Check data channel is open in console

**Wrong voice:**
- Check persona -> voice mapping in instructions.ts
- Verify voice is being passed to token endpoint
