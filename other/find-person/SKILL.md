---
name: find-person
description: "Найти человека и его каналы связи по нашим ЖЕ данным: архив ТГ 16.7 млн сообщений, CRM, книга чатов, почта, досье. Триггеры: /find-person, найди хэндл, как с ним связаться, найди контакт, где он есть, кто это, найди телеграм <имя>, найди человека. НЕ путать: /find = поиск по волту; /triage = кого касаться; этот = где у человека дверь и что мы о нём уже знаем."
version: 1.0.0
consumer: "Антон (ТГ-хэндлы лидов) · рутина enrichment цели №1 (handle->GitHub) · /triage перед касанием · /fa перед фоллоуапом"
---

# /find-person — где у человека дверь

> 🧒 Антону в конце: блок «Простыми словами».

Своя дверь под задачу «найти канал связи с человеком», построенная на НАШИХ данных.
Повод (11.09.2026): пак `osint-skills` даёт 29 скиллов, но десять самых нужных —
`find-anyone`, `hunt-a-handle`, `x-ray-a-company`, `whose-number-is-this` — автор закрыл
флагом `disable-model-invocation`. Их зовёт только человек, набрав слэш-команду; робот
не может, и запрет обходить обозначен прямо. Поэтому мы строим СВОЮ дверь на своём
корпусе, а их пак остаётся справочником по внешним источникам.

## Почему наша дверь сильнее чужой на ПЕРВОМ шаге

У нас лежит то, чего у публичного OSINT нет: 16 765 326 сообщений и 115 341 диалог в
архиве Telegram, 70 946 человек в CRM с рангом теплоты, книга чатов на ~99 тысяч
разговоров и досье. Человек, которого ищем, чаще всего УЖЕ у нас — просто под другим
именем, в другом аккаунте или в групповом чате.

Чужие публичные источники нужны только тогда, когда свои дали ноль. Порядок обратный
привычному: сначала дом, потом улица.

## Шаги

**0. Область и право.** Назови, кого ищем и ЗАЧЕМ одной строкой. Разрешено: люди из
нашей CRM, кто нам писал, публичные профессиональные профили. ⛔ Запрещено: частные лица
без деловой связи с нами, сбор адресов и родственников, обход приватности площадок.
Сомнение — спроси Антона, не угадывай.

**1. Свои базы, по убыванию дешевизны (0 токенов).** Живые файлы лежат в подпапках
`_imports`, корневые тёзки нулевые — перед выводом «пусто» проверь РАЗМЕР файла
(`consumers-of-a-conclusion-need-two-instruments`):
- `dialogs/tg_archive.db` — переписки и группы, ищи по имени, фамилии, latin-транслиту;
- `dm_messages.db` — личка четырёх наших аккаунтов;
- CRM (`leads.db`, досье) — карточка, теплота, источник знакомства;
- книга чатов `search_catalog.db` — где имя всплывало в разговорах;
- `browser_history` — заходили ли мы на его профиль.

**2. Транслит и ослышки.** Одно имя живёт в четырёх написаниях: кириллица, латиница,
уменьшительное, ник. Ищи все; «[человек]» = «[человек]» = «Женя» = «[человек]».

**3. Наши публичные соседи.** GitHub-профиль по хэндлу, наши общие группы, подписи в
письмах, участники общих созвонов (транскрипты Granola/Fireflies).

**4. Только теперь наружу.** Публичные профессиональные источники — GitHub, личный сайт,
профиль на площадке, где он сам оставил контакт. Справочник методов по внешним
источникам: `~/.claude/packs/osint-skills/skills/*/SKILL.md` — ЧИТАЕМ как документацию,
их скиллы НЕ вызываем.

**5. Вердикт с провенансом.** По каждому найденному каналу: что нашли · где именно
(файл/таблица/ссылка) · дата последнего касания · уверенность. Не нашли — скажи «не
нашёл, искал там-то», а не «этого нет» (`ask-the-tool-before-declaring-impossible`).

**6. В CRM.** Найденный канал дописывается в карточку человека со всеми семью полями
провенанса (§9.9). Найти и не записать = не найти.

## Границы

⛔ Отправка сообщения найденному человеку — отдельное действие по своим правилам
(`/triage`, `/fa`, гейт Tier-2 на холодное). Эта дверь только НАХОДИТ.
⛔ Результат не уезжает наружу и не попадает в публичный контент.

## Связано
Стенд чужих паков: `~/.claude/scripts/packs_bench.py` · счётчик вызовов:
`_shared/skill_usage_log.py` · память `foreign-skill-pack-install-gotchas`,
`engineer-acquisition-enrichment-not-scraping`, `crm-lead-full-provenance`.


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
