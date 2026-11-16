---
name: review
description: "Use to review code, diffs, branches, PRs or repos; assess breakage; or handle review feedback."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "DietrichGebert/ponytail 4.7.0 skills/ponytail-review (lean tags); DietrichGebert/ponytail 5.3.2 skills/ponytail-review, skills/ponytail-audit, skills/ponytail-debt; mattpocock/skills review; obra/superpowers 7.0.0 skills/requesting-code-review (SKILL.md, code-reviewer.md), skills/receiving-code-review; cursor/plugins pstack 0.15.25 skills/blast-radius, skills/interrogate (reviewer-prompt.md, rubric.md); garrytan/gstack 1.60.1.0 review/SKILL.md.tmpl, review/checklist.md; MCT (local) ~/.claude/skills/code-review, ~/.claude/agents/reviewer.md"
---

# Review

Review like the engineer who gets paged when it breaks. In priority order, the change must be **correct, safe, hold under load, be tested, be fast, and be lean**. Lean still counts, because every extra line gets read, tested and fixed later.

| Ask | Branch |
|---|---|
| Review this, a diff, commit, branch or PR | A. Change review |
| Audit the repo, find bloat, what can I delete | B. Repo audit |
| List the shortcuts or the debt | C. Debt ledger |
| What could this break, blast radius, a small diff you don't trust | D. Blast radius |
| Review comments arrived from the user, a reviewer or a bot | E. Receiving feedback |

Branches A to D report and change no code. Apply fixes only when the user picks them ("fix 2 and 5") or asked up front ("review and fix").

## A. Change review

1. **Pin the scope.** Use what the user names: staged or uncommitted changes, a commit, a branch (`git diff <base>...HEAD` plus `git log <base>..HEAD --oneline`), or a PR (`gh pr diff <n>`). With nothing named, review the uncommitted changes, or the last commit if there are none. Done when: the ref resolves and the diff is non-empty.
2. **Read past the diff.** Read the callers of every changed function, what it calls, its tests and the README. When a signature, return value, enum or behavior changes, read every consumer. Find the expected load (README, deploy config) and state which load you assumed. For application motion changes, read [the motion review procedure](../frontend/references/motion-review.md); mocked product illustrations and cursor demos also use `stageshow`. Done when: you can trace data in, stored and out.
3. **Two axes, kept separate** so that one can't mask the other:
   - **Standards:** the repo's documented rules (CONTRIBUTING, AGENTS.md or CLAUDE.md, ADRs). Cite the rule. Skip whatever tooling already enforces.
   - **Spec:** the issue, PR body or plan behind the change (`#123` in commits, docs/specs). Report requirements that are missing or partial, behavior nobody asked for, and requirements implemented wrong, quoting the spec line. With no spec, write "Spec: none found".
4. **Hunt, in priority order:**
   1. **Bug:** a wrong result, a crash, an edge case (empty, zero, last item, rounding, time zones), a caller the change broke, or a fix applied in one caller while the shared function stays broken.
   2. **Safe:** injection, secrets, unchecked user input, unsafe HTML, weak randomness. Data loss from swallowed errors, writes in the wrong order or a missing transaction.
   3. **Load:** check-then-write races, a query per item, lists or memory that only grow, O(n²) on large input, per-process state that must be shared.
   4. **Tested:** risky new logic (a branch, a parser, money, auth, data writes, a bug fix) with no test that fails when it breaks. Ask for one good test, not coverage.
   5. **Fast:** a big slowdown is a finding. A small win is nice-to-have.
   6. **Lean**, tagged with the replacement named:
      - `delete:` dead code or a speculative feature
      - `reuse:` the repo already has it (give the path)
      - `stdlib:` the standard library already does it (name the function)
      - `native:` the platform does it, or a dependency was added for a few lines
      - `yagni:` an abstraction with one implementation, or config nobody sets
      - `shrink:` the same logic in fewer lines (show the form)
   7. **Architecture**, only when the diff adds or reshapes a module boundary, or callers repeatedly reach into a module's internals or pass through shallow wrappers. Report one `architecture:` finding naming the boundary and the callers, and point to `/honey:architecture` for the redesign. Don't run that skill inline or add this lens to every review.
5. **Check before reporting.** Each finding needs a concrete case: "this input leads to this wrong result". Re-read the lines and confirm the caller exists, the value can really be empty, or the code really is unused (grep the whole tree, including tests, config and string references). A claim that something is "handled elsewhere" needs the line cited, and "tests cover this" needs the test named. A `shortcut:` or `ponytail:` comment that names its limit is a decision, not a finding, unless the expected load already crosses that limit. Drop style taste, "consider…", and anything the diff already addresses. Done when: every finding has a case and a citation.

