---
name: resolve-ambiguity
description: Systematic ambiguity resolution through tiered information gathering. Use when facing unclear requirements, unknown context, uncertain implementation choices, or any situation where guessing would be risky.
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - Task
---

<objective>
Resolve ambiguity through a systematic process that prioritizes accurate information over guessing. This skill determines the best source for missing information and retrieves it efficiently.

Core principle: **Rather ask than guess.** Wrong assumptions waste more time than clarifying questions.
</objective>

<quick_start>
<decision_tree>
When you encounter ambiguity, classify it:

1. **Technical/Factual** - "How does X work?" "What is the correct syntax?"
   → Likely found in project or online sources
   → Follow the tiered lookup process

2. **Intent/Choice** - "Which approach should I use?" "What does the user want?"
   → Requires user input
   → Use AskUserQuestion immediately
</decision_tree>

<immediate_action>
If ambiguity is about user intent or preference:
→ Skip lookup, go directly to `<user_clarification>` section

If ambiguity is technical/factual:
→ Follow `<tiered_lookup>` process
</immediate_action>
</quick_start>

<tiered_lookup>
<description>
For technical/factual ambiguity, check sources in this order. Stop as soon as you find authoritative information.
</description>

<tier_1 name="Project Context Files">
**Check first - fastest and most relevant**

1. Read `.claude/workspace-info.toon`
   - Contains workspace structure, projects, capabilities, outcomes
   - Shows current focus and IDE configuration

2. Read `.claude/project-info.toon`
   - Contains project technology, dependencies, entry points
   - Shows repository and IDE details

```
Task(subagent_type="Explore", model="haiku", prompt="""
Check for context files:
- .claude/workspace-info.toon
- .claude/project-info.toon

If found, extract relevant information about: {specific question}
Return only the relevant fields, not the entire file.
""")
```
</tier_1>

<tier_2 name="Architectural Files">
**Check second - project-specific patterns**

Look within current scope for:
- `CLAUDE.md` - Project instructions and conventions
- `README.md` - Project overview and setup
- `ARCHITECTURE.md` or `docs/architecture.md` - Design decisions
- Configuration files relevant to the question:
  - `package.json`, `tsconfig.json` (JavaScript/TypeScript)
  - `pyproject.toml`, `setup.py` (Python)
  - `Cargo.toml` (Rust)
  - `.env.example` (environment variables)

```
Glob for architectural files:
- **/CLAUDE.md
- **/README.md
- **/ARCHITECTURE.md
- **/docs/*.md
```
</tier_2>

<tier_3 name="Documentation via MCP">
**Check third - if MCP documentation tools are available**

If MCP tools are available for documentation lookup:
- Use `mcp__context7__*` for library documentation
- Use `mcp__firecrawl__*` for web documentation
- Use other documentation-specific MCP tools

These provide structured access to official documentation.
</tier_3>

<tier_4 name="Web Search Official Sources">
**Check fourth - for external APIs, libraries, standards**

Use WebSearch and WebFetch for:
- Official documentation sites
- GitHub repositories of libraries
- API reference documentation
- RFC or specification documents

<search_strategy>
1. WebSearch with specific query: "{library/API name} documentation {specific topic} 2024 2025"
2. WebFetch the most authoritative result (official docs preferred)
3. Extract only the relevant information

Prefer sources in this order:
1. Official documentation (*.dev, *.io, readthedocs)
2. GitHub repository README/docs
3. Stack Overflow with high votes (for edge cases)
</search_strategy>
</tier_4>

<when_to_stop>
Stop the tiered lookup when:
- You find authoritative information that resolves the ambiguity
- You've checked all relevant tiers without finding information
- The information found indicates this is actually a choice/intent question

If all tiers exhausted without answer → proceed to `<user_clarification>`
</when_to_stop>
</tiered_lookup>

<user_clarification>
<description>
For intent/choice questions, or when tiered lookup fails, ask the user directly. **Never guess when user input is available.**
</description>

<principles>
1. **Explain what you need** - Tell the user what information is missing
2. **Explain why you need it** - Describe how the answer affects the outcome
3. **Offer smart choices** - If you can infer likely options, present them
4. **Best practice first** - Order choices with recommended approach at top
5. **Bad ideas last** - If including risky options, put them at the bottom
6. **Always allow custom input** - User can always provide their own answer
7. **When uncertain, don't guess choices** - Better to ask open-ended than offer wrong options
</principles>

<with_known_choices>
When you can confidently identify the options:

```
AskUserQuestion with structure:
- Question: Clear, specific question explaining context
- Options ordered by preference:
  1. Best practice / Most common / Recommended
  2. Good alternative
  3. Another valid option
  4. Least recommended / Has drawbacks
- Each option includes description explaining implications
- User can always select "Other" for custom input
```

<example>
Question: "Which authentication approach should I implement?"

Options (ordered best → least recommended):
1. **JWT with refresh tokens** - Industry standard, stateless, works well with APIs
2. **Session-based auth** - Simple, works well for server-rendered apps
3. **OAuth2 only** - Good for social login, but adds complexity
4. **Basic auth** - Simple but less secure, only for internal tools

