---
name: dataforseo-ai-tracker
description: Track brand mentions and citations in ChatGPT, Gemini, Google AI Overviews and AI Mode, Copilot, Claude and Perplexity at scale through the DataForSEO API, with a cost estimate and spending cap before every run. Use for "track our AI visibility with DataForSEO", "LLM rank tracking" or AEO, LLM SEO and GEO reports.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/dataforseo-ai-tracker
---

# Track AI answers at scale with DataForSEO

Run a fixed prompt set through the DataForSEO API, three samples per prompt per engine, inside a spending cap the user has approved, and turn the raw answers into mention rate, citation rate, first-mention position, share of voice against named competitors, and the domains each engine cites. You hand back the cost estimate before anything is spent, then the raw JSON, three CSVs and a short report that stays comparable month to month.

> **Romeo's rule:** Show the bill before you start the meter, and never report one answer as a result: the engines reshuffle their recommendations nearly every time you ask.

## Use this when

- The hand-run baseline from `ai-search-visibility` works and you now want 50 to 500 prompts tracked monthly without copying answers into a spreadsheet.
- A client or board report needs AI visibility numbers with sample sizes, across several engines, before and after a piece of work.
- You want share of voice against named competitors, or the list of domains each engine cites for the category.
- You want a ChatGPT or AI Overviews trend from DataForSEO's pre-collected database, with no sampling of your own (LLM Mentions).

## Don't use this for

- Choosing and wording the prompts to track → `ai-prompt-research`.
- Deciding what to fix from the results, or tracking by hand without an API account → `ai-search-visibility`.
- AI referral traffic, signups and revenue → `ai-traffic-analytics`.
- Google's own AI Overview and AI Mode impression data from Search Console → `google-ai-overviews-audit`.

## What you need

### Required

- A DataForSEO account. Pay as you go: $1 trial credit at sign-up, $50 minimum top-up, and funds don't expire. The API login and API password are at app.dataforseo.com/api-access; the API password is not the account password.
- Those two values in the environment variables `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD`, set by the user in their own shell, secrets manager or CI secrets. The agent never asks for them in chat and never writes them into a file, command, URL, log or report.
- A prompt file, built with `ai-prompt-research`. Either `prompts.txt` (one prompt per line; blank lines and lines starting with `#` are skipped) or that skill's CSV (header `id,prompt,type,intent,stage,segment,priority,money_prompt,...`): the script reads `prompt`, keeps `id` and `type`, and `--money-only` keeps only rows where `money_prompt` is true. 500 characters at most per prompt.
- A brands file: one brand per line, yours first, then 2 to 9 competitors, as `Name | aliases | domains`, e.g. `Acme | Acme, Acme Payroll | acme.com`. Aliases (comma-separated, defaulting to the name) are what counts as a mention, matched as case-sensitive whole words; domains only count citations.
- Market (DataForSEO `location_code` and `language_code`, e.g. `2840` and `en` for the US), the engines to track, a spending cap (default $2 per run) and, for Claude or Perplexity, a model picked from DataForSEO's free models list.

### Helpful

- Python 3.8 or newer for the script below, or an MCP-capable agent for the official MCP server.
- A recent hand-run baseline, to check that the API numbers resemble what people see in the apps.
- Wrong facts about the brand already known, so you can watch for them in the raw answers.

### No tools?

No account, no budget, or no way to set environment variables: use the manual method in `ai-search-visibility` (15 or more prompts on the 3 engines the audience uses, each run at least twice in clean sessions, logged in a spreadsheet). The script's `estimate` command needs no account and no network, so you can price a tracked run before deciding. Search Console's generative AI performance report and Bing Webmaster Tools' AI Performance report are free and cover Google's and Microsoft's side.

## Ground rules

