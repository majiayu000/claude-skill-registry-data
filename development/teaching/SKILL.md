---
name: teaching
description: Turns any technical output (creation, structure, architectural decision) into a learning opportunity - a tree of where the element lives, an x-ray of what-it-is/where-it-sits/what-it-is-for, a connection map, a business analogy, and explained decisions. Always use in technical output for a non-programmer reader.
---

> **Auto-Trigger:** Always active in every technical output that involves creation, structure, or architectural decisions.
> **Keywords:** "teach", "explain", "how does it work", "where does it live", "architecture", "teaching", "why"
> **Priority:** MEDIUM
> **Tools:** Read, Write, Bash

## When to activate
ALWAYS. In every output that involves:
- File creation
- A proposed structure
- Execution plans
- Technical decisions
- Mention of paths, folders, formats, connections

## When NOT to Activate

Even though it is "ALWAYS active" for technical output, do NOT apply the 5 teaching blocks when:

- **Conversational/non-technical reply** (status, "where did we stop?", simple confirmation, business question with no technical element) - there is no file/structure/connection to teach.
- **Purely factual output of live data** (metrics, health score, counts) - the focus is the verified data, not the architecture.
- **Trivial edits** (typo, comma, 1-line tweak with no structural impact) - the teaching overhead becomes noise.
- **Internal batch execution by a subagent** where the output goes to another agent/orchestrator, not to a human learner.
- **When the user explicitly asks for brevity** ("just do it", "no explanation", "short answer") - respect the direct instruction.

## Contract

**INPUT:** any technical output (text) the model is about to deliver, covering creation/structure/architectural decision.

**OUTPUT:** the same output, with the 5 teaching blocks attached (tree, x-ray, connections, analogy, decisions).

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | always - this is a FORMATTING/BEHAVIOR skill, there is no possible execution failure; the "contract" is about output completeness, verifiable via the validator in the Proof section |

**STATE IT TOUCHES:**

| Resource | Reads/Writes | Purpose |
|---|---|---|
| (no file) | - | this skill reads/writes no state - it shapes the FORM of the model's reply |

## Mandatory format of every technical output

### BLOCK 1: 🗺️ WHERE WE ARE (Architectural Tree)

Draw the project's COMPLETE tree showing WHERE the current element lives.
Mark the file or folder in question with ➡️.
Use clear visual language.

```
projeto-raiz/
├── CLAUDE.md              ← General rules (the "company handbook")
├── agents/                ← All agents live here
│   ├── vendedor.md
│   └── analista.md
├── skills/                ← All reusable competencies
│   ├── teaching/
│   │   └── SKILL.md
│   └── copywriting/
│       └── SKILL.md
├── workflows/             ← All orchestrated processes
│   ├── qualificar-lead.yml    ➡️ WE ARE HERE
│   └── onboarding-cliente.yml
├── hooks/                 ← All automatic triggers
│   └── on-lead-entry.yml
└── tasks/                 ← Unit tasks (optional; they can live inside the workflows)
```

TREE RULES:
- Always show the tree FROM THE ROOT of the project
- Never show only the partial path - always the full context
- Mark with ➡️ the element being created/modified/explained
- If the project is very large, show the 2 most relevant levels + the full path down to the element

---

### BLOCK 2: 🔍 X-RAY OF THE ELEMENT

For EACH file or folder mentioned, you MUST answer:

| Question | Answer |
|----------|----------|
| **What is this?** | A 1-sentence explanation, no jargon. Use a business-world analogy. |
| **Where does it live?** | Full path from the root. E.g. `/projeto/workflows/qualificar-lead.yml` |
| **Inside what?** | Which folder contains this file and why that folder exists. |
| **How many of this kind exist?** | 1 per process? 1 per agent? No limit? Explain the rule. |
| **What is it connected to?** | List ALL the other files that connect to this one. Show the direction: who calls whom. |
| **Who triggers it?** | What makes this file run? A command? A hook? Another workflow? |
| **What is inside?** | Summarized internal structure. Which sections, fields or blocks exist inside this file. |
| **Why this format?** | `.yml`, `.md`, `.json` - why this one and not another? What is the practical advantage? |
| **What happens if I delete it?** | Real consequence. What breaks, what stops working. |
| **Possible alternative?** | Was there another way to do this? If so, why did we choose this one? |

---

### BLOCK 3: 🔗 CONNECTION MAP

Draw how this element connects to the others using simple arrows:

```
[CLAUDE.md] ──defines rules for──▶ [agents/vendedor.md]
                                          │
                                    uses the skill
                                          │
                                          ▼
                                   [skills/copywriting/SKILL.md]
                                          │
                                  is called by the workflow
                                          │
                                          ▼
                              [workflows/qualificar-lead.yml]  ➡️ THIS ONE
                                          │
                                   triggered by
                                          │
                                          ▼
                                [hooks/on-lead-entry.yml]
```

