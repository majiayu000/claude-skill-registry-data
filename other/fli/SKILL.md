---
name: fli
description: Search flights or flexible travel dates with the installed Fli CLI.
---

# Fli

Use `fli` for Google Flights searches.
It is installed through this personal Pi configuration; do not use `pip`, `pipx`, or a source checkout.

```sh
# Specific date
fli flights JFK LHR 2026-10-25

# Flexible date range
fli dates JFK LHR --from 2026-10-01 --to 2026-10-31
```

Use `fli flights --help` or `fli dates --help` before adding filters.
Use `--format json` only when machine-readable output is required; its schema is experimental.
Live Google Flights requests can be rate-limited or fail temporarily, so retry once after a short delay rather than treating one failure as a configuration error.
