---
name: memory-user-edits
description: Expert guidance for Claude's memory_user_edits tool. Helps users understand how to effectively use memory edits for persistent facts across conversations. Key insight - memory edits work for FACTS, not BEHAVIORS. Triggers on memory-related questions, "remember", "forget", or memory_user_edits tool usage.
---

# Memory User Edits: Expert Guidance

## THE CORE INSIGHT

**Memory edits work for FACTS, not BEHAVIORS.**

| ✅ Works (Facts) | ❌ Doesn't Work (Behaviors) |
|-----------------|---------------------------|
| "Backend stores 7KB per user" | "Always check docs first" |
| "Architecture: two-layer model" | "Prioritize architecture over details" |
| "User prefers TypeScript" | "Never suggest JavaScript" |

---

## THE FOUR COMMANDS

| Command | Purpose | Parameters |
|---------|---------|------------|
| `view` | See current edits | None |
| `add` | Create new edit | `control` (max 200 chars) |
| `remove` | Delete by line number | `line_number` |
| `replace` | Update existing | `line_number`, `replacement` |

**Constraints:**
- Maximum 30 edits total
- 200 characters per edit
- Project-scoped only (not regular chats)
- Plain text only (no markdown/HTML)

---

## WHEN TO USE memory_user_edits

**Use for:**
- User says "remember that...", "don't forget...", "please note..."
- User asks "what do you know about me?"
- User wants to correct a fact Claude keeps getting wrong
- User shares persistent preferences or constraints

**Don't use for:**
- Behavioral instructions (use Project Instructions instead)
- Temporary information
- Complex conditional logic
- Information that changes frequently

---

## BEST PRACTICES

### Writing Good Edits

**✅ Good (atomic, factual):**
```
"Backend: PostgreSQL 15 with Knex.js" (36 chars)
"User timezone: CET (UTC+1)" (26 chars)
"Project deadline: January 2026" (30 chars)
```

**❌ Bad (vague, behavioral):**
```
"Uses good database practices" (vague)
"Always check architecture first" (behavioral)
"Remember to prioritize user needs" (instruction)
```

### Priority Framework

When approaching 30 edits, prioritize:

| Priority | Type | Action |
|----------|------|--------|
| P0 | Facts Claude gets wrong repeatedly | Keep always |
| P1 | Important preferences, key definitions | Keep if space |
| P2 | Nice-to-haves, well-documented info | Remove first |

---

## RESPONSE PROTOCOL

When user asks about memory:

1. **View first:** Always check current edits before adding
2. **Check for duplicates:** Don't add redundant information
3. **Verify facts:** Ensure it's a FACT, not a BEHAVIOR
4. **Confirm action:** Tell user what was added/removed/changed

When user says "remember X":

1. Rewrite X as a concise fact (under 200 chars)
2. Check for conflicts with existing edits
3. Add the edit
4. Confirm: "Added memory #N: [content]"

---

## TROUBLESHOOTING

**"Claude ignores my memory edits"**
- Verify you're in a Claude Project (not regular chat)
- Check if edit is a FACT (works) vs BEHAVIOR (doesn't work)
- Ensure query is relevant to the stored fact

**"Memory edits work inconsistently"**
- Edit may be too vague → make more specific
- Documentation may contradict → align them
- Edit may be behavioral → rewrite as fact

**"Hit 30-edit limit"**
- View all edits
- Remove P2 (nice-to-haves) first
- Consolidate related edits

---

## QUICK REFERENCE

**Add a fact:**
```
add control="[concise fact under 200 chars]"
```

**View all edits:**
```
view
```

**Remove an edit:**
```
remove line_number=[N]
```

**Update an edit:**
```
replace line_number=[N] replacement="[new text]"
```

---

## THE FOUR-LAYER SYSTEM

Memory edits work best as part of a complete system:

| Layer | Purpose |
|-------|---------|
| **Project Instructions** | HOW Claude should work (behaviors) |
| **Documentation** | Detailed project knowledge |
| **Memory Edits** | Critical facts always in focus |
| **Active Steering** | Real-time corrections |

**Key:** Memory edits amplify Project Instructions—they don't replace them.

---

*Memory User Edits Guide by Francesco Marinoni Moretto — CC BY 4.0*
