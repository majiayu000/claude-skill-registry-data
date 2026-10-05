---
name: pack
description: "📦 УПАКОВКА КОНТРИБЬЮШЕНА КАК ПРОДУКТА (декрет Антона 24.08.2026: «нам нужно всегда делать КАЧЕСТВЕННО... Триггеры: “/pack“, “/упакуй“, “упакуй как продукт“, “сделай качественно“, “package this properly“, а также АВТОМАТИЧЕСКИ из /share-fix Шаг 3 (перед созданием gist) и /release-slice (перед выкладкой)"
version: 1.0.0
---

# /pack — не сниппет, а продукт

**Зачем существует:** сниппет решает задачу автора; продукт решает задачу ЧУЖОГО человека,
который видит его впервые, не знает контекста и не будет спрашивать. Каждый наш артефакт
наружу — витрина лаборатории (Mission-2): по нему судят, брать ли нас всерьёз.
Эталон: workdir-sentry 24.08.2026 — v1 (сниппет: код + 2 строки) → v2 (продукт).

## Шаг 0 — что пакуем и для кого (30 секунд, письменно в чате)
Одной строкой: артефакт · чужой пользователь (кто он, что у него болит) · формат
(gist / repo / файл в тред). Если пользователь = «мы сами» → /pack не нужен, не наряжай ёлку.

## Шаг 1 — README = продукт (главная половина, порядок обязателен)
Чужой человек читает README, не код. Скелет — СТРОГО в этом порядке:
1. **Одно предложение жирным**: что это и какую боль снимает.
2. **Боль с УЗНАВАЕМЫМИ симптомами** — как жалуется страдалец своими словами
   («Claude ignores my CLAUDE.md», «my history disappeared»), не наша терминология.
3. **Цифры/замер** — почему боль реальна. ТОЛЬКО наши доказанные числа
   ([[fake-it-courage-not-fake-numbers]]); таблица лучше абзаца.
4. **Самодиагностика за 30 секунд** — как читателю понять, что это ЕГО болезнь
   (одна команда / куда посмотреть). Это самый конвертирующий блок.
5. **Как чинит** — механизм по-человечески + пример реального выхлопа (цитата warning-строки).
6. **Design choices / safety contract** — почему нам можно доверять в чужом hook-чейне:
   fail-open? zero deps? что НЕ делает?
7. **Install пошагово** — по ОС, копипастные блоки, с проверкой «как убедиться, что работает».
8. **FAQ** — 3-5 вопросов, которые задаст скептик (почему warn а не block? работает ли в X?).
9. **Атрибуция + лицензия**: «by Mycroft (synthetic cofounder) & Tony, Palo Alto AI Research
   Lab» + MIT. Раскрытие Майкрофта = §3.3.
9-бис. ⭐ ПОДПИСЬ И КОНТАКТЫ — НЕ «ГДЕ УМЕСТНО», А ВСЕГДА (anton 10.09, голосовая hub:6539).
   Пак = публичная поверхность, значит README/карточка несут **полный блок** (кто мы +
   `github.com/tonydzi` + WhatsApp + группа). Единственный источник текста:
   `$OBSIDIAN_VAULT/08-Templates/github-touch-signature.md` §Полный блок; карта поверхностей
   (что куда) = `$OBSIDIAN_VAULT/08-Templates/outbound-signature.md`. Прежняя формулировка
   «где уместно» была дырой: замер 10.09 — 94% наших GitHub-касаний ушли без ссылки на нас.
   ⚠️ Научная поверхность (arXiv/Zenodo/JOSS/CITATION.cff) = исключение: там
   `Anton Dziatkovskii (Tony Dzi)` + ORCID, без CTA.

## Шаг 2 — код = продукт
- **Докстринг-шапка**: WHY THIS EXISTS → WHAT IT DOES → SAFETY CONTRACT → USAGE → CONFIG.
  Человек должен понять файл, не читая тела.
- **Комментарии объясняют ЗАЧЕМ, не что**: у каждого неочевидного хода — причина, лучше с
  граблей («PowerShell 5.1 pipes prepend U+FEFF — this exact byte broke two of our tools»).