- No paid call without a cost estimate and an explicit yes from the user for that amount. Default cap $2 per run. Any change to prompts, engines, samples, models or market needs a new estimate. Claude and Perplexity model charges vary call by call, so the cap is enforced between calls: the script stops before any call that could pass it, and if one unusually expensive call overshoots, it says so.
- Credentials only through environment variables. If the user pastes them into chat, tell them to change the API password (it now sits in a transcript) and set the variables in their own shell.
- Prompts are sent to DataForSEO and, depending on the endpoint, other AI providers. Generalise prompts derived from private records locally and remove personal identifiers and confidential facts. Tell the user the destination and obtain permission before sending any remaining private information.
- Sandbox first. New or edited code runs against `https://sandbox.dataforseo.com` (free, dummy data in the real response shape, same login) before it touches the paid API.
- Three samples per prompt per engine by default. Two answers rarely list the same recommendations (SparkToro and Gumshoe, early 2026: under a 1% chance that two runs return the same list), so report rates with sample sizes.
- Know what each endpoint measures. LLM Scraper returns ChatGPT and Gemini as users see them; LLM Responses sends the prompt through the model's API, which can answer differently from the app; the Bing results-page answer is not the Copilot app. Label every number with its endpoint.
- Standard queue for batches (`task_post`, up to 100 tasks per POST, about a third of the Live price for LLM Scraper); Live only when the user is waiting.
- Cache and never pay twice: SERPs for 7 days, LLM Mentions and AI search volume for 30 days, sampled answers per run date.
- Keep price traps off unless asked: `depth` above 10, search operators (5× price), `calculate_rectangles` (2×), clickstream data, `max_output_tokens` above 2,048, and LLM Mentions calls without an explicit `limit` (rows are billed).
- Pre-collected database numbers (LLM Mentions) and your own sampled prompts answer different questions. Report them side by side, never added together.

## Steps

1. **Set up the account safely.**
   - Sign up, keep the $1 trial credit for a first small paid test, and top up only once the user has approved the plan.
   - The user runs `export DATAFORSEO_LOGIN=...` and `export DATAFORSEO_PASSWORD=...` in their own terminal. Check they're set without revealing them: `python3 -c "import os; print(all(os.environ.get(k) for k in ('DATAFORSEO_LOGIN', 'DATAFORSEO_PASSWORD')))"`.
   - Free balance and price check: `GET /v3/appendix/user_data`. Read `tasks[0].result[0].money.balance`, any spending limits in `money.limits`, and current prices under `price`. If they differ from the script's rate table, edit the table before estimating.
   - MCP alternative: DataForSEO's [official server](https://github.com/dataforseo/mcp-server-typescript) offers `https://mcp.dataforseo.com/v3/mcp` with OAuth. Its tools include `docs_search` and `api_request`; call any endpoint below through `api_request` with its path and body. If a local server is needed, review the official source and pin an exact reviewed package version before running it or providing credentials; do not run `@latest` with secrets. Same rules: estimate, approval, cap, three samples.
2. **Prepare the inputs.**
   - Brand names that are common words ("Notion", "Apple", "Monday") cause false mentions. Case-sensitive matching skips "a notion" but not "on Monday", so leave the bare word out of the aliases and list distinctive forms (`Monday | monday.com, Monday CRM | monday.com`). Hand-check those rows anyway.
   - Keep the prompt set fixed between runs. Add new prompts as a new group so the trend stays comparable.
3. **Pick engines and endpoints.** Script engine names in brackets.
   - ChatGPT as users see it (`chatgpt`): `/v3/ai_optimization/chat_gpt/llm_scraper/live/advanced` with `keyword`, `location_code`, `language_code`. Read `markdown`, `sources[]` (what the answer cited), `search_results[]` (everything retrieved, cited or not) and `brand_entities[]`. $0.004 Live, $0.0012 Standard (about 45 minutes).
   - Gemini as users see it (`gemini`): `/v3/ai_optimization/gemini/llm_scraper/live/advanced`, same body; `markdown` and `sources[]`. Same prices.
   - Google AI Overviews (`aio`): `/v3/serp/google/organic/live/advanced` with `load_async_ai_overview: true` (without it you only get cached AI Overviews; it adds $0.002, refunded when none loads) and `depth: 10`. Read the `ai_overview` item and its `ai_overview_reference` entries. No `ai_overview` item means no AI answer, not "not mentioned".
   - Google AI Mode (`ai_mode`): `/v3/serp/google/ai_mode/live/advanced`; `ai_overview` item with `markdown` and references. $0.004 Live, $0.0012 Standard; only in markets where Google offers AI Mode.
   - Copilot, approximately (`copilot`): `/v3/serp/bing/organic/live/advanced`; an `ai_overview` item appears when Bing showed an AI answer on the results page. Confirm the Bing price in `user_data`; the script assumes up to $0.004.
   - Claude (`claude`): `/v3/ai_optimization/claude/llm_responses/live` with `user_prompt`, `model_name` (required: pick from the free `.../claude/llm_responses/models` list, preferring the cheapest Haiku-class model on that list for tracking) and `web_search: true`. Read `items[].sections[].text` and `annotations[]` (can be empty even with search on). Cost is $0.0006 plus `money_spent`, the provider's token and search charge, which varies by call: DataForSEO's docs example is $0.55 for one Opus call with web search.
   - Perplexity (`perplexity`): `/v3/ai_optimization/perplexity/llm_responses/live` (Live only), `model_name` required: `sonar` is the cheap choice and searches by default; avoid deep-research models for tracking.
   - ChatGPT through its API also exists (`chat_gpt/llm_responses`); prefer the scraper for "what users see".
