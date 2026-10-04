---
name: timermeet-security-audit
description: Run a deep, adversarial multi-angle vulnerability hunt across TimerMeet (beyond the routine pre-release bandit/pip-audit checklist). Use when the user explicitly asks to look for vulnerabilities, worries about being hacked, wants a security audit/pentest-style self-review, or periodically for a major release -- NOT for every routine release (use `timermeet-security-guardian` for that fast gate instead).
---

# TimerMeet Security Audit

## When to use this vs. `timermeet-security-guardian`

- **`timermeet-security-guardian`** = the fast, cheap gate that runs before *every* release: bandit, pip-audit, the hardening checklist. Keep using that every time.
- **`timermeet-security-audit`** (this skill) = a slower, deliberately adversarial hunt for vulnerabilities the routine gate isn't designed to catch on its own -- logic-level trust-boundary issues, injection via data fields, build/supply-chain risk, OS-integration surface. Use this when the user explicitly asks for a vulnerability search / worries about "being hacked" / wants a real audit, or before a major version bump, not on every patch release.

## Threat model (don't invent threats outside this)

TimerMeet is a **local, single-user, no-server Windows desktop app** -- there is no listening port, no remote attacker, no multi-tenant data, no auth. The only externally-influenceable input is:
- `data/meetings.json`/`data/settings.json`, which can arrive edited by another PC/person via OneDrive sync, or be hand-edited/corrupted.
- A Teams URL typed into the form (or synced in from another PC).
- The PyInstaller-built `.exe` itself (build/supply-chain integrity, not signed -- see `SECURITY.md`).

Don't spend audit effort on SQL injection, CSRF, auth bypass, or other threats that require a server/network/multi-tenant model this app doesn't have.

## How to run the audit

This is a multi-perspective, adversarially-verified process -- run it as a `Workflow` (preferred, when workflow orchestration is available/authorized in the session) or as an equivalent manual sequence of parallel `Agent` calls if it isn't. Either way, the shape is the same:

1. **Find** -- run 5 independent finder passes in parallel, one per dimension (see `references/dimensions.md` for the exact prompt template for each -- reuse them verbatim, updating only the specific recent changes/context line at the top):
   - URLs and data-field trust boundary (`is_http_url()` scheme allow-list, `soundProfile`/other fields reaching a file path or native call unvalidated, notification text reaching a native API unescaped).
   - File I/O and persistence (atomic-write races, quarantine-on-corrupt-JSON robustness, JSON-bomb/resource-exhaustion handling, lock-file abuse, file permissions).
   - Dependencies and build/supply-chain (real `pip-audit` output, pin looseness, PyInstaller `--onefile` extraction/DLL-side-loading risk for the pinned version, unsigned-exe disclosure adequacy, CI/CD workflow trust if any exists).
   - Code-execution sweep (full-repo grep for `eval`/`exec`/`pickle`/`subprocess`/`os.system`, independent judgment of every existing `# nosec` suppression, MCI command-string construction in `audio.py`, Pillow/tray-icon image loading).
   - OS integration surface (pystray thread-safety re: Tkinter, plyer notification robustness, any local IPC/socket/protocol-handler surface, privilege escalation, alarm-spoofing by another local process).
   Each finder must actually run the tools it references (`bandit`, `pip-audit`, `grep`) itself and cite real file/line evidence -- never report a finding it hasn't personally verified by reading the code.
2. **Verify** -- for every candidate finding, run 2 independent adversarial skeptics in parallel, each trying to REFUTE the finding by reading the actual code themselves (not trusting the finder's claim), each defaulting to "not real" if they can't personally confirm it. A finding is **confirmed** only if both skeptics agree it's real; **disputed** if they split; otherwise **refuted**.
3. **Report** confirmed findings first (with file/line, concrete attack scenario, severity), then disputed ones (flag the disagreement, don't silently pick a side), then a short "checked, nothing found" summary per dimension so the user knows the audit's actual coverage, not just its hits.
4. **Fix confirmed findings** the same way any other bug gets fixed in this project: root-cause, minimal targeted change, re-run the full test suite + bandit/pip-audit, then follow the normal version-bump/commit/release process (`timermeet-stable-fix-release` skill) -- a security fix is still a fix, don't skip this project's usual rigor for it.

## Guardrails

- Every finder and every verifier must actually execute/read something real (run the command, open the file) -- a finding that's just plausible-sounding reasoning without a cited file/line and a concrete "what data would need to contain X for Y to happen" scenario should not survive the Find phase, and should never survive Verify.
- Don't manufacture severity -- most findings in a codebase this size and threat model will legitimately be low/informational or "nothing found." That's a valid, useful outcome; don't inflate to justify the audit's cost.
- This is read-only investigation until the Report step. Don't fix anything mid-audit -- finish finding and verifying first, then fix as a separate, deliberate step so the fix itself gets the same rigor (tests, review) as any other change.

## References

- `references/dimensions.md` -- the 5 reusable finder prompt templates and the adversarial-verifier prompt template, so the audit doesn't need to be re-designed from scratch each time.
