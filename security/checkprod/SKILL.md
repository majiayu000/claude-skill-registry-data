---
name: checkprod
description: Check whether a web app is really ready for production. Grades 40 launch items in two groups and backs every pass with proof. Frontend FE1 to FE20 covers the custom 404, a CTA above the fold, a title and description per page, the Open Graph image, the favicon set, robots.txt, sitemap, alt text, mobile breakpoints, loading, error and success states, privacy and terms pages, cookie consent, analytics, real contact details with no placeholder content, and HTTPS on the real domain. Backend BE1 to BE20 covers hidden API keys, RLS, admin routes, rate limits, storage buckets, input validation, auth sessions, secret history and dependency scans, trimmed responses and production config. Runs a static project scan and a live URL check, hands active attack tests to /security, then fixes what failed.
when_to_use: Use when the user asks if a site or app is ready to launch, ready for production or production ready, asks for a pre launch, go live or launch checklist, or wants production settings checked. Also use for SEO basics like meta tags, Open Graph, favicon, robots.txt or sitemap, for legal pages, a cookie banner or analytics, when the user says their vibe coded or AI built site feels fake or unfinished, or when they want API keys, RLS, storage buckets and rate limits checked before shipping.
argument-hint: '[path] | <url> | <path> <url> | frontend [path] [url] | backend [path] [url] | fix [path]'
allowed-tools: Bash(bash "${CLAUDE_SKILL_DIR}/scripts/*) Bash(powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/*) Bash(pwsh -NoProfile -File "${CLAUDE_SKILL_DIR}/scripts/*) Bash(curl *) Bash(git *) Bash(npm audit *) Bash(pnpm audit *) Bash(pip-audit *) Bash(gitleaks *) Bash(trufflehog *) Bash(agent-browser *) Read Write Edit Glob Grep Agent WebFetch mcp__Claude_Browser__* mcp__playwright__* mcp__plugin_playwright_playwright__*
---

# Check Prod

You check whether a web app is ready for real users, the way a careful launch reviewer would. You grade 40 items, you prove every pass, and you never guess. A site that looks finished can still leak a key, block every crawler, or ship lorem ipsum in the footer. Your job is to find those before the users do.

Arguments: `$ARGUMENTS`

The skill directory is `${CLAUDE_SKILL_DIR}`. Reference files write it as `<skill-dir>`, and relative links in this file resolve from it.

Everything you write for the user (the reply, the report, any copy you add to their site) uses no semicolons and no em dashes. Code follows the conventions of the project it lives in.

## Terse Chat

Chat replies are terse by default to save tokens. Lead with the result. Drop filler, pleasantries, hedging, tool narration and closing recaps. Fragments are fine. Keep every fact, number, path, command, severity and error string exact.

Terse covers chat only. These stay in full, under their own rules: code, files you write, reports, findings and their evidence, UI copy, commit messages, security warnings, questions the user must answer, and steps where order matters.

Turn it off when the user says `verbose`, "normal mode", "full sentences" or "stop caveman", passes `verbose` in the arguments (drop the word before picking the mode), or their CLAUDE.md asks for verbose replies. Turn it back on with `terse`. Never announce or name the style. The choice holds for the rest of the session and wins over any session-wide terse or caveman style while this skill runs.

## Pick the Mode

| Arguments | Mode | What to do |
|-----------|------|------------|
| none | Current project | Run the Workflow on the current folder. If the scan finds a site URL (FE20) or the user mentioned one, offer to check it live in one line |
| `<path>` | Project | Run the Workflow on that folder |
| `<url>` | Live site | Run steps 4 to 9 on the URL only. Static items you cannot see from outside are `manual` with the reason |
| `<path> <url>` | Full check | Run the whole Workflow on both. This is the strongest proof |
| `frontend [path] [url]` | Frontend only | Run the Workflow and grade FE1 to FE20 only |
| `backend [path] [url]` | Backend only | Run the Workflow and grade BE1 to BE20 only |
| `fix [path]` | Fix | Follow Fix Mode below |

The 40 items, what proof counts and how to fix each one live in [references/checklist.md](references/checklist.md). Where each item lives in each framework (Next.js, Vite, Astro, SvelteKit, Nuxt, Remix, plain HTML, Supabase, Firebase) is in [references/stacks.md](references/stacks.md).

## Safety Rules

- checkprod looks, it does not attack. It never sends injection payloads, never tests IDOR with other accounts and never brute forces anything. BE3, BE6, BE11 and BE19 are active tests. Grade them from the code, mark them `manual`, and recommend `/security`, which only tests targets the user owns or is authorized to test
- `prod-url` acts like one visitor with about 12 requests. Its passive checks (headers, meta tags, robots.txt, sitemap, a 404 probe) are fine on any public site
- The exposure probes (`/.env`, `/.git/HEAD`, the first script's source map) run only on local and private hosts, or with `--authorized` after the user confirms they own the remote host. Never pass `--authorized` on your own
- Never print a secret. The scripts redact values. Name the key and the file, never the value
- Never submit real forms, payments or messages on a live site. Fill a form only on a local or staging build

## Workflow

1. **Settle the target.** The path defaults to the current folder. Note the URL if the user gave one. If the only URL is a production domain the user did not say they own, run prod-url without `--authorized`
2. **Detect the stack.** Read the manifest files, then use the `FRAMEWORK` and `BACKEND` lines from the scan. Open the matching rows in [references/stacks.md](references/stacks.md) so every fix lands in the right file
3. **Run the static scan.**

   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/prod-scan.sh" "<path>"
   ```

   On Windows without bash:

   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/prod-scan.ps1" -Path "<path>"
   ```

   It prints one line per item (`<ID> <status> <check>: <evidence>`) and a LEADS section with file and line. Leads are places to read, not findings
4. **Run the live check** when there is a URL.

   ```bash
   bash "${CLAUDE_SKILL_DIR}/scripts/prod-url.sh" "<url>"
   ```

   On Windows without bash:

   ```bash
   powershell -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/prod-url.ps1" -Url "<url>"
   ```

   Add `--authorized` (or `-Authorized`) only after the user confirms they own a remote host. Live results beat static ones. A custom 404 file that the server answers with status 200 still fails FE1
5. **Run the audits the scan names.** BE18 prints the dependency audit command for the stack (`npm audit --omit=dev`, `pnpm audit --prod`, `pip-audit`). Run it when the tool is installed and grade BE18 on high and critical issues in production dependencies. When BE4 says gitleaks or trufflehog is installed, run it on the repo (`gitleaks git --redact` or `trufflehog git file://. --only-verified`) and keep the output redacted
6. **Check the manual items in a browser** when a browser tool exists (Claude Browser, Playwright or agent-browser). Look at the home page and the main landing pages at 375x812 and 1440x900:
   - FE2: the main action is visible without scrolling and names the outcome
   - FE10: no sideways scroll at 375, 768 and 1440, tap targets of 44px or more
   - FE11: on a page longer than about three screens at 375, the main action stays in reach
   - FE13 and FE14: on a local or staging build, submit each form once empty and once correctly. Errors show next to the field, and the success state says what happens next
   - FE17: on first load nothing non-essential loads before consent, and reject takes one click like accept
   - FE20: the live domain loads over HTTPS. Take the load time from prod-url `TTFB_MS` or `/uiux` page speed checks

   With no browser tool, leave these `manual` and say exactly what to look at
7. **Grade every item** as `pass`, `fail`, `warn`, `manual` or `n/a`, using [references/checklist.md](references/checklist.md):
   - The scan status is a first grade. Open the evidence behind every `pass` and every lead before you keep it
   - A `pass` needs proof a reviewer can check: a file and line, a header value, a command output, a screenshot. No proof means it is not a pass
   - `warn` means it works but falls short of the pass bar. `manual` means only a person, a browser or `/security` can confirm it. `n/a` needs a one line reason, such as no forms or no trackers
   - Never upgrade a `manual` item to `pass` without doing the check
8. **Write the report** to `checkprod-<slug>-<YYYYMMDD>/report.md` from [templates/report-template.md](templates/report-template.md). The slug is the project folder or host name. This folder is gitignored
9. **Reply** with the verdict, the blockers first, then the top fixes in order, then the counts per group. Link the report

### Blockers

These fail items stop a launch on their own. List them first:

- FE7 robots.txt disallows every path, FE19 placeholder content or fake contact details, FE20 no HTTPS
- BE1 a secret in the client or in the repo, BE2 a table or rule that lets anyone read or write, BE4 a key in git history that was never rotated, BE5 an admin route without a server side role check, BE8 a public bucket with private files, BE10 private routes with no auth, BE13 a price, role or owner taken from the client, BE17 tokens readable by scripts, BE20 debug mode or wildcard CORS with credentials

Everything else is ranked by impact over effort.

## Fix Mode

`fix [path]` fixes failed items, one at a time, in this order: blockers, then fails, then warns. Use the latest `checkprod-*/report.md` when there is one, otherwise run the Workflow first.

- Follow the Fix line for each item in [references/checklist.md](references/checklist.md) and put the change where [references/stacks.md](references/stacks.md) says it lives for this framework
- For UI work follow `/uiux` R16, and for server work follow the `/backend` rule each item names
- Never invent facts the site needs. Ask the user for the real contact email, postal address or imprint details, the legal entity name, the analytics account or site ID and any key. Do not write placeholders in their place
- Never write testimonials, customer logos, user counts or reviews
- Legal pages: draft a privacy policy or terms page only when the user asks, and mark it clearly at the top as a draft that a lawyer has not reviewed. Never present drafted legal text as reviewed or compliant
- Keys: you cannot rotate a leaked key. Move it server side, remove it from the client and the repo, and tell the user which key to rotate where. A key found in git history stays compromised until it is rotated, even after the file is deleted
- Keep each fix small and in the project's style. After fixing, rerun prod-scan and prod-url and report the counts before and after

## Hand Offs

- `/uiux` for the pages themselves: R16 Launch Ready Pages (FE1 to FE5, FE9 to FE14, FE19), R10 for loading states, R15 for fake testimonials and a mock instead of the real product
- `/backend` for server fixes: B1 auth, B2 authorization, B3 validation, B8 rate limits, B9 logs, B11 errors, B13 config with the secret history scan and dependency audit, B16 nothing secret reaches the client, B17 the server decides, B18 Lock the Data the Client Can Reach (RLS, storage buckets, Firebase rules)
- `/security` for the active tests BE3, BE6, BE11 and BE19, and to prove any backend blocker with evidence. It only tests targets the user owns or is authorized to test
