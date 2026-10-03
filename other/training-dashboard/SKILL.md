---
name: training-dashboard
description: Generate a comprehensive HTML training dashboard showing progress toward half marathon training goals. Outputs a single self-contained HTML file with retro styling, ASCII charts, weekly mileage tracking, session completion rates, pace adherence, phase progress, and coaching commentary. Use when the athlete wants to see their training progress, check if they're on track, view their training statistics, or get an overview of their plan progress. Trigger phrases include "show my dashboard", "training progress", "how am I doing", "show my stats", or any request for a training overview.
---

# Training Dashboard

Generate an HTML dashboard with retro styling showing comprehensive training progress toward the half marathon goal. Outputs a single HTML file saved to `dashboard.html` that can be opened in any browser.

## Dashboard Configuration

When generating the dashboard, you will prompt the user for their preferences. If the user has previously provided preferences in the conversation, use those. Otherwise, ask for the following:

### Configuration Prompts

**1. Layout Style**

Ask: "What level of detail would you like?"
- `detailed` (default): Full metrics, large charts, extensive commentary
- `compact`: Key metrics, medium charts, brief commentary
- `ultra-compact`: Essential metrics only, small charts, minimal commentary

**2. Retro Style Theme**

Ask: "Which retro theme would you like?"
- `terminal-green` (default): Classic green phosphor CRT terminal (green on black)
- `amber-monitor`: Vintage amber monochrome display (amber on dark brown)
- `ibm-blue`: IBM mainframe blue screen (cyan on blue)
- `paper-print`: Dot matrix printer style (black on cream)

**3. Commentary Style**

Ask: "What style of coaching commentary?"
- `conversational` (default): Chatty, casual coaching style with personality
- `analytical`: Data-focused with objective observations
- `motivational`: Encouraging and uplifting focus
- `minimal`: Brief, to-the-point feedback

**4. Optional Customization**

Only ask if the user seems interested in customization:
- Chart styles (weekly mileage: `bar` | `sparkline` | `progress-bar`)
- Which sections to show/hide

### Default Configuration

If the user wants to skip configuration or says "just use defaults", use:
- Layout: `detailed`
- Theme: `terminal-green`
- Commentary: `conversational`
- Chart styles: `bar` for mileage, `timeline` for phase, `grid` for sessions
- All sections enabled

---

## Dashboard Generation Workflow

### 1. Prompt for Configuration