For a large diff, or when the session context is crowded, run the Standards and Spec axes as two parallel read-only subagents using `references/reviewer-prompt.md`, then lay their reports side by side without reranking.

**Output.** One finding per line, numbered across all groups. Skip empty groups.

```
What this change does: <two sentences>. Load assumed: <one user | N concurrent ...>.
Must fix
1. `api/orders.ts:40` bug: <input> gives <wrong result>. Fix: <smallest fix; prefer deleting code>.
Should fix
2. `lib/retry.ts:12` tested: new backoff branch has no failing-when-broken test. Fix: <test>.
Nice to have
3. `util/dates.ts:4` native: moment imported for one format call. `Intl.DateTimeFormat`, 0 deps.
4. `billing/invoice.ts:88` architecture: 5 callers read `invoice._lines` directly. A deeper Invoice interface would hide it; see `/honey:architecture`.
Standards: 5. `<file:line>` breaks "<rule>" (CONTRIBUTING.md).
Spec: 6. missing "<quoted requirement>".
Verdict: fix 1 and 5 first.   net: -24 lines possible.   Not checked: <what mattered and could not run>.
```

If nothing is found, give the summary, then `Looks good. Ship.`, then one line on what you checked.

**Second opinion.** When the user asks, ask the other agent with the filled `references/reviewer-prompt.md`: from Claude Code run `codex exec -s read-only "<prompt>"`, and from Codex run `claude -p --permission-mode plan "<prompt>"`. If that CLI is missing, say so and skip. Merge the answers as lead reviewer: a finding both raised is the strongest signal; mark each of the other's findings as act on, consider, or dismissed with a reason. Response mode does not request a second opinion.

## B. Repo audit

Use the same hunt and the same check-before-reporting as A, across the scope the user names (default: the whole repo).

1. Map it: README, build and deploy config, the dependency list, entry points (routes, handlers, jobs, CLI) and tests. State the load you assumed.
2. Trace the main flows end to end and read the costly paths fully: user input, money, auth, data writes, background jobs, shared state. In a big repo go deep where a mistake costs most, and list what you didn't read.
3. Rank at most 20 findings in Must / Should / Nice groups, and say how many smaller ones you left out.

End with `Verdict: <healthy | fix N first>`, then `Lean: -<N> lines, -<M> dependencies possible.`, then `Not checked: <parts>`.

## C. Debt ledger

```
git grep --no-index --exclude-standard -nE '(#|//|/[*]|--|<!--) ?(shortcut|ponytail):'
```

Use the user's marker word instead if they name one. Write one row per marker, grouped by file, skipping hits that aren't deferrals:

`<file>:<line>, <what was simplified>. limit: <named limit>. upgrade: <trigger>.`

Tag `no-trigger` on markers that name no upgrade trigger, because those quietly become permanent. Tag `crossed` on markers whose limit the expected load already exceeds. End with `<N> markers, <M> no-trigger, <K> crossed.` If there are none, write `No shortcut debt.`

## D. Blast radius

Listing callers is the easy part. The job is the breakage grep won't show. Read `references/blast-radius.md` for the steps and the proof ladder. The core is to find the one fact that makes the change safe and prove it by running real code, or mark it `unproven`.

## E. Receiving feedback

1. Read every item before acting. If any item is unclear, ask about those items before implementing any of them, because items are often related.
2. Verify each one against the code. Is it correct for this codebase and this stack version? Does it break existing behavior? Is there a reason for the current code? Did the reviewer see the full context? For "implement this properly", grep for real usage first, and propose deleting it if nothing calls it.
3. Respond per item:
   - **Correct:** fix it, then reply with the fix and its location: `Fixed: <what>, <file:line>`.
   - **Wrong:** push back with evidence such as a test, a `file:line` or a version constraint.
   - **Conflicts with an earlier decision by the user:** ask the user.
   Skip agreement theatre and thanks, because the fix is the acknowledgement. If your pushback turns out wrong, write: `Checked <x>, you're right because <y>. Fixing.`
4. Implement in order: blocking issues (breakage, security), then simple fixes, then complex ones. Run the relevant check after each.
5. When the user wants replies posted on GitHub, reply in the inline thread: `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body='…'`.

Done when: every item is fixed with a check, pushed back with evidence, or waiting on the user.
