---
name: adsPower
description: Give every account on a browser platform its AdsPower profile, give profiles back, check the Local API, and keep the browser-driver rules (rules 35, 44)
---

# adsPower

## Hard boundaries

1. **Twenty stays the source.** An AdsPower profile is the browser for one
   `socialAccounts` row, linked by `adsPowerProfileId`. The Twenty row is never deleted; a DEACTIVATED
   account, or one whose home is not in `LOG_ADSPOWER_HOMES`, gives its profile back (deleted from
   AdsPower, `adsPowerProfileId` cleared).
2. **No secret in AdsPower at rest.** Profiles are made with no proxy, password or 2FA key.
   `python/browser/browserDriver.py` puts the proxy on only to open, after the gate, and clears it at close.
3. **Same as Camoufox** (rule 44). An AdsPower session goes through the same gate and
   self-check (rule 35), session HAR (rule 19), human mouse and scroll. `docs/browsers.md`
   lists what's built; `bun run check:browsers` keeps every browser in step.
4. **Camoufox stays.** With `browserDriver` empty, an account with a linked profile opens on AdsPower
   and one without opens on Camoufox. Never remove it.
5. **Never print `ADSPOWER_API_KEY`.** It lives in `.env.local` and the local-scope MCP config.

## Environment

- The AdsPower app is running here: `log adsPower status` says "up".
- `.env.local` has `ADSPOWER_HOST` (default `http://local.adspower.net:50325`) and `ADSPOWER_API_KEY`.
- AdsPower's MCP server (`adspower-local-api`) is added at local scope. AdsPower's own skill is
  reinstalled with `npx skills add https://github.com/adspower/adspower-browser --skill adspower-browser`
  (vendor kebab-case names, git-ignored by rule 1).

## Commands

```bash
log adsPower status                 # the Local API answers
log adsPower profiles               # AdsPower's profiles, and the Twenty account of each
log adsPower sync                   # dry run: release / create / relink / linked / skip per account
log adsPower sync --apply           # give back DEACTIVATED and out-of-home profiles, make the missing ones, link them in Twenty
log adsPower sync --apply --homes US  # this run's homes (default LOG_ADSPOWER_HOMES)
log adsPower sync --apply --account <accountName>
```

Run `sync --apply` through Monitor (rule 26): it prints one line per account as it goes.
A `skip` is a banned or dead account, one with no home country in `HOME_COUNTRIES`, or one outside the
homes that holds no profile. What the sync must do: `docs/specs/adsPower.md`.
A failed create usually means the plan's profile limit: the AdsPower plan must hold at least as many profiles as accounts.

## Adding another browser

Write a `BrowserDriver` (`src/browser/driver/types.ts`): prepare, gate, start, selfCheck, stop.
Add its name to `BROWSER_DRIVERS`. The machine already enforces the order, so the new browser
can't skip the gate or the self-check. Details: `docs/adsPower.md`.
