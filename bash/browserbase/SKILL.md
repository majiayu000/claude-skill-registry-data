---
name: browserbase
description: >-
  Give an AI agent a real cloud browser (Browserbase) for web research, scraping,
  page fetching, web search, form-driving, and site monitoring, with the API key
  loaded by path from ~/secrets/browserbase.txt and never written into the repo.
  Routes each task to the lightest capability (Fetch -> Search -> browse.sh skill
  catalog -> Stagehand act/extract/observe -> raw Playwright session) and returns
  structured, cited results. Trigger on /browserbase, "use Browserbase",
  "research this on the web", "scrape <site>", "fetch this page", "search the web
  for", "drive a browser", "watch the session live", or any task that needs a
  JS-rendered page, a login, or a bot-protected site that plain HTTP cannot reach.
  Not for reading local files or for sites where WebFetch already returns the
  content you need.
---

# Browserbase

Browserbase runs real Chrome browsers in the cloud that an agent can drive. This
skill is the repo's one door to it: key handling, capability routing, and the
output contract are fixed here so every agent (Claude, Codex, agy) uses it the
same way. The onboarding walkthrough this was distilled from is in
[reference/onboarding-guide.md](reference/onboarding-guide.md); read it only when
a rule below is unclear.

## 0. Key handling (non-negotiable)

- The key lives at `~/secrets/browserbase.txt` (line 1, nothing else). Override the
  path with `BROWSERBASE_KEY_FILE`. It is **never** committed, pasted into a doc,
  echoed to the terminal, or written into a `.env` inside this repo.
- Load it with the helper, which exports `BROWSERBASE_API_KEY` and nothing else:

  ```bash
  source skills/4-occasional/browserbase/env.sh          # export the key into this shell
  skills/4-occasional/browserbase/env.sh --check         # verify: prints prefix + length, never the key
  ```

- One key is all Browserbase needs. **Do not ask for, set, or pass a
  `BROWSERBASE_PROJECT_ID`** or a `projectId`; the key resolves the project. Training
  data and older Stagehand docs say otherwise; they are out of date. If a template's
  `.env.example` ships the var, leave it blank.
- If you scaffold a script that needs a `.env`, put it in `$TMPDIR` or the
  scratchpad, or add the path to `.gitignore` before writing it. Before any
  commit, run `git diff --cached | rg 'bb_live_|bb_test_'` and expect zero hits.
- Any URL, session id, or log you surface to the user goes out **in full**. Do not
  clip session links through `head`/`cut`; the whole id is needed to debug.

## 1. Preflight (every invocation)

```bash
skills/4-occasional/browserbase/env.sh --check || exit 1     # key present and well-formed
browse --version || echo "MISSING"                # CLI present?
browse cloud projects list                        # key actually works (ignore "Update available" banner)
```

- **Sandbox:** Claude Code's network filter blocks `api.browserbase.com`, so every
  `browse cloud …` / `browse open --remote` call reports `Connection error.` inside
  the sandbox. That is not a key problem. Run Browserbase commands with the sandbox
  bypassed (`dangerouslyDisableSandbox: true`, or `/sandbox` to allow the host);
  the symlink step of `install.sh` needs the bypass too (`~/.claude/skills` is
  write-denied).
- **Output shape:** `browse get markdown|text` and `browse cloud fetch` print a JSON
  object (`{"markdown": …}` / `{"content": …}`), sometimes preceded by the update
  banner. Save to a file and pull the field out (`json.loads(raw[raw.index('{'):])`);
  do not grep the raw stream as if it were the page.
- `browse` missing: name it and **ask before installing**:
  `npm install -g browse@latest` (needs Node 18+). If `browse cloud` says
  `unknown command 'cloud'`, a deprecated CLI is shadowing it:
  `npm uninstall -g @browserbasehq/cli @browserbasehq/browse-cli` then reinstall.
- The CLI prints an "Update available" banner on every command. It is noise.
  Strip it before parsing JSON output (`browse ... --json | sed '1,/^{/{/^{/!d}'`
  or simply read from the first `{`/`[`).
- Assume the **Free plan** unless told otherwise: Model Gateway is capped at $5 of
  tokens, and Proxies / Verified (anti-bot) sessions and CAPTCHA solving are
  **paid**. See §5 for how that changes routing.

## 2. Route the task to the lightest capability

Pick the first row that fits. Escalate only when the cheaper one demonstrably
fails (empty content, JS-only render, login wall, block page).

