---
name: ask-any
description: "ПОРУЧИТЬ РАБОТУ ЛЮБОЙ ЖИВОЙ LLM, а не только Claude: задание уходит ОДНОВРЕМЕННО на codex + grok + gemini + claude, побеждает первая ответившая. Триггеры: «/ask-any», «/любой», «/раздай», «спроси всех», «спроси кого угодно», «дай это другой ллм», «claude кончился», «бак пуст», «спроси параллельно», «у кого спросить», «ask any», «race the rails»"
version: 1.0.0
---

# ask-any — работу делает тот, кто жив

## Зачем

06.08.2026 замерено на хабе: бак подписки Claude исчерпан до 08.08, **все** LLM-рутины стоят.
При этом Codex ответил за 8 с, Grok за 13 с, Gemini за 4 с. Три живых вендора простаивали,
потому что все рельсы к ним были построены как «вторая пара глаз» с обязательным тегом вердикта.
Дверь была, но открывалась только внутрь ревью.

## Как звать

```bash
python ~/.claude/scripts/llm_ask.py --prompt "задание"
```

Дефолт `--mode race`: все рельсы стартуют **одновременно**, побеждает первая ответившая. Мёртвый
вендор просто не приходит первым, и его таймаут никого не задерживает.

| режим | что делает | когда брать |
|---|---|---|
| `race` (дефолт) | все разом, побеждает первый успех | обычная работа, нужен ответ быстро |
| `first` | по очереди, останавливается на первом живом | когда бережём чужие квоты |
| `all` | все разом, собираем ВСЕ ответы с подписями | сравнить мнения, спорный вопрос |

Ещё ручки: `--rails codex,grok` (сузить круг), `--prompt-file p.txt`, `--timeout 180`, `--list`.

Замер 06.08: гонка 13,9 с против очереди 16,4 с на живом хабе; в режиме `all` три мнения
приходят за 13 с вместо 25 с последовательно.

## ⛔ Две породы рельс — главное, что нельзя путать

| рельса | что умеет | когда брать |
|---|---|---|
| `claude` `codex` `grok` `gemini` | только ГОВОРИТЬ | суждение, синтез, черновик, разбор |
| `codex-agent` | ДЕЛАТЬ: файлы, команды | работа, которую рутина делала бы сама |

Grok и Gemini физически не могут действовать: они зовутся с выключенными инструментами.
Отдашь им действие — получишь прозу вместо дела, и потребитель примет её за результат
(память `green-exit-on-spent-bucket`).

У агента рабочая папка = `LLM_ASK_CWD`, песочница ограничена ею. Пустой stdout при коде 0 у
агента = **работа сделана**: у него результат это побочный эффект, а не текст.

Tier-2, гейт [коллега] и правда в цифрах не ослаблены: сменился исполнитель, не правила.

## Для рутин (раскатано 06.08 на 24 ночные рутины хаба)

```
python claude_run.py <timeout> --extfallback codex-agent --stdin <файл> -- claude -p ...
```

Рутина сперва идёт своим путём; если бак пуст, задание уезжает Codex-агенту и рутина реально
доделывает работу. Рабочую папку `claude_run` подставляет сам (волт), потому что задача из
планировщика стартует в `system32`.

Доказано сквозным прогоном 06.08: бак Claude пуст → Codex выполнил инструкцию рутины → файл
на диске → rc=0.

## Что ломается и как понять

| в stderr | что это | лечение |
|---|---|---|
| `бак подписки исчерпан` | у вендора кончилась квота | ничего, другие подхватят |
| `рельса разлогинена` | сессия вендора умерла | `grok login --device-auth` / `claude setup-token` |
| `CLI не на PATH` | вендор не стоит на этом узле | поставить или убрать из `--rails` |
| `ВСЕ рельсы мимо` | все двери закрыты | причина названа поимённо, читать её |

Главный риск — **отписка, принятая за ответ**: вендоры печатают «я разлогинен» и выходят НУЛЁМ.
Сеть на такие фразы стоит в одной точке и узкая по длине (отписка это весь вывод, а не фраза
внутри работы), иначе законный ответ про лимиты выбрасывался бы как смерть рельсы.

## Проверки

- регресс: `python ~/.claude/scripts/_test_llm_ask.py` (20 проверок, краснеет мутантом)
- паспорт: волт `00-System\LLM-Ask-Passport.md`
- счётчик: `_shared/skill_usage_log.py`, `kind=part`, имя `llm_ask:<рельса>`

Канон: память `other-llm-rails-were-review-only`, `green-exit-on-spent-bucket`,
CLAUDE.md §6.3 «выгребай лимиты».


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
