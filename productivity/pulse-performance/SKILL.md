---
name: pulse-performance
description: Performance- und Ressourcenprüfung für Pulse – 768-MiB-Containerbudget (Warnung/Kritisch/Notfall 500/620/700 MB), begrenzte Caches/Queues, blockierende Aufrufe im Event-Loop, teure Dashboard-Seiten, SQLite-Abfragen, Scheduler und Discord-Rate-Limits. Verwenden bei langsamen Seiten, steigendem Speicher, neuen Hintergrundjobs/Caches oder vor Merge ressourcenrelevanter Änderungen.
argument-hint: [diff | Route/Modul | messen <route>]
disable-model-invocation: true
---

# Pulse-Performance

Bot und Webserver laufen im **selben Prozess und Event-Loop** – jede blockierende Arbeit im Dashboard verzögert den Bot und umgekehrt. Nur lokal messen (Preview-Server / TestClient), nie gegen den VPS lasten.

## 1. Statische Prüfung (Diff oder Bereich)
1. **Speicher (Regel 7):** Jede neue Sammlung, die mit Nutzern/Nachrichten/Zeit wächst, braucht eine Obergrenze (`deque(maxlen=…)`, LRU, Ablauf). Vorbild: begrenzter Rate-Limiter in `webserver.py` („full state rejects new keys“). Keine vollständigen Member-/Nachrichtenlisten im Speicher halten.
2. **Event-Loop:** Keine `time.sleep`, synchronen HTTP-Aufrufe, großen Datei-/Zip-/SQLite-Operationen direkt in `async def` – `asyncio.to_thread` nutzen. Discord-Fetches (`fetch_*`) statt Cache nur wo nötig.
3. **Scheduler:** Neue Hintergrundarbeit in vorhandene Loops/`pulse_jobs.tracked(...)` einhängen, Tasks über `pulse_tasks.spawn` (Fehler werden erfasst). Kein neuer Dauer-Loop pro Feature, `jitter` für Intervalle.
4. **Discord-Limits:** Massenaktionen (Rollen, Nicknames, Nachrichten) gedrosselt, 429/`retry_after` respektiert, kein endloses Retry.
5. **SQLite/JSON:** Keine N+1-Abfragen in Schleifen über Mitglieder; Indizes für neue Filterspalten (Migration in `pulse_migrations`); große JSON-Dateien nicht pro Request mehrfach laden.
5a. **Polling/Netzwerk:** Keine engen Polling-Schleifen (Dashboard-JS oder Bot); externe Aufrufe mit Timeout, Backoff und Ausfall-Fallback, kein Abruf pro Request, wenn ein Cache mit TTL reicht.
6. **Dashboard-Seiten:** HTML-Aufbau in Schleifen ohne wiederholte teure Lookups (`guild.get_member` vorab sammeln); Paginierung/Limit für Listen (Audit-Log, Tickets, Transkripte).

## 2. Messen (bei Bedarf)
- Gleichwertigkeit + Laufzeit: Muster aus `tests/test_performance.py` (Phase-3-Optimierungen müssen identische Ergebnisse liefern).
- Seitenzeit lokal: Preview-Server (`tools/preview_server.py`) starten und mit `httpx` mehrfach abrufen (Median/p95), oder `cProfile` um den Handler mit TestClient.
- Speicher: `tracemalloc` vor/nach N simulierten Ereignissen; Wachstum muss bei Obergrenze stagnieren. Produktionswert liefert `/healthz` (`memory_mb` via `pulse_ultimate.container_memory_mb`) – nur lesen.

## 3. Ergebnis (Deutsch)
Befunde mit `datei:zeile`, erwarteter Wirkung (z. B. „wächst pro Nachricht um ~1 KB ohne Grenze“), Messwerten vorher/nachher falls gemessen, und Test, der Obergrenze bzw. Ergebnisgleichheit absichert. Nichts als „schneller“ melden, was nicht gemessen wurde; Messwerte und Schätzungen getrennt ausweisen. Vorhandene Werkzeuge (`tracemalloc`, `cProfile`, `tests/test_performance.py`) vor neuen Abhängigkeiten nutzen; keine kostenpflichtige KI-API einführen.