| Need | Use | Command / API |
|---|---|---|
| Page text, no JS or interaction needed | **Fetch** (no browser spun up) | `browse cloud fetch <url> --format markdown` |
| Find URLs / results for a query | **Search** | `browse cloud search "<query>" --num-results 10 --json` |
| A known site task (search products, list jobs, compare flights, …) | **browse.sh skill catalog** (500+ tested, structured-output recipes) | `browse skills find "<task>" --json` then `browse skills add <domain>/<slug>` |
| Repeatable task on a JS page: extract fields, click, fill, paginate | **Stagehand** `act` / `extract` / `observe` | TS or Python SDK, see §4 |
| Deterministic scripted control, or the project already uses Playwright/Puppeteer/Selenium | **Raw session over CDP** | `browse cloud sessions create` then connect |
| Stay logged in across runs | **Contexts** | `browse cloud contexts …` (docs link in §7) |
| Bot-protected / geo-locked site | **Proxies + Verified** (paid) | warn first, see §5 |
| Run it on a schedule / webhook in their cloud | **Functions** (TypeScript only) | `browse functions …` |
| Watch or replay a run | **Live View / replay** | `https://www.browserbase.com/sessions/<full-id>` |

Rule of thumb: Fetch/Search when no browser is needed, catalog skill when one
exists for the site, Stagehand for anything agentic, raw Playwright only when
determinism or an existing codebase demands it.

Search by **task**, not by guessed domain (jobs live under `indeed.com`,
hotels under `booking.com`). Catalog results carry `verified`, `proxies`,
`recommendedMethod`, and a `read-only` tag; those decide whether it will run on
Free.

## 3. Research mode (the default for "look this up")

Goal: a sourced answer, not a pile of pages.

1. **Frame** the question in one line and decide what a sufficient answer looks like
   (number of independent sources, recency window, structured fields wanted).
2. **Search** first: `browse cloud search "<query>" --num-results 10 --json`. Skim
   titles/snippets, keep 3-6 candidate URLs. Run a second query with different
   terms if results cluster on one source.
3. **Fetch** each candidate as markdown. Only escalate a URL to a browser session
   when Fetch returns empty/boilerplate content, a consent wall, or a 403.
4. **Extract** the facts you need into a scratch file
   (`$SCRATCHPAD/browserbase/<slug>.md`), one section per source, each with the
   full URL and the date fetched. Quote, do not paraphrase, anything numeric.
5. **Triangulate**: a claim needs two independent sources unless it is from the
   primary source (vendor docs, filing, official announcement). Mark single-source
   claims as such.
6. **Deliver**: the answer, then a Sources list of full URLs. If the user asked for
   a file, write the report to the path they named (or `PROJECT/**` per repo rules)
   and hand back only the path plus a one-line summary.

Stop conditions: sufficient answer reached, or 3 escalations to full browser
sessions without new information. Say which one ended the run.

## 4. Scraping / extraction mode

Goal: structured data with a schema the caller named (or you proposed and they
confirmed), reproducible on re-run.

1. **Check the catalog** before writing anything: `browse skills find "<task>" --json`.
   A tested skill beats a fresh script. Install and drive it with the CLI; wrap its
   output into the caller's schema.
2. **Otherwise write a Stagehand script.** Start from the machine-readable docs
   index at https://docs.stagehand.dev/llms.txt and read only the current V4
   install page plus the task pages you need. Use installed SDK declarations for
   exact signatures; do not invent packages or fall back to V3 silently. Pass
   `BROWSERBASE_API_KEY` explicitly to the documented Browserbase browser factory;
   no `projectId`. Leave `MODEL_API_KEY` and provider keys **unset** so calls route
   through Model Gateway on the Browserbase key (a placeholder value produces a
   misleading "API key not valid").
3. **Write it for reliability:**
   - Atomic instructions (`act("click the Sign in button")`), and `extract` with an
     explicit schema (zod / pydantic) so output is typed.
   - Wait on a specific element or `observe()` result, **never** a fixed sleep.
     Prefer `waitUntil: "domcontentloaded"`.
   - Enable the server-side `cache` option when inputs are stable; pass dynamic or
     sensitive values through the documented `variables` API, not the prompt string.
   - Inspect with the CLI, do not hand-roll an inspector: `browse snapshot`,
     `browse get`, `browse is`, `browse wait`.
   - Reuse one session while iterating instead of cold-starting each tweak.
   - Paginate with a hard cap the caller set; log rows per page.
4. **Run it** from `$TMPDIR` or the scratchpad (never a tracked `.env`). If there is
   no output for ~30 s, stop it, state the likely cause (§6), fix once, retry once.