Each option explains trade-offs so user can make informed choice.
</example>
</with_known_choices>

<without_known_choices>
When you cannot confidently identify the options:

**DO NOT GUESS.** Ask an open-ended question instead.

```
AskUserQuestion:
- Question: Explain what you need to know and why
- Options:
  1. A general direction if you have any hint
  2. (Keep options minimal or omit entirely)
- Allow free-form input as primary response method
```

<example>
Instead of guessing configuration options:

Question: "I need to configure the database connection. What database are you using and what are the connection details?"

Options:
1. **I'll provide the details** - Let me type the configuration

This is better than guessing "PostgreSQL" or "MySQL" when you don't know.
</example>
</without_known_choices>

<formatting_rules>
1. **Single question at a time** - Don't overwhelm with multiple questions
2. **2-4 options maximum** - More becomes confusing
3. **Descriptions are required** - Every option needs context
4. **No yes/no when options exist** - Offer the actual choices instead
5. **Acknowledge uncertainty** - "I'm not sure which applies, so..."
</formatting_rules>
</user_clarification>

<ambiguity_categories>
<category name="Technical Implementation">
**Examples**: "How do I call this API?" "What's the correct syntax?"

**Resolution path**:
1. Check project context files
2. Check architectural docs
3. WebSearch official documentation
4. If still unclear → ask user for clarification
</category>

<category name="Project Conventions">
**Examples**: "What naming convention?" "Where should this file go?"

**Resolution path**:
1. Check CLAUDE.md for explicit conventions
2. Check existing code for patterns (Glob + Read)
3. Check README/contributing guide
4. If no clear pattern → ask user preference
</category>

<category name="User Intent">
**Examples**: "Which feature first?" "Should I also refactor X?"

**Resolution path**:
1. Skip lookup - this requires user input
2. AskUserQuestion immediately
3. Present inferred options if confident
4. Allow open-ended response if uncertain
</category>

<category name="External Dependencies">
**Examples**: "Which version of X?" "What's the API for Y?"

**Resolution path**:
1. Check package.json/pyproject.toml for versions
2. WebSearch for current documentation
3. WebFetch official docs
4. If version-specific behavior → confirm with user
</category>

<category name="Configuration Values">
**Examples**: "What port?" "What environment variables?"

**Resolution path**:
1. Check .env.example or config files
2. Check project-info.toon
3. Check README for setup instructions
4. If sensitive values → ask user (never guess credentials)
</category>

<category name="Architectural Decisions">
**Examples**: "Monolith or microservices?" "Which pattern to use?"

**Resolution path**:
1. Check ARCHITECTURE.md or design docs
2. Check workspace-info.toon for project structure
3. This is usually a choice → AskUserQuestion
4. Present trade-offs clearly in options
</category>
</ambiguity_categories>

<process>
<step_1>
**Detect ambiguity**: Identify what information is missing and classify it:
- Technical/Factual → Tier lookup
- Intent/Choice → User clarification
</step_1>

<step_2>
**For technical ambiguity**: Execute tiered lookup in order:
1. Project context files (.claude/*.toon)
2. Architectural files (CLAUDE.md, README, docs)
3. MCP documentation tools (if available)
4. WebSearch/WebFetch official sources
</step_2>

<step_3>
**For intent ambiguity or lookup failure**: Use AskUserQuestion:
- Explain what's needed and why
- Offer choices ordered by recommendation (if known)
- Don't guess choices if uncertain
- Always allow custom input
</step_3>

<step_4>
**Apply the answer**: Use the information to proceed with the task.
Document any decisions made for future reference.
</step_4>
</process>

<success_criteria>
Ambiguity is resolved when:

- **Information found**: Authoritative source confirms the answer
- **User clarified**: User provided explicit direction
- **Documented**: Decision is captured for future reference

Signs of good resolution:
- No guessing occurred
- User wasn't asked unnecessary questions
- The answer came from the most appropriate source
- Forward progress is now possible
</success_criteria>

<anti_patterns>
<pattern name="Guessing and Hoping">
**Wrong**: Making assumptions and proceeding without verification
**Instead**: Take 30 seconds to check or ask
</pattern>

<pattern name="Too Many Questions">
**Wrong**: Asking 5 questions before doing anything
**Instead**: Ask only what's blocking immediate progress
</pattern>

<pattern name="Vague Questions">
**Wrong**: "How should I proceed?"
**Instead**: "Should I use approach A (benefit) or B (benefit)?"
</pattern>

<pattern name="Assuming User Expertise">
**Wrong**: "Should I use the factory pattern or strategy pattern?"
**Instead**: Explain the options in plain terms with trade-offs
</pattern>

<pattern name="Hiding Behind Defaults">
**Wrong**: Silently using a default without mentioning alternatives
**Instead**: "I'll use X (the standard approach). Let me know if you'd prefer Y."
</pattern>
</anti_patterns>
