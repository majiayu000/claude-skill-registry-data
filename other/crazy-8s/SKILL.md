---
name: crazy-8s
version: 1.0.0
description: Solo rapid ideation method based on Google Design Sprint Crazy 8's exercise. Generates 8 distinct solution ideas in 8 minutes through rapid-fire ideation or sketch documentation. Use when working alone and need to explore multiple solution directions quickly, push beyond first obvious ideas, or generate variety before converging. Includes creativity warm-up questions, built-in timer, optional creative constraints, and generates visual HTML/CSS prototypes plus comparison table. NOT for team sessions (traditional Crazy 8's works better for teams).
---

# Crazy 8's (Solo Version)

Rapid ideation method that pushes you to generate 8 distinct solution ideas in 8 minutes. Based on Google Design Sprint's Crazy 8's exercise, adapted for solo work with AI assistance.

## What This Skill Does

- Facilitates solo rapid ideation sessions with 8-minute timer
- Offers optional creativity warm-up with provocative questions
- Supports two modes: rapid-fire ideation or sketch documentation
- Generates HTML/CSS prototypes for quick visualization
- Creates comparison table for decision-making
- Pushes beyond first obvious ideas through speed and constraints

## What This Skill Does NOT Do

- Facilitate team Crazy 8's (traditional physical method works better for teams)
- Make decisions about which ideas are best (you decide)
- Create high-fidelity designs (these are rough prototypes)
- Guarantee all 8 ideas are good (quantity over quality is the goal)

## Core Principle

**Speed kills the inner critic.** You don't have time to overthink. The goal is divergent thinking - weird, impractical, and bold ideas often spark the truly innovative ones. Not all 8 ideas will be winners, and that's perfect.

## Workflow Decision Tree

**Start:** "I want to do a Crazy 8's session"

**Step 1:** Claude asks about the design challenge
→ You describe the problem and context

**Step 2:** Claude asks: "Want a quick creativity warm-up? (adds ~2 minutes)"
→ **Yes:** Claude asks 2-3 provocative questions to spark ideas
→ **No:** Skip directly to mode selection

**Step 3:** Claude asks: "Which mode?"
→ **Rapid Ideation:** You rapid-fire ideas, Claude generates prototypes
→ **Sketch Documentation:** You sketch on paper, then share photos

**Step 4:** Claude asks: "What are you designing?"
→ Mobile app, web app, dashboard, feature, etc.

**Step 5:** Claude asks: "Want creative constraints for more variety?"
→ Optional constraints based on Google methodology

**Step 6:** Claude creates timer artifact and session begins

## Creativity Warm-Up (Optional)

If you choose the warm-up, Claude asks 2-3 fast questions (30 seconds each) to activate divergent thinking. These are provocative, brain-stretching questions selected from `references/icebreaker-questions.md` based on your problem.

### Example Warm-Up Flow

**Claude:** "Let me spark some ideas with quick questions - answer instinctively!"

**Question examples:**
- "What if this was designed for your most impatient user?"
- "What if this felt more like a game than a [product type]?"
- "What would the most delightful version look like?"

**You answer quickly** (no overthinking - 20-30 seconds each)

**Claude captures responses** and says: "Perfect! Keep that energy. Ready for the timer?"

### Benefits

- Activates divergent thinking before time pressure
- Seeds unexpected directions
- Reduces blank-page anxiety
- Takes only 2 minutes but increases idea variety

**Note:** If you skip warm-up, jump straight to mode selection. The warm-up is helpful but optional.

## Mode 1: Rapid Ideation

Best for speed, remote work, and when you think better by talking than sketching.

### How It Works

1. **Timer starts** - Claude creates React timer artifact (8:00 countdown)
2. **You rapid-fire ideas** - Short phrases describing solution directions
   - "Card-based feed layout"
   - "Timeline view with filters"
   - "Conversational interface"
   - etc.
3. **Claude captures** - Confirms each idea (✅ or numbered acknowledgment)
4. **Timer ends** - Either automatic or you say "done"
5. **Claude generates** - HTML/CSS prototypes for all 8 ideas in grid layout
6. **Claude creates** - Comparison table for review

### During the Session

**Your role:**
- Don't stop to explain - just name the idea
- Don't judge ideas as you go - save critique for later
- Keep moving - if you get 8 before time ends, keep going
- Embrace weird ideas - they often spark great ones

**What to say:**
- Short descriptive phrases (3-7 words)
- "Split-screen dashboard"
- "Gesture-based navigation"
- "Voice-first interface"
- "Minimalist card design"

**What NOT to do:**
- Don't elaborate during the 8 minutes
- Don't ask Claude to develop ideas yet
- Don't critique your own ideas
- Don't slow down to sketch (that's the other mode)

### After Timer Ends

Claude generates:

