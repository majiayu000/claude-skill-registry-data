---
name: find-sellers
description: Get homes from a data source or spreadsheet, score them, and show Steve the best off-market seller leads. Use when Steve asks for leads, new homes, a list, the report, owner emails, or to load a file.
---

# Find likely sellers

1. Run `uv run python -m sellers sources` to see which sources are ready.
2. Pick the source with Steve:
   - **demo**: fake homes for practice. Free.
   - **rentcast**: real owners. Each city costs 1 request, and the free plan has
     50 requests a month. Before you run it, tell Steve how many requests this
     pull uses (one per city in `settings.toml`).
   - **a spreadsheet** (Realist, PropStream...): ask Steve where the file is,
     then run `uv run python -m sellers import "<path>"`. If the address column is
     not found, read the column names it printed. Add the right one to `ALIASES`
     in `sellers/sources/csv_file.py`, then run it again.
3. Pull: `uv run python -m sellers pull <source>`. Add `--city "Dana Point"` for
   one city. The tool scores the homes for you.
4. Show the top homes: `uv run python -m sellers top --n 10`. Explain in plain
   words why the first 2-3 homes scored high.
5. Open the full list: `uv run python -m sellers report`. Tell Steve he can
   search, filter, and click the column names to sort.

Next steps to offer, one at a time:
- No emails yet? Offer to find them (see below).
- Has emails? Offer `/write-emails`.
- Wants a different order? Change the points in `[scoring]` in `settings.toml`,
  then run `uv run python -m sellers score`.
- A home is not a fit? Run `uv run python -m sellers mark <id> skip --note "why"`.

## Finding owner emails (Tracerfy)

- Practise first, for free: `uv run python -m sellers find-emails --test --n 3`.
  The results are fake and use example.com.
- Live lookups cost about 2-4 cents per owner found, and nothing if no one is
  found. Before each live run, ask Steve and tell him the most it can cost
  (`--n` times $0.04). Then run `uv run python -m sellers find-emails --n <number>`.

Never share owner details outside this computer, except in Steve's own Gmail drafts.
