---
name: krux-flow
description: Use when the user wants iterative one-step-at-a-time execution, approval before each move, no upfront plan. Triggers on "włącz flow", "wyłącz flow".
---

Tryb iteracyjny: zero planu z góry, jeden ruch na raz.

**Włącz:** `włącz flow`. **Wyłącz:** `wyłącz flow`. Hook przypomina przy `SessionStart`, nie na każdym prompcie.

1. Zaproponuj jeden najmniejszy ruch + powód. Zapytaj o zgodę.
2. Po `tak`/`rób`/`leć` — wykonaj tylko ten ruch.
3. Raport: `plik:linia — zmiana, status testu`.
4. Kolejny ruch z rezultatu, nie z góry ułożonej listy.
5. Blocker → 2-3 opcje + pytanie.
6. Cel osiągnięty → `Cel osiągnięty. N ruchów.`

Niezależne od persony i konkret — można łączyć.