RULES:
- Always show at least 1 level above and 1 level below the current element
- Use clear verbs on the arrows: "calls", "defines", "triggers", "uses", "reads", "writes"
- If there is more than one path, show them all

---

### BLOCK 4: 💡 TRANSLATION TO THE REAL WORLD

Make a direct analogy with company operations:

> **In your company:** This workflow is like the process your sales team follows
> when a new lead comes in. The `.yml` file is the written checklist any new
> salesperson would receive on day one. The hook that triggers it is like the
> automatic alert the CRM sends when a form is filled in. The skill it uses is
> like the qualification script the salesperson follows on the call.

RULES:
- Always use an analogy with company operations, sales, marketing or management
- Never use technical jargon without an immediate translation
- If the concept has no obvious analogy, create one and be explicit: "There is no perfect analogy, but think of it like this..."

---

### BLOCK 5: ⚠️ DECISIONS I MADE AND WHY

Whenever the agent makes any technical decision, it MUST explain:

```
DECISION: I created the workflow as .yml, not .md
WHY: Because .yml lets the system read and interpret the structure
     automatically (parsing). A .md file is just human-readable text -
     the system cannot extract steps from it without interpretation.
ALTERNATIVE: It could be .json, but .json is harder to read and edit
             by hand. .yml is the middle ground: readable by humans AND by machines.
CONSEQUENCE: If in the future you want the system to run workflows automatically,
             .yml is already ready. Had I used .md, it would need a rewrite.
```

---

## Language rules

1. **Never shorten paths without context.**
   - ❌ "It lives in `/workflows/`"
   - ✅ "It lives in `/projeto-raiz/workflows/qualificar-lead.yml` - the `workflows` folder is where ALL the project's orchestrated processes live, and it sits directly at the root."

2. **Never use a technical term without an immediate translation.**
   - ❌ "This is a YAML parser"
   - ✅ "This is an automatic reader of .yml files (YAML is just the file format - think of it as a simplified spreadsheet where each line has a key and a value)"

3. **Never assume the reader knows what is inside a folder.**
   - Always list the contents, even if it is "empty for now, but it will contain X"

4. **Always answer the question before it is asked.**
   - If you mentioned a format, explain the format
   - If you mentioned a connection, show the connection visually
   - If you mentioned a folder, show what is inside

5. **Controlled depth.**
   - Go up to 2 levels of "why".
   - If the explanation pulls in a third level, stop and say: "This opens another topic (X). Do you want me to go deeper?"

## Complete example of output with Teaching Mode active

**Scenario:** The agent needs to create a lead-qualification workflow.

---

**Agent output:**

I will create the lead-qualification workflow.

🗺️ **WHERE WE ARE:**
```
meu-projeto/
├── CLAUDE.md
├── agents/
│   └── qualificador.md
├── skills/
│   └── perguntas-spin/
│       └── SKILL.md
├── workflows/
│   └── qualificar-lead.yml    ➡️ CREATING THIS NOW
└── hooks/
    └── novo-lead.yml
```

🔍 **X-RAY:**

| Question | Answer |
|----------|----------|
| **What is it?** | A written process that defines step by step how to qualify a lead. It is the "salesperson's checklist". |
| **Where does it live?** | `/meu-projeto/workflows/qualificar-lead.yml` |
| **Inside what?** | The `workflows/` folder, which sits at the project root. That folder exists to hold ALL the project's processes. Each process is a separate file. |
| **How many of this kind?** | 1 file per process. If you have 5 different processes, you will have 5 `.yml` files inside `workflows/`. No limit. |
| **What is it connected to?** | It calls the agent `agents/qualificador.md` to execute. The agent uses the skill `skills/perguntas-spin/SKILL.md`. |
| **Who triggers it?** | The hook `hooks/novo-lead.yml` fires when a new lead comes in. Or it can be called manually by command. |
| **What is inside?** | Workflow name, description, list of steps, and for each step: which agent executes it, which skill it uses, what the expected output is. |
| **Why .yml?** | Because both machine and human can read it. Unlike .md (only humans read it well) and .json (only machines read it well). |
| **If deleted?** | The hook will try to call this workflow and will error. The agent still exists but nobody will trigger it automatically. |
| **Alternative?** | It could be .md if it were only documentation. But since we want the system to execute the steps, it needs a structured format. |

