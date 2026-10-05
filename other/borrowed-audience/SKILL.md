---
name: borrowed-audience
description: "Добыть ВНЕШНИЕ ССЫЛКИ на наши репо через чужие курируемые поверхности — awesome-lists, каталоги тулов, вендорские showcase. Триггеры “/borrowed-audience“, “/ba“, “заёмная аудитория“, “куда положить наши репо“, “добудь внешние ссылки“, “подай в awesome-листы“, “найди курируемые списки“, “где нас разместить“, “borrowed audience“, “get external links“"
version: 1.0.0
---

Добываем **внешние ссылки**, а не производим артефакты. Отчёт Антону по-русски, в конце блок «🧒 Простыми словами» ([[eli5-always]]).

## Зачем этот скилл существует

Замер 27.07.2026: 9 уникальных заходов на флагман за неделю, **100% трафика из нашего же Facebook**, внешних человеческих ссылок ноль, форков ноль. Артефакты есть — аудитории нет. Курируемые списки дают чужую аудиторию бесплатно.

Второй замер, 28.07.2026: из 22 наших PR наружу **21 висел открытым**, включая 7 почти одинаковых PR по одному рецепту, разосланных веером по вендорам 24.07. Массовая одинаковая подача не работает и портит репутацию. Этот скилл существует, чтобы так больше не делать.

## Железные границы (нарушение = провал, а не «оптимизация»)

- **Один список — одна запись.** Не пихать все 4 репо в один список.
- **Один тул — тот, что подходит ЛУЧШЕ ВСЕГО.** Не веером.
- **Никаких одинаковых PR.** Каждое тело PR отвечает на критерии ИМЕННО этого CONTRIBUTING.
- **Замер ДО подачи, всегда** ([[cold-pr-into-silent-queue]]). Холодный PR в глухую очередь = шум.
- **Просят issue-first — значит issue-first.** Запрещают PR — значит PR не открываем.
- **Не пере-подавать** в список, который уже отказал.
- Отправка PR — сама, по мандату [[github-publish-autonomous]] + §4.7 (GitHub-коммуникация без «+» Антона и без гейта [коллега]). Юридическое подписание (CLA/DCO) — Tier-2, аск Антону.

## Движки (0 LLM, 0 токенов на замер — только `gh` + арифметика)

| Скрипт | Что делает |
|---|---|
| `~/.claude/scripts/list_discover.py` | НАХОДИТ кандидатов: веер поисков → дедуп → предфильтр (звёзды, свежесть push, не архив/форк) |
| `~/.claude/scripts/list_liveness.py` | МЕРИТ живость: мержи от ЛЮДЕЙ за 90д, число разных авторов, медиана часов до мержа, очередь, CONTRIBUTING → вердикт 🟢/🟡/🔴 |
| `~/.claude/scripts/issue_match.py` | Сосед: замер ОДНОГО репо под PR с кодом + поиск живого issue |

## Токен — отдельная грабля, читать до старта

Fine-grained PAT **не умеет форкать чужие репо** (403 «Resource not accessible by personal access token»). Нужен **classic** PAT со скоупом `public_repo`:
```
export GH_TOKEN=$(grep '^GITHUB_PAT_PUBLIC_PR=' "$USERPROFILE/!CLAUDE-HP17 May26/secrets/github.env" | cut -d= -f2- | tr -d '\r')
```
Протух → добывать заново, порядок в памяти [[github-pat-cannot-fork]]. `gh auth login --web` в этой среде НЕ проходит (вкладки MCP всегда `hidden`, кнопка Authorize не разблокируется) — не тратить время.

---

# Ритуал: 6 шагов

## Шаг 0. RECALL — не подавать дважды
```
gh search prs --author tonydzi --json repository,number,title,state,createdAt --limit 100
```
Плюс память [[awesome-list-liveness-map]] — там карта уже замеренных, включая кладбища, куда ходить не надо. Уже есть открытый PR в этом списке → **второй туда не шлём**, пока первый не разрешился.

