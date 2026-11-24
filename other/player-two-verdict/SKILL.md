---
name: player-two-verdict
description: Independently investigate a pasted security scanner finding (SAST, SCA, Secrets, IaC, or DAST) to determine if it's a true or false positive, using actual repo access rather than trusting the tool's verdict. Trigger this whenever the user pastes a security finding, vulnerability report, CVE, CWE, scanner output, or asks to triage, validate, review, or challenge a security finding. Also trigger on requests like "is this a real vulnerability" or "help me figure out if I can suppress this finding."
---

# Player Two Verdict

## Why this skill exists

Security scanners generate a lot of noise. SAST tools flag sinks without checking if input is sanitized. SCA tools flag packages without checking if the vulnerable function is ever called. The tool's severity rating is a generic CVSS score, not an assessment of what this finding means in this codebase.

The job here is to do what a senior AppSec engineer actually does when a finding lands on their desk: treat the tool's verdict as a claim, go verify it against the real code, and come back with an answer someone can act on. Never relay the scanner's conclusion as fact. Never accept "the tool says Critical" as a reason to skip checking whether it's actually exploitable here.

## Step 0: Prerequisite check

Confirm repo/filesystem access to the codebase the finding references, grepping and reading files is how every investigation in Step 3 actually works. If the user hasn't said which repo, or the finding references something that doesn't exist in the accessible codebase, that's the one case worth asking about rather than guessing.

A bare CVE/CWE ID with no real description attached will need a web search before investigation can start (see Step 1), this assumes that capability is available.

## Step 1: Parse the input

The user will paste whatever their scanner gave them. There's no fixed format, extract what's there: tool name, rule ID, CWE/CVE, reported severity, file/line (SAST/DAST) or package/version (SCA), code snippet, data flow path, endpoint/route (DAST), secret type and location (Secrets), resource and template path (IaC).

If a critical field is missing, e.g. no line number on a SAST finding, find it in the repo yourself with grep or search rather than asking the user. Only ask the user when the repo genuinely can't resolve it (e.g. they didn't say which repo, or the finding references something that doesn't exist in this codebase).

If the pasted CVE or CWE reference lacks a real description (just an ID, no context), web search for it before starting the investigation. You need to know what the vulnerability actually is before you can judge reachability.

## Step 2: Handle multiple findings

If the user pastes more than one finding, figure out whether they share a root cause first.

**Same root cause** (same CWE/rule/package, clearly one pattern repeated across locations): investigate the pattern once. Don't re-derive the same context for each instance, that's wasted work and increases the odds of an inconsistent verdict across nearly identical findings. Produce one verdict block, list every file:line instance underneath it.

**Unrelated findings** (different CWEs, different packages, no shared cause): cap it at 3-4 per run. Each unrelated investigation loads different context into the same window, and the more of them stack up, the higher the risk of cross-contaminating evidence between findings, attributing something you found for finding 2 to finding 5. If the paste has more than 4 unrelated findings, say so directly and either ask the user to split it up or proceed with the first 4, your call based on how the user framed the request.

After any multi-finding run, close with a note recommending the user run `/compact` before the next review. This keeps the context clean for the next investigation instead of letting old evidence linger and get pulled into a verdict it doesn't belong to.

## Step 3: Investigate

Work silently. Read files, grep, trace calls, check the lockfile, whatever the finding type requires. Don't narrate what you're doing as you do it, no "let me check the imports" or "searching for sanitization." The user wants the finished verdict, not a transcript of your process. Only the final output block described in Step 5 should appear in your response.

The goal of every investigation is the same regardless of finding type: find a reason the finding is wrong before you accept that it's right. If you can't find one after genuinely looking, that's what makes a true positive verdict credible.

### SAST

- Locate the exact line and function.
- Trace the input backward to its source. Is it attacker-controlled (request params, headers, user-submitted data) or internal/trusted (config, hardcoded values, another trusted service)?
- Check for sanitization, encoding, or parameterization between source and sink. Look past the obvious cases, custom wrapper functions and framework helpers often do this without being named anything the scanner would recognize.
- Check if the code path is actually reachable from an entry point, or if it's dead code, test-only, or behind a feature flag that's off.
- Check for compensating controls nearby: middleware, decorators, framework-level auto-escaping.

### SCA

- Confirm the vulnerable version is actually what's resolved in the lockfile, not just an allowed range in the manifest.
- Trace reachability to the vulnerable function itself, not just the package. A vulnerable package that's installed but whose vulnerable function is never called isn't exploitable here. Go as deep into the call graph as the finding's complexity actually requires, don't stop at "package is imported" if the CVE is specific to one function.
- Confirm the way the package is used actually matches the vulnerable code path described in the CVE.
- Determine direct vs transitive. If transitive, identify the direct dependency pulling it in, that's what the user actually has to act on.
- Assess package health, independent of the CVE verdict:
  - 6+ months behind current stable: note it as a minor issue.
  - Deprecated, EOL, or abandoned (no commits in 12+ months): note it as a major issue.
  - This applies regardless of what the CVE verdict turns out to be. An abandoned package is a standing risk even if this specific CVE isn't reachable. Don't let a false positive verdict erase that fact, it goes in its own line in the output either way.

### Secrets

- Determine if it's a live credential or a placeholder, example value, or test fixture.
- If it's not in the current HEAD, check git history. A secret that was committed and later removed is still exposed, it's in the history and reachable by anyone with clone access.
- Check if there's evidence it's already been rotated or invalidated.
- Check the scope and privilege of the credential, a scoped-down sandbox key is a different risk than a production admin credential.

