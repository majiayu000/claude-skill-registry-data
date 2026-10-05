---
name: verifica-prima-di-completare
description: Prima di dichiarare una task completata, fixata, funzionante o pronta per il deploy, esegui il comando di verifica e leggi l'output. Da usare quando stai per scrivere "fatto", "risolto", "funziona", "pronto", "deployato" o equivalenti. NON da usare per task di pura esplorazione/lettura senza modifiche.
---

# Verifica prima di completare

**Principio**: l'evidenza precede la dichiarazione di "fatto".

## La regola

Niente claim di completamento senza evidenza fresca dell'esecuzione.

Prima di scrivere "fatto / risolto / funziona / pronto":

1. **Identifica** il comando che prova la claim (test, build, lint, type-check, curl, navigazione browser)
2. **Esegui** il comando completo (non un subset, non da cache vecchia)
3. **Leggi** l'output integrale e l'exit code
4. **Conferma** che l'output corrisponda alla claim
5. **Solo allora** comunica il successo

## Red flag linguistici

Se stai per scrivere queste parole senza aver verificato, **fermati**:

- "dovrebbe funzionare"
- "probabilmente"
- "sembra funzionare"
- "il fix è semplice e non rompe nulla"
- "ho aggiornato X, ora dovrebbe andare"

Queste frasi indicano che stai per dichiarare done senza prova.

## Rationalizzazioni da bloccare

| Pensiero | Realtà |
|---|---|
| "Il lint passa, quindi funziona" | Linter ≠ compiler ≠ test ≠ runtime |
| "Il type-check passa, quindi funziona" | Compila ≠ funziona |
| "Il test unitario passa" | Test unit ≠ integrazione ≠ E2E |
| "L'agente ha detto che ha finito" | Richiede verifica indipendente |
| "L'ho già verificato 10 minuti fa" | Lo stato può essere cambiato — rifai |
| "Ho fretta" | Falsi positivi costano più tempo di una verifica |

## Casi specifici del workflow

- **Modifiche backend (Laravel/Node)**: esegui i test rilevanti + un curl reale o chiamata dell'endpoint
- **Modifiche frontend (Vue/React)**: build + caricamento pagina nel browser (non solo HMR)
- **Modifiche Flutter**: `flutter analyze` + build release per la piattaforma toccata
- **Modifiche Docker/Traefik**: `docker compose config` + `docker compose up` + curl al servizio esposto
- **Modifiche KB / project-memory**: rileggi il file dopo la scrittura, verifica frontmatter valido
- **Modifiche presentazioni didattiche**: build + apertura in browser, verifica che le slide non siano vuote o rotte
- **Commit/push**: dopo il push, verifica con `git log origin/<branch>` che il commit sia arrivato

## Eccezioni legittime

Non serve verifica per:
- Pura lettura/esplorazione senza modifiche
- Task esplicitamente di sola ricerca ("trovami dove sta X")
- Quando l'utente dice "non testare, voglio solo vedere il diff"

In tutti gli altri casi: **se hai modificato, verifica**.
