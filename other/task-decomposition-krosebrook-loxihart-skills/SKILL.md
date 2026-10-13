---
name: task-decomposition
description: Decompose complex multi-part requests into parallel workstreams with dependency tracking and integration planning. Use this skill whenever a request involves 3 or more distinct components, domains, or deliverables that could be worked on independently — even if the user doesn't explicitly ask for decomposition. Triggers on multi-deliverable requests like "build X + Y + Z", "create A, B, and C", "audit these 4 things", or any task where components span different domains (frontend + backend, research + writing + formatting, design + code + deploy). Also triggers when the user says "break this down", "decompose", "parallel plan", "workstreams", or "what are all the pieces". Even casual compound requests like "set up auth, database, and deployment" should activate this skill. Do NOT trigger on simple multi-step tasks within a single domain (e.g., "write a function that validates, transforms, and returns data" — that's one workstream with sequential steps, not parallel workstreams).
metadata:
  version: "1.0.0"
---

# Task Decomposition & Parallel Reasoning

## Purpose

Teach Claude to think in **parallel workstreams** instead of processing complex requests linearly. When someone asks for something with 3+ distinct components, Claude decomposes the request, identifies what's independent vs. dependent, surfaces cross-cutting concerns, and structures its response so nothing gets dropped or poorly integrated.

## Why this matters

Without this skill, Claude processes compound requests as a single monolithic task — walking through everything sequentially, often losing coherence on later components or forgetting integration points. The result: the first component gets deep treatment, the last gets a paragraph, and nobody planned how they connect.

With this skill, Claude plans the workstream map first, then executes each stream at consistent depth, with explicit integration points.

## When to activate

**Activate when ALL of these are true:**
1. The request contains 3+ distinct components, deliverables, or domains
2. At least 2 of those components could be worked on independently
3. The request is complex enough that a linear pass would likely drop something

**Do NOT activate when:**
- The request is a single domain with sequential steps (write → test → deploy is one stream)
- The request has 2 or fewer components (just handle it directly)
- The user explicitly asked for a quick/LITE response
- The task is conversational, not deliverable-oriented

## Relationship to staff-engineer-v4

**For engineering/build requests:** This skill activates *inside* staff-engineer-v4's Step 3 (Plan). Staff-engineer-v4 handles the outer loop (Clarify → Stack → Plan → Implement → Document → Critique). During the Plan step, if the implementation involves 3+ parallel workstreams, this skill structures those workstreams before staff-engineer-v4 proceeds to Implement.

**For non-engineering requests:** This skill operates standalone. Multi-part content creation, research tasks, audit projects, and operational work all benefit from workstream decomposition without needing staff-engineer-v4's engineering-specific workflow.

**Priority rule:** If both skills trigger, staff-engineer-v4 is the outer wrapper. Task Decomposition is the inner planning engine. They never compete — they layer.

---

## The Decomposition Process

### Step 1: Identify workstreams (silent — do this in your reasoning)

Parse the request and extract distinct workstreams. A workstream is a unit of work that:
- Has its own domain expertise (frontend, backend, content, research, design, infra)
- Could be started without waiting for other workstreams to finish
- Produces a distinct deliverable or artifact

For each workstream, identify:
- **What:** The deliverable or outcome
- **Domain:** The expertise area
- **Inputs needed:** What does this workstream need to start?
- **Outputs produced:** What does this workstream hand off?

### Step 2: Map dependencies

Classify relationships between workstreams:

- **Independent:** Can start immediately, no dependencies. These are your parallel opportunities.
- **Dependent:** Requires output from another workstream before starting. These must be sequenced.
- **Cross-cutting:** Decisions in one workstream constrain another (e.g., auth model affects both frontend and backend). These need to be resolved FIRST, before parallel work begins.

Cross-cutting concerns are the most commonly missed piece. Look for:
- Shared data models or schemas
- Authentication/authorization decisions
- API contracts between components
- Naming conventions or style guides
- Environment or deployment constraints
- Error handling patterns

### Step 3: Present the workstream map (only if 3+ workstreams)

Show the decomposition concisely before executing. Format:

```
## Workstream map

**Cross-cutting (resolve first):**
- [Decision that affects multiple streams]
- [Shared constraint or contract]

**Parallel workstreams:**
1. [Workstream A] — [1-line description]
2. [Workstream B] — [1-line description]
3. [Workstream C] — [1-line description]

**Sequential (depends on above):**
4. [Integration/assembly step] — depends on 1, 2, 3

**Estimated depth:** [Balanced / Front-loaded / Back-loaded]
```

Keep this map to 10-15 lines max. It's a navigation aid, not a document. The user should be able to glance at it and know what's coming.

### Step 4: Resolve cross-cutting concerns

Before touching any workstream, make decisions on shared concerns. State each decision explicitly:

> **Auth model decision:** JWT with refresh tokens, Supabase Auth provider. This affects workstreams 1 (frontend login flow), 2 (backend middleware), and 3 (RLS policies).

These decisions become constraints that every subsequent workstream respects.

**When you can't resolve a cross-cutting concern without user input, ask immediately.** Do not guess and proceed — a wrong assumption here cascades into every workstream. Frame the question with your best recommendation and why:

> I need to resolve the event trigger pattern before proceeding — it affects workstreams 3 and 4. My recommendation is a Supabase database webhook → n8n fan-out, because it keeps the registration form simple and gives you retry logic for free. Does that work, or do you have a different pattern in mind?

This is the one place where asking a clarifying question mid-response is worth the interruption. A wrong cross-cutting decision costs more than the delay.

### Step 5: Execute workstreams at consistent depth

Work through each workstream, giving each **proportional depth** based on complexity — not based on order. The third workstream should get the same quality treatment as the first.

For each workstream:
1. Reference the cross-cutting decisions that constrain it
2. Produce the deliverable or output
3. Explicitly note what this workstream hands off to dependent workstreams
4. If a workstream's deliverable is best produced by another installed skill (e.g., a docx by loxihart-doc-generator, a presentation by the pptx skill), name the skill and describe what it should produce — then either chain to it or flag it for the user

**Depth balancing rule:** If you're running long on an early workstream, compress it. The user asked for N things — delivering 1 deeply and N-1 shallowly is worse than delivering all N at consistent medium depth. You can always go deeper on a specific stream if the user asks.

### Step 6: Integration checkpoint

After all parallel workstreams are complete, explicitly handle integration:

1. **Verify contracts:** Do the outputs from each workstream actually connect? Does the frontend call the API endpoints the backend defined? Does the database schema support the queries the backend needs?
2. **Surface gaps:** What did the parallel workstreams each assume about the others that needs reconciliation?
3. **Produce the integration artifact:** This might be a wiring diagram, a test plan, a deployment sequence, or just a paragraph explaining how everything connects.

---

## Output calibration

**For 3-4 workstreams:** Show the map, resolve cross-cutting, execute each stream, brief integration note. This is the common case.

**For 5-7 workstreams:** Show the map, resolve cross-cutting, execute each stream at compressed depth, thorough integration section. Warn the user that depth per stream is limited and offer to go deeper on specific streams.

**For 8+ workstreams:** Show the map, resolve cross-cutting, group related streams into 3-4 clusters, execute clusters, integration section. At this scale, individual stream depth is necessarily shallow — suggest breaking into multiple conversations or sessions.

---

## Examples

### Example 1: Engineering build (nests inside staff-engineer-v4)

**User:** "Build an e-commerce platform with React frontend, Python API, PostgreSQL database, and Stripe payments"

**Workstream map:**
- Cross-cutting: Data model (products, orders, users), auth model (Supabase Auth + RLS), API contract (REST endpoints)
- Parallel: Frontend (React + Tailwind), Backend (FastAPI), Database (PostgreSQL schema + RLS), Payments (Stripe integration)
- Sequential: Integration testing (depends on all 4), Deployment (depends on integration)

### Example 2: Content/operational (standalone)

**User:** "Create a weekly newsletter edition with research brief, non-tech summary, and tech department deep-dive"

**Workstream map:**
- Cross-cutting: This week's theme/topic, key developments to cover
- Parallel: Research brief (sources + analysis), Non-tech tier (accessible summary), Tech dept tier (technical depth)
- Sequential: Final review (consistency across tiers), Formatting (HTML + Teams + docx)

### Example 3: Audit/analysis (standalone)

**User:** "Audit our codebase for security issues, performance bottlenecks, test coverage gaps, and documentation holes"

**Workstream map:**
- Cross-cutting: Repo structure, tech stack, deployment environment
- Parallel: Security audit (OWASP), Performance analysis (profiling), Test coverage (gap analysis), Documentation audit (completeness)
- Sequential: Prioritized remediation plan (synthesizes all 4 findings)

### Example 4: Single-domain pipeline (DO NOT decompose)

**User:** "Write a Python function that validates URLs, fetches content, and summarizes each page"

This is validate → fetch → summarize — sequential steps in one function, not parallel workstreams. Just write the function directly. The fact that there are 3 verbs does not mean there are 3 workstreams.

---

## Anti-patterns to avoid

**Over-decomposition:** "Write a blog post about AI" is NOT 3 workstreams (research, writing, editing). That's one workstream with sequential steps. Only decompose when components are genuinely independent.

**Decomposition theater:** Don't show a workstream map for simple requests just because the skill triggered. If you start decomposing and realize it's actually 2 workstreams, skip the map and just execute.

**Unbalanced depth:** The most common failure mode. You spend 80% of tokens on the first workstream and rush through the rest. Track your depth and compress early streams if needed.

**Ignoring cross-cutting concerns:** The second most common failure. Two workstreams make contradictory assumptions about a shared interface. Always resolve shared decisions before parallel execution.

**Map without execution:** Producing a beautiful decomposition plan and then asking "which workstream should I start with?" defeats the purpose. Decompose AND execute in the same response unless the scope is genuinely too large.

---

## Quality checklist (internal — don't show to user)

Before finalizing a decomposed response, verify:
- [ ] Every workstream from the map is addressed in the response
- [ ] Depth is roughly proportional across workstreams (no 80/20 skew)
- [ ] Cross-cutting decisions are stated before workstream execution
- [ ] Integration points are explicitly handled
- [ ] Dependent workstreams reference outputs from their dependencies
- [ ] Nothing from the original request was silently dropped
