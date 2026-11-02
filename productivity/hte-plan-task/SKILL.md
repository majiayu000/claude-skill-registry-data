---
name: hte-plan-task
description: Plan scoped HatchTheEgg features or implementation stages with real dependencies and acceptance criteria. Use for task decomposition or planning, not isolated bug diagnosis.
---

# Planowanie zadania HatchTheEgg

Zaplanuj wyłącznie cel zlecony przez użytkownika. Rozpocznij od [kontekstu](../../../docs/WORKING_CONTEXT.md) i [specyfikacji](../../../docs/CURRENT_SPEC.md); z [mapy workflow](../../../docs/workflow/WORKFLOW.md) dobierz tylko źródła danego systemu.

## Procedura

1. Ustal oczekiwany rezultat, obecny stan i kryteria odbioru. Oddziel wykonanie, weryfikację i akceptację użytkownika. Nie otwieraj zakończonego zadania na podstawie starego raportu.
2. Podziel tylko rzeczywiście złożoną pracę na małe zadania: cel, dozwolone pliki, wyłączenia, konkretna zależność i sprawdzenie. Wspólny etap/reviewer nie jest zależnością; wskaż dokładny wymagany wynik innego zadania.
3. Sprawdź granicę odłożonego bilansu. Przygotowanie kontraktu lub testu nie pozwala zamienić proponowanych cen/szans w parametry gry. Nie blokuj niezależnego zakresu samym oczekiwaniem na bilans.
4. Potrzebne decyzje techniczne zapisz proporcjonalnie, korzystając z [ADR](../../../docs/ecc/adaptations/adr_template_and_guide.md). Nie wymagaj arbitralnej liczby ADR ani pytania o każdą nazwę modułu. Zmianę zatwierdzonego zachowania przedstaw jako osobną decyzję produktu.
5. Gdy zadanie obejmuje assety, sprawdź istniejące zasoby i koszt adaptacji kandydatów. Dla samej matematyki/zapisu pomiń research artystyczny.

## Wynik i granice

Jeśli zadanie obejmuje samouczek, uwzględnij odzyskanie postępu po utracie wymaganego zasobu, resecie lub ponownym wejściu. Uzupełnienie zasobu i cofnięcie do kroku pozyskania są możliwymi wzorcami do oceny, a nie zatwierdzonymi mechanikami HTE. Nie przyznawaj automatycznie darmowych zasobów i nie ustalaj ich ilości; rozwiązanie zmieniające ekonomię lub zatwierdzone zachowanie wymaga osobnego rozstrzygnięcia produktu, bez wznawiania bilansu w ramach planowania.

Użyj krótkiego [briefu](../../../docs/workflow/TASK_TEMPLATES.md). Wskaż prace gotowe do wykonania i konkretnie zależne. [Etapy](../../../docs/workflow/IMPLEMENTATION_STAGES.md) są mapą, nie automatycznym zleceniem ich realizacji. Przy zamykaniu etapu lub zadania uwzględnij aktualizację nagłówków dat/statusów w indeksach ([README](../../../docs/README.md), [CURRENT_SPEC](../../../docs/CURRENT_SPEC.md), [TODO](../../../docs/TODO.md), [WORKING_CONTEXT](../../../docs/WORKING_CONTEXT.md)), liczników otwartych/zamkniętych zadań w [backlogu 32](../../../docs/32_parallel_delivery_backlog.md) względem [rejestru GitHub](../../../docs/workflow/github_task_registry.json) oraz oczyszczenie tymczasowych skryptów z `build/` (samo dopisanie sekcji na końcu dokumentu bez korekty nagłówka z wcześniejszego etapu tworzy sprzeczność).

Planowanie nie uprawnia do implementacji, delegacji, instalacji narzędzi, publikacji lub mutacji GitHub. Nie wznawiaj bilansu, nie zmieniaj docs/17–21 i nie otwieraj ponownie zamkniętych ustaleń niezwiązanych z zadaniem.