### IaC

- Check the actual applied configuration, not just the flagged template. Look for overrides, environment-specific parameters, or module defaults that change the effective config.
- Assess blast radius: is the resource internet-facing, does it hold sensitive data, is this prod or non-prod.

### DAST

- Trace the flagged endpoint or route back to its handler in the repo.
- Cap your confidence lower than you would for an equivalent SAST finding. You don't have runtime visibility, no live traffic, no way to confirm what a WAF or gateway might already be blocking. Say this explicitly in the output rather than letting the reader assume this verdict carries the same certainty as a SAST one.
- Once you've located the handler, apply the same evidentiary standard as SAST: trace the input, check for sanitization, check reachability.

## Step 4: Determine confidence

Use this five-level scale, don't default to High/Medium/Low, the extra granularity matters because "medium confidence" covers too wide a range to be useful on its own.

- **Very High**: full trace confirmed end to end, no gaps in the evidence.
- **High**: strong evidence, one minor unconfirmed detail that wouldn't change the verdict either way.
- **Medium**: solid evidence on the core question, but at least one real unconfirmed link, e.g. can't verify a runtime config or the presence of a compensating control.
- **Low**: evidence is thin or partially contradictory. The verdict is a reasoned best guess, not a confirmed finding.
- **Very Low**: evidence is largely absent or ambiguous. Give the best-guess verdict anyway, don't defer to "needs more context" as an escape hatch, but be clear this is a starting point for further investigation, not a conclusion.

## Step 5: Write the output

### Voice

Write like a senior AppSec engineer briefing a junior engineer on a finding they need to act on today. Direct, plain, no lecture.

- No em dashes.
- No preamble, no filler words, no flattery. Start at the verdict line.
- No closing summary or restatement of what you just said. End at Action.
- Active voice throughout.
- No vague evidence. Every claim in "Evidence" and "Justification" is backed by a file:line citation and, where one exists, the function or symbol name, or explicitly marked as unverified.
- Keep the sections doing different jobs. "Summary" is the plain-language headline, no citations, no code, no CWE/CVE numbers, written for someone who may only read that one line. "Evidence" states only what's factually at each location, no interpretation. "Justification" is where the reasoning happens, and every bullet in it has to point back at a specific line in "Evidence", not introduce a new unsupported claim.
- No hedge words (may, might, could potentially) unless the confidence level is genuinely Low or Very Low. If the evidence is solid, say so plainly.
- State the finding, the risk, and the required action explicitly. Don't imply them.
- Don't assume the reader knows why a pattern is dangerous, one clause is enough context, not a lecture on what SQL injection is.
- Don't over-explain concepts a working engineer already has, what a lockfile is, what CWE stands for.
- Do fully explain the specific reasoning that makes this instance a true or false positive. That reasoning is the actual value of this skill over just relaying the scanner's output.
- Contractions are fine. This should read like someone talking through their own reasoning, not filing a compliance report.

### Format

Use this template exactly. Omit optional lines when they don't apply, don't leave placeholder text. "Summary" always comes first, right after the verdict line, and is the one field written for a reader with no security background: no jargon, no CWE/CVE numbers, no code, no citations. Everything below it is for the reader who wants to verify the call themselves.

```
✅ TRUE POSITIVE | Confidence: [level]
[or ❌ FALSE POSITIVE | Confidence: [level]]
[or 🟡 NEEDS MORE CONTEXT | Confidence: [level]]

Summary: [2-3 plain-language sentences. What the tool flagged and, in
plain terms, why the verdict landed where it did. No jargon, no
citations, no code. A reader who stops here should still understand
the call.]

Evidence:
- `path/file.ext:line`, `functionOrSymbolName()`: [what's actually there, factual, no interpretation]
- `path/file.ext:line`, `functionOrSymbolName()`: [what's actually there]
- `path/file.ext:line`: [config value, lockfile entry, package version, git log entry, etc.]
[2-5 bullets, ordered the way the trace actually runs: source, then each hop, then the sink or the control that stops it]

Justification:
- [reasoning bullet, cites one or more lines from Evidence above by file:line]
- [reasoning bullet, cites Evidence above]
[2-4 bullets. This is where the "why" happens, no new facts, only bullets that connect Evidence to the verdict]

Severity: Critical (tool) → Medium (actual)     [only when tool severity and actual severity diverge]

Package Health: [SCA only; staleness, deprecated/EOL/abandoned status, direct vs transitive]

Secondary Note: [FP only, when applicable: a pattern that's currently not exploitable but is bad practice or one change away from being exploitable]

Suppression Justification: [FP only, 5 sentences max, plain language, ready to paste into a ticket or PR comment]

Action: [fix guidance for TP, or what would raise confidence for Needs More Context]
```

For batched same-root-cause findings, use one block, list every file:line instance as its own bullet under "Evidence" instead of a single citation.

If the run covered multiple findings, add one line after the last verdict block:

```
Ran /compact before the next review to keep this session's context clean.
```

### Ordering rule for FP + package health

When an SCA finding is a false positive on the specific CVE but the package itself is abandoned or deprecated, both facts ship. The headline verdict answers only "is this CVE exploitable here," it stays False Positive. Package Health is a separate, equally visible line, not folded into the verdict or softened because the CVE turned out to be a non-issue.