4. **Add database share of voice if useful (LLM Mentions).** Pre-collected answers, no sampling, Live only, $0.10 per task plus $0.001 per row returned.
   - Coverage: Google AI Overviews (`platform: "google"`) and ChatGPT (`"chat_gpt"`, US English only: `location_code` 2840, `language_code` `en`); monthly history from August 2025. Its prompts are DataForSEO's, not yours.
   - Share of voice: `/v3/ai_optimization/llm_mentions/multi_target_metrics/live` with 2 to 10 `targets`, each `{"key": "acme", "target": [{"keyword": "acme", "search_scope": ["answer"]}, {"domain": "acme.com", "search_scope": ["sources"]}]}`. Groups can overlap, so totals are not shares: compute each brand's share of the group sum and say so.
   - Cited domains: `.../llm_mentions/top_mentioned_domains/live`. Real questions and answers: `.../llm_mentions/search_mentions/live` with an explicit `limit` (max 1,000).
   - A share-of-voice pack (multi-target metrics, historical and top domains) costs about $0.90.
5. **Estimate and get a yes.** Run `estimate` (below): no network, no credentials. Show the user the calls per engine, the Live range, the Standard-queue range, and the uncertainty in Claude and Perplexity model charges. Ask: "This run makes [N] calls and costs between $[low] and $[high], capped at $[cap]. Go ahead?" Wait for a clear yes.
   - Example: 30 prompts × 3 samples on ChatGPT, Gemini, AI Overviews and AI Mode = 360 calls, $1.26 to $1.44 Live. Adding Claude and Perplexity shows a worst case of about $64, because the rate table sizes their calls for the dearest models ($0.60 and $0.10). Cheaper models should cost far less: run 5 prompts first and read `money_spent` before approving a large run.
6. **Save the script.** Save the block below as `ai_tracker.py` (standard library only, Python 3.8+). It sits outside the list on purpose, so it copies without stray indentation.

