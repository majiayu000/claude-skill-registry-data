---
name: qa-detect-word-break
section: responsiveness
description: "Detects long unbreakable text (URLs, emails, code identifiers) that overflows its container — common with user-generated content and missing overflow-wrap"
model: haiku
applyOn: all
needsSetup: false
viewportSensitive: true
---

## What it checks

When containers hold user-generated text (URLs, emails, hashes, long IDs), a single unbreakable token can push the container past its parent and cause horizontal overflow. The fix is `overflow-wrap: anywhere` or `word-break: break-word`.

This skill finds text-bearing containers whose `scrollWidth` exceeds their `clientWidth` due to long unbreakable words.

## Probe (browser_evaluate)

```js
() => {
  const sel = el => {
    const id = el.id ? `#${el.id}` : '';
    const cls = (el.className && typeof el.className === 'string')
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return (el.tagName.toLowerCase() + id + cls).slice(0, 120);
  };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };
  const out = [];

  // Text-bearing containers: p, span, td, li, dd, blockquote, pre, code, .description, .comment
  const candidates = document.querySelectorAll(
    'p, td, li, dd, blockquote, pre, code, ' +
    '[class*="description"], [class*="comment"], [class*="message"], [class*="body"]'
  );

  for (const el of candidates) {
    if (out.length >= 12) break;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const text = (el.innerText || '').trim();
    if (text.length < 10) continue;

    // Does the element overflow horizontally?
    const overflows = el.scrollWidth > el.clientWidth + 4;
    if (!overflows) continue;

    const style = getComputedStyle(el);
    // If it has proper wrapping, skip
    const hasWrap = style.overflowWrap === 'anywhere' || style.overflowWrap === 'break-word' ||
                     style.wordBreak === 'break-all' || style.wordBreak === 'break-word' ||
                     style.overflowX === 'auto' || style.overflowX === 'scroll' ||
                     style.overflowX === 'hidden';
    if (hasWrap) continue;

    // Find the longest unbreakable token in the text
    const tokens = text.split(/\s+/);
    let longestLen = 0;
    let longestSample = '';
    for (const t of tokens) {
      if (t.length > longestLen) {
        longestLen = t.length;
        longestSample = t.slice(0, 40) + (t.length > 40 ? '…' : '');
      }
    }
    if (longestLen < 20) continue;  // Probably normal overflow, not long-word

    out.push({
      issueType: 'longWordOverflow',
      severity: 'medium',
      selector: sel(el),
      description: `Element ${sel(el)} overflows due to long unbreakable token "${longestSample}" (${longestLen} chars). Add overflow-wrap: anywhere or word-break: break-word.`,
      bbox: bb(el)
    });
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| longWordOverflow | medium | "Container overflows due to a long unbreakable token (URL/email/hash) — add overflow-wrap or word-break" |