- **`--selftest` встроен**: встроенные кейсы, PASS/FAIL, exit 0/1 — читатель проверяет ДО
  установки. **`--check <вход>`** — сухой прогон одного случая руками, где применимо.
- **Ядро = чистая функция** (без I/O/env) — тестируемо и переносимо в чужой стек.
- **Zero dependencies, один файл** где возможно (АК-47); английский; generic-имена.

## Шаг 3 — гейт перед публикацией (все пункты, молча скипать нельзя)
- [ ] `--selftest` прогнан СЕЙЧАС, PASS (не «прогонял раньше»).
- [ ] Запуск с чистого листа: из пустой папки / без нашего конфига — падает вежливо, не трейсбеком.
- [ ] Leak-scan глазами: ни секретов, ни внутренних имён узлов/людей/путей, ни приватных цифр.
- [ ] Цифры в README = правда с источником; непроверенное помечено 🤔 прямо в тексте.
- [ ] После пуша — проверь, что ДОЕХАЛО (размеры/содержимое; грабля 24.08: `gh gist edit --add`
      молча НЕ обновил существующий файл, чинилось `gh api PATCH`).
- [ ] **Формат repo — прибором, не глазами** (только если пакуем в репозиторий):
      `python ~/.claude/scripts/repo_birth_kit.py --check <папка>` → exit 0. Красный
      называет поимённо: нет файла · скелет с TODO не дописан · файл не в git (push его
      не отправит). Замер 09.09.2026: 7 из 7 репо родились без CITATION.cff/FOR-ROBOTS.md.
- [ ] Формат по размеру: сниппет-масштаб → gist; растёт/ждём вклада → repo. Каталоги
      (awesome-list и т.п.) — их CONTRIBUTING читается ЦЕЛИКОМ, подача ровно по их формату.

## Шаг 4 — вердикт (строка в отчёт)
«📦 упаковано: <артефакт> · README 9/9 блоков · selftest PASS · leak-scan ✅ · формат <gist/repo>»
либо честное «📦 не дотянул: <чего не хватает>» — полуфабрикат наружу не выходит.
Дальше раздача = /share-fix (этот скилл НЕ решает, куда нести).

## ⭐ Чёрный юмор обязателен (anton 10.09.2026, голосом)

Любой текст, который этот скилл отправляет ЖИВОМУ человеку наружу, несёт чёрную самоиронию — ровный служебный тон = дефект, объяснять надо не шутку, а её отсутствие. Строку берёшь через `/mycroft-joke` (полка (д) банка + строки 56-62 под холодное касание), приёмка — `/taste-check` P36. ⛔ Не шутим ровно в трёх зонах, и они не про вкус: строго-научная публикация (arXiv/журнал/JOSS) · юр.обязательство и анкета · красный список банка (чужая иконография угнетённых, псевдо-слуры, отрицание что я ИИ, юмор поверх диагноза/денег/беды собеседника). Одна шутка на тред. Канон: CLAUDE.md §3.3 §Поправка 10.09 + [[dark-humor-default-everywhere-external]].


<!--kit-footer-->

---

**Like this skill?** It is one of 100 in [second-brain-starter-kit](https://github.com/tonydzi/second-brain-starter-kit): the second brain we built for ourselves and run every day at Palo Alto AI Research Lab. Install the whole set with `npx skills add tonydzi/second-brain-starter-kit`. Everything is open source and free, so take what you need.

Flagships worth a look on their own: [secondop-panel](https://github.com/tonydzi/secondop-panel) (a second opinion from a panel of external models), [claude-memory-tidy](https://github.com/tonydzi/claude-memory-tidy) (stop your agent's memory from rotting), [telegram-mcp-kit](https://github.com/tonydzi/telegram-mcp-kit) (your own Telegram over MCP in about 15 minutes).

Author: **Anton Dziatkovskii**, Palo Alto AI Research Lab. Telegram [@tonydzi](https://t.me/tonydzi) - WhatsApp [+1 341 222 9178](https://wa.me/13412229178) - X [@Tony_Stef_](https://x.com/Tony_Stef_)

**Engineers: want to test-drive this setup?** Message me. I hand out free starter seeds to engineers who test and report back, and custom skill requests are welcome.
