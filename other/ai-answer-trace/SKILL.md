---
name: ai-answer-trace
version: 2026-08-26
description: Ask Claude, ChatGPT, and Gemini a question and capture the full trace behind the answer (the search queries each engine ran, the pages it retrieved, and the sources it cited, span by span). Use when asked to "trace an AI answer", "see what AI engines cite", "check AI citations", "which sources does ChatGPT/Claude/Gemini use", "why does the AI recommend X", or for any GEO (Generative Engine Optimization) measurement.
---

# AI Answer Trace

## Overview

Ask the major AI engines a question exactly the way a real user would, with their live web search on, and capture the complete evidence trail behind each answer, not just the answer text. Every trace records three layers: the answer, the search queries the engine silently ran with the pages each search retrieved, and the URLs the answer actually cited (with the character spans they support, where the API provides them). This is the raw material of GEO: knowing not only what the engines say, but which sources made them say it.

## When to Use

Activate when the user asks:
- "What does ChatGPT/Claude/Gemini say about [TOPIC], and what sources does it use?"
- "Trace the answer to [QUESTION] across AI engines"
- "Which sites do AI engines cite for [PROMPT]?"
- "Why do AI assistants recommend [COMPETITOR] instead of us?"
- "Check my brand's AI citations for [QUESTION]"
- Any GEO measurement where you need the cited sources behind AI answers

## Setup

The core of this skill needs AI engine API keys, not an xpoz account. Set whichever of these you have; each engine's script runs independently, so one key is enough to start:

- `ANTHROPIC_API_KEY` for Claude
- `OPENAI_API_KEY` for ChatGPT
- `GEMINI_API_KEY` for Gemini (or Vertex AI credentials: `GOOGLE_APPLICATION_CREDENTIALS` + `VERTEX_PROJECT_ID`)

