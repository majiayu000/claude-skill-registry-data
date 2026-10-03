---
name: spike
description: "Throwaway experiments to validate an idea before build."
allowed-tools:
  - bash
  - write_file
  - read_file
  - web_search
  - browse_page
enabled: true
related-skills: [plan, systematic-debugging]
license: MIT
author: Adapted from hermes-agent (Nous Research, MIT); gsd-build/get-shit-done
---

# Spike

Use this skill when the user wants to **feel out an idea** before committing to
a real build — validating feasibility, comparing approaches, or surfacing
unknowns that no amount of research will answer. Spikes are disposable by
design. Throw them away once they've paid their debt.

Load this when the user says things like "let me try this", "I want to see if
X works", "spike this out", "before I commit to Y", "quick prototype of Z",
"is this even possible?", or "compare A vs B".

## When NOT to use this

- The answer is knowable from docs or reading code — just do research, don't build
- The work is production path — use the `plan` skill instead
- The idea is already validated — jump straight to implementation

## Core method

Regardless of scale, every spike follows this loop:

```
decompose  →  research  →  build  →  verdict
   ↑__________________________________________↓
                  iterate on findings
```

### 1. Decompose

Break the user's idea into **2-5 independent feasibility questions**. Each
question is one spike. Present them as a table with Given/When/Then framing:

| # | Spike | Validates (Given/When/Then) | Risk |
|---|-------|----------------------------|------|
| 001 | websocket-streaming | Given a WS connection, when LLM streams tokens, then client receives chunks < 100ms | High |
| 002a | pdf-parse-pdfjs | Given a multi-page PDF, when parsed with pdfjs, then structured text is extractable | Medium |
| 002b | pdf-parse-camelot | Given a multi-page PDF, when parsed with camelot, then structured text is extractable | Medium |

**Spike types:**
- **standard** — one approach answering one question
- **comparison** — same question, different approaches (shared number, letter suffix)

**Order by risk.** The spike most likely to kill the idea runs first.

**Skip decomposition** only if the user already knows exactly what they want to
spike. Then take their idea as a single spike.

### 2. Align (for multi-spike ideas)

Present the spike table. Ask: "Build all in this order, or adjust?" Let the
user drop, reorder, or re-frame before you write any code.

### 3. Research (per spike, before building)

Spikes are not research-free — you research enough to pick the right approach,
then you build. Per spike:

1. **Brief it.** 2-3 sentences: what this spike is, why it matters, key risk.
2. **Surface competing approaches** if there's real choice:

   | Approach | Tool/Library | Pros | Cons | Status |
   |----------|-------------|------|------|--------|
   | ... | ... | ... | ... | maintained / abandoned / beta |

3. **Pick one.** State why. If 2+ are credible, build quick variants within the spike.
4. **Skip research** for pure logic with no external dependencies.

Use Poirot tools for the research step:

- `web_search("python websocket streaming libraries 2025")` — find candidates
- `browse_page(url="https://websockets.readthedocs.io/...")` — read the docs
- `bash("pip show websockets | grep Version")` — check what's installed

### 4. Build

One directory per spike. Keep it standalone.

```
spikes/
├── 001-websocket-streaming/
│   ├── README.md
│   └── main.py
├── 002a-pdf-parse-pdfjs/
│   ├── README.md
│   └── parse.js
└── 002b-pdf-parse-camelot/
    ├── README.md
    └── parse.py
```

**Bias toward something the user can interact with.** Spikes fail when the only
output is a log line that says "it works." Default choices, in order:

1. A runnable CLI that takes input and prints observable output
2. A minimal HTML page that demonstrates the behavior
3. A small web server with one endpoint
4. A unit test that exercises the question with recognizable assertions

**Depth over speed.** Never declare "it works" after one happy-path run. Test
edge cases. Follow surprising findings.

**Avoid** unless the spike specifically requires it: complex package management,
build tools/bundlers, Docker, env files, config systems. Hardcode everything —
it's a spike.

**Building one spike** — a typical tool sequence:

```
bash("mkdir -p spikes/001-websocket-streaming")
write_file("spikes/001-websocket-streaming/README.md", "# 001: websocket-streaming\n\n...")
write_file("spikes/001-websocket-streaming/main.py", "...")
bash("cd spikes/001-websocket-streaming && python3 main.py")
# Observe output, iterate.
```

> **Poirot note:** The original skill runs comparison spikes (002a / 002b) in
> parallel via subagent delegation. Poirot has no subagents, so build
> comparison spikes **sequentially** — finish one before starting the next,
> then do the head-to-head comparison.

### 5. Verdict

Each spike's `README.md` closes with:

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED

### What worked
- ...

### What didn't
- ...

### Surprises
- ...

### Recommendation for the real build
- ...
```

**VALIDATED** = the core question was answered yes, with evidence.
**PARTIAL** = it works under constraints X, Y, Z — document them.
**INVALIDATED** = doesn't work, for this reason. This is a successful spike.

## Comparison spikes

When two approaches answer the same question (002a / 002b), build them **back
to back**, then do a head-to-head comparison:

```markdown
## Head-to-head: pdfjs vs camelot

| Dimension | pdfjs (002a) | camelot (002b) |
|-----------|--------------|----------------|
| Extraction quality | 9/10 structured | 7/10 table-only |
| Setup complexity | npm install, 1 line | pip + ghostscript |
| Perf on 100-page PDF | 3s | 18s |
| Handles rotated text | no | yes |

**Winner:** pdfjs for our use case.
```

## Output

- Create `spikes/` in the repo root
- One dir per spike: `NNN-descriptive-name/`
- `README.md` per spike captures question, approach, results, verdict
- Keep the code throwaway — a spike that takes 2 days to "clean up for
  production" was a bad spike
