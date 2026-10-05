---
name: qruiq-domain-name
description: |
  Find an available, memorable .com domain for a project. Reads the project to
  understand its semantic, brainstorms 15-20 brandable candidates, batch-checks
  whois, then ranks survivors by brevity, pronounceability, and brand fit.
  Use when asked to "pick a domain", "find a domain name", "name this project",
  "取个域名", "起个域名", "找个 .com 域名", or any request to choose a domain.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# qruiq-domain-name

Workflow for picking a `.com` domain that is **available, short, and memorable** — based on what the project actually does, not generic word salad.

## When to use

User wants a domain name for a project / product / side project. Default TLD is `.com` unless the user specifies otherwise. If they ask for `.io`, `.ai`, `.app`, etc., adapt the whois loop's domain list and adjust the brand criteria (e.g. `.ai` allows shorter, more abstract names).

## Step 1 — Understand the project (do not skip)

A good name comes from the product's actual semantic, not the user's prompt. Spend ~30 seconds:

1. Read `README.md` (and `README.zh.md` if present) for the elevator pitch and feature list.
2. Skim `package.json` `name` + key deps to identify the stack and category (SaaS? CLI? mobile? B2B vs B2C?).
3. Note 3-5 **semantic anchors**: the core noun (invoice, calendar, scraper), the audience tone (enterprise vs playful), and any unique angle (multi-company, AI-native, offline-first).

If the project has no README or it's too thin, **ask the user one question**: "What does this product do in one sentence, and who's it for?"

## Step 2 — Brainstorm 15-20 candidates

Generate a single batch using these patterns. Mix patterns — don't pick all from one bucket.

| Pattern | Example | Notes |
|---|---|---|
| Core noun + suffix `-ly`, `-ify`, `-er`, `-io` | `invoicely`, `billify` | Most are taken — try anyway, sometimes new ones survive |
| Core noun + neutral noun (`-hive`, `-trove`, `-dock`, `-raft`, `-seed`, `-mint`) | `billtrove`, `invoseed` | Higher availability rate |
| Truncated noun + vowel ending (`-o`, `-y`, `-a`, `-i`) | `invoyo`, `invoory` | Brandable, often available |
| Verb + noun (snap, flow, nudge, click + bill/voice) | `snapbill`, `nudgebill` | Common — many taken |
| Foreign / latin roots | `factura`, `solvo`, `quitto` | Niche but distinctive |
| Two short words joined | `paperbill`, `paydock` | Often taken; try less obvious combos |
| Playful / emoji-coded | `invomoji`, `billmoji` | High availability; only suit consumer/B2C |

**Rules for candidates:**
- Length ≤ 11 letters (shorter = more brandable, but most short names are taken)
- One or two syllables preferred, three max
- No numbers, no hyphens
- Pronounceable on first read by an English speaker
- No trademark conflicts with obvious brands (skip `googlevoice`, `stripebill`, etc.)

## Step 3 — Batch whois check

Run all candidates in one bash loop. **Critical zsh gotcha:** do NOT name the loop variable `status` — it's read-only in zsh and will crash the loop. Use `result`.

```bash
for d in candidate1.com candidate2.com candidate3.com; do
  result=$(whois "$d" 2>/dev/null | grep -iE "no match|not found|no data found|domain not found" | head -1)
  if [ -n "$result" ]; then
    echo "AVAILABLE: $d"
  else
    echo "TAKEN:     $d"
  fi
done
```

**Why this grep pattern:** different `.com` whois servers return different "not registered" phrases. These four cover Verisign, MarkMonitor, and most resellers. Don't simplify to just `"no match"` — you'll miss registrars.

If `whois` is missing, fall back to:
```bash
brew install whois   # macOS
```

## Step 4 — Re-verify survivors (avoid false positives)

The grep heuristic occasionally false-positives on rate-limited or unusual whois responses. For each `AVAILABLE:` hit, re-run with full output to confirm:

```bash
for d in survivor1.com survivor2.com; do
  echo "=== $d ==="
  whois "$d" 2>/dev/null | grep -iE "domain name:|registrar:|creation date:|no match|not found" | head -5
  echo ""
done
```

A truly available domain shows **only** the `No match` / `Not found` line and nothing else. If you see a `Creation Date:` or `Registrar:`, it's taken — drop it.

## Step 5 — If too few survivors, run a second batch

Aim for **at least 4-5 final candidates** to give the user real choice. If round 1 yields fewer, generate a second batch of 15-20 with different patterns (lean harder into invented words, foreign roots, or two-syllable joins). Don't repeat a pattern that produced 0 hits — pivot.

## Step 6 — Rank and recommend

Present 3-5 survivors ranked by **this priority order**:

1. **Brandability** — does it sound like a company name, not a description?
2. **Brevity** — fewer letters/syllables wins (within reason).
3. **Pronounceability** — can a non-native English speaker say it correctly on first read?
4. **Semantic fit** — does it hint at what the product does without being literal?
5. **Typeability** — no awkward letter combos, no easy typos (`invoory` is fine; `invohrxqy` is not).

For each, write **one sentence** explaining the etymology and vibe. Pick a single top recommendation and say why.

## Step 7 — Always include the registrar caveat

End with this disclaimer (paraphrase, don't copy verbatim):

> ⚠️ Whois showing "no match" doesn't guarantee you can register cheaply. Some unregistered names are flagged as **premium** by registrars and cost \$1k+. Confirm final price on Namecheap / Cloudflare Registrar / Porkbun before celebrating.

## Output format

Concise. Don't pad. Example shape:

```
推荐排序

1. **invoory.com** ⭐ — invoice + memory，4 音节 7 字母，最像独立单词
2. **invoseed.com** — invoice + seed，创业感、寓意正面
3. **billtrove.com** — bill + trove，归档调性

我会选 **invoory.com**：[一句话理由]

⚠️ [registrar caveat]
```

## What NOT to do

- Don't suggest `.com` domains without checking whois — "this might be available" is useless.
- Don't recommend a name with a hyphen or number (low brand value, hard to say out loud).
- Don't pick something that's only a literal description (`makesinvoices.com`) — that's SEO bait, not a brand.
- Don't recommend more than 5 finalists — choice paralysis.
- Don't run whois on 50+ domains in one shot — batches of 15-20 are the sweet spot for signal vs noise.
