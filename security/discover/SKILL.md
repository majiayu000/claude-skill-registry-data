---
name: discover
description: Spawn parallel specialist agents to scan the codebase and produce a prioritized improvement backlog
---

<Purpose>
Discover scans a codebase through 6 parallel specialist agents — Security, Quality, Tests, Performance, Documentation, and Architecture — and consolidates their findings into a prioritized improvement backlog. It surfaces actionable improvements that might otherwise go unnoticed.
</Purpose>

<Use_When>
- User wants to identify improvement opportunities: `/discover`, "scan for improvements", "find issues"
- Starting work on an unfamiliar codebase and wanting a quality baseline
- Preparing for a release and wanting a comprehensive quality check
- User wants a prioritized backlog of technical debt
</Use_When>

<Do_Not_Use_When>
- User wants to review a specific PR or changeset — use `/deep-review` instead
- User wants to fix a specific bug — delegate to debugger agent
- User wants to plan a feature — use `/plan` instead
</Do_Not_Use_When>

<Why_This_Exists>
Codebases accumulate technical debt across many dimensions — security gaps, missing tests, performance hotspots, documentation gaps, architectural drift. No single agent can efficiently cover all dimensions. Discover parallelizes specialist scans and produces a unified, deduplicated, severity-prioritized backlog that teams can act on.
</Why_This_Exists>

<Execution_Policy>
- All 6 scan agents MUST run in parallel (independent concerns)
- Each agent focuses exclusively on its category — no overlap
- Consolidation agent runs after all scans complete
- Default scope: encourage explicit scoping to a subdirectory. Full-codebase scan only if user explicitly requests it
- Output: `.omg/discover/backlog.md`
</Execution_Policy>

<Steps>
1. **Determine scope**: Parse the invocation for a scope argument
   - `/discover src/hooks/` → scope to `src/hooks/`
   - `/discover` → prompt user: "Which directory should I scan? (e.g., `src/`, `src/hooks/`, or `.` for full codebase)"
   - `/discover .` or `/discover --all` → full codebase scan

2. **Launch 6 parallel scans**: Fire all agents simultaneously

   **Scan 1 — Security**:
   ```
   Task(subagent_type="oh-my-copilot:security-reviewer", model="sonnet", name="discover-security", prompt="
   DISCOVERY SCAN: Security
   Scan the codebase at [SCOPE] for security vulnerabilities and risks.
   Focus on: OWASP Top 10, hardcoded secrets, injection risks, auth gaps, input validation.

   For each finding, output:
   FINDING:
   - category: security
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's wrong and why it matters]
   - suggestedAction: [specific fix recommendation]
   END_FINDING
   ")
   ```

   **Scan 2 — Quality**:
   ```
   Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="discover-quality", prompt="
   DISCOVERY SCAN: Code Quality
   Scan the codebase at [SCOPE] for anti-patterns, complexity hotspots, and SOLID violations.
   Focus on: God objects, high cyclomatic complexity (>10), deep nesting (>4 levels), code duplication, magic numbers.

   For each finding, output:
   FINDING:
   - category: quality
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's wrong and why it matters]
   - suggestedAction: [specific fix recommendation]
   END_FINDING
   ")
   ```

   **Scan 3 — Tests**:
   ```
   Task(subagent_type="oh-my-copilot:test-engineer", model="sonnet", name="discover-tests", prompt="
   DISCOVERY SCAN: Test Coverage
   Scan the codebase at [SCOPE] for test coverage gaps and test quality issues.
   Focus on: untested public APIs, missing edge case tests, flaky test patterns, missing integration tests.

   For each finding, output:
   FINDING:
   - category: tests
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's missing and why it matters]
   - suggestedAction: [specific test to add]
   END_FINDING
   ")
   ```

   **Scan 4 — Performance**:
   ```
   Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="discover-perf", prompt="
   DISCOVERY SCAN: Performance
   Scan the codebase at [SCOPE] for performance issues and optimization opportunities.
   Focus on: N+1 queries, O(n²) algorithms, unnecessary re-renders, missing caching, synchronous I/O in hot paths, memory leaks.

   For each finding, output:
   FINDING:
   - category: performance
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's slow and why it matters]
   - suggestedAction: [specific optimization]
   END_FINDING
   ")
   ```

   **Scan 5 — Documentation**:
   ```
   Task(subagent_type="oh-my-copilot:writer", model="haiku", name="discover-docs", prompt="
   DISCOVERY SCAN: Documentation
   Scan the codebase at [SCOPE] for documentation gaps.
   Focus on: undocumented public APIs, stale README sections, missing module-level docs, outdated examples.

   For each finding, output:
   FINDING:
   - category: documentation
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's missing]
   - suggestedAction: [what to document]
   END_FINDING
   ")
   ```

   **Scan 6 — Architecture**:
   ```
   Task(subagent_type="oh-my-copilot:architect", model="sonnet", name="discover-arch", prompt="
   DISCOVERY SCAN: Architecture
   Scan the codebase at [SCOPE] for architectural issues.
   Focus on: circular dependencies, abstraction leaks, coupling issues, module boundary violations, scaling bottlenecks.

   For each finding, output:
   FINDING:
   - category: architecture
   - severity: CRITICAL|HIGH|MEDIUM|LOW
   - title: [brief title]
   - file: [file:line]
   - description: [what's wrong structurally]
   - suggestedAction: [architectural improvement]
   END_FINDING
   ")
   ```

