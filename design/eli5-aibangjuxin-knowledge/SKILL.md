---
name: eli5
description: Explain like I'm five via single HTML. Use for /eli5 topics.
---

# eli5 — Explain Like I'm 5

Explain any topic to someone who knows **nothing** about it, using a **single self-contained HTML file** as the artifact. Big visuals, very few words.

## When to load this skill

Load when:
- User types `/eli5 <topic>`
- User asks "explain X like I'm five", "explain simply", "ELI5", "give me the dumb version"
- User wants a learning explainer for someone new (onboarding doc, kid, non-engineer)

Do NOT load when:
- User wants a detailed architecture diagram → use `architecture-diagram`
- User wants an ADR or formal design doc → use `architectrue`
- User wants code examples → just write code

## Input

Topic: `$ARGUMENTS` (when invoked via slash command) — the thing to explain.
If loaded outside slash command, the topic will appear in chat context; ask if unclear.

## Output format — strict

Produce **one HTML file** with these rules:

1. **Single self-contained file** — inline CSS, system font stack, no JS, no external CSS frameworks, no CDN font dependencies (system fonts only — keeps the file portable across company networks).
2. **Total visible text ≤ 250 words.** We're explaining to a 5-year-old, not a network engineer. Every word earns its place.
3. **4–6 panels**, each = one big visual (SVG icon, emoji, or simple shape) + one short caption (≤ 20 words).
4. **No jargon without inline definition.** The first time a technical term appears, immediately define it in plain language ("Response Policy — a little instruction that says: when someone asks for THIS name, give back THAT IP").
5. **Dark theme default** — `#020617` background, `#e2e8f0` text, `#22d3ee` cyan accent, `#34d399` emerald for "the answer / success state". Mirrors `architecture-diagram` palette so visual identity stays consistent.
6. **Cover both directions** — for systems, explain forward (what happens when X is asked) AND reverse (who set this up, who can change it, where is it logged). One inline aside is enough.
7. **HTML comments for citations** — at the bottom of the file, add one `<!-- cite: <URL> -->` per factual claim. Invisible to readers, visible to maintainers. Implements the "简化 vs 严格原话" two-column discipline: simple text on screen, strict source in source.

## Suggested panel structure

1. **Hero** — one-line question that frames the topic
2. **The trigger** — who/what starts the action
3. **The middle** — the mechanism (1-3 panels depending on complexity)
4. **The outcome** — what happens at the end
5. **(Optional) who controls it** — ownership / audit / change-control aside

> For systems topics with ≥3 of {two independent actors, clear mechanism, accept-list / auth, crisp outcome}, use all 6 panels. See `references/worked-examples.md` for a real one (PSC) and common mapping mistakes.

## Tools

- `scripts/wordcount.py` — counts REAL visible words (strips `<style>`, `<svg>`, `<!-- -->` before counting). The naive `sed | wc -w` recipe overcounts by 2-3x.

## Style rules

- System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- Generous whitespace (≥ 1.5rem between panels)
- One `<h1>` total — the title in plain language, not the topic jargon
- Each panel is a `<section>` with a class (e.g. `panel panel-trigger`)
- SVG inline only — no `<img>` tags pointing to external files

## Verification checklist before saving

- [ ] **Visible text count** uses the corrected recipe (not naive `sed`). Run the bundled `scripts/wordcount.py` — the naive `sed -E 's/<[^>]+>//g'` inflates the count by 2-3x because it includes `<style>` CSS, `<svg>` text attributes, and HTML comments. Target ≤ 250, hard cap ≤ 280.
  ```bash
  python3 scripts/wordcount.py file.html             # 224 words  [OK]
  python3 scripts/wordcount.py file.html --verbose   # also prints the visible text
  python3 scripts/wordcount.py file.html --budget 230 # tighter budget
  ```
- [ ] All factual claims have a corresponding `<!-- cite: -->` comment at bottom
- [ ] No external resource requests (open in preview pane with network throttling — should look identical offline)
- [ ] Dark theme intact, panels render in order, no JS console errors
- [ ] Filename follows user's naming convention: `<topic>-eli5.html` or `<topic>-explainer.html`

## Pitfalls

- **CSS counts as words.** The naive `wc -w` / `sed '<[^>]+>'` recipe in the checklist counts CSS rules and SVG `<text>` elements as visible text. A 224-word ELI5 file measures ~587 with that recipe. Always strip `<style>`, `<svg>`, and `<!-- -->` blocks BEFORE counting.
- **First drafts run 20-30% over budget.** Plan for it. Write the panels at 70% of target length, then expand only if under. A 6-panel file with ~35-40 words per panel lands in range.
- **Forward + reverse is mandatory for systems topics**, not optional. The reverse panel (who set this up, who can change it, where audit logs land) usually eats 25-35 words — budget for it from the start instead of trimming it at the end.
- **Inline jargon definition adds word count.** Each first-mention of a term like "NEG" or "IAM" costs ~5-8 words. Pre-budget: if you have 3 jargon terms, that's ~20 words of overhead before the panel's main message.

## Example invocation

```
/eli5 how does GCP Cloud DNS Response Policy work
```

Expected: a single HTML file with ≤ 6 panels, dark theme, ≤ 250 words of visible text, explaining the response policy mechanism to someone who has never heard of DNS.