🔗 **CONNECTIONS:**
```
[hooks/novo-lead.yml] ──fires──▶ [workflows/qualificar-lead.yml] ➡️
                                           │
                                     calls agent
                                           ▼
                                   [agents/qualificador.md]
                                           │
                                      uses skill
                                           ▼
                                [skills/perguntas-spin/SKILL.md]
```

💡 **IN YOUR WORLD:**
It is like when your company's CRM detects a new sign-up (hook),
automatically opens the qualification process (workflow),
which escalates to the responsible SDR (agent),
who follows the SPIN selling script (skill).

⚠️ **DECISIONS:**
```
DECISION: I separated the workflow from the agent into different files
WHY: The same agent can be used in several different workflows.
     Merging them would mean duplicating the agent every time.
CONSEQUENCE: More flexible. The qualifier can be called by other
             processes in the future without rewriting anything.
```

---

## Executed examples

This skill's contract (completeness of the 5 blocks) is verifiable with a small validator:

```console
$ python -c "
def missing_teaching_blocks(text):
    checks = {'tree': '🗺️' in text, 'xray': '🔍' in text, 'connections': '🔗' in text, 'analogy': '💡' in text, 'decisions': '⚠️' in text}
    return [k for k, ok in checks.items() if not ok]
complete = '🗺️ x\n🔍 x\n🔗 x\n💡 x\n⚠️ x'
print('missing:', missing_teaching_blocks(complete))
"
missing: []
```
<!-- executed: 2026-10-30 · exit=0 -->
(output with all 5 blocks present - Teaching Mode complete, 0 blocks missing.)

```console
$ python -c "
def missing_teaching_blocks(text):
    checks = {'tree': '🗺️' in text, 'xray': '🔍' in text, 'connections': '🔗' in text, 'analogy': '💡' in text, 'decisions': '⚠️' in text}
    return [k for k, ok in checks.items() if not ok]
incomplete = 'I will create the file X.'
missing = missing_teaching_blocks(incomplete)
print('missing:', missing)
import sys; sys.exit(1 if missing else 0)
"
missing: ['tree', 'xray', 'connections', 'analogy', 'decisions']
```
<!-- executed: 2026-10-30 · exit=1 -->
(a technical output with NONE of the 5 blocks - exactly what this skill exists to prevent.)

```console
$ python -c "
def missing_teaching_blocks(text):
    checks = {'tree': '🗺️' in text, 'xray': '🔍' in text, 'connections': '🔗' in text, 'analogy': '💡' in text, 'decisions': '⚠️' in text}
    return [k for k, ok in checks.items() if not ok]
partial = '🗺️ x\n🔍 x'
print('missing:', missing_teaching_blocks(partial))
"
missing: ['connections', 'analogy', 'decisions']
```
<!-- executed: 2026-10-30 · exit=0 -->
(PARTIAL output - only tree and x-ray - 3 blocks still missing; useful for reviewing an output in progress.)

## Anti-patterns

- ❌ Applying the 5 blocks to a purely conversational reply ("hi", "where did we stop?") - it becomes noise, see "When NOT to Activate".
- ❌ Mentioning a folder without showing what is inside it.
- ❌ Using a technical term (parser, hook, schema) without translating it in the same sentence.
- ❌ Going beyond 2 levels of "why" without asking whether the reader wants to go deeper.

## Proof

```bash
python -c "
def missing_teaching_blocks(text):
    checks = {'tree': '🗺️' in text, 'xray': '🔍' in text, 'connections': '🔗' in text, 'analogy': '💡' in text, 'decisions': '⚠️' in text}
    return [k for k, ok in checks.items() if not ok]
assert missing_teaching_blocks('🗺️🔍🔗💡⚠️') == []
assert len(missing_teaching_blocks('nothing here')) == 5
print('self-test OK')
"
```

## Final instruction for CLAUDE.md

Paste this block into your CLAUDE.md to activate Teaching Mode globally:

```markdown
## 🧠 Teaching Mode (ALWAYS ACTIVE)

When creating, modifying or explaining any technical element, you MUST include:
1. 🗺️ Full architectural tree showing WHERE the element lives (from the root)
2. 🔍 X-ray with: what it is, where it lives, inside what, connected to what, format and why
3. 🔗 Visual connection map with arrows and verbs
4. 💡 Analogy with company operations (sales, marketing, management)
5. ⚠️ Every technical decision explained: what, why, alternative, consequence

Rules:
- Never shorten paths without showing the full context
- Never use a technical term without an immediate translation
- Never mention a folder without showing what is inside it
- Go up to 2 levels deep. At the 3rd level, ask whether to go deeper.
- Use business language as the primary analogy.

Full reference: ${CLAUDE_PLUGIN_ROOT}/skills/teaching/SKILL.md
```
