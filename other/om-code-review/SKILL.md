---
name: om-code-review
description: Repo-local extension of om-code-review for aitl-starter. Adds project rules from docs/ENGINEERING_STANDARDS.md (layering, coverage, no console, DB changes need integration tests) on top of the installed skill.
---

@../../../.claude/skills/om-code-review/SKILL.md

# aitl-starter: dodatkowe reguły review

Reguły poniżej rozszerzają skill bazowy. Przy konflikcie dotyczącym specyfiki repozytorium wygrywają te reguły. Reguł bezpieczeństwa i jakości skilla bazowego nie osłabiają.

## Dodatkowe sprawdzenia (każde naruszenie to co najmniej **major**)

1. **Kierunek zależności.** `apps/web` importuje `@aitl/core`, nigdy odwrotnie. `domain/` nie importuje z `application/` ani `infrastructure/`. `application/` zależy od interfejsów, nie od MikroORM.
2. **I/O w domenie.** W `packages/core/src/domain/` brak dostępu do bazy, sieci, systemu plików i `Date.now()` bez wstrzyknięcia. Jest to **blocker**.
3. **Pokrycie.** Nowy lub zmieniony kod w `domain/` i `application/` ma testy jednostkowe. Próg 100% jest wymuszony w `vitest.config.ts`. Obniżenie progu lub dodanie wykluczeń do `coverage.exclude` bez uzasadnienia w PR to **blocker**.
4. **Zmiany bazy.** Zmiana encji lub repozytorium w `infrastructure/` wymaga testu integracyjnego w `packages/core/test/`. Brak testu to **major**.
5. **Zakazane konstrukcje.** `console.*`, `any` bez komentarza z uzasadnieniem, `--no-verify`, wyłączenie reguły ESLint bez komentarza.
6. **Kontrakty.** Zmiany publicznych eksportów `@aitl/core` i tras `/api/*` sprawdź z `BACKWARD_COMPATIBILITY.md`. Usunięcie lub zmiana sygnatury bez okresu przejściowego to **blocker**.
7. **Wnioski.** Jeśli PR naprawia błąd lub zmienia nieoczywistą decyzję, a nie dopisuje wpisu do `.ai/lessons.md`, zgłoś **nit**.

## Format raportu (dodatek)

Na końcu raportu dodaj sekcję **"Zgodność z lokalnymi regułami"** z listą punktów 1-7 i wynikiem: OK / naruszenie (plik, linia).
