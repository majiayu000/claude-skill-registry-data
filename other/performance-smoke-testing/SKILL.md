---
name: performance-smoke-testing
category: qa
description: Use when a criterion mentions speed or limits, or the change touches a list, query, endpoint or page that could get slower - timing loops, the N-vs-10N data check and Lighthouse on a production build
---
# Performance Smoke Testing

Not full load testing — a smoke check run locally, never against stage or prod.

## API

```bash
for i in $(seq 20); do curl -s -o /dev/null -w '%{time_total}\n' "$BASE/api/tasks?limit=50"; done | sort -n | awk '{a[NR]=$1} END{print "p50="a[int(NR*.5)]" p95="a[int(NR*.95)]" max="a[NR]}'
```

Then run the same with 10x the seeded rows. p95 growing more than 3x for 10x the data is an N+1 suspicion — report it with the two numbers. Fail bar: p95 >1s for a simple read on localhost, or any number a criterion states explicitly. 0.5-1s is a note, not a fail.

## Concurrency smoke

Only when the change implies it (a shared resource, a write path under contention):

```bash
npx -y autocannon -c 10 -d 10 <url>
```

Errors must be 0.

## Web

Measure a **production build**, never a dev server — dev builds are unoptimized and that is where false fails come from:

```bash
npm run build && (nohup npx vite preview --port 4173 > "$QA/preview.log" 2>&1 &)
CHROME_PATH="$CHROME_BIN" npx -y lighthouse@13 http://localhost:4173/<page> --only-categories=performance --form-factor=mobile --screenEmulation.width=360 --chrome-flags="--headless=new" --output=json --output-path="$QA/lh-perf.json"
```

Report LCP/CLS/TBT against "good": LCP ≤2.5s, CLS ≤0.1, TBT ≤200ms. Fail only for a criterion's own number or a CLS shift you can see on a changed screen; other misses are notes, not fails.

## Never

Load-test stage or prod. Use k6 only when the repo already ships k6 scripts — not as the default tool.

## Recording

Record cases as `category: other` with a title prefix `perf:` — the category enum has no performance value of its own.
