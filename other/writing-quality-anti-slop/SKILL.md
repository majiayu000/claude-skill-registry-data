---
name: writing-quality-anti-slop
description: Kill-list of overused AI vocabulary and structural tells. Prevents robotic, AI-generated prose in documentation, READMEs, blog posts, and user-facing text. Use when writing any text that humans will read.
---

# Writing Quality & Anti-Slop

## Problem it solves

AI-generated text has recognizable tells that mark it as robotic:
- Overused vocabulary ("delve", "leverage", "robust", "utilize")
- Forced structural patterns (triads, sycophantic openers)
- Verbose preamble before getting to the point
- Fake enthusiasm and hedging
- Readers lose trust in content that sounds machine-written

## Protocol

### 1. Kill-list — never use these words

| Word/Phrase | Instead use |
|---|---|
| delve | explore, examine, or just say what you're doing |
| leverage | use |
| robust | reliable, thorough, or specific |
| utilize | use |
| game-changer | significant, transformative, or specific impact |
| paradigm | model, approach, way |
| revolutionize | change, improve |
| cutting-edge | modern, recent, specific technology name |
| seamless | smooth, integrated, or nothing |
| granular | detailed, fine-grained, or specific |
| holistic | complete, comprehensive, or nothing |
| optimize | improve, make faster, specific metric |
| ecosystem | environment, platform, system, community |
| empower | enable, allow, help |
| innovative | new, different, or specific feature |
| navigate | handle, deal with, work with |
| landscape | area, field, market |
| robust | specific quality (reliable, fast, secure) |
| deep dive | examine, explore, analyze |
| actionable | specific, concrete, useful |
| best-in-class | specific comparison or nothing |
| state-of-the-art | specific technology or nothing |

### 2. Structural tells — avoid these patterns

**The forced triad**: "X, Y, and Z" where the list has exactly three items and sounds rehearsed.
- ❌ "This solution is fast, reliable, and scalable."
- ✅ "This solution handles 10K QPS with 99.9% uptime."

**Sycophantic openers**: Padding before the substance.
- ❌ "Great question! That's an excellent point. Let me dive deep into that."
- ✅ Start with the answer. "The API uses OAuth2 with refresh tokens."

**Verbose self-praise**: "I've carefully analyzed" / "My thorough investigation shows"
- ❌ "I've taken a comprehensive look at your codebase and have identified several areas for improvement."
- ✅ "Three issues found in auth.rs: unvalidated redirect (line 42), hardcoded secret (line 89), missing rate limit."

**False hedging**: "It seems like" / "I believe" / "In my opinion" — when you should be certain or uncertain with evidence.
- ❌ "I believe the issue might be related to caching."
- ✅ "The cache TTL is 5 minutes but the data changes every minute — that's the likely cause."

**The conclusion that adds nothing**: Restating what was already said.
- ❌ "In conclusion, implementing these changes will result in a more robust, scalable, and maintainable system."
- ✅ (Just stop. The last substantive sentence is the conclusion.)

### 3. How to write instead

- **Short sentences**. One idea per sentence.
- **Specific over general**. Don't say "improved performance", say "reduced P95 latency from 200ms to 50ms"
- **Active voice**. "The API returns the user" not "The user is returned by the API"
- **No preamble**. State the conclusion or recommendation first, then explain.
- **No filler transitions**. "Furthermore", "Moreover", "Additionally" — delete unless they add logical flow.

### 4. Tone guidelines

- **Professional but direct**: Like a senior engineer explaining to a peer
- **No enthusiasm inflation**: "This works" not "This is amazing!"
- **No false modesty**: "I think" / "Perhaps" / "Maybe" — commit or don't
- **No corporate speak**: "Circle back", "Touch base", "Synergize"

## Detection triggers

Activate when:
- Writing or editing documentation, README, blog posts, or user-facing text
- Writing commit messages, PR descriptions, or code comments
- Reviewing text for AI-slop before shipping
- User says "make this sound less like AI", "write this", "draft a post"

## When NOT to use

- Internal notes or scratchpads
- Code generation (code has different quality standards)
- User explicitly asks for "detailed, thorough" writing
- Brainstorming or early drafts (edit later)

## Cross-references

- **anti-sycophancy** — Sycophantic openers and performative enthusiasm are forms of sycophancy. This skill provides the vocabulary kill-list; anti-sycophancy covers the behavioral pattern.

- **adr-and-documentation** — ADRs and docs should follow these writing guidelines. No slop in architectural documentation.

- **follow-existing-patterns** — Writing style should match the project's existing documentation voice and tone.

- **code-review** — The readability axis should flag AI-slop language alongside code quality issues.

- **self-validate** — After writing, self-validate against the kill-list before presenting to the user.