**1. Visual Prototypes**
- Single HTML artifact with 8-grid layout
- Each idea rendered as quick HTML/CSS prototype
- Mobile or web viewport based on your context
- Rough but concrete enough to evaluate

**2. Comparison Table**
- All 8 ideas listed with descriptions
- Key features for each
- Patterns and themes observed
- Recommendations for next steps

## Mode 2: Sketch Documentation

Best when you think spatially, want traditional Crazy 8's feel, or prefer drawing to typing.

### How It Works

1. **Timer starts** - Claude creates React timer artifact (8:00 countdown)
2. **You sketch on paper** - Fold paper into 8 sections, sketch one idea per section
3. **Timer ends** - Put pen down
4. **You photograph** - Take photo(s) of your sketches
5. **You upload** - Share images with Claude
6. **Claude analyzes** - Interprets each sketch
7. **Claude generates** - Descriptions + optional HTML/CSS prototypes
8. **Claude creates** - Comparison table

### Sketching Tips

**Materials:**
- One sheet of paper, folded into 8 rectangles
- Thick marker or pen (forces simplicity)
- Timer visible while you work

**Sketching approach:**
- Rough rectangles and basic shapes
- Label key elements
- Use arrows for interactions
- Don't worry about beauty - communication over art

**What makes a good sketch:**
- Clear enough that someone else could understand it
- Shows the key differentiator of this idea
- Includes 2-3 UI elements minimum

### After Upload

Claude analyzes each sketch and provides:

**1. Written Descriptions**
- What Claude sees in each sketch
- Key UI patterns identified
- Interaction suggestions based on arrows/annotations
- Metaphors or inspirations detected

**2. Optional Prototypes**
- HTML/CSS versions of your sketches
- Best-effort interpretation
- You can request refinements

**3. Comparison Table**
- Same as Rapid Ideation mode

## Creative Constraints (Optional)

Before timer starts, you can add constraints to push for more variety. Based on Google Design Sprint methodology.

**Claude asks:** "Want creative constraints to increase variety?"

**Options:**

**Interaction Types:**
- Vary: touch, voice, gesture, AI-assisted, mixed modality
- Example: "Make ideas 1-3 touch-based, 4-6 voice-first, 7-8 gesture"

**User Contexts:**
- Vary: desktop, mobile, tablet, AR/VR, wearable
- Example: "Explore mobile-first, desktop, and one AR idea"

**Emotional Tones:**
- Vary: calm, data-driven, playful, serious, energetic
- Example: "Try playful, professional, and meditative approaches"

**Metaphors:**
- Vary: timeline, gallery, chat, map, game, tool, etc.
- Example: "What if it was organized like: a chat, a map, a game?"

**When to use constraints:**
- When your first few ideas feel similar
- When you want to force variety
- When exploring a new problem space

**When to skip:**
- When you already have diverse ideas in mind
- When constraints feel limiting rather than liberating

## The Timer Artifact

Claude creates a React component featuring:

```
┌─────────────────────────┐
│   CRAZY 8'S TIMER       │
│                         │
│  📖 How It Works [+]    │
│                         │
│        08:00            │
│    [progress bar]       │
│                         │
│  Ideas Generated 0/8    │
│  [■ ■ ■ ■ ■ ■ ■ ■]     │
│   ✓ Idea Captured       │
│                         │
│      [START] [RESET]    │
│                         │
│  💡 Dynamic tips here   │
└─────────────────────────┘
```

**Features:**
- Countdown from 8:00 to 0:00
- Collapsible "How It Works" instructions
- Start/Pause/Reset controls
- Ideas counter with "Idea Captured" button
- Visual indication when time ends
- Clean, minimal interface with gradient design

**Smart Urgency System:**
Each of the 8 idea blocks represents a 1-minute window and blinks red during the last 30 seconds of its window:
- Block 1 blinks: 7:30 → 7:00 (time for first idea!)
- Block 2 blinks: 6:30 → 6:00 (second idea!)
- Block 3 blinks: 5:30 → 5:00
- ...and so on through all 8 blocks

This creates a rolling wave of urgency and provides visual pacing feedback. You can tell at a glance if you're ahead or behind the "1 minute per idea" target. Once you capture an idea, its block turns solid purple/blue.

**Timer ends when:**
- Countdown reaches 0:00, OR
- You say "done" or "finished"

**Time's Up Message:**
When timer hits 0:00, a large animated alert appears:
- "⏰ TIME'S UP!"
- "👉 Tell Claude 'done' in the chat"
- Explains Claude will generate prototypes and comparison table

## Visual Prototypes Output

After ideation, Claude generates one artifact with 8 prototypes in grid:

```html
<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px;">
  <!-- 8 prototype blocks -->
  <div class="idea-1">
    <h3>1. [Idea Name]</h3>
    <div class="prototype">
      [HTML/CSS mockup]
    </div>
  </div>
  <!-- ... repeat for all 8 -->
</div>
```

