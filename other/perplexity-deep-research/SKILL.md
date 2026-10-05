---
name: perplexity_deep_research
description: Режим Deep Research через Perplexity MCP для широких и важных multi-source вопросов, когда допустимы высокий расход и более долгое выполнение.
compatibility:
  runtimes:
    - codex
    - claude_code
    - cursor
    - windsurf
metadata:
  category: research
  capability_taxonomy_ids:
    - cap.research.deep_research
    - cap.research.comparative_analysis
  distribution_scope: internal
  invocation_strategy: explicit
  version: v0.1
  source_of_truth: https://github.com/nicshik/perplexity-mcp-skills
---

# Perplexity Deep Research

Используй этот skill, когда задаче явно нужен Deep Research mode по многим источникам через Perplexity MCP и больший расход допустим.

Skill вызывается явно, потому что `perplexity_research` заметно дороже Search only и Pro Search modes.

Реальный снимок биллинга после тестов навыков стоил `$2.52`; основная часть пришлась на `sonar-deep-research`: 478 195 reasoning tokens (`$1.43`), 117 поисковых запросов (`$0.59`), 67 825 citation tokens (`$0.14`) и 15 158 output tokens (`$0.12`).

## Preconditions

- MCP-сервер `perplexity` установлен и включен в Codex или Windsurf.
- `PERPLEXITY_API_KEY` уже задан в окружении MCP-сервера.

## Non-Negotiable Rules

- Используй только MCP path `perplexity_research`.
- Не заменяй его незаметно на `perplexity_search`, `perplexity_ask` или `perplexity_reason`.
- Даже в глубоком режиме держи границы вопроса узкими.
- Отдавай приоритет практическому выводу, а не общим формулировкам.

## Default Flow

1. Убедись, что вопрос действительно требует Deep Research mode.
2. Сузь область: рынок, набор конкурентов, период, документы или конкретный предмет сравнения.
3. Запусти `perplexity_research`.
4. Верни короткий вывод с самыми сильными ссылками.
5. Если пользователю были нужны только ссылки или короткий sourced answer, предложи в следующий раз `$perplexity_search_only` или `$perplexity-pro-search`.

## Recommended Prompt Shape

- `Используй $perplexity_deep_research для глубокого исследования "<question>". Сфокусируйся на практических выводах и пиши кратко.`

## References

- `references/prompt_recipes.md`
