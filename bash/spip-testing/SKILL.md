---
name: spip-testing
description: Guides automated testing of SPIP plugins and squelettes using PHPUnit — the standard test tool for SPIP. Covers the full self-contained setup (composer, spip-cli), unit tests with lightweight mocks, and integration tests against a real SPIP instance. Written for SPIP 4.x; on a SPIP 5.0 project the integration bootstrap and test install change (see the SPIP 5.0 section). Use whenever the user wants to test, verify, or validate a SPIP plugin or squelette — even if they don't mention PHPUnit — including questions like "how do I test my plugin", "I want to make sure my filtre works", or "how do I write tests for my autorisation / CVT form / #BALISE".
---

# SPIP testing

PHPUnit is the standard test tool for SPIP plugins and squelettes, used by SPIP core and the official plugin ecosystem.

## SPIP 5.0

This skill describes SPIP 4.x. Check the version first and name the marker you relied on. A site is 5.0 if **any**
of: `ecrire/src/SpipVersion.php` declares `VERSION = '5.…'`, `bin/spip` exists, `vendor/spip/framework/` exists,
plugins live in `plugins-dist/spip/`. A plugin targets 5.0 if its `paquet.xml` `compatibilite` reaches 5.x or
its `composer.json` requires `spip/framework`.

- The integration bootstrap of this skill dies on 5.0 (`Undefined constant "_FILE_OPTIONS"`). Fix the existing
  `tests/bootstrap_integration.php`: boot the Kernel between `vendor/autoload.php` and `ecrire/inc_version.php`, then
  push a `Request` (without it `Spip::setInput()` and `set_request()` throw a `LogicException`):

  ```php
  $spip5 = is_dir($spipRoot . '/vendor/spip/framework');
  if ($spip5) {
      \SpipLeague\Component\Kernel\Kernel::boot();
  }
  require_once $spipRoot . '/ecrire/inc_version.php';
  if ($spip5 && \Spip::service('request_stack')->getCurrentRequest() === null) {
      \Spip::service('request_stack')->push(\Symfony\Component\HttpFoundation\Request::create('/'));
  }
  ```

  Keep the `$spip5` guard for a plugin tested on 4.4 **and** 5.0. Never guard with `class_exists(Kernel::class)`:
  4.4 has that class, with a private `boot()`.
- Form inputs: in 5.0 `_request()` / `Spip::input()` never see `$_POST` / `$_GET` set by a test. Plugin for 5.0
  only: `Spip::setInput('email', $v)` (`null` clears it); `set_request()` is deprecated in 5.0. Plugin for 4.4
  **and** 5.0: `set_request('email', $v)`, the only API in both.
- The test SPIP: spip-cli (`core:telecharger`, `plugins:activer`, …) is a 4.x tool, and 5.0's `bin/spip` has no
  install or plugin-activation command. A 5.0 test site comes from `composer create-project
  --repository=https://get.spip.net/composer spip/spip <dir> 5.0.x-dev` (PHP 8.4); say that the 4.4 install script
  must be replaced, never point it at another `-b` branch.

Details: `spip-migration-5` (`references/audit-outils.md`: `bin/spip` commands); installing the 5.0 test site
(web installer, `composer create-project`): `spip5-instance` (`references/prerequis.md`).

## Quick-start

```bash
composer install            # install PHPUnit, spip/tests, spip/spip-cli
composer tests-unit         # unit tests — no SPIP needed, uses mocked stubs
composer install-spip-test  # download + install SPIP into vendor/spip/spip/
composer tests-integration  # integration tests — real SPIP + SQLite3
```

---

## Two test tiers

| Tier | Directory | Bootstrap | Needs SPIP? |
|---|---|---|---|
| **Unit** | `tests/unit/` | `tests/bootstrap.php` (mocks) | No — PHP only |
| **Integration** | `tests/integration/` | `tests/bootstrap_integration.php` | Yes — `vendor/spip/spip/` |

## Two base classes

| Use case | Class |
|---|---|
| PHP functions (filtre, autorisation, inc…) | `PHPUnit\Framework\TestCase` |
| Squelettes, `#BALISE`, `\|filtre` in templates | `Spip\Test\SquelettesTestCase` |

`SquelettesTestCase` requires the integration tier (real SPIP loaded).

---

## Decision tree — I want to…

| Goal | Read |
|---|---|
| Set up composer.json, phpunit.xml, scripts from scratch | `references/howto-test.md` §Setup |
| Write a unit test (filtre, autorisation — no real SPIP) | `references/howto-test.md` §Unit tests |
| Write a mock bootstrap (`tests/bootstrap.php`) | `references/howto-test.md` §Unit bootstrap |
| Write an integration test (SQL, CVT, pipelines) | `references/howto-test.md` §Integration tests |
| Configure `scripts/install-spip-test.sh` | `references/howto-test.md` §install-spip-test.sh template |
| Test a squelette or `#BALISE` (SquelettesTestCase) | `references/howto-test.md` §Testing squelettes |
| Verify the plugin is active in the integration environment | `references/howto-test.md` §Verify the plugin is active |
| Test a BOUCLE loop with DB fixtures (ordering, doublons, pagination) | `references/squelettes-test.md` |
| Test `charger()`, `verifier()`, or `traiter()` directly | `references/formulaires-cvt-test.md` |
| Test `#FORMULAIRE_{nom}` rendering or error display | `references/formulaires-cvt-test.md` §Testing the rendered template |
