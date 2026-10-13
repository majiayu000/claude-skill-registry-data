---
name: critique
description: Critique all unpushed commits before pushing to remote
argument-hint: "[branch-or-range]"
---

<Purpose>
Devil's Advocate critique of all unpushed commits. Spawns an independent adversarial reviewer that finds what is wrong, suboptimal, insufficient, faulty, or broken — and proposes concrete fixes — before code reaches the remote.
</Purpose>

<Use_When>
- Before pushing commits: "critique my changes", "review before push", `/critique`
- When you want a second opinion on uncommitted or unpushed work
- As a pre-PR quality gate
- When Claude has been writing code and you want an independent check
</Use_When>

<Do_Not_Use_When>
- Reviewing a PR that's already pushed — use `/review` or `code-reviewer` agent instead
- Deep multi-pass review needed — use `/deep-review` instead
- Only want security review — use `security-reviewer` agent directly
</Do_Not_Use_When>

<Why_This_Exists>
Claude writes code confidently. Too confidently. Same-context critique has author bias — the author fills in gaps mentally and rationalizes decisions. An independent subagent only sees the artifact and the codebase, catching flaws the author is blind to. This is the last line of defense before code reaches the remote.
</Why_This_Exists>

<Execution_Policy>
- The devils-advocate agent MUST run as an independent subagent (Task), never inline — this prevents author bias
- Agent is read-only (Write/Edit blocked)
- Agent uses opus model for thoroughness (user can override via config)
- Results are presented to the user with a clear PUSH / FIX FIRST recommendation
</Execution_Policy>

<Steps>
1. **Determine scope**:
   - If argument provided, use it as the git range (e.g., `HEAD~3..HEAD`, `abc123..def456`)
   - Otherwise, detect unpushed commits. A non-zero exit here just means the branch has
     no upstream; treat it as "try the fallback", not as an error to report:
     ```bash
     git log @{u}..HEAD --oneline
     ```
   - If that fails, try `origin/main` and then `origin/master`. This picks whichever
     exists and prints nothing when neither does:
     ```bash
     node -e "const{spawnSync}=require('node:child_process');for(const base of ['origin/main','origin/master']){const r=spawnSync('git',['log',base+'..HEAD','--oneline'],{encoding:'utf8'});if(r.status===0){process.stdout.write(r.stdout);break}}"
     ```
   - If no unpushed commits found, report **"Nothing to critique — no unpushed commits found."** and stop

2. **Gather context** (run in parallel):
   - Commit log: `git log <range> --format="%h %s" `
   - Changed files summary: `git diff <range> --stat`
   - Full diff: `git diff <range>`
   - If the full diff exceeds ~3000 lines, use `git diff <range> --stat` plus targeted `git diff <range> -- <file>` for the most critical files (prioritize: security-sensitive, core logic, new files)

3. **Spawn independent devils-advocate agent**:
   ```
   Task(subagent_type="oh-my-copilot:devils-advocate", model="opus", name="critique", prompt="
   INDEPENDENT PRE-PUSH CRITIQUE

   Review the following unpushed commits for flaws, suboptimal code, insufficient implementation,
   faults, and broken behavior. You are an independent reviewer — the author cannot see your
   investigation process, only your final report.

   ## Commits
   [paste commit log here]

   ## Changed Files
   [paste diff stat here]

   ## Full Diff
   [paste diff here]

   Produce a structured Pre-Push Critique report with PASS/FAIL for each criterion,
   file:line citations and proposed fixes for every FAIL, and a clear PUSH or FIX FIRST recommendation.
   ")
   ```

4. **Present results**: Display the structured critique report to the user exactly as returned by the agent.

5. **Ask the user**: Based on the recommendation:
   - If **PUSH**: "The critique found no blocking issues. Proceed with push?"
   - If **FIX FIRST**: "The critique found issues that should be fixed before pushing. Would you like to address them or push anyway?"
</Steps>

<Tool_Usage>
- Use Bash with `git log` and `git diff` to gather commit and diff data
- Use `Task(subagent_type="oh-my-copilot:devils-advocate", ...)` to spawn the independent reviewer
- Do NOT run the critique inline — it MUST be a separate subagent for independence
</Tool_Usage>

<Examples>
<Good>
User says: "/critique"
Agent runs: git log @{u}..HEAD --oneline → finds 3 unpushed commits
Agent runs: git diff @{u}..HEAD → gets the diff
Agent spawns: Task(subagent_type="oh-my-copilot:devils-advocate", model="opus", name="critique", prompt="...")
Agent presents: Structured report with 18 PASS, 3 FAIL, recommendation: FIX FIRST
Agent asks: "The critique found 3 issues. Fix them or push anyway?"
Why good: Full workflow, independent agent, clear recommendation.
</Good>

<Good>
User says: "/critique HEAD~5..HEAD"
Agent uses the provided range instead of auto-detecting upstream.
Why good: Respects user-provided scope.
</Good>

<Bad>
Agent reviews the diff itself without spawning a subagent.
Why bad: Same-context review has author bias. MUST use independent subagent.
</Bad>

<Bad>
Agent spawns the subagent but doesn't show the full report — just says "looks fine."
Why bad: User needs the detailed findings to make an informed decision.
</Bad>
</Examples>

<Output_Format>
[Display the full Pre-Push Critique report from the devils-advocate agent]

---
**Recommendation**: PUSH / FIX FIRST
[If FIX FIRST, list the critical FAILs that need attention]

Proceed with push, or fix the issues first?
</Output_Format>

<Final_Checklist>
- [ ] Unpushed commits detected (or user-provided range used)
- [ ] Full diff gathered (or targeted diffs for large changesets)
- [ ] Independent devils-advocate agent spawned (NOT inline review)
- [ ] Structured report with PASS/FAIL per criterion presented
- [ ] Every FAIL has file:line citation and proposed fix
- [ ] Clear recommendation issued (PUSH / FIX FIRST)
- [ ] User asked how to proceed
</Final_Checklist>
