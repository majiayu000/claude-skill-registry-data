---
name: subito-cli
repo: remorses/subito-cli
description: |
  subito-cli searches subito.it listings (cars, and other categories) with
  every filter subito supports and prints NDJSON to stdout for piping into
  jq. It fetches through Playwriter (the user's real Chrome session), not a
  bare HTTP client, and parses subito's embedded __NEXT_DATA__ payload
  directly instead of scraping the DOM. ALWAYS load this skill when the user
  asks to search subito.it, find listings/cars/items on subito, or runs the
  `subito` command. Requires Chrome with the Playwriter extension enabled
  and the relay running (`playwriter serve`).
---

# subito-cli

Always run `subito --help` and `subito search --help` before using this CLI
to see the current filter flags, aliases, and examples.

For brand/model codes, first run `subito values cars/brands` (and
`subito values cars/brands/<code>/metamodels`) rather than guessing codes.

Output is NDJSON on stdout (one listing per line); use `jq -s` to collect
into an array before filtering/sorting/ranking. Progress and totals are
printed to stderr, so stdout stays pipeable.