Before generating the dashboard, ask the user for their preferences (unless they've already specified them in the conversation):

1. Ask about layout style, theme, and commentary style (see Configuration Prompts above)
2. If the user says "default" or "just show me", use the default configuration
3. Store these preferences for the current dashboard generation
4. Present a brief summary: "Generating [detailed/compact/ultra-compact] dashboard with [theme] theme and [style] commentary..."

### 2. Load Training Data

Read these files:
- `training-plan.md` - Full 12-week plan structure, goals, paces
- `training-log/week-*.md` - All completed training logs
- Check which weeks have logs vs which are planned

Extract from training-plan.md:
- Goal: Target time, pace, distance
- Total plan duration (12 weeks)
- Phase structure (Foundation, Build, Specific, Taper)
- Weekly planned mileage and sessions
- Prescribed paces (Easy, Steady, Threshold, Interval, HM)

Extract from training logs:
- Completed weeks
- Actual mileage per week
- Actual sessions completed
- Actual paces achieved
- Activity types (Run, Ride, Walk, Workout)

### 3. Calculate Metrics

Calculate these key metrics:

**Plan Progress:**
- Current week number / Total weeks
- Current phase
- Weeks completed / Weeks remaining
- Time to race (if race date known)

**Mileage Tracking:**
- Total miles run vs total planned (for completed weeks)
- Average weekly mileage (actual)
- Highest mileage week
- Weekly comparison (actual vs planned for each week)

**Session Completion:**
- Total sessions completed vs planned
- Completion rate percentage
- Which session types were completed (threshold, intervals, long runs, easy runs)
- Missed sessions

**Pace Adherence:**
- For each pace type (Easy, Threshold, Interval, HM):
  - How many sessions at this pace
  - Average actual pace vs prescribed range
  - Adherence score (within range, too fast, too slow)
- Most common issue (e.g., "easy runs too fast")

**On Track Status:**
Determine overall status based on:
- Completion rate (>85% = good, 70-85% = okay, <70% = behind)
- Mileage adherence (within 10% = good, 10-20% = okay, >20% = adjust)
- Pace adherence (Easy runs especially - are they truly easy?)
- Progressive overload (volume building appropriately?)

Status: `On Track` | `Slightly Behind` | `Needs Adjustment` | `Ahead of Schedule`

### 4. Generate HTML Dashboard

Create a single self-contained HTML file with:
- Tailwind CSS loaded from CDN (https://cdn.tailwindcss.com)
- Retro styling based on configured theme
- ASCII charts displayed in monospace `<pre>` tags
- Responsive layout using Tailwind utilities
- No JavaScript required

**HTML Structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Half Marathon Training Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Retro theme styles - see Theme Styles section below */
    </style>
</head>
<body class="[theme-classes]">
    <!-- Dashboard sections -->
</body>
</html>
```

**Theme Styles:**

**Terminal Green (terminal-green):**
```css
body {
    background: #0a0a0a;
    color: #33ff33;
    font-family: 'Courier New', monospace;
}
.card {
    background: #0f0f0f;
    border: 2px solid #33ff33;
    box-shadow: 0 0 10px rgba(51, 255, 51, 0.3);
}
.accent { color: #66ff66; }
.warning { color: #ffff33; }
.success { color: #33ff33; }
.muted { color: #5aaa5a; }
```

**Amber Monitor (amber-monitor):**
```css
body {
    background: #2b1810;
    color: #ffb000;
    font-family: 'Courier New', monospace;
}
.card {
    background: #1a0f08;
    border: 2px solid #ffb000;
    box-shadow: 0 0 10px rgba(255, 176, 0, 0.3);
}
.accent { color: #ffc840; }
.warning { color: #ff8800; }
.success { color: #ffb000; }
.muted { color: #7a5830; }
```

**IBM Blue (ibm-blue):**
```css
body {
    background: #00007f;
    color: #aaffff;
    font-family: 'Courier New', monospace;
}
.card {
    background: #000066;
    border: 2px solid #aaffff;
    box-shadow: 0 0 10px rgba(170, 255, 255, 0.3);
}
.accent { color: #ccffff; }
.warning { color: #ffff00; }
.success { color: #aaffff; }
.muted { color: #5588aa; }
```

**Paper Print (paper-print):**
```css
body {
    background: #f5f5dc;
    color: #1a1a1a;
    font-family: 'Courier New', monospace;
}
.card {
    background: #fafae6;
    border: 2px solid #1a1a1a;
    box-shadow: 3px 3px 0px rgba(0, 0, 0, 0.2);
}
.accent { color: #000000; font-weight: bold; }
.warning { color: #8b0000; }
.success { color: #006400; }
.muted { color: #666666; }
```

### 4. Generate ASCII Visualizations

ASCII charts are embedded within `<pre>` tags in the HTML for retro appearance:

Based on chart styles from user configuration in step 1, generate visualizations:

#### Bar Chart (for weekly mileage)
```
Week 1  [████████████████░░░░] 24.5 / 28 mi  (88%)
Week 2  [█████████████░░░░░░░] 22.3 / 28 mi  (80%)
Week 3  [████████████████████] 30.1 / 30 mi (100%)
```

#### Sparkline (compact weekly mileage)
```
Weeks 1-12: ▂▃▅▇█▆▄▃▅▆▂░
            Completed─┘ └─Planned
```

#### Progress Bar (for phase progress)
```
Phase 2: Build ████████████████░░░░░░░░ 67% (Week 6 of 9)
```

#### Phase Progress (compact style)
```
Phase: Foundation ✓✓✓ | Build ✓○○○ | Specific ○○○○ | Taper ○
```

#### Grid (for session completion)
```
Week 1: [✓] Threshold  [✓] Easy  [✓] Long
Week 2: [✓] Intervals  [✓] Easy  [○] Long
Week 3: [✓] Threshold  [✓] Easy  [✓] Long
```

#### Checklist (for session completion)
```
✓ 3x1 mile @ Threshold (Week 1)
✓ 8 miles Easy (Week 1)
✓ 10 miles Long (Week 1)
✓ 6x1k @ Interval (Week 2)
○ 9 miles Easy (Week 2) - MISSED
```

#### Percentage Display (compact)
```
Sessions: 15/18 completed (83%)
Mileage:  48.2/56 miles (86%)
```

### 6. Generate Coaching Commentary

Based on the commentary style selected by the user in step 1, provide feedback:

**Conversational Style:**
"Alright, let's see how you're doing! You're in Week 2 of the Build phase, and honestly? Looking solid. You've knocked out 83% of your sessions, which is right where we want to be. The mileage is slightly behind (86%), but that's not a red flag at all - life happens, and you're still getting the quality work done.

One thing I'm noticing though - those easy runs are still a bit spicy. You're averaging 7:20/mile when we want 7:35-8:13. I know, I know, I sound like a broken record, but trust me on this one. Slow down those easy days and you'll actually feel better on the hard days. Deal?"

**Analytical Style:**
"Current Status: Week 2, Build Phase (Week 6 of 12)
- Completion Rate: 83% (15/18 sessions)
- Mileage: 48.2/56 miles (86% of planned)
- Primary Issue: Easy pace 15 sec/mile too fast
- Recommendation: Reduce easy run pace by 20 seconds/mile
- Overall Assessment: On track with minor pace adjustment needed"

**Motivational Style:**
"You're crushing it! 🎉 Week 2 of Build phase and you're showing up consistently. 83% completion rate shows serious commitment. Sure, the mileage is a touch behind, but you know what? Quality > quantity, and you're nailing those key workouts. Keep bringing this energy and that half marathon time is yours for the taking!"

**Minimal Style:**
"Week 2/12. On track. 83% sessions complete. Easy runs too fast - slow down. Otherwise solid."

### 7. Assemble HTML Dashboard

Combine all sections based on user configuration from step 1 using Tailwind classes:

**HTML Layout Structure:**
```html
<body class="p-8 min-h-screen">
    <div class="max-w-6xl mx-auto">
        <!-- Header -->
        <header class="card p-6 rounded-lg mb-6">
            <h1 class="text-4xl font-bold mb-2">HALF MARATHON TRAINING DASHBOARD</h1>
            <p class="text-xl">Target: 1:23:00 (6:19/mile)</p>
        </header>

        <!-- Sections in cards -->
        <div class="space-y-6">
            <!-- Each enabled section -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b pb-2">SECTION TITLE</h2>
                <pre class="text-sm overflow-x-auto">ASCII content here</pre>
            </div>
        </div>

        <!-- Footer -->
        <footer class="mt-8 text-center muted text-sm">
            Generated: [timestamp]
        </footer>
    </div>
</body>
```

**Section Order** (include if enabled):
1. **Plan Overview**: Goal details, timeline
2. **Phase Progress**: Visual of phase progression
3. **On Track Status**: Overall status indicator
4. **Weekly Mileage**: Weekly mileage chart
5. **Session Completion**: Session tracking visual
6. **Pace Adherence**: Pace analysis by type
7. **Coaching Commentary**: Coach's feedback in a more prominent card
8. **Next Week Preview**: What's coming up

### 8. Save HTML File

Write the complete HTML to `dashboard.html` in the project root directory. After saving, inform the user:
- File location
- How to open it (double-click or open in browser)
- Remind them they can refresh the page after updating training logs

### 9. Example Dashboard Outputs

#### HTML Dashboard Example (Terminal Green Theme)

The generated `dashboard.html` file will be a complete, self-contained HTML file that looks like this:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Half Marathon Training Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background: #0a0a0a;
            color: #33ff33;
            font-family: 'Courier New', monospace;
        }
        .card {
            background: #0f0f0f;
            border: 2px solid #33ff33;
            box-shadow: 0 0 10px rgba(51, 255, 51, 0.3);
        }
        .accent { color: #66ff66; }
        .warning { color: #ffff33; }
        .success { color: #33ff33; }
        .muted { color: #1a7a1a; }
        pre { font-family: 'Courier New', monospace; }
    </style>
</head>
<body class="p-8 min-h-screen">
    <div class="max-w-6xl mx-auto">
        <header class="card p-6 rounded-lg mb-6">
            <h1 class="text-4xl font-bold mb-2">HALF MARATHON TRAINING DASHBOARD</h1>
            <p class="text-xl mt-4 accent">Target: 1:23:00 (6:19/mile)</p>
            <p class="text-lg muted" style="text-shadow: none;">Week 2 of 12 • Foundation Phase</p>
        </header>

        <div class="space-y-6">
            <!-- Plan Overview -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">PLAN OVERVIEW</h2>
                <div class="grid grid-cols-2 gap-4 text-lg">
                    <div><span class="muted">Goal Distance:</span> <span class="accent">13.1 miles</span></div>
                    <div><span class="muted">Target Time:</span> <span class="accent">1:23:00</span></div>
                    <div><span class="muted">Target Pace:</span> <span class="accent">6:19/mile</span></div>
                    <div><span class="muted">Weeks Remaining:</span> <span class="accent">10</span></div>
                </div>
            </div>

            <!-- Phase Progress -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">PHASE PROGRESS</h2>
                <p class="text-lg mb-2">Phase: Foundation ✓○○ | Build ○○○○ | Specific ○○○○ | Taper ○</p>
                <p class="mt-4"><span class="muted">Current:</span> <span class="accent">Foundation Phase (Week 1 of 3)</span></p>
                <p class="muted text-sm">Focus: Build volume foundation while introducing quality work</p>
            </div>

            <!-- On Track Status -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">STATUS: <span class="success">→ ON TRACK ✓</span></h2>
                <div class="space-y-3">
                    <div>
                        <div class="flex justify-between mb-1">
                            <span>Overall Progress</span>
                            <span class="accent">82%</span>
                        </div>
                        <pre class="text-sm">[████████████████░░░░] 82%</pre>
                    </div>
                    <div class="grid grid-cols-2 gap-4 text-lg mt-4">
                        <div><span class="muted">Running Miles:</span> <span class="accent">22.4 / 24.5</span></div>
                        <div><span class="muted">Sessions:</span> <span class="accent">2.5 / 3</span></div>
                    </div>
                </div>
            </div>

            <!-- Weekly Mileage -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">WEEKLY MILEAGE</h2>
                <pre class="text-sm">
Week 1  [██████████████████░░] 22.4 / 24.5 mi  (91%) <span class="success">✓</span>
Week 2  [░░░░░░░░░░░░░░░░░░░░]  0.0 / 28.0 mi   (0%) <span class="accent">→</span>
Week 3  [░░░░░░░░░░░░░░░░░░░░]  0.0 / 30.0 mi   (0%)
Week 4  [░░░░░░░░░░░░░░░░░░░░]  0.0 / 24.0 mi   (0%)
                </pre>
                <div class="grid grid-cols-2 gap-4 text-lg mt-4">
                    <div><span class="muted">Total:</span> <span class="accent">22.4 miles</span></div>
                    <div><span class="muted">Weekly Avg:</span> <span class="accent">22.4 mi/wk</span></div>
                </div>
            </div>

            <!-- Pace Adherence -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">PACE ADHERENCE</h2>
                <div class="space-y-2 text-lg">
                    <div><span class="muted">Easy (7:35-8:13):</span> <span class="warning">7:22 ⚠ TOO FAST</span></div>
                    <div><span class="muted">Threshold (6:04-6:19):</span> <span class="success">6:12 ✓ GOOD</span></div>
                    <div><span class="muted">Interval (5:41-5:55):</span> <span class="success">5:56 ✓ GOOD</span></div>
                    <div><span class="muted">HM Pace (6:19):</span> <span class="muted">No data yet</span></div>
                </div>
                <p class="mt-4 warning text-sm">⚠ Primary Issue: Easy runs consistently too fast</p>
            </div>

            <!-- Coach's Commentary -->
            <div class="card p-6 rounded-lg border-4">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">💬 COACH'S COMMENTARY</h2>
                <div class="space-y-4 text-base leading-relaxed">
                    <p>Hey! Week 1 in the books - nice way to kick things off! 💪</p>

                    <p><span class="accent font-bold">The Good Stuff:</span><br>
                    That threshold workout? *Chef's kiss* You're executing quality sessions well and showing up consistently.</p>

                    <p><span class="warning font-bold">We Need to Talk:</span><br>
                    Those easy runs at 7:48 when we want 7:35-8:13... I know it feels wrong to slow down, but this is where the magic happens. Easy miles build your aerobic base without fatiguing you for the hard days.</p>

                    <p><span class="success font-bold">Bottom Line:</span><br>
                    You're on track! Just need ONE thing: when it says "easy", run ACTUALLY easy. Aim for 8:00 pace. Your future self will thank you!</p>
                </div>
            </div>

            <!-- Next Week Preview -->
            <div class="card p-6 rounded-lg">
                <h2 class="text-2xl font-bold mb-4 border-b border-current pb-2">NEXT WEEK PREVIEW (Week 2)</h2>
                <p class="text-lg mb-4"><span class="muted">Target Volume:</span> <span class="accent">28.0 miles</span></p>
                <div class="space-y-2">
                    <p class="accent font-bold">Key Sessions:</p>
                    <ul class="list-disc list-inside muted space-y-1 ml-4">
                        <li>Intervals: 6 x 1km @ 5:41-5:55/mi</li>
                        <li>Easy: 9 miles @ 7:35-8:13/mi</li>
                        <li>Long Run: 11.5 miles easy</li>
                    </ul>
                </div>
            </div>
        </div>

        <footer class="mt-8 text-center muted text-sm py-4">
            <p>Generated: 2026-01-27 • dashboard.html</p>
        </footer>
    </div>
</body>
</html>
```

#### Compact Layout Example

```
═══════════════════════════════════════════════════
  HALF MARATHON TRAINING DASHBOARD
  Target: 1:23:00 (6:19/mile) | Week 2/12
═══════════════════════════════════════════════════

STATUS: → ON TRACK ✓

Phase: Foundation ✓✓✓ | Build ✓○○○ | Specific ○○○○ | Taper ○

Sessions: 15/18 (83%) ░░░░░░░░░░░░░░░░░░░░
Mileage:  48.2/56 mi (86%)

Week 1: ████████████████░░░░ 24.5/28 mi ✓
Week 2: █████████████░░░░░░░ 23.7/28 mi ✓

Pace Check:
  Easy: 7:22 (target 7:35-8:13) ⚠ TOO FAST
  Threshold: 6:12 ✓
  Interval: 5:56 ✓

Coach Says: Solid work! Hitting your quality sessions well.
Just need to slow those easy runs down - aim for 7:45ish.
Week 3 is a big one (30 mi), but you're ready for it!

Next: 4x1mi @ Threshold, 10mi Easy, 12.5mi Long
═══════════════════════════════════════════════════
```

#### Ultra-Compact Layout Example

```
HM Training: Week 2/12 | Target 1:23:00 | ON TRACK ✓
Phase: Foundation ✓✓✓ | Build ✓○○○ | Specific ○○○○ | Taper ○
Sessions: 15/18 (83%) | Miles: 48.2/56 (86%)
Wk1: ████░ 24.5mi | Wk2: ███░░ 23.7mi
Easy pace: ⚠ TOO FAST | Threshold/Interval: ✓ GOOD
Coach: Slow easy runs to 7:45. Otherwise solid!
```

## Tips for Customization

**To use different dashboard settings:**
1. When asked to generate a dashboard, specify your preferences ("use compact layout with amber theme")
2. Or say "use defaults" to quickly generate with standard settings
3. You can change settings between dashboard generations

**Common preference patterns:**
- "Show me a quick overview" → Use ultra-compact layout
- "I want all the details" → Use detailed layout with conversational commentary
- "Make it look retro" → Suggest terminal-green or amber-monitor theme
- "Just the facts" → Use analytical or minimal commentary style

**Regenerating with different settings:**
Just ask! "Can you regenerate with a different theme?" or "Show me the compact version instead."

## Notes

- The dashboard reads data from `training-plan.md` and `training-log/week-*.md` files
- All calculations are done fresh each time the dashboard is generated
- The HTML file is self-contained (no external dependencies except Tailwind CDN)
- ASCII charts are displayed in `<pre>` tags for monospace rendering
- The dashboard is responsive and works on mobile devices
- No JavaScript required - pure HTML and CSS
- "On Track" status is subjective and based on completion rate, mileage, and pace adherence
- Coaching commentary references actual data and provides actionable feedback
- Save location: `dashboard.html` in project root
- To view: Double-click the file or open in any web browser
- Refresh the browser after regenerating to see updates
