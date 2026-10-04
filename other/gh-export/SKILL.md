---
name: gh-export
description: Formats all confirmed pentest findings from findings.json into copy-pasteable GitHub issue markdown blocks, following the AppSec reporting guide template.
argument-hint: [optional: path to findings.json]
user-invocable: true
---

# GitHub Issue Export

## Purpose

Read `findings.json` from the current pentest session and produce one copy-pasteable GitHub issue markdown block per confirmed finding.

Each block follows the AppSec reporting guide format — concrete impact, reproducible steps, raw PoC — so developers can act immediately without back-and-forth.

## Workflow

1. Read `findings.json` from the repo root (or the path provided in `$ARGUMENTS` if given)
2. For each entry in `findings[].findings` (skip diagram entries):
   - Format it using the template below
   - Check `pocs/` for any `.http` file whose name contains a keyword from the finding title — if found, read it and paste the content into the PoC block
   - After formatting the block, call `http(action="request", ...)` with method `PATCH`, url `http://localhost:7777/api/findings/{finding.id}`, body `{"gh_issue": "<the formatted markdown block>"}`, and headers `{"Content-Type": "application/json"}` — this couples the block to the finding in the dashboard
3. Write all formatted blocks to `gh-issues.md` in the repo root, separated by `---`, with a header line `# GitHub Issues — <target> — <date>` at the top. Create or overwrite the file.
4. Print all blocks consecutively with a `---` separator between them
5. After the last block, print a one-line summary: `X issue(s) ready to file — saved to gh-issues.md and copied above.`

## Output Template

For every finding, output exactly this structure (omit `## Browsers Verified In` for non-browser/non-web findings):

~~~markdown
**Summary:** <one sentence: what the vulnerability is and which component/endpoint is affected>

**Impact:** <what an attacker can concretely do — name the data exposed, the privilege gained, or the service disrupted. Never write "could lead to" — write "allows an attacker to". One short paragraph.>

**Severity Level:** <Critical | High | Medium | Low>

## Steps To Reproduce:

1. <exact first step — full URL, parameter name, payload>
2. <exact second step>
3. <what to observe in the response that confirms the issue>

## PoC

```
<paste the raw curl command, HTTP request from pocs/*.http, or tool output excerpt that proves exploitability>
```

## Supporting Material/References:

* <CVE ID if applicable, otherwise omit this line>
* Affected target: <target URL or file path from the finding>
* Tool: <tool_used value from the finding>
* <any additional evidence: key excerpt from raw tool output>

## Remediation

<if the finding has a `remediation` field, include this section — otherwise omit it entirely>

**Effort:** <effort level> | **Breaking change:** <Yes/No>

```diff
<paste the diff from remediation.diff, or show before/after from remediation.before and remediation.after>
```

**File:** <remediation.file>:<remediation.line>

**Verification:** <remediation.verification — how to confirm the fix worked>

**References:**
* <each URL from remediation.references>
~~~

## Rules

- **One block per finding** — never merge two findings into one issue
- **Impact must be concrete** — derive it from the finding's `description` and `evidence` fields; never invent hypothetical consequences
- **Steps to Reproduce must be self-contained** — if the finding has a `reproduction` field, use its `command` as the primary reproduction step. Otherwise include full URLs and exact payloads so a developer can reproduce without asking questions
- **PoC block is mandatory** — if a matching `.http` file exists in `pocs/`, paste its full content; if the finding has `reproduction.command`, include that; otherwise extract the most relevant raw evidence line from the `evidence` field
- **Remediation section** — if the finding has a `remediation` field, include the ## Remediation section with the diff, effort level, verification step, and references. If no remediation exists, omit the section entirely
- **Severity mapping**: critical → `Critical`, high → `High`, medium → `Medium`, low → `Low`
- Output only the markdown blocks and the final summary line — no extra prose, no headers, no explanation around the blocks
