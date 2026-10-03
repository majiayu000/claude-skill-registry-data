---
name: sprint-planning
description: >
  Planowanie sprintu dla projektów Elixir/Phoenix z Ash Framework.
  Rozbija user stories na taski techniczne z estymacją story points.
user-invocable: true
---

# Sprint Planning — Ash/Phoenix

## Twoje zadanie

Pomagasz w planowaniu sprintu:
1. Analizujesz user stories
2. Rozbijasz je na taski techniczne (z uwzględnieniem Ash)
3. Estymujesz w story points

## Input

Użytkownik poda:
- User stories (format: "Jako X chcę Y, żeby Z")
- Opcjonalnie: velocity zespołu, długość sprintu

## Proces

### 1. Analiza User Story

Dla każdej story odpowiedz:
- Które **domeny Ash** są zaangażowane?
- Jakie **Resources** trzeba utworzyć/zmodyfikować?
- Jakie **Actions** (create/read/update/destroy/custom)?
- Czy potrzebne **Policies**?
- Czy jest **LiveView** UI?

### 2. Rozbicie na Taski Techniczne

Każdy task powinien być:
- **Atomowy** — można go zrobić niezależnie
- **Testowalny** — wiadomo kiedy jest "done"
- **Mały** — max 1-2 dni pracy

**Typowa struktura tasków dla Ash feature:**

```
□ [Backend] Utworzyć Resource <Name>
  - atrybuty, relacje, identities
  - mix ash.gen.resource + migracja

□ [Backend] Zdefiniować Actions dla <Name>
  - create/update z accept
  - custom actions jeśli potrzebne

□ [Backend] Dodać Policies dla <Name>
  - kto może read/create/update/destroy

□ [Backend] Napisać testy dla <Name>
  - actions, walidacje, policies

□ [Frontend] LiveView lista <Names>
  - stream, filtrowanie, paginacja

□ [Frontend] LiveView formularz <Name>
  - AshPhoenix.Form, walidacja

□ [Frontend] Routing + integracja
  - router.ex, nawigacja
```

### 3. Estymacja Story Points

Używaj skali Fibonacciego: **1, 2, 3, 5, 8, 13**

| SP | Znaczenie | Przykład Ash |
|----|-----------|--------------|
| 1 | Trywialne | Dodanie atrybutu do istniejącego Resource |
| 2 | Proste | Nowy prosty Resource (CRUD, brak relacji) |
| 3 | Standardowe | Resource z relacjami + podstawowe UI |
| 5 | Złożone | Feature z wieloma Resources + custom actions |
| 8 | Duże | Nowa domena, integracja zewnętrzna |
| 13 | Epik | Rozbij na mniejsze stories! |

**Czynniki zwiększające estymację:**
- +1 SP: Custom actions (nie tylko CRUD)
- +1 SP: Złożone policies (role-based)
- +1 SP: Real-time (PubSub, presence)
- +2 SP: Integracja zewnętrzna (API, webhook)
- +1 SP: Brak podobnego wzorca w projekcie

### 4. Output Format

```markdown
## Sprint X Planning

### User Story 1: [Tytuł]
> Jako [kto] chcę [co], żeby [po co]

**Zaangażowane domeny:** Companies, Drivers
**Estymacja:** 5 SP

#### Taski:
- [ ] [2 SP] Utworzyć Resource Driver z relacją do Company
- [ ] [1 SP] Dodać policies dla Driver (tylko właściciel firmy)
- [ ] [1 SP] Testy jednostkowe Driver
- [ ] [1 SP] LiveView lista kierowców z filtrem po firmie

---

### Podsumowanie sprintu
| Story | SP | Priorytet |
|-------|-----|-----------|
| User Story 1 | 5 | Must |
| User Story 2 | 3 | Should |
| **Razem** | **8** | |

Velocity zespołu: X SP
Capacity: OK / Przekroczone
```

## Zasady

- Pytaj jeśli story jest niejasna — lepiej dopytać niż zgadywać
- Sugeruj rozbicie jeśli story > 8 SP
- Uwzględniaj techniczny dług (testy, refaktoring)
- Pamiętaj o Definition of Done (testy, code review, dokumentacja)

## Przykład użycia

```
/sprint-planning

User stories na sprint 3:
1. Jako admin chcę dodawać firmy przewozowe, żeby mieć bazę klientów
2. Jako kierowca chcę widzieć moje zlecenia, żeby wiedzieć co mam robić
```
