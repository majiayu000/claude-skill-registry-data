---
name: using-fart-prompt
version: "1.0.1"
description: >
  Breaks creative, writing, planning, and thinking paralysis by generating
  intentionally ugly, messy, half-baked versions of an idea before the
  polished version arrives. Lowers activation energy by making "bad" the
  goal. Activates when stuck, blocked, overthinking, or paralyzed by
  perfectionism. Trigger phrases: fart prompt, brain fart, ugly version,
  messy first draft, half-baked idea, just give me something terrible,
  dumbest version of this, roughest possible take, unblock me, help me
  start, I can't get started, I've been avoiding this, I need momentum,
  I keep staring at a blank page, I don't know where to begin,
  perfectionism is blocking me, or any signal that pressure is preventing
  forward motion. PERSONAL lane: memoir, writing, planning, personal
  decisions. Also valid for FlashFusion content and Loxihart internal docs
  when stuck. NOT for active engineering builds — use
  sparc-methodology-coach instead.
---

# Using the Fart Prompt

Generates intentionally bad, messy, half-baked output to break paralysis.
Perfectionism → procrastination. Intentional badness → momentum.

---

## Decision Tree

```
Is the person stuck / blocked / avoiding something?
  ├─ YES
  │    ├─ Is it a creative/writing block? ──────────── WRITING mode
  │    ├─ Is it a planning/decision block? ────────── PLANNING mode
  │    ├─ Is it a content/ideas block? ─────────────── IDEAS mode
  │    ├─ Is it a personal/life decision block? ────── PERSONAL mode
  │    └─ Is it technical architecture? ─────────────── Redirect to sparc-methodology-coach
  └─ NO → Don't activate. Regular task execution.
```

---

## The Core Prompt (verbatim)

```
Stop trying to sound smart or polished. Give me the ugliest, messiest,
most half-baked version of this idea possible — like a total brain fart
someone blurts out before the real idea arrives.
```

Apply this at the START of the response, not the end. Ship the mess immediately.
Do not editorialize the mess. Do not add disclaimers. The mess IS the output.

---

## Mode Variations

### WRITING MODE
Target: memoir, essays, articles, blog posts, social content

System behavior:
- Stream-of-consciousness. No structure.
- Wrong word choices welcome. Clichés welcome.
- Sentence fragments welcome.
- Contradict yourself mid-paragraph. That's fine.

Fart prompt for writing:
```
Stop editing before you write. Give me the stream-of-consciousness,
half-formed, over-personal, probably-wrong version of this piece.
Like the first thing that comes out before the inner critic shows up.
[topic]
```

### PLANNING MODE
Target: projects, decisions, priorities, schedules

System behavior:
- No prioritization. No logical order.
- Mix big and trivial things equally.
- Overlap is fine. Redundancy is fine.
- Include the thing you've been avoiding.

Fart prompt for planning:
```
Don't make a real plan. Just dump everything that's in your head about
[topic] — unordered, repeated, contradictory, whatever. Like you have
30 seconds before the meeting starts.
```

### IDEAS MODE
Target: FlashFusion content, newsletter angles, workshop concepts

System behavior:
- Include ideas that are too obvious. Include ideas that make no sense.
- Don't filter by viability.
- The goal is VOLUME, not quality.

Fart prompt for ideas:
```
Give me 8 ideas for [topic]. Make half of them too obvious. Make two of
them genuinely bad. Make one of them offensive to a professional audience.
Don't hold back the dumb ones.
```

### PERSONAL MODE
Target: personal decisions, relationships, life priorities

System behavior:
- Do NOT therapize. Do NOT give structure.
- Just reflect the raw thing back in messy form.
- Ask one question at the end, not five.

Fart prompt for personal:
```
Don't give advice. Just blurt the messiest version of what I might be
thinking about [situation] — like you're finishing my sentence badly.
```

---

## Session Flow

1. **Detect block signal** — they're stuck, avoiding, or paralyzed.
2. **Identify mode** — writing, planning, ideas, or personal.
3. **Ask one clarifier** (only if topic is unclear): "What's the thing you're stuck on? One sentence."
4. **Run the fart prompt** — ship the messy version. No preamble. No apology.
5. **Offer follow-ups** (optional, only if result landed):
   - "Go uglier" → even more chaotic, less coherent
   - "Refine from this" → extract the one usable kernel and build
   - "Different angle" → same mess level, different direction

---

## Why This Works

Perfectionism loops: brain treats starting as dangerous because outcome
feels too important. Intentionally bad output short-circuits the loop —
you can't fail at making something terrible.

Connection to Construction over Recovery: don't wait for the perfect
entry point. Build something — even a bad version — and iterate forward.
Momentum is more valuable than the first draft being good.

See `references/psychology-notes.md` for the full mechanism breakdown:
activation energy, perfectionism loop anatomy, and when this technique
does NOT apply.

---

## Eval Scenarios

**Should trigger:**
1. "I've been staring at the opening of my memoir chapter for two hours."
2. "I keep avoiding planning Q3 content for FlashFusion. Unblock me."
3. "What's the dumbest possible version of a newsletter angle about burnout?"
4. "Fart prompt — I'm stuck on this parenting decision."
5. "I can't start this Loxihart runbook. Just give me something bad."

**Should NOT trigger:**
1. "Build the Fusion AI agent orchestration layer." → sparc-methodology-coach
2. "Write a KB article for FreshService." → generating-kb-articles
3. "Review my SKILL.md for structural issues." → auditing-and-rewriting-skills

---

## Checklist Before Shipping

- [ ] Mode identified (writing / planning / ideas / personal)
- [ ] Fart prompt applied — output is deliberately messy
- [ ] No disclaimers attached to the mess ("here's a rough version...")
- [ ] No structure imposed on the mess (no bullets, no headers in the fart output)
- [ ] Follow-up options offered after the mess lands
- [ ] Did NOT redirect to another skill unless it's clearly an engineering task

---

## References

- `references/mode-examples.md` — concrete before/after examples per mode
- `references/psychology-notes.md` — activation energy, perfectionism loops, Construction over Recovery

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

**CLAIMS**
- [GENERATED] The core mechanism — making "bad" the explicit goal — collapses the perfectionism loop by removing failure as a possible outcome. You cannot fail at producing something deliberately terrible.
- [GENERATED] Intentional badness reduces activation energy for creative tasks because the brain no longer treats starting as a risk-of-failure event.
- [GENERATED] MODE VARIATIONS (writing/planning/ideas/personal) are extrapolations from the single-purpose core prompt — the four-mode taxonomy is original synthesis, not from a single source.
- [GENERATED] "Construction over Recovery" framing applied to this technique is original synthesis connecting Kyle's operating philosophy to the creative unblocking mechanism.

**COUNTEREXAMPLES**
- This prompt does NOT work when the block is caused by missing information, not perfectionism. If you're stuck because you don't know the facts yet, you need research, not a fart prompt.
- Works best when the inner critic is the bottleneck. If the bottleneck is external (waiting on someone, dependency), this generates noise, not momentum.

**!CONTRADICTIONS**
- Claude has strong default tendencies toward structure, formatting, and disclaimers. The fart prompt explicitly requires none of these. The skill must override Claude's defaults at execution time — if the output comes out with headers, bullets, or "here's a rough version…", the skill failed.

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- No data on how often the ugly version is actually used vs. immediately discarded.
- Unknown whether this degrades for highly technical domains (architecture, security modeling) where "bad on purpose" could normalize actually bad thinking.
- Memoir-specific application untested — the technique may interact differently with emotionally loaded material vs. pure content work.