**Each prototype includes:**
- Idea number and name
- Visual representation (HTML/CSS)
- Mobile or desktop viewport
- Basic interactivity where relevant

**Quality level:**
- Quick and rough (not production-ready)
- Concrete enough to evaluate and discuss
- Shows key differentiators between ideas
- Takes 2-3 minutes to generate all 8

## Comparison Table Output

After prototypes, Claude generates structured comparison:

```markdown
# Crazy 8's Results: [Your Challenge]

## The 8 Ideas

### 1. [Idea Name]
**Description:** [What it is]
**Key Features:**
- Feature A
- Feature B
- Feature C
**Interaction Pattern:** [How users interact]
**Visual Approach:** [Layout/style]
**Unique Angle:** [What makes this different]

[Repeat for all 8 ideas]

---

## Quick Comparison Matrix

| # | Idea | Complexity | Novelty | User Value | Feasibility |
|---|------|-----------|---------|-----------|-------------|
| 1 | [Name] | Low/Med/High | Low/Med/High | Low/Med/High | Low/Med/High |
...

---

## Patterns Observed

**Common Themes:**
- [Pattern across multiple ideas]
- [Recurring approach]

**Unique Approaches:**
- [Standout idea 1 and why]
- [Standout idea 2 and why]

**Interesting Tensions:**
- [Competing philosophy A vs B]

---

## Recommended Next Steps

**For Prototyping:**
- [Top 2-3 ideas with rationale]

**For Combining:**
- [Ideas that could be merged]

**For Research:**
- [Ideas that need user validation]
```

## Best Practices

### For All Sessions

**Before starting:**
- Have your design challenge clearly defined
- Know your target platform (mobile/web/etc)
- Remove distractions - focus for 8 minutes

**During the 8 minutes:**
- Speed over quality - first idea to mind
- Don't critique as you go
- Embrace weird/impractical ideas
- If stuck, make something up and keep moving

**After timer ends:**
- Review all ideas before judging any
- Look for patterns across ideas
- Notice which ideas excite you most
- Consider combinations of ideas

### For Rapid Ideation Mode

**Effective idea phrases:**
- ✅ "Dashboard with real-time activity feed"
- ✅ "Gesture-controlled navigation"
- ✅ "Conversational onboarding flow"

**Less effective:**
- ❌ "Something with cards" (too vague)
- ❌ "Like Instagram but different" (need more specificity)
- ❌ Full sentences explaining rationale (too slow)

**Pacing:**
- Aim for ~1 minute per idea
- First 3 come fast, ideas 4-6 require push, ideas 7-8 are often surprisingly good

### For Sketch Documentation Mode

**Good sketches:**
- Show layout and key elements
- Include labels for clarity
- Use arrows to show interactions
- One clear concept per rectangle

**Common issues:**
- Too much detail (wastes time)
- Too abstract (Claude can't interpret)
- Forgetting to label elements
- Sketching too small

## Common Pitfalls

❌ **Stopping to elaborate during 8 minutes**
✅ **Capture the core idea and keep moving**

❌ **Judging ideas as "too crazy" and censoring them**
✅ **Write everything down - evaluate later**

❌ **Only getting 3-4 ideas and calling it done**
✅ **The magic happens in ideas 6-8 when you're forced to think differently**

❌ **Making all 8 ideas variations of the same concept**
✅ **Use constraints or warm-up questions to push variety**

❌ **Expecting polished, production-ready outputs**
✅ **These are rough explorations to spark discussion**

## What Happens Next

After Crazy 8's, you typically:

1. **Review and discuss** - Look at all 8 ideas without judgment first
2. **Vote or prioritize** - Which 2-3 ideas are most promising? (use `design-critique` skill)
3. **Combine ideas** - Can you merge the best parts of multiple concepts?
4. **Prototype further** - Take top ideas to higher fidelity
5. **User test** - Validate assumptions with actual users

Crazy 8's is for divergence. The next steps are about convergence and validation.

## Tips for Success

**When you're stuck:**
- Use creative constraints to force different thinking
- Do the warm-up questions (even mid-session)
- Think about extreme users (5-year-old vs expert)
- Ask "what would the opposite look like?"

**When all ideas feel the same:**
- You're probably not going fast enough
- Add interaction type constraints
- Try a different metaphor for each idea

**When you're not feeling creative:**
- That's exactly when to use this method
- The timer forces you past the mental block
- Quantity over quality - ideas 7-8 are often best

**For best results:**
- Do this early in the process (before settling on direction)
- Do it alone first, then share with team
- Do multiple rounds if first round felt too similar
- Trust the process - speed is your friend

## Ready to Start?

Say: **"I want to do a Crazy 8's session"**

Claude will guide you through the full process.