3. **Consolidate findings**: After all 6 scans complete, consolidate:
   - Collect all FINDING blocks from all agents
   - Deduplicate: merge findings that reference the same file:line with the same concern
   - Sort by severity (CRITICAL > HIGH > MEDIUM > LOW), then by category
   - Count totals per category and severity

4. **Generate backlog**: Write the consolidated backlog to `.omg/discover/backlog.md`:

   ```markdown
   # Discovery Backlog

   **Scope:** [scanned directory]
   **Generated:** [timestamp]
   **Total Findings:** N

   ## Summary
   | Category | Critical | High | Medium | Low | Total |
   |----------|----------|------|--------|-----|-------|
   | Security | ... | ... | ... | ... | ... |
   | Quality | ... | ... | ... | ... | ... |
   | Tests | ... | ... | ... | ... | ... |
   | Performance | ... | ... | ... | ... | ... |
   | Documentation | ... | ... | ... | ... | ... |
   | Architecture | ... | ... | ... | ... | ... |

   ## Critical Priority
   [findings...]

   ## High Priority
   [findings...]

   ## Medium Priority
   [findings...]

   ## Low Priority
   [findings...]
   ```

5. **Report**: Present a summary to the user with the backlog location
</Steps>

<Tool_Usage>
- Fire all 6 scan agents simultaneously using Task with appropriate agent types
- Use the model tiers from docs/shared/agent-tiers.md
- Writer agent uses haiku (documentation scan is lightweight)
- All other agents use sonnet
- Consolidation is done by the orchestrator (no additional agent needed for small backlogs)
- For large backlogs (50+ findings), spawn a code-reviewer (opus) for intelligent deduplication
</Tool_Usage>

<Examples>
<Good>
All 6 scans fired simultaneously:
```
Task(subagent_type="oh-my-copilot:security-reviewer", model="sonnet", name="discover-security", prompt="...")
Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="discover-quality", prompt="...")
Task(subagent_type="oh-my-copilot:test-engineer", model="sonnet", name="discover-tests", prompt="...")
Task(subagent_type="oh-my-copilot:code-reviewer", model="sonnet", name="discover-perf", prompt="...")
Task(subagent_type="oh-my-copilot:writer", model="haiku", name="discover-docs", prompt="...")
Task(subagent_type="oh-my-copilot:architect", model="sonnet", name="discover-arch", prompt="...")
```
Why good: All independent scans run in parallel for maximum throughput.
</Good>

<Bad>
Running scans sequentially:
```
security = Task(...) # wait
quality = Task(...) # wait
tests = Task(...) # wait
```
Why bad: Scans are independent and should run in parallel.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- If a scan agent fails, report the failure but continue with remaining scans
- If all scans fail, report the issue and suggest running individual reviews instead
- If scope is too broad and agents time out, suggest narrowing the scope
</Escalation_And_Stop_Conditions>

<Final_Checklist>
- [ ] All 6 scan agents launched in parallel
- [ ] Findings collected from all successful scans
- [ ] Findings deduplicated across agents
- [ ] Backlog sorted by severity (CRITICAL > HIGH > MEDIUM > LOW)
- [ ] Backlog written to `.omg/discover/backlog.md`
- [ ] Summary presented to user
</Final_Checklist>
