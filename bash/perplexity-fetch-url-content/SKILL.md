---
name: perplexity-fetch-url-content
description: Режим Fetch URL через встроенный Perplexity Sonar Pro tool `fetch_url_content`. Использовать, когда нужно прочитать, извлечь или проверить одну или несколько страниц глубже поисковых сниппетов.
compatibility:
  runtimes:
    - codex
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.web_search
    - cap.research.extraction
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: https://github.com/nicshik/perplexity-mcp-skills
---

# Perplexity Fetch URL Content

Используй этот skill, когда пользователь явно хочет Fetch URL mode для одного или нескольких известных URL через встроенную возможность Sonar Pro `fetch_url_content`.

В документации Perplexity `fetch_url_content` описан как встроенный Pro Search tool, который модель включает сама. Это не отдельный endpoint и не пользовательский MCP tool. Поэтому script отправляет строгий запрос в Sonar Pro, а затем проверяет `reasoning_steps`, чтобы понять, какие URL действительно были прочитаны.

## Preconditions

- `PERPLEXITY_API_KEY` доступен в окружении shell, в `CODEX_HOME/config.toml` / `~/.codex/config.toml` или в `~/.codeium/windsurf/mcp_config.json`.
- Разрешен доступ к `https://api.perplexity.ai`.
- Если песочница блокирует сеть, повтори скрипт с повышенным доступом. Не заменяй его обычным веб-поиском.

## Non-Negotiable Rules

- Используй local script `scripts/fetch_url_content.py`.
- Сохраняй `stream=true`, `stream_mode="concise"` и `web_search_options.search_type="pro"`.
- Не утверждай, что API возвращает полный сырой HTML или гарантирует дословную выгрузку всей страницы.
- Используй `--json`, когда Codex должен проверить `fetched_urls`, `missing_requested_urls` или расход.
- Используй `--require-fetch`, когда важно подтвердить чтение каждого URL.

## Default Flow

1. Передай целевые URL прямо в `scripts/fetch_url_content.py`.
2. По умолчанию используй `--mode max-text`, если пользователь не просит точный ответ или краткую сводку.
3. Добавь `--question "<question>"`, когда пользователь задает конкретный вопрос по страницам.
4. Используй `--json` для дальнейшей обработки и проверки.
5. Ясно сообщай о `missing_requested_urls`. Не подразумевай, что эти страницы были прочитаны.

## Recommended Commands

```bash
python3 scripts/fetch_url_content.py https://docs.perplexity.ai/docs/sonar/pro-search/tools --json
python3 scripts/fetch_url_content.py https://example.com/report.pdf --question "Extract the methodology and key findings." --mode qa --json
python3 scripts/fetch_url_content.py https://example.com/a https://example.com/b --mode summary --require-fetch
```

## Output Shape

- Обычный вывод показывает извлеченный ответ, проверку URL, источники и расход.
- `--json` возвращает `content`, `search_results`, `usage`, `reasoning_steps`, `fetched_urls`, `missing_requested_urls` и `payload`.
- `--dry-run` печатает запрос и выходит без API-ключа.

## References

- `references/prompt_recipes.md`