## Шаг 1. НАЙТИ поверхности
```
python ~/.claude/scripts/list_discover.py --seen <прошлый liveness_out.json> --min-stars 40 --max-push-days 45
```
⚠️ **Порог звёзд держать НИЗКИМ (40, не 150).** Замер доказал обратную корреляцию: большие списки чаще кладбища, маленькие живые мержат за сутки.

Keyword-поиск и topic-поиск дают **разную** выдачу — гнать оба:
```
gh search repos --topic awesome-list --topic <llm|ai-agents|rag|llmops|ai-safety|agentic-ai|llm-evaluation> --sort updated --limit 12
```
Отсеивать руками: авто-генерируемые «radar/tracker/live» репо (бот коммитит сам себе, PR не принимает) и явно чужие темы.

## Шаг 2. ЗАМЕРИТЬ живость — цифрами, до единой буквы подачи
```
python ~/.claude/scripts/list_liveness.py <repo> [<repo> ...]
```
Что читать в выводе:
- `merged_90d` — мержи **от людей** за 90 дней. 0 → 🔴, не входим.
- `distinct_outside_authors_90d` — **сколько РАЗНЫХ чужих авторов**. Это главная цифра: 54 мержа от 1 автора = мейнтейнер мержит сам себя, дверь для чужого закрыта; 12 мержей от 12 авторов = дверь открыта настежь.
- `median_hrs_to_merge` — сколько ждать.
- `open_oldest_age_d` — старейший висящий PR. >400д = там умирают.
- `contributing` — есть ли писаные правила.

Две грабли, уже зашитые в движок, но знать надо:
1. **Ботов не считаем.** Авто-обновления звёзд от `github-actions` раздували «живость» вчетверо.
2. **Медиана возраста берётся по новейшим И старейшим.** По одним новейшим врёт в разы при большом бэклоге.

## Шаг 3. ПРОЧИТАТЬ правила — это не формальность
```
gh api repos/<repo>/contents/CONTRIBUTING.md --jq '.content' | base64 -d
```
Ищем: формат строки · нужную секцию · алфавит или дату · запрет эмодзи · требования к лицензии · **не запрещены ли PR вообще**.

⚠️ Живой пример, почему это делается до, а не после: `hesreallyhim/awesome-claude-code` (51k★) **запрещает PR** — только issue-форма через веб-UI, и её замер: **262 заявки → одобрено 3 (~1%)**. Выглядел главным призом, оказался глухой очередью.

## Шаг 4. РАНЖИРОВАТЬ и НАЗНАЧИТЬ
Порядок = живость × аудитория × точность попадания. Дальше каждому списку — **один** наш тул, тот, что реально в его тему. Не наоборот («куда бы засунуть claude-consensus»), а от списка: «какая наша вещь тут уместна, и уместна ли вообще». Ни одна не уместна → **список пропускаем**, это нормальный исход.

## Шаг 5. ПОДАТЬ
⛔ **ИМЕНА ФОРКОВ СТАЛКИВАЮТСЯ.** Грабля 29.07: `topoteretes/awesome-ai-memory` и `IAAR-Shanghai/Awesome-AI-Memory` дают форк с одним именем (GitHub не различает регистр). Форк молча не создался, а `git clone` вытянул НАШ СТАРЫЙ форк другого репо — и правка чуть не поехала в чужой README. **Всегда проверять `.full_name` в ответе форка и после клона убеждаться, что якорь в файле есть.** При коллизии GitHub сам даёт суффикс (`awesome-ai-memory-1`) — клонировать надо ИМЕННО его, а не угаданное имя.

```
gh api -X POST repos/<upstream>/forks --jq '.full_name'   # ← прочитать РЕАЛЬНОЕ имя
git clone --depth 1 https://x-access-token:${GH_TOKEN}@github.com/tonydzi/<fork>.git
git checkout -b add-<тул>
# правка строго в формате репо
git commit && git push -u origin add-<тул>
gh pr create --repo <upstream> --base main --head tonydzi:<ветка> --title ... --body ...
```
До коммита — **дедуп внутри README** (`grep -i` по имени тула и по нашему owner) и глазами diff: одна строка должна быть одной строкой.