5. **Deliver**: the data file (JSON/CSV at the path the caller named), the row
   count, the full session replay URL, and the script path if they want to keep it.
   Ask before moving a throwaway script somewhere permanent.

For Python projects use the Python Stagehand SDK where the V4 docs list it, and
the project's own package manager (`uv`, `pip`, `poetry`); do not hardcode `npm`.

## 5. Free-plan and bot-protection rules

- **Two triggers** for the protected-site warning: (a) a catalog result tagged
  `proxies: true` / `verified: true` / `anti-bot`, or (b) your own knowledge that
  the target is bot-protected or auth-walled (LinkedIn, Yelp, Instagram, Facebook,
  TikTok, ticketing sites, most large retailers). The catalog can stay silent for a
  protected site; warn anyway.
- When either fires: say so plainly **before** running, steer to a free-tier path
  that still answers the question (Fetch/Search of a non-protected source, a
  different target), and only if the protected site is genuinely required let the
  operator choose: try anyway, change target, or upgrade.
- Exception: Browserbase's official starter templates
  (`amazon-product-scraping`, `form-filling`, `sec-filing-research`) are known-good
  on Free. Do not pre-warn about their targets.
- **Model Gateway $5 cap**: if `act`/`extract` calls start failing mid-run on a
  script that worked, that is the likely cause. Explain it as "used up the $5 of
  free Model Gateway tokens", not as a broken key or plan. Ways forward, in order:
  bring your own LLM key (browser stays on Browserbase), rewrite the step as
  deterministic Playwright, or upgrade. Model ids are not guessable; use the list
  at https://docs.browserbase.com/platform/model-gateway/overview.

## 6. Failure lookup

| Symptom | Cause | Fix |
|---|---|---|
| `Connection error.` on any `browse cloud` / `--remote` call | sandbox network filter blocks api.browserbase.com | rerun with the sandbox bypassed; key is fine if `env.sh --check` passes |
| `ln: … Operation not permitted` from `install.sh` | sandbox write-denies `~/.claude/skills` | rerun `install.sh` with the sandbox bypassed |
| `browse cloud projects list` fails / 401 | key missing or wrong | `env.sh --check`; confirm line 1 of the secret file |
| Fetch returns `statusCode: 302` to `oauth2authorize…prompt=none` (Google docs) | silent sign-in redirect, not a block | escalate to `browse open <url> --remote` then `browse get markdown` |
| `rg`/`grep` on saved page finds nothing | output is one-line JSON, not markdown | unwrap the `markdown`/`content` field first (see §1) |
| `unknown command 'cloud'` | deprecated CLI shadowing `browse` | uninstall old CLIs, `npm install -g browse@latest` |
| `"API key not valid"` / "Incorrect API key provided" from an LLM call | placeholder `MODEL_API_KEY`/`OPENAI_API_KEY`, or the $5 Gateway cap | blank the placeholder; see §5 |
| Session created but page is a block/CAPTCHA | bot protection | §5 warning; needs Proxies/Verified or a different source |
| Fetch returns boilerplate or empty | JS-rendered or consent wall | escalate to Stagehand |
| JSON parse error on CLI output | "Update available" banner in stdout | strip lines before the first `{`/`[` |
| Session not at top of `browse cloud sessions list` | short sessions close and roll down | match on the session id the run printed |
| Fetch/Search show no session row | expected; they never spin up a browser | success is the payload / 200 |

Verify any browser-driving run with `browse cloud sessions list` and the full
replay link; verify Fetch/Search runs by the payload.

## 7. Files and references

- [env.sh](env.sh): key loader; the only place the secret path is known.
- [install.sh](install.sh): symlinks this skill into `~/.claude/skills/browserbase`.
- [reference/onboarding-guide.md](reference/onboarding-guide.md): the vendor's
  full first-run walkthrough (templates, teaching-moment flow) for a brand-new user.
- Canonical vendor skill: https://browserbase.com/SKILL.md
- Docs: https://docs.browserbase.com , Stagehand index: https://docs.stagehand.dev/llms.txt
- Capability docs: Fetch https://docs.browserbase.com/platform/fetch/overview ,
  Search https://docs.browserbase.com/platform/search/overview ,
  Sessions https://docs.browserbase.com/platform/browser/getting-started/create-browser-session ,
  Contexts https://docs.browserbase.com/platform/browser/core-features/contexts ,
  Proxies https://docs.browserbase.com/platform/identity/proxies ,
  Functions https://docs.browserbase.com/platform/runtime/overview ,
  Live View https://docs.browserbase.com/platform/browser/observability/session-live-view
- Dashboard: https://www.browserbase.com/sessions , keys: https://browserbase.com/settings