```python
"""AI answer tracker on the DataForSEO API. Standard library only, Python 3.8+.
  estimate PROMPTS [--engines chatgpt,gemini,aio,ai_mode] [--samples 3] [--money-only]        offline: no network, no credentials
  run PROMPTS BRANDS [same options] [--max-usd 2] [--max-calls 500] [--sandbox] [--out DIR] [--date YYYY-MM-DD]
  score PROMPTS BRANDS [same options as the run]                       re-score saved answers: no calls, no credentials
PROMPTS: .txt, one prompt per line, or the ai-prompt-research CSV. BRANDS: "Name | alias, alias | domain, domain", yours first.
claude and perplexity need --claude-model / --perplexity-model (free list: GET /v3/ai_optimization/<llm>/llm_responses/models).
Credentials come only from env DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD; they are never printed or saved."""
import argparse, base64, csv, datetime, hashlib, json, os, re, sys, urllib.error, urllib.parse, urllib.request
# engine: (endpoint, USD per Live call (low, worst case), USD per Standard-queue call or None). Nov 2026 published prices: check
# GET /v3/appendix/user_data. LLM Responses add a variable model charge, so their worst cases are estimates sized for the
# dearest models (the docs' example Claude call cost $0.55); a dearer call seen during a run raises that engine's worst case.
RATES = {
    "chatgpt": ("ai_optimization/chat_gpt/llm_scraper/live/advanced", (0.004, 0.004), (0.0012, 0.0012)),
    "gemini": ("ai_optimization/gemini/llm_scraper/live/advanced", (0.004, 0.004), (0.0012, 0.0012)),
    "aio": ("serp/google/organic/live/advanced", (0.002, 0.004), (0.0006, 0.0026)),  # +$0.002 when an async AIO loads
    "ai_mode": ("serp/google/ai_mode/live/advanced", (0.004, 0.004), (0.0012, 0.0012)),
    "copilot": ("serp/bing/organic/live/advanced", (0.002, 0.004), (0.0006, 0.002)),  # Bing results-page AI answer
    "claude": ("ai_optimization/claude/llm_responses/live", (0.005, 0.60), (0.0046, 0.60)),
    "perplexity": ("ai_optimization/perplexity/llm_responses/live", (0.003, 0.10), None)}
LLMR = ("claude", "perplexity")
host = lambda url: re.sub(r"^www\.", "", (urllib.parse.urlsplit(url).hostname or "").lower())
def load_prompts(path, money_only=False):  # .txt: one prompt per line; .csv: ai-prompt-research export ("prompt" column)
    with open(path, encoding="utf-8-sig", newline="") as f:
        if path.lower().endswith(".csv"):
            rows = [{k.strip().lower(): (v or "").strip() for k, v in r.items() if k} for r in csv.DictReader(f)]
            rows = [r for r in rows if r.get("prompt") and (not money_only or r.get("money_prompt", "").lower() in ("true", "yes", "y", "1"))]
            out = [(r.get("id") or str(n + 1), r.get("type") or r.get("group", ""), r["prompt"]) for n, r in enumerate(rows)]
        else: out = [(str(n + 1), "", l) for n, l in enumerate(l.strip() for l in f if l.strip() and not l.lstrip().startswith("#"))]
    return out if out and max(len(p) for _, _, p in out) <= 500 else sys.exit("No prompts (check --money-only) or one over 500 chars: " + path)
def load_brands(path):  # "Name | alias, alias | domain, domain": aliases are case-sensitive whole words; domains only count citations
    out = []
    for line in open(path, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"): continue
        if "|" not in line and "," in line: sys.exit("Brands lines look like 'Acme | Acme, Acme Payroll | acme.com': %s" % line.strip())
        name, aliases, doms = [c.strip() for c in (line.split("|") + ["", ""])[:3]]
        names = [p.strip() for p in aliases.split(",") if p.strip()] or [name]
        out.append((name, re.compile(r"(?<!\w)(?:%s)(?!\w)" % "|".join(map(re.escape, names))),
                    [re.sub(r"^(https?://)?(www\.)?", "", d.strip().lower()).strip("/") for d in doms.split(",") if d.strip()]))
    return out if len(out) > 1 else sys.exit("The brands file needs your brand plus at least one competitor.")
engines = lambda s: s.replace(" ", "").split(",") if set(s.replace(" ", "").split(",")) <= set(RATES) else sys.exit("Engines: " + ", ".join(RATES))
def body(eng, prompt, a):  # request bodies as documented; one task per Live call
    loc = {"location_code": a.location_code, "language_code": a.language_code}
    if eng in ("chatgpt", "gemini", "ai_mode"): return [dict(keyword=prompt, **loc)]
    if eng in ("aio", "copilot"): return [dict(keyword=prompt, depth=10, **loc, **({"load_async_ai_overview": True} if eng == "aio" else {}))]
    task = dict(user_prompt=prompt, model_name=getattr(a, eng + "_model"), max_output_tokens=2048, web_search_country_iso_code=a.country)
    return [dict(task, web_search=True) if eng == "claude" else task]  # Perplexity's Sonar models search by default
def call(method, path, payload, api):
    token = base64.b64encode(("%s:%s" % (os.environ["DATAFORSEO_LOGIN"], os.environ["DATAFORSEO_PASSWORD"])).encode()).decode()
    req = urllib.request.Request(api + "/v3/" + path, data=None if payload is None else json.dumps(payload).encode(),
                                 method=method, headers={"Authorization": "Basic " + token, "Content-Type": "application/json"})
    try: resp = urllib.request.urlopen(req, timeout=180)
    except urllib.error.HTTPError as e: resp = e  # 401 and similar still carry a JSON status_message
    return json.loads(resp.read().decode("utf-8"))
def cost_of(data):  # largest reported figure: task cost = base price + money_spent (the model provider's charge)
    task = (data.get("tasks") or [{}])[0]; res = (task.get("result") or [{}])[0] or {}
    return max(float(data.get("cost") or 0), float(task.get("cost") or 0), float(res.get("money_spent") or 0))
def walk(o):  # every dict in a JSON tree
    if isinstance(o, dict): yield o; o = list(o.values())
    for v in o if isinstance(o, list) else []: yield from walk(v)
def extract(eng, res):  # -> (answer text, or None when no AI answer was shown or it was empty; cited URLs)
    text, urls = None, []
    if res and eng in ("aio", "ai_mode", "copilot"):
        box = next((i for i in res.get("items") or [] if i.get("type") == "ai_overview"), None)
        refs = [d for d in walk(box) if d.get("type") == "ai_overview_reference"]
        text = box and (box.get("markdown") or " ".join(d["text"] for d in walk(box) if d not in refs and isinstance(d.get("text"), str)))
        urls = [d["url"] for d in refs if d.get("url")]
    elif res and eng in LLMR:
        secs = [s for i in res.get("items") or [] if i.get("type") == "message" for s in i.get("sections") or []]
        text, urls = " ".join(s.get("text") or "" for s in secs), [n["url"] for s in secs for n in s.get("annotations") or [] if n.get("url")]
    elif res: text, urls = res.get("markdown"), [s["url"] for s in res.get("sources") or [] if s.get("url")]
    return (text if text and text.strip() else None), urls
def write(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, list(rows[0]) if rows else ["empty"]); w.writeheader(); w.writerows(rows)
def summarise(prompts, marks, jobs, out):
    rows, doms, summary = [], {}, []
    for eng, i, s, path in (j for j in jobs if os.path.exists(j[3])):
        text, urls = extract(eng, (json.load(open(path, encoding="utf-8"))["tasks"][0].get("result") or [None])[0])
        hosts = {host(u) for u in urls}
        for h in hosts: doms[(eng, h)] = doms.get((eng, h), 0) + 1
        first = {name: m.start() for name, pat, _ in marks for m in [pat.search(text or "")] if m}
        order = sorted(first, key=first.get)  # position = order of first mention among the tracked brands
        rows += [dict(engine=eng, prompt_id=prompts[i][0], group=prompts[i][1], prompt=prompts[i][2], sample=s, answered=int(text is not None),
                      brand=name, mentioned=int(name in first), position=order.index(name) + 1 if name in first else "",
                      cited=int(any(h == d or h.endswith("." + d) for h in hosts for d in ds))) for name, _, ds in marks]
    for eng in sorted({r["engine"] for r in rows}):
        er = [r for r in rows if r["engine"] == eng]; total = sum(r["mentioned"] for r in er) or 1
        for name, _, _ in marks:
            b = [r for r in er if r["brand"] == name]; answered, m = sum(r["answered"] for r in b), sum(r["mentioned"] for r in b)
            pos, n = [r["position"] for r in b if r["position"] != ""], max(answered, 1)
            summary.append(dict(engine=eng, brand=name, runs=len(b), answered=answered, mention_rate=round(m / n, 3),
                                citation_rate=round(sum(r["cited"] for r in b) / n, 3), named_first_rate=round(pos.count(1) / n, 3),
                                avg_position=round(sum(pos) / len(pos), 2) if pos else "", share_of_voice=round(m / total, 3)))
    write(os.path.join(out, "runs.csv"), rows); write(os.path.join(out, "summary.csv"), summary)
    write(os.path.join(out, "domains.csv"), [dict(engine=e, domain=d, runs_citing=c) for (e, d), c in sorted(doms.items(), key=lambda x: -x[1])])
    for r in summary: print("  ".join("%s=%s" % kv for kv in r.items()))
    print("Wrote runs.csv, summary.csv and domains.csv to %s" % out)
def estimate(a):
    engs, n = engines(a.engines), len(load_prompts(a.prompts, a.money_only)) * a.samples
    usd = lambda r: "$%.2f-%.2f" % (n * r[0], n * r[1]) if r else "n/a (Live only)"
    for e in engs: print("%-10s %5d calls  Live %s  Standard queue %s" % (e, n, usd(RATES[e][1]), usd(RATES[e][2])))
    print("All engines, Live: %s for %d calls. No network calls made." % (usd([sum(RATES[e][1][k] for e in engs) for k in (0, 1)]), n * len(engs)))
    if set(engs) & set(LLMR): print("Claude and Perplexity add variable model charges: the range is a guess, and the cap is enforced between calls.")
def run(a):
    prompts, marks, engs = load_prompts(a.prompts, a.money_only), load_brands(a.brands), engines(a.engines)
    no_model = [e for e in engs if e in LLMR and not getattr(a, e + "_model")]
    if no_model: sys.exit("Pick a model with --%s-model from the free GET /v3/ai_optimization/%s/llm_responses/models list." % (no_model[0], no_model[0]))
    api, date = "https://%s.dataforseo.com" % ("sandbox" if a.sandbox else "api"), a.date or str(datetime.date.today())
    out = a.out or "aitrack-%s%s" % ("sandbox-" if a.sandbox else "", date); os.makedirs(os.path.join(out, "raw"), exist_ok=True)
    key = lambda e, p: hashlib.sha1(repr((e, getattr(a, e + "_model", ""), p, a.location_code, a.language_code, a.country, date)).encode()).hexdigest()[:12]
    jobs = [(e, i, s, os.path.join(out, "raw", "%s-%s-s%d.json" % (e, key(e, p[2]), s)))
            for e in engs for i, p in enumerate(prompts) for s in range(1, a.samples + 1)]
    todo = [] if a.cmd == "score" else [j for j in jobs if not os.path.exists(j[3])]  # saved answers are never paid for twice
    low, worst = (sum(RATES[j[0]][1][k] for j in todo) for k in (0, 1))
    print("%d calls to make, %d saved. Estimate $%.2f-%.2f, cap %s" % (len(todo), sum(os.path.exists(j[3]) for j in jobs), low, worst,
          "none (sandbox is free)" if a.sandbox else "$%.2f" % a.max_usd))
    if len(todo) > a.max_calls: sys.exit("That is more than --max-calls %d. Raise it only if the user expects this many calls." % a.max_calls)
    if not a.sandbox and low > a.max_usd: sys.exit("Even the low estimate is over the cap: cut prompts, engines or samples, or get the user's OK for more.")
    if not a.sandbox and worst > a.max_usd: print("The worst case is over the cap, so the run may stop early. The cap is checked before every call.")
    if todo and not (os.environ.get("DATAFORSEO_LOGIN") and os.environ.get("DATAFORSEO_PASSWORD")):
        sys.exit("Set DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD in your own shell first.")
    if todo:
        try: user = call("GET", "appendix/user_data", None, api); balance = float(user["tasks"][0]["result"][0]["money"]["balance"])
        except (OSError, ValueError) as e: sys.exit("Balance check failed (%s). No calls were made." % type(e).__name__)
        except (KeyError, IndexError, TypeError): sys.exit("Balance check failed: %s. No calls were made." % user.get("status_message"))
        print("Balance $%.2f" % balance) if a.sandbox or balance >= min(worst, a.max_usd) else sys.exit("The balance is below what this run may spend.")
    spent, seen = 0.0, {}
    for eng, i, s, path in todo:
        risk = max(RATES[eng][1][1], seen.get(eng, 0))  # this engine's worst case, raised by any dearer call already seen
        if not a.sandbox and spent + risk > a.max_usd: print("Stopped before a call that could pass the cap."); break
        try: data = call("POST", RATES[eng][0], body(eng, prompts[i][2], a), api)
        except (OSError, ValueError) as e: print("Stopped on a network or parse error (%s)." % type(e).__name__); break
        c = 0.0 if a.sandbox else cost_of(data); spent += c; seen[eng] = max(seen.get(eng, 0), c); task = (data.get("tasks") or [{}])[0]
        if c > risk: print("Warning: a %s call cost $%.4f, above its $%.2f worst case. Spent $%.4f of the $%.2f cap." % (eng, c, risk, spent, a.max_usd))
        if data.get("status_code") != 20000 or task.get("status_code") != 20000:
            print("Stopped, API error (%s, prompt %s): %s" % (eng, prompts[i][0], task.get("status_message") or data.get("status_message"))); break
        with open(path, "w", encoding="utf-8") as f: json.dump(data, f)
    print("Spent this run: $%.4f%s" % (spent, " (sandbox, free)" if a.sandbox else " of the $%.2f cap" % a.max_usd)); summarise(prompts, marks, jobs, out)
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("estimate", "run", "score"):
        p = sub.add_parser(name); p.add_argument("prompts"); p.add_argument("--engines", default="chatgpt,gemini,aio,ai_mode")
        p.add_argument("--samples", type=int, default=3); p.add_argument("--money-only", action="store_true", help="CSV: money_prompt rows only")
        p.add_argument("--location-code", type=int, default=2840); p.add_argument("--language-code", default="en")
        p.add_argument("--country", default="US", help="web search country for Claude and Perplexity")
        p.add_argument("--claude-model"); p.add_argument("--perplexity-model")
        if name == "estimate": continue
        p.add_argument("brands"); p.add_argument("--out"); p.add_argument("--date", help="reuse a dated run's saved answers")
        p.add_argument("--max-usd", type=float, default=2.0); p.add_argument("--max-calls", type=int, default=500); p.add_argument("--sandbox", action="store_true")
    args = ap.parse_args(); estimate(args) if args.cmd == "estimate" else run(args)
```

   - Price check: `python3 ai_tracker.py estimate prompts.txt --engines chatgpt,gemini,aio,ai_mode --samples 3`.
   - Sandbox: `python3 ai_tracker.py run prompts.txt brands.txt --sandbox`. The money cap is off there (it's free); `--max-calls` (default 500) still applies.
   - Real run: `python3 ai_tracker.py run prompts.csv brands.txt --money-only --max-usd 2`. With Claude: `--engines chatgpt,claude --claude-model <cheapest Haiku model from the models list>`. Add `--location-code`, `--language-code` and `--country` for other markets.
   - What `run` does: refuses to start if even the low estimate is over `--max-usd`, and warns when the worst case is; checks the balance with `user_data` (a failed check stops with a message and no calls); makes one Live call at a time and adds up each response's actual `cost`, which includes `money_spent`; before every call, stops if spend plus that engine's worst case could pass the cap, raising the worst case to the dearest call seen so far; prints a warning if one call costs more than its worst case (the only way spend can end above the cap); stops at the first API or network error; saves each response to `raw/`; then writes `runs.csv` (one row per call and brand), `summary.csv` (rates per engine and brand) and `domains.csv` (cited domains per engine).
   - Cache: answers are keyed by engine, model, prompt, market, run date and sample, so a new model or market never reuses old answers. Re-running the same day pays nothing for what's saved; `score` re-scores a folder without calls after you fix aliases (add `--date` for an older run).
   - Limits: Live calls only (fine under a few hundred calls); mentions are case-sensitive text matches, so check common-word names by hand; an empty answer counts as no answer; "position" is order among your tracked brands, not among everything named; the rate table holds published prices from November 2026.
   - How it was tested (2 November 2026): `estimate` run with `python3 -I` on Python 3.9.6 and 3.14.4 with network sockets disabled; `run` and `score` tested offline against fixture responses built from DataForSEO's documented response shapes for all seven engines, checking request bodies, the auth header, that credentials never reach output, parsing (empty answers, case-sensitive aliases, names vs domains), the low-estimate refusal, the worst-case warning, mid-run cap stops when real costs beat the table (a $0.90 Claude call), cache reuse and fresh calls when the model or date changes, required model flags, a 401, a network error on the balance check, missing credentials, the CSV format with `--money-only`, and the sandbox host with no money cap but a call limit. Python 3.8 was checked for syntax only. It has not been run against the live API or the sandbox (the sandbox needs an account login), and no paid calls were made.
7. **Test on the sandbox.** Run with `--sandbox` first. It confirms the credentials, the request bodies and the parsing; the dummy answers mean nothing, so don't read the numbers. Sandbox results go to their own folder.
8. **Run it.** With the user's yes, run without `--sandbox` at the approved cap. Paste the script's printed summary and spend into the report. If it stops on the cap, report what was collected and ask before raising the cap.
9. **Move batches to the Standard queue.** For several hundred calls or scheduled monthly runs, POST to `.../task_post` (up to 100 tasks per POST, each with a `tag` holding the prompt id and sample), poll `.../tasks_ready`, and fetch `.../task_get/advanced/{id}` (LLM Responses: `.../task_get/{id}`). Save each result in the same `raw/` layout and re-score with the script. LLM Responses on the Standard queue can take up to 72 hours; Perplexity is Live only.
10. **Check the numbers before you trust them.**
    - Open 5 raw answers per engine and confirm the brand flags in `runs.csv` are right. If not, fix the aliases and re-run `score` (no calls).
    - Definitions: answer rate = runs with an AI answer ÷ runs; mention rate = runs naming the brand ÷ runs with an answer; citation rate = runs citing the brand's domain ÷ runs with an answer; named-first rate = runs where the brand is the first tracked brand named ÷ runs with an answer; share of voice = the brand's mentions ÷ mentions of all tracked brands on that engine.
    - Per money prompt, report how many of the 3 samples named the brand (0/3 to 3/3). 3/3 is steady presence; 1/3 is a coin toss.
    - Cited domains with 3 or more runs per engine form the source map for `ai-search-visibility`'s outreach and fix steps.
    - Copy wrong statements about the brand word for word, with engine and prompt, for `ai-brand-facts`.
11. **Report and repeat.** Same prompts, engines, market and samples each month. Call a change real only when it holds across two monthly runs, and keep a running cost log.

## What to hand back

Fill this in after each run. Every recommendation gets a priority label and an evidence label (`tool` for API data, `seen` for answers you opened) with confidence.

```markdown
# AI visibility tracking: [brand], [market], [date]

**What I found:** [one line, e.g. "Named in 31% of ChatGPT runs and 12% of AI Overviews that appeared; Globex leads both."]
**What matters most:** [one line, e.g. "G2's payroll category page is cited in 70% of runs and doesn't list us."]
**What to do first:** [one line]

## Method
- Prompts: [N] ([file], [groups]); engines, endpoints and models: [list]; samples per prompt: [n]; market: [location_code / language_code]; run dates: [dates]
- Cost: estimate $[low]-$[high], approved by [user] for cap $[cap]; actual $[spent]; cached calls: [n]

## Results by engine
| Engine (endpoint) | Answer rate | Mention rate | Citation rate | Named first | Share of voice | Leading competitor (mention rate) |
|---|---|---|---|---|---|---|

## Money prompts
- "[prompt]": [engine] [x/3], [engine] [x/3]; competitors named: [list]

## Most-cited domains
- [domain]: [engines], cited in [n] runs; mentions us: [yes / no / not checked]

## Database view (LLM Mentions, if run)
- [platform], [period]: our mentions [n], share of group sum [x%]; not comparable with sampled rates above

## What to do next
1. [Fix now | Fix next | Worth doing] [action] - why: [reason] - evidence: [tool | seen], [high | medium | low]

## What I could not check
- [engine, market or endpoint not run, calls that failed, rows not hand-checked, and what would verify them]
```

## Stop and flag if

- The user hasn't approved the estimate, or a run would go above the approved cap. Don't make the call.
- Credentials appear anywhere in chat, a file, a command line or output. Stop, tell the user to change the API password, and remove the file or line.
- The balance check fails, returns an error, or the balance is below the worst-case cost.
- The sandbox run fails or returns a shape the parser can't read. Fix that before any paid run.
- An engine returns errors for most calls (an unsupported `model_name`, a market without AI Mode). Report it rather than retrying in a loop.
- Unacceptable output: a single sample reported as a rate, numbers mixed across endpoints or markets without labels, LLM Mentions totals presented as shares, or any figure you didn't get from the API or a hand check.

## Next step

- `ai-search-visibility` with `summary.csv`, `domains.csv` and the gap prompts, to turn the numbers into a fix list.
- `ai-brand-facts` with the wrong statements copied from the raw answers.
- `ai-prompt-research` to add or retire prompts before next month's run, as a new group.

---
Part of the free RomeoSEO skill library: https://romeoseo.com/skills