⛔ **ПЕРЕНОСЫ СТРОК — вставлять только через `~/.claude/scripts/list_insert.py`.** Грабля 29.07: обычный `io.open(p, encoding='utf-8')` при чтении схлопывает CRLF в LF, и файл переписывается целиком — diff вышел **+211 / −210** вместо +1. Такой PR отбраковывают не читая. Хелпер читает и пишет с `newline=''` и сам подставляет родной EOL файла. **Проверка обязательна: `git diff --stat` должен показать ровно столько вставок, сколько строк добавили, и НОЛЬ удалений.** Не сошлось → откатить и переделать, не пушить.

Тело PR обязано содержать:
1. Куда положили и **почему именно туда**.
2. Что это, нейтрально, без продажи.
3. **Ответ на критерии ИМЕННО этого CONTRIBUTING** (лицензия, OSS-substance, поддерживаемость, отсутствие платного бэкенда).
4. Подтверждение, что дубль проверен.
5. Предложение подвинуть в другую секцию, если мейнтейнер видит иначе.

⛔ **Цифры в теле PR — только доказанные.** Списки вроде `awesome-rag-production` требуют источник + дату + тег на любое число. Нет источника — не пишем число ([[fake-it-courage-not-fake-numbers]], [[prichina-kak-claim]]).

⚠️ **Фактуру о СВОЁМ репо тоже проверять по репо, а не по памяти.** Живой прокол 28.07: чуть не отправил выдуманный список из 8 доменов LEASH — настоящие лежали в `docs/leash-8.md`.

## Шаг 6. СТОРОЖ
`git push` ≠ ссылка добыта. Ссылка добыта только на мерже. Ставим одноразовую проверку через 3 дня:
```
mcp__scheduled-tasks__create_scheduled_task, fireAt = +3 дня, 05:30 Лиссабона (ночное окно §4.6)
```
Промпт задачи: замерить каждый PR → разложить на смержен / ответил мейнтейнер / закрыт / тишина. **Ответил мейнтейнер = отвечаем САМИ и сразу** (§4.7, молчание в живом треде = провал). Тишина <14 дней — не пинговать, это спам.

---

## Что считаем результатом

Метрика — **не отправленные PR, а смерженные записи и заходы не из нашего Facebook.** Отчёт таблицей: список · аудитория · живость · что подали · статус. Плюс честная строка «ссылок добыто N из M». Ноль — говорим ноль.

## Известный риск, который замер не лечит

У наших репо 0–2 звезды. README самого `agent-leash` признаёт: каталоги обычно ждут ~10 звёзд социального доказательства. Часть отказов будет **по этой причине**, а не из-за плохого замера. Это не повод не подавать — это повод не удивляться и не переписывать замер задним числом.

## Канон
[[cold-pr-into-silent-queue]] (замер очереди — первый шаг) · [[awesome-list-liveness-map]] (карта замеренного) · [[github-pat-cannot-fork]] (токен) · [[github-communication-autonomous]] §4.7 · [[github-publish-autonomous]] · [[ship-github-no-plus-wait]] · Библия `reglament-zametnost-v-top-10-llm-issue-matching` · миссия `04-Projects\mission-llm-hire-weekly-plan.md` лейн W3.

## Анти-слоп гейт (anton 14.08)
Любой ИИ-написанный текст наружу из этого скилла перед отправкой - финальный проход `/ai-slop` (ban-лист + ритм). Исключения ровно три: текст с плашкой Майкрофта (§3.3) · машиночитаемое (GitHub/техдока/dev-log/journey-machine) · текст, написанный Антоном руками. Канон: `reglament-posty-ot-lica-antona-tolko-cherez-ai-slop`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
