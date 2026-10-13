---
name: code-review-php
description: >
  Security review of PHP code — dangerous sinks and framework pitfalls (Laravel/Symfony/WordPress).
  Load when reviewing a PHP codebase/PR, on .php source in scope, or "review this PHP". Signals:
  composer.json, index.php, Laravel/Symfony/WP, unserialize, include/require with variables, mysqli/PDO.
domain: code-review
type: reference
stability: learning
modes: [bugbounty, defense, pentest]
severity: info
cwe: [CWE-94, CWE-89, CWE-78, CWE-98, CWE-502]
tools: [semgrep, psalm, phpstan, progpilot, ripgrep]
schema_version: 1
---

# PHP source review

## When it applies
Reviewing PHP source (a repo, a PR, or a leaked webroot). PHP's defaults and dynamic features make
several classes easy to introduce, so a grep-then-trace pass finds most of them fast.

## Why it works
Many PHP sinks execute or include whatever string they're given, and loose typing turns comparison
and casting into logic bugs. Tracing each sink back to a request source (`$_GET/$_POST/$_REQUEST/
$_COOKIE/$_SERVER`, `php://input`) tells you which are actually reachable.

## Sinks & patterns (grep, then trace to user input)
- **Code exec**: `eval`, `assert`, `preg_replace` with `/e`, `create_function`, `call_user_func(_array)`.
- **Command exec**: `system`, `exec`, `shell_exec`, `passthru`, `proc_open`, `popen`, backticks.
- **File include (LFI/RFI)**: `include`/`require`(`_once`) with a variable; `allow_url_include`.
- **SQLi**: string-interpolated queries into `mysqli_query`/`PDO::query` (vs prepared statements).
- **Deserialization**: `unserialize()` on input (POP chains); `phar://` via file functions.
- **File / path**: `file_get_contents`, `fopen`, `readfile`, `move_uploaded_file` with user paths.
- **Other**: `extract()` on input (variable overwrite), `parse_str`, SSRF via `curl`/`file_get_contents`.

## Framework specifics
- **Laravel**: `DB::raw`/`whereRaw`, Blade `{!! !!}` (unescaped), mass assignment (`$guarded=[]`),
  `unserialize` in queues, `Storage` path traversal.
- **Symfony**: unsafe deserialization, Twig `|raw`, expression-language injection.
- **WordPress**: unsanitised `$wpdb->query`, missing nonce/cap checks, unsafe `add_query_arg`,
  unauthenticated AJAX/REST callbacks.

## Method
1. `rg` the sinks above; for each, trace the argument back to a request source.
2. Note type-juggling auth checks (`==` vs `===`, `strcmp` returning `0`/null) and loose casts.
3. Check upload handlers (extension/content-type allowlist, exec in upload dir).
4. Confirm exploitability with the matching runtime skill (`web-command-injection`,
   `web-deserialization`, `web-lfi-path-traversal`, `web-sqli`).

## Gotchas
- A sink is only a bug if input reaches it — don't report unreachable `eval`.
- WordPress plugins: unauthenticated `wp_ajax_nopriv_*` and REST endpoints are the high-value paths.
- `==` type juggling (`"0e123"=="0e456"`) still breaks weak hash/token comparisons.

## References
OWASP PHP security; RIPS/progpilot sink catalogue; PHP `unserialize` POP-chain research (PHentication).