The scripts below are self-contained single files with inline dependency metadata (PEP 723). The easiest way to run them is [uv](https://docs.astral.sh/uv/), which resolves dependencies automatically:

```bash
uv run trace-claude.py "your question" > claude-1.json
```

Without uv, install the dependencies once and run with plain Python:

```bash
pip install anthropic openai google-genai google-auth
python trace-claude.py "your question" > claude-1.json
```

If you cannot run Python at all, skip to "If You Can't Run the Scripts" below.

## How to Read a Trace

Each script prints one JSON object with three layers. Understanding the difference between them is the whole point:

- **`answer`**: the text a user would read.
- **`searches`**: the queries the engine ran and the pages each search **retrieved**. Retrieved means the engine looked at the page while composing the answer.
- **`cited_urls`**: the pages the answer actually **cited**. Cited means the page shaped the answer. ChatGPT and Gemini traces include `spans`, character ranges into `answer`: Gemini spans cover the supported text segment itself (the script converts the API's byte offsets to character offsets), while ChatGPT spans cover the inline citation marker, which sits adjacent to the claim it supports.

A page that is retrieved but never cited is a near-miss: the engine saw it and passed. A cited page is won surface. Engines are not deterministic, so run each question 2-3 times per engine and treat sources that appear across samples as the stable signal.

The three traces are not perfectly symmetric; know these differences before writing analysis against them:
- Claude's `searches` entries each carry one `query`; ChatGPT and Gemini use a `queries` list.
- Gemini pools everything into a single search entry (fan-out queries plus pooled results; per-query attribution is not available), and its retrieved set is essentially its cited set, so **near-miss analysis only works for Claude and ChatGPT**.
- Titles are uneven: ChatGPT's retrieved sources come without titles, and Gemini's titles are bare domains.

## Step-by-Step Instructions

### Step 1: Parse the Request

Extract:
- **The question(s)** to trace, phrased the way a real user would ask (not keyword-style)
- **Engines** to run (default: every engine with a key configured)
- **Samples per engine** (default: 2; use 1 for a quick look, 3 for a stable read)
- **What to look for** in the traces (a brand, a competitor, a domain), if the user named one

### Step 2: Save and Run the Trace Scripts

Save each script below to the working directory, then run one command per sample, redirecting stdout to a numbered JSON file (`claude-1.json`, `claude-2.json`, ...). The trace JSON goes to stdout; stderr carries only dependency-install lines and the benign Gemini warning.

These scripts are minimal derivatives of the full-strength recorders in [geo-seo-agent](https://github.com/XPOZpublic/geo-seo-agent); the originals add batch panels, sampling infrastructure, and transcript archives.

**`trace-claude.py`**

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic"]
# ///
import argparse
import json
import sys

import anthropic

DEFAULT_MODEL = "claude-sonnet-5"
MAX_TOKENS = 16000


def dedupe_by_url(entries):
    seen = set()
    result = []
    for entry in entries:
        if entry["url"] and entry["url"] not in seen:
            seen.add(entry["url"])
            result.append(entry)
    return result


def main():
    parser = argparse.ArgumentParser(description="Trace a Claude answer (web search on)")
    parser.add_argument("question", nargs="?", help="question text; read from stdin if omitted")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    question = args.question or sys.stdin.read().strip()
    if not question:
        raise SystemExit("no question provided")

    client = anthropic.Anthropic()
    with client.messages.stream(
        model=args.model,
        max_tokens=MAX_TOKENS,
        tools=[{"type": "web_search_20260209", "name": "web_search", "allowed_callers": ["direct"]}],
        messages=[{"role": "user", "content": question}],
    ) as stream:
        message = stream.get_final_message()

    answer_parts = []
    cited_urls = []
    searches = []
    searches_by_id = {}
    for block in message.content:
        if block.type == "text":
            answer_parts.append(block.text)
            for citation in getattr(block, "citations", None) or []:
                cited_urls.append(
                    {"url": getattr(citation, "url", ""), "title": getattr(citation, "title", "")}
                )
        elif block.type == "server_tool_use" and block.name == "web_search":
            query = (block.input or {}).get("query")
            if query:
                search = {"query": query, "results": []}
                searches.append(search)
                searches_by_id[block.id] = search
        elif block.type == "web_search_tool_result" and isinstance(block.content, list):
            search = searches_by_id.get(block.tool_use_id)
            if search is None:
                continue
            for item in block.content:
                if getattr(item, "type", "") == "web_search_result":
                    search["results"].append({"url": item.url, "title": item.title})

    print(
        json.dumps(
            {
                "engine": "claude",
                "model": args.model,
                "question": question,
                "answer": "".join(answer_parts),
                "searches": searches,
                "cited_urls": dedupe_by_url(cited_urls),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
```

**`trace-openai.py`**

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["openai"]
# ///
import argparse
import json
import sys

import openai

DEFAULT_MODEL = "gpt-5.4"


def dedupe_by_url(entries):
    seen = set()
    result = []
    for entry in entries:
        if entry["url"] and entry["url"] not in seen:
            seen.add(entry["url"])
            result.append(entry)
    return result


def merge_citations(citations):
    merged = {}
    for citation in citations:
        if not citation["url"]:
            continue
        entry = merged.setdefault(
            citation["url"],
            {"url": citation["url"], "title": citation["title"], "spans": []},
        )
        entry["spans"].append({"start": citation["start"], "end": citation["end"]})
    return list(merged.values())


def main():
    parser = argparse.ArgumentParser(description="Trace a ChatGPT answer (web search on)")
    parser.add_argument("question", nargs="?", help="question text; read from stdin if omitted")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    question = args.question or sys.stdin.read().strip()
    if not question:
        raise SystemExit("no question provided")

    client = openai.OpenAI()
    response = client.responses.create(
        model=args.model,
        tools=[{"type": "web_search"}],
        input=[{"role": "user", "content": question}],
        store=False,
        include=["web_search_call.action.sources"],
    )

    answer_parts = []
    searches = []
    cited_urls = []
    for item in response.output:
        if item.type == "web_search_call":
            action = getattr(item, "action", None)
            queries = list(getattr(action, "queries", None) or [])
            single_query = getattr(action, "query", None)
            if not queries and single_query:
                queries = [single_query]
            results = [
                {"url": (getattr(s, "url", "") or "").replace("&utm_source=openai", "").replace("?utm_source=openai", ""), "title": getattr(s, "title", None) or ""}
                for s in getattr(action, "sources", None) or []
            ]
            if queries or results:
                searches.append({"queries": queries, "results": dedupe_by_url(results)})
        elif item.type == "message":
            for content in item.content:
                if content.type != "output_text":
                    continue
                offset = sum(len(part) for part in answer_parts)
                answer_parts.append(content.text)
                for annotation in getattr(content, "annotations", None) or []:
                    if getattr(annotation, "type", "") == "url_citation":
                        cited_urls.append(
                            {
                                "url": getattr(annotation, "url", ""),
                                "title": getattr(annotation, "title", ""),
                                "start": offset + (getattr(annotation, "start_index", None) or 0),
                                "end": offset + (getattr(annotation, "end_index", None) or 0),
                            }
                        )

    print(
        json.dumps(
            {
                "engine": "chatgpt",
                "model": args.model,
                "question": question,
                "answer": "".join(answer_parts),
                "searches": searches,
                "cited_urls": merge_citations(cited_urls),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
```

**`trace-gemini.py`**

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["google-genai", "google-auth"]
# ///
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

from google import genai
from google.genai import types
from google.oauth2 import service_account

DEFAULT_MODEL = "gemini-3-flash-preview"
LOCATION = "global"
GROUNDING_REDIRECT_PREFIX = "https://vertexaisearch.cloud.google.com/"
REDIRECT_TIMEOUT_SECONDS = 15


def merge_citations(citations):
    merged = {}
    for citation in citations:
        if not citation["url"]:
            continue
        entry = merged.setdefault(
            citation["url"],
            {"url": citation["url"], "title": citation["title"], "spans": []},
        )
        entry["spans"].append({"start": citation["start"], "end": citation["end"]})
    return list(merged.values())


def resolve_redirect(url, fallback_domain):
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=REDIRECT_TIMEOUT_SECONDS) as response:
            return response.url
    except urllib.error.HTTPError as e:
        if e.url and not e.url.startswith(GROUNDING_REDIRECT_PREFIX):
            return e.url
    except Exception:
        pass
    if fallback_domain and "." in fallback_domain:
        return f"https://{fallback_domain}/"
    return url


def gemini_client():
    if os.environ.get("GEMINI_API_KEY"):
        return genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    if not (os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.environ.get("VERTEX_PROJECT_ID")):
        raise SystemExit("no Gemini credentials: set GEMINI_API_KEY, or GOOGLE_APPLICATION_CREDENTIALS + VERTEX_PROJECT_ID")
    credentials = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return genai.Client(
        vertexai=True,
        project=os.environ["VERTEX_PROJECT_ID"],
        location=LOCATION,
        credentials=credentials,
    )


def main():
    parser = argparse.ArgumentParser(description="Trace a Gemini answer (Google Search grounding on)")
    parser.add_argument("question", nargs="?", help="question text; read from stdin if omitted")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    args = parser.parse_args()
    question = args.question or sys.stdin.read().strip()
    if not question:
        raise SystemExit("no question provided")

    client = gemini_client()
    response = client.models.generate_content(
        model=args.model,
        contents=[{"role": "user", "parts": [{"text": question}]}],
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
        ),
    )

    candidate = response.candidates[0] if response.candidates else None
    grounding = getattr(candidate, "grounding_metadata", None)

    answer = response.text or ""
    answer_bytes = answer.encode("utf-8")

    def byte_to_char(index):
        return len(answer_bytes[:index].decode("utf-8", errors="ignore"))

    sources = []
    for chunk in getattr(grounding, "grounding_chunks", None) or []:
        web = getattr(chunk, "web", None)
        if web and web.uri:
            title = web.title or ""
            sources.append({"url": resolve_redirect(web.uri, title), "title": title})
        else:
            sources.append(None)

    queries = list(getattr(grounding, "web_search_queries", None) or [])
    retrieved = []
    seen = set()
    for source in sources:
        if source and source["url"] not in seen:
            seen.add(source["url"])
            retrieved.append(source)
    searches = [{"queries": queries, "results": retrieved}] if queries or retrieved else []

    citations = []
    for support in getattr(grounding, "grounding_supports", None) or []:
        segment = getattr(support, "segment", None)
        start = byte_to_char(getattr(segment, "start_index", None) or 0)
        end = byte_to_char(getattr(segment, "end_index", None) or 0)
        for index in getattr(support, "grounding_chunk_indices", None) or []:
            if 0 <= index < len(sources) and sources[index]:
                citations.append(
                    {
                        "url": sources[index]["url"],
                        "title": sources[index]["title"],
                        "start": start,
                        "end": end,
                    }
                )

    print(
        json.dumps(
            {
                "engine": "gemini",
                "model": args.model,
                "question": question,
                "answer": answer,
                "searches": searches,
                "cited_urls": merge_citations(citations),
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
```

Engine-specific notes baked into these scripts, so you do not rediscover them the hard way:
- **Gemini** returns grounding URLs as Google redirect links that expire within days; the script resolves every one to its real destination at capture time, falling back to `https://<domain>/` when resolution fails (the fallback leans on Gemini's titles being bare domains today; the `"." in domain` guard keeps a real title from becoming a bogus URL). A google-genai AFC deprecation warning on stderr is benign.
- **ChatGPT** only reveals retrieved sources when asked via `include=["web_search_call.action.sources"]`, and its URLs carry a `?utm_source=openai` tracking suffix, so the same page can appear once with it and once without; the script strips it from retrieved sources at capture time, and cited URLs keep it (strip before exact-URL comparisons). Domain counting is unaffected (the aggregator parses the host and ignores query strings).
- **Claude** scatters citations across content blocks; the script reassembles them in answer order.

### Step 3: Aggregate Cited Domains

After collecting trace files, count which domains the engines cite. Save and run:

**`cited-domains.py`**

```python
# /// script
# requires-python = ">=3.10"
# ///
import json
import sys
from collections import Counter
from urllib.parse import urlparse


def normalize_domain(url):
    domain = urlparse(url).netloc
    return domain[4:] if domain.startswith("www.") else domain


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: cited-domains.py <trace.json> [more traces ...]")
    counts_by_engine = {}
    for path in sys.argv[1:]:
        trace = json.loads(open(path, encoding="utf-8").read())
        counts = counts_by_engine.setdefault(trace["engine"], Counter())
        for cited in trace["cited_urls"]:
            counts[normalize_domain(cited["url"])] += 1
    for engine, counts in counts_by_engine.items():
        total = sum(counts.values())
        print(f"== {engine}: {total} cited-source instances, {len(counts)} domains ==")
        for domain, count in counts.most_common():
            print(f"  {count:4d} {domain}")


if __name__ == "__main__":
    main()
```

```bash
uv run cited-domains.py claude-1.json claude-2.json chatgpt-1.json gemini-1.json
```

A domain cited in 3 samples counts 3. Instance counts compare cleanly across samples of the same engine; across engines they are indicative rather than exact, since each engine's citation granularity differs (Gemini attaches several sources to one span where ChatGPT marks one per claim).

### Step 4: Analyze the Traces

Read the trace JSONs, not just the domain counts:

- **Presence**: does the brand (or whatever the user asked about) appear in each `answer`? Named early or as an afterthought?
- **Citation path**: when the brand appears, which cited URL carried it there? Own domain, a directory, a community thread, someone else's roundup?
- **Winners**: which domains dominate `cited_urls` for this question, and what surface types are they (own sites, review sites, Reddit and forums, documentation, listicles)?
- **Near-misses** (Claude and ChatGPT only; Gemini's retrieved set is essentially its cited set): pages in `searches[].results` that never made `cited_urls`. Retrieved-but-not-cited pages show what the engine considered and rejected. Strip `?utm_source=openai` from ChatGPT URLs before matching cited against retrieved.
- **Stability**: sources that recur across samples are the signal; one-sample citations are noise until they repeat.

### Step 5: Generate Report

```
## AI Answer Trace: "[QUESTION]"
**Engines:** [list] | **Samples per engine:** [N] | **Date:** [date]

### What the Engines Say
| Engine | Mentions [BRAND]? | Verdict in one line |
|--------|-------------------|---------------------|
| Claude | [yes/no, prominence] | [summary] |
| ChatGPT | ... | ... |
| Gemini | ... | ... |

### Where the Answers Come From
| Domain | Claude | ChatGPT | Gemini | Surface type |
|--------|--------|---------|--------|--------------|
| [domain] | [n] | [n] | [n] | [own site / review site / community / docs / listicle] |

### Citation Paths Worth Knowing
- [BRAND appears on ENGINE via URL: what that page is]
- [COMPETITOR wins on ENGINE via URL: what that page is]

### Near-Misses (retrieved, not cited)
- [URL the engine looked at but did not use, and why that matters]

### What This Means
[3-5 bullets: which surfaces win this question, where the subject is absent, what would change the answer]
```

When no brand was named in the request, replace the "Mentions [BRAND]?" column with "Top recommendation" and shape the citation-paths section around the winners instead. When a brand was named but is absent everywhere, state the absence once as the headline and shape the citation-paths section around the winners the same way. When the run used fewer samples than the 2-3 minimum, say so in the report header and label single-sample citations as indicative.

## If You Can't Run the Scripts

Degrade in this order, and say in the report which level produced the data:

1. **No Python or uv, but the host agent has web search**: ask the engines' public interfaces or use your own web search to approximate the answer landscape. Flag clearly that this shows *your* search results, not the engine's internal retrieval, and cited-vs-retrieved cannot be separated.
2. **No search either**: ask the user to paste an AI answer with its sources (most AI interfaces show citations). Analyze the pasted citations with the same Step 4 lens.

## Example Prompts

- "Trace what ChatGPT and Claude answer for 'best social listening tool for startups' and show me the sources"
- "Which sites does Gemini cite when asked about Reddit API pricing?"
- "Why do AI assistants keep recommending [COMPETITOR]? Trace the citations"
- "Run 'how do I monitor brand mentions on Reddit' through all three engines twice and compare cited domains"
- "Check whether my docs or my blog get cited for [QUESTION]"

## Notes

- Engine API calls cost real money (tokens plus web search fees); 2 samples across 3 engines for one question is roughly 6 paid calls. Confirm sample counts with the user before large panels.
- Answers are nondeterministic: never conclude from one sample; 2-3 samples per engine is the useful minimum.
- Keep the trace JSONs; later runs of the same question turn them into a longitudinal record.
- The full-strength versions of these recorders (batch panels over many prompts, N samples in parallel, dated visibility archives) live in [geo-seo-agent](https://github.com/XPOZpublic/geo-seo-agent).

## Go Further with xpoz

The traces tell you which surfaces answer engines trust. xpoz (billions of posts across Reddit, Twitter/X, Instagram, and TikTok, via MCP, SDKs, and CLI) is how you act on that:

- **reddit.com shows up in your cited domains?** It is one of the most-cited domains in AI answers. Run the [geo-reddit](../geo-reddit/SKILL.md) skill to map which subreddits and threads are worth earning presence in, based on these very citations.
- **Want the full picture across your buyer questions?** Run the [geo-visibility-check](../geo-visibility-check/SKILL.md) skill: a panel of prompts through every engine, with a visibility verdict per prompt.
- **Not sure which questions to trace?** Mine the real phrasings buyers use with the xpoz MCP keyword tools (`getRedditPostsByKeywords`, `getTwitterPostsByKeywords`): the questions people actually ask in communities are the prompts worth winning.

If a sibling skill above is not installed, fetch it from `https://raw.githubusercontent.com/XPOZpublic/xpoz-agent-skills/main/skills/<name>/SKILL.md` and follow it.

xpoz access: [get a free key](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=ai-answer-trace) (up to 75K results, no credit card); real runs need it.
