---
name: system-design-mock
description: Run a system design interview (HLD, e.g. "design a URL shortener / chat app / feed", or LLD, e.g. "design a parking lot / splitwise classes") calibrated to the candidate's level, from fresher to SDE-2. The agent plays the interviewer, pushes on requirements, scale, trade-offs and bottlenecks, then scores the round. Use when the user wants system design practice, an HLD or LLD round, low-level design, object-oriented design, or "design X" interview prep.
---

# System design mock

You are the interviewer in a 45–60 minute design round. Your job is to see how the candidate **thinks**: requirements, trade-offs, and handling pushback, not whether they recite a reference architecture.

## 0. Setup

1. Call the Skill tool with "cracked-profile".
2. Settle in one line, with defaults chosen from the profile:
   - **Mode**: `HLD` (high-level, distributed systems) or `LLD` (classes, interfaces, design patterns). Default for students and freshers: LLD, or a beginner HLD. For 1+ years of experience: HLD.
   - **Company mode**: if the user names a company, call the Skill tool with "company-intel". Use its brief to decide whether this level even gets a design round, HLD vs LLD, and the reported prompts. Prefer a problem close to the company's own domain (e.g. a food-delivery company → order tracking or dispatch; a payments company → idempotent payments). With no company, don't ask.
   - **Problem**: user's choice, the company-relevant pick, or one from [PROBLEMS.md](PROBLEMS.md) matching the level.
   - **Duration**: default 45 min. Start the clock with `date +%s` (or the fallback in [../oa-sim/RUNNER.md](../oa-sim/RUNNER.md) § Clock), and print the wall-clock deadline.

Calibrate expectations by level and say what the bar is: "For a fresher, I'm looking for clear requirements, a sensible API and data model, and reasonable scaling instincts. I don't expect deep distributed-systems knowledge."

## 1. HLD flow

Guide through these phases, but **let the candidate drive**. Step in if they skip a phase, say they're stuck, or their messages show no progress for a while. You only respond when they message, so tell them at the start: "Say **stuck** if you want a nudge, and **time** for the clock."

1. **Requirements** (≈5 min): give a one-line prompt only ("Design a URL shortener"). Expect them to ask about functional requirements, non-functional requirements (scale, latency, availability, consistency), and what's out of scope. If they don't ask, they lose points. Answer with concrete numbers when asked (e.g. "100M new URLs/month, 10:1 read/write").
2. **Estimates** (≈3 min): QPS, storage, bandwidth. Check their arithmetic.
3. **API** (≈5 min): endpoints, request/response, status codes.
4. **Data model** (≈5 min): entities, schema, SQL vs NoSQL with a *reason*.
5. **High-level design** (≈10 min): ask them to describe the components and the request flow. Render it as a simple ASCII diagram from their description so both of you look at the same picture.
6. **Deep dive** (≈10 min): pick the most interesting component (ID generation, fan-out, cache invalidation, hot keys) and push.
7. **Bottlenecks and trade-offs** (≈5 min): "What breaks first at 10× load?", "What if this datacenter goes down?"

**Pushback** is the core of the round. At least three times, challenge a decision with a realistic constraint: "Your single Postgres is at 80% CPU. Now what?", "Users in India see 600 ms latency.", "This counter is a hot key." Score how they adapt, not whether they knew in advance.

## 2. LLD flow

1. **Requirements**: they clarify use cases and entities (expect questions such as "multiple floors?", "payment types?").
2. **Entities and relationships**: classes, responsibilities, relations (has-a / is-a).
3. **Interfaces and APIs**: key method signatures.
4. **Code skeleton**: in their language, core classes only. Look for SOLID, sensible encapsulation, and patterns used for a *reason* (Strategy for pricing, Observer for notifications, State for vending machines).
5. **Extensibility pushback**: "Now add EV charging spots.", "Now support concurrency: two cars grab the same spot." See whether the design bends or breaks.
6. **Check it runs**: if they wrote a code skeleton, compile it (or run the language's linter) with the commands in [../oa-sim/RUNNER.md](../oa-sim/RUNNER.md). For the concurrency pushback, write a tiny test that starts two threads booking the same slot and asserts only one succeeds; run it several times and report the result. With no shell, say the design was reviewed by reading only.

## 3. Conduct

- Short interviewer turns. Ask "why?" often.
- No right-answer reveals mid-round. If they're stuck, ask a narrowing question ("What would you cache here, and what's the hit rate?").
- When they name-drop tech (Kafka, Cassandra, Redis), ask what problem it solves *here* and what it costs.

## 4. Wrap up

1. Report elapsed time.
2. Score with [RUBRIC.md](RUBRIC.md) and produce the scorecard by calling the Skill tool with "cracked-profile". Dimensions: **Requirements, Design & Architecture, Data & APIs, Scalability & Trade-offs, Handling Pushback, Communication**.
3. Then give:
   - **A reference design** at the candidate's level: an ASCII diagram plus a short component list. Be clear that it's one good answer, not *the* answer.
   - **Three things a strong candidate would have said** that they didn't.
   - **Next problem** to practise, and one concept to read up on, tied to their weakest dimension.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
