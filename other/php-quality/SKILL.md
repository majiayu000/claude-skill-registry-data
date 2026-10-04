---
name: php-quality
description: PHP品質チェック。PHPStan/Pint/PHPUnit実行時に使用。「PHPの品質チェック」「PHPの静的解析」で起動。Do NOT use for 他言語の静的解析（→ python-quality / js-quality / ts-quality）。
allowed-tools: Bash, Read, Grep, Glob
---

## Tools
analysis: `./vendor/bin/phpstan analyse --level=8` | format: `./vendor/bin/pint` | test: `./vendor/bin/phpunit` / `pest` / `artisan test`

## Standards

| 項目 | 目標 |
|------|------|
| PHPStan Level | 8 |
| カバレッジ | 90%+ |
| Pint | エラー0 |

## Reference
- [reference.md](reference.md)
