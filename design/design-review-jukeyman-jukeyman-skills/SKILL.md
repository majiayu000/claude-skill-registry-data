---
name: design-review
description: Review UI for anti-AI-slop compliance
---

# Design Review Checklist

1. Screenshot or render the page
2. Check fonts: are banned fonts (Inter, Roboto, Arial) used? FAIL if yes.
3. Check colors: generic purple/blue gradient? FAIL if yes.
4. Check layout: centered-everything? Card grid without variation? FAIL.
5. Check images: placeholder.com or Lorem? FAIL.
6. Check animations: no motion at all? FAIL. Excessive jank? FAIL.
7. Check states: missing loading/error/empty states? FAIL.
8. Check mobile: broken at 375px? FAIL.
9. Check accessibility: contrast ratio < 4.5:1? FAIL.
10. Score: PREMIUM (9-10 pass) / ACCEPTABLE (7-8) / AI-SLOP (< 7)